# 특별편 동작·의상 스프라이트 — Genspark 프롬프트

대상 페이지: `sp_tensor_fight.html` · 작성 2026-11-08 · 캐릭터 기준: CHAR_lab4 18-3(그림체)·18-4(고정 외형)·C5(뒤집기)·C6(추가 팩)

## 왜 필요한가
지금 특별편의 '행동' 축(서기·점프·돌진·필살기)과 '복장' 축(연구복·전투복·사이버)은 **얼굴 표정 그림 한 장을 위아래로 흔들고 색만 바꿔서** 흉내 내고 있습니다. 전신 동작 프레임이 없어서 필살기를 눌러도 몸이 움직이지 않습니다. 아래 시트를 받으면 프레임을 잘라 캔버스에서 실제로 재생하고, 텐서 효과(원-핫 칸, 등고선, 특이값 막대 등)는 코드가 그 위에 그립니다.

## 넣는 방법 (모든 프롬프트 공통)
1. **참고 그림을 꼭 첨부:** 그 캐릭터의 기본 표정 그림 192px(`doc_front`, `asst_smile`, `fly_clip`, `robo_smile`)과 설정샷 3면도(k02 박사, k03 조수, k04 초파리, 주판봇은 `specs/jupanbot/00_character_core.md`의 그림)를 함께 넣고, 한국어 지시 한 줄을 앞에 붙입니다: *"첨부한 캐릭터와 똑같은 얼굴·색·비율로, 아래 영어 프롬프트대로 그려 줘."*
2. **각 캐릭터의 첫 시트(D1·A1·F1·R1)를 먼저** 만들고, 마음에 드는 결과가 나오면 그 결과도 이후 시트의 참고 그림으로 함께 첨부합니다. 시트끼리 얼굴이 달라지는 것을 줄입니다.
3. 비율은 프롬프트에 적힌 대로(대부분 16:9, 의상 시트만 3:2). 가능하면 가장 큰 해상도로 받습니다.
4. 이번에 보여 주신 예시 시트(교복 소녀, 닌자, 픽셀 인물 모음)는 **배치 참고용으로만** 썼습니다. 다른 사람의 그림이고 그중 하나는 스톡 이미지라 Genspark에 첨부하지 마세요. 프롬프트에도 특정 게임·작품 이름은 넣지 않았습니다.

## 받은 뒤 확인할 것
- 배경이 한 가지 회색으로 평평한지(제가 회색을 지워 투명하게 만듭니다), 칸마다 발 높이가 같은지, 글자·숫자·효과선이 없는지
- 박사의 흰 브릿지, 조수의 남색 브릿지가 모든 칸에서 같은 쪽에 있는지 (두 캐릭터는 좌우 뒤집기 금지라서 박사는 오른쪽, 조수는 왼쪽을 보도록 따로 그립니다)
- 어긋난 칸이 1~2개면 그대로 주셔도 됩니다. 그 칸만 빼거나 이웃 칸으로 대신합니다.
- **파일 이름:** `시트번호_캐릭터.png` (예: `D5_doc.png`, `A6_asst.png`). 이 이름대로 잘라 추가 팩 키(`doc_fight_d5_f01` …)로 넣습니다.

## 시트 목록 한눈에

