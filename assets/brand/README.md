# Brand assets

## LinkedIn banner

`linkedin-banner-light.png` and `linkedin-banner-dark.png` are sized to
LinkedIn's 1584x396. The `@2x` versions are the same artwork at double
resolution, for anywhere that wants a sharper file.

The left 392px is left empty on purpose: LinkedIn drops the profile photo
over the lower left of the banner, and anything placed there is hidden.

### Regenerating

`banner.py` renders both variants from `assets/logo.png` and `fonts.css`.
It needs Pillow and a headless Chromium to screenshot the HTML it writes:

```
python3 assets/brand/banner.py     # writes banner-light.html / banner-dark.html
```

Then screenshot each at 1584x396 with a deviceScaleFactor of 3 and downsample;
that is where the crispness comes from. Editing the tagline, colours, or spacing
means editing the template in that script, not the PNGs.

### Sizing the copy

LinkedIn renders the banner at roughly half its actual width, and crops a
little off the top and bottom. Type has to be sized for that, not for
1584x396: anything under about 20px in the file is unreadable on a real
profile. Check any change by scaling the export to 860px wide and reading
it at that size before uploading.
