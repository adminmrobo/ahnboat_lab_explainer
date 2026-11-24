#!/usr/bin/env python3
"""꼬리표 초안 자동 만들기 (ai-lab-retrofit R1·R2 보조) — 지식 색인이 없는 저장소용.

페이지 본문을 읽어, 사이트에 이미 있는 개념(지식 노드 지도 ontology.json)과 분야 뼈대 주제의 이름이
나오는 곳을 찾아 kg.json·meta.json·refs.json 초안을 만들고 retrofit.py로 덧붙인다. 본문은 건드리지 않는다.
- 같은 개념은 사이트에 이미 있는 ID를 그대로 쓴다(시리즈 사이 연결).
- 뼈대 주제에 broader로 걸고, 다른 페이지에서 이미 확인된 개념 사이 관계는 confidence medium으로 옮긴다.
- 결과는 저장소 kg/pages/ 아래에 페이지별 JSON으로 남고, kg/reapply.py로 언제든 다시 덧붙일 수 있다
  (빌드 스크립트가 페이지를 다시 만드는 저장소는 빌드 끝에서 부른다).

  python3 autokg.py 저장소폴더 --repo 저장소이름 --series "콘텐츠 제목" --domains ml,dl \
      --onto ontology.json --skill 스킬저장소 --pages-url https://adminmrobo.github.io/저장소/ [--max 30]
"""
import argparse, datetime as dt, glob, html as H, json, os, re, shutil, subprocess, sys
from bs4 import BeautifulSoup, NavigableString, Tag

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
LANG_DIR = re.compile(r'(^|/)(en|zh|ja|uz|ru|vi|ko|i18n|lang|archive|old|backup|_drafts?|node_modules|\.git|build|tools|templates?|assets)(/|$)|\.src\.html$|template\.html$', re.I)
LANG_SUF = re.compile(r'[._-](en|zh|ja|uz|ru|vi)\.html?$', re.I)
GENERIC = set('''데이터 모델 학습 결과 방법 문제 값 입력 출력 예측 정답 분석 정보 변수 함수 시스템 구조 과정 그림 기호 단계 사례 질문 목표 개념 이론 기준 정의 평가 성능
문제점 원리 특징 이유 비교 선택 처리 계산 확률 오차 비용 규칙 패턴 예시 실험 테스트 코드 파이썬 수식 공식 그래프 표 차트 크기 방향 공간 시간 거리 속도 점 선 면
가중치 층 노드 신호 이미지 텍스트 단어 문장 사람 사용자 연구 기술 도구 연구실 이야기 박사 조수 하루 초파리 주판봇 시아 모아 인공지능 AI 머신러닝 딥러닝 신경망
걸음 저장소 화면 버튼 페이지 장면 그림판 연습 실습 퀴즈 정리 요약 소개 목차 시작 다음 이전 처음 마지막 오늘 내일 하나 둘 셋
data model learning result method value input output prediction analysis information variable function system structure process step example code python formula graph table chart'''.split())


AI_SET = {'ai', 'ml', 'dl', 'neuro', 'rl', 'genai', 'llm'}
NEAR = {'math', 'stats', 'data'}


def allowed_domains(doms):
    a = set(doms) | NEAR
    if a & AI_SET:
        a |= AI_SET
    if a & {'econ', 'fin', 'biz', 'acct'}:
        a |= {'econ', 'fin', 'biz', 'acct'}
    return a


def nm(s):
    s = re.sub(r'\([^)]*\)', '', str(s or '')).lower()
    return re.sub(r"[\s·\-–—_,./'’\"“”:;!?()]+", '', s)


GEN_N = set()


def base_pages(repo):
    out = []
    for p in sorted(glob.glob(os.path.join(repo, '**', '*.html'), recursive=True)):
        rel = os.path.relpath(p, repo).replace(os.sep, '/')
        if LANG_DIR.search('/' + rel) or LANG_SUF.search(rel):
            continue
        t = open(p, encoding='utf-8', errors='replace').read()
        if not re.search(r'<html|<!doctype', t[:4096], re.I):
            continue
        if re.search(r'http-equiv\s*=\s*["\']?refresh', t[:4096], re.I) and len(t) < 6000:
            continue
        out.append((rel, p, t))
    return out


