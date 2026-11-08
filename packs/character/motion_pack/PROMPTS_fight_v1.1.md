# 동작 팩 fight 1.1 — 추가 시트 8장 지침서

이전 20장(fight 1.0)과 **같은 방식**입니다. 다른 점은 아래 세 가지뿐입니다.

1. **방향을 맨 앞에 못 박았습니다.** 박사는 오른쪽, 조수는 왼쪽(둘이 마주 봄). 프롬프트 첫 문장 뒤에 `IMPORTANT: … faces RIGHT/LEFT` 가 들어 있습니다.
2. **참고 그림은 방향이 맞는 시트만** 첨부합니다. 각 시트의 "첨부" 칸을 보세요. 지금의 D2·D5·D6(왼쪽을 보는 시트)은 **첨부하지 마세요.** 생성기가 방향까지 따라 합니다.
3. 의상 동작(D9·D10·A8·A9)은 의상 시트(D8·A7)에서 해당 칸을 잘라 첨부하면 의상이 덜 흔들립니다.

## 넣는 법 (매번)
- 첨부: 표정 기본 그림(`doc_front` / `asst_smile`) + 설정샷 3면도(박사 k02, 조수 k03) + 표의 "첨부" 시트
- 한국어 한 줄을 앞에 붙임: *"첨부한 캐릭터와 똑같은 얼굴·색·비율로, 아래 영어 프롬프트대로 그려 줘. 방향이 가장 중요해."*
- 비율 16:9, 가장 큰 해상도
- 받은 뒤 확인: 모든 칸에서 박사는 오른쪽, 조수는 왼쪽을 보는지 · 배경이 단색 회색인지 · 글자·효과선이 없는지
- 파일 이름: `D2_doc.png`, `D9_doc.png`, `A10_asst.png` … (시트번호_캐릭터). 다시 그린 D2·D5·D6은 **같은 이름**으로 주시면 바꿔 끼웁니다.

## 시트 목록

| 번호 | 내용 | 첨부할 기존 시트 | 왜 |
|---|---|---|---|
| D2 | 박사 · 점프·돌진 (다시 그리기) | D1_doc.png, D3_doc.png (오른쪽을 보는 시트) | 왼쪽을 보고 그려져 임시 반전 중 |
| D5 | 박사 · 필살기 특이값 분해 참 (다시 그리기) | D1_doc.png, D7_doc.png | 왼쪽을 보고 그려져 임시 반전 중 |
| D6 | 박사 · 필살기 브로드캐스트 웨이브 (다시 그리기) | D1_doc.png, D7_doc.png | 왼쪽을 보고 그려져 임시 반전 중 |
| D9 | 박사 · 전투복 돌진·필살기 | D8_doc.png(의상 시트) 가운데 칸 + D1_doc.png | 새 시트 (복장 축 '전투복'의 돌진·필살기) |
| D10 | 박사 · 사이버 돌진·필살기 | D8_doc.png 오른쪽 칸 + D1_doc.png | 새 시트 (복장 축 '사이버'의 돌진·필살기) |
| A8 | 조수 · 전투복 돌진·필살기 | A7_asst.png(의상 시트) 가운데 칸 + A1_asst.png | 새 시트 (복장 축 '전투복'의 돌진·필살기) |
| A9 | 조수 · 사이버 돌진·필살기 | A7_asst.png 오른쪽 칸 + A1_asst.png | 새 시트 (복장 축 '사이버'의 돌진·필살기) |
| A10 | 조수 · 역전파 카운터 | A1_asst.png, A3_asst.png | 새 시트 (콤보 기술 '역전파 카운터') |

급하면 **D5·D6 → D2 → A10** 순서로 주세요(필살기 화면에 바로 보이는 순서). 의상 4장은 나중에 주셔도 됩니다.

---

### D2 · 박사 · 점프·돌진 (다시 그리기)
- 첨부: D1_doc.png, D3_doc.png (오른쪽을 보는 시트)

