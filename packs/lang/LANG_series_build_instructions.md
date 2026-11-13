---
pack: lang
id: series-build-i18n
label: 번역 팩 — 미션형 시리즈 제작 지시서 + 언어팩 v1.3
version: 1.0
core_min: 1.9
tools: langpack/ (v1.3)
---

# 제작 지시서 — 인터랙티브 교육 HTML 시리즈 (한국어 원본 + 6개 외국어판)

> **저장소판 메모 (본문은 저자 원문 그대로):**
> - 이 지시서는 두 가지로 쓰인다. ① **번역 팩**: 8장(언어 전환), 13~17장(README·외국어판·언어팩·검사·전달), 실행 도구는 같은 폴더의 `langpack/`. ② **미션형 형식**: 2·4·5장이 본 스킬 4-4의 미션형 구조다.
> - 캐릭터의 성격과 자리는 캐릭터 팩 `packs/character/CHAR_lab4.md` C2를 따른다. 2-1의 역할은 그 표의 "미션형 자리"와 같다.
> - 4장의 `localStorage`(완료 표시)와 8장의 언어 기억은 본 스킬 12-2의 예외에 해당한다.
> - 대결형 페이지(본 스킬 4-1·4-2)를 번역할 때도 8장, 13~17장과 `langpack/`을 그대로 쓴다.
> - 이미 번역된 시리즈에 언어 하나만 더할 때는 `packs/task/TASK_add_lang.md`.

이 지시서 한 장으로 **기획 → 한국어 HTML 설계·제작 → 외국어판(영어·중국어·일본어·우즈베크어·러시아어·베트남어) → README → 검사 → 전달**까지 한 번에 끝낸다. 기준 작품은 「AI는 동작을 어떻게 알아보고 만들까?」(동작 AI 5-1 ~ 5-5, 글 안상선)이며, 같은 형식의 다른 시리즈에도 주제만 바꿔 그대로 쓴다.

> AI에게 줄 때: 이 파일 전체와 함께 **[0. 입력]**의 빈칸을 채워 "이 지시서대로 시리즈 전체를 만들어 줘"라고 요청한다. 이미 한국어 HTML이 있으면 "6장부터(외국어판) 진행해 줘"라고 한다.

---

## 0. 입력 (작가가 채울 것)

| 항목 | 예시 (동작 AI 시리즈) |
|---|---|
| 시리즈 제목 / 약칭 | AI는 동작을 어떻게 알아보고 만들까? / 동작 AI |
| 편 번호와 편 수 | 5-1 ~ 5-5 (다섯 편) + 첫 화면 `index.html` |
| 이야기 틀 | 새벽 두 시 골목 CCTV에서 시작하는 긴급 미션 다섯 개 |
| 등장인물 | 박사 · 조수(하루, 예명 세나) · 초파리 연구원 · 주판봇 |
| 편별 주제와 핵심 숫자 | 5-1 규칙 60.7% → 학습 99.7% … |
| 앞선 시리즈와 링크 | 3-x 딥러닝 A to Z, 4-x AI는 이미지를 어떻게 구분할까? |
| 그림·영상 | 저자가 만든 장면 그림, 캐릭터 시트, 춤 영상(10초) |
| 저자 표기 | 글 · 안상선 ((주)M-Robo 대표) |
| 공개 주소 | https://adminmrobo.github.io/<저장소>/ |
| 라이선스 | CC BY-NC 4.0 |

---

## 1. 산출물 한눈에

```
index.html                       첫 화면 (미션 목록)
5-1_<영문_이름>.html ~ 5-5_….html  각 편
index.en.html, 5-1_….en.html …   영어판 (zh, ja, uz, ru, vi도 같은 방식)
README.md                        한국어 → English → 中文 → 日本語 → Oʻzbekcha → Русский → Tiếng Việt
```

- 모든 HTML은 **한 파일에 그림·영상·데이터·스크립트를 모두 담는다**(base64). 빌드 과정 없이 브라우저로 열기만 하면 된다. 외부에서 불러오는 것은 Google Fonts(와 첫 화면의 픽셀 글꼴 Galmuri)뿐이다.
- 번역판은 **하위 폴더 없이 같은 폴더**에 `이름.언어코드.html`로 둔다. GitHub 웹 업로드는 폴더를 올릴 수 없기 때문이다.
- 파일 이름은 `편번호_영문소문자_밑줄.html`. 한 번 정하면 바꾸지 않는다(편끼리 링크·언어 전환이 이름에 기대므로).

---

## 2. 시리즈 설계

### 2-1. 이야기 틀
- 시리즈 전체를 **하나의 사건**으로 묶는다(예: 긴급 미션 다섯 개). 각 편은 "지령 → 실습으로 해결 → 남은 한계 → 다음 미션"으로 끝나 다음 편을 부른다.
- **연구실 식구**가 말풍선으로 등장한다: 박사(정리·설명), 조수(하루, 예명 세나 — 초보 독자의 질문·감탄), 초파리 연구원(다음 단계 제시), 주판봇(준비물·숫자 보고). 말풍선은 짧게, 이야기보다 개념이 앞선다.
- 하나의 **공통 소재**(예: 막대 인형)가 모든 편을 관통한다. 한 편의 결과가 다음 편의 재료가 되도록 숫자와 데이터를 이어 쓴다.

### 2-2. 편 구성표 (README에도 그대로 쓴다)
각 편마다 정한다: 제목(주제 — 부제), 다루는 내용, 난이도 ★1~5, 들어가는 것 / 나오는 것 / 다음 편으로 넘기는 질문, 핵심 숫자 1~2개(반드시 Colab 코드 실행 결과), 주요 실습 4~6개, Colab 코드 2개.

