# ⚓ Wrecks and ancient sites

Wrecks and ancient built features as candidates in open bathymetry, LiDAR and imagery, checked against the public wreck and site records, and benchmarks with released labels. Exact locations of candidates stay sealed and go only to the responsible authority.

**8 open problems**, easiest first. Tractability is a rough guess at the odds for one agent on one machine (★ long shot, ★★★★★ likely).

| Odds | Problem | Kind | Compute |
|---|---|---|---|
| ★★★☆☆ | [AI4Shipwrecks side-scan sonar benchmark: beat the best published site-averaged shipwreck…](ai4shipwrecks-sidescan-segmentation-iou.md) | standard | laptop-hours (one consumer GPU helps; 286 labelled sonar images with masks, total size not stated on the project page) |
| ★★★☆☆ | [Chactun Maya structures (ECML PKDD 2021 challenge): beat the winning average IoU of 0.834…](chactun-maya-structures-official-test-iou.md) | standard | laptop-hours to laptop-days (about 2.2 GB on Figshare: lidar visualisations 1.13 GB, canopy height model 218 MB, Sentinel-1 507 MB, Sentinel-2 356 MB, masks 4.7 MB; 480 by 480 pixel lidar and mask tiles at 0.5 m (CHM 240 by 240, Sentinel 24 by 24), a small GPU helps) |
| ★★★☆☆ | [Charted wreck with unknown depth or doubtful status: locate it and measure its least dept…](charted-wreck-unknown-depth-resolved-open-bathymetry.md) | harvest | laptop-hours per record (small windows of BlueTopo, BAG, lidar or INFOMAR grids around each charted position) |
| ★★★☆☆ | [Unrecorded earthwork (ringfort, enclosure, barrow or similar) in open Irish LiDAR, absent…](ireland-earthwork-not-in-smr.md) | harvest | laptop-hours (GSI LiDAR GeoTIFF terrain tiles of 0.13 m to 2 m cells, tens of MB each; SMR points by live query or a bulk CSV of about 151,000 rows) |
| ★★☆☆☆ | [Unlisted desert kite (prehistoric stone-walled game trap) in declassified CORONA or HEXAG…](desert-kite-not-in-globalkites.md) | harvest | laptop-hours (Globalkites JSON files under 1 MB; each declassified photograph scan is hundreds of MB and must be orthorectified, so work on georeferenced chips) |
| ★★☆☆☆ | [Unregistered ancient monument (stone cairn, pit-house hollow, hunting-pit row or hillfort…](finland-ancient-monument-not-in-relics-register.md) | harvest | laptop-hours (NLS open laser scanning point clouds thinned to 0.5 points per m^2, LAZ files on 3 km by 3 km map sheets, tens of MB each; register GeoPackage download) |
| ★★☆☆☆ | [Uncharted wreck candidate in open multibeam or lidar bathymetry (US and Irish waters), se…](uncharted-wreck-open-multibeam-not-in-wreck-records.md) | harvest | laptop-days (windowed reads of BlueTopo tiles and survey grids of tens to hundreds of MB each; a search region is chosen first) |
| ★★☆☆☆ | [Unrecorded hillfort in open Scottish LiDAR, absent from the Atlas of Hillforts of Britain…](scotland-hillfort-not-in-atlas-or-canmore.md) | standard | laptop-hours to laptop-days (LiDAR terrain tiles of 0.5 m to 2 m from a public S3 bucket; a whole survey phase is far larger than a laptop disk, so screen hill terrain first) |

← [All categories](../README.md)
