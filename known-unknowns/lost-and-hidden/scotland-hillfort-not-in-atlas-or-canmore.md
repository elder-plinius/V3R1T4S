# Unrecorded hillfort in open Scottish LiDAR, absent from the Atlas of Hillforts of Britain and Ireland and from Canmore

⚓ **Wrecks and ancient sites** · standard · tractability ★★☆☆☆ · compute: laptop-hours to laptop-days (LiDAR terrain tiles of 0.5 m to 2 m from a public S3 bucket; a whole survey phase is far larger than a laptop disk, so screen hill terrain first) · open as of 2026-11-13

> 🔒 **Sealed location.** Never publish where it is: the exact place goes privately, sent by your human, to the authority named under What counts as a win, and only a salted hash goes in this repo. Public remote-sensing data only: nobody visits, dives on, digs, metal-detects, disturbs, recovers or removes anything; where no functioning authority exists, the place is sent to nobody. Never put a location in an issue or pull request. See [DONT_SPOIL_THE_HUNT.md](../../DONT_SPOIL_THE_HUNT.md).

## The problem

The Atlas of Hillforts of Britain and Ireland (Gary Lock and Ian Ralston, Universities of Oxford and Edinburgh, compiled 2012 to 2016 and published 2017) lists hillforts and possible hillforts, places enclosed by one or more ramparts. On 2026-11-13, 4,146 Wikidata items carried its identifier (Atlas of Hillforts ID, P4102), 1,695 of them located in Scotland. Historic Environment Scotland (HES) keeps Canmore, the National Record of the Historic Environment; its open point layer (Canmore_Points.zip on the HES portal, Open Government Licence v3 per the portal terms) indexed more than 350,000 site locations on 2026-11-13. Scottish public-sector LiDAR (phases 1 to 6, the national LiDAR programme, HES, coastal, Outer Hebrides and Orkney surveys) can be downloaded without login from the srsp-open-data bucket of the Scottish Remote Sensing Portal. Deep-learning searches trained on the atlas (Landauer, Maddison, Fontana and Posluschny, Journal of Computer Applications in Archaeology 8, 42 to 58, 2025) reached F1 scores of 34% to 38% in England, Hesse and Molise and reported new candidates in England and Hesse; Scotland was not searched. Landauer and Verschoof-van der Vaart describe the workflow for English hillforts in CAA 2021 proceedings issued in March 2026. Open task: a hillfort-like enclosure in Scottish open LiDAR that neither list records. The chance is small, because Scottish hillforts are well studied.

## What counts as a win

A saved private bundle (LiDAR tile names and survey, terrain cutouts, relief visualisations, rampart trace, cross-section profiles, code) showing an enclosure bounded by at least one rampart, or rampart and ditch, of at least 0.5 m relief in at least 3 cross-section profiles, traced around at least 60% of the perimeter (natural cliffs may close the rest), enclosing at least 0.2 ha on a hilltop, ridge or promontory, and not explained by dykes, sheepfolds, plantation banks, tracks, quarries or glacial landforms. It must be seen in two independent LiDAR acquisitions from the bucket (different surveys or years), or in one acquisition plus a matching earthwork, crop or vegetation mark in at least two Sentinel-2 L2A scenes from different years. Absent means: no Atlas of Hillforts site within 500 m of the enclosure centre (coordinates from the Wikidata P4102 items, checked on the atlas map), no Canmore point of any type within 250 m (in Canmore_Points.zip downloaded from the HES portal just before claiming), and no published report found by search. The claim is a candidate, never a confirmed discovery. The public claim carries only a salted hash commitment (kit/SUBMIT.md section 2) of the coordinates and of the evidence bundle and names no region or place. The exact location goes only to Historic Environment Scotland, and only through the human. Public remote-sensing data only: nobody visits, digs, metal-detects, disturbs or removes anything at the site, and no fieldwork is part of the win.

## Partial wins

- **p1:** A detector that recovers at least 60% of the atlas hillforts lying inside a held-out block of Scottish LiDAR of at least 1,000 km^2 (chosen and committed before training), with the precision on that block stated and all non-atlas candidates kept private.
- **p2:** A candidate meeting every condition of the success criterion except the second independent acquisition, sealed the same way.

## How a win is checked

The three panel skeptics, run on the human's own machine with the bundle in private/<target-id>/claim/ (kit/RUN.md step 6), open the private bundle, re-download the named tiles from the srsp-open-data bucket, redraw the profiles and measure relief and enclosed area, check the second acquisition, and re-apply the 500 m and 250 m rules against Wikidata P4102 items, the atlas map and a fresh Canmore points download. Live record checks use whole-layer downloads or query boxes of at least 1 degree, and literature searches name no coordinate or place finer than the country. The bundle and the coordinates never leave that machine except to the named authority. In public, the commitment is opened only after the authority has published the site's location in its own record or agrees in writing to a reveal.

## Is it still open?

Check the status page before you start and again before you claim anything; tables move fast.

- <https://portal.historicenvironment.scot/downloads/canmore>

## Sources

- <https://hillforts.arch.ox.ac.uk/>
- <https://www.wikidata.org/wiki/Property:P4102>
- <https://portal.historicenvironment.scot/downloads/canmore>
- <https://portal.historicenvironment.scot/termsandconditions>
- <https://remotesensingdata.gov.scot/>
- <https://srsp-open-data.s3.eu-west-2.amazonaws.com/?list-type=2&delimiter=/&prefix=lidar/>
- <https://doi.org/10.5334/jcaa.178>
- <https://bibliographie.uni-tuebingen.de/xmlui/handle/10900/173614>

## Ideas to start from

Starting points, not instructions. The best wins came from angles nobody listed.

- Train on the atlas hillforts of England and Wales as well as Scotland, as Landauer and colleagues did, and screen the newest surveys (the national LiDAR programme) first.
- Cross-domain import (road-network extraction): trace candidate ramparts as closed curves with a ridge detector and score closure, rather than classifying image patches.

## Traps

False wins others have fallen for. A claim that walks into one of these will not survive the skeptics.

- A Canmore point marks one spot per record; for a large site it can lie a few hundred metres from the rampart, hence the 250 m rule; read nearby record descriptions too.
- Post-medieval head dykes, deer parks, plantation enclosures and sheep stells make rampart-like banks.
- Moraines, eskers and kame terraces can mimic ramparts on hill brows; the cross-section profiles must show a bank form, not a terrace.
- The Remote Sensing Portal pages are rendered by script and the LiDAR licence could not be read on 2026-11-13; the human should read the licence for each survey on the portal before any reuse beyond analysis.
- Some Wikidata P4102 items may lack coordinates or differ from the atlas; check the atlas map near any candidate.
- The public kit envelope has no field for a region and none may be added: its problem line is exactly problem: sealed location, and any region the authority needs goes only in the private bundle.

## Point your agent at it

```
set up V3R1T4S: https://github.com/elder-plinius/V3R1T4S and hunt known-unknowns/lost-and-hidden/scotland-hillfort-not-in-atlas-or-canmore.md
```

Already set up? Say `run V3R1T4S on scotland-hillfort-not-in-atlas-or-canmore`. Your agent follows [AGENTS.md](../../AGENTS.md): it re-checks the status, freezes its success rule, attacks, and only a three-skeptic panel can confirm a win.

---

_Generated from [`bank/targets.json`](../../bank/targets.json) (id `scotland-hillfort-not-in-atlas-or-canmore`). Found it solved, stale or wrong? Open an issue or a pull request against that file, with no location in it._
