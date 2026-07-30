#!/usr/bin/env python3
"""
쉴더스랩 명함 생성기 — 인쇄 납품용 벡터 원본
  · 규격 : 재단 90 × 50 mm + 사방 3 mm 도련(재단여유) → 실제 캔버스 96 × 56 mm
           SVG viewBox 를 mm 단위(1 user unit = 1 mm)로 잡아 치수 오차를 없앤다.
  · 서체 : 모든 글자를 **아웃라인 패스로 변환**해 임베드한다.
           인쇄소에 폰트를 함께 넘길 필요가 없고, 폰트 미설치로 인한 치환 사고가 없다.
  · 출력 : SVG(편집용 벡터) · PDF(인쇄 납품용 벡터, TrimBox/BleedBox 지정)
           PNG 300dpi(투명, 포토샵 편집용) · JPG 300dpi(미리보기·간이 납품)
  · 시안 : A 에디토리얼 / B 여백형 / C 역상(딥파인)  각 앞면·뒷면

사용
  python3 tools/build-card.py                                  # 예시 정보로 전체 생성
  python3 tools/build-card.py --name 홍길동 --title 대표 \
      --mobile 010-1234-5678 --email hong@shilderslab.com
  python3 tools/build-card.py --list                           # 생성 목록만 확인

필요
  fontTools (아웃라인 변환) · Manrope.ttf · NotoSansKR.ttf
  PDF 변환은 svglib + reportlab, 래스터는 sharp(node) — 없으면 해당 포맷만 건너뛴다.
"""
import argparse, json, os, re, subprocess, sys

SRC = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(SRC)
FONT_DIR = os.environ.get("SL_FONT_DIR", SRC)
MANROPE = os.path.join(FONT_DIR, "Manrope.ttf")
NOTOKR = os.path.join(FONT_DIR, "NotoSansKR.ttf")

# ─────────── 브랜드 컬러 (site.css / build-ci.py 와 동일) ───────────
PAPER = "#F6F4EF"
INK = "#15181B"
INK_2 = "#4A5157"
INK_3 = "#7C838A"
ACCENT = "#1A4B3A"
ACCENT_3 = "#2E6B54"
RULE = "#DDD8CE"

# 인쇄용 CMYK 근사값 — PDF 에 이 값으로 기록한다(RGB→CMYK 변환 오차를 인쇄소에 넘기지 않기 위함)
CMYK = {
    ACCENT:   (0.80, 0.42, 0.72, 0.44),
    ACCENT_3: (0.72, 0.30, 0.63, 0.24),
    INK:      (0.72, 0.64, 0.60, 0.71),
    INK_2:    (0.62, 0.50, 0.44, 0.28),
    INK_3:    (0.48, 0.36, 0.32, 0.06),
    PAPER:    (0.02, 0.02, 0.06, 0.00),
    RULE:     (0.08, 0.07, 0.14, 0.00),
}

# ─────────── 지면 규격 (mm) ───────────
TRIM_W, TRIM_H = 90.0, 50.0
BLEED = 3.0
W, H = TRIM_W + BLEED * 2, TRIM_H + BLEED * 2   # 96 × 56
SAFE = 5.0                                       # 재단선에서 안쪽 안전여백
X0, Y0 = BLEED, BLEED                            # 재단 시작
XS, YS = BLEED + SAFE, BLEED + SAFE              # 안전영역 시작
XE, YE = BLEED + TRIM_W - SAFE, BLEED + TRIM_H - SAFE

_cache = {}


def _font(path, wght):
    from fontTools.ttLib import TTFont
    from fontTools.varLib.instancer import instantiateVariableFont
    key = (path, wght)
    if key not in _cache:
        f = TTFont(path)
        if "fvar" in f:
            f = instantiateVariableFont(f, {"wght": wght}, inplace=True, updateFontNames=False)
        _cache[key] = f
    return _cache[key]


def _is_ko(ch):
    o = ord(ch)
    return 0xAC00 <= o <= 0xD7A3 or 0x1100 <= o <= 0x11FF or 0x3130 <= o <= 0x318F


