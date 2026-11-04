#!/usr/bin/env python3
"""
초파리 연구실 캐릭터 팩 빌드 스크립트 (ai-lab-explainer 스킬 v1.6 부록 E)

원본: https://github.com/adminmrobo/fruitfly-lab-expressions
  images/{doctor,haru,fruitfly,jupanbot}/E01_joy.png ... E24_shock.png (불투명 단색·그라데이션 배경)

하는 일
  1) 배경 제거: 테두리에서 시작해 이웃 픽셀과 색이 비슷한 영역만 투명하게 만든다
     (그라데이션 배경도 따라가고, 캐릭터의 굵은 외곽선에서 멈춘다)
  2) 크기 줄이기: 원본 구도를 그대로 둔 채 정사각형으로 (기본 96px, 192px)
  3) WebP(알파) 저장 + base64 묶음(JS) + 매니페스트(JSON)

사용
  python3 build_character_pack.py --repo ./fruitfly-lab-expressions --out ./character_pack
  python3 build_character_pack.py --clone --out ./character_pack          # git clone부터
  python3 build_character_pack.py --pack ./character_pack --pick fly_point,robo_coin,doc_think --size 96
      → 그 페이지에 쓰는 키만 골라 `var SPRITE={...}` 조각을 출력 (HTML에 붙여 넣기)
  python3 build_character_pack.py --ingest ./받은그림 --plates bg_07=F,sc_07_hero=E --out received_07
      → 외부에서 받은 그림을 판에 맞게 처리하고 `Object.assign(SPRITE,{...})` 조각을 만든다 (SKILL 18-15)

필요: Python 3.8+, Pillow(WebP 지원), numpy
"""
import argparse, base64, collections, hashlib, json, os, subprocess, sys

REPO_URL = "https://github.com/adminmrobo/fruitfly-lab-expressions"

# 스킬의 캐릭터 이름(who) ↔ 저장소 폴더
# robo = 주판봇(AbaBot). 2026-11 Money-Robo((주)M-Robo 회사 캐릭터)를 대신함. 키 이름 robo는 호환을 위해 그대로 둠
WHO = {"doc": "doctor", "asst": "haru", "fly": "fruitfly", "robo": "jupanbot"}

EXPRESSIONS = [
    ("E01", "joy", "기쁨"), ("E02", "sadness", "슬픔"), ("E03", "anger", "분노"),
    ("E04", "surprise", "놀람"), ("E05", "fear", "두려움"), ("E06", "disgust", "혐오"),
    ("E07", "explaining", "설명"), ("E08", "guiding", "안내"), ("E09", "thinking", "생각"),
    ("E10", "confirming", "확인"), ("E11", "apologizing", "사과"), ("E12", "cheering", "응원"),
    ("E13", "neutral", "기본"), ("E14", "sheepish", "머쓱함"), ("E15", "flustered", "당황"),
    ("E16", "proud", "뿌듯함"), ("E17", "sleepy", "졸림"), ("E18", "sulking", "삐짐"),
    ("E19", "sparkle_eyes", "반짝눈"), ("E20", "sweat_drop", "식은땀"),
    ("E21", "waterfall_tears", "폭포 눈물"), ("E22", "puffed_angry", "뿔남"),
    ("E23", "blank_dot_eyes", "멍"), ("E24", "shock", "충격"),
]

