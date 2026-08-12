# Aethon Intelligence — client results one-pager

A single static page of client case studies, built to be linked from LinkedIn
outreach. No build step, no dependencies.

```
index.html          the whole page
css/onepager.css    all styling
assets/logo.png     brand mark
vercel.json         static hosting config
```

## Deploying to Vercel

Import the repo at [vercel.com/new](https://vercel.com/new) and deploy — there is
no framework to select and no build command to set. Vercel serves `index.html`
at the root. Every push to this branch redeploys automatically.

To preview locally: `python3 -m http.server 8000` and open `localhost:8000`.

## Editing the numbers

Each case study is one `<section class="case">`, in the order it appears on the
page. Inside it:

- `.scale-strip` — the four context figures under the client name
- `.case-grid` — problem / what we built / the outcome
- `.systems` — the numbered list of what shipped
- `.metrics` — the four headline numbers; the last one is highlighted
- `.case-note` — the caveat paragraph underneath

## Two conventions worth keeping

**`.est`** puts a dashed underline under any figure that is modelled or
projected rather than measured. Wrap every soft number in it. Two of the three
clients have figures that are estimates, and the page says so rather than
letting them read as production data.

**`.ph`** highlights a placeholder in pale orange so unfinished content is
impossible to miss on the rendered page. There are none left — if you add one
while drafting, the highlight is your reminder to remove it before deploying.