def lexicon(onto, skill):
    """이름 → 후보. 사이트 개념(같은 ID 재사용)과 뼈대 주제."""
    import rehang
    DOM, T = rehang.load_backbones(skill)
    node = {n['id']: n for n in onto['nodes']}
    lex = {}
    def add(name, ent):
        k = nm(name)
        if len(k) < 2 or name.strip() in GENERIC or k in GEN_N:
            return
        if re.fullmatch(r'[a-z0-9]+', k) and len(k) < 3:
            return
        lex.setdefault(k, []).append(ent)
    for n in onto['nodes']:
        e = {'id': n['id'], 't': n['t'], 'ko': n['ko'], 'en': n.get('en') or n['ko'], 'def': n.get('def'),
             'tp': n.get('tp', []), 'd': n.get('d', []), 'n': len(n.get('p', []))}
        add(n['ko'], e)
        if n.get('en'):
            add(n['en'], e)
    for tid, t in T.items():
        e = {'id': None, 'topic': tid, 't': 'Concept', 'ko': t['ko'], 'en': t['en'], 'def': None, 'tp': [tid],
             'd': t['domain'][:1], 'n': 0, 'level': t['level']}
        add(t['ko'], e)
        add(t['en'], e)
    return lex, T, node


STR_RE = re.compile(r'"((?:[^"\\\n]|\\.){2,400})"\s*([:,\]}])')
HANGUL = re.compile('[가-힣]')


def script_segments(soup):
    """본문이 스크립트 안 데이터(JSON)에 들어 있는 페이지: 한글이 든 문자열을 글로 쓴다. 제목 성격 키는 강조."""
    out = []
    for sc in soup.find_all('script'):
        t = sc.get_text()
        if len(t) < 5000 or len(HANGUL.findall(t)) < 500:
            continue
        prev_key = None
        for m in STR_RE.finditer(t):
            try:
                v = json.loads('"%s"' % m.group(1))
            except ValueError:
                continue
            if m.group(2) == ':':
                prev_key = v
                continue
            if not HANGUL.search(v):
                continue
            emph = 1 if prev_key in ('title', 'ch', 'q', 'name', 'heading', 'cmd', 'term', 'label') else 0
            out.append((None, re.sub(r'<[^>]+>', ' ', v), emph))
    return out


def segments(soup, scripts=False):
    """문서 순서대로 (앵커, 글, 강조 여부)."""
    extra = script_segments(soup) if scripts else []
    body = soup.body or soup
    for s in body.find_all(['script', 'style', 'noscript', 'svg', 'template']):
        s.decompose()
    for s in body.select('#kg, #export, [data-lab-kg]'):
        s.decompose()
    out, anchor = [], None
    BLOCK = {'section', 'article', 'div', 'h1', 'h2', 'h3', 'h4', 'h5', 'details', 'aside', 'figure', 'li', 'p', 'table', 'main', 'header'}
    for el in body.descendants:
        if isinstance(el, Tag) and el.get('id') and el.name in BLOCK:
            anchor = el['id']
        elif isinstance(el, NavigableString) and el.strip():
            par = el.parent
            emph = 2 if any(a.name in ('h1', 'h2', 'h3', 'h4') for a in [par] + list(par.parents)[:3] if isinstance(a, Tag)) else \
                (1 if any(a.name in ('strong', 'b', 'dfn', 'em', 'mark', 'th') for a in [par] + list(par.parents)[:2] if isinstance(a, Tag)) else 0)
            out.append((anchor, str(el), emph))
    return out + extra


def find_terms(segs, lex, maxn):
    text_all = ' '.join(s[1] for s in segs)
    hits = {}
    full = nm(text_all)
    keys_ko = [k for k in lex if not re.fullmatch(r'[a-z0-9]+', k) and k in full]
    keys_en = [k for k in lex if re.fullmatch(r'[a-z0-9]+', k) and k in full]
    for a, t, emph in segs:
        tn = nm(t)
        if not tn:
            continue
        for k in keys_ko:
            if k in tn:
                h = hits.setdefault(k, {'cnt': 0, 'emph': 0, 'anchor': None, 'first': None})
                c = tn.count(k)
                h['cnt'] += c
                h['emph'] = max(h['emph'], emph)
                if h['first'] is None:
                    h['first'] = a
                if emph and h['anchor'] is None:
                    h['anchor'] = a
        low = ' ' + re.sub(r'[^a-z0-9]+', ' ', t.lower()) + ' '
        for k in keys_en:
            # 영어 이름은 원래 낱말 경계로 (예: "relu", "gradientdescent" → "gradient descent")
            ent = lex[k][0]
            raw = re.sub(r'\([^)]*\)', '', ent['en'] if nm(ent['en']) == k else ent['ko']).lower()
            pat = ' ' + re.sub(r'[^a-z0-9]+', ' ', raw).strip() + ' '
            if len(pat.strip()) < 3 or pat not in low:
                continue
            h = hits.setdefault(k, {'cnt': 0, 'emph': 0, 'anchor': None, 'first': None})
            h['cnt'] += low.count(pat)
            h['emph'] = max(h['emph'], emph)
            if h['first'] is None:
                h['first'] = a
            if emph and h['anchor'] is None:
                h['anchor'] = a
    # 더 긴 이름 안에만 나오는 짧은 이름은 뺀다 ('회귀' ⊂ '로지스틱회귀')
    ks = sorted(hits, key=len, reverse=True)
    for i, k in enumerate(ks):
        inner = sum(hits[j]['cnt'] * j.count(k) for j in ks[:i] if k in j and j != k)
        hits[k]['own'] = hits[k]['cnt'] - inner
    keep = []
    for k, h in hits.items():
        if h['own'] <= 0:
            continue
        sc = h['own'] + 3 * (h['emph'] == 2) + 1.5 * (h['emph'] == 1)
        if h['own'] >= 2 or h['emph']:
            keep.append((sc, k, h))
    keep.sort(key=lambda x: (-x[0], x[1]))
    return keep[:maxn]