| 번호 | 캐릭터 | 내용 | 프레임 | 페이지에서 쓰는 곳 |
|---|---|---|---|---|
| D1 | 박사 | 기본 A · 서기·걷기 | 8 | 행동 축 '서기', 대전 대기 |
| D2 | 박사 | 기본 B · 점프·돌진 | 8 | 행동 축 '점프'·'돌진' |
| D3 | 박사 | 기본 C · 잽·가드·피격 | 8 | 잽·가드 버튼, 데미지 장면 |
| D4 | 박사 | 기본 D · 승리·KO | 8 | 라운드 결과 |
| D5 | 박사 | 필살기 ① 특이값 분해 참 | 8 | 필살기 '특이값 분해 참' (4장 SVD) |
| D6 | 박사 | 필살기 ② 브로드캐스트 웨이브 | 8 | 필살기 '브로드캐스트 웨이브' (3장 브로드캐스트) |
| D7 | 박사 | 필살기 ③ 역전파 카운터 | 8 | 콤보 마지막 기술 '역전파 카운터' |
| D8 | 박사 | 의상 3종 (복장 축) | 6 | 복장 축 '연구복·전투복·사이버' |
| A1 | 조수 하루 | 기본 A · 서기·걷기 | 8 | 행동 축 '서기', 대전 대기 |
| A2 | 조수 하루 | 기본 B · 점프·돌진 | 8 | 행동 축 '점프'·'돌진' |
| A3 | 조수 하루 | 기본 C · 잽·가드·피격 | 8 | 잽·가드 버튼, 데미지 장면 |
| A4 | 조수 하루 | 기본 D · 승리·KO | 8 | 라운드 결과 |
| A5 | 조수 하루 | 필살기 ① 원-핫 연타 | 8 | 필살기 '원-핫 연타' (특별편 특성공학) |
| A6 | 조수 하루 | 필살기 ② 경사하강 킥 | 8 | 필살기 '경사하강 킥' (4장 경사하강) |
| A7 | 조수 하루 | 의상 3종 (복장 축) | 6 | 복장 축 '연구복·전투복·사이버' |
| F1 | 초파리 연구원 (심판) | 심판 A · 대기·시작 신호 | 8 | 라운드 시작 연출 |
| F2 | 초파리 연구원 (심판) | 심판 B · 판정 | 8 | 라운드 판정 (박사 승 / 조수 승) |
| F3 | 초파리 연구원 (심판) | 심판 C · 무승부·의심 | 8 | 무승부·반칙 확인 |
| R1 | 주판봇 (점수판) | 점수판 A · 대기·주판 계산 | 8 | 점수판 대기·점수 갱신 |
| R2 | 주판봇 (점수판) | 점수판 B · 환호·실망 | 8 | 콤보 성공·실패 반응 |

총 20장 (박사 8 · 조수 7 · 초파리 3 · 주판봇 2). 급하면 **D5·D6·A5·A6(필살기 4장)과 D1·A1**부터 주셔도 필살기 동작을 먼저 붙일 수 있습니다.

---

## 박사

고정 외형: *chibi scientist (big head, about 2.5 heads tall), thin teal rectangular glasses, spiky black hair with one white streak, small ponytail at the back, white lab coat over black vest and tie, dark trousers, brown shoes*

### D1 · 기본 A · 서기·걷기
- 비율 16:9 · 4 열 × 2 행 · 쓰는 곳: 행동 축 '서기', 대전 대기

```
Pixel art sprite sheet of one original character: chibi scientist (big head, about 2.5 heads tall), thin teal rectangular glasses, spiky black hair with one white streak, small ponytail at the back, white lab coat over black vest and tie, dark trousers, brown shoes, facing right in side view (3/4 toward the viewer). Grid 4 columns x 2 rows, aspect ratio 16:9. Row 1: idle stance, 4 frames: fighting-game ready stance, fists up, gentle breathing bob, coat hem sways slightly. Row 2: walk forward, 4 frames: walk cycle toward the right, arms swinging. Same face, same proportions, same colors in every frame; only the pose changes. Keep the white hair streak on the same side in every frame. Never mirror the character. 16-bit RPG pixel art sprite sheet, crisp pixels, no anti-aliasing blur, bold dark outline (#1d1a22), 2-3 step cel shading with a tiny highlight, full body, same character scale and same ground line in every frame, every frame inside its own equal grid cell with empty margin, nothing crossing cell borders, flat solid plain medium gray background (#9e9e9e) with no gradient, no floor, no shadow, no scenery, no text, no letters, no numbers, no labels, no logo, no watermark, no extra visual effects beyond what is described, no motion lines, no speed lines.
```

### D2 · 기본 B · 점프·돌진
- 비율 16:9 · 4 열 × 2 행 · 쓰는 곳: 행동 축 '점프'·'돌진'

```
Pixel art sprite sheet of one original character: chibi scientist (big head, about 2.5 heads tall), thin teal rectangular glasses, spiky black hair with one white streak, small ponytail at the back, white lab coat over black vest and tie, dark trousers, brown shoes, facing right in side view (3/4 toward the viewer). Grid 4 columns x 2 rows, aspect ratio 16:9. Row 1: jump, 4 frames: crouch, rise with knees tucked, peak, land. Row 2: dash, 4 frames: lean forward low, rush forward, coat tails flying back, stop. Same face, same proportions, same colors in every frame; only the pose changes. Keep the white hair streak on the same side in every frame. Never mirror the character. 16-bit RPG pixel art sprite sheet, crisp pixels, no anti-aliasing blur, bold dark outline (#1d1a22), 2-3 step cel shading with a tiny highlight, full body, same character scale and same ground line in every frame, every frame inside its own equal grid cell with empty margin, nothing crossing cell borders, flat solid plain medium gray background (#9e9e9e) with no gradient, no floor, no shadow, no scenery, no text, no letters, no numbers, no labels, no logo, no watermark, no extra visual effects beyond what is described, no motion lines, no speed lines.
```

