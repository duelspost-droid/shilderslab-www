#!/usr/bin/env python3
"""
쉴더스랩 CI 벡터 원본 빌더
  · 워드마크는 Manrope / Noto Sans KR (SIL OFL) 글리프를 **아웃라인 패스로 변환**해 임베드
    → 폰트 설치 여부와 무관하게 어디서나 동일 렌더, 인쇄·간판 등 로우데이터로 재사용 가능
  · 심볼은 실드 실루엣 + 'S' 네거티브 스페이스를 단일 컴파운드 패스(fill-rule=evenodd)로 구성
    → 일러스트레이터에서 컴파운드 패스 하나로 열리고, 단색 각인·커팅에도 그대로 사용 가능
"""
import json, os, sys
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.boundsPen import BoundsPen
from fontTools.misc.transform import Identity

SRC = os.path.dirname(os.path.abspath(__file__))
OUT = sys.argv[1] if len(sys.argv) > 1 else "/Users/hk/shilderslab-www/assets/ci"
MANROPE = os.path.join(SRC, "Manrope.ttf")
NOTOKR = os.path.join(SRC, "NotoSansKR.ttf")

# ─────────── 브랜드 컬러 (site.css 토큰과 동일) ───────────
CY_200, CY_300, CY_400, CY_500, CY_600 = "#B4F6FF", "#7CEBFB", "#38D8EF", "#12B5CE", "#0A8CA3"
VI_400 = "#8B93F8"
INK_950, INK_900, INK_850 = "#03070E", "#050B16", "#08111F"
WHITE, FG_DIM = "#FFFFFF", "#B8C8DC"

_cache = {}


def font(path, wght):
    key = (path, wght)
    if key not in _cache:
        f = TTFont(path)
        if "fvar" in f:
            f = instantiateVariableFont(f, {"wght": wght}, inplace=True, updateFontNames=False)
        _cache[key] = f
    return _cache[key]


def text_path(text, fpath, wght, cap, tracking=0.0, x0=0.0, baseline=0.0):
    """문자열을 SVG 패스 d 로. 반환: (d, advance_width, ink_bbox(x1,y1,x2,y2))"""
    f = font(fpath, wght)
    cmap, gs, hmtx = f.getBestCmap(), f.getGlyphSet(), f["hmtx"]
    cap_units = getattr(f["OS/2"], "sCapHeight", None) or int(f["head"].unitsPerEm * 0.72)
    scale = cap / cap_units
    parts, x, bounds = [], float(x0), None
    for ch in text:
        g = cmap.get(ord(ch))
        if g is None:
            raise SystemExit(f"glyph missing: {ch!r}")
        if ch != " ":
            t = Identity.translate(x, baseline).scale(scale, -scale)
            sp = SVGPathPen(gs, ntos=lambda v: f"{v:.2f}")
            gs[g].draw(TransformPen(sp, t))
            if sp.getCommands():
                parts.append(sp.getCommands())
            bp = BoundsPen(gs)
            gs[g].draw(TransformPen(bp, t))
            if bp.bounds:
                bounds = bp.bounds if bounds is None else (
                    min(bounds[0], bp.bounds[0]), min(bounds[1], bp.bounds[1]),
                    max(bounds[2], bp.bounds[2]), max(bounds[3], bp.bounds[3]))
        x += hmtx[g][0] * scale + tracking * cap
    return " ".join(parts), round(x - tracking * cap - float(x0), 3), bounds


# ══════════════════════════════════════════════════════════════
# 심볼 — 64×64 그리드
#   실드: 상단 어깨 폭 50.8, 하단 첨점 (32,61.6), 좌우 대칭
# ══════════════════════════════════════════════════════════════
SHIELD = ("M32 2.4 L57.4 11.9 V32.2 C57.4 46.4 46.6 57.9 32 61.6 "
          "C17.4 57.9 6.6 46.4 6.6 32.2 V11.9 Z")
SHIELD_INNER = ("M32 8.1 L52 15.6 V32 C52 43.1 43.6 52.3 32 55.6 "
                "C20.4 52.3 12 43.1 12 32 V15.6 Z")