### 2-3. 숫자의 원칙
- 페이지의 모든 핵심 숫자는 **그 편의 Colab 코드를 실제로 실행한 결과**다. 코드는 시드를 고정해 언제 실행해도 같은 값이 나오게 한다.
- 브라우저 실습은 Colab 코드와 **같은 계산**을 JS로 다시 한다(난수만 브라우저 것). 숫자가 조금 달라질 수 있음을 밝힌다.
- 설명용으로 꾸민 값·그림은 각 편 푸터의 **「설명용 모형인 것」**에 무엇이 실제 계산이고 무엇이 예시인지 적는다.
- 데이터는 합성 데이터를 기본으로 하고, 실제 사람을 촬영한 데이터는 쓰지 않는다(쓰면 동의·이용 조건을 밝힌다).

---

## 3. 디자인 시스템

### 3-1. 색과 글꼴 (각 편)
```css
:root{
  --bg:#ffffff; --panel:#f6f8fa; --panel2:#eef2f6; --rule:#d5dbe2;
  --text:#16212b; --muted:#5b6874;
  --stain:#9b3fb5; --gfp:#13733a; --eye:#c9302c; --amber:#a35c00; --info:#1e55c8;
  --font:"IBM Plex Sans KR","Apple SD Gothic Neo","Malgun Gothic","Noto Sans KR",system-ui,sans-serif;
  color-scheme:light;
}
```
- 흰 배경 한 가지 테마("낮의 연구실", 본 스킬 8장). 다크 테마는 만들지 않는다. 강조색 의미를 고정한다: 초록 `--gfp` = 좋음·통과, 빨강 `--eye` = 나쁨·경보, 앰버 `--amber` = 주의·포커스·용어 밑줄, 보라 `--stain` = 숫자·잠재값, 파랑 `--info` = 정보.
- 본문 16px, 줄 간격 1.7, 문단 최대 72ch. `h1` clamp(32px,5vw,56px), `h2` clamp(24px,3vw,34px), `h3` 19px. 한국어는 `word-break:keep-all`.
- 내용 폭 `.wrap{max-width:1180px; padding:0 clamp(14px,3vw,32px)}`.
- 첫 화면(index)은 같은 계열의 **픽셀 아트 톤**: 흰 배경(#ffffff, 연한 격자 무늬 `rgba(22,33,43,.05)`), 픽셀 상자(굵은 잉크색 테두리 + 옅은 그림자), 픽셀 글꼴 Galmuri11(`--px`)과 본문 IBM Plex Sans KR(`--sans`).
- 그림은 저자가 만든 픽셀/일러스트 이미지를 `<img src="data:…">`로 넣고, 모든 그림에 내용을 설명하는 `alt`를 단다.

### 3-2. 접근성·모바일
- 모든 `canvas`에 무엇이 그려지는지 `aria-label`. 결과 문구 상자는 `aria-live="polite"`.
- `:focus-visible` 앰버 테두리, `prefers-reduced-motion`이면 애니메이션 끔.
- 휴대폰 폭 390px에서 가로 넘침이 없어야 한다. 상단 목차는 가로 스크롤, 표는 `.tw`로 감싸 가로 스크롤.
- `env(safe-area-inset-*)`로 노치 대응, `scroll-padding-top`으로 고정 메뉴 아래 앵커 위치 맞춤.

---

## 4. 첫 화면 `index.html` 구조

1. **경보 띠** (`.alarm`, 화면 맨 위 고정): 깜빡이는 빨간 램프, 흐르는 자막("!!! 긴급 미션 수신 !!! …"), 오른쪽 "미션 보기" 버튼.
2. **히어로**: 시리즈 태그(긴급 · 시리즈 제목 · 미션 번호 범위), 큰 장면 그림(MISSION RECEIVED 도장, 시각 표시), 제목 + 핵심 질문, 리드 문단, 저자 줄.
3. **LOG — 연구실 상황**: `[SYSTEM]` 줄 + 식구 네 명의 말풍선 대화.
4. **ORDER — 본부 지령서**: 등급, 질문, 임무, 조건.
5. **MISSIONS — 미션 카드 다섯 장**: 편 번호, 제목/부제, 지령 문단, 난이도, 핵심 숫자, "미션 시작" 링크, "완료" 체크(브라우저 `localStorage`에 기억) + 진행 막대(`n / 5 CLEAR`).
6. **KIT — 미션마다 들어 있는 장비**: 실습, Colab 코드, 프롬프트, 용어, 교육자 TIP 소개.
7. **SIDE — 보조 미션**: 앞선 시리즈의 관련 편 링크.
8. **푸터**: 저자, 이미지 출처, CC 라이선스.

---

## 5. 각 편 페이지 구조

순서를 지킨다. 실습 섹션은 숫자 육각형(`.hexno` 1~7), 공통 섹션은 알파벳 육각형(A~F).

| 순서 | 요소 | 내용 |
|---|---|---|
| 상단 | `nav.top` (고정) | 육각형 로고 + 편 제목(brand), 섹션 바로가기 링크, **언어 선택 상자(8장)** |
| 히어로 | `header.hero` | 배경 그림, 시리즈 알약 목록(`#series`, 현재 편 강조), 키커("동작 AI · 5-3 · 긴급 미션"), `h1`(주제 — 부제), 리드 문단, 저자 줄 + "저자 소개" 링크 |
| | `.kpis` | 이 페이지의 숫자 요약 4~6칸(값 + 설명, 출처 "(코드 1)") |
| | `aside.prereq` | 먼저 읽으면 좋은 편 (이전 편, 앞선 시리즈) |
| 1 | 미션 `#brief` | 지령 말풍선(`[SYSTEM]` + 식구 대화), 장면 그림 |
| 2~6 | 실습 섹션 | `.lvhead`(육각형 번호, `h2`, `.sub` 안내) → `.panel` 안에 `canvas` + `.ctrl`(버튼 그룹 `.group`, 슬라이더) + `.kpis`(실시간 수치) + `.insight`(해석 문구, 초록/빨강/앰버) → 필요하면 "코드 N의 결과" 표(`.tb`) |
| 7 | 한계와 다음 미션 `#limits` | 이 편으로 안 되는 것(`.pair` 비교) → 다음 편으로 넘기는 질문 |
| A | Colab 코드 `#code` | 코드 패널 2개 (9장) |
| B | AI 응용 프롬프트 `#prompt` | 프롬프트 카드 4종 (10장) |
| C | 용어 정리 `#terms` | 용어 사전 표 (11장) |
| D | 비유 모음 `#analogy` | 개념 · 일상 비유 · 사람의 지각 비유(강도: 직접/부분/없음) · 비유가 틀리는 지점 |
| E | 저자 소개와 레퍼런스 `#refs` | E-1 저자 소개(`#author`), E-2 학술 레퍼런스 [R1]…, E-3 그림과 숫자의 출처, E-4 주석 |
| F | 교육자를 위한 TIP `#teach` | 12장 |
| 마무리 | `section.outro` | "미션 5-3 완료!", 정리 그림, 식구 세 명의 한마디(박사는 핵심 3줄 목록), 편 이동(이전 편 · 처음 화면 · 다음 편) |
| 푸터 | `footer` | 편 이름 — 저자, **설명용 모형인 것**, CC 배지 + 라이선스 문장 + 출처 표기 예 |

### 공통 JS (각 편 같은 코드)
- 작은 도우미 `U`: `U.$`(id 찾기), `U.fit`(canvas를 화면 폭과 기기 픽셀비에 맞춤), `U.rng`(시드 난수), `U.kpis`(수치 칸 그리기), `U.seg`(버튼 그룹 선택), `U.playBtn`(재생/멈춤), `U.pct`, `U.COL`(색), `U.onResize`.
- 애니메이션은 한 개의 타이머 루프(초당 15프레임)에 모아 돌린다.
- 시리즈 알약 목록은 JS 배열 하나에서 만들어 모든 편이 같다.
- 페이지 안 바로가기는 해시 이동 대신 스크립트로 스크롤(고정 메뉴 높이만큼 보정; GitHub 미리보기·iframe에서도 작동).
- 숫자·데이터 묶음(학습된 가중치 등)은 base64 Float32 배열로 넣고 브라우저에서 풀어 쓴다.

---

## 6. 한국어 문체

- 독자는 초보자. 짧은 평서문(~다), 한 문장에 개념 하나. 처음 나오는 용어는 쉬운 말로 먼저 풀고 괄호에 정식 용어.
- 시리즈 고유 비유를 정하고 끝까지 같은 말로 쓴다(예: 잠재 변수 = **손잡이(잠재 변수)**, 인코더 = 깔때기). README의 「용어 표기」에 이유를 적는다.
- 숫자에는 출처를 붙인다("(코드 2)"). 과장하지 않고 한계를 반드시 쓴다.
- 말풍선은 캐릭터 말투를 유지하되 한두 문장.

---

## 7. 인터랙티브 실습 규칙

- 실습마다 **손으로 바꾸는 것 → 바로 바뀌는 그림 → 바뀌는 숫자 → 한 줄 해석**의 고리를 만든다.
- 해석 문구(`.insight`)는 상황에 따라 색(통과 초록, 실패 빨강, 주의 앰버)과 문장을 바꾼다.
- 재생형 실습은 ▶ 재생 / ❚❚ 멈춤 버튼, 프레임 표시("프레임 12 / 46").
- 캔버스 안 글자는 짧게(번역 시 길어진다). 긴 설명은 캔버스 밖 HTML로.
- 실습 아래에 "코드 N의 결과" 표를 두어 브라우저 결과와 Colab 결과를 견준다.

---

## 8. 언어 전환 UI (한국어 원본에도 넣는다)

모든 페이지에 두 가지를 **함께** 넣는다.

1. **최상단 메뉴의 언어 선택 상자** `🌐 [언어 ▾]`
   - 각 편: `nav.top`의 제목(brand) 바로 옆.
   - 첫 화면: 경보 띠의 "미션 보기" 버튼 앞.
2. **오른쪽 아래 🌐 배너**: 화면 오른쪽 아래 고정 둥근 버튼(현재 언어 이름). 누르면 7개 언어 목록, 현재 언어는 앰버. Esc·바깥 클릭으로 닫힘. 인쇄 시 숨김.

언어 순서와 표시 이름: 한국어 · English · 中文 · 日本語 · Oʻzbekcha · Русский · Tiếng Việt

### 전환 동작 (`<head>`의 `<meta charset>` 바로 뒤에 넣는 작은 스크립트)
- 저장 키 하나(예: `motion_ai_lang`)를 `localStorage`에 쓴다. 메뉴·배너에서 고르면 저장하고 같은 페이지의 그 언어 파일로 이동(`#섹션` 유지).
- `?lang=xx`가 있으면 저장하고 그 언어로 연다.
- **한국어 페이지에서만** 자동 전환: 저장된 언어, 없으면 브라우저 언어(`navigator.languages` 앞 두 글자)가 지원 언어면 이동. 지원하지 않는 언어는 한국어 그대로.
- **404 방지**: 이동 전에 `fetch(…, {method:'HEAD'})`로 번역 파일이 있는지 확인하고 없으면 머문다. 확인하는 동안만 화면을 숨기고 2.5초 뒤에는 무조건 보인다. `file://`로 열었을 때는 저장된 선택만 따른다.
- 번역판 주소로 들어온 사람은 자동 전환하지 않는다(공유한 영어 링크는 영어로 열린다).
- 각 파일에 `<link rel="alternate" hreflang="ko|en|zh-CN|ja|uz|ru|vi|x-default">`.

---

## 9. Colab 코드 (각 편 2개)

- Colab 기본 설치 라이브러리만(numpy, matplotlib, scikit-learn, OpenCV). 시드 고정.
- 머리 주석 형식:
  ```
  # ===============================================================
  # 5-3 인코더·디코더 · 코드 1: 동작을 숫자 k개로 접었다 펼치기 (선형 오토인코더 = PCA)
  #  - 라이브러리: numpy, matplotlib (Colab 기본 설치)
  #  - 실행 확인: 2026-10-05, numpy 2.4 · matplotlib 3.10 (CPU 약 3초)
  #  - 하는 일: ① … ② … ③ …
  #  - 웹페이지 섹션 2~4의 숫자와 같다. 시드를 고정해 언제 실행해도 같다.
  # ===============================================================
  ```
- 셀 구분은 `# ---------- 제목 ----------` 줄로(노트북 변환 시 셀이 나뉜다).
- 코드 원문은 `<script type="text/plain" id="src-code1">`에 넣고, 패널(`.codepanel`)에서 색칠해 보여 준다.
- 패널 머리: "코드 1 · 제목", "섹션 2·3과 연결 · 라이브러리 · CPU 시간", 버튼 **복사 · .py 내려받기 · 노트북(.ipynb) 내려받기**. 노트북 첫 셀은 제목·저자·라이선스 마크다운.
- `.codenote`: 하는 일 + **내 데이터로 바꾸려면** 안내.
- 실행 결과(`figure.runshot`): 실제 출력 텍스트 + 실행 날짜·버전·CPU.
- 외부 파일이 필요한 코드(예: 영상)는 무엇을 어디에 올리는지 적는다.

## 10. AI 응용 프롬프트 (B)

카드 4종, 각 카드에 제목 · 언제 쓰나 · 팁 · 프롬프트 본문. "복사"를 누르면 프롬프트 뒤에 고른 코드(코드 1/2 선택)가 붙는다.
1. 응용 분야 찾기 2. 해커톤 48시간 계획 3. 공모전 기획서 초안 4. 논문 실험 설계
아래에 주의 문구: AI의 답은 출발점, 논문·수치·함수는 원문 확인, 실제 사람 데이터는 동의·이용 조건 확인.

## 11. 용어 사전 (C)과 말풍선

- JS 객체 하나 `GL = { "용어": ["용어 (English term)", "분야", "뜻 한두 문장", "처음 나온 섹션 id"], … }`.
- 본문에서 키와 같은 글자를 찾아 **노란 점선 밑줄 + 말풍선**을 자동으로 단다(블록마다 처음 한 번만, 제목·버튼·캔버스·코드는 제외).
- C 섹션 표는 GL에서 만든다: 용어 · 영어 · 뜻 · 처음 나온 곳(섹션 링크). 제목의 괄호를 기준으로 "용어"와 "영어"를 나눈다.

## 12. 교육자를 위한 TIP (F)

1. 운영안 세 가지 표(예: 강의형 50분 / 실습형 90분 / 과제형), 단계별 시간 배분
2. 섹션별 운영 포인트 표
3. 흔한 오해 Top 5 표(오해 · 바로잡기)
4. 확인 문제 5개 — `<details><summary>Q1. …</summary><p>해설</p></details>`
5. Colab 과제(기본 · 심화)
6. 난이도 조절과 더 배우기 표

---

## 13. README.md

### 한국어 부분 (원본)
제목 → 한 문단 소개 → **바로 보기** 주소 → 저자 → **언어**(13-2) → 구성(편 표: 편 · 제목 · 다루는 내용 · 난이도) → 막대 인형이 걸어온 길(들어가는 것 · 나오는 것 · 다음 질문) → 각 편의 핵심 숫자 → 각 편에 들어 있는 것 + 주요 실습 표 → Colab 코드 표(코드1 · 코드2 · 라이브러리 · 실행 시간) → 파일(구조 블록 + 크기 표) → 먼저 읽으면 좋은 편 → 데이터와 이미지(설명용 모형 표) → 용어 표기 → 라이선스(출처 표기 예).

### 13-2. 「언어」 절
- 고르는 방법(최상단 메뉴의 🌐 선택 상자, 오른쪽 아래 🌐 배너, 고른 언어 기억), 자동 전환, `?lang=`
- 언어 예외가 있는 편(예: 5-4)
- 표: 언어 · 파일 이름 · 바로 보기 주소(`index.en.html` …)
- 파일 구조 블록에 `*.en.html *.zh.html *.ja.html` / `*.uz.html *.ru.html *.vi.html` 줄 추가

### 13-3. 다국어 README 조립
- 맨 위: `**[한국어](#ko) · [English](#en) · [中文](#zh) · [日本語](#ja) · [Oʻzbekcha](#uz) · [Русский](#ru) · [Tiếng Việt](#vi)**`
- `---` + `<a id="ko"></a>` + 한국어 전체 → 영어 → 중국어 → 일본어 → 우즈베크어 → **러시아어 → 베트남어(러시아어·베트남어는 지정 순서 밖이라 맨 끝)**.
- 각 언어 부분의 이 시리즈 링크는 그 언어 파일로(`5-1_….html` → `5-1_….en.html`, 사이트 주소 → `index.en.html`). 다른 시리즈 링크와 언어 표의 링크는 그대로. CC 링크는 언어별 deed.

---

## 14. 외국어판 HTML 규칙

### 14-1. 언어

| 코드 | 언어 | 표시 이름 | `<html lang>` | 추가 글꼴 | CC deed |
|---|---|---|---|---|---|
| `ko` | 한국어 (원본) | 한국어 | `ko` | — | `deed.ko` |
| `en` | 영어 | English | `en` | IBM Plex Sans | `deed.en` |
| `zh` | 중국어 간체 | 中文 | `zh-CN` | Noto Sans SC | `deed.zh-hans` |
| `ja` | 일본어 | 日本語 | `ja` | Noto Sans JP | `deed.ja` |
| `uz` | 우즈베크어(라틴) | Oʻzbekcha | `uz` | IBM Plex Sans | `deed.en` |
| `ru` | 러시아어 | Русский | `ru` | IBM Plex Sans | `deed.ru` |
| `vi` | 베트남어 | Tiếng Việt | `vi` | IBM Plex Sans (vietnamese 하위 집합 포함) | `deed.vi` |

### 14-2. 번역판을 만들 때 같이 바꾸는 것
- `<html lang>`, 글꼴(`--font`/`--sans` 앞에 추가 글꼴, `--px`도 대체 글꼴 포함), CC 링크.
- **편끼리 링크**(HTML의 href와 JS 문자열 모두): `5-2_….html` → `5-2_….en.html`, `index.html` → `index.en.html`. 절대 주소(앞에 `/`가 있는 것)와 다른 시리즈 링크는 그대로.
- 언어 UI(8장)를 넣은 뒤 링크 변환을 하면 배너의 한국어 링크까지 바뀌므로 **링크 변환 → UI 삽입** 순서를 지킨다.
- **베트남어 글꼴**: 첫 화면의 픽셀 글꼴 Galmuri에는 베트남어 성조 부호가 없을 수 있으므로 vi판의 `--px`는 `"Galmuri11","IBM Plex Sans",monospace`처럼 대체 글꼴을 바로 뒤에 둔다.
- **중국어·일본어 줄바꿈**: 원본의 `word-break:keep-all`을 `*{word-break:normal!important;line-break:strict}`로 덮어쓴다.
- **용어 말풍선**(en·uz·ru·vi): 용어 찾기 정규식에 `'i'` 플래그, 말풍선 조회도 대소문자 무시.

### 14-3. 번역 범위
- 옮긴다: HTML 본문, `<title>`, `meta description/og`, `alt`, `title`, `aria-label`, `placeholder`, 표 머리글 HTML이 든 속성, JS 문자열(버튼, 캔버스 글자, 결과 문구, 퀴즈, 용어 사전, 프롬프트, 말풍선, 토스트), Colab 코드의 **주석·docstring·print 문구**.
- 옮기지 않는다: 코드 식별자·숫자·연산자·f-string 식, 단위, 파일 이름, URL, 고유 명칭(Colab, YOLO, OpenPose, MediaPipe, numpy, CAM-07, MISSION RECEIVED, `[SYSTEM]`), 이모지·화살표·원문자(→ ▶ ❚❚ ①②), 편 번호, CSS·JS 주석, 그림 파일 속 글자.
- 번역판 화면에 한국어가 남으면 안 된다(14-5 예외만 허용).

### 14-4. 코드와 엮인 문자열
- **같은 한국어 문자열 = 사이트 전체에서 같은 번역 하나.** JS 비교(`===`)·객체 키·용어 키가 어긋나지 않는다.
- 숫자와 이어 붙는 조각(`n+'개'`, `'정확도 '+x+'%'`)은 이어 붙인 결과가 자연스럽게, 이음매 띄어쓰기 유지(en·uz·ru·vi는 단위 앞 띄어쓰기, zh·ja는 띄어쓰기 없이).
- 캔버스 라벨은 한국어와 비슷한 길이로 짧게.
- 태그·속성·엔티티(`&nbsp;`)·JS 따옴표 안전(ASCII 따옴표가 문자열을 깨지 않게) 유지.
- 같은 데이터(관절 이름 등)를 Python과 JS가 함께 쓰면 두 곳을 같은 말로.

### 14-5. 언어 자체를 다루는 실습의 예외
한국어 입력이 있어야만 작동하는 실습(예: 5-4 단어 주머니 — 한국어 단어 조각 40개로 학습)은:
- 모델에 넣는 예시 문장·단어 조각·연결어("다가", "고 나서")와 데이터 배열(VOCAB, CAPTIONS 등)을 **한국어로 두고**, 화면에 처음 나올 때 괄호로 뜻을 붙인다: en `"캔을 던진다" (throws a can)`.
- 같은 데이터를 쓰는 Colab 코드의 데이터 문자열도 한국어로 두고 주석만 옮긴다(결과 숫자가 그대로 맞도록).
- 그 밖의 편에서 인용한 프롬프트("춤춰")는 정상 번역(en "Dance!").

### 14-6. 용어 사전(GL)
- 제목은 `번역어 (English term[, 덧붙임])` 형식 유지(괄호로 칸을 나누므로). zh·ja·uz·ru·vi: `边界框 (Bounding box)`, `Khung bao (Bounding box)`.
- en: 괄호가 같은 말 반복이면 빼고(`Bounding box`), 별칭이 있을 때만 남김(`Keypoint (joint)`). 표 머리글 "영어"는 영어판에서만 "Also known as".
- 키는 번역 본문에 그대로 나오는 가장 짧은 형태(en·uz·ru·vi는 소문자).

### 14-7. 언어별 문체
- **en:** 쉬운 교재 영어, 짧은 문장.
- **zh:** 간체자, 평서문.
- **ja:** 본문과 설명은 부드러운 です・ます체, 말풍선은 자연스러운 구어. 판정만 짧게 끊는다.
- **uz:** 라틴 문자 표준 문어, oʻ·gʻ는 U+02BB(ʻ), 끊음 표시는 U+02BC(ʼ, 공개된 번역판과 같음), 독자는 siz. 딱딱한 관청 문체보다 부드러운 설명체.
- **ru:** 중립적 과학 대중서 문체, 독자는 «вы».
- **vi:** 쉽고 친근한 교재체 평서문, 독자는 "bạn". 성조·발음 부호를 빠짐없이 쓰고(유니코드 NFC), 한자어보다 일상어를 먼저 쓴 뒤 괄호에 정식 용어.
- 숫자·소수·단위 그대로. 천 단위 구분은 en·zh·ja `6,220,800`, ru·uz `6 220 800`도 가능. vi는 원본 표기(`6,220,800`, 소수점 `.`)를 그대로 둔다 — 화면 숫자와 코드 출력이 어긋나지 않게.
- 뜻을 옮기고 정보를 더하거나 빼지 않는다. 미션 이야기의 재미는 살린다.

### 14-8. 고정 용어표
저자·등장인물·시리즈 고유 용어는 아래를 따른다(새 시리즈는 이 표에 행을 더한다). 그 밖의 기술 용어는 각 언어의 표준 용어.


| 한국어 | en | zh | ja | uz | ru | vi |
|---|---|---|---|---|---|---|
| AI는 동작을 어떻게 알아보고 만들까? (시리즈 제목) | How Does AI Recognize and Create Motion? | AI 如何识别和生成动作？ | AIは動作をどう見分け、どう作るのか？ | AI harakatni qanday taniydi va yaratadi? | Как ИИ распознаёт и создаёт движения? | AI nhận biết và tạo ra chuyển động như thế nào? |
| 동작 AI (시리즈 약칭) | Motion AI | 动作 AI | 動作AI | Harakat AI | ИИ движений | AI chuyển động |
| 긴급 미션 / 최종 미션 | Emergency mission / Final mission | 紧急任务 / 最终任务 | 緊急ミッション / 最終ミッション | Shoshilinch missiya / Yakuniy missiya | Срочная миссия / Финальная миссия | Nhiệm vụ khẩn cấp / Nhiệm vụ cuối cùng |
| 안상선 ((주)M-Robo 대표) | Ahn Sangsun (CEO, M-Robo Co., Ltd.) | Ahn Sangsun（M-Robo 株式会社代表） | アン・サンソン（株式会社M-Robo代表） | Ahn Sangsun (M-Robo kompaniyasi rahbari) | Ан Сансон (генеральный директор M-Robo Co., Ltd.) | Ahn Sangsun (Giám đốc điều hành, M-Robo Co., Ltd.) |
| 글 · 안상선 | Written by Ahn Sangsun | 作者 · Ahn Sangsun | 文・アン・サンソン | Muallif · Ahn Sangsun | Автор · Ан Сансон | Tác giả · Ahn Sangsun |
| 박사 | the Doctor | 博士 | 博士 | Doktor | Доктор | Tiến sĩ |
| 조수 | the Assistant | 助手 | 助手 | Yordamchi | Ассистент | Trợ lý |
| 조수(하루) | the Assistant (Haru) | 助手（Haru） | 助手（ハル） | Yordamchi (Haru) | ассистент (Хару) | Trợ lý (Haru) |
| 세나 (조수의 예명) | Sena | Sena | セナ | Sena | Сена | Sena |
| 초파리 연구원 | the Fruit Fly Researcher | 果蝇研究员 | ショウジョウバエ研究員 | Meva pashshasi tadqiqotchisi | Исследователь-дрозофила | Nhà nghiên cứu Ruồi giấm |
| 주판봇 | AbaBot | 算盘宝 | アバボット | AbaBot | АбаБот | AbaBot |
| 연구실 (식구들) | the lab (crew) | 研究室（成员） | 研究室（の仲間たち） | laboratoriya (jamoasi) | лаборатория (команда) | phòng thí nghiệm (các thành viên) |
| 본부 | HQ | 总部 | 本部 | shtab | штаб | Sở chỉ huy |
| 막대 인형 | stick figure | 火柴人 | 棒人間 | chiziqcha odam | человечек-палочка (стик-фигура) | người que |
| 쓰레기 (무단) 투기 | (illegal) littering / dumping | （乱扔）垃圾 / 乱扔垃圾 | ゴミの（不法）投棄 | chiqindini (noqonuniy) tashlash | (незаконный) выброс мусора | (lén) vứt rác / xả rác bừa bãi |
| 투기 / 정상 (판정 이름) | Littering / Normal | 乱扔 / 正常 | 投棄 / 正常 | Tashlash / Normal | Выброс / Норма | Xả rác / Bình thường |
| 판정보류 | abstain ("no call") | 暂不判定 | 判定保留 | qaror kechiktirildi | воздержание от решения | tạm hoãn phán định |
| 관제실 (라이브 관제실) | control room (live control room) | 监控室（实时监控室） | 管制室（ライブ管制室） | nazorat xonasi (jonli nazorat xonasi) | диспетчерская (живая диспетчерская) | phòng giám sát (phòng giám sát trực tiếp) |
| 관절 | joint (keypoint) | 关节（关键点） | 関節（キーポイント） | boʻgʻim (kalit nuqta) | сустав (ключевая точка) | khớp (điểm mốc) |
| 특징 | feature | 特征 | 特徴 | belgi (xususiyat) | признак | đặc trưng |
| 규칙 대 학습 | rules vs. learning | 规则 vs 学习 | ルール対学習 | qoida va oʻrganish | правила против обучения | quy tắc và học |
| 헛경보 / 놓침 | false alarm / miss | 误报 / 漏报 | 誤報 / 見逃し | soxta signal / oʻtkazib yuborish | ложная тревога / пропуск | báo động giả / bỏ sót |
| 판별 모델 / 생성 모델 | discriminative model / generative model | 判别模型 / 生成模型 | 識別モデル / 生成モデル | diskriminativ model / generativ model | дискриминативная / генеративная модель | mô hình phân biệt / mô hình sinh |
| 생성기 (A~E) | generator (A–E) | 生成器 | 生成器 | generator | генератор | bộ sinh (A–E) |
| 감독관 (채점표) | the Evaluator (score sheet) | 评审员（评分表） | 審査官（採点表） | Nazoratchi (baholash varaqasi) | Эксперт (оценочный лист) | Giám khảo (phiếu chấm điểm) |
| 진짜 같음 · 다양성 · 새로움 | realism · diversity · novelty | 逼真度 · 多样性 · 新颖性 | 本物らしさ・多様性・新しさ | haqqoniylik · xilma-xillik · yangilik | правдоподобие · разнообразие · новизна | độ chân thực · độ đa dạng · độ mới |
| 뼈 길이 오차 | bone-length error | 骨长误差 | 骨の長さの誤差 | suyak uzunligi xatosi | ошибка длины костей | sai số độ dài xương |
| 손잡이(잠재 변수) | knob (latent variable) | 旋钮（潜变量） | つまみ（潜在変数） | dasta (yashirin oʻzgaruvchi) | ручка (латентная переменная) | núm vặn (biến tiềm ẩn) |
| 손잡이 | knob | 旋钮 | つまみ | dasta | ручка | núm vặn |
| 잠재 지도 / 잠재 공간 | latent map / latent space | 潜在地图 / 潜在空间 | 潜在マップ / 潜在空間 | yashirin xarita / yashirin fazo | латентная карта / латентное пространство | bản đồ tiềm ẩn / không gian tiềm ẩn |
| 깔때기 (말 깔때기, 동작 깔때기) | funnel (text funnel, motion funnel) | 漏斗（文字漏斗、动作漏斗） | じょうご（言葉じょうご、動作じょうご） | voronka (soʻz voronkasi, harakat voronkasi) | воронка (текстовая, двигательная) | phễu (phễu chữ, phễu chuyển động) |
| 인코더 · 디코더 | encoder · decoder | 编码器 · 解码器 | エンコーダ・デコーダ | enkoder · dekoder | кодировщик · декодер (энкодер · декодер) | bộ mã hóa · bộ giải mã |
| 병목 | bottleneck | 瓶颈 | ボトルネック | tor boʻgʻiz (bottleneck) | узкое место (бутылочное горлышко) | nút thắt cổ chai |
| 떨림 / 가림 | jitter / occlusion | 抖动 / 遮挡 | 揺れ / 隠れ | titrash / toʻsilish | дрожание / перекрытие | rung / che khuất |
| 단어 주머니 | bag of words | 词袋 | 単語袋（バッグ・オブ・ワーズ） | soʻzlar xaltasi | мешок слов | túi từ |
| 사전 (조각) | dictionary (pieces) | 词典（片段） | 辞書（かけら） | lugʻat (boʻlaklar) | словарь (фрагменты) | từ điển (mảnh từ) |
| 짝 맞추기 | pair matching | 配对 | ペア合わせ | juftlash | подбор пар | ghép cặp |
| 대조 학습 | contrastive learning | 对比学习 | 対照学習 | kontrastiv oʻrganish | контрастивное обучение | học tương phản |
| 공유 지도 / 같은 지도 | shared map / the same map | 共享地图 / 同一张地图 | 共有マップ / 同じ地図 | umumiy xarita / bitta xarita | общая карта / одна карта | bản đồ chung / cùng một bản đồ |
| 찾기 · 만들기 · 이어 붙이기 | find · make · stitch | 查找 · 生成 · 拼接 | 探す・作る・つなぐ | topish · yaratish · ulash | найти · создать · склеить | tìm · tạo · nối |
| 포즈 맵 | pose map | 姿态图 | ポーズマップ | poza xaritasi | карта позы | bản đồ tư thế |
| 참조 이미지 | reference image | 参考图像 | 参照画像 | namuna rasm | референсное изображение | ảnh tham chiếu |
| 동작 일치율 | motion match score | 动作一致率 | 動作一致率 | harakat mosligi | процент совпадения движений | tỉ lệ khớp chuyển động |
| 나란히 보기 | side-by-side view | 并排查看 | 並べて見る | yonma-yon koʻrish | просмотр бок о бок | xem song song |
| 교육자를 위한 TIP / 교육자 TIP | Tips for educators / Educator tips | 教师指南 / 教师 TIP | 教育者向けTIP | Oʻqituvchilar uchun maslahatlar | Советы преподавателям | Mẹo cho người dạy / Mẹo giảng dạy |
| 확인 문제 | check questions | 练习题 | 確認問題 | nazorat savollari | проверочные вопросы | câu hỏi kiểm tra |
| 용어 정리 / 용어 사전 | glossary | 术语表 | 用語集 | atamalar lugʻati | глоссарий | bảng thuật ngữ |
| 비유 / 비유가 틀리는 지점 | analogy / where the analogy breaks | 比喻 / 比喻失效之处 | たとえ / たとえが外れるところ | oʻxshatish / oʻxshatish notoʻgʻri boʻladigan joy | аналогия / где аналогия не работает | phép so sánh / chỗ phép so sánh không đúng |
| 레퍼런스 | references | 参考文献 | 参考文献 | manbalar | источники | tài liệu tham khảo |
| 설명용 모형인 것 | what is an illustrative mock-up | 仅供说明的示意部分 | 説明用の模型であるもの | tushuntirish uchun maket boʻlgan narsalar | что здесь — иллюстративный макет | những gì là mô hình minh họa |
| 코드 1 / 코드 2 | Code 1 / Code 2 | 代码 1 / 代码 2 | コード1 / コード2 | 1-kod / 2-kod | Код 1 / Код 2 | Mã 1 / Mã 2 |
| 복사 · .py 내려받기 · 노트북 내려받기 | Copy · Download .py · Download notebook | 复制 · 下载 .py · 下载笔记本 | コピー・.pyをダウンロード・ノートブックをダウンロード | Nusxalash · .py yuklab olish · Notebook yuklab olish | Копировать · Скачать .py · Скачать ноутбук | Sao chép · Tải .py · Tải notebook |
| 딥러닝 A to Z (3-x 시리즈) | Deep Learning A to Z | 深度学习 A to Z | ディープラーニング A to Z | Chuqur oʻrganish A dan Z gacha | Глубокое обучение от A до Z | Học sâu từ A đến Z |
| AI는 이미지를 어떻게 구분할까? (4-x 시리즈) | How Does AI Tell Images Apart? | AI 如何区分图像？ | AIは画像をどう見分けるのか？ | AI rasmlarni qanday ajratadi? | Как ИИ различает изображения? | AI phân biệt hình ảnh như thế nào? |
| 크리에이티브 커먼즈 저작자표시-비영리 4.0 국제 라이선스(CC BY-NC 4.0) | Creative Commons Attribution-NonCommercial 4.0 International License (CC BY-NC 4.0) | 知识共享 署名-非商业性使用 4.0 国际许可协议（CC BY-NC 4.0） | クリエイティブ・コモンズ 表示-非営利 4.0 国際ライセンス（CC BY-NC 4.0） | Creative Commons Attribution-NonCommercial 4.0 International litsenziyasi (CC BY-NC 4.0) | лицензия Creative Commons «Атрибуция — Некоммерческое использование» 4.0 Международная (CC BY-NC 4.0) | Giấy phép Creative Commons Ghi công – Phi thương mại 4.0 Quốc tế (CC BY-NC 4.0) |

---

## 15. 외국어판 제작 절차 — 언어팩 v1.3으로 실행

손으로 HTML을 고치지 않는다. 외국어판은 **언어팩**(`langpack_v1.3.zip`)으로 만든다. 언어팩이 문장 단위 추출·번역 메모리·번역 검사·조립·언어 전환 UI·README 조립·브라우저 검사를 맡는다. 자세한 사용법은 언어팩의 `README.md`.

1. **준비**: 저장소 루트에 `langpack/`을 두고 `config.example.json`을 `config.json`으로 복사한다. 시리즈마다 정할 것:
   - `pages`, `siteUrl`(공개 주소), `langStorageKey`(예: `motion_ai_lang`), `readme`
   - `switcherHosts`: 각 편은 기본값(`nav.top .brand` 뒤), 첫 화면은 `[".alarm .go","before"]`를 앞에 둔다.
   - `fontVars`: `["--font","--sans"]`
2. **용어표**: 14-8의 시리즈 고유 용어를 `rules/glossary/20_topic_<시리즈>.json`으로 옮긴다. 캐릭터·저자 이름은 `00_series.json`에 이미 있다.
3. **추출과 왕복 검사**: `extract` → `roundtrip`(OK여야 다음으로) → `seed` → `pending all`.
4. **번역**: 언어마다 하위 에이전트 하나(en·zh·ja Haiku급, ru·uz·vi Sonnet급) 또는 `api_translate.py`. 묶음은 에이전트 실행이면 언어당 하나(3만 자).
5. **검사**: `check` → 실패분은 `retry`로 모아 한 번 더.
6. **조립**: `merge`가 HTML 번역판, `dist/README.md`(7개 언어, 「언어」 절 포함), Colab 코드 compile 검사를 한다. `codecheck --run`으로 코드를 실제 실행한다.
7. **브라우저 검사**: `node langpack/browser_check.js --shots` → "모두 통과".

언어팩이 하지 않는 것(작가가 원본에서 처리):
- **편끼리 링크 변환(14-2)**: 번역판의 다른 편 링크는 한국어 파일을 가리킨다. 언어 전환 스크립트가 기억된 언어로 다시 옮겨 준다.
- **용어 말풍선의 `i` 플래그(14-2)**: 페이지 코드에 맞춰 `postReplaceRegex`로 한 번 정해 둔다.
- **언어 자체를 다루는 실습(14-5)**: 한국어로 남길 데이터 배열은 `skipVars`·`data-i18n-skip`으로 빼고, 괄호 뜻풀이는 원본에 쓴다.
- **바깥 파일의 글자**: 화면 글자는 HTML 안에 둔다(1장: 한 파일에 모두 담는다).

## 16. 검사 (전달 전에 모두 통과)

- [ ] 모든 `<script>`가 구문 오류 없이 파싱된다(42개 파일).
- [ ] 7개 언어 × 모든 페이지를 헤드리스 브라우저로 열고 버튼을 모두 눌러 본다: 스크립트 오류 0, 화면·`alt`·`aria-label`에 남은 한국어 0(14-5 예외만).
- [ ] 페이지 안 Colab 코드를 모든 언어에서 `compile()` + 실제 실행(외부 파일이 필요한 코드 제외) → 오류 0.
- [ ] 자동 전환: 브라우저 언어 en/ja/zh/uz/ru/vi → 해당 파일, de/ko → 한국어. 고른 언어 기억, `?lang=`, `#섹션` 유지, 편끼리 링크가 같은 언어로 이어짐.
- [ ] 최상단 메뉴의 언어 선택 상자와 🌐 배너가 데스크톱(1280px)·휴대폰(390px)에서 보이고 작동한다. 가로 넘침 없음.
- [ ] 베트남어 성조 부호가 글꼴 깨짐 없이 보인다(제목·픽셀 글꼴·캔버스 글자).
- [ ] 중국어·일본어 줄바꿈 정상, 용어 밑줄·말풍선 정상, 용어 표 머리글 정상.
- [ ] 스크린샷으로 실습 섹션 몇 곳을 눈으로 확인(캔버스 글자 넘침).

---

## 17. 전달

- 저장소 루트에 그대로 올릴 수 있게 **폴더 없이** HTML(한국어 6 + 번역 36)과 `README.md`를 묶는다.
- 압축 파일 하나가 30MB를 넘으면 나눈다: ① 한국어 + en + zh + README ② ja + uz + ru ③ vi (언어 하나가 압축 후 약 7MB).
- 전달 글에 적을 것: 언어 전환 방식(최상단 메뉴·🌐 배너·자동 전환·기억·`?lang=`), 확인한 것, 언어 예외가 있는 편, 그림 속 글자는 그대로라는 점, 다른 시리즈 링크는 한국어로 연결된다는 점, README 러시아어·베트남어는 순서 밖이라 맨 끝에 붙였다는 점, **원어민 검수 전**(특히 우즈베크어·러시아어·베트남어).
