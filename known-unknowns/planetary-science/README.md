# 🪐 Planets and moons

Solar-system and exoplanet problems with checkable wins: new moons and minor bodies as vetted candidates, surface benchmarks, orbit and shape records, exoplanet challenges with released truth.

**11 open problems**, easiest first. Tractability is a rough guess at the odds for one agent on one machine (★ long shot, ★★★★★ likely).

| Odds | Problem | Kind | Compute |
|---|---|---|---|
| ★★★☆☆ | [New lunar pit (steep-walled collapse feature) in public LROC NAC images, absent from the…](lunar-pit-candidate-not-in-lroc-atlas.md) | harvest | laptop-hours (LROC NAC EDR/CDR frames are 100-500 MB each; searches restricted to mare, impact-melt and highland target areas) |
| ★★★☆☆ | [SPOCK orbital-stability benchmark (Thadhani et al. 2025 cleaned data): beat SPOCK 2.0's h…](spock-stability-auc-cleaned-dataset.md) | standard | laptop-days (labels and initial conditions are a 33 MB Zenodo zip; short REBOUND integrations of ~1.3e5 systems take CPU-hours to a day; the 10^9-orbit labels are supplied) |
| ★★☆☆☆ | [2018 WFIRST/Roman Microlensing Data Challenge: one automated pipeline that recovers more…](roman-microlensing-data-challenge-2018-planet-recovery.md) | standard | laptop-days (293 two-band light curves, about 100 MB; binary-lens fits with public codes such as MulensModel, pyLIMA or VBMicrolensing take minutes to hours per event) |
| ★★☆☆☆ | [Moonstone lunar benchmark: beat MG-MAE on crater segmentation, mare segmentation or geolo…](moonstone-lunar-benchmark-beat-mg-mae.md) | standard | laptop-days (the repository's downstream scripts read patch pixels from pretraining/mmap, about 123 GB, and split metadata from benchmark/lunar_patches_v4.h5, about 75 GB: about 200 GB of downloads; one GPU recommended) |
| ★★☆☆☆ | [New dark comet candidate: a near-Earth asteroid with a non-gravitational acceleration tha…](dark-comet-candidate-nongrav-no-coma.md) | standard | laptop-hours (MPC astrometry is kilobytes to megabytes per object; an orbit fit with non-gravitational terms runs in minutes; archival image cutouts are megabytes) |
| ★★☆☆☆ | [New satellite of a TNO, Centaur, Jupiter Trojan or asteroid resolved in public archival H…](small-body-satellite-archival-not-in-johnston.md) | standard | laptop-hours (HST WFC3/ACS cutouts are MB each; PSF fitting of a few thousand visits overnight) |
| ★★☆☆☆ | [Significant Yarkovsky drift for a near-Earth asteroid that neither the JPL SBDB nor ESA N…](nea-yarkovsky-detection-not-in-sbdb-neocc.md) | harvest | laptop-hours (MPC astrometry per object is KB-MB; a full N-body least-squares fit with ephemerides DE440 and SB441-N16 takes minutes) |
| ★★☆☆☆ | [ExoMiner++ TESS 2-minute TCE vetting benchmark: beat the published 10-fold cross-validate…](exominerpp-tess-2min-cv-pr-auc.md) | standard | laptop-days (the released TFRecord inputs are 19 GB; a CNN trains in hours per fold on CPU or an Apple GPU, ten folds; or rebuild inputs from MAST SPOC DV products) |
| ★★☆☆☆ | [New irregular (or small inner) satellite of Jupiter, Saturn, Uranus or Neptune in public…](giant-planet-satellite-archival-shift-and-stack.md) | standard | laptop-days (tens of GB of archival CCD frames per planet field per night; shift-and-stack over a grid of rates) |
| ★★☆☆☆ | [Physical model of a tumbling (non-principal-axis) asteroid from public lightcurves, beyon…](asteroid-tumbler-npa-model-not-in-damit.md) | standard | laptop-hours (ALCDEF lightcurves are KB-MB per object; NPA inversion over a period grid takes hours per object) |
| ★★☆☆☆ | [A new YORP detection: significant change in an asteroid's rotation rate measured from dec…](asteroid-yorp-detection-beyond-twelve.md) | standard | laptop-hours (lightcurves KB-MB per object; convex inversion with a linear frequency change over a period grid takes hours) |

← [All categories](../README.md)