### D3 · 기본 C · 잽·가드·피격
- 비율 16:9 · 4 열 × 2 행 · 쓰는 곳: 잽·가드 버튼, 데미지 장면

```
Pixel art sprite sheet of one original character: chibi scientist (big head, about 2.5 heads tall), thin teal rectangular glasses, spiky black hair with one white streak, small ponytail at the back, white lab coat over black vest and tie, dark trousers, brown shoes, facing right in side view (3/4 toward the viewer). Grid 4 columns x 2 rows, aspect ratio 16:9. Row 1: jab, 4 frames: quick straight punch forward and back. Row 2: guard 2 frames + hit 2 frames, 4 frames: frames 1-2 arms crossed blocking; frames 3-4 knocked back, eyes shut, glasses tilted. Same face, same proportions, same colors in every frame; only the pose changes. Keep the white hair streak on the same side in every frame. Never mirror the character. 16-bit RPG pixel art sprite sheet, crisp pixels, no anti-aliasing blur, bold dark outline (#1d1a22), 2-3 step cel shading with a tiny highlight, full body, same character scale and same ground line in every frame, every frame inside its own equal grid cell with empty margin, nothing crossing cell borders, flat solid plain medium gray background (#9e9e9e) with no gradient, no floor, no shadow, no scenery, no text, no letters, no numbers, no labels, no logo, no watermark, no extra visual effects beyond what is described, no motion lines, no speed lines.
```

### D4 · 기본 D · 승리·KO
- 비율 16:9 · 4 열 × 2 행 · 쓰는 곳: 라운드 결과

```
Pixel art sprite sheet of one original character: chibi scientist (big head, about 2.5 heads tall), thin teal rectangular glasses, spiky black hair with one white streak, small ponytail at the back, white lab coat over black vest and tie, dark trousers, brown shoes, facing right in side view (3/4 toward the viewer). Grid 4 columns x 2 rows, aspect ratio 16:9. Row 1: victory, 4 frames: fist pump, then arms crossed proudly, small purple flame flickering on one hand. Row 2: knocked out, 4 frames: stagger, kneel, sit down dizzy, lie down. Same face, same proportions, same colors in every frame; only the pose changes. Keep the white hair streak on the same side in every frame. Never mirror the character. 16-bit RPG pixel art sprite sheet, crisp pixels, no anti-aliasing blur, bold dark outline (#1d1a22), 2-3 step cel shading with a tiny highlight, full body, same character scale and same ground line in every frame, every frame inside its own equal grid cell with empty margin, nothing crossing cell borders, flat solid plain medium gray background (#9e9e9e) with no gradient, no floor, no shadow, no scenery, no text, no letters, no numbers, no labels, no logo, no watermark, no extra visual effects beyond what is described, no motion lines, no speed lines.
```

### D5 · 필살기 ① 특이값 분해 참
- 비율 16:9 · 4 열 × 2 행 · 쓰는 곳: 필살기 '특이값 분해 참' (4장 SVD)

```
Pixel art sprite sheet of one original character: chibi scientist (big head, about 2.5 heads tall), thin teal rectangular glasses, spiky black hair with one white streak, small ponytail at the back, white lab coat over black vest and tie, dark trousers, brown shoes, facing right in side view (3/4 toward the viewer). Grid 4 columns x 2 rows, aspect ratio 16:9. special: singular value chop, 8 frames, read left to right then top to bottom: gather purple flame in the right hand, raise the hand high, step in, karate chop straight down with the open hand, follow-through, hold the pose, recover; the purple flame grows on the hand only. Same face, same proportions, same colors in every frame; only the pose changes. Keep the white hair streak on the same side in every frame. Never mirror the character. 16-bit RPG pixel art sprite sheet, crisp pixels, no anti-aliasing blur, bold dark outline (#1d1a22), 2-3 step cel shading with a tiny highlight, full body, same character scale and same ground line in every frame, every frame inside its own equal grid cell with empty margin, nothing crossing cell borders, flat solid plain medium gray background (#9e9e9e) with no gradient, no floor, no shadow, no scenery, no text, no letters, no numbers, no labels, no logo, no watermark, no extra visual effects beyond what is described, no motion lines, no speed lines.
```