# 스킬 표정 키(5-8, 18-5) → 저장소 표정 ID. 그림을 눈으로 보고 정함 (2026-10-28).
# exact = 표정·몸짓·소품이 맞음 / near = 감정은 맞고 소품·몸짓이 다름 / missing = 맞는 그림 없음(대신 쓰는 그림)
ALIASES = {
    "doc_front":   ("E08", "exact", "눈 감고 웃으며 손을 펴서 가리킴"),
    "doc_board":   ("E07", "near",  "검지를 세워 설명 (지휘봉 없음)"),
    "doc_judge":   ("E10", "near",  "윙크 + 엄지 + 체크 표시"),
    "doc_verdict": ("E18", "near",  "팔짱 + 단호한 눈"),
    "doc_scale":   ("E09", "deprecated", "v1.9: doc_think로 바꿈 (저울 그림 없음). 옛 페이지용 별칭"),
    "doc_magic":   ("E16", "exact", "양손 보랏빛 불꽃"),
    "doc_think":   ("E09", "exact", "턱에 손 + 물음표"),
    "asst_smile":  ("E13", "exact", "기본 미소"),
    "asst_firm":   ("E12", "exact", "주먹 쥔 결의"),
    "asst_ledger": ("E07", "deprecated", "v1.9: asst_report로 바꿈 (장부 그림 없음). 옛 페이지용 별칭"),
    "asst_report": ("E07", "exact", "검지를 세워 발표 (숫자 발표)"),
    "asst_spark":  ("E01", "exact", "입 벌려 웃음 + 반짝이"),
    "asst_shock":  ("E24", "exact", "질린 얼굴 + 땀"),
    "asst_sigh":   ("E02", "near",  "눈을 내리깐 시무룩 (한숨 방울 없음)"),
    "asst_board":  ("E16", "deprecated", "v1.9: asst_proud로 바꿈 (점수판 그림 없음). 옛 페이지용 별칭"),
    "asst_proud":  ("E16", "exact", "뿌듯한 미소 (결산·목차)"),
    "fly_clip":    ("E10", "exact", "클립보드 기록"),
    "fly_point":   ("E08", "exact", "손가락으로 가리킴"),
    "fly_arms":    ("E16", "exact", "팔짱 + 반짝이 (자신만만)"),
    "fly_coffee":  ("E13", "exact", "커피잔"),
    "fly_cry":     ("E21", "exact", "폭포 눈물"),
    "fly_type":    ("E09", "exact", "키보드 타이핑"),
    "fly_magnify": ("E07", "exact", "돋보기"),
    # 주판봇: 명세 기준(specs/jupanbot). 그림이 임시(placeholder)인 동안은 모두 같은 그림이 나옴
    "robo_smile":  ("E13", "exact", "네모 픽셀 눈 + 작은 미소, 주판을 듦"),
    "robo_coin":   ("E16", "exact", "반쯤 감은 눈 + 반짝이는 주판알 (키 이름은 옛 금화 시절 그대로)"),
    "robo_chart":  ("E07", "exact", "상승 막대 차트 판을 가리킴"),
    "robo_happy":  ("E12", "exact", "주판을 머리 위로 + 상승 화살표"),
    "robo_sigh":   ("E20", "near",  "점 눈 + 땀방울 (본전·손절)"),
    "robo_meh":    ("E18", "exact", "일자 눈 + 팔짱"),
    "robo_cry":    ("E21", "exact", "폭포 눈물 + 흩어진 주판알"),
    "robo_wow":    ("E04", "exact", "동그란 눈 + o 입"),
    "robo_blush":  ("E14", "exact", "분홍 픽셀 볼"),
    "robo_calc":   ("E09", "exact", "주판알을 튕기며 계산"),
}

# 그림이 바라보는 쪽 (눈으로 판정, 대결 화면 좌우 뒤집기에 씀). 적지 않은 것은 front.
FACING = {
    "doc_e07": "left", "doc_e08": "left",
    "asst_e07": "left", "asst_e08": "left", "asst_e10": "left",
    "fly_e07": "left", "fly_e08": "left", "fly_e09": "left", "fly_e10": "left",
    "fly_e13": "left", "fly_e18": "left",
    # 주판봇은 새 그림이 오면 눈으로 보고 다시 적는다 (임시 그림은 모두 정면)
}


def key(who, eid):
    return "%s_e%s" % (who, eid[1:])