# 실드 안에 들어갈 'S' — ink bbox 기준으로 정확히 중앙 정렬
S_CAP = 27.5
_d, _adv, _bb = text_path("S", MANROPE, 800, S_CAP)
_cx, _cy = (_bb[0] + _bb[2]) / 2, (_bb[1] + _bb[3]) / 2
S_IN_SHIELD, _, _ = text_path("S", MANROPE, 800, S_CAP,
                              x0=32 - _cx, baseline=30.6 - _cy)

SYMBOL_COMPOUND = f"{SHIELD} {S_IN_SHIELD}"


def svg(w, h, body, extra=""):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" '
            f'width="{w}" height="{h}" role="img"{extra}>\n{body}\n</svg>\n')


def grad(gid, c1, c2, x2="1", y2="1"):
    return (f'<linearGradient id="{gid}" x1="0" y1="0" x2="{x2}" y2="{y2}">'
            f'<stop offset="0" stop-color="{c1}"/><stop offset="1" stop-color="{c2}"/>'
            f'</linearGradient>')


def write(name, content):
    path = os.path.join(OUT, name)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  ✓ {name}  ({len(content):,}B)")


# ─────────── 1) 심볼 (컬러 / 모노) ───────────
write("symbol.svg", svg(64, 64,
      '<title>쉴더스랩 심볼</title>\n<defs>\n ' + grad("slSym", CY_300, CY_500) + '\n'
      ' <linearGradient id="slSymEdge" x1="0" y1="0" x2="1" y2="1">'
      f'<stop offset="0" stop-color="{CY_200}" stop-opacity=".9"/>'
      f'<stop offset="1" stop-color="{VI_400}" stop-opacity=".55"/></linearGradient>\n</defs>\n'
      f'<path d="{SYMBOL_COMPOUND}" fill="url(#slSym)" fill-rule="evenodd"/>\n'
      f'<path d="{SHIELD_INNER}" fill="none" stroke="{INK_950}" stroke-opacity=".22" stroke-width="1.1"/>\n'
      f'<path d="{SHIELD}" fill="none" stroke="url(#slSymEdge)" stroke-width="1.2"/>'))

write("symbol-mono.svg", svg(64, 64,
      '<title>쉴더스랩 심볼 · 단색(currentColor)</title>\n'
      f'<path d="{SYMBOL_COMPOUND}" fill="currentColor" fill-rule="evenodd"/>'))

for tag, col in (("white", WHITE), ("black", INK_950)):
    write(f"symbol-mono-{tag}.svg", svg(64, 64,
          f'<title>쉴더스랩 심볼 · 단색 {tag}</title>\n'
          f'<path d="{SYMBOL_COMPOUND}" fill="{col}" fill-rule="evenodd"/>'))

# ─────────── 2) 워드마크 (순수 패스) ───────────
EN_CAP, KO_CAP = 100, 74
en_d, en_w, _ = text_path("SHILDERS LAB", MANROPE, 800, EN_CAP, tracking=0.035, baseline=EN_CAP)
ko_d, ko_w, _ = text_path("쉴더스랩", NOTOKR, 700, KO_CAP, tracking=0.02, baseline=KO_CAP)

write("wordmark-en.svg", svg(round(en_w, 1), EN_CAP,
      '<title>SHILDERS LAB 영문 워드마크</title>\n'
      f'<path d="{en_d}" fill="currentColor"/>'))
write("wordmark-ko.svg", svg(round(ko_w, 1), KO_CAP,
      '<title>쉴더스랩 국문 워드마크</title>\n'
      f'<path d="{ko_d}" fill="currentColor"/>'))

# ─────────── 3) 가로 락업 (심볼 + 영문 워드마크 + 국문) ───────────
#  심볼 64 · 간격 22 · 영문 cap 30 (baseline y=36) · 국문 cap 15 (baseline y=57)
SY = 64
GAP = 22
TX = SY + GAP
en_l_d, en_l_w, _ = text_path("SHILDERS LAB", MANROPE, 800, 30, tracking=0.035, x0=TX, baseline=36.0)
ko_l_d, ko_l_w, _ = text_path("쉴더스랩 · 정보보호 컨설팅", NOTOKR, 500, 14, tracking=0.02, x0=TX + 1.2, baseline=57.0)
LOCK_W = round(TX + max(en_l_w, ko_l_w) + 2, 1)


