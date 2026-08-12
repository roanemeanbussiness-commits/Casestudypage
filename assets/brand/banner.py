#!/usr/bin/env python3
"""Render the Aethon LinkedIn banner at LinkedIn's exact 1584x396.

Text and logo are rendered, not generated, so the wordmark is sharp, the
saffron is the exact brand hex, and the mark is the real file.
"""
import base64, io, re, pathlib, subprocess
from PIL import Image

HERE = pathlib.Path(__file__).parent
SITE = pathlib.Path(__file__).parents[2]

# ---- logo: trim the baked-in white ground and make it transparent ----
im = Image.open(SITE / "assets/logo.png").convert("RGBA")
px = im.load()
w, h = im.size
for y in range(h):
    for x in range(w):
        r, g, b, a = px[x, y]
        if r > 244 and g > 244 and b > 244:
            px[x, y] = (r, g, b, 0)
im = im.crop(im.getchannel("A").getbbox())
im.thumbnail((520, 520), Image.LANCZOS)
buf = io.BytesIO()
im.save(buf, "PNG", optimize=True)
LOGO = base64.b64encode(buf.getvalue()).decode()
print("logo trimmed to", im.size)

# ---- fonts: reuse the latin faces already fetched for the page ----
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

TEMPLATE = """<!doctype html><meta charset="utf-8"><style>
%(faces)s
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:1584px;height:396px;overflow:hidden}
.banner{position:relative;width:1584px;height:396px;display:flex;align-items:center;
  background:%(bg)s;font-family:"Inter",sans-serif;overflow:hidden}

/* saffron light source, behind the mark */
.glow{position:absolute;left:80px;top:50%%;width:820px;height:820px;
  transform:translateY(-50%%);border-radius:50%%;
  background:radial-gradient(circle,rgba(255,164,28,%(glow)s) 0%%,rgba(255,164,28,0) 62%%)}

/* faint ray geometry, echoing the sun mark without competing with it */
.rays{position:absolute;left:-99px;top:50%%;width:1100px;height:1100px;
  transform:translateY(-50%%);opacity:%(rays)s;
  background:repeating-conic-gradient(from 0deg at 50%% 50%%,
    %(ray)s 0deg 1deg, transparent 1deg 7.5deg);
  -webkit-mask-image:radial-gradient(circle,transparent 9%%,#000 17%%,transparent 46%%);
          mask-image:radial-gradient(circle,transparent 9%%,#000 17%%,transparent 46%%)}

/* LinkedIn drops the avatar over the lower left, so that column stays empty */
.safe{width:392px;flex:none}

.lockup{position:relative;display:flex;align-items:center;gap:34px}
.mark{width:152px;height:152px;flex:none;object-fit:contain;
  filter:drop-shadow(0 6px 22px rgba(255,164,28,.34))}
.word{display:flex;flex-direction:column;gap:11px}
.word b{font-family:"Fraunces",Georgia,serif;font-weight:400;font-size:76px;
  line-height:.92;letter-spacing:-.018em;color:%(ink)s}
.word b em{font-style:normal;color:#ffa41c}
.word i{font-style:normal;font-size:15px;font-weight:600;letter-spacing:.42em;
  text-transform:uppercase;color:%(muted)s;padding-left:3px}

.rule{position:relative;width:1px;height:132px;margin:0 52px;
  background:linear-gradient(180deg,transparent,%(line)s 22%%,%(line)s 78%%,transparent)}

.say{position:relative;max-width:430px;display:flex;flex-direction:column;gap:15px}
.say strong{font-family:"Fraunces",Georgia,serif;font-weight:300;font-size:29px;
  line-height:1.26;letter-spacing:-.01em;color:%(ink)s}
.say strong em{font-style:normal;color:#ffa41c}
.say span{font-size:14.5px;font-weight:450;line-height:1.6;color:%(muted)s}

/* saffron edge, so the banner still reads as branded when scaled down */
.edge{position:absolute;left:0;right:0;bottom:0;height:5px;
  background:linear-gradient(90deg,#ffa41c,#ffc46b 46%%,#ffa41c)}
</style>
<div class="banner">
  <div class="glow"></div><div class="rays"></div>
  <div class="safe"></div>
  <div class="lockup">
    <img class="mark" src="data:image/png;base64,%(logo)s" alt="" />
    <span class="word"><b>Aethon</b><i>Intelligence</i></span>
  </div>
  <div class="rule"></div>
  <div class="say">
    <strong>AI systems your business <em>actually owns</em>.</strong>
    <span>We audit how you run it, build the system around it, and hand you the keys.</span>
  </div>
  <div class="edge"></div>
</div>"""

THEMES = {
    "light": dict(bg="linear-gradient(105deg,#ffffff 0%,#fffaf2 52%,#fff3e0 100%)",
                  ink="#14120e", muted="#6f6a60", line="rgba(20,18,14,.20)",
                  glow=".20", rays=".13", ray="#c98c2a"),
    "dark":  dict(bg="linear-gradient(105deg,#0c0b09 0%,#131108 55%,#1b1508 100%)",
                  ink="#f3ece0", muted="#a09889", line="rgba(243,236,224,.24)",
                  glow=".26", rays=".20", ray="#ffc46b"),
}

for name, t in THEMES.items():
    (HERE / f"banner-{name}.html").write_text(
        TEMPLATE % dict(t, faces="\n".join(faces), logo=LOGO))
    print("wrote", f"banner-{name}.html")