### D6 · 필살기 ② 브로드캐스트 웨이브
- 비율 16:9 · 4 열 × 2 행 · 쓰는 곳: 필살기 '브로드캐스트 웨이브' (3장 브로드캐스트)

```
Pixel art sprite sheet of one original character: chibi scientist (big head, about 2.5 heads tall), thin teal rectangular glasses, spiky black hair with one white streak, small ponytail at the back, white lab coat over black vest and tie, dark trousers, brown shoes, facing right in side view (3/4 toward the viewer). Grid 4 columns x 2 rows, aspect ratio 16:9. special: broadcast wave, 8 frames, read left to right then top to bottom: plant feet wide, pull both hands back to the hip, thrust both open palms forward, hold the push while leaning in, slowly return; purple flame glows on both palms only. Same face, same proportions, same colors in every frame; only the pose changes. Keep the white hair streak on the same side in every frame. Never mirror the character. 16-bit RPG pixel art sprite sheet, crisp pixels, no anti-aliasing blur, bold dark outline (#1d1a22), 2-3 step cel shading with a tiny highlight, full body, same character scale and same ground line in every frame, every frame inside its own equal grid cell with empty margin, nothing crossing cell borders, flat solid plain medium gray background (#9e9e9e) with no gradient, no floor, no shadow, no scenery, no text, no letters, no numbers, no labels, no logo, no watermark, no extra visual effects beyond what is described, no motion lines, no speed lines.
```

### D7 · 필살기 ③ 역전파 카운터
- 비율 16:9 · 4 열 × 2 행 · 쓰는 곳: 콤보 마지막 기술 '역전파 카운터'

```
Pixel art sprite sheet of one original character: chibi scientist (big head, about 2.5 heads tall), thin teal rectangular glasses, spiky black hair with one white streak, small ponytail at the back, white lab coat over black vest and tie, dark trousers, brown shoes, facing right in side view (3/4 toward the viewer). Grid 4 columns x 2 rows, aspect ratio 16:9. special: backpropagation counter, 8 frames, read left to right then top to bottom: take a hit pose, slide backward, spin around once, reverse the momentum, deliver a rising palm strike upward, land in a ready stance. Same face, same proportions, same colors in every frame; only the pose changes. Keep the white hair streak on the same side in every frame. Never mirror the character. 16-bit RPG pixel art sprite sheet, crisp pixels, no anti-aliasing blur, bold dark outline (#1d1a22), 2-3 step cel shading with a tiny highlight, full body, same character scale and same ground line in every frame, every frame inside its own equal grid cell with empty margin, nothing crossing cell borders, flat solid plain medium gray background (#9e9e9e) with no gradient, no floor, no shadow, no scenery, no text, no letters, no numbers, no labels, no logo, no watermark, no extra visual effects beyond what is described, no motion lines, no speed lines.
```

### D8 · 의상 3종 (복장 축)
- 비율 3:2 · 3 열 × 2 행 · 쓰는 곳: 복장 축 '연구복·전투복·사이버'

```
Pixel art sprite sheet of one original character: chibi scientist (big head, about 2.5 heads tall), thin teal rectangular glasses, spiky black hair with one white streak, small ponytail at the back, white lab coat over black vest and tie, dark trousers, brown shoes, facing right in side view (3/4 toward the viewer). Grid 3 columns x 2 rows, aspect ratio 3:2. costumes, 6 frames, read left to right then top to bottom: columns = three outfits on the SAME character in the same idle stance: column 1 default lab outfit; column 2 'battle outfit' = lab coat sleeves rolled up, purple headband, purple fingerless gloves, purple sash belt, black training shoes; column 3 'cyber outfit' = lab coat with thin glowing cyan circuit lines, cyan lens glow on the glasses, silver shoulder plates, cyan-soled boots. Row 1 idle stance, row 2 the same three outfits in the jump peak pose. Same face, same proportions, same colors in every frame; only the pose changes. Keep the white hair streak on the same side in every frame. Never mirror the character. 16-bit RPG pixel art sprite sheet, crisp pixels, no anti-aliasing blur, bold dark outline (#1d1a22), 2-3 step cel shading with a tiny highlight, full body, same character scale and same ground line in every frame, every frame inside its own equal grid cell with empty margin, nothing crossing cell borders, flat solid plain medium gray background (#9e9e9e) with no gradient, no floor, no shadow, no scenery, no text, no letters, no numbers, no labels, no logo, no watermark, no extra visual effects beyond what is described, no motion lines, no speed lines.
```