def lockup(sym_fill, en_fill, ko_fill, defs="", title="쉴더스랩 로고"):
    return svg(LOCK_W, SY,
               f'<title>{title}</title>\n'
               + (f'<defs>\n {defs}\n</defs>\n' if defs else "")
               + f'<path d="{SYMBOL_COMPOUND}" fill="{sym_fill}" fill-rule="evenodd"/>\n'
               + f'<path d="{en_l_d}" fill="{en_fill}"/>\n'
               + f'<path d="{ko_l_d}" fill="{ko_fill}"/>')


write("lockup-horizontal-dark.svg", lockup("url(#slLockD)", WHITE, CY_300,
      grad("slLockD", CY_300, CY_500), "쉴더스랩 로고 · 어두운 배경용"))
write("lockup-horizontal-light.svg", lockup("url(#slLockL)", INK_950, CY_600,
      grad("slLockL", CY_500, CY_600), "쉴더스랩 로고 · 밝은 배경용"))
write("lockup-mono-white.svg", lockup(WHITE, WHITE, WHITE, "", "쉴더스랩 로고 · 단색 white"))
write("lockup-mono-black.svg", lockup(INK_950, INK_950, INK_950, "", "쉴더스랩 로고 · 단색 black"))

# ─────────── 4) 세로 락업 ───────────
st_en_d, st_en_w, _ = text_path("SHILDERS LAB", MANROPE, 800, 26, tracking=0.05, baseline=0)
st_ko_d, st_ko_w, _ = text_path("쉴더스랩", NOTOKR, 500, 15, tracking=0.06, baseline=0)
SW = round(max(st_en_w, st_ko_w, 64) + 8, 1)
SH = 64 + 26 + 30 + 18
st_en_d2, _, _ = text_path("SHILDERS LAB", MANROPE, 800, 26, tracking=0.05,
                           x0=(SW - st_en_w) / 2, baseline=64 + 30)
st_ko_d2, _, _ = text_path("쉴더스랩", NOTOKR, 500, 15, tracking=0.06,
                           x0=(SW - st_ko_w) / 2, baseline=64 + 30 + 24)
write("lockup-stacked-dark.svg", svg(SW, SH,
      '<title>쉴더스랩 로고 · 세로형(어두운 배경)</title>\n<defs>\n ' + grad("slStk", CY_300, CY_500) + '\n</defs>\n'
      f'<g transform="translate({round((SW-64)/2,2)} 0)"><path d="{SYMBOL_COMPOUND}" '
      f'fill="url(#slStk)" fill-rule="evenodd"/></g>\n'
      f'<path d="{st_en_d2}" fill="{WHITE}"/>\n<path d="{st_ko_d2}" fill="{CY_300}"/>'))

# ─────────── 5) 파비콘 (16~32px 가독 최적화: 라운드 사각 + 실드 S) ───────────
fav_s_d, _, fav_bb = text_path("S", MANROPE, 800, 19)
fcx, fcy = (fav_bb[0] + fav_bb[2]) / 2, (fav_bb[1] + fav_bb[3]) / 2
fav_s, _, _ = text_path("S", MANROPE, 800, 19, x0=16 - fcx, baseline=16 - fcy)
write("favicon.svg", svg(32, 32,
      '<title>쉴더스랩</title>\n<defs>\n ' + grad("slFav", CY_300, CY_500) + '\n</defs>\n'
      '<rect width="32" height="32" rx="7.5" fill="url(#slFav)"/>\n'
      f'<path d="{fav_s}" fill="{INK_950}"/>'))

# 마스크 아이콘(사파리 pinned tab 등) — 단색 실루엣
write("mask-icon.svg", svg(64, 64,
      '<title>쉴더스랩 마스크 아이콘</title>\n'
      f'<path d="{SYMBOL_COMPOUND}" fill="black" fill-rule="evenodd"/>'))

