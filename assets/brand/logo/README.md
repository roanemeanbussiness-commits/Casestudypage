# Aethon logo files

All PNGs. Every file except the two `profile-*` ones has a transparent
background, so it drops onto any colour without a white box behind it.

## The mark on its own

| File | Use |
|---|---|
| `aethon-mark-1024.png` | Master. Start here for anything print or large. |
| `aethon-mark-512.png` / `-256.png` / `-128.png` | Web and documents. |
| `aethon-mark-square-1024.png` / `-512.png` / `-256.png` | Padded to exactly 1:1, still transparent. App icons, anywhere a square is required. |
| `aethon-mark.ico` | Browser tabs and Windows. Contains 16px through 256px. |

## Profile pictures

| File | Use |
|---|---|
| `aethon-profile-light-1024.png` | White ground. LinkedIn, X, Instagram. |
| `aethon-profile-dark-1024.png` | Brand dark `#0c0b09`. |

These are the only two without transparency, because profile pictures get
composited onto whatever the platform decides and transparency there turns
into a grey or black square.

## Full lockup (mark plus wordmark)

| File | Use |
|---|---|
| `aethon-lockup-light-1600.png` / `-800.png` | Dark type. Use on light backgrounds. |
| `aethon-lockup-dark-1600.png` / `-800.png` | Light type. Use on dark backgrounds. |

Pick by the background you are placing it on, not by the name of the file.

## Regenerating

`../logokit.py` rebuilds everything from `assets/logo.png`.

The source has a white ground and a faint non-zero alpha across the entire
canvas, so a plain alpha bounding box does not find the artwork and returns
almost the whole 1024x1536 frame. The script crops to actual ink instead,
which is 880x903 and very close to square. Anything that trims this logo
needs to do the same, or it ends up with a mark surrounded by dead space.
