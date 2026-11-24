"""Build the Ivy T mark and logo lockup from the live logo's measured rectangles.

The live IVYCPA-TAX-LOGO-.png (409x398) is entirely axis-aligned bars, so the
mark is rebuilt exactly from the bars measured in the browser (normalized to the
mark's own 219x200 box). Text is outlined with fontTools so logo.svg needs no fonts.
"""
import json, sys, os
from fontTools.ttLib import TTFont, TTCollection
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen

HERE = os.path.dirname(os.path.abspath(__file__))
FONTS = sys.argv[1] if len(sys.argv) > 1 else "fonts"

# bars of the mark, normalized to a 219 x 200 box (x, y, w, h)
BARS = [
    (0, 0, 219, 18), (0, 18, 18, 45), (201, 18, 18, 45), (0, 63, 55, 19),
    (101, 63, 118, 19), (101, 82, 18, 84),            # outer spiral
    (69, 32, 118, 18), (69, 50, 18, 132), (132, 95, 18, 87), (69, 182, 81, 18),  # inner spiral
]
RED = (32, 32, 23, 18)

def bars_path(bars, ox=0, oy=0, s=1.0):
    return "".join(f"M{(x+ox)*s:g} {(y+oy)*s:g}h{w*s:g}v{h*s:g}h{-w*s:g}z" for x, y, w, h in bars)

MARK = bars_path(BARS)
REDP = bars_path([RED])

def outline(font, text, size, x0, y0, tracking=0.0):
    gs = font.getGlyphSet(); cmap = font.getBestCmap(); upm = font["head"].unitsPerEm
    hmtx = font["hmtx"]; s = size / upm; x = x0; parts = []
    for ch in text:
        g = cmap.get(ord(ch))
        if g is None:
            x += size * 0.3; continue
        pen = SVGPathPen(gs)
        tp = TransformPen(pen, (s, 0, 0, -s, x, y0))
        gs[g].draw(tp)
        parts.append(pen.getCommands())
        x += hmtx[g][0] * s + tracking * size
    return " ".join(parts), x - x0

def sc_font():
    ttc = TTCollection("/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc")
    for f in ttc.fonts:
        if "SC" in f["name"].getDebugName(1):
            return f
    return ttc.fonts[0]

if __name__ == "__main__":
    out = sys.argv[2] if len(sys.argv) > 2 else HERE
    pop = TTFont(os.path.join(FONTS, "Poppins-Medium.ttf"))
    sc = sc_font()
    # lockup: mark centered over 安腾会计 / Ivy Tax & Business (matches the live stacked logo)
    zh, zw = outline(sc, "安腾会计", 46, 0, 0, tracking=0.08)
    en, ew = outline(pop, "Ivy Tax & Business", 26, 0, 0)
    W = max(219, zw, ew) + 20
    mx = (W - 219) / 2
    zx = (W - zw) / 2; ex = (W - ew) / 2
    zh, _ = outline(sc, "安腾会计", 46, zx, 262, tracking=0.08)
    en, _ = outline(pop, "Ivy Tax & Business", 26, ex, 306)
    H = 320
    logo = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W:g} {H}" role="img" aria-label="Ivy Tax &amp; Business 安腾会计">
<path fill="#2E3192" d="{bars_path(BARS, mx, 0)}"/>
<path fill="#E5231B" d="{bars_path([RED], mx, 0)}"/>
<path fill="#4A4D57" d="{zh}"/>
<path fill="#4A4D57" d="{en}"/>
</svg>
'''
    open(os.path.join(out, "logo.svg"), "w").write(logo)
    fav = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="14" fill="#2E3192"/><g transform="translate(9.5 11.5) scale(0.205)"><path fill="#fff" d="{MARK}"/><path fill="#FF5A4E" d="{REDP}"/></g></svg>
'''
    open(os.path.join(out, "favicon.svg"), "w").write(fav)
    json.dump({"mark": MARK, "red": REDP, "zh": None}, open(os.path.join(HERE, "mark.json"), "w"))
    print("ok", W, H)