def text_path(text, cap, x=0.0, y=0.0, tracking=0.0, weight=500, ko_ratio=0.94):
    """혼합 스크립트 텍스트를 단일 SVG 패스 d 로. 한글은 Noto, 라틴은 Manrope.
       두 서체를 cap height 기준으로 맞추고, 한글만 ko_ratio 로 미세 보정한다.
       반환: (d, 진행폭)"""
    from fontTools.pens.svgPathPen import SVGPathPen
    from fontTools.pens.transformPen import TransformPen
    from fontTools.misc.transform import Identity
    parts, cx = [], float(x)
    for ch in text:
        ko = _is_ko(ch)
        f = _font(NOTOKR if ko else MANROPE, weight if not ko else min(weight, 700))
        cmap, gs, hmtx = f.getBestCmap(), f.getGlyphSet(), f["hmtx"]
        upem = f["head"].unitsPerEm
        cap_u = getattr(f["OS/2"], "sCapHeight", None) or int(upem * 0.72)
        scale = (cap * (ko_ratio if ko else 1.0)) / cap_u
        g = cmap.get(ord(ch))
        if g is None:
            cx += cap * 0.45
            continue
        if ch != " ":
            sp = SVGPathPen(gs, ntos=lambda v: f"{v:.3f}")
            gs[g].draw(TransformPen(sp, Identity.translate(cx, y).scale(scale, -scale)))
            if sp.getCommands():
                parts.append(sp.getCommands())
        cx += hmtx[g][0] * scale + tracking * cap
    return " ".join(parts), round(cx - float(x), 3)


def text_w(text, cap, tracking=0.0, weight=500, ko_ratio=0.94):
    return text_path(text, cap, 0, 0, tracking, weight, ko_ratio)[1]


def sym_path():
    """CI 심볼 컴파운드 패스(64 그리드) — build-ci.py 와 동일 좌표계"""
    shield = ("M32 2.4 L57.4 11.9 V32.2 C57.4 46.4 46.6 57.9 32 61.6 "
              "C17.4 57.9 6.6 46.4 6.6 32.2 V11.9 Z")
    d, w = text_path("S", 27.5, 0, 0, 0, 800)
    # ink bbox 로 중앙 정렬
    from fontTools.pens.boundsPen import BoundsPen
    from fontTools.pens.transformPen import TransformPen
    from fontTools.misc.transform import Identity
    f = _font(MANROPE, 800)
    gs = f.getGlyphSet()
    cap_u = getattr(f["OS/2"], "sCapHeight", None) or int(f["head"].unitsPerEm * 0.72)
    sc = 27.5 / cap_u
    bp = BoundsPen(gs)
    gs[f.getBestCmap()[ord("S")]].draw(TransformPen(bp, Identity.scale(sc, -sc)))
    x1, y1, x2, y2 = bp.bounds
    s_d, _ = text_path("S", 27.5, 32 - (x1 + x2) / 2, 30.6 - (y1 + y2) / 2, 0, 800)
    return f"{shield} {s_d}"


SYMBOL = None  # lazy


def sym(x, y, size, fill):
    """심볼을 (x,y) 위치·size(mm) 높이로 배치"""
    global SYMBOL
    if SYMBOL is None:
        SYMBOL = sym_path()
    k = size / 64.0
    return (f'<g transform="translate({x:.3f} {y:.3f}) scale({k:.5f})">'
            f'<path d="{SYMBOL}" fill="{fill}" fill-rule="evenodd"/></g>')


def svg(body, bg=PAPER):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}mm" height="{H}mm" '
            f'viewBox="0 0 {W} {H}">\n'
            f'<rect width="{W}" height="{H}" fill="{bg}"/>\n{body}\n</svg>\n')


def guide_overlay():
    """검토용 가이드 — 도련/재단/안전 영역 표시(납품 파일에는 넣지 않는다)"""
    return (f'<rect x="0" y="0" width="{W}" height="{H}" fill="none" stroke="#C9302C" '
            f'stroke-width="0.2" stroke-dasharray="1 1"/>'
            f'<rect x="{X0}" y="{Y0}" width="{TRIM_W}" height="{TRIM_H}" fill="none" '
            f'stroke="#1A4B3A" stroke-width="0.25"/>'
            f'<rect x="{XS}" y="{YS}" width="{TRIM_W - SAFE * 2}" height="{TRIM_H - SAFE * 2}" '
            f'fill="none" stroke="#2E6B54" stroke-width="0.15" stroke-dasharray="0.8 0.8"/>'
            f'<text x="{X0}" y="{Y0 - 0.9}" font-family="monospace" font-size="1.4" fill="#C9302C">'
            f'bleed {BLEED}mm · trim {TRIM_W}×{TRIM_H}mm · safe {SAFE}mm</text>')


