#!/usr/bin/env python3
"""Aethon LinkedIn banner, light. Rendered at 3x and downsampled for crispness.

Three things do the sharpening: a luminance-keyed alpha on the logo so it has
no white fringe, rays drawn as real SVG strokes instead of a conic gradient,
and Fraunces pinned to its 144pt optical size, which is the display cut with
finer serifs and higher contrast.
"""
import base64, io, math, re, pathlib, subprocess
from PIL import Image

HERE = pathlib.Path(__file__).parent
SITE = pathlib.Path(__file__).parents[2]

# ---- logo: key out the white ground without leaving a grey halo ----
src = Image.open(SITE / "assets/logo.png").convert("RGBA")
px = src.load()
for y in range(src.height):
    for x in range(src.width):
        r, g, b, a = px[x, y]
        if a == 0:                              # already transparent: leave it
            continue
        hi, lo = max(r, g, b), min(r, g, b)
        if hi - lo < 20 and hi > 198:           # near-neutral and bright: ground
            keyed = max(0, min(255, round((255 - hi) * 255 / 57)))
            px[x, y] = (r, g, b, min(a, keyed))
        else:                                   # anything with colour stays
            px[x, y] = (r, g, b, a)
src = src.crop(src.getchannel("A").getbbox())
src.thumbnail((640, 640), Image.LANCZOS)
buf = io.BytesIO(); src.save(buf, "PNG", optimize=True)
LOGO = base64.b64encode(buf.getvalue()).decode()
print("logo", src.size)

# ---- rays: real strokes, so they stay sharp at any scale ----
RAYS, R0, R1 = 44, 78, 470
lines = []
for i in range(RAYS):
    a = 2 * math.pi * i / RAYS
    ca, sa = math.cos(a), math.sin(a)
    # Alternate long and short rays, the way the mark's own points do.
    r1 = R1 if i % 2 == 0 else R1 * 0.72
    lines.append(f'<line x1="{R0*ca:.1f}" y1="{R0*sa:.1f}" '
                 f'x2="{r1*ca:.1f}" y2="{r1*sa:.1f}" />')
def ray_svg(ray):
  return (
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="-550 -550 1100 1100">'
    '<defs><radialGradient id="f">'
    '<stop offset="6%" stop-color="#fff" stop-opacity="0"/>'
    '<stop offset="15%" stop-color="#fff" stop-opacity="1"/>'
    '<stop offset="30%" stop-color="#fff" stop-opacity=".78"/>'
    '<stop offset="48%" stop-color="#fff" stop-opacity="0"/>'
    '</radialGradient>'
    '<mask id="m"><circle r="550" fill="url(#f)"/></mask></defs>'
    f'<g mask="url(#m)" stroke="{ray}" stroke-width="1.5" stroke-linecap="round">'
    f'{"".join(lines)}</g></svg>')
def ray_uri(ray):
    return "data:image/svg+xml;base64," + base64.b64encode(ray_svg(ray).encode()).decode()

# ---- fonts ----
faces = []
for subset, block in re.findall(r"/\*\s*([\w\-\[\]]+)\s*\*/\s*(@font-face\s*\{.*?\})",
                                (HERE / "fonts.css").read_text(), re.S):
    if subset != "latin":
        continue
    url = re.search(r"url\((https://[^)]+)\)", block).group(1)
    data = subprocess.run(["curl", "-sS", "-A", "Mozilla/5.0", url],
                          capture_output=True, check=True).stdout
    faces.append(re.sub(r"url\(https://[^)]+\)",
                        f"url(data:font/woff2;base64,{base64.b64encode(data).decode()})", block))