---

## 조수 하루

고정 외형: *chibi girl researcher (big head, about 2.5 heads tall, slightly shorter than the doctor), long pink hair with two round buns and a navy streak, blue eyes, white lab coat over lavender hoodie, blue jeans, white sneakers*

### A1 · 기본 A · 서기·걷기
- 비율 16:9 · 4 열 × 2 행 · 쓰는 곳: 행동 축 '서기', 대전 대기

```
Pixel art sprite sheet of one original character: chibi girl researcher (big head, about 2.5 heads tall, slightly shorter than the doctor), long pink hair with two round buns and a navy streak, blue eyes, white lab coat over lavender hoodie, blue jeans, white sneakers, facing left in side view (3/4 toward the viewer). Grid 4 columns x 2 rows, aspect ratio 16:9. Row 1: idle stance, 4 frames: fighting-game ready stance, fists up, light bounce on toes, hair buns bob. Row 2: walk forward, 4 frames: walk cycle toward the left, arms swinging. Same face, same proportions, same colors in every frame; only the pose changes. Keep the navy hair streak on the same side in every frame. Never mirror the character. 16-bit RPG pixel art sprite sheet, crisp pixels, no anti-aliasing blur, bold dark outline (#1d1a22), 2-3 step cel shading with a tiny highlight, full body, same character scale and same ground line in every frame, every frame inside its own equal grid cell with empty margin, nothing crossing cell borders, flat solid plain medium gray background (#9e9e9e) with no gradient, no floor, no shadow, no scenery, no text, no letters, no numbers, no labels, no logo, no watermark, no extra visual effects beyond what is described, no motion lines, no speed lines.
```

### A2 · 기본 B · 점프·돌진
- 비율 16:9 · 4 열 × 2 행 · 쓰는 곳: 행동 축 '점프'·'돌진'

```
Pixel art sprite sheet of one original character: chibi girl researcher (big head, about 2.5 heads tall, slightly shorter than the doctor), long pink hair with two round buns and a navy streak, blue eyes, white lab coat over lavender hoodie, blue jeans, white sneakers, facing left in side view (3/4 toward the viewer). Grid 4 columns x 2 rows, aspect ratio 16:9. Row 1: jump, 4 frames: crouch, rise with knees tucked, peak, land. Row 2: dash, 4 frames: lean forward low, rush forward, hair and coat flying back, stop. Same face, same proportions, same colors in every frame; only the pose changes. Keep the navy hair streak on the same side in every frame. Never mirror the character. 16-bit RPG pixel art sprite sheet, crisp pixels, no anti-aliasing blur, bold dark outline (#1d1a22), 2-3 step cel shading with a tiny highlight, full body, same character scale and same ground line in every frame, every frame inside its own equal grid cell with empty margin, nothing crossing cell borders, flat solid plain medium gray background (#9e9e9e) with no gradient, no floor, no shadow, no scenery, no text, no letters, no numbers, no labels, no logo, no watermark, no extra visual effects beyond what is described, no motion lines, no speed lines.
```

### A3 · 기본 C · 잽·가드·피격
- 비율 16:9 · 4 열 × 2 행 · 쓰는 곳: 잽·가드 버튼, 데미지 장면

```
Pixel art sprite sheet of one original character: chibi girl researcher (big head, about 2.5 heads tall, slightly shorter than the doctor), long pink hair with two round buns and a navy streak, blue eyes, white lab coat over lavender hoodie, blue jeans, white sneakers, facing left in side view (3/4 toward the viewer). Grid 4 columns x 2 rows, aspect ratio 16:9. Row 1: jab, 4 frames: quick straight punch forward and back. Row 2: guard 2 frames + hit 2 frames, 4 frames: frames 1-2 arms crossed blocking; frames 3-4 knocked back, eyes shut. Same face, same proportions, same colors in every frame; only the pose changes. Keep the navy hair streak on the same side in every frame. Never mirror the character. 16-bit RPG pixel art sprite sheet, crisp pixels, no anti-aliasing blur, bold dark outline (#1d1a22), 2-3 step cel shading with a tiny highlight, full body, same character scale and same ground line in every frame, every frame inside its own equal grid cell with empty margin, nothing crossing cell borders, flat solid plain medium gray background (#9e9e9e) with no gradient, no floor, no shadow, no scenery, no text, no letters, no numbers, no labels, no logo, no watermark, no extra visual effects beyond what is described, no motion lines, no speed lines.
```

