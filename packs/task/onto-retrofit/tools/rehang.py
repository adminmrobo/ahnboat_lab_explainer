#!/usr/bin/env python3
"""다시 걸기 (ai-lab-retrofit 15장) — 이미 꼬리표가 있는 페이지의 개념을 분야 뼈대 주제에 건다.

본문은 건드리지 않는다. 페이지의 kg-raw(원본)와 kg-ld(검색 엔진용) 두 블록만 고친다.
저장소마다 결정을 kg/rehang.json(덧씌우기 파일)에 남기므로, 빌드 스크립트로 페이지를 다시 만드는 저장소도
빌드 끝에 apply_overlay()를 부르면 같은 결과가 유지된다.

  python3 rehang.py plan  저장소폴더 --domains econ,math [--skill 스킬저장소] [--min 2]
        → 저장소폴더/kg/rehang.json 을 만든다 (자동 후보, 사람이 보고 지울 수 있다)
  python3 rehang.py apply 저장소폴더 [--skill 스킬저장소]
        → rehang.json 대로 모든 페이지의 kg-raw·kg-ld 를 고친다 (여러 번 돌려도 같은 결과)

덧씌우기 형식 kg/rehang.json:
  {"version":"1.0","made":"2026-11-24","via":"rehang-2026-11-24","domains":["econ","math"],
   "topics":{"lab:topic/consumer-choice":{"ko":..,"en":..,"domain":["econ"],"level":2}},
   "links":{"lab:concept/x":{"topic":"lab:topic/consumer-choice","score":3,"why":"이름 같음"}},
   "retag":{"from":["ai"],"to":["geom"]}}           # 선택: domain이 정확히 from인 노드를 to로
표준 라이브러리만 쓴다.
"""
import argparse, datetime as dt, glob, json, os, re, sys

VIA = 'rehang-2026-11-24'
KEEP = {'Concept', 'Method', 'Term', 'Theory', 'Metric', 'Distribution', 'Identity', 'Assumption', 'Indicator',
        'Framework', 'Definition', 'Theorem', 'Axiom', 'Structure', 'Estimator', 'Account', 'Standard', 'Task'}
BLOCK = r'(<script[^>]*\bid\s*=\s*["\']%s["\'][^>]*>)(.*?)(</script>)'
STOP = {'and', 'of', 'the', 'a', 'an', 'in', 'for', 'to', 'with', 'on', 'etc', 'its', 'as', 'by', 'vs'}


def nm(s):
    s = re.sub(r'\([^)]*\)', '', str(s or '')).lower()
    return re.sub(r"[\s·\-–—_,./'’\"“”:;!?∇()]+", '', s)


def words(s):
    return {w for w in re.findall(r'[a-z0-9]+', re.sub(r'\([^)]*\)', '', str(s or '')).lower()) if w not in STOP and len(w) > 1}


def load_backbones(skill):
    reg = json.load(open(os.path.join(skill, 'data', 'domains.json'), encoding='utf-8'))
    lens, owner = {}, {}
    for d in reg['domains']:
        for a in (d.get('backbone_areas') or []) + (d.get('backbone_areas_extra') or []):
            lens.setdefault(a, []).append(d['code'])
        if d.get('backbone') and not d.get('backbone_areas'):
            owner[d['backbone']] = d['code']
    T = {}
    for f, code in owner.items():
        bb = json.load(open(os.path.join(skill, f), encoding='utf-8'))
        up = {e['s']: e['o'] for e in bb['edges'] if e['p'] == 'lab:broader'}
        for n in bb['nodes']:
            if n['type'] != 'Topic':
                continue
            ds = [code] + [c for c in lens.get(up.get(n['id']), []) if c != code]
            T[n['id']] = {'ko': n['label']['ko'], 'en': n['label']['en'], 'domain': ds, 'level': n.get('level', 1),
                          'area': up.get(n['id'])}
    return {d['code']: d for d in reg['domains']}, T


def pages(repo):
    out = []
    for p in sorted(glob.glob(os.path.join(repo, '**', '*.html'), recursive=True)):
        rel = os.path.relpath(p, repo)
        if rel.split(os.sep)[0] in ('.git', 'node_modules', 'archive', 'old', 'backup'):
            continue
        h = open(p, encoding='utf-8').read()
        m = re.search(BLOCK % 'kg-raw', h, re.S)
        if m:
            try:
                out.append((p, h, json.loads(m.group(2).replace('<\\/', '</'))))
            except ValueError:
                print('kg-raw JSON 오류, 건너뜀:', rel, file=sys.stderr)
    return out