# ─────────── 6) OG 커버 1200×630 ───────────
og_en, og_en_w, _ = text_path("SHILDERS LAB", MANROPE, 800, 76, tracking=0.03, x0=96, baseline=340)
og_ko, _, _ = text_path("정보보호 컨설팅 · 쉴더스랩", NOTOKR, 500, 26, tracking=0.03, x0=98, baseline=404)
og_tag, _, _ = text_path("ISMS-P · 모의해킹 · 취약점진단 · 클라우드보안 · 개인정보 컴플라이언스",
                         NOTOKR, 500, 19, tracking=0.02, x0=98, baseline=470)
og_dom, _, _ = text_path("shilderslab.com", MANROPE, 700, 20, tracking=0.08, x0=98, baseline=552)
write("og-cover.svg", svg(1200, 630,
      '<title>쉴더스랩 · 정보보호 컨설팅</title>\n<defs>\n'
      f' <linearGradient id="ogBg" x1="0" y1="0" x2="1" y2="1">'
      f'<stop offset="0" stop-color="#071426"/><stop offset=".55" stop-color="{INK_900}"/>'
      f'<stop offset="1" stop-color="{INK_950}"/></linearGradient>\n'
      f' <radialGradient id="ogGlow" cx=".82" cy=".12" r=".6">'
      f'<stop offset="0" stop-color="{CY_400}" stop-opacity=".3"/>'
      f'<stop offset="1" stop-color="{CY_400}" stop-opacity="0"/></radialGradient>\n'
      f' <radialGradient id="ogGlow2" cx=".08" cy=".95" r=".55">'
      f'<stop offset="0" stop-color="{VI_400}" stop-opacity=".26"/>'
      f'<stop offset="1" stop-color="{VI_400}" stop-opacity="0"/></radialGradient>\n'
      ' <pattern id="ogGrid" width="48" height="48" patternUnits="userSpaceOnUse">'
      '<path d="M48 0 H0 V48" fill="none" stroke="#FFFFFF" stroke-opacity=".045" stroke-width="1"/></pattern>\n'
      ' ' + grad("ogSym", CY_300, CY_500) + '\n</defs>\n'
      '<rect width="1200" height="630" fill="url(#ogBg)"/>\n'
      '<rect width="1200" height="630" fill="url(#ogGrid)"/>\n'
      '<rect width="1200" height="630" fill="url(#ogGlow)"/>\n'
      '<rect width="1200" height="630" fill="url(#ogGlow2)"/>\n'
      f'<rect x="0" y="0" width="1200" height="4" fill="url(#ogSym)"/>\n'
      f'<g transform="translate(96 108) scale(1.86)"><path d="{SYMBOL_COMPOUND}" '
      f'fill="url(#ogSym)" fill-rule="evenodd"/></g>\n'
      f'<path d="{og_en}" fill="{WHITE}"/>\n'
      f'<path d="{og_ko}" fill="{CY_300}"/>\n'
      f'<path d="{og_tag}" fill="{FG_DIM}"/>\n'
      f'<path d="{og_dom}" fill="{CY_500}"/>\n'
      f'<g transform="translate(1104 96)"><path d="{SYMBOL_COMPOUND}" fill="{WHITE}" '
      f'fill-opacity=".07" fill-rule="evenodd" transform="scale(4.6) translate(-32 -14)"/></g>'))

meta = {
    "symbol_grid": 64, "shield": SHIELD, "s_cap": S_CAP,
    "lockup_width": LOCK_W, "wordmark_en_width": round(en_w, 2),
    "colors": {"cy200": CY_200, "cy300": CY_300, "cy400": CY_400, "cy500": CY_500,
               "cy600": CY_600, "vi400": VI_400, "ink950": INK_950, "ink900": INK_900},
    "fonts": {"latin": "Manrope ExtraBold (SIL OFL 1.1) — 아웃라인 변환",
              "hangul": "Noto Sans KR (SIL OFL 1.1) — 아웃라인 변환"},
}
write("ci-meta.json", json.dumps(meta, ensure_ascii=False, indent=2) + "\n")
print("\n완료:", OUT)