def pick_entity(cands, domains):
    """같은 이름의 후보 가운데: 분야가 맞는 사이트 개념 → 여러 페이지에 나온 것 → 뼈대 주제."""
    def key(e):
        return (bool(set(e['d']) & set(domains)), e['id'] is not None, e['n'])
    return max(cands, key=key)


def slug(s):
    s = re.sub(r'\([^)]*\)', '', s).lower()
    s = re.sub(r'[^a-z0-9]+', '-', s).strip('-')
    return s[:60] or 'x'


def make_kg(rel, text, ctx, num=1):
    soup = BeautifulSoup(text, 'html.parser')
    title = H.unescape(re.sub(r'\s+', ' ', (soup.title.string if soup.title and soup.title.string else '') or '').strip())
    segs = segments(soup, ctx.get('scripts'))
    page = re.sub(r'\.html?$', '', rel).replace('/', '__')
    hits = find_terms(segs, ctx['lex'], ctx['max'])
    ids_in_page = set(re.findall(r'\bid\s*=\s*["\']([^"\']+)["\']', text))
    nodes, edges, seen = {}, [], {}
    allow = allowed_domains(ctx['domains'])
    for sc, k, h in hits:
        cands = [c for c in ctx['lex'][k] if set(c['d'] or []) & allow]
        if len(k) <= 2:
            cands = [c for c in cands if set(c['d'] or []) & set(ctx['domains'])]
        if not cands:
            continue
        e = pick_entity(cands, ctx['domains'])
        nid = e['id'] or 'lab:concept/' + (e['topic'].split('/', 1)[1] if e.get('topic') else slug(e['en']))
        if nid in nodes:
            continue
        anc = h['anchor'] or h['first']
        anc = '#' + anc if anc and anc in ids_in_page else '#kg'
        typ = e['t'] if e['t'] not in ('Topic', 'Area') else 'Concept'
        dm = [d for d in (e['d'] or [])] or ctx['domains'][:1]
        for d in ctx['domains'][:1]:
            if d not in dm:
                dm = [d] + dm
        n = {'id': nid, 'type': typ, 'label': {'ko': e['ko'], 'en': e['en']}, 'page': page, 'anchor': anc,
             'level': e.get('level', 2), 'status': 'known', 'confidence': 'medium',
             'coverage': 'explained' if (h['emph'] or h['own'] >= 3) else 'mentioned',
             'domain': dm[:3], 'match': [], 'auto': 'autokg-2026-11-24'}
        if e.get('def'):
            n['definition'] = {'ko': e['def']}
        nodes[nid] = n
        seen[nid] = e
    # 뼈대 주제에 걸기
    topics = {}
    for nid, e in seen.items():
        for t in [x for x in (e.get('tp') or []) if x in ctx['T']][:1]:
            if t == nid:
                continue
            topics[t] = 1
            edges.append({'s': nid, 'p': 'lab:broader', 'o': t, 'anchor': nodes[nid]['anchor'], 'confidence': 'medium'})
    for t in topics:
        tt = ctx['T'][t]
        nodes[t] = {'id': t, 'type': 'Topic', 'label': {'ko': tt['ko'], 'en': tt['en']}, 'page': page, 'anchor': '#kg',
                    'level': tt['level'], 'status': 'known', 'confidence': 'high', 'coverage': 'mentioned',
                    'domain': tt['domain'][:1], 'match': []}
    # 다른 페이지에서 확인된 관계 옮기기 (두 끝이 모두 이 페이지에 있을 때)
    ids = set(nodes)
    for s, o, p in ctx['onto_edges']:
        if s in ids and o in ids and s != o and p != 'broader':
            edges.append({'s': s, 'p': 'lab:' + p, 'o': o, 'anchor': nodes[s]['anchor'], 'confidence': 'medium',
                          'note': '다른 해설 페이지에서 확인된 관계'})
    # 관계가 하나도 없는 노드는 뺀다 (이름만 스친 약한 짝일 가능성이 크다)
    while True:
        used = {e['s'] for e in edges} | {e['o'] for e in edges}
        lone = [i for i in nodes if i not in used]
        if not lone:
            break
        for i in lone:
            del nodes[i]
        edges = [e for e in edges if e['s'] in nodes and e['o'] in nodes]
    kg = {'version': '1.0', 'page': page, 'nodes': list(nodes.values()), 'edges': edges}
    about = [n['id'] for n in list(nodes.values())[:5] if n['type'] != 'Topic']
    meta = {'title': title or ctx['series'], 'number': '%02d' % num, 'series': ctx['series'], 'date': ctx['date'], 'version': '1.1',
            'creator': [{'name': '안상선', 'role': 'author'}], 'contributor': [{'name': 'AI 보조 제작', 'role': 'assistant'}],
            'about': about, 'basedOn': [], 'educationalLevel': '입문~중급', 'license': '',
            'url': ctx['pages_url'] + rel, 'registry': 'KG_00_registry 0.3', 'seeAlso': '',
            'suggestedCitation': '안상선 (%s). %s. %s, v1.1.' % (ctx['date'][:4], title or ctx['series'], ctx['series'])}
    return kg, meta, len([n for n in nodes.values() if n['type'] != 'Topic'])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('repo')
    ap.add_argument('--repo-name', required=True)
    ap.add_argument('--series', required=True)
    ap.add_argument('--domains', required=True)
    ap.add_argument('--onto', required=True)
    ap.add_argument('--skill', default=os.path.join(HERE, '..', '..', '..', '..'))
    ap.add_argument('--pages-url', required=True)
    ap.add_argument('--max', type=int, default=30)
    ap.add_argument('--min', type=int, default=3, help='개념이 이보다 적은 페이지는 꼬리표를 달지 않음')
    ap.add_argument('--dry', action='store_true')
    ap.add_argument('--scripts', action='store_true', help='본문이 스크립트 안 데이터(JSON)에 있는 페이지')
    a = ap.parse_args()
    onto = json.load(open(a.onto, encoding='utf-8'))
    GEN_N.update(nm(g) for g in GENERIC)
    lex, T, node = lexicon(onto, a.skill)
    ctx = {'lex': lex, 'T': T, 'domains': a.domains.split(','), 'max': a.max, 'series': a.series,
           'date': dt.date.today().isoformat(), 'pages_url': a.pages_url.rstrip('/') + '/',
           'onto_edges': [tuple(e[:3]) for e in onto['edges']], 'scripts': a.scripts}
    kd = os.path.join(a.repo, 'kg')
    os.makedirs(os.path.join(kd, 'pages'), exist_ok=True)
    if not a.dry:
        for f in ('retrofit.py', 'kgx.js'):
            shutil.copy(os.path.join(HERE, f), os.path.join(kd, f))
        shutil.copy(os.path.join(HERE, 'autokg_reapply.py'), os.path.join(kd, 'reapply.py'))
    done = []
    num = 0
    for rel, path, text in base_pages(a.repo):
        if rel.startswith('kg/'):
            continue
        if re.search(r'<script[^>]*id=["\']kg-raw', text):
            continue   # 이미 꼬리표가 있음
        num += 1
        kg, meta, n = make_kg(rel, text, ctx, num)
        if n < a.min:
            print('  건너뜀(개념 %d): %s' % (n, rel))
            continue
        base = os.path.join(kd, 'pages', rel.replace('/', '__'))
        for suf, o in (('.kg.json', kg), ('.meta.json', meta), ('.refs.json', [])):
            json.dump(o, open(base + suf, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
        done.append((rel, n, len(kg['edges'])))
        print('  %-50s 개념 %3d · 관계 %3d' % (rel[:50], n, len(kg['edges'])))
    if not a.dry and done:
        r = subprocess.run([sys.executable, os.path.join(kd, 'reapply.py'), a.repo], capture_output=True, text=True)
        print(r.stdout[-600:], r.stderr[-600:])
    print('%s: 페이지 %d · 개념 %d · 관계 %d' % (a.repo_name, len(done), sum(d[1] for d in done), sum(d[2] for d in done)))


if __name__ == '__main__':
    main()