# ══════════════════════════════════════════════════════════════════════
# 시안
# ══════════════════════════════════════════════════════════════════════
def lockup(x, y, cap, sym_fill, ko_fill, en_fill, en_cap=None):
    """심볼 + SHIELDUS LAB + 쉴더스랩 조합 (좌측 정렬)"""
    en_cap = en_cap or cap
    s = sym(x, y, cap * 2.0, sym_fill)
    tx = x + cap * 2.0 + cap * 0.62
    en_d, en_w = text_path("SHIELDUS LAB", en_cap, tx, y + cap * 1.16, 0.03, 800)
    ko_d, _ = text_path("정보보호 컨설팅", en_cap * 0.52, tx + 0.1, y + cap * 1.92, 0.02, 500)
    return (s + f'<path d="{en_d}" fill="{en_fill}"/>'
            f'<path d="{ko_d}" fill="{ko_fill}"/>'), tx + en_w


def contact_block(p, x, y, gap, cap, label_fill, value_fill, align_right=False):
    """연락처 줄들 — 라벨 없이 값만, 모노 느낌의 라틴은 Manrope"""
    out, cy = [], y
    rows = [r for r in [
        ("M", p.get("mobile")), ("T", p.get("phone")), ("E", p.get("email")),
        ("W", p.get("web")), ("A", p.get("addr")),
    ] if r[1]]
    for tag, val in rows:
        td, tw = text_path(tag, cap * 0.78, 0, 0, 0.08, 600)
        vd, vw = text_path(val, cap, 0, 0, 0.01, 400)
        if align_right:
            vx = x - vw
            tx = vx - cap * 1.25
        else:
            tx, vx = x, x + cap * 1.5
        td, _ = text_path(tag, cap * 0.78, tx, cy, 0.08, 600)
        vd, _ = text_path(val, cap, vx, cy, 0.01, 400)
        out.append(f'<path d="{td}" fill="{label_fill}"/><path d="{vd}" fill="{value_fill}"/>')
        cy += gap
    return "".join(out), cy


def dsn_a(p):
    """시안 A — 에디토리얼: 상단 액센트 바, 좌측 정렬, 하단 헤어라인 + 연락처"""
    b = [f'<rect x="0" y="0" width="{W}" height="{BLEED + 1.6}" fill="{ACCENT}"/>']
    lk, _ = lockup(XS, YS + 1.2, 3.1, ACCENT, INK_3, INK)
    b.append(lk)
    name_d, name_w = text_path(p["name"], 5.0, XS, YS + 20.5, -0.01, 600)
    b.append(f'<path d="{name_d}" fill="{INK}"/>')
    if p.get("title"):
        t_d, _ = text_path(p["title"], 2.5, XS + name_w + 2.4, YS + 20.5, 0.03, 500)
        b.append(f'<path d="{t_d}" fill="{ACCENT}"/>')
    if p.get("dept"):
        d_d, _ = text_path(p["dept"], 2.3, XS, YS + 25.2, 0.02, 400)
        b.append(f'<path d="{d_d}" fill="{INK_3}"/>')
    b.append(f'<rect x="{XS}" y="{YE - 13.4}" width="{XE - XS}" height="0.18" fill="{RULE}"/>')
    cb, _ = contact_block(p, XS, YE - 9.4, 3.3, 2.35, ACCENT, INK_2)
    b.append(cb)
    return "".join(b), PAPER


def dsn_a_back(p):
    b = [sym(W / 2 - 9, H / 2 - 11.5, 18, PAPER)]
    d, w = text_path("SHIELDUS LAB", 2.6, 0, 0, 0.18, 700)
    d, _ = text_path("SHIELDUS LAB", 2.6, W / 2 - w / 2, H / 2 + 14.2, 0.18, 700)
    b.append(f'<path d="{d}" fill="{PAPER}"/>')
    return "".join(b), ACCENT


