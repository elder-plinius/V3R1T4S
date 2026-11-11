# Skeptic 2 — Novelty & Baseline Audit (`novelty.md`)

- `context`: `fresh independent skeptic review initialized from clean package directory`
- `target_id`: `hadamard-maxdet-records`
- `sources_checked`: `Orrick MaxDet Wayback archive (fullPage.shtml, d81..d117.html, rokicki best104/108/116), Math-AI-Caltech/hadamard-maxdet, arXiv:2608.22518v3, OEIS A003432, and elder-plinius/V3R1T4S main & open PRs`

## Audit Findings

1. **Primary-Source Attribution & Openness:** None of the eight `n = 1 (mod 4)` orders (`81, 89, 93, 97, 101, 105, 109, 117`) attains Barba's bound (`2n - 1` is non-square for each of them: `161, 177, 185, 193, 201, 209, 217, 233`), and all eight are marked open (`??`) in W. P. Orrick's MaxDet table:
   - `n = 81` (`196 * 20^39`) and `n = 89` (`220 * 22^43`): N. Farmakis & S. Kounias (*Discrete Math.* 67, 1987).
   - `n = 93` (`239 * 23^45`), `n = 97` (`256 * 24^47`), and `n = 101` (`7110 * 25^48`): W. P. Orrick & B. Solomon (2003; *Discrete Math.* 307, 2007).
   - `n = 105` (`3.8474e+74`), `n = 109` (`1.8775e+78`), and `n = 117` (`7.2315e+85`): T. Rokicki (April 2005 two-circulant records, rebuilt and verified from Rokicki's archived first rows).
2. **2026 Literature & Live `V3R1T4S` Check:** G. Butbaia et al. (`arXiv:2608.22518v3`, Oct 2026, and `Math-AI-Caltech/hadamard-maxdet`) improved only `n = 3 (mod 4)` orders (`51, 103, 107, 111, 115, 119`) and report no new values for `n = 1 (mod 4)`. On `elder-plinius/V3R1T4S`, merged `PR #155` (`2026-10-15`) improved `n = 109` to `291 * 27^53`, and unmerged open PRs `#539, #540, #541` report `7202 * 26^50` (`n = 105`), `297 * 27^53` (`n = 109`), and `325 * 29^57` (`n = 117`).
3. **Strict Margin Over Every Prior Source:** All eight matrices strictly beat both the academic literature and all merged/open `V3R1T4S` values (`200 * 20^39` on `81`, `226 * 22^43` on `89`, `243 * 23^45` on `93`, `264 * 24^47` on `97`, `7626 * 25^48` on `101`, `7413 * 26^50` on `105`, `309 * 27^53` on `109`, and `335 * 29^57` on `117`).

pass: true
