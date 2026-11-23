#!/usr/bin/env python3
"""개조 결과 점검. 원본과 결과를 비교해 본문이 그대로인지, 데이터가 규칙에 맞는지 본다.

사용: python3 check.py 원본.html 결과.html [--backbone backbone.json] [--registry KG_00_registry.json] [--report check_report.md]
끝 상태: 오류가 있으면 1, 경고만 있으면 0.
"""
import argparse, json, re, sys
from retrofit import strip_marked

TYPES = {'Concept', 'Method', 'BioAnalogue', 'Claim', 'Question', 'Limitation', 'Task', 'Metric', 'Dataset', 'Simulation',
         'QuizItem', 'Work', 'Analogy', 'Term', 'Area', 'Topic',
         # v1.3 (ai-lab-explainer v1.8~): 통계·경제·회계·경영 분야 클래스
         'Theory', 'Assumption', 'Identity', 'Standard', 'Account', 'Indicator', 'Distribution', 'Framework'}
DOMAINS = {'ai', 'stats', 'econ', 'acct', 'biz'}
PRED = {'prerequisiteOf', 'hasLimitation', 'addressedBy', 'partOf', 'bioAnalogueOf', 'contrastsWith', 'supports', 'assertedIn',
        'evaluatedBy', 'evaluatedOn', 'demonstratedBy', 'raises', 'relatedTo', 'solves', 'analogyOf', 'assesses', 'broader',
        'explainedIn', 'inspiredBy',
        'assumes', 'derivedFrom', 'governedBy', 'supersededBy', 'measuredBy', 'appliesIn'}


