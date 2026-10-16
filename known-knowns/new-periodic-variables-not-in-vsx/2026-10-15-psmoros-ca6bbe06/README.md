# vsx-reproduce-known: a calibration gate for a ZTF period pipeline against VSX (77/80 recovered, 0/400 false alarms)

## What

The hash-pinned pipeline in code/, which never reads a catalog period, recovered the B/vsx (2026-10-05) period within 0.1% or at a 2x alias for 77 of 80 seeded-random VSX EW/EA/RRAB/DSCT stars with >= 50 ZTF epochs within 1.5 arcsec (70 of those 77 VSX periods being identical to Chen+2020 ZTF periods per results/variables.csv, so this is mainly a ZTF re-derivation, not independent-survey confirmation), and the identical pipeline on 67 VSX CST stars and 333 Gaia DR3 non-variables reports a false-alarm rate of 0/67 (CST) and 0/400 (all) at the pre-frozen threshold S > 54.0, saved per star in results/vsx_reproduce_known_table.csv and results/controls_table.csv.

This is the bank partial win `vsx-reproduce-known` of the target `new-periodic-variables-not-in-vsx`, a
calibration gate. It finds no new variable star and claims none.

## Check it yourself

Python 3 (standard library only) and a POSIX shell, from this folder:

```sh
sh verify-it-yourself/run_checks.sh
```

Expected last line: `PASS` (a few seconds). It checks every file against SHA256SUMS, recounts the recoveries with
its own agree() from the tables, checks the draws against the saved B/vsx pool and seeded order, and recounts the
false alarms of the 400 controls (67 VSX CST) at the pre-frozen threshold S > 54.0. With the public light curves
fetched (verify-it-yourself/fetch_lightcurves.py, about 2 minutes) it also folds each of the 77 recovered stars at
its recovered period against 100 random periods (phase dispersion). RUN_IT_YOURSELF.md re-runs the frozen pipeline
itself (numpy/scipy/astropy) on the light curves, whose exact URLs and sha256 are in how-we-built-it/data/lc_manifest.csv.

## Compared to

No record table applies: this is a calibration gate, not a record. The bank's status source,
https://vsx.aavso.org/index.php?view=api.list&ra=291.0&dec=42.5&radius=0.1&format=json, answered HTTP 200 at
2026-10-15T17:42:18Z (scout) and again at 2026-10-15T19:39:25Z (NOVELTY skeptic), page sha256
686920557fcf33a7bbdef0642253c51bbc25f80e01c809e8b5adeaf6ef325594; see the-record-we-beat/. The VSX periods
compared against are from CDS B/vsx version 2026-10-05. The NOVELTY skeptic found no earlier claim of this partial
win in TROPHY_CASE.md or the open pull requests of this repository (2026-10-15T19:39-19:44Z).

## Not claimed

- No new variable star, no period correction, nothing about the full success criterion of the target.
- Not an independent-survey confirmation: 70 of the 77 recovered VSX periods equal Chen et al. (2020) ZTF periods, so
  the gate mostly shows that this pipeline re-derives ZTF-based VSX periods from later ZTF photometry.
- The astrophysics is known: recovering known EW/EA/RRAB/DSCT periods from ZTF is established practice (Chen et al.
  2020 report about 99% period accuracy). "First" here means only the first claim of this bank partial win.
- The false-alarm rate is measured on these 400 controls only (one-sided 95% upper limits about 4.4% for the 67 CST
  stars and 0.75% for all 400); "randomly drawn" means a seeded 1/1000 OID slice of B/vsx plus a seeded permutation.
- The completeness of the saved Gaia control window against the live Gaia archive was not re-checked by the panel
  (Gaia TAP answered HTTP 429; PENDING TABLE CHECK); its internal properties were verified.
- The code in how-we-built-it/code is the hash-pinned code with one change: absolute workspace paths were replaced by a
  WORKDIR placeholder (privacy; "[workspace]" in documents); how-we-built-it/code_hashes.json lists both hashes.
- Reviewers were three fresh contexts (two Claude Opus 5.5, one Claude Fable 5.1), not humans.

## Credits

- ZTF: Bellm et al. 2019 (PASP 131, 018002); Masci et al. 2019 (PASP 131, 018003); https://www.ztf.caltech.edu.
  Light curves through the SNAD ZTF database API, Malanchev et al. 2023 (PASP 135, 024503), https://db.ztf.snad.space.
- VSX / AAVSO: Watson, Henden & Price 2006 (SASS 25, 47), https://vsx.aavso.org, through CDS VizieR B/vsx,
  https://cdsarc.cds.unistra.fr/viz-bin/cat/B/vsx (Ochsenbein, Bauer & Marcout 2000).
- Gaia DR3: Gaia Collaboration, Vallenari et al. 2023 (A&A 674, A1), https://gea.esac.esa.int/archive/.
- Chen et al. 2020 (ApJS 249, 18), ZTF periodic variables, VizieR J/ApJS/249/18 (provenance column).
- astropy (Astropy Collaboration 2013, 2018, 2022); Lomb-Scargle: VanderPlas 2018 (ApJS 236, 16); numpy, scipy, pandas.
- Submission credit: psmoros. Built and reviewed with the V3R1T4S protocol, https://github.com/elder-plinius/V3R1T4S
  (repo commit in prompt/repo.txt).
