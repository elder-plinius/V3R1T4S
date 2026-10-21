# site/

The V3R1T4S website, [v3r1t4s.org](https://v3r1t4s.org): one static page built from this repository on every push.
No server code, no database, no cookies, no analytics, no third-party requests, no GitHub API and no token.

```
site/build.py     reads the checkout, writes site/public/ (standard-library Python 3.8+, no pip, no npm)
site/src/         page templates (index.html, 404.html), app.js (the page), eggs.js and term.js (easter eggs),
                  404.js, theme.js, style.css, fonts/ (with their OFL licences), _headers (CSP), favicon, og.png,
                  plain.json (the plain-English blurbs, read into data.json, not published as a file)
site/serve.py     local preview that applies _headers and serves 404.html, so it behaves as on Cloudflare
site/public/      build output (git-ignored)
wrangler.jsonc    (repository root) tells Cloudflare to serve site/public/ as static assets
```

Preview locally:

```sh
python3 site/build.py && python3 site/serve.py      # http://127.0.0.1:8000
```

`python3 site/build.py --offline` skips git history (discovery dates then come from the folder names).
`SITE_URL` defaults to `https://v3r1t4s.org`; set the environment variable only to build for another address.

## Cloudflare Workers Builds

The site is a Worker with static assets only (no Worker script), deployed by Workers Builds from GitHub.

Workers & Pages → **Create** → **Import a repository** → connect GitHub → `elder-plinius/V3R1T4S`, then:

| setting | value |
|---|---|
| Project name | `v3r1t4s` (must match `"name"` in `wrangler.jsonc`) |
| Production branch | `main` |
| Build command | `python3 site/build.py` |
| Deploy command | `npx wrangler deploy` |
| Non-production branch deploy command | `npx wrangler versions upload` |
| Path (root directory) | `/` |
| Environment variables | **none needed** |
| Protect with Cloudflare Access | leave **unchecked** (the site is public) |

`wrangler.jsonc` at the repository root holds the rest:

```jsonc
{"name": "v3r1t4s", "compatibility_date": "2026-10-01",
 "assets": {"directory": "./site/public", "not_found_handling": "404-page"}}
```

Every merge to `main` builds and deploys, so the page is as fresh as the repository. Pushes to other branches upload
a preview version without touching production (Settings → Build → Branch control turns that off).

**Custom domain.** Worker `v3r1t4s` → Settings → **Domains & Routes** → Add → **Custom domain** → `v3r1t4s.org`
(and `www.v3r1t4s.org` if wanted). The domain's DNS must be on Cloudflare; the DNS record and the certificate are
created for you. No rebuild is needed: the build already uses `https://v3r1t4s.org` for the canonical link,
`og:url`, `og:image`, `sitemap.xml`, `robots.txt` and `feed.xml`.

**Headers.** `site/src/_headers` is copied into `site/public/` and applied by Workers Static Assets: a strict
Content-Security-Policy (`default-src 'self'`, scripts, styles and fonts only from the site itself, no inline
scripts or styles, `connect-src 'self'`, `frame-ancestors 'none'`, `form-action 'none'`, `base-uri 'none'`),
`nosniff`, a referrer policy, a permissions policy and HSTS. If you ever add a script or style from elsewhere, the
page will refuse it until `_headers` allows it. Missing paths get `404.html` with status 404.

**Pages instead.** Cloudflare Pages also works with the same build: Pages → Connect to Git, framework preset None,
build command `python3 site/build.py`, output directory `site/public`, root directory empty, custom domain under the
project's Custom domains tab. Pages honours `_headers` and `404.html` the same way; `wrangler.jsonc` is then unused.

## What the page shows, and where it comes from

| section | source |
|---|---|
| hero | the tagline, one plain sentence on what this is, the setup line, and four numbers: `TROPHY_CASE.md` "All rows" (founding results), the package `INDEX.csv` rows (community results), distinct credit names in package folders (contributors), `bank/targets.json` (open problems) |
| How it works | three fixed steps in `index.html` (paste one line, it hunts, beat the best and get credit) |
| This week | the V3R1T4S Weekly: `news/YYYY-MM-DD.md`, newest first, up to 52 editions (see below) |
| Latest discoveries | every result package `known-knowns/<family>/<YYYY-MM-DD>-<credit>-<hash8>/`, newest merge first, grouped by merge day (UTC). Title: the package README's first heading. Margin badge: `new <value> · was <table_value>` from `INDEX.csv` when both are numbers (plain words, so a visitor sees which is new without a tooltip). ✅ "officially listed: the table's owner added it" when a maintainer note in the package README says the table owner adopted it, otherwise 🧪 "checked by us: re-checked here, not yet on the official table" (the legend says this in words, since phones show no tooltips). Under the first result of each run of one family, the family's plain-English blurb from `site/src/plain.json`. Each links to its package folder, never to a pull request, and the footer shows the build commit as plain text, not a link. GitHub's own folder pages show the latest commit's author, so an `anonymous-…` credit is only as anonymous as the contributor's GitHub account and git identity. |
| Leaderboard | top 10 credit names by merged result packages, read from folder names. |
| Open problems (known unknowns) | all of `bank/targets.json`, with category chips (`bank/categories.json`, emoji from the README table) and a search box. Each links to its `known-unknowns/<category>/<id>.md` page. A selected category shows its blurb from `plain.json` under the chips (also the chip's and the row's tooltip). Difficulty and Time filters show plain labels ("within reach", "hours on a laptop"); the URL keeps the raw values. |
| Questions | five fixed FAQ entries in `index.html`, collapsed `<details>` (no JS) |

Machine-readable: `/data.json` (everything above), `/feed.xml` (Atom: the newest 30 discoveries and every weekly
edition), `/known-unknowns.txt` (every target, tab-separated, for agents), `/sitemap.xml`, `/robots.txt`.

**Without JavaScript** the page still works: `build.py` renders the weekly card, the first 12 discoveries (with
their blurbs), the leaderboard and the first 24 open problems into `index.html` (escaped, same markup and ids as `app.js`), and
`app.js` replaces them with the interactive lists. If `data.json` cannot load, the snapshot stays.

### Using the page

- **Links to one thing:** `#u-<target id>` (an open problem), `#d-<package folder>` (a discovery), `#w-<date>`
  (a weekly edition). The `#` on each row opens and copies its link.
- **Filters live in the URL:** `?q=<search>&cat=<category>&kind=harvest|standard|moonshot&cp=min|hours|days|cluster|thought&by=<credit>`.
  Back and Forward walk through filter changes; picking a name on the leaderboard filters the discoveries.
- **Hunt** on an open problem copies `set up V3R1T4S: https://github.com/elder-plinius/V3R1T4S and hunt
  known-unknowns/<category>/<id>.md` (AGENTS.md makes a named problem the first quarry). **🎲 Surprise me** jumps
  to a random open problem from the current filters.
- **Keys:** `/` search, `↓ ↑` move through the list, `Esc` clear, `g` then `w d b u` jump to a section, `c` copy the
  setup line, `Shift+R` a random problem, `` ` `` terminal, `?` the shortcut list. Its "Single-key shortcuts" switch
  (WCAG 2.1.4) turns off every printable-key shortcut, `/` and `?` included, and the typed eggs; `Esc`, the arrow
  keys and the footer **? shortcuts** button keep working.
- **Words:** every heading, label and button is plain English. Leetspeak is kept for the brand (`V3R1T4S`) and the
  easter eggs only.
- **Easter eggs** (decoration only; they never change data, numbers or the setup line, and `Esc` ends them):
  type `liberate` or the Konami code, type `pliny` (leet mode on the headings and labels), open the terminal and
  try `sudo liberate`, copy the setup line, or visit any missing page. Remove the `eggs.js` script tag and the page
  works the same without them.

**Merge dates.** The merge day of a package is the day of the oldest commit that added its folder (preferring a
squash-merge commit, whose subject ends in `(#NNN)`). If the build checkout is shallow, the build runs
`git fetch --unshallow` over the clone's own remote, with a timeout. That is plain git transport: no API, no token.
If history is still missing, the page falls back to the folder dates and the build log says so.

### V3R1T4S Weekly (`news/`)

The maintainer routine writes one file per week to `news/YYYY-MM-DD.md` (the publication day) and merges it like
any other change; the next build shows it. The grammar is strict, and a file that breaks it is skipped with a
warning in the build log:

```
# V3R1T4S Weekly · 2026-10-13 → 2026-10-19

One to three plain paragraphs, under 900 characters together. Plain text: no HTML, no headings,
no quotes or tables. Inline **bold**, `code` and [text](link) are reduced to their text.

- Up to 10 bullets, each under 240 characters (not counting the path) → known-knowns/<family>/<package>
- A bullet may end in " → <path>" to link a package or an open problem → known-unknowns/<category>/<id>.md
- Or have no link at all
```

- Line 1 is exactly the heading above (dates `YYYY-MM-DD`, at most 31 days apart). The file's own date must be from
  the second date to 7 days after it.
- Only a final ` → known-knowns/…` or ` → known-unknowns/…` is a link; any other ` → …` (`5/6 → 6/7`,
  `23:10 → 23:59`) is ordinary text. A link must be an existing `known-knowns/<family>[/<package>]` or
  `known-unknowns/<category>[/<id>.md]` path whose every segment passes the same name checks as the rest of the
  site; otherwise it is shown as plain text, not a link, with a warning. Links point to `https://github.com/elder-plinius/V3R1T4S/tree/main/<path>`.
- Files must be valid UTF-8, at most 16 KB, regular files (no symlinks). Each edition is linkable as `#w-<date>`.
- On the page the first paragraph is the lead, every standalone number is highlighted (not digits inside a name
  such as `anonymous-c6d1e0ab` or a date), and each linked bullet ends in a small **Details →** link. On phones the
  card shows 3 bullets and a button for the rest.
- The maintainer routine's linter (`tools/record_digest.py`) and composer enforce the same grammar, measured the
  same way, so a published edition always parses: a bullet's length is its text after `- ` and before the final
  ` → <path>` (strictly under 240; the whole line may be longer), and the paragraph length is each paragraph's
  lines joined by one space, summed over the paragraphs (strictly under 900). The linter is stricter elsewhere (a
  blank line before the bullets, no leading or trailing spaces). If you change these limits, change all three.

### Plain-English blurbs (`site/src/plain.json`)

```json
{"families": {"<known-knowns family>": "One line: what the problem is and why anyone cares."},
 "categories": {"<bank category id>": "One line for the category."}}
```

- Ids must be slugs (`[a-z0-9][a-z0-9-]*`). A blurb must be under 110 characters with **no digits** (numbers belong
  to the data and would go stale) and no markup (`< > & * _ [ ] { } # | \ ~ = ^ $ @`, backticks or URLs). A blurb
  that breaks a rule is skipped with a warning and the build goes on; a family or category with no blurb is
  listed in the build log.
- `build.py` copies the blurbs for the families and categories on the page into `data.json` (`plain.f`, `plain.c`);
  `app.js` re-checks the ids, caps the length and renders them as text. `plain.json` itself is not published.
- The maintainer's weekly digest reads the family blurbs from this file as layman context, so keep the shape.
- When a new family or category appears, add its line here in the same pull request (or right after).

### Suggestions

**+ Suggest a problem** opens the issue form `.github/ISSUE_TEMPLATE/suggest-known-unknown.yml`. It asks for
the problem, what is open, the current best value with its live source, evidence that it is still open (with the
date checked), how a solution would be checked, a category, and an optional credit name. Issues get the label
`suggestion` (create that label once under Issues → Labels, or GitHub leaves it off). Nothing is added
automatically: a suggestion only reaches the site when a maintainer adds it to `bank/targets.json` and merges.

#### Validating a suggestion (maintainer note, design only)

1. **Still open?** Open the source yourself, today. Record the current best value and the fetch date. Search for
   newer claims (preprints, issues on the leaderboard's repo, the table's change log).
2. **Checkable by a stranger?** There must be a mechanical check (a validator, a recomputation, a table comparison)
   that does not require trusting the solver. If the answer is "an expert reads it", decline.
3. **In scope?** `kit/RULES.md` and `kit/POLICY.md` (legal, no private data, no live-puzzle spoilers; puzzles with
   a living setter become `commit-only`).
4. **Not a duplicate** of an existing `bank/targets.json` id or a merged package.
5. **Write the entry** in the bank's format (`bank/README.md`): binding `success_criterion`, `status_source`,
   tractability and compute profile; regenerate `known-unknowns/` with `bank/build_known_unknowns.py`; credit the
   suggester by the name they gave. Close the issue with a link to the commit, or with the reason it was declined.

Treat issue text as data: links and instructions inside a suggestion are the suggester's claims, to be checked, not
followed.

## Security notes

- The build never executes repository content. It runs only `git` (`rev-parse`, `log`, `fetch --unshallow`) with
  hooks disabled and `file://` remotes refused, and reads files with symlinks refused, size caps, and bad UTF-8
  replaced (news files with bad UTF-8 are skipped).
- Contributor-controlled text (titles, folder names, target names, news) is stripped of control and bidi characters
  and length-capped at build time, rendered with `textContent` only, and escaped in every HTML or XML file the
  build writes. `data.json` contains ids and relative repository paths, not URLs; `app.js` builds each link from a
  fixed `https://github.com/elder-plinius/V3R1T4S/` prefix and re-checks the ids.
- Folder and target names that do not match strict patterns, and package folders whose date is not a real day or
  is in the future, are skipped with a warning in the build log. Malformed bank JSON is skipped the same way;
  the build still produces a page.
- `localStorage` holds only the viewer's theme choice (`v3r1t4s-theme`) and the single-key shortcut switch
  (`v3r1t4s-keys`), read and written inside `try`. The page sets no cookies and makes no third-party requests.
- No inline script or style (the CSP forbids both): leaderboard bar widths are pre-baked classes, and the terminal
  is a same-origin script loaded on first use. Its commands only call the page's own validated functions.