### A4 · 기본 D · 승리·KO
- 비율 16:9 · 4 열 × 2 행 · 쓰는 곳: 라운드 결과

```
Pixel art sprite sheet of one original character: chibi girl researcher (big head, about 2.5 heads tall, slightly shorter than the doctor), long pink hair with two round buns and a navy streak, blue eyes, white lab coat over lavender hoodie, blue jeans, white sneakers, facing left in side view (3/4 toward the viewer). Grid 4 columns x 2 rows, aspect ratio 16:9. Row 1: victory, 4 frames: jump with a V sign, then hold up a clipboard proudly with a smile. Row 2: knocked out, 4 frames: stagger, kneel, sit down dizzy, lie down. Same face, same proportions, same colors in every frame; only the pose changes. Keep the navy hair streak on the same side in every frame. Never mirror the character. 16-bit RPG pixel art sprite sheet, crisp pixels, no anti-aliasing blur, bold dark outline (#1d1a22), 2-3 step cel shading with a tiny highlight, full body, same character scale and same ground line in every frame, every frame inside its own equal grid cell with empty margin, nothing crossing cell borders, flat solid plain medium gray background (#9e9e9e) with no gradient, no floor, no shadow, no scenery, no text, no letters, no numbers, no labels, no logo, no watermark, no extra visual effects beyond what is described, no motion lines, no speed lines.
```

### A5 · 필살기 ① 원-핫 연타
- 비율 16:9 · 4 열 × 2 행 · 쓰는 곳: 필살기 '원-핫 연타' (특별편 특성공학)

```
Pixel art sprite sheet of one original character: chibi girl researcher (big head, about 2.5 heads tall, slightly shorter than the doctor), long pink hair with two round buns and a navy streak, blue eyes, white lab coat over lavender hoodie, blue jeans, white sneakers, facing left in side view (3/4 toward the viewer). Grid 4 columns x 2 rows, aspect ratio 16:9. special: one-hot barrage, 8 frames, read left to right then top to bottom: step in, rapid alternating straight punches (left, right, left, right), the final punch fully extended, hold, recover; one fist at a time is forward. Same face, same proportions, same colors in every frame; only the pose changes. Keep the navy hair streak on the same side in every frame. Never mirror the character. 16-bit RPG pixel art sprite sheet, crisp pixels, no anti-aliasing blur, bold dark outline (#1d1a22), 2-3 step cel shading with a tiny highlight, full body, same character scale and same ground line in every frame, every frame inside its own equal grid cell with empty margin, nothing crossing cell borders, flat solid plain medium gray background (#9e9e9e) with no gradient, no floor, no shadow, no scenery, no text, no letters, no numbers, no labels, no logo, no watermark, no extra visual effects beyond what is described, no motion lines, no speed lines.
```

### A6 · 필살기 ② 경사하강 킥
- 비율 16:9 · 4 열 × 2 행 · 쓰는 곳: 필살기 '경사하강 킥' (4장 경사하강)

```
Pixel art sprite sheet of one original character: chibi girl researcher (big head, about 2.5 heads tall, slightly shorter than the doctor), long pink hair with two round buns and a navy streak, blue eyes, white lab coat over lavender hoodie, blue jeans, white sneakers, facing left in side view (3/4 toward the viewer). Grid 4 columns x 2 rows, aspect ratio 16:9. special: gradient descent kick, 8 frames, read left to right then top to bottom: run up, jump high, tuck, extend one leg into a diagonal flying kick going downward, keep descending along a slope, land on one knee, stand up. Same face, same proportions, same colors in every frame; only the pose changes. Keep the navy hair streak on the same side in every frame. Never mirror the character. 16-bit RPG pixel art sprite sheet, crisp pixels, no anti-aliasing blur, bold dark outline (#1d1a22), 2-3 step cel shading with a tiny highlight, full body, same character scale and same ground line in every frame, every frame inside its own equal grid cell with empty margin, nothing crossing cell borders, flat solid plain medium gray background (#9e9e9e) with no gradient, no floor, no shadow, no scenery, no text, no letters, no numbers, no labels, no logo, no watermark, no extra visual effects beyond what is described, no motion lines, no speed lines.
```

### A7 · 의상 3종 (복장 축)
- 비율 3:2 · 3 열 × 2 행 · 쓰는 곳: 복장 축 '연구복·전투복·사이버'

