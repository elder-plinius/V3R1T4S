# Research charter v2 (2026-10-14)

## Thesis

Use precise geometry, physical feasibility, and numerical models as a common thread across packing, orbit reconstruction, and periodic-signal search. Prioritize targets with independent checkers, manageable inputs, and useful partial-win paths; give the highest weight to the geometry target with the clearest audit route, while keeping one orbital-recovery quarry as the wild choice.

## Quarries

- **packomania-hyperspheres-hsp4-hsp6** — Which listed 4D, 5D, or 6D row admits a feasible, non-isometric packing that beats the live radius by at least 1e-10 and is outside every live queue range? Shape: explicit centers, a 50-digit feasibility checker, and a comparison with the posted arrangement. Defined by bank target `packomania-hyperspheres-hsp4-hsp6` and Packomania Section 4 (`https://packomania.com/hsp4/hsp4.html`). Recheck the dimension-specific radius table, history, and pending queue before work and any claim. The bank also defines a data-integrity audit and extension-row partial win. Why this quarry: a small geometric checker can test every recorded configuration independently. Weight 5; wild: no.
- **new-periodic-variables-not-in-vsx** — Can a batch of at least 10 periodic variables be recovered in two independent surveys and shown absent from VSX and the listed machine catalogs? Shape: source light curves, frozen periodograms, catalog queries, and matched controls. Defined by bank target `new-periodic-variables-not-in-vsx`, AAVSO VSX (`https://vsx.aavso.org/`), ZTF/IRSA, and the named survey catalogs. Recheck catalog availability and entries before work and any claim; treat error responses as unknown. Why this quarry: periodicity and cross-survey agreement have numerical checks, and the target has a reproducible calibration partial win. Weight 3; wild: no.
- **asteroid-precovery-arc-extension** — Can public survey images establish at least two detections of a known minor planet more than 60 days before its first recorded observation, with consistent motion, a refit, and the required catalog exclusions? Shape: saved FITS cutouts, centroids, propagated covariance, orbit residuals, and MPC/JPL records. Defined by bank target `asteroid-precovery-arc-extension`, JPL SBDB (`https://ssd-api.jpl.nasa.gov/sbdb.api`), MPC observations, and the named ZTF, Pan-STARRS, or DECam archive. Recheck the full observation record and archive frames before work and any claim. Why this quarry: orbit propagation turns image matching into a falsifiable dynamical prediction. Weight 4; wild: yes.

## Lenses

- **Audit the contact geometry** — Start with the posted 4D/5D/6D centers, independently recompute every feasible radius, then search construction families and polish their best candidates. First move: validate the parser on a small row and reproduce its published radius. The line is dead if the baseline cannot be reproduced or the candidate fails the strict feasibility margin.
- **Recover a signal across surveys** — Begin with known periodic variables as a blind calibration set, then search modest fields for periods that agree across two independent surveys. Freeze the period statistic and controls first. The line is dead if known periods are missed, control stars pass, or catalog coverage is incomplete.
- **Propagate backward, verify forward** — Select recent objects whose prior orbit uncertainty intersects archival coverage, predict motion and brightness, then test detections in independent frames and refit. The line is dead if the MPC record already contains the epoch, a static source explains the pixels, or the fit fails the frozen residual limits.
- **Try to falsify the premise** — Re-fetch the primary tables, queues, and catalogs; independently recompute a baseline; search for stale values, prior candidates, alias periods, or equivalent configurations before optimizing. The line is dead only when the status and checker both support continuing.

## Scout voice

Read the primary definition first, copy its success rule literally, and establish live status with one honest request. Record gaps in source coverage as unknown; do not infer absence from a failed query. Keep data volume bounded and preserve the exact inputs used.

## Attacker voice

Treat feasibility as a hard constraint and objective values as claims to reproduce. Prefer a short model with a rerunnable checker to a complicated search whose output cannot be independently verified. Keep surprising leads, but scale effort only after the baseline works.

## Heuristics

1. Reproduce a published baseline before searching for an improvement.
2. Freeze the criterion, statistic, threshold, and null design before scoring results.
3. For searches, run the full pipeline on at least 400 controls when the protocol requires them; report the best control beside the real result.
4. For astronomical detections, require independent epochs or surveys and check the full observation history, not only a summary date.
5. For geometric records, compute feasibility from the saved coordinates at the precision required by the criterion.
6. A source-query error means unknown, never absent.
7. Prefer a bounded audit or enumerated partial win when a full record search is unlikely to fit the budget.

## Kill criteria

1. The live primary source shows the target is solved, queued, or otherwise no longer novel.
2. A baseline cannot be reproduced with a small independent checker.
3. The candidate fails any feasibility, residual, control, or catalog-absence condition in the bank criterion.
4. Required source data are blocked, unavailable, or cannot be used under their published terms.
5. A run cannot produce useful, bounded work within the selected effort; preserve a precise next step instead of overstating progress.

## Self-critique

The chosen direction has only a small amount of user-provided context behind it. The packing and orbit targets have explicit checkers, but a new record or precovery may still be rare. The periodic-variable task has many catalog-exclusion requirements and a batch threshold, so calibration may be the only realistic short-run result. Bank tractability ratings and source snapshots can be stale; every run must check them again.

## Method cards used

Random draw: `construct-space`, `solver`, `smaller-first`.

## Changelog

Replaced the initial ancient-text quarry with geometry, periodic-signal, and orbit-recovery targets after the human requested a more relevant charter and stronger bias toward checkable progress. Kept the surprise-me approach and the randomly drawn method cards; prioritized the geometric target with a concrete data-audit partial win.
