# old_skill — 폐기·구형 스킬 보관소

더 이상 쓰지 않는 스킬과 개정 전 판을 날짜별로 보관한다. 이 폴더의 파일은 **불러와 쓰지 않는다**. 현재 판은 Claude 계정 스킬과 저장소 루트를 따른다.

## 2026-11-23 (2) — 픽셀 깨짐 보정 코드 도입 전 판
| 폴더 | 무엇 | 상태 |
|---|---|---|
| `ai-lab-explainer_v1.16` | 본 스킬(표지·캐릭터 그림에 `image-rendering:pixelated`를 강제하던 판) | v1.17로 대체(18-15-3 보정 코드) |
| `ai-lab-retrofit_v1.5` | 온톨로지 보강 팩(표지 인라인 `pixelated`, 꾸러미 조수 얼굴 각진 픽셀 고정) | v1.6으로 대체 |
| `ai-lab-explainer-plain_v1.3` · `ai-lab-report-news_v1.3` · `ai-lab-report-finding_v1.3` | 표지 규격에 `pixelated`가 있던 판 | v1.4로 대체 |

## 2026-11-23 — 픽셀아트 표지 변환·꾸러미 조수 그림 개정 전 판
| 폴더 | 무엇 | 상태 |
|---|---|---|
| `ai-lab-explainer_v1.15` | 본 스킬(표지를 1600×900 손실 WebP로 줄이던 판) | v1.16으로 대체 |
| `ai-lab-retrofit_v1.4` | 온톨로지 보강 팩(꾸러미 조수가 글자 상자이던 `kgx.js`·`assembler.html` 포함) | v1.5로 대체 |
| `ai-lab-explainer-plain_v1.2` · `ai-lab-report-news_v1.2` · `ai-lab-report-finding_v1.2` | 표지 1600×900 문구가 있던 판 | v1.3으로 대체 |

## 2026-11-21 — 교수법 스킬 통합
| 폴더 | 무엇 | 상태 |
|---|---|---|
| `teaching-method_v1.1` | 첫 교수법 스킬(원리 먼저 7원칙 P1~P7, 개념 리듬 ①~⑧, 검토 모드) | 폐기 |
| `concept-first-teaching_v1.0` | 위 스킬의 이름만 바꾼 판 | 폐기 |
| `ai-lab-explainer-plain_v1.1` | 교수법을 외부 스킬로 불러오던 판 | v1.2로 대체(교수법 9장 내장) |
| `ai-lab-extend_v1.1` | 〃 | v1.2로 대체(교수법 8장 내장, 교안·슬라이드·퀴즈 검토 포함) |
| `ai-lab-report-news_v1.1` | 〃 | v1.2로 대체(교수법 11장 내장) |
| `ai-lab-report-finding_v1.1` | 〃 | v1.2로 대체(교수법 10장 내장) |

교수법 내용은 따로 두지 않고 위 네 스킬 안에 모두 옮겼다.
