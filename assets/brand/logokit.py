#!/usr/bin/env python3
"""Export the Aethon mark as a clean, transparent set.

The source file carries a white ground and a faint non-zero alpha across the
whole canvas, so an alpha bbox does not find the artwork. This crops to actual
ink instead, keys the white out, and writes the sizes you actually need.
"""
import base64, io, pathlib
from PIL import Image

SRC = pathlib.Path("/home/user/Landingpage/assets/logo.png")
OUT = pathlib.Path("/home/user/Landingpage/assets/brand/logo")
OUT.mkdir(parents=True, exist_ok=True)

DARK = (12, 11, 9)
PAD = 0.10           # breathing room inside square exports


def clean(im):
    """Key out the white ground, keep everything with colour."""
    im = im.convert("RGBA")
    px = im.load()
    for y in range(im.height):
        for x in range(im.width):
            r, g, b, a = px[x, y]
            hi, lo = max(r, g, b), min(r, g, b)
            if hi - lo < 20 and hi > 198:            # near-neutral, bright: ground
                px[x, y] = (r, g, b, min(a, max(0, round((255 - hi) * 255 / 57))))
            elif a < 250:                            # faint canvas noise
                px[x, y] = (r, g, b, 0 if a < 12 else a)
    return im


def ink_box(im):
    """Bounding box of real artwork, ignoring the ground and canvas noise."""
    px = im.load()
    xs, ys = [], []
    for y in range(im.height):
        for x in range(im.width):
            r, g, b, a = px[x, y]
            if a < 24:
                continue
            if max(r, g, b) - min(r, g, b) < 20 and max(r, g, b) > 198:
                continue
            xs.append(x); ys.append(y)
    return min(xs), min(ys), max(xs) + 1, max(ys) + 1


mark = clean(Image.open(SRC))
mark = mark.crop(ink_box(mark))
print("mark cropped to", mark.size)


def fit_square(src, size, bg=None):
    """Centre the mark on a square canvas, padded and optionally on a ground."""
    inner = round(size * (1 - PAD * 2))
    m = src.copy()
    m.thumbnail((inner, inner), Image.LANCZOS)
    canvas = Image.new("RGBA", (size, size), (*bg, 255) if bg else (0, 0, 0, 0))
    canvas.alpha_composite(m, ((size - m.width) // 2, (size - m.height) // 2))
    return canvas


# Transparent mark, natural proportions
for px_w in (1024, 512, 256, 128):
    m = mark.copy()
    m.thumbnail((px_w, px_w), Image.LANCZOS)
    m.save(OUT / f"aethon-mark-{px_w}.png", optimize=True)

# Square, transparent: app icons, favicons, anywhere needing 1:1
for px_w in (1024, 512, 256):
    fit_square(mark, px_w).save(OUT / f"aethon-mark-square-{px_w}.png", optimize=True)

# Square on a ground: profile pictures, which cannot use transparency
fit_square(mark, 1024, bg=(255, 255, 255)).convert("RGB") \
    .save(OUT / "aethon-profile-light-1024.png", optimize=True)
fit_square(mark, 1024, bg=DARK).convert("RGB") \
    .save(OUT / "aethon-profile-dark-1024.png", optimize=True)

# ICO for browser tabs and Windows
fit_square(mark, 256).save(OUT / "aethon-mark.ico",
                           sizes=[(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)])

for f in sorted(OUT.iterdir()):
    print(f" {f.name:34} {f.stat().st_size/1024:6.0f} KB")

# Hand the cleaned mark to the lockup renderer
buf = io.BytesIO(); mark.save(buf, "PNG", optimize=True)
(pathlib.Path(__file__).parent / "mark.b64").write_text(
    base64.b64encode(buf.getvalue()).decode())
