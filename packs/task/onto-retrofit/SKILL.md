---
name: ai-lab-retrofit
description: 완성된 해설 HTML의 본문은 그대로 두고 지식 색인(#kg)과 온톨로지·서지 꾸러미(#export)만 덧붙인다. 글 표지 보강과 시리즈 커버리지(O5)도 맡는다. '기존 페이지에 꼬리표 달아 줘'에 쓴다.
---

# 완성된 HTML 꼬리표 달기 스킬 (ai-lab-retrofit)

> **스킬 정보:** version: 1.3 · targets: Claude, ChatGPT, Gemini, Genspark, 코딩 에이전트(Claude Code, Codex, Cursor 등) 공통 · language: ko
>
> **자세한 설명:** 이미 완성된 HTML 교육 페이지(단일 파일, 여러 파일로 된 사이트, GitHub 저장소)를 다시 만들지 않고, 본문은 그대로 둔 채 지식 색인(#kg)과 온톨로지·서지 꾸러미(#export)를 덧붙이고, 맨 위 글 표지가 없으면 네 캐릭터 표지의 생성 지시문(Genspark용)과 반영 절차도 함께 다룬다. 그 결과 꾸러미를 KG_00 시리즈 커버리지 지도에 합칠 수 있게 된다. "기존 페이지에 꼬리표 달아 줘", "이 저장소 페이지들 지도에 올려 줘", "완성된 HTML을 온톨로지에 연결" 같은 요청에 쓴다. 새 페이지를 만드는 일은 ai-lab-explainer 스킬이 맡는다.

> **한 줄 요약:** 완성된 페이지를 읽는다 → 지식 그래프·참고문헌·페이지 정보 JSON 세 개를 만든다 → 조립 도구로 페이지 끝에 두 섹션을 붙인다 → 점검 도구로 "본문 차이 0"을 확인한다 → 꾸러미를 KG_00 지도에 넣는다.
>
> 이 문서와 `tools/` 폴더만 있으면 어떤 AI에서도 같은 결과가 나오도록 기본값을 모두 정해 두었다. 본편 스킬(ai-lab-explainer) 없이도 쓸 수 있다.
>
> **v1.3 (저장소판):** 이 폴더는 저장소 `ahnboat_lab_explainer`의 `packs/task/onto-retrofit/`이다. 뼈대와 등록부는 도구 폴더가 아니라 저장소 **`data/`**에 한 벌만 둔다(`data/backbone_ai.json`, `data/KG_00_registry.json`). 이 폴더만 따로 다른 AI에 줄 때는 `data/`의 두 파일을 함께 첨부한다. 영역 완성 파이프라인(옛 본편 O5장)은 같은 폴더의 `O5_pipeline.md`다. 본편 v1.8~1.9에 맞춘 변경은 14장.

---

## 목차

0. 이 스킬이 하는 일
1. 어디서 작업하나 (네 가지 길)
2. 묶음 구성
3. 입력과 출력
4. 작업 순서 (R0~R6)
5. 바꾸지 않는 규칙
6. 데이터 형식
7. 뼈대에 걸기
8. 여러 파일로 된 사이트
9. GitHub에서 작업할 때
10. 프롬프트 템플릿
11. 점검 체크리스트
12. 문제가 생겼을 때
13. 표지 보강 (글 표지 지시문 · 받은 그림 반영)
14. v1.3 변경: 분야, 새 어휘, 저장소 경로

---

## 0. 이 스킬이 하는 일

| 한다 | 하지 않는다 |
|---|---|
| 페이지 끝(마지막 바닥글 앞)에 **지식 색인**과 **꾸러미** 두 섹션을 붙인다 | 본문 글, 그림, 시뮬레이션, 코드, 용어, 참고문헌을 고치지 않는다 |
| `<head>`에 서지 메타 태그를 붙인다 | 디자인을 바꾸지 않는다 |
| 데이터 블록 네 개(`kg-raw`, `kg-ld`, `refs-csl`, `page-meta`)를 넣는다 | 페이지에 없는 DOI·쪽수·저자를 지어내지 않는다 |
| 개조 기록과 점검 보고서를 남긴다 | 발견한 오타·오류를 몰래 고치지 않는다 (기록만 한다) |
| 등록부(`KG_00_registry.json`)에 새 ID를 더한다 | 새 페이지를 만들지 않는다 (→ ai-lab-explainer) |

**왜 하나:** 꾸러미가 없는 페이지는 KG_00 커버리지 지도에 보이지 않는다. 그래서 이미 다룬 영역이 "이 시리즈가 아직 다루지 않은 영역"으로 잘못 나온다. 꼬리표를 달면 지도가 실제 시리즈를 기준으로 다시 계산된다.

**사람의 일과 AI의 일:** 페이지를 읽고 무엇이 개념이고 무엇이 근거인지 판단하는 일(R1~R2)은 AI가 한다. 붙이고 점검하는 일(R3~R4)은 도구가 한다. 도구가 기계적인 부분을 맡으므로, 어느 AI가 하든 붙이는 방식은 같다.

---

## 1. 어디서 작업하나 (네 가지 길)

| 길 | 이럴 때 | 하는 방법 | 결과를 돌려놓는 법 |
|---|---|---|---|
| **A. GitHub + 코딩 에이전트** (추천) | 페이지가 GitHub 저장소에 있고, Claude Code·Codex·Cursor 같은 코딩 에이전트를 쓸 수 있다 | 에이전트에 저장소를 연결하고 이 스킬 폴더를 저장소에 넣거나 첨부한다. 에이전트가 브랜치를 만들고 `tools/`를 직접 실행한다 | 에이전트가 만든 PR(변경 요청)을 보고 합친다 |
| **B. 코드 실행이 되는 Claude 대화** | 저장소가 없거나 에이전트를 안 쓴다 | GitHub에서 **Code → Download ZIP**으로 받은 ZIP(또는 HTML 하나)과 이 스킬 폴더를 첨부한다 | 결과 ZIP을 받아 원래 폴더에 덮어쓰고, GitHub에 올린다 |
| **C. 코드 실행이 없는 채팅 AI** (ChatGPT, Gemini, Genspark 등) | 다른 AI를 쓰고 싶다 | 페이지 HTML과 이 문서를 주고 **JSON 세 개만** 받는다. 그다음 `tools/assembler.html`(꼬리표 조립기)을 브라우저로 열어 원본 HTML과 JSON을 넣는다 | 조립기가 만든 HTML을 받아 원래 파일과 바꾼다 |
| **D. 내 컴퓨터에서 직접** | 파이썬을 쓸 줄 안다 | JSON 세 개는 AI에게 받고, `python3 tools/retrofit.py` → `python3 tools/check.py` | 그대로 커밋 |

**고르는 법:** 저장소가 있고 코딩 에이전트가 있으면 A, 없으면 B. Claude가 아닌 AI를 써야 하면 C.

**C 길에서 조립기를 쓰는 이유:** 채팅 AI에게 수백 KB짜리 HTML 전체를 다시 쓰게 하면 중간에 끊기거나 본문이 바뀐다. AI는 판단이 필요한 JSON만 쓰고, 붙이는 일은 조립기가 한다. 조립기는 인터넷 연결 없이 브라우저 안에서만 동작한다.

---

## 2. 묶음 구성

```
ai-lab-retrofit/
├─ SKILL.md                   이 문서
├─ tools/
│  ├─ retrofit.py             조립 (파이썬 3, 외부 패키지 없음. node가 있으면 JSON-LD도 만든다)
│  ├─ check.py                점검 (본문 차이 0, 끊긴 관계, 없는 anchor, 출처, 금지 표현)
│  ├─ assembler.html          꼬리표 조립기 (브라우저용, retrofit.py + check.py 핵심과 같은 일)
│  ├─ kgx.js                  지식 색인·꾸러미 화면과 내보내기 모듈 (외부 라이브러리 없음)
│  (v1.3: backbone.json, KG_00_registry.json은 저장소 data/로 옮김)
├─ O5_pipeline.md            영역 온톨로지 완성 파이프라인 (+ 표지 보강 부록)
└─ templates/
   ├─ kg.template.json        지식 그래프 예시
   ├─ refs.template.json      참고문헌 예시
   └─ meta.template.json      페이지 정보 예시
```

---

## 3. 입력과 출력

### 3-1. 입력

| 입력 | 필수 | 없을 때 |
|---|---|---|
| 페이지 HTML (또는 저장소 / 폴더 ZIP) | 필수 | 묻는다 |
| 뼈대 `data/backbone_{분야}.json` | 필수 (저장소 `data/`) | 인공지능은 `backbone_ai.json`. 다른 분야는 분야 팩 P10으로 만든다 |
| `data/KG_00_registry.json` | 권장 (저장소 `data/`) | 분야와 상관없이 하나. 새 ID를 더해 함께 낸다 |
| 분야 | 권장 | 14-1. 옛 페이지는 대개 `ai` |
| 저자 이름·라이선스·공개 주소 | 선택 | 페이지에 적혀 있으면 그것을, 아니면 **빈칸**. 지어내지 않는다 |
| 시리즈 이름, 페이지 번호 | 선택 | 페이지 제목·파일 이름에서 읽는다. 애매하면 묻는다 |
| KG_00 지도 주소 | 선택 | `meta.seeAlso`를 빈칸으로 |

### 3-2. 출력 (페이지 하나마다)

1. **꼬리표를 단 HTML** (같은 파일 이름)
2. `kg.json`, `refs.json`, `meta.json` (조립에 쓴 원본, 저장소에는 `kg/` 폴더에 둔다)
3. `check_report.md` (오류 0이어야 함)
4. `retrofit_log.md` (6-5절 형식)
5. 등록부 갱신분 (새 ID가 생겼을 때)

---

## 4. 작업 순서 (R0~R6)

### R0. 목록 만들기

저장소나 폴더 전체를 받았으면 먼저 표를 만들고, 사람에게 보여 준 뒤 순서를 정한다.

| 페이지 파일 | 제목 | 섹션 id 목록 | 참고문헌 수 | 이미 꼬리표 있음 | 추정 영역 (추정·미검증) |
|---|---|---|---|---|---|

- "이미 꼬리표 있음"은 `<!-- lab-kg:body -->` 표시나 `id="kg-raw"`가 있는지로 본다. 있으면 다시 만들지 말고 갱신만 한다.
- 목차(index), 허브, 404 페이지는 뺀다.
- **순서 기본값:** "채울 것으로 보이는 영역 수 × 참고문헌 수"가 큰 페이지부터.

### R1. 페이지 읽고 항목 뽑기

| # | 페이지에서 찾을 것 | 만드는 노드 | 만드는 관계 |
|---|---|---|---|
| E1 | 섹션 제목과 그 섹션이 설명하는 핵심 개념·방법 | `Concept` / `Method` | 앞 개념 → 뒤 개념 `prerequisiteOf` (본문 순서와 설명이 그렇게 이어질 때만) |
| E2 | "한계", "문제점", "왜 안 되나" 같은 설명 | `Limitation` | 개념 `hasLimitation` 한계, 한계 `addressedBy` 다음 방법 |
| E3 | 용어 사전·용어 말풍선 항목 | `Term` 또는 `Concept` | 뼈대 주제 `broader` |
| E4 | 출처가 붙은 사실 문장, 실험 결과 | `Claim` (+ `source`) | `supports` 대상, `assertedIn` 문헌 |
| E5 | 참고문헌 목록의 각 항목 | `Work` | — (E4가 이어 줌) |
| E6 | 비유 상자, 짝 카드 ("○○는 △△와 닮았다") | `Analogy` / `BioAnalogue` | `analogyOf` / `bioAnalogueOf` |
| E7 | 비교·대결 장치 (A vs B) | `Method` 2개 | `contrastsWith`, 판정 기준 `evaluatedBy` 지표 |
| E8 | 시뮬레이션, 대시보드, Colab 코드 | `Simulation` | 개념 `demonstratedBy` |
| E9 | 퀴즈·확인 문제 | `QuizItem` | `assesses` 개념 |
| E10 | "아직 모른다", "확인 필요", 열린 질문 | `Question` | 개념 `raises` 질문 |

- **anchor:** 각 노드가 설명되는 본문 섹션의 `id`. 섹션에 id가 없으면 가장 가까운 상위 요소의 id를 쓰고, 그것도 없으면 `#top`. **id를 새로 만들어 본문에 넣지 않는다.**
- **규모:** 노드 30~80개, 관계 50~150개. 고립 노드 0.
- **상태 판정 (`coverage`):**

| 값 | 기준 | 예 |
|---|---|---|
| `explained` | 정의 문장이 있고, 예시·그림·시뮬레이션·코드 중 하나 이상이 그 개념을 직접 보여 준다 | 활성화 함수 섹션의 ReLU: 정의 + 그래프 + 코드 |
| `mentioned` | 이름이나 비유로만 나오고 정의·예시가 없다 | "LoRA와 닮았다"고만 한 경우 |
| (노드 안 만듦) | 목록·각주에 이름만 한 번 지나간다 | 참고문헌 제목 속 단어 |

애매하면 낮은 쪽으로 판정한다.

### R2. JSON 세 개 쓰기

6장 형식대로 `kg.json`, `refs.json`, `meta.json`을 쓴다. `templates/`를 본뜬다. 쓰기 전에 등록부를 읽고, 같은 개념이면 등록부의 ID를 쓴다.

출력이 끊기는 AI라면 나눠서 요청한다: ① `meta.json`과 `refs.json` → ② `kg.json`의 `nodes` → ③ `kg.json`의 `edges`. 마지막에 합친다.

### R3. 조립

```bash
# 단일 파일 페이지
python3 tools/retrofit.py pages/3-2_building_blocks.html \
  --kg kg/3-2/kg.json --refs kg/3-2/refs.json --meta kg/3-2/meta.json \
  --backbone ../../../data/backbone_ai.json
# → 원본 자리에 결과, 원본은 .bak로 남음 (-o로 다른 이름 가능)

# 여러 파일 사이트: kgx.js를 한 곳에 두고 연결
python3 tools/retrofit.py site/3-2.html ... --js assets/js/kgx.js
```

코드 실행이 없으면 `tools/assembler.html`을 브라우저로 열어 같은 일을 한다.

**조립 도구가 하는 일:**
- `</head>` 앞에 메타 태그
- 마지막 `<footer` 앞(없으면 `</body>` 앞)에 두 섹션과 데이터 블록
- `</body>` 앞에 `kgx.js`
- 모두 `<!-- lab-kg:head|body|script -->` 표시 사이에 넣는다. 다시 돌리면 표시 사이만 바뀐다 (몇 번을 돌려도 결과가 같다).

### R4. 점검

```bash
python3 tools/check.py 원본.html 결과.html --backbone ../../../data/backbone_ai.json \
  --registry ../../../data/KG_00_registry.json --report check_report.md
```

**오류가 0이 될 때까지 R2로 돌아가 JSON을 고친다.** HTML을 손으로 고치지 않는다. 경고는 읽고, 맞으면 그대로 두고 `retrofit_log.md`에 이유를 적는다.

그다음 브라우저로 열어 본다: 지식 색인에 숫자·목록·그래프가 보이는지, 꾸러미의 "ZIP 내려받기"가 되는지, 폭 390px에서 가로로 넘치지 않는지.

### R5. 기록

- `retrofit_log.md` 작성 (6-5절)
- 새 ID를 등록부에 더한다 (`entries`에 `id`, `type`, `label_ko`, `label_en`, `pages`)

### R5-1. 표지 보강 (해당할 때)

맨 위 글 표지가 없는 페이지면 13장 규칙으로 표지 지시문을 함께 낸다. 사용자가 그림을 돌려주면 13-4 절차로 넣는다. 꼬리표와 표지는 순서에 상관없다.

### R6. 지도에 넣기

결과 페이지의 꾸러미 섹션에서 **꾸러미 ZIP 내려받기** → KG_00 커버리지 지도의 "꾸러미 넣기"에 넣는다. 여러 페이지를 한 번에 넣어도 된다. 바뀐 지표를 `pipeline_log.json`(`O5_pipeline.md` O5-10)에 한 회차로 남긴다.

---

## 5. 바꾸지 않는 규칙

| # | 규칙 |
|---|---|
| N1 | **본문 차이 0.** 표시(`lab-kg`) 밖은 한 글자도 바꾸지 않는다. 예외는 사용자가 요청해 넣은 글 표지 블록(`<!-- lab-cover -->`, ai-lab-explainer 18-15)뿐이며, 점검 도구는 이 표시도 덧붙인 부분으로 보고 비교에서 뺀다. 조립 도구는 표지 블록을 지우지 않는다. 목차에 "지식 색인" 링크를 더하고 싶어도 하지 않고 `retrofit_log.md`의 "사람이 할 일"에 적는다 |
| N2 | **참고문헌은 페이지에 적힌 것만.** 제목·저자·연도·학술지를 페이지 표기 그대로 옮긴다. 페이지에 없는 DOI·쪽수·권호는 넣지 않고 `verified`에 `false`로 둔다. 외부에서 확인해 채울 때는 `checkedBy`에 확인한 곳과 날짜를 적는다 |
| N3 | **저자·라이선스·주소는 페이지에 적혀 있거나 사용자가 준 값만.** 없으면 빈칸 |
| N4 | **근거 없는 Claim을 만들지 않는다.** 페이지에서 그 문장을 뒷받침하는 참고문헌을 찾지 못하면 Claim 대신 `Concept`의 정의로만 남긴다 |
| N5 | **금지 표현:** "아무도 손대지 않은", "미개척", "세계 최초". 시리즈 기준이면 "이 시리즈가 아직 다루지 않은"이라고 쓴다 |
| N6 | **외부 라이브러리·브라우저 저장소를 쓰지 않는다.** `kgx.js`만 쓴다. localStorage·sessionStorage·IndexedDB 금지 |
| N7 | **뼈대는 작성자 초안이다.** 화면과 문서에서 "공식 분류 체계"라고 부르지 않는다 |
| N8 | **발견한 오류는 기록만.** 오타, 틀린 수치, 깨진 링크는 `retrofit_log.md`에 위치와 함께 적고, 고칠지는 사람이 정한다 |

---

## 6. 데이터 형식

### 6-1. `kg.json`

```json
{"version": "1.0", "page": "3-2_building_blocks", "nodes": [ … ], "edges": [ … ]}
```

**노드:**

| 필드 | 필수 | 규칙 |
|---|---|---|
| `id` | 필수 | `lab:{종류 소문자}/{영어 kebab-case}`. 예 `lab:concept/relu`, `lab:method/adam`, `lab:claim/…`, `lab:work/{참고문헌 id}`, `lab:quiz/p{번호}-{섹션}-{n}`. 등록부에 있으면 그 ID |
| `type` | 필수 | 6-2 표 |
| `label` | 필수 | `{"ko": …, "en": …}`. 페이지 표기 그대로 |
| `page` | 필수 | 페이지 슬러그 |
| `anchor` | 필수 | 본문에 실제로 있는 `#id` (Work는 `#export`) |
| `level` | 필수 | 1 기초 · 2 핵심 · 3 응용 · 4 최신·심화 |
| `status` | 필수 | `known` |
| `confidence` | 필수 | `high` · `medium` · `low` (페이지가 "확인 필요"라고 한 것은 `low`) |
| `coverage` | 필수 | `explained` · `mentioned` (R1 판정표) |
| `definition` | 개념류 권장 | `{"ko": 페이지 정의를 한 문장으로}` |
| `family` | 권장 | 뼈대 영역의 `family` 값 (7장 표) |
| `altLabel` | 선택 | `{"ko": [다른 이름들]}` |
| `source` | Claim 필수 | `[{"ref": 참고문헌 id, "loc": 페이지에 적힌 쪽·그림 번호 또는 ""}]` |
| `match` | 필수 | 외부 온톨로지 대응. 확인 전에는 `[]` |

**관계:** `{"s": 출발 id, "p": "lab:관계", "o": 도착 id, "anchor": "#id", "confidence": "high"}`

### 6-2. 종류와 관계 어휘

| 종류 (`type`) | 뜻 |
|---|---|
| `Concept` | 개념 |
| `Method` | 방법·모델·알고리즘 |
| `Limitation` | 한계 |
| `Term` | 용어 (개념만큼 설명되지 않은 것) |
| `Claim` | 출처 있는 사실 문장 |
| `Work` | 참고문헌 |
| `Question` | 열린 질문, 확인 필요 |
| `Analogy` · `BioAnalogue` | 비유 · 생물 대응물 |
| `Task` · `Metric` · `Dataset` | 과제 · 지표 · 데이터 |
| `Simulation` | 시뮬레이션, 대시보드, 코드 실습 |
| `QuizItem` | 퀴즈 문항 |

| 관계 (`p`) | 뜻 | 관계 (`p`) | 뜻 |
|---|---|---|---|
| `lab:broader` | 상위 주제 (뼈대에 걸기) | `lab:supports` | 주장이 뒷받침함 |
| `lab:prerequisiteOf` | 먼저 알아야 함 | `lab:assertedIn` | 주장의 출처 문헌 |
| `lab:hasLimitation` | 한계가 있음 | `lab:demonstratedBy` | 시뮬레이션으로 보임 |
| `lab:addressedBy` | 한계를 해결함 | `lab:assesses` | 퀴즈가 확인함 |
| `lab:partOf` | 부분 | `lab:raises` | 질문을 낳음 |
| `lab:contrastsWith` | 대비 | `lab:evaluatedBy` · `lab:evaluatedOn` | 지표 · 데이터로 평가 |
| `lab:analogyOf` · `lab:bioAnalogueOf` | 비유 · 생물 대응 | `lab:relatedTo` | 관련 (전체의 15% 이하) |

### 6-3. `refs.json` (CSL-JSON + `lab` 확장)

```json
[{"id": "nair2010rectified", "type": "paper-conference",
  "title": "…페이지 표기 그대로…", "author": [{"family": "Nair", "given": "Vinod"}],
  "issued": {"date-parts": [[2010]]}, "container-title": "…",
  "lab": {"work": "lab:work/nair2010rectified", "role": "background",
          "supports": ["lab:claim/…"], "locs": [],
          "verified": {"title": true, "author": true, "year": true, "container": false, "pages": false, "doi": false},
          "checkedBy": "페이지 참고문헌 목록에서 옮김 (외부 대조 안 함)", "checkedSource": "page"}}]
```

- `id`: 제1저자 성(소문자) + 연도 + 제목 첫 실질 단어. 예 `vaswani2017attention`.
- `type`: `article-journal`, `paper-conference`, `book`, `chapter`, `report`, `thesis`, `webpage`, `dataset`, `software`.
- 저자가 "외"로만 적혀 있으면 적힌 사람까지만 넣고 마지막에 `{"literal": "et al."}`.
- `role`: `primary`(주 자료) · `background` · `data`(수치 출처) · `figure`(그림 출처).
- `verified`의 `true`는 "페이지 표기와 일치"를 뜻한다. 외부에서 대조했으면 `checkedBy`에 적는다.

### 6-4. `meta.json`

| 필드 | 규칙 |
|---|---|
| `title`, `number`, `series` | 페이지 표기 그대로 |
| `date` | 꼬리표를 단 날 |
| `version` | 기존 판에 0.1을 더한다 (모르면 `1.1`) |
| `creator` | `[{"name": …, "role": "author"}]`. 페이지에 적혀 있거나 사용자가 준 이름만 |
| `contributor` | `[{"name": "AI 보조 제작", "role": "assistant"}]` |
| `about` | 페이지 핵심 노드 id 3~6개 |
| `basedOn` | 주 자료 참고문헌 id |
| `educationalLevel` | 입문 · 입문~중급 · 중급 · 심화 |
| `license`, `url` | 사용자가 준 값만, 없으면 `""` |
| `registry` | `KG_00_registry 0.2` |
| `seeAlso` | KG_00 지도 주소 (없으면 `""`) |
| `suggestedCitation` | `{저자} ({연도}). {제목}. {시리즈} {번호}, v{판}.` |

### 6-5. `retrofit_log.md`

```markdown
# 개조 기록 — {페이지 파일}
- 날짜: {YYYY-MM-DD} · 도구: retrofit.py / assembler.html · AI: {모델 이름}
- 결과: 노드 {n} · 관계 {n} · 문헌 {n} · 점검 오류 0 · 경고 {n}
## 뼈대 밖 항목 (맞는 주제가 없어 broader를 걸지 않음)
- {항목} — {이유}
## 발견한 문제 (고치지 않음)
- {위치 #id}: {내용}
## 경고를 그대로 둔 이유
- {경고}: {이유}
## 사람이 할 일
- 목차에 "지식 색인", "꾸러미" 링크 추가 (선택)
- 저자 이름·라이선스 채우기
```

---

## 7. 뼈대에 걸기

개념·방법·한계·용어·생물 대응 노드는 모두 `lab:broader`로 **뼈대 주제 1~2개**에 건다. 주제 ID는 `lab:topic/{아래 이름}`이다. 맞는 주제가 없으면 걸지 않고 `retrofit_log.md`의 "뼈대 밖 항목"에 적는다(뼈대 판을 올릴 때 참고).

| 영역 | family | 주제 |
|---|---|---|
| 수학 기초 | `math` | linear-algebra, probability-statistics, calculus-optimization-math, information-theory |
| 머신러닝 기초 | `ml-basics` | supervised-learning, unsupervised-learning, generalization, bias-variance, data-splitting, feature-engineering, rule-vs-learning |
| 고전 모델 | `classical` | linear-regression, logistic-regression, svm, knn, decision-tree, naive-bayes |
| 앙상블 | `ensemble` | bagging, random-forest, boosting, stacking |
| 신경망 기초 | `nn-basics` | weights-and-biases, perceptron, mlp, activation-function, loss-function, backpropagation, universal-approximation |
| 최적화 | `optimization` | gradient-descent, sgd-minibatch, momentum-adam, learning-rate-schedule |
| 정규화·일반화 기법 | `regularization` | weight-decay, dropout, early-stopping, normalization-layers, data-augmentation |
| 합성곱·시각 | `vision` | convolution, pooling, receptive-field, residual-connections, object-detection, segmentation |
| 시퀀스 모델 | `sequence` | rnn, lstm-gru, seq2seq, time-series |
| 어텐션·트랜스포머 | `attention` | attention-mechanism, self-attention, multi-head-attention, positional-encoding, transformer |
| 언어 모델·자연어 처리 | `language` | tokenization, word-embedding, pretrained-lm, transfer-learning, lora, prompting, rag |
| 생성 모델 | `generative` | autoencoder, vae, gan, diffusion, autoregressive-generation |
| 표현 학습 | `representation` | embedding-space, self-supervised, contrastive, sparse-representation, random-features, multi-task-learning |
| 강화 학습 | `rl` | mdp, reward, value-function, q-learning, policy-gradient, exploration, reward-prediction-error |
| 비지도 기법 | `unsupervised` | clustering, pca, tsne-umap, density-estimation, anomaly-detection |
| 평가 | `evaluation` | accuracy-metrics, precision-recall, roc-auc, confusion-matrix, data-leakage, ablation |
| 그래프 학습 | `graph` | gnn, message-passing, knowledge-graph |
| 시스템·MLOps | `systems` | deployment, distribution-shift, monitoring, reproducibility |
| 책임 있는 AI | `responsible` | fairness, interpretability, ai-safety, privacy |
| 신경과학과 AI | `neuro` | biological-neuron, synaptic-plasticity, connectome, sensory-processing, learning-memory-circuits, circuit-methods |

뼈대는 표준 교과서 목차와 분야 구분을 참고해 이 시리즈용으로 만든 **작성자 초안 v0.1**이다. 다른 분야의 시리즈라면 같은 형식으로 새 `backbone.json`을 만들어 바꿔 끼운다.

---

## 8. 여러 파일로 된 사이트

| 상황 | 처리 |
|---|---|
| 이미지·CSS·JS가 `assets/` 등에 따로 있음 | HTML만 조립한다. 다른 파일과 상대 경로는 건드리지 않는다 |
| 페이지가 여러 개 | `kgx.js`를 `assets/js/kgx.js` 한 곳에 두고 모든 페이지가 `--js assets/js/kgx.js`로 연결한다. 페이지가 하위 폴더에 있으면 경로를 맞춘다 (예 `../assets/js/kgx.js`) |
| 단일 파일로 배포해야 함 | `--js inline` (기본). 이미지를 HTML 안에 넣는 일은 이 스킬이 하지 않는다 |
| 한 페이지가 여러 HTML로 나뉨 (1부·2부) | 각 HTML이 따로 꾸러미를 가진다. `page` 값을 다르게 하고, 같은 개념은 같은 ID |
| GitHub Pages | 상대 경로만 쓰면 그대로 동작한다. `kgx.js`는 저장소 안에 두고, 외부 CDN을 쓰지 않는다 |
| JSON 원본 보관 | `kg/{페이지 번호}/kg.json · refs.json · meta.json · retrofit_log.md · check_report.md` |

---

## 9. GitHub에서 작업할 때

### 9-1. 코딩 에이전트 (길 A)

1. 이 스킬 폴더를 저장소의 `tools/ai-lab-retrofit/`에 넣는다(또는 에이전트에 첨부).
2. 에이전트에 10-1 프롬프트를 준다.
3. 에이전트가 하는 일: 브랜치 `kg/retrofit-{페이지}` → R0 목록 → 페이지마다 R1~R5 → 커밋 → PR.
4. **PR 하나에 페이지 하나**를 기본으로 한다. 검토가 쉽고, 되돌리기 쉽다.
5. PR 설명에는 점검 보고서 요약(오류 0, 경고 목록), 노드·관계·문헌 수, 사람이 할 일을 적는다.

**커밋 메시지 형식:** `kg: {페이지 번호} 지식 색인·꾸러미 추가 (노드 {n}, 문헌 {n})`

### 9-2. ZIP으로 받아서 (길 B·C)

1. GitHub 저장소 화면 → 초록색 **Code** 단추 → **Download ZIP**.
2. ZIP을 Claude(길 B)에 첨부하거나, 페이지 HTML만 꺼내 채팅 AI(길 C)에 준다.
3. 결과 HTML을 원래 자리에 덮어쓴다. `kg/` 폴더(JSON 원본)도 함께 넣는다.
4. GitHub 웹에서 **Add file → Upload files**로 올리고, 커밋 메시지는 9-1 형식.

---

## 10. 프롬프트 템플릿

### 10-1. 코딩 에이전트 (저장소 전체)

```
[역할] tools/ai-lab-retrofit/SKILL.md를 따른다.
[할 일]
1. R0: 저장소의 HTML 페이지 목록 표를 만들어 보여 주고, 순서를 기본값으로 정한다.
2. 첫 페이지 {파일 이름}부터 R1~R5를 한다. JSON은 kg/{번호}/에 둔다.
3. python3 tools/ai-lab-retrofit/tools/check.py로 오류 0을 확인한다. 오류가 있으면 JSON을 고친다. HTML은 손으로 고치지 않는다.
4. 브랜치 kg/retrofit-{번호}에 커밋하고 PR을 연다. PR 설명에 점검 요약과 "사람이 할 일"을 적는다.
[금지] 본문 수정, 페이지에 없는 DOI·쪽수·저자, 외부 라이브러리, 브라우저 저장소.
[모르면] 저자·라이선스는 빈칸. 시리즈 이름·번호가 애매하면 묻는다.
```

### 10-2. Claude 대화 (ZIP 또는 HTML 첨부)

```
첨부한 SKILL.md(ai-lab-retrofit)를 따라, 첨부한 {페이지 HTML / 사이트 ZIP}에 꼬리표를 달아 줘.
- tools/의 retrofit.py로 조립하고 check.py로 오류 0을 확인한다.
- 여러 파일 사이트면 폴더 구조를 그대로 둔 ZIP으로 돌려준다.
- 결과: 꼬리표 단 HTML(또는 ZIP), kg.json·refs.json·meta.json, check_report.md, retrofit_log.md, 등록부 갱신분.
저자: {이름 또는 "빈칸"} · 라이선스: {값 또는 "빈칸"} · KG_00 주소: {주소 또는 "빈칸"}
```

### 10-3. 코드 실행이 없는 채팅 AI (JSON만)

```
첨부한 SKILL.md(ai-lab-retrofit)의 R1·R2와 6장 형식대로, 첨부한 페이지 HTML의 kg.json, refs.json, meta.json 세 파일만 만들어 줘.
- HTML 전체를 다시 쓰지 마. 세 JSON을 각각 코드 블록 하나로.
- 등록부(첨부한 KG_00_registry.json)에 있는 개념은 그 ID를 쓴다.
- anchor는 페이지에 실제로 있는 id만. 참고문헌은 페이지 표기 그대로, 없는 DOI·쪽수는 넣지 않는다.
- 뼈대 주제는 SKILL 7장 표의 이름만 쓴다.
- 끊기면 ① meta·refs → ② kg nodes → ③ kg edges 순서로 나눠서.
마지막에 retrofit_log.md 초안도 줘.
```

받은 JSON 세 개를 파일로 저장한 뒤 `tools/assembler.html`(꼬리표 조립기)을 브라우저로 열어 원본 HTML과 함께 넣는다. 조립기의 점검 결과가 "오류 없음"이면 결과 HTML을 받는다. 오류가 있으면 그 문장을 그대로 AI에게 보여 주고 JSON만 고쳐 달라고 한다.

---

## 11. 점검 체크리스트

- [ ] `check.py`(또는 조립기) 오류 0
- [ ] "본문 차이 0" 확인됨
- [ ] 모든 anchor가 본문에 실제로 있음
- [ ] 고립 노드 0, 끊긴 관계 0, `relatedTo` 15% 이하
- [ ] 개념·방법 노드마다 뼈대 주제 1~2개, 없으면 retrofit_log에 사유
- [ ] Claim마다 `source`가 있고, 그 문헌이 `refs.json`에 있음
- [ ] 페이지에 없는 DOI·쪽수·저자를 넣지 않음 (넣었다면 `checkedBy`에 확인처와 날짜)
- [ ] 저자·라이선스는 페이지 표기나 사용자 값, 없으면 빈칸
- [ ] 금지 표현 없음 (N5)
- [ ] 브라우저에서 지식 색인·꾸러미가 보이고 ZIP이 내려받아짐
- [ ] 폭 390px에서 가로 넘침 없음, 콘솔 오류 0
- [ ] 등록부 갱신분과 retrofit_log.md를 함께 냄

---

## 12. 문제가 생겼을 때

| 증상 | 원인과 처리 |
|---|---|
| "본문에 없는 anchor" 오류 | JSON의 `anchor`를 본문에 있는 id로 바꾼다. 본문에 id를 새로 만들지 않는다 |
| "끊긴 관계" 오류 | 관계의 `s`나 `o`가 노드 목록에 없다. 노드를 더하거나 관계를 지운다. `lab:topic/…`이면 7장 표의 이름이 맞는지 본다 |
| "본문이 바뀜" 오류 | HTML을 손으로 고쳤거나 다른 도구가 줄바꿈을 바꿨다. 원본(.bak)에서 다시 조립한다 |
| "원본 페이지에 없는 DOI" 경고 | 외부에서 확인한 것이면 `checkedBy`를 채우고 그대로 둔다. 확인하지 않았으면 지운다 |
| `kg-ld 없음` 경고 | 조립한 컴퓨터에 node가 없다. 페이지는 정상이고, 꾸러미 ZIP에는 JSON-LD가 들어간다. 조립기(assembler.html)로 다시 조립하면 블록이 생긴다 |
| 지식 색인 글자가 밑줄 말풍선으로 덮임 | 페이지의 용어 말풍선 스크립트가 새 섹션도 훑는다. 본문은 고치지 않는다. retrofit_log의 "사람이 할 일"에 "말풍선 제외 목록에 `.kgx` 추가"를 적는다 |
| 색이 페이지와 안 어울림 | `kgx.js`는 페이지의 `--bg`, `--panel`, `--text`, `--gfp` 등 색 변수가 있으면 따르고, 없으면 흰 배경(낮의 연구실) 기본색을 쓴다. 관계 그래프 상자만 어두운 화면으로 둔다(노드 색이 잘 보이게). 바꾸고 싶으면 페이지 CSS에 그 변수를 정의한다 (본문 수정이므로 사람이 정한다) |
| `<footer>`가 페이지 중간에 있음 | 조립 도구는 마지막 `<footer` 앞에 넣는다. 위치가 이상하면 `</body>` 바로 앞에 넣도록 사람에게 묻는다 |
| AI 출력이 끊김 | 10-3의 세 단계 나눠 쓰기. "끊긴 곳부터 같은 파일의 나머지만" |

---

## 13. 표지 보강 (이미 만든 페이지에 글 표지 더하기)

예전에 제1부만으로 만든 페이지에는 맨 위 **글 표지 그림**이 없다. 온톨로지 꼬리표를 달 때 표지도 함께 보강한다. 순서는 **① 지시문 만들기 → ② 사용자가 그림 생성 → ③ 받은 그림 반영**이다. 본편 스킬 v1.6의 18-14·18-15와 같은 규칙이며, 이 장만으로도 작업할 수 있게 필요한 값을 모두 적었다.

### 13-1. 몇 장, 어디에

| 경우 | 표지 | 키 |
|---|---|---|
| 목차(index) | 1장 | `cover_index` |
| 챕터 하나 = HTML 하나 | HTML마다 1장 | `cover_{N}` |
| 챕터 하나 = HTML 여러 개 | 챕터 첫 HTML에 1장, 나머지 페이지는 같은 그림을 낮은 띠로 재사용 | `cover_ch{n}` |
| 지식 지도·부록 같은 도구 페이지 | 기본 없음 | — |

자리: 상단 내비 바로 아래(내비가 없으면 `<body>` 맨 앞). 페이지에 이미 맨 위 장면 그림이 있으면, 표지로 **바꿀지 / 그 위에 더할지** 사용자에게 묻는다.

### 13-2. 규격 (판 L)

| 항목 | 값 |
|---|---|
| 생성 | 16:9, 가로 1920 이상 |
| 빌드 | WebP 1600×900 (220 KB 이하) + 960×540 (110 KB 이하). 단일 파일 페이지는 1600 하나를 base64로 |
| 캐릭터 | **넷 모두**: 박사, 조수, 초파리 연구원, 주판봇 |
| 안전 영역 | 얼굴·손·핵심 소품은 좌우 12%, 위 10%, 아래 18% 안쪽 |
| 왼쪽 아래 | 30% × 20%는 어둡고 단순하게 (시리즈 칩 자리) |
| 금지 | 그림 안 글자·숫자·로고, 승패 암시(표지는 대결 전 장면), 생물 앵커가 아닌 편의 현미경·해부 소품, 실존 브랜드 |

### 13-3. 지시문 만들기 (AI가 페이지를 읽고 채운다)

페이지마다 아래 네 가지를 정한다. 같은 시리즈 표지끼리 장소·포즈·소품이 겹치지 않게 한다.

1. **장소:** 페이지 주제에 맞는 곳. 생물 → 형광 현미경 실험대 / 연구실 → 낮의 연구실 / 매출 기록(돈·금융) → 큰 주판과 금고가 있는 회계실 / 생활 → 도서관·서재·공장 등 (연구실의 연보라 소품을 한쪽에 남긴다)
2. **주제 은유:** 페이지 핵심 개념을 글자 없는 장면 하나로 (예: 어텐션 → 질문 카드에서 책들로 뻗는 빛줄기)
3. **네 캐릭터 포즈:** 초파리는 왼쪽에서 오른쪽을, 주판봇은 오른쪽에서 왼쪽을 본다. 박사는 가운데 뒤, 조수는 한쪽 옆
4. **대체 글:** 한국어 한 문장

**Genspark에 붙여 넣기 틀** (참고 이미지: 네 캐릭터 기본 그림 4장, 기준 GitHub `adminmrobo/fruitfly-lab-expressions`)

```
웹페이지 맨 위에 거는 표지 그림 1장을 만들어 줘.
- 비율 16:9, 가로 1920px 이상
- 첨부한 참고 이미지의 네 캐릭터(박사, 조수, 초파리 연구원, 주판봇)를 같은 그림체·같은 외형으로, 넷 모두 등장
- 그림 안에 글자·숫자·로고를 넣지 말 것
- 얼굴과 손은 가장자리에서 떨어진 가운데 영역에, 왼쪽 아래 구석은 어둡고 단순하게
아래 영어 프롬프트를 그대로 써 줘.

Website top cover illustration, wide 16:9.
Match the art style, proportions and colors of the attached reference images exactly (if there are no reference images: 16-bit RPG style pixel art, bold dark outline, 2-3 tone shading, small highlights).
Bright daytime laboratory mood, soft natural sunlight through large windows, clean white walls, light lavender, mint and pink accents.
Scene: {장소 영어}.
All four characters together:
the chibi scientist (thin teal rectangular glasses, spiky black hair with one white streak, small ponytail at the back, white lab coat over black vest and tie) at the back center, {포즈};
the girl researcher (long pink hair with two round buns and a navy streak, blue eyes, white lab coat over lavender hoodie, jeans) at one side, {포즈};
the anthropomorphic fruit fly researcher (black body, big red compound eyes, blue helmet with a gold stripe and pink and blue cables, white lab coat over a black vest, black gloves, transparent wings), on the left facing right, {포즈};
the boxy beige retro CRT-monitor robot 주판봇 (dark green screen face with mint pixel eyes, short antenna topped with a red-brown abacus bead, gray segmented arms, two small tank treads, holding a wooden abacus), on the right facing left, {포즈}.
Visual metaphor of the topic: {주제 은유 영어, 글자 없이}.
Composition: keep every face and hand inside the central safe area (12% margin left and right, 10% top, 18% bottom); keep the bottom-left corner plain, bright and simple; the light falls on {핵심 소품}.
Mood: curious, friendly rivalry, the moment before the result.
No text, no letters, no numbers, no logos, no weapons, no cigarettes, no alcohol, no blood, no real brands.
```

고칠 때(같은 대화에서): `Same four characters, same art style and composition. Change only: {고칠 점}. Still no text.`

시리즈 전체를 한 번에 만들면 한 파일 `COVER_PROMPTS_{시리즈}.md`에 모은다: 쓰는 법 → 한눈에 보기 표(키·페이지·장소·은유) → 표지마다 표(키, 페이지, 장소, 은유, 대체 글) + 붙여 넣기 칸 → 돌려줄 파일 이름 표(`{키}.png`).

### 13-4. 받은 그림 반영

| 단계 | 할 일 |
|---|---|
| 1 확인 | 16:9(±3%), 가로 1600 이상, 그림 안 글자 없음, 네 캐릭터가 모두 있고 외형이 같은지. 다르면 무엇이 다른지 적고 쓸지 묻는다 |
| 2 변환 | WebP 1600×900·960×540, 용량 기준까지 품질을 낮춘다 |
| 3 넣기 | 아래 블록을 상단 내비 바로 아래에, `<!-- lab-cover -->`로 시작해 `<!-- /lab-cover -->`와 줄바꿈 하나로 끝나게 넣는다(앞에 줄바꿈을 더하지 않음). **블록 밖 본문은 바꾸지 않는다** |
| 4 점검 | 폭 390·768·1280에서 얼굴 잘림 없음, 콘솔 오류 0, 가로 넘침 0, 페이지 그림 합계 600 KB 이하 |

```html
<!-- lab-cover -->
<style>.cover{position:relative;margin:0;background:linear-gradient(160deg,#eef2f8,#ffffff);aspect-ratio:16/9;max-height:72vh;overflow:hidden}.cover img{display:block;width:100%;height:100%;object-fit:cover;object-position:50% 40%}.cover-chip{position:absolute;left:16px;bottom:14px;padding:4px 10px;border-radius:999px;background:rgba(255,255,255,.88);border:1px solid #d5dbe2;color:#16212b;font-size:13px}@media (max-width:600px){.cover{max-height:none}}</style>
<header class="cover" id="cover" data-img="cover_{N}">
  <picture>
    <source type="image/webp" srcset="assets/img/cover_{N}_960.webp 960w, assets/img/cover_{N}.webp 1600w" sizes="100vw">
    <img src="assets/img/cover_{N}.webp" width="1600" height="900" alt="{대체 글}" fetchpriority="high" decoding="async">
  </picture>
  <span class="cover-chip">{시리즈 이름} · {N}</span>
</header>
<!-- /lab-cover -->
```

`lab-cover` 표시가 있으므로 다시 넣거나 뺄 때 그 사이만 바꾼다. 꼬리표 점검(본문 차이 0)에서도 이 블록은 덧붙인 부분으로 본다.

### 13-5. 프롬프트

**표지 지시문만 받기**
```
첨부한 기존 페이지들(목차 포함)을 읽고, SKILL 13-1~13-3 규칙으로 표지 지시문을 만들어 줘.
한 파일 COVER_PROMPTS_{시리즈}.md에 모으고, 표지마다 "Genspark에 붙여 넣기" 칸(한국어 지시 + 영어 프롬프트)과 대체 글을 넣어 줘.
표지끼리 장소·포즈·소품이 겹치지 않게.
```

**받은 표지 반영하기**
```
첨부한 표지 그림을 13-4 절차로 반영해 줘. 그림 → 페이지 짝: {cover_index.png → index.html, …}
먼저 확인 결과(비율·크기·글자·네 캐릭터)를 보여 주고, 문제가 없으면 넣는다. <!-- lab-cover --> 블록 밖 본문은 바꾸지 않는다.
```


---

## 14. v1.3 변경: 분야, 새 어휘, 저장소 경로

### 14-1. 분야 정하기

옛 페이지는 대부분 인공지능(`ai`)이다. 페이지를 읽고 본편 2-0-1의 신호어로 분야를 추정하고, `ai`가 아니면 사용자에게 한 번 확인한다. 정한 분야는 `meta.json`과 모든 노드의 `domain`에 쓴다.

### 14-2. 데이터 형식에 더한 것 (6장)

| 필드 | 필수 | 규칙 |
|---|---|---|
| `domain` | 권장 (`check.py`는 없으면 경고) | 분야 코드 배열 `["ai"]`, `["econ","stats"]` |
| `asOf`, `jurisdiction` | `Standard`와 기준·법령 Claim | 기준일, 관할·기준 체계 (`K-IFRS` 등) |

| 새 종류 | 뜻 | 새 관계 | 뜻 |
|---|---|---|---|
| `Theory` | 이론·모형 | `lab:assumes` | 가정을 둔다 |
| `Assumption` | 가정 | `lab:derivedFrom` | 유도된다 |
| `Identity` | 항등식·정의식 | `lab:governedBy` | 기준·법령이 정한다 |
| `Standard` | 기준서·조항·법령 | `lab:supersededBy` | 개정으로 대체됨 |
| `Account` | 계정과목 | `lab:measuredBy` | 공식 지표로 잰다 |
| `Indicator` | 공식 지표 | `lab:appliesIn` | 그 관할에서 적용 |
| `Distribution` | 확률분포 | | |
| `Framework` | 경영 분석 틀 | | |

뜻과 매핑은 본편 O1-3~O1-5, 분야별로 주로 쓰는 것은 분야 팩 P9.

### 14-3. 뼈대와 등록부

- 뼈대는 분야마다 `data/backbone_{분야}.json`. 인공지능 외 분야는 분야 팩 P10 표로 처음 만든다(작성자 초안 표시, O5-3).
- 등록부는 하나다. 같은 개념이 다른 분야 페이지에 나오면 같은 ID를 쓰고 `domain`만 늘린다(본편 19-5).
- `assembler.html`(브라우저 조립기)에는 인공지능 뼈대 v0.1이 들어 있다. 다른 분야 페이지는 `retrofit.py --backbone data/backbone_{분야}.json`과 `check.py`로 조립·점검한다.

### 14-4. 미션형 페이지

미션형(긴급 미션 + A~F 공통 섹션) 페이지도 같은 방법으로 꼬리표를 단다. 두 섹션은 아웃트로 다음, 바닥글 앞이다(R7과 같은 순서). 번역판이 있는 시리즈는 한국어 원본에만 달고, 번역판은 번역 팩으로 다시 만든다(언어팩 `dataBlocks`가 `kg-raw`·`page-meta`를 번역한다).

---

---

*ai-lab-retrofit v1.3 (2026-11-02): 저장소판. 뼈대·등록부를 `data/`로 옮기고, 본편 v1.8~1.9의 분야(`domain`), 새 종류 8개·관계 6개, 분야별 뼈대를 받도록 `check.py`·`kgx.js`·`assembler.html`을 고쳤다. 표지 프롬프트의 캐릭터 외형을 설정샷 기준으로 고쳤다(14장).*

*ai-lab-retrofit v1.2 (2026-10-31): 13장 표지 보강(네 캐릭터 글 표지 지시문, 받은 그림 반영 블록)을 더했다.*

*ai-lab-retrofit v1.1 (2026-10-31): 글 표지 블록(`lab-cover`) 표시를 점검 비교에서 빼고 조립 때 보존하도록 고쳤다.*

*ai-lab-retrofit v1.0 (2026-10-25). 본편 스킬 ai-lab-explainer v1.5의 O1·O2·O5-4를 기존 페이지 전용으로 떼어 내 도구와 함께 묶었다. 2번 페이지(Dolan 외 2018 논문 도해)의 원본에 이 도구로 꼬리표를 다시 달아, 본문 차이 0과 점검 오류 0을 확인했다.*