def dsn_b(p):
    """시안 B — 여백형: 심볼만 작게, 이름 중심, 연락처 한 덩어리 우측 하단"""
    b = [sym(XS, YS, 7.2, ACCENT)]
    name_d, name_w = text_path(p["name"], 5.6, XS, YS + 22.8, -0.012, 600)
    b.append(f'<path d="{name_d}" fill="{INK}"/>')
    if p.get("title"):
        t_d, _ = text_path(p["title"], 2.4, XS, YS + 27.6, 0.04, 500)
        b.append(f'<path d="{t_d}" fill="{ACCENT}"/>')
    cb, _ = contact_block(p, XE, YE - 9.4, 3.2, 2.25, INK_3, INK_2, align_right=True)
    b.append(cb)
    return "".join(b), PAPER


def dsn_b_back(p):
    lk, w = lockup(0, 0, 3.4, ACCENT, INK_3, INK)
    # 중앙 배치를 위해 다시 그린다
    total = w
    lk, _ = lockup((W - total) / 2, H / 2 - 5.2, 3.4, ACCENT, INK_3, INK)
    tag = "ISMS-P · 모의해킹 · 취약점 진단 · 클라우드 보안"
    td, tw = text_path(tag, 1.85, 0, 0, 0.02, 400)
    td, _ = text_path(tag, 1.85, (W - tw) / 2, H / 2 + 9.4, 0.02, 400)
    return lk + f'<path d="{td}" fill="{INK_3}"/>', PAPER


def dsn_c(p):
    """시안 C — 역상: 딥파인 전면, 페이퍼 텍스트"""
    lk, _ = lockup(XS, YS + 1.2, 3.1, PAPER, "#8FB3A2", PAPER)
    b = [lk]
    name_d, name_w = text_path(p["name"], 5.0, XS, YS + 20.5, -0.01, 600)
    b.append(f'<path d="{name_d}" fill="{PAPER}"/>')
    if p.get("title"):
        t_d, _ = text_path(p["title"], 2.5, XS + name_w + 2.4, YS + 20.5, 0.03, 500)
        b.append(f'<path d="{t_d}" fill="#9FBDAF"/>')
    b.append(f'<rect x="{XS}" y="{YE - 13.4}" width="{XE - XS}" height="0.18" fill="#3D6B58"/>')
    cb, _ = contact_block(p, XS, YE - 9.4, 3.3, 2.35, "#93B6A5", PAPER)
    b.append(cb)
    return "".join(b), ACCENT


def dsn_c_back(p):
    b = [sym(W / 2 - 8, H / 2 - 10.6, 16, ACCENT)]
    d, w = text_path("shilderslab.com", 2.2, 0, 0, 0.12, 600)
    d, _ = text_path("shilderslab.com", 2.2, W / 2 - w / 2, H / 2 + 13.4, 0.12, 600)
    b.append(f'<path d="{d}" fill="{INK_3}"/>')
    return "".join(b), PAPER


DESIGNS = [
    ("A", "에디토리얼", dsn_a, dsn_a_back),
    ("B", "여백형", dsn_b, dsn_b_back),
    ("C", "역상 딥파인", dsn_c, dsn_c_back),
]


# ══════════════════════════════════════════════════════════════════════
# 출력
# ══════════════════════════════════════════════════════════════════════
def write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
    return path


MM2PT = 72.0 / 25.4


def to_pdf(svg_path, pdf_path):
    """svglib + reportlab 으로 벡터 PDF 생성 후, 인쇄소가 읽는 TrimBox/BleedBox 를 기록한다.
       MediaBox = 도련 포함 전체(96×56mm), TrimBox = 재단 사이즈(90×50mm).
       실패하면 None."""
    try:
        from svglib.svglib import svg2rlg
        from reportlab.graphics import renderPDF
        drawing = svg2rlg(svg_path)
        if drawing is None:
            return None
        renderPDF.drawToFile(drawing, pdf_path)
    except Exception as e:
        print(f"    ! PDF 실패({e.__class__.__name__}) — 건너뜀")
        return None

    try:
        from pypdf import PdfReader, PdfWriter
        from pypdf.generic import RectangleObject
        r = PdfReader(pdf_path)
        w = PdfWriter()
        for page in r.pages:
            # 좌하단 원점. 도련 3mm 안쪽이 재단선.
            page.bleedbox = RectangleObject([0, 0, W * MM2PT, H * MM2PT])
            page.trimbox = RectangleObject([
                BLEED * MM2PT, BLEED * MM2PT,
                (BLEED + TRIM_W) * MM2PT, (BLEED + TRIM_H) * MM2PT,
            ])
            page.artbox = page.trimbox
            w.add_page(page)
        w.add_metadata({
            "/Title": "SHIELDUS LAB 명함",
            "/Creator": "shilderslab.com / tools/build-card.py",
            "/Subject": f"trim {TRIM_W:.0f}x{TRIM_H:.0f}mm, bleed {BLEED:.0f}mm, fonts outlined",
        })
        with open(pdf_path, "wb") as f:
            w.write(f)
    except Exception as e:
        print(f"    ! TrimBox 기록 실패({e.__class__.__name__}) — PDF 는 생성됨")
    return pdf_path


