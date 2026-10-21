# New periodic variable stars / eclipsing binaries absent from VSX, confirmed in two independent surveys

🔭 **Sky archives** · harvest (many cells or partial wins within reach) · tractability ★★★★☆ · compute: laptop-hours (ZTF light curves are fetched per cone query, a few hundred KB each; TESScut 5x5-pixel cutouts are ~1 MB per sector; the CDS vsx.dat dump is 2.2 GB; Gaia and Chen+2020 catalogs are queried, not downloaded in full) · open as of 2026-10-20

## The problem

Discover periodic variable stars (eclipsing binaries, RR Lyrae, delta Scuti, rotational, etc.) that are absent from the AAVSO International Variable Star Index (VSX, > 2 million entries; live API at vsx.aavso.org and full dump at CDS B/vsx updated 2026-10-18) AND absent from the major machine catalogs that VSX has not fully ingested: Gaia DR3 vari_summary (11.75 million sources, incl. vari_eclipsing_binary 2.18 million), ASAS-SN variables, ZTF periodic variables Chen+2020 (VizieR J/ApJS/249/18), ATLAS variables Heinze+2018 (J/AJ/156/241), Catalina CRTS Drake+2014/2017 (J/ApJS/213/9, J/MNRAS/469/3688), WISE periodic variables Chen+2018 (J/ApJS/237/28), OGLE OCVS where in the OGLE footprint, TESS-EBs HLSP, and SIMBAD; with the period independently recovered (within 0.1% or an exact 2x alias) in two independent public data sets, e.g. ZTF DR23 light curves (IRSA) and TESS FFI light curves, or ZTF and Gaia DR3 epoch photometry. The AAVSO forum states that many millions of known-variable candidates await VSX ingestion, so the machine-catalog absence condition is what makes a find non-trivial.

## What counts as a win

A batch of >= 10 objects, each with a saved bundle {Gaia DR3 source_id, RA/Dec, ZTF object ids and light-curve CSVs (IRSA URLs), second-survey light curve (TESS FFI cutout URL or Gaia epoch photometry), periodograms, period and uncertainty from each survey, folded curves, amplitude, classification, and every catalog response used with timestamps} such that for every object: (1) no VSX entry within 10 arcsec via the live api.list query at https://vsx.aavso.org/index.php?view=api.list (re-fetched live immediately before claiming; an error response counts as 'unknown', never as 'absent') and none in the CDS B/vsx dump; (2) no Gaia DR3 vari_summary source within 2 arcsec with any classification (Gaia TAP); (3) no ASAS-SN variable, no Chen+2020 ZTF periodic or suspected variable, no ATLAS (J/AJ/156/241), CRTS (J/ApJS/213/9, J/MNRAS/469/3688) or WISE (J/ApJS/237/28) variable, no OGLE OCVS entry (if inside the OGLE footprint), and no TESS-EBs entry within 10 arcsec; a SIMBAD TAP cone of 3 arcsec returns no object with a variable-star otype (V*, EB*, RR*, dS*, Ro*, Pu*, Er*, LP*, Mi* or their candidate forms); if the TESS Ten Thousand EB catalog (arXiv:2506.05631) machine-readable table is obtainable it is also checked and saved, and if it is not obtainable the TESS leg may not be used as a survey for EB-type candidates; (4) periods from the two surveys agree within 0.1% (or exactly 2x), each with bootstrap FAP < 1e-4, and the period is not within 1% of a sidereal-day alias (n/k day, k <= 4) unless the second survey is space-based; (5) amplitude > 5x the per-survey median scatter at that magnitude; (6) the TESS detection (if used) is not a blend: the signal is absent in neighbours within 1 arcmin that are brighter, or a pixel-level centroid shows it on target; (7) null test: the identical pipeline applied to 50 VSX 'constant'/non-variable comparison stars of similar magnitude yields zero objects passing (4)-(5), saved with the batch. Claim is 'new periodic variable, not in VSX or the listed catalogs'.

## Partial wins

- **vsx-reproduce-known:** Pipeline recovers, blind, the VSX period for at least 50 randomly drawn VSX EW/EA/RRAB/DSCT stars with ZTF coverage (within 0.1% or 2x alias) and reports its own false-alarm rate on 50 VSX 'constant' / non-variable comparison stars; saved as a table (calibration gate).
- **vsx-new-variables-single-survey:** A batch of >= 20 objects satisfying (1)-(3) and (5) with a ZTF-only period at FAP < 1e-6 but no second-survey confirmation; logged as 'single-survey candidates', not claimed.
- **vsx-period-corrections:** A table of >= 20 VSX entries imported from Gaia DR3 whose VSX period is a wrong alias (the AAVSO forum notes many are), with the correct period demonstrated in ZTF + a second survey; checkable by re-folding.

## How a win is checked

Skeptic re-runs the VSX api.list cone query, the Gaia TAP cone query, the SIMBAD cone, the VizieR matches (ASAS-SN/Chen+2020/ATLAS/CRTS/WISE/TESS-EBs, saved catalogs), re-downloads the ZTF light curve CSV from the IRSA URL in the bundle and the TESS cutout via TESScut, and re-computes the Lomb-Scargle/BLS period with the saved script for each of the >= 10 objects plus the 50 null-test stars. Under one hour for the batch.

## Is it still open?

Check the status page before you start and again before you claim anything; tables move fast.

- <https://vsx.aavso.org/index.php?view=api.list&ra=291.0&dec=42.5&radius=0.1&format=json>

## Sources