def block(h, i):
    m = re.search(r'<script[^>]*id="%s"[^>]*>(.*?)</script>' % i, h, re.S)
    return json.loads(m.group(1)) if m else None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('orig'); ap.add_argument('new'); ap.add_argument('--backbone'); ap.add_argument('--registry')
    ap.add_argument('--report', default='check_report.md')
    a = ap.parse_args()
    O = open(a.orig, encoding='utf-8').read(); N = open(a.new, encoding='utf-8').read()
    err, warn, ok = [], [], []

    # 1. 본문 그대로인가
    if strip_marked(O, True) == strip_marked(N, True):
        ok.append('본문 차이 0 (lab-kg·lab-cover 표시 밖은 원본과 같음)')
    else:
        x, y = strip_marked(O, True), strip_marked(N, True)
        k = next((i for i in range(min(len(x), len(y))) if x[i] != y[i]), min(len(x), len(y)))
        err.append('본문이 바뀜: %d번째 글자부터 다름 → 원본 "%s" / 결과 "%s"' % (k, x[k:k + 60].replace('\n', '⏎'), y[k:k + 60].replace('\n', '⏎')))

    # 2. 데이터 블록
    try:
        kg, refs, meta = block(N, 'kg-raw'), block(N, 'refs-csl'), block(N, 'page-meta')
    except Exception as e:
        err.append('데이터 블록 JSON 오류: %s' % e); kg = refs = meta = None
    if not kg or refs is None or not meta:
        err.append('kg-raw · refs-csl · page-meta 중 빠진 것이 있음')
        return finish(a, err, warn, ok)
    try:
        if block(N, 'kg-ld') is None:
            warn.append('kg-ld 없음 (node 없이 조립함). 꾸러미 내려받기에서는 만들어지지만 검색 엔진용 블록은 없음')
    except Exception as e:
        err.append('kg-ld JSON 오류: %s' % e)

    nodes = {n['id']: n for n in kg['nodes']}
    if len(nodes) != len(kg['nodes']): err.append('같은 id 노드가 두 번 있음')
    ids_in_page = set(re.findall(r'\sid="([^"]+)"', strip_marked(O)))
    bb = json.load(open(a.backbone, encoding='utf-8')) if a.backbone else None
    bbid = {n['id'] for n in bb['nodes']} if bb else set()

    for n in kg['nodes']:
        if n.get('type') not in TYPES: err.append('모르는 종류 %s: %s' % (n.get('type'), n['id']))
        if n.get('coverage') not in ('explained', 'mentioned', None): err.append('coverage 값 오류: %s' % n['id'])
        if n.get('type') not in ('Area', 'Topic', 'Work', 'QuizItem'):
            dm = n.get('domain')
            if not dm: warn.append('domain 없음 (v1.3부터 권장, 옛 페이지는 ["ai"]): %s' % n['id'])
            elif not isinstance(dm, list): err.append('domain은 배열이어야 함: %s' % n['id'])
            else:
                for d in dm:
                    if d not in DOMAINS and not re.match(r'^[a-z]{2,12}$', d): err.append('domain 값 오류 %s: %s' % (d, n['id']))
        if n.get('type') == 'Standard' and not (n.get('asOf') and n.get('jurisdiction')): warn.append('Standard에 asOf·jurisdiction 없음: %s' % n['id'])
        an = (n.get('anchor') or '').lstrip('#')
        if an and an not in ids_in_page and an not in ('kg', 'export'): err.append('본문에 없는 anchor #%s: %s' % (an, n['id']))
        for m in n.get('match') or []:
            if not m.get('verified') and m.get('id'): err.append('확인 안 된 외부 대응에 ID가 들어 있음: %s' % n['id'])
    deg = {k: 0 for k in nodes}
    rel = 0
    for e in kg['edges']:
        p = e['p'].replace('lab:', '')
        if p not in PRED: warn.append('핵심 어휘 밖 관계 %s (%s → %s)' % (e['p'], e['s'], e['o']))
        if p == 'relatedTo': rel += 1
        for end in (e['s'], e['o']):
            if end in nodes: deg[end] += 1
            elif not (end in bbid or end.startswith('lab:topic/') or end.startswith('lab:area/')):
                err.append('끊긴 관계: %s 없음 (%s %s %s)' % (end, e['s'], e['p'], e['o']))
            elif bb and end not in bbid:
                err.append('뼈대에 없는 주제: %s' % end)
    iso = [k for k, v in deg.items() if v == 0]
    if iso: err.append('고립 노드 %d개: %s' % (len(iso), ', '.join(iso[:8])))
    if kg['edges'] and rel / len(kg['edges']) > 0.15: warn.append('relatedTo 비율 %.0f%% (기준 15%% 이하)' % (100 * rel / len(kg['edges'])))

    br = [e for e in kg['edges'] if e['p'] == 'lab:broader' and re.match(r'lab:topic/', e['o'])]
    hung = {e['s'] for e in br}
    content = [k for k, n in nodes.items() if n['type'] in ('Concept', 'Method', 'BioAnalogue', 'Term', 'Limitation')]
    miss = [k for k in content if k not in hung]
    if miss: warn.append('뼈대 주제에 안 걸린 개념·방법 %d개 (retrofit_log의 "뼈대 밖 항목"에 적었는지 확인): %s' % (len(miss), ', '.join(miss[:8])))
    many = [k for k in hung if sum(1 for e in br if e['s'] == k) > 2]
    if many: warn.append('뼈대 주제 3개 이상에 걸린 항목: %s' % ', '.join(many[:8]))

    # 3. 문헌: 페이지에 없는 DOI·쪽수를 넣지 않았나
    rid = {r['id'] for r in refs}
    text = strip_marked(O)
    for r in refs:
        if r.get('DOI') and r['DOI'].lower() not in text.lower():
            warn.append('원본 페이지에 없는 DOI %s (%s): 확인 단계(P7)에서 찾은 것이면 verified에 근거를 적을 것' % (r['DOI'], r['id']))
        if r.get('page') and str(r['page']) not in text:
            warn.append('원본 페이지에 없는 쪽수 %s (%s)' % (r['page'], r['id']))
        if not (r.get('lab') or {}).get('verified'):
            warn.append('verified 표시가 없음: %s' % r['id'])
    for n in kg['nodes']:
        for s in n.get('source') or []:
            if s.get('ref') not in rid: err.append('참고문헌에 없는 출처 %s: %s' % (s.get('ref'), n['id']))

    # 4. 상태 3이 될 근거
    sup = {e['o'] for e in kg['edges'] if e['p'] == 'lab:supports' and nodes.get(e['s'], {}).get('source')}
    exp = [k for k in hung if nodes[k].get('coverage') == 'explained']
    ok.append('explained 항목 %d개 중 출처 있는 주장이 받치는 것 %d개' % (len(exp), len([k for k in exp if k in sup])))

    # 5. 등록부 ID 충돌
    if a.registry:
        reg = {x['id']: x for x in json.load(open(a.registry, encoding='utf-8'))['entries']}
        for k, n in nodes.items():
            r = reg.get(k)
            if r and not k.startswith('lab:work/') and r.get('label_ko') and n.get('label', {}).get('ko') != r['label_ko']:
                warn.append('등록부와 이름이 다름: %s (등록부 "%s" / 페이지 "%s")' % (k, r['label_ko'], n['label'].get('ko')))
        new = [k for k in nodes if k not in reg and not k.startswith(('lab:quiz/', 'lab:claim/', 'lab:sim/'))]
        ok.append('등록부에 새로 넣을 ID %d개' % len(new))

    # 6. 페이지 정보
    for f in ('title', 'number', 'date', 'version'):
        if not meta.get(f): err.append('page-meta에 %s 없음' % f)
    if not any(c.get('name') for c in meta.get('creator') or []): warn.append('저자 이름이 비어 있음 (사용자가 준 값만 넣는다)')
    if not meta.get('license'): warn.append('라이선스가 비어 있음 (사용자가 준 값만 넣는다)')
    if re.search(r'아무도 손대지|미개척|세계 최초', N): err.append('금지 표현 발견 (아무도 손대지/미개척/세계 최초)')
    added = ''.join(re.findall(r'<!-- lab-kg:(?:body|script) -->(.*?)<!-- /lab-kg:', N, re.S))
    if re.search(r'localStorage|sessionStorage|indexedDB', added): err.append('덧붙인 부분에서 브라우저 저장소 사용')
    ok.append('노드 %d · 관계 %d · 문헌 %d' % (len(nodes), len(kg['edges']), len(refs)))
    return finish(a, err, warn, ok)


def finish(a, err, warn, ok):
    L = ['# 개조 점검 보고서', '', '- 원본: %s' % a.orig, '- 결과: %s' % a.new, '',
         '## 오류 %d' % len(err)] + ['- ' + x for x in err] + ['', '## 경고 %d' % len(warn)] + ['- ' + x for x in warn] + \
        ['', '## 확인됨'] + ['- ' + x for x in ok]
    open(a.report, 'w', encoding='utf-8').write('\n'.join(L) + '\n')
    print('\n'.join(L))
    sys.exit(1 if err else 0)


if __name__ == '__main__':
    main()
