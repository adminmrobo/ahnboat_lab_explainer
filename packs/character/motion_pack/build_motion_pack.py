#!/usr/bin/env python3
"""
연구실 캐릭터 동작 팩 (fight 1.0) — 페이지에 넣을 조각 만들기 (CHAR_lab4 C8)

원본: https://github.com/adminmrobo/fruitfly-lab-expressions  (motions.html, specs/motions/motions.json)
들어 있는 것: webp/{key}_{192|128}.webp  가로 스트립 한 장 = 시트 한 장 (프레임 i 는 x = i*fw)
            motion_map.json              시트별 who·제목·보는 쪽·구간(seg)·프레임 크기·발 기준선(base)

사용
  python3 build_motion_pack.py --pick D1,D5,A1,A5 --size 128            → var MOTION={...}; + 재생 함수
  python3 build_motion_pack.py --pick D1,D5 --size 128 --no-player      → 데이터만
  python3 build_motion_pack.py --list                                    → 시트 목록
  python3 build_motion_pack.py --build ../../../../fruitfly-lab-expressions --who sia,moa,x1,x2,x3
      → 원본 저장소의 프레임(images/motions/{who}/)으로 그 캐릭터의 스트립을 다시 만들고 motion_map.json에 넣는다

출력하는 재생 함수 (본 스킬 12-6)
  drawMotion(ctx, sheet, seg, t, cx, cy, h, opt) → true(그림) / false(아직 로드 전 또는 없음 → 표정 그림으로 대신)
    sheet  'D5' 같은 시트 번호     seg  구간 이름('idle', 'svd_chop') 또는 null(전체)
    t      초(누적)                 cx,cy 발 기준점(가운데 아래)   h  그릴 높이(px, 프레임 칸 높이)
    opt.face   'left'|'right' 원하는 방향. 그림의 facing과 다르면 좌우 반전
               (박사·조수는 반전 금지 → opt.forceMirror 없으면 반전하지 않고 그대로 그림)
    opt.fps    기본 10        opt.once  true면 마지막 프레임에서 멈춤      opt.frame  특정 프레임 고정(0부터)
  motionLen(sheet, seg, fps) → 그 구간 재생 시간(초)

필요: Python 3.8+
"""
import argparse, base64, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))

PLAYER = r"""
var MOTION_IMG={};
function motionImg(k){var m=MOTION[k];if(!m)return null;if(!MOTION_IMG[k]){var im=new Image();im.src=m.src;MOTION_IMG[k]=im}return MOTION_IMG[k]}
function motionRange(m,seg){var r=seg&&m.seg[seg]?m.seg[seg]:[1,m.n];return [r[0]-1,r[1]-1]}
function motionLen(k,seg,fps){var m=MOTION[k];if(!m)return 0;var r=motionRange(m,seg);return (r[1]-r[0]+1)/(fps||10)}
function drawMotion(x,k,seg,t,cx,cy,h,opt){opt=opt||{};var m=MOTION[k],im=motionImg(k);if(!m||!im||!im.complete||!im.naturalWidth)return false;
  var r=motionRange(m,seg),n=r[1]-r[0]+1,i=Math.floor(t*(opt.fps||10));i=opt.frame!=null?opt.frame:(opt.once?Math.min(i,n-1):i%n);
  var f=r[0]+Math.max(0,i),s=h/m.fh,w=m.fw*s,flip=opt.face&&m.facing!=='front'&&opt.face!==m.facing&&(m.mirror||opt.forceMirror);
  x.save();x.translate(cx,cy);if(flip)x.scale(-1,1);x.drawImage(im,f*m.fw,0,m.fw,m.fh,-w/2,-m.base*s,w,m.fh*s);x.restore();return true}
"""


# 원본 저장소 who → 이 팩의 who (박사·조수·초파리·주판봇은 fight 1.1에서 만든 스트립을 그대로 둔다)
BUILD_WHO = {"sia": "sia", "moa": "moa", "x1": "x1", "x2": "x2", "x3": "x3"}
MIRROR_DEFAULT = {"sia": False, "moa": False, "x1": True, "x2": True, "x3": True}
REF_SHEET = {"sia": "S1", "moa": "M1", "x1": "X1A", "x2": "X2A", "x3": "X3A"}  # 똑바로 선 기준 프레임이 있는 시트