- <https://vsx.aavso.org/index.php?view=api.list&ra=291.0&dec=42.5&radius=0.1&format=json>
- <https://vsx.aavso.org/index.php?view=api.object&ident=RR+Lyr&format=json>
- <https://cdsarc.cds.unistra.fr/ftp/B/vsx/>
- <https://gea.esac.esa.int/tap-server/tap/sync?REQUEST=doQuery&LANG=ADQL&FORMAT=csv&QUERY=select+count(*)+from+gaiadr3.vari_summary>
- <https://irsa.ipac.caltech.edu/cgi-bin/ZTF/nph_light_curves?POS=CIRCLE+255.9302+11.8654+0.0028&FORMAT=csv&BAD_CATFLAGS_MASK=32768>
- <https://irsa.ipac.caltech.edu/cgi-bin/Gator/nph-query?catalog=ztf_objects_dr23&spatial=cone&objstr=255.93+11.86&radius=10&outfmt=1>
- <https://mast.stsci.edu/tesscut/api/v0.1/sector?ra=84.291188&dec=-80.469119>
- <https://asas-sn.osu.edu/variables.csv?per_page=10>
- <https://vizier.cds.unistra.fr/viz-bin/asu-tsv?-source=J/ApJS/249/18&-out.max=2>
- <https://archive.stsci.edu/hlsps/tess-ebs/hlsp_tess-ebs_tess_lcf-ffi_s0001-s0026_tess_v1.0_cat.csv>
- <https://arxiv.org/abs/2506.05631>
- <https://ztf.snad.space/>
- <https://vizier.cds.unistra.fr/viz-bin/asu-tsv?-source=J/AJ/156/241&-out.max=2>
- <https://vizier.cds.unistra.fr/viz-bin/asu-tsv?-source=J/ApJS/213/9&-out.max=2>
- <https://vizier.cds.unistra.fr/viz-bin/asu-tsv?-source=J/MNRAS/469/3688&-out.max=2>
- <https://vizier.cds.unistra.fr/viz-bin/asu-tsv?-source=J/ApJS/237/28&-out.max=2>
- <https://ogledb.astrouw.edu.pl/~ogle/OCVS/>
- <https://gea.esac.esa.int/tap-server/tap/sync?REQUEST=doQuery&LANG=ADQL&FORMAT=csv&QUERY=select+count(*)+from+gaiadr3.vari_eclipsing_binary>
- <https://simbad.cds.unistra.fr/simbad/sim-tap/sync?REQUEST=doQuery&LANG=ADQL&FORMAT=csv&QUERY=select+main_id,otype,ra,dec+from+basic+where+contains(point('ICRS',ra,dec),circle('ICRS',289.0758,51.7572,0.001))=1>

## Ideas to start from

Starting points, not instructions. The best wins came from angles nobody listed.

- Sky regions where Gaia DR3 variability is incomplete (crowded low-latitude fields, |b| < 10 deg, and stars with few Gaia transits) but ZTF has > 200 epochs: run a Lomb-Scargle + BLS search on ZTF objects with high chi2 (ztf_objects_dr23 'chi'/'nobs' columns via Gator).
- Faint end (ZTF r 18-20.5) below ASAS-SN's limit and below the Chen+2020 threshold, where VSX is emptiest.
- Short-period (P < 0.2 d) EW/delta-Scuti systems whose Gaia DR3 period is an alias: cross-check with TESS 200-s FFI cutouts, which break ground-based aliases.
- Use the TESS Ten Thousand '~900k unvetted targets with score > 0.9 and no known EB within 21 arcsec' list (arXiv:2506.05631) as a pre-filtered input and resolve each with ZTF (which has 21x finer pixels).
- Automate a VSX-absence checker that queries api.list in batches with a 10-arcsec radius and caches results, to keep the AAVSO server load low (radius = 5 deg queries time out).

## Traps

False wins others have fallen for. A claim that walks into one of these will not survive the skeptics.

- Absence from VSX alone is trivial: millions of Gaia DR3 / ZTF / ASAS-SN / ATLAS / CRTS / WISE / OGLE variables are not yet in VSX. A find must be absent from ALL listed machine catalogs and SIMBAD, otherwise it is a catalog cross-match exercise, not a discovery.
- TESS 21-arcsec pixels: a periodic signal in a TESS cutout usually belongs to a brighter neighbour; without ZTF/Gaia confirmation on the same source it is a blend.
- ZTF alias periods (1 d, 0.5 d, sidereal-day harmonics) and the ZTF 'catflags' bad-data flags produce fake periodicities; mask catflags and reject periods within 1% of n/k day aliases unless confirmed by TESS.
- VSX name matching is not enough: match by position (10 arcsec) because VSX entries carry survey names (Gaia DR3, ZTF, ASASSN-V, KIC) not Gaia source_ids.
- The api.list endpoint returns a PHP fatal error for large radii (5 deg timed out); the checker must use small cones and treat an error response as 'unknown', never as 'absent'.
- The TESS Ten Thousand catalog (arXiv:2506.05631) had no VizieR/MAST machine-readable copy found on 2026-10-08; until one is saved in the bundle, TESS-based EB candidates cannot be declared absent from it.

## Point your agent at it

```
set up V3R1T4S: https://github.com/elder-plinius/V3R1T4S and hunt known-unknowns/sky-archives/new-periodic-variables-not-in-vsx.md
```

Already set up? Say `run V3R1T4S on new-periodic-variables-not-in-vsx`. Your agent follows [AGENTS.md](../../AGENTS.md): it re-checks the status, freezes its success rule, attacks, and only a three-skeptic panel can confirm a win.

---

_Generated from [`bank/targets.json`](../../bank/targets.json) (id `new-periodic-variables-not-in-vsx`). Found it solved, stale or wrong? Open an issue or a pull request against that file._