```
Pixel art sprite sheet of one original character: chibi scientist (big head, about 2.5 heads tall), thin teal rectangular glasses, spiky black hair with one white streak, small ponytail at the back, white lab coat over black vest and tie, dark trousers, brown shoes, side view (3/4 toward the viewer). IMPORTANT: the character faces RIGHT in every frame (looking toward the right edge of the image, the attacking hand and leg reach to the RIGHT). Do not mirror; keep the white hair streak on the same side as in the attached reference. Grid 4 columns x 2 rows, aspect ratio 16:9. Row 1: jump, 4 frames: crouch, rise with knees tucked, peak, land. Row 2: dash, 4 frames: lean forward low, rush toward the RIGHT, coat tails flying back to the left, stop. Same face, same proportions, same colors in every frame; only the pose changes. Keep the white hair streak on the same side in every frame. Never mirror the character. 16-bit RPG pixel art sprite sheet, crisp pixels, no anti-aliasing blur, bold dark outline (#1d1a22), 2-3 step cel shading with a tiny highlight, full body, same character scale and same ground line in every frame, every frame inside its own equal grid cell with empty margin, nothing crossing cell borders, flat solid plain medium gray background (#9e9e9e) with no gradient, no floor, no shadow, no scenery, no text, no letters, no numbers, no labels, no logo, no watermark, no extra visual effects beyond what is described, no motion lines, no speed lines.
```

---

### D5 · 박사 · 필살기 특이값 분해 참 (다시 그리기)
- 첨부: D1_doc.png, D7_doc.png

```
Pixel art sprite sheet of one original character: chibi scientist (big head, about 2.5 heads tall), thin teal rectangular glasses, spiky black hair with one white streak, small ponytail at the back, white lab coat over black vest and tie, dark trousers, brown shoes, side view (3/4 toward the viewer). IMPORTANT: the character faces RIGHT in every frame (looking toward the right edge of the image, the attacking hand and leg reach to the RIGHT). Do not mirror; keep the white hair streak on the same side as in the attached reference. Grid 4 columns x 2 rows, aspect ratio 16:9. special: singular value chop, 8 frames, read left to right then top to bottom: gather purple flame in the right hand, raise the hand high, step in toward the RIGHT, karate chop straight down with the open hand in front of the body on the RIGHT side, follow-through, hold the pose, recover; the purple flame grows on the hand only. Same face, same proportions, same colors in every frame; only the pose changes. Keep the white hair streak on the same side in every frame. Never mirror the character. 16-bit RPG pixel art sprite sheet, crisp pixels, no anti-aliasing blur, bold dark outline (#1d1a22), 2-3 step cel shading with a tiny highlight, full body, same character scale and same ground line in every frame, every frame inside its own equal grid cell with empty margin, nothing crossing cell borders, flat solid plain medium gray background (#9e9e9e) with no gradient, no floor, no shadow, no scenery, no text, no letters, no numbers, no labels, no logo, no watermark, no extra visual effects beyond what is described, no motion lines, no speed lines.
```

---

### D6 · 박사 · 필살기 브로드캐스트 웨이브 (다시 그리기)
- 첨부: D1_doc.png, D7_doc.png

```
Pixel art sprite sheet of one original character: chibi scientist (big head, about 2.5 heads tall), thin teal rectangular glasses, spiky black hair with one white streak, small ponytail at the back, white lab coat over black vest and tie, dark trousers, brown shoes, side view (3/4 toward the viewer). IMPORTANT: the character faces RIGHT in every frame (looking toward the right edge of the image, the attacking hand and leg reach to the RIGHT). Do not mirror; keep the white hair streak on the same side as in the attached reference. Grid 4 columns x 2 rows, aspect ratio 16:9. special: broadcast wave, 8 frames, read left to right then top to bottom: plant feet wide, pull both hands back to the hip on the LEFT, thrust both open palms forward to the RIGHT, hold the push while leaning to the RIGHT, slowly return; purple flame glows on both palms only. Same face, same proportions, same colors in every frame; only the pose changes. Keep the white hair streak on the same side in every frame. Never mirror the character. 16-bit RPG pixel art sprite sheet, crisp pixels, no anti-aliasing blur, bold dark outline (#1d1a22), 2-3 step cel shading with a tiny highlight, full body, same character scale and same ground line in every frame, every frame inside its own equal grid cell with empty margin, nothing crossing cell borders, flat solid plain medium gray background (#9e9e9e) with no gradient, no floor, no shadow, no scenery, no text, no letters, no numbers, no labels, no logo, no watermark, no extra visual effects beyond what is described, no motion lines, no speed lines.
```

---

### D9 · 박사 · 전투복 돌진·필살기
- 첨부: D8_doc.png(의상 시트) 가운데 칸 + D1_doc.png