# ---------------------------------------------------------------- 배경 제거
def remove_background(img, tol=22, chroma_margin=8, enclosed_min=0, halo_tol=34):
    """배경색(행마다 위 테두리→아래 모서리 사이를 보간한 회색)과 가깝고 채도가 낮은 픽셀 중,
    위쪽 테두리·양옆 위 55%에 이어진 덩어리만 투명하게 만든다.
    - 흰 가운이 아래 테두리에 닿아도 출발점이 아니므로 지워지지 않는다
    - 가운의 연보라 그림자는 채도 조건으로 지켜진다
    - enclosed_min>0 이면 캐릭터 안에 갇힌 배경색 덩어리(그 크기 이상)도 지운다 (초파리 케이블 사이)"""
    import numpy as np
    from PIL import Image
    from scipy import ndimage
    rgb = np.asarray(img.convert("RGB")).astype(np.int16)
    h, w, _ = rgb.shape
    top = np.median(rgb[0], axis=0)
    corners = np.concatenate([rgb[-3:, :6].reshape(-1, 3), rgb[-3:, -6:].reshape(-1, 3)])
    bottom = np.median(corners, axis=0)
    if np.abs(bottom - top).max() <= tol:
        ref = np.repeat(top[None, :], h, axis=0)                 # 단색 배경
    else:
        # 그라데이션 배경 (E24 충격 등): 행마다 양 끝 4px의 중앙값을 기준색으로,
        # 캐릭터가 가장자리에 닿은 행은 위아래 31행 중앙값으로 눌러 준다
        edge = np.concatenate([rgb[:, :4], rgb[:, -4:]], axis=1)
        rowref = np.median(edge, axis=1)
        ref = ndimage.median_filter(rowref, size=(31, 1), mode="nearest")
    diff = np.abs(rgb - ref[:, None, :]).max(axis=2)
    chroma = rgb.max(axis=2) - rgb.min(axis=2)
    ref_chroma = (ref.max(axis=1) - ref.min(axis=1))[:, None]
    cand = (diff <= tol) & (chroma <= ref_chroma + chroma_margin)
    lab, n = ndimage.label(cand)
    seeds = np.zeros_like(cand)
    seeds[0, :] = True
    seeds[: int(h * 0.55), 0] = True
    seeds[: int(h * 0.55), -1] = True
    keep = set(np.unique(lab[seeds & cand])) - {0}
    if enclosed_min:
        sizes = ndimage.sum(np.ones_like(lab), lab, index=range(1, n + 1))
        keep |= {i + 1 for i, s in enumerate(sizes) if s >= enclosed_min}
    bg = np.isin(lab, list(keep))
    # 배경에 닿은 1px 띠 중 배경색이 섞인 것도 지운다 (어두운 화면에서 밝은 테두리가 뜨지 않게)
    ring = ndimage.binary_dilation(bg) & ~bg
    ring &= (np.abs(rgb - ref[:, None, :]).max(axis=2) <= halo_tol) & (chroma <= ref_chroma + chroma_margin + 6)
    bg |= ring
    alpha = np.where(bg, 0, 255).astype(np.uint8)
    out = img.convert("RGBA")
    out.putalpha(Image.fromarray(alpha))
    return out, float(bg.mean())


BG_OPTIONS = {"fly": {"enclosed_min": 30}}  # 초파리만 갇힌 배경 덩어리 제거 (다른 캐릭터는 흰 가운 보호)

# 눈으로 확인한 배경 제거 한계 (2026-10-28 빌드)
BG_NOTES = {
    "doc_e24": "위쪽에 회보라 띠와 세로 효과선이 남음 (번개가 양옆을 덮어 배경색 추정 불가). 충격 연출로 그대로 둠",
    "fly_e24": "위쪽에 옅은 세로 효과선이 일부 남음",
}