```
Pixel art sprite sheet of one original character: chibi girl researcher (big head, about 2.5 heads tall, slightly shorter than the doctor), long pink hair with two round buns and a navy streak, blue eyes, white lab coat over lavender hoodie, blue jeans, white sneakers, facing left in side view (3/4 toward the viewer). Grid 3 columns x 2 rows, aspect ratio 3:2. costumes, 6 frames, read left to right then top to bottom: columns = three outfits on the SAME character in the same idle stance: column 1 default lab outfit; column 2 'battle outfit' = lab coat sleeves rolled up, pink headband, pink fingerless gloves, pink sash belt, sport sneakers; column 3 'cyber outfit' = lab coat with thin glowing cyan circuit lines, cyan visor-style hair clips, silver knee pads, cyan-soled boots. Row 1 idle stance, row 2 the same three outfits in the jump peak pose. Same face, same proportions, same colors in every frame; only the pose changes. Keep the navy hair streak on the same side in every frame. Never mirror the character. 16-bit RPG pixel art sprite sheet, crisp pixels, no anti-aliasing blur, bold dark outline (#1d1a22), 2-3 step cel shading with a tiny highlight, full body, same character scale and same ground line in every frame, every frame inside its own equal grid cell with empty margin, nothing crossing cell borders, flat solid plain medium gray background (#9e9e9e) with no gradient, no floor, no shadow, no scenery, no text, no letters, no numbers, no labels, no logo, no watermark, no extra visual effects beyond what is described, no motion lines, no speed lines.
```

---

## 초파리 연구원 (심판)