def build(repo, whos):
    """원본 프레임(182×280 등, 발 기준선 ground_y)을 가로 스트립으로 묶는다.
    캐릭터마다 하나의 배율: 기준 시트 1번 프레임(똑바로 선 자세)의 키 = fh × fill.
    원본 프레임은 이미 캐릭터마다 같은 배율로 잘려 있으므로(fruitfly-lab-expressions specs/motions/README) 시트끼리 크기가 맞는다."""
    from PIL import Image
    M = json.load(open(os.path.join(HERE, "motion_map.json"), encoding="utf-8"))
    src = json.load(open(os.path.join(repo, "specs", "motions", "motions.json"), encoding="utf-8"))
    fill = M.get("fill", 0.72)
    os.makedirs(os.path.join(HERE, "webp"), exist_ok=True)
    added = 0
    for who in whos:
        sheets = [s for s in src["sheets"] if s["who"] == who]
        if not sheets:
            sys.exit("원본에 없는 캐릭터: %s" % who)
        ref = next(s for s in sheets if s["id"] == REF_SHEET[who])
        bb = Image.open(os.path.join(repo, ref["frames"][0])).getbbox()
        stand = bb[3] - bb[1]
        for s in sheets:
            FW, FH = s["frame_size"]; GY = s["ground_y"]
            kind = "crowd" if s["id"].startswith("X") else "fight"
            key = "%s_%s_%s" % (who, kind, s["id"].lower())
            strips = {}
            for fh in (192, 128):
                k = fill * fh / stand
                base = fh - 4
                fw = max(1, round(FW * k))
                strip = Image.new("RGBA", (fw * len(s["frames"]), fh), (0, 0, 0, 0))
                for i, f in enumerate(s["frames"]):
                    fr = Image.open(os.path.join(repo, f)).convert("RGBA")
                    fr = fr.resize((fw, max(1, round(FH * k))), Image.LANCZOS)
                    strip.alpha_composite(fr, (i * fw, round(base - GY * k)) if base - GY * k >= 0 else (i * fw, 0))
                path = os.path.join("webp", "%s_%d.webp" % (key, fh))
                strip.save(os.path.join(HERE, path), "WEBP", quality=88, method=6)
                strips[str(fh)] = {"file": path, "fw": fw, "fh": fh, "base": base, "bytes": os.path.getsize(os.path.join(HERE, path))}
            ent = {"who": who, "key": key, "title": s["title"], "facing": s["facing"], "n": len(s["frames"]),
                   "seg": s["seg"], "strips": strips}
            if s.get("regen"):
                ent["regen"] = s["regen"]
            if s.get("hidden"):
                ent["hidden"] = True
            M["sheets"][s["id"]] = ent
            added += 1
        M["mirror"][who] = MIRROR_DEFAULT.get(who, False)
    json.dump(M, open(os.path.join(HERE, "motion_map.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    sys.stderr.write("스트립 %d장 (%s)\n" % (added, ",".join(whos)))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pick", default="")
    ap.add_argument("--size", type=int, default=128, choices=[128, 192])
    ap.add_argument("--no-player", action="store_true")
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--build", help="원본 저장소 폴더 (fruitfly-lab-expressions)")
    ap.add_argument("--who", default="sia,moa,x1,x2,x3")
    a = ap.parse_args()
    if a.build:
        build(a.build, [w.strip() for w in a.who.split(",") if w.strip()])
        return
    M = json.load(open(os.path.join(HERE, "motion_map.json"), encoding="utf-8"))
    if a.list:
        for sid, s in M["sheets"].items():
            print("%-3s %-5s %-6s %s  %s%s" % (sid, s["who"], s["facing"], s["title"], ",".join(s["seg"]),
                                             ("  ※" + s["regen"]) if s.get("regen") else ""))
        return
    pick = [p.strip().upper() for p in a.pick.split(",") if p.strip()] or list(M["sheets"])
    out, total = {}, 0
    for sid in pick:
        if sid not in M["sheets"]:
            sys.exit("없는 시트: %s (--list로 확인)" % sid)
        s = M["sheets"][sid]; st = s["strips"][str(a.size)]
        raw = open(os.path.join(HERE, st["file"]), "rb").read(); total += len(raw)
        out[sid] = {"who": s["who"], "n": s["n"], "seg": s["seg"], "facing": s["facing"], "fw": st["fw"], "fh": st["fh"],
                    "base": st["base"], "mirror": M["mirror"][s["who"]], "src": "data:image/webp;base64," + base64.b64encode(raw).decode()}
    sys.stdout.write("var MOTION=%s;\n" % json.dumps(out, ensure_ascii=False, separators=(",", ":")))
    if not a.no_player:
        sys.stdout.write(PLAYER)
    sys.stderr.write("motion %d sheets, %d KB (size %d)\n" % (len(out), total // 1024, a.size))


if __name__ == "__main__":
    main()