```
Pixel art sprite sheet of one original character: chibi scientist (big head, about 2.5 heads tall), thin teal rectangular glasses, spiky black hair with one white streak, small ponytail at the back, white lab coat over black vest and tie, dark trousers, brown shoes, wearing the battle outfit: lab coat sleeves rolled up, purple headband, purple fingerless gloves, purple sash belt, black training shoes, side view (3/4 toward the viewer). IMPORTANT: the character faces RIGHT in every frame (looking toward the right edge of the image, the attacking hand and leg reach to the RIGHT). Do not mirror; keep the white hair streak on the same side as in the attached reference. Grid 4 columns x 2 rows, aspect ratio 16:9. Row 1: dash, 4 frames: lean forward low, rush toward the RIGHT, coat tails flying back, stop. Row 2: special chop, 4 key frames: raise the open hand with a purple flame, step in, chop straight down on the RIGHT side, hold. Same face, same proportions, same colors in every frame; only the pose changes. Keep the white hair streak on the same side in every frame. Never mirror the character. 16-bit RPG pixel art sprite sheet, crisp pixels, no anti-aliasing blur, bold dark outline (#1d1a22), 2-3 step cel shading with a tiny highlight, full body, same character scale and same ground line in every frame, every frame inside its own equal grid cell with empty margin, nothing crossing cell borders, flat solid plain medium gray background (#9e9e9e) with no gradient, no floor, no shadow, no scenery, no text, no letters, no numbers, no labels, no logo, no watermark, no extra visual effects beyond what is described, no motion lines, no speed lines.
```

---

### D10 · 박사 · 사이버 돌진·필살기
- 첨부: D8_doc.png 오른쪽 칸 + D1_doc.png

```
Pixel art sprite sheet of one original character: chibi scientist (big head, about 2.5 heads tall), thin teal rectangular glasses, spiky black hair with one white streak, small ponytail at the back, white lab coat over black vest and tie, dark trousers, brown shoes, wearing the cyber outfit: lab coat with thin glowing cyan circuit lines, cyan lens glow on the glasses, silver shoulder plates, cyan-soled boots, side view (3/4 toward the viewer). IMPORTANT: the character faces RIGHT in every frame (looking toward the right edge of the image, the attacking hand and leg reach to the RIGHT). Do not mirror; keep the white hair streak on the same side as in the attached reference. Grid 4 columns x 2 rows, aspect ratio 16:9. Row 1: dash, 4 frames: lean forward low, rush toward the RIGHT, coat tails flying back, stop. Row 2: special chop, 4 key frames: raise the open hand with a purple flame, step in, chop straight down on the RIGHT side, hold. Same face, same proportions, same colors in every frame; only the pose changes. Keep the white hair streak on the same side in every frame. Never mirror the character. 16-bit RPG pixel art sprite sheet, crisp pixels, no anti-aliasing blur, bold dark outline (#1d1a22), 2-3 step cel shading with a tiny highlight, full body, same character scale and same ground line in every frame, every frame inside its own equal grid cell with empty margin, nothing crossing cell borders, flat solid plain medium gray background (#9e9e9e) with no gradient, no floor, no shadow, no scenery, no text, no letters, no numbers, no labels, no logo, no watermark, no extra visual effects beyond what is described, no motion lines, no speed lines.
```

---

### A8 · 조수 · 전투복 돌진·필살기
- 첨부: A7_asst.png(의상 시트) 가운데 칸 + A1_asst.png

```
Pixel art sprite sheet of one original character: chibi girl researcher (big head, about 2.5 heads tall, slightly shorter than the doctor), long pink hair with two round buns and a navy streak, blue eyes, white lab coat over lavender hoodie, blue jeans, white sneakers, wearing the battle outfit: lab coat sleeves rolled up, pink headband, pink fingerless gloves, pink sash belt, sport sneakers, side view (3/4 toward the viewer). IMPORTANT: the character faces LEFT in every frame (attacks reach to the LEFT). Do not mirror. Grid 4 columns x 2 rows, aspect ratio 16:9. Row 1: dash, 4 frames: lean forward low, rush toward the LEFT, hair and coat flying back, stop. Row 2: one-hot barrage, 4 key frames: step in, left straight punch, right straight punch, final punch fully extended to the LEFT. Same face, same proportions, same colors in every frame; only the pose changes. Keep the navy hair streak on the same side in every frame. Never mirror the character. 16-bit RPG pixel art sprite sheet, crisp pixels, no anti-aliasing blur, bold dark outline (#1d1a22), 2-3 step cel shading with a tiny highlight, full body, same character scale and same ground line in every frame, every frame inside its own equal grid cell with empty margin, nothing crossing cell borders, flat solid plain medium gray background (#9e9e9e) with no gradient, no floor, no shadow, no scenery, no text, no letters, no numbers, no labels, no logo, no watermark, no extra visual effects beyond what is described, no motion lines, no speed lines.
```