def score(n, t):
    ko, en = n['label'].get('ko', ''), n['label'].get('en', '')
    a, b = nm(ko), nm(t['ko'])
    if a and (a == b or nm(en) == nm(t['en'])):
        return 3, '이름 같음'
    if len(b) >= 3 and b in a and len(b) >= 0.5 * len(a):
        return 2, '주제 이름이 개념 이름에 들어 있음'
    if len(a) >= 3 and a in b and len(a) >= 0.6 * len(b):
        return 2, '개념 이름이 주제 이름에 들어 있음'
    tw, nw = words(t['en']), words(en)
    if tw and nw and len(tw) >= 2 and tw <= nw and len(tw) >= 0.6 * len(nw):
        return 2, '영어 이름 낱말이 모두 겹침'
    return 0, ''


def plan(a):
    DOM, T = load_backbones(a.skill)
    doms = [d for d in a.domains.split(',') if d]
    allow = set(doms) | {DOM[d].get('parent') for d in doms if d in DOM}
    cand = {k: v for k, v in T.items() if set(v['domain']) & allow}
    links, topics, seen = {}, {}, set()
    for p, h, kg in pages(a.repo):
        has = {e['s'] for e in kg.get('edges', []) if e.get('p') == 'lab:broader' and e.get('o', '').startswith('lab:topic/')}
        for n in kg.get('nodes', []):
            if n.get('type') not in KEEP or n['id'] in seen or n['id'] in has or not isinstance(n.get('label'), dict):
                continue
            seen.add(n['id'])
            best = None
            for tid, t in cand.items():
                s, why = score(n, t)
                if s >= a.min and (not best or (s, len(t['ko'])) > (best[0], len(T[best[1]]['ko']))):
                    best = (s, tid, why)
            if best:
                links[n['id']] = {'topic': best[1], 'score': best[0], 'why': best[2], 'ko': n['label'].get('ko', '')}
                t = T[best[1]]
                topics[best[1]] = {'ko': t['ko'], 'en': t['en'], 'domain': t['domain'], 'level': t['level']}
    ov = {'version': '1.0', 'made': dt.date.today().isoformat(), 'via': VIA, 'domains': doms,
          'note': '분야 뼈대 주제에 다시 걸기(ai-lab-retrofit 15장). links는 자동 후보이며 틀린 줄은 지우면 된다. 빌드 스크립트가 있는 저장소는 빌드 끝에 rehang.apply_overlay()가 이 파일을 적용한다.',
          'topics': dict(sorted(topics.items())), 'links': dict(sorted(links.items()))}
    if a.retag:
        rules = []
        for r in a.retag.split(';'):        # 여러 규칙: 'accounting:acct;accounting,coding:acct,data'
            f, t = r.split(':')
            rules.append({'from': [x for x in f.split(',') if x], 'to': [x for x in t.split(',') if x]})
        ov['retag'] = rules[0] if len(rules) == 1 else rules
    os.makedirs(os.path.join(a.repo, 'kg'), exist_ok=True)
    out = os.path.join(a.repo, 'kg', 'rehang.json')
    json.dump(ov, open(out, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print('%s: 개념 %d개를 주제 %d개에 걸 후보' % (out, len(links), len(topics)))
    for k, v in list(links.items())[:400]:
        print('  %-40s %s → %s (%s)' % (k, v['ko'], T[v['topic']]['ko'], v['why']))


def apply_overlay(G, ov):
    """kg-raw 그래프(dict)에 덧씌우기를 적용해 돌려준다. 여러 번 적용해도 같다."""
    nodes = {n['id']: n for n in G.get('nodes', [])}
    G['edges'] = [e for e in G.get('edges', []) if e.get('via') != VIA]
    G['nodes'] = [n for n in G.get('nodes', []) if n.get('via') != VIA]
    nodes = {n['id']: n for n in G['nodes']}
    for n in G['nodes']:                      # 옛 페이지: domain이 문자열("ai")인 경우 배열로
        if isinstance(n.get('domain'), str):
            n['domain'] = [n['domain']]
    rts = ov.get('retag') or []
    for rt in (rts if isinstance(rts, list) else [rts]):
        for n in G['nodes']:
            if n.get('type') in ('Area', 'Topic', 'Work', 'QuizItem'):
                continue
            if sorted(n.get('domain') or []) == sorted(rt['from']):
                n['domain'] = list(rt['to'])
    page = G.get('page')
    used = set()
    for nid, l in ov.get('links', {}).items():
        n = nodes.get(nid)
        t = ov['topics'].get(l['topic'])
        if not n or not t:
            continue
        dm = n.get('domain') if isinstance(n.get('domain'), list) else []
        for c in t['domain'][:1]:
            if c not in dm:
                dm = dm + [c]
        n['domain'] = dm
        G['edges'].append({'s': nid, 'p': 'lab:broader', 'o': l['topic'], 'anchor': n.get('anchor', ''),
                           'confidence': 'mid' if l.get('score', 2) < 3 else 'high', 'via': VIA})
        used.add(l['topic'])
    for tid in sorted(used):
        t = ov['topics'][tid]
        G['nodes'].append({'id': tid, 'type': 'Topic', 'label': {'ko': t['ko'], 'en': t['en']}, 'page': page,
                           'anchor': '#kg', 'domain': t['domain'][:1], 'status': 'known', 'confidence': 'high',
                           'level': t.get('level', 1), 'via': VIA})
    return G


def patch_ld(ld, G):
    """kg-ld(@graph)에 다시 걸기 결과만 더한다: 주제 노드와 skos:broader. 다른 항목은 그대로 둔다."""
    if not isinstance(ld, dict) or not isinstance(ld.get('@graph'), list):
        return ld
    g = [o for o in ld['@graph'] if not (isinstance(o, dict) and o.get('lab:via') == VIA)]
    for o in g:
        if isinstance(o, dict) and isinstance(o.get('skos:broader'), list):
            o['skos:broader'] = [x for x in o['skos:broader'] if not (isinstance(x, dict) and x.get('lab:via') == VIA)]
            if not o['skos:broader']:
                del o['skos:broader']
    by = {o.get('@id'): o for o in g if isinstance(o, dict)}
    for e in G['edges']:
        if e.get('via') == VIA and e['s'] in by:
            by[e['s']].setdefault('skos:broader', []).append({'@id': e['o'], 'lab:via': VIA})
    for n in G['nodes']:
        if n.get('via') == VIA:
            g.append({'@id': n['id'], '@type': ['skos:Concept', 'lab:Topic'], 'lab:via': VIA,
                      'skos:prefLabel': [{'@value': n['label']['ko'], '@language': 'ko'}, {'@value': n['label']['en'], '@language': 'en'}]})
    ld['@graph'] = g
    return ld


def dump(o, like):
    """원래 블록의 모양(들여쓰기 여부, </ 처리)을 따라 쓴다."""
    s = json.dumps(o, ensure_ascii=False, indent=1 if '\n' in like.strip() else None)
    return s.replace('</', '<\\/') if '<\\/' in like else s


def apply_html(h, ov):
    m = re.search(BLOCK % 'kg-raw', h, re.S)
    if not m:
        return h, 0
    G = json.loads(m.group(2).replace('<\\/', '</'))
    G = apply_overlay(G, ov)
    n = sum(1 for e in G['edges'] if e.get('via') == VIA)
    h = h[:m.start(2)] + dump(G, m.group(2)) + h[m.end(2):]
    m2 = re.search(BLOCK % 'kg-ld', h, re.S)
    if m2:
        try:
            ld = json.loads(m2.group(2).replace('<\\/', '</'))
            h = h[:m2.start(2)] + dump(patch_ld(ld, G), m2.group(2)) + h[m2.end(2):]
        except ValueError:
            pass
    return h, n


def body_of(h):
    for i in ('kg-raw', 'kg-ld'):
        h = re.sub(BLOCK % i, r'\1\3', h, flags=re.S)
    return h


def apply(a):
    ov = json.load(open(os.path.join(a.repo, 'kg', 'rehang.json'), encoding='utf-8'))
    tot = files = 0
    for p, h, _ in pages(a.repo):
        new, n = apply_html(h, ov)
        if body_of(new) != body_of(h):
            sys.exit('본문이 바뀜 (멈춤): %s' % p)
        if new != h:
            open(p, 'w', encoding='utf-8').write(new)
            files += 1
        tot += n
    print('적용: 페이지 %d개 바뀜, 걸린 관계 %d개' % (files, tot))


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('cmd', choices=['plan', 'apply'])
    ap.add_argument('repo')
    ap.add_argument('--domains', default='')
    ap.add_argument('--retag', help='예: ai:geom — domain이 정확히 ["ai"]인 노드를 ["geom"]으로. 여러 규칙은 ;로')
    ap.add_argument('--skill', default=os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', '..'))
    ap.add_argument('--min', type=int, default=2)
    a = ap.parse_args()
    plan(a) if a.cmd == 'plan' else apply(a)