def square(img, size):
    from PIL import Image
    w, h = img.size
    side = max(w, h)
    canvas = Image.new("RGBA", (side, side), (0, 0, 0, 0))
    canvas.paste(img, ((side - w) // 2, side - h))  # 아래 맞춤 (발·그림자 기준선 유지)
    return canvas.resize((size, size), Image.LANCZOS)


def b64(path):
    with open(path, "rb") as f:
        return "data:image/webp;base64," + base64.b64encode(f.read()).decode()


# ---------------------------------------------------------------- 빌드
def build(repo, out, sizes, quality):
    from PIL import Image
    commit = ""
    try:
        commit = subprocess.check_output(["git", "-C", repo, "rev-parse", "HEAD"], text=True).strip()
    except Exception:
        pass
    os.makedirs(out, exist_ok=True)
    items, js = [], {s: {} for s in sizes}
    for who, folder in WHO.items():
        for eid, slug, ko in EXPRESSIONS:
            src = os.path.join(repo, "images", folder, "%s_%s.png" % (eid, slug))
            if not os.path.exists(src):
                print("없음:", src, file=sys.stderr)
                continue
            img = Image.open(src)
            cut, bg_ratio = remove_background(img, **BG_OPTIONS.get(who, {}))
            k = key(who, eid)
            rec = {"key": k, "who": who, "id": eid, "slug": slug, "ko": ko,
                   "source": "images/%s/%s_%s.png" % (folder, eid, slug),
                   "source_size": list(img.size), "bg_removed": round(bg_ratio, 3),
                   "facing": FACING.get(k, "front"), "files": {}}
            if k in BG_NOTES:
                rec["bg_note"] = BG_NOTES[k]
            for s in sizes:
                d = os.path.join(out, "webp", str(s), who)
                os.makedirs(d, exist_ok=True)
                p = os.path.join(d, "%s.webp" % k)
                square(cut, s).save(p, "WEBP", quality=quality, method=6)
                rec["files"][str(s)] = {"path": os.path.relpath(p, out), "bytes": os.path.getsize(p)}
                js[s][k] = b64(p)
            # 확인용 투명 PNG (원본 크기)
            d = os.path.join(out, "png", who)
            os.makedirs(d, exist_ok=True)
            cut.save(os.path.join(d, "%s.png" % k), optimize=True)
            items.append(rec)
            print("ok", k, "배경 %.0f%%" % (bg_ratio * 100))
    aliases = {a: {"key": key(a.split("_")[0], e), "match": m, "note": n} for a, (e, m, n) in ALIASES.items()}
    manifest = {
        "package": "fruitfly-lab-character-pack", "version": "1.0",
        "source": {"repo": REPO_URL, "commit": commit},
        "who": {w: {"repo_folder": f} for w, f in WHO.items()},
        "names": {"doc": "박사", "asst": "조수(하루)", "fly": "초파리 연구원", "robo": "주판봇"},
        "key_format": "{who}_e{NN}  예: fly_e08 = 초파리 E08 안내",
        "sizes": sizes, "expressions": [{"id": e, "slug": s, "ko": k} for e, s, k in EXPRESSIONS],
        "aliases": aliases, "images": items,
    }
    with open(os.path.join(out, "character_pack.json"), "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=1)
    with open(os.path.join(out, "expression_map.json"), "w", encoding="utf-8") as f:
        json.dump(aliases, f, ensure_ascii=False, indent=1)
    for s in sizes:
        alias_js = {a: v["key"] for a, v in aliases.items()}
        face_js = {r["key"]: r["facing"] for r in items if r["facing"] != "front"}
        with open(os.path.join(out, "sprites_%d.js" % s), "w", encoding="utf-8") as f:
            f.write("/* 초파리 연구실 캐릭터 팩 %dpx — %s @ %s */\n" % (s, REPO_URL, commit[:7]))
            f.write("var LAB_PACK={size:%d,commit:%s,alias:%s,facing:%s,img:%s};\n" % (
                s, json.dumps(commit[:7]), json.dumps(alias_js), json.dumps(face_js),
                json.dumps(js[s], separators=(",", ":"))))
    print("완료:", out)


# ---------------------------------------------------------------- 필요한 키만 뽑기
def pick(pack, keys, size):
    with open(os.path.join(pack, "character_pack.json"), encoding="utf-8") as f:
        m = json.load(f)
    alias = {a: v["key"] for a, v in m["aliases"].items()}
    files = {r["key"]: r for r in m["images"]}
    out, total, face = {}, 0, {}
    # 쓰는 캐릭터마다 기본 표정(E13)을 함께 넣는다 — 없는 키를 대신할 그림 (5-8)
    whos = []
    for k in keys:
        w = alias.get(k, k).split("_")[0]
        if w in WHO and w not in whos:
            whos.append(w)
    keys = list(keys) + ["%s_e13" % w for w in whos if "%s_e13" % w not in [alias.get(k, k) for k in keys]]
    for k in keys:
        real = alias.get(k, k)
        if real not in files:
            print("/* 없는 키: %s */" % k)
            continue
        p = os.path.join(pack, files[real]["files"][str(size)]["path"])
        out[real] = b64(p)
        total += os.path.getsize(p)
        if files[real]["facing"] != "front":
            face[real] = files[real]["facing"]
    used_alias = {k: alias[k] for k in keys if k in alias}
    print("/* 캐릭터 팩 %s @ %s, %dpx, %d장, %.1f KB */" % (m["source"]["repo"], m["source"]["commit"][:7], size, len(out), total / 1024))
    print("var SPRITE=%s;" % json.dumps(out, separators=(",", ":")))
    print("var SPRITE_ALIAS=%s;" % json.dumps(used_alias, ensure_ascii=False))
    print("var SPRITE_FACING=%s;" % json.dumps(face))


# ---------------------------------------------------------------- 받은 그림 반영 (SKILL 18-15)
# 판별 처리: 배경 제거 여부, 빌드 후 크기 (SKILL 18-2)
PLATES = {
    "A": ("cut", "square"), "B": ("cut", "square"), "C": ("cut", "square"), "D": ("cut", "square"),
    "H": ("cut", 32),
    "E": ("keep", 760), "F": ("keep", 1280), "G": ("keep", 640),
    "I": ("keep", 400), "J": ("keep", 1280), "K": ("keep", 1200),
}


def ingest(folder, plates, out, quality, square_sizes=(96, 192)):
    from PIL import Image
    os.makedirs(out, exist_ok=True)
    files = {os.path.splitext(f)[0]: os.path.join(folder, f) for f in sorted(os.listdir(folder))
             if f.lower().endswith((".png", ".jpg", ".jpeg", ".webp"))}
    result, report = {}, []
    for k, path in files.items():
        plate = plates.get(k)
        if not plate:
            # 표정 키(doc_/asst_/fly_/robo_)는 판을 몰라도 A~D로 본다
            plate = "A" if k.split("_")[0] in WHO else None
        if plate not in PLATES:
            report.append("건너뜀 %s: 판을 모름 (--plates %s=F 처럼 알려 주세요)" % (k, k))
            continue
        mode, size = PLATES[plate]
        img = Image.open(path)
        w0, h0 = img.size
        note = ""
        if mode == "cut":
            img, ratio = remove_background(img, **BG_OPTIONS.get(k.split("_")[0], {}))
            note = "배경 %.0f%% 제거" % (ratio * 100)
            if ratio < 0.15 or ratio > 0.92:
                note += " (확인 필요: 배경 비율이 이상함)"
        else:
            img = img.convert("RGB")
        outs = []
        if size == "square":
            for s in square_sizes:
                p = os.path.join(out, "%s_%d.webp" % (k, s))
                square(img, s).save(p, "WEBP", quality=quality, method=6)
                outs.append(p)
        else:
            im = img
            if im.width > size:
                im = im.resize((size, round(im.height * size / im.width)), Image.LANCZOS)
            p = os.path.join(out, "%s.webp" % k)
            im.save(p, "WEBP", quality=quality, method=6)
            outs.append(p)
        main_file = outs[0]  # 정사각 표정은 96px를 기본으로 넣는다
        result[k] = b64(main_file)
        report.append("%s  판 %s  원본 %dx%d → %s  %.1f KB  %s" % (
            k, plate, w0, h0, ", ".join(os.path.basename(o) for o in outs),
            os.path.getsize(main_file) / 1024, note))
    total = sum(len(v) for v in result.values()) / 1024
    snippet = "/* 받은 그림 %d장, base64 %.0f KB */\nObject.assign(SPRITE,%s);\n" % (
        len(result), total, json.dumps(result, separators=(",", ":")))
    with open(os.path.join(out, "sprite_add.js"), "w", encoding="utf-8") as f:
        f.write(snippet)
    with open(os.path.join(out, "ingest_report.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(report) + "\n")
    print("\n".join(report))
    print("→ %s (base64 합계 %.0f KB)" % (os.path.join(out, "sprite_add.js"), total))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--repo", help="받아 둔 저장소 폴더")
    ap.add_argument("--clone", action="store_true", help="저장소를 git clone 해서 쓴다")
    ap.add_argument("--out", default="character_pack")
    ap.add_argument("--sizes", default="96,192")
    ap.add_argument("--quality", type=int, default=82)
    ap.add_argument("--pack", help="--pick 모드에서 쓸 팩 폴더")
    ap.add_argument("--pick", help="쉼표로 구분한 키 (예: fly_point,robo_e16)")
    ap.add_argument("--size", type=int, default=96)
    ap.add_argument("--ingest", help="받은 그림 폴더 (파일 이름 = 키). SKILL 18-15")
    ap.add_argument("--plates", default="", help="키=판 목록. 예: bg_07=F,sc_07_hero=E")
    a = ap.parse_args()
    if a.ingest:
        plates = dict(p.split("=") for p in a.plates.split(",") if "=" in p)
        ingest(a.ingest, plates, a.out if a.out != "character_pack" else "received", a.quality)
        return
    if a.pick:
        pick(a.pack or a.out, [k.strip() for k in a.pick.split(",") if k.strip()], a.size)
        return
    repo = a.repo
    if a.clone:
        repo = repo or "fruitfly-lab-expressions"
        if not os.path.exists(repo):
            subprocess.check_call(["git", "clone", "--depth", "1", REPO_URL, repo])
    if not repo:
        ap.error("--repo 또는 --clone 이 필요합니다")
    build(repo, a.out, [int(s) for s in a.sizes.split(",")], a.quality)


if __name__ == "__main__":
    main()