HTML = """<!doctype html><meta charset="utf-8"><style>
%(faces)s
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:1584px;height:396px;overflow:hidden;background:%(page)s}
.banner{position:relative;width:1584px;height:396px;display:flex;align-items:center;
  font-family:"Inter",sans-serif;overflow:hidden;
  background:
    radial-gradient(1200px 620px at 29%% 50%%, %(lift)s 0%%, rgba(255,253,249,0) 70%%),
    %(bg)s;
  text-rendering:geometricPrecision;
  -webkit-font-smoothing:antialiased}

.glow{position:absolute;left:75px;top:50%%;width:800px;height:800px;
  transform:translateY(-50%%);border-radius:50%%;
  background:radial-gradient(circle,rgba(255,164,28,.17) 0%%,rgba(255,178,64,.07) 34%%,rgba(255,164,28,0) 66%%)}
.rays{position:absolute;left:-75px;top:50%%;width:1100px;height:1100px;
  transform:translateY(-50%%);opacity:.34}

/* soft scrim so the ray field does not ghost through the wordmark */
.scrim{position:absolute;left:520px;top:50%%;width:600px;height:320px;
  transform:translateY(-50%%);
  background:radial-gradient(ellipse at center,%(scrimA)s 0%%,
    %(scrimB)s 45%%,%(scrim0)s 74%%)}

/* LinkedIn drops the profile photo over the lower left; that column stays empty */
.safe{width:392px;flex:none}

.lockup{position:relative;display:flex;align-items:center;gap:36px}
.mark{width:172px;height:172px;flex:none;object-fit:contain;
  filter:drop-shadow(0 5px 20px rgba(214,140,26,.30))}
.word{display:flex;flex-direction:column;gap:13px}
.word b{font-family:"Fraunces",Georgia,serif;font-weight:400;font-size:86px;
  font-variation-settings:"opsz" 144;
  line-height:.9;letter-spacing:-.021em;color:%(ink)s}
.word i{font-style:normal;font-size:17px;font-weight:600;letter-spacing:.42em;
  text-transform:uppercase;color:%(muted)s;padding-left:4px}

.rule{position:relative;width:1px;height:160px;margin:0 50px;
  background:linear-gradient(180deg,%(rule0)s,%(rule)s 20%%,%(rule)s 80%%,%(rule0)s)}

.say{position:relative;max-width:600px;display:flex;flex-direction:column;gap:18px}
.say strong{font-family:"Fraunces",Georgia,serif;font-weight:400;font-size:44px;
  font-variation-settings:"opsz" 120;
  line-height:1.16;letter-spacing:-.015em;color:%(ink2)s}
.say strong em{font-style:normal;color:%(accent)s}
.say span{font-size:21px;font-weight:500;letter-spacing:.005em;line-height:1.5;color:%(muted2)s}

.edge{position:absolute;left:0;right:0;bottom:0;height:4px;
  background:linear-gradient(90deg,#f39c14,#ffc257 44%%,#f39c14)}
</style>
<div class="banner">
  <div class="glow"></div>
  <img class="rays" src="%(rays)s" alt="" />
  <div class="scrim"></div>
  <div class="safe"></div>
  <div class="lockup">
    <img class="mark" src="data:image/png;base64,%(logo)s" alt="" />
    <span class="word"><b>Aethon</b><i>Intelligence</i></span>
  </div>
  <div class="rule"></div>
  <div class="say">
    <strong>AI systems your business<br /><em>actually owns</em>.</strong>
    <span>Audited. Built. Owned by you.</span>
  </div>
  <div class="edge"></div>
</div>"""

THEMES = {
  "light": dict(
    page="#fff", ray="#d08f22", accent="#e8930f",
    bg="linear-gradient(100deg,#ffffff 0%,#fffdf8 46%,#fff4e2 100%)",
    lift="#fffdf9", ink="#100e0b", ink2="#181510", muted="#8a8172", muted2="#6a6255",
    rule="rgba(20,18,14,.22)", rule0="rgba(20,18,14,0)",
    scrimA="rgba(255,253,249,.95)", scrimB="rgba(255,253,249,.72)", scrim0="rgba(255,253,249,0)"),
  "dark": dict(
    page="#0c0b09", ray="#e8a83e", accent="#ffb43c",
    bg="linear-gradient(100deg,#0c0b09 0%,#131108 52%,#1c1608 100%)",
    lift="rgba(46,34,10,.55)", ink="#f6f0e5", ink2="#efe8db", muted="#9c9384", muted2="#b0a795",
    rule="rgba(246,240,229,.24)", rule0="rgba(246,240,229,0)",
    scrimA="rgba(14,12,9,.88)", scrimB="rgba(14,12,9,.62)", scrim0="rgba(14,12,9,0)"),
}

for name, t in THEMES.items():
    (HERE / f"banner-{name}.html").write_text(
        HTML % dict(t, faces="\n".join(faces), logo=LOGO, rays=ray_uri(t["ray"])))
    print("wrote", f"banner-{name}.html")