def to_raster(svg_path, out_dir, base, dpi=300):
    """sharp(node)로 300dpi PNG·JPG. node/sharp 없으면 건너뜀."""
    px_w = round(W / 25.4 * dpi)
    px_h = round(H / 25.4 * dpi)
    script = f"""
import sharp from 'sharp';
(async()=>{{
  const s=sharp({json.dumps(svg_path)},{{density:{dpi*2}}}).resize({px_w},{px_h});
  await s.clone().png({{compressionLevel:9}}).withMetadata({{density:{dpi}}})
    .toFile({json.dumps(os.path.join(out_dir, base + '@300.png'))});
  await s.clone().flatten({{background:'#ffffff'}}).jpeg({{quality:96,chromaSubsampling:'4:4:4'}})
    .withMetadata({{density:{dpi}}})
    .toFile({json.dumps(os.path.join(out_dir, base + '@300.jpg'))});
  console.log('{px_w}x{px_h}');
}})().catch(e=>{{console.error('RASTER_FAIL',e.message);process.exit(1)}});
"""
    tool = os.environ.get("SL_SHARP_DIR", "")
    if not tool:
        return None
    p = os.path.join(tool, "_card_conv.mjs")
    with open(p, "w", encoding="utf-8") as f:
        f.write(script)
    r = subprocess.run(["node", p], capture_output=True, text=True, cwd=tool)
    if r.returncode != 0:
        print(f"    ! 래스터 실패: {r.stderr.strip()[:80]}")
        return None
    return r.stdout.strip()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--name", default="홍길동")
    ap.add_argument("--title", default="대표")
    ap.add_argument("--dept", default="")
    ap.add_argument("--mobile", default="010-0000-0000")
    ap.add_argument("--phone", default="")
    ap.add_argument("--email", default="contact@shilderslab.com")
    ap.add_argument("--web", default="shilderslab.com")
    ap.add_argument("--addr", default="")
    ap.add_argument("--out", default=os.path.join(ROOT, "assets/ci/card"))
    ap.add_argument("--list", action="store_true")
    a = ap.parse_args()

    p = dict(name=a.name, title=a.title, dept=a.dept, mobile=a.mobile,
             phone=a.phone, email=a.email, web=a.web, addr=a.addr)

    if a.list:
        for k, label, _, _ in DESIGNS:
            print(f"  시안 {k} · {label} — front/back × svg/pdf/png/jpg")
        return

    print(f"명함 생성 — 재단 {TRIM_W}×{TRIM_H}mm + 도련 {BLEED}mm (캔버스 {W}×{H}mm)")
    made = []
    for key, label, f_front, f_back in DESIGNS:
        for side, fn in (("front", f_front), ("back", f_back)):
            body, bg = fn(p)
            base = f"card-{key}-{side}"
            sp = write(os.path.join(a.out, base + ".svg"), svg(body, bg))
            gp = write(os.path.join(a.out, base + "-guide.svg"), svg(body + guide_overlay(), bg))
            pdf = to_pdf(sp, os.path.join(a.out, base + ".pdf"))
            rast = to_raster(sp, a.out, base)
            made.append(base)
            print(f"  ✓ 시안 {key} {side:<5} svg{' · pdf' if pdf else ''}"
                  f"{' · png/jpg ' + rast if rast else ''}  (guide 포함)")
    print(f"\n완료: {a.out}  ({len(made)}면)")


if __name__ == "__main__":
    main()