고정 외형: *anthropomorphic fruit fly researcher, small (about 40% of the doctor's height), black body, big red compound eyes, blue helmet with a gold stripe and pink and blue cables at the back, white lab coat over a black vest, black gloves, transparent wings*

### F1 · 심판 A · 대기·시작 신호
- 비율 16:9 · 4 열 × 2 행 · 쓰는 곳: 라운드 시작 연출

```
Pixel art sprite sheet of one original character: anthropomorphic fruit fly researcher, small (about 40% of the doctor's height), black body, big red compound eyes, blue helmet with a gold stripe and pink and blue cables at the back, white lab coat over a black vest, black gloves, transparent wings, facing the viewer, front view. Grid 4 columns x 2 rows, aspect ratio 16:9. Row 1: idle, 4 frames: standing referee pose, wings fluttering slightly, holding a small blank white flag. Row 2: round start, 4 frames: raise one arm high, then swing it down sharply to signal the start. Same face, same proportions, same colors in every frame; only the pose changes. Six limbs total (two arms, four legs) stay visible and consistent. 16-bit RPG pixel art sprite sheet, crisp pixels, no anti-aliasing blur, bold dark outline (#1d1a22), 2-3 step cel shading with a tiny highlight, full body, same character scale and same ground line in every frame, every frame inside its own equal grid cell with empty margin, nothing crossing cell borders, flat solid plain medium gray background (#9e9e9e) with no gradient, no floor, no shadow, no scenery, no text, no letters, no numbers, no labels, no logo, no watermark, no extra visual effects beyond what is described, no motion lines, no speed lines.
```

### F2 · 심판 B · 판정
- 비율 16:9 · 4 열 × 2 행 · 쓰는 곳: 라운드 판정 (박사 승 / 조수 승)

```
Pixel art sprite sheet of one original character: anthropomorphic fruit fly researcher, small (about 40% of the doctor's height), black body, big red compound eyes, blue helmet with a gold stripe and pink and blue cables at the back, white lab coat over a black vest, black gloves, transparent wings, facing the viewer, front view. Grid 4 columns x 2 rows, aspect ratio 16:9. Row 1: point to the left fighter, 4 frames: turn and point firmly to the viewer's left with the arm extended, flag up. Row 2: point to the right fighter, 4 frames: turn and point firmly to the viewer's right with the arm extended, flag up. Same face, same proportions, same colors in every frame; only the pose changes. Six limbs total (two arms, four legs) stay visible and consistent. 16-bit RPG pixel art sprite sheet, crisp pixels, no anti-aliasing blur, bold dark outline (#1d1a22), 2-3 step cel shading with a tiny highlight, full body, same character scale and same ground line in every frame, every frame inside its own equal grid cell with empty margin, nothing crossing cell borders, flat solid plain medium gray background (#9e9e9e) with no gradient, no floor, no shadow, no scenery, no text, no letters, no numbers, no labels, no logo, no watermark, no extra visual effects beyond what is described, no motion lines, no speed lines.
```

### F3 · 심판 C · 무승부·의심
- 비율 16:9 · 4 열 × 2 행 · 쓰는 곳: 무승부·반칙 확인

```
Pixel art sprite sheet of one original character: anthropomorphic fruit fly researcher, small (about 40% of the doctor's height), black body, big red compound eyes, blue helmet with a gold stripe and pink and blue cables at the back, white lab coat over a black vest, black gloves, transparent wings, facing the viewer, front view. Grid 4 columns x 2 rows, aspect ratio 16:9. Row 1: draw, 4 frames: cross both arms in an X, then shake head. Row 2: suspicious check, 4 frames: lean forward, hand on chin, squint, then nod. Same face, same proportions, same colors in every frame; only the pose changes. Six limbs total (two arms, four legs) stay visible and consistent. 16-bit RPG pixel art sprite sheet, crisp pixels, no anti-aliasing blur, bold dark outline (#1d1a22), 2-3 step cel shading with a tiny highlight, full body, same character scale and same ground line in every frame, every frame inside its own equal grid cell with empty margin, nothing crossing cell borders, flat solid plain medium gray background (#9e9e9e) with no gradient, no floor, no shadow, no scenery, no text, no letters, no numbers, no labels, no logo, no watermark, no extra visual effects beyond what is described, no motion lines, no speed lines.
```

---

## 주판봇 (점수판)

고정 외형: *boxy beige retro CRT-monitor robot (about 70% of the doctor's height), dark green screen face with mint pixel eyes and mouth, short antenna topped with a red-brown abacus bead, gray segmented arms, two small tank treads, holding a wooden abacus*

### R1 · 점수판 A · 대기·주판 계산
- 비율 16:9 · 4 열 × 2 행 · 쓰는 곳: 점수판 대기·점수 갱신

```
Pixel art sprite sheet of one original character: boxy beige retro CRT-monitor robot (about 70% of the doctor's height), dark green screen face with mint pixel eyes and mouth, short antenna topped with a red-brown abacus bead, gray segmented arms, two small tank treads, holding a wooden abacus, facing the viewer, 3/4 front view. Grid 4 columns x 2 rows, aspect ratio 16:9. Row 1: idle, 4 frames: rolling slightly back and forth on the treads, antenna bead bobbing. Row 2: counting, 4 frames: flicking abacus beads quickly with both hands, screen eyes looking down at the abacus. Same face, same proportions, same colors in every frame; only the pose changes. No round white head, no yellow eyes, no ball antenna, no chest lights, no floating, no gold coins. 16-bit RPG pixel art sprite sheet, crisp pixels, no anti-aliasing blur, bold dark outline (#1d1a22), 2-3 step cel shading with a tiny highlight, full body, same character scale and same ground line in every frame, every frame inside its own equal grid cell with empty margin, nothing crossing cell borders, flat solid plain medium gray background (#9e9e9e) with no gradient, no floor, no shadow, no scenery, no text, no letters, no numbers, no labels, no logo, no watermark, no extra visual effects beyond what is described, no motion lines, no speed lines.
```

### R2 · 점수판 B · 환호·실망
- 비율 16:9 · 4 열 × 2 행 · 쓰는 곳: 콤보 성공·실패 반응

```
Pixel art sprite sheet of one original character: boxy beige retro CRT-monitor robot (about 70% of the doctor's height), dark green screen face with mint pixel eyes and mouth, short antenna topped with a red-brown abacus bead, gray segmented arms, two small tank treads, holding a wooden abacus, facing the viewer, 3/4 front view. Grid 4 columns x 2 rows, aspect ratio 16:9. Row 1: cheer, 4 frames: raise the abacus high, screen shows happy pixel eyes, small hop on treads. Row 2: disappointed, 4 frames: lower the abacus, screen shows flat pixel eyes, body tilts forward. Same face, same proportions, same colors in every frame; only the pose changes. No round white head, no yellow eyes, no ball antenna, no chest lights, no floating, no gold coins. 16-bit RPG pixel art sprite sheet, crisp pixels, no anti-aliasing blur, bold dark outline (#1d1a22), 2-3 step cel shading with a tiny highlight, full body, same character scale and same ground line in every frame, every frame inside its own equal grid cell with empty margin, nothing crossing cell borders, flat solid plain medium gray background (#9e9e9e) with no gradient, no floor, no shadow, no scenery, no text, no letters, no numbers, no labels, no logo, no watermark, no extra visual effects beyond what is described, no motion lines, no speed lines.
```