---

### A9 · 조수 · 사이버 돌진·필살기
- 첨부: A7_asst.png 오른쪽 칸 + A1_asst.png

```
Pixel art sprite sheet of one original character: chibi girl researcher (big head, about 2.5 heads tall, slightly shorter than the doctor), long pink hair with two round buns and a navy streak, blue eyes, white lab coat over lavender hoodie, blue jeans, white sneakers, wearing the cyber outfit: lab coat with thin glowing cyan circuit lines, cyan visor-style hair clips, silver knee pads, cyan-soled boots, side view (3/4 toward the viewer). IMPORTANT: the character faces LEFT in every frame (attacks reach to the LEFT). Do not mirror. Grid 4 columns x 2 rows, aspect ratio 16:9. Row 1: dash, 4 frames: lean forward low, rush toward the LEFT, hair and coat flying back, stop. Row 2: one-hot barrage, 4 key frames: step in, left straight punch, right straight punch, final punch fully extended to the LEFT. Same face, same proportions, same colors in every frame; only the pose changes. Keep the navy hair streak on the same side in every frame. Never mirror the character. 16-bit RPG pixel art sprite sheet, crisp pixels, no anti-aliasing blur, bold dark outline (#1d1a22), 2-3 step cel shading with a tiny highlight, full body, same character scale and same ground line in every frame, every frame inside its own equal grid cell with empty margin, nothing crossing cell borders, flat solid plain medium gray background (#9e9e9e) with no gradient, no floor, no shadow, no scenery, no text, no letters, no numbers, no labels, no logo, no watermark, no extra visual effects beyond what is described, no motion lines, no speed lines.
```

---

### A10 · 조수 · 역전파 카운터
- 첨부: A1_asst.png, A3_asst.png

```
Pixel art sprite sheet of one original character: chibi girl researcher (big head, about 2.5 heads tall, slightly shorter than the doctor), long pink hair with two round buns and a navy streak, blue eyes, white lab coat over lavender hoodie, blue jeans, white sneakers, side view (3/4 toward the viewer). IMPORTANT: the character faces LEFT in every frame (attacks reach to the LEFT). Do not mirror. Grid 4 columns x 2 rows, aspect ratio 16:9. special: backpropagation counter, 8 frames, read left to right then top to bottom: take a hit pose leaning back, slide backward to the RIGHT, spin around once, reverse the momentum, deliver a rising palm strike upward toward the LEFT, land in a ready stance facing LEFT. Same face, same proportions, same colors in every frame; only the pose changes. Keep the navy hair streak on the same side in every frame. Never mirror the character. 16-bit RPG pixel art sprite sheet, crisp pixels, no anti-aliasing blur, bold dark outline (#1d1a22), 2-3 step cel shading with a tiny highlight, full body, same character scale and same ground line in every frame, every frame inside its own equal grid cell with empty margin, nothing crossing cell borders, flat solid plain medium gray background (#9e9e9e) with no gradient, no floor, no shadow, no scenery, no text, no letters, no numbers, no labels, no logo, no watermark, no extra visual effects beyond what is described, no motion lines, no speed lines.
```

---

## 받은 뒤 제가 하는 일
1. fruitfly-lab-expressions에 원본·프레임 추가, `motions.json`과 갤러리 갱신 (D2·D5·D6은 교체, 다시 그리기 표시 제거)
2. ahnboat_lab_explainer 동작 팩을 fight 1.1로 (`motion_map.json`, 스트립, CHAR_lab4 C8 표, CHANGELOG)
3. 특별편: 박사 임시 반전 제거, 전투복·사이버의 돌진·필살기를 의상 동작으로, 콤보에 조수 역전파 카운터 재생 → 검수 5회차 → 푸시
