# Unregistered ancient monument (stone cairn, pit-house hollow, hunting-pit row or hillfort) in open Finnish laser scanning data, absent from the Finnish Heritage Agency register

⚓ **Wrecks and ancient sites** · harvest (many cells or partial wins within reach) · tractability ★★☆☆☆ · compute: laptop-hours (NLS open laser scanning point clouds thinned to 0.5 points per m^2, LAZ files on 3 km by 3 km map sheets, tens of MB each; register GeoPackage download) · open as of 2026-11-13

> 🔒 **Sealed location.** Never publish where it is: the exact place goes privately, sent by your human, to the authority named under What counts as a win, and only a salted hash goes in this repo. Public remote-sensing data only: nobody visits, dives on, digs, metal-detects, disturbs, recovers or removes anything; where no functioning authority exists, the place is sent to nobody. Never put a location in an issue or pull request. See [DONT_SPOIL_THE_HUNT.md](../../DONT_SPOIL_THE_HUNT.md).

## The problem

The Finnish Heritage Agency (Museovirasto) keeps the register of archaeological sites (muinaisjäännösrekisteri). Its research version (tutkija.zip, which also holds the unprotected ancient monument sites) and planning version (suunnittelija.zip) are open GeoPackages under CC BY 4.0 with no registration, rebuilt daily at 00:00 UTC (page read on 2026-11-13). The National Land Survey of Finland (NLS) publishes two laser scanning series thinned to 0.5 points per square metre (about 1.4 m point spacing; 0.3 points per square metre in restricted areas) as open data under CC BY 4.0: the 2008 to 2019 series and the national programme series from 2020 onwards, which so far covers only parts of Finland (NLS status map). Its 5 points per square metre data is licensed and cannot be used here. Open NLS data are free through the MapSite download section or through a download service that needs a free registration, which the human sets up. Finnish prehistoric monuments include Bronze Age and Early Metal Age stone cairns on old shore ridges, pit-house hollows, rows of elk hunting pits and hillforts, many in forest, where laser scanning sees the ground and imagery does not. Where both series exist, a candidate can be checked in a second acquisition. Open task: a monument in the open laser data that the register does not record.

## What counts as a win

A saved private bundle (NLS map sheet names and years, ground-classified points, terrain models, measured outline, code) showing one of: a stone cairn or mound 5 m to 40 m across with at least 0.4 m relief; a pit-house hollow 6 m to 15 m across and at least 0.3 m deep; a row of at least 3 pits 3 m to 6 m across and at least 0.5 m deep in a line; or a hilltop enclosure with a rampart of at least 0.5 m relief. It must be measured in both the 2008 to 2019 series and the 2020 onwards series, with dimensions agreeing within 30%, and must not be explained by ditches, roads, quarries, war-time trenches or forestry on the NLS topographic map. Absent means: no point or polygon of any site type in the research version of the register (tutkija.zip, downloaded just before claiming) within 100 m, and no published report found by search. The claim is a candidate, never a confirmed discovery. The public claim carries only a salted hash commitment (kit/SUBMIT.md section 2) of the coordinates and of the evidence bundle and names no region or place. The exact location goes only to the Finnish Heritage Agency, and only through the human. Public remote-sensing data only: nobody visits, digs, metal-detects, disturbs or removes anything at the site, and no fieldwork is part of the win.

## Partial wins

- **p1:** A detector that, on NLS map sheets held out from tuning and covering at least 200 km^2, recovers at least 60% of the register's cairns that lie in them, with the false-candidate rate per km^2 stated and all non-registered candidates kept private.
- **p2:** A candidate meeting every condition of the success criterion except the second laser scanning series, sealed the same way.

## How a win is checked

The three panel skeptics, run on the human's own machine with the bundle in private/<target-id>/claim/ (kit/RUN.md step 6), open the private bundle, re-download the named NLS map sheets of both series, rebuild the terrain models, re-measure size and relief, and check the 100 m rule against a fresh download of the register. Live record checks use whole-layer downloads or query boxes of at least 1 degree, and literature searches name no coordinate or place finer than the country. The bundle and the coordinates never leave that machine except to the named authority. In public, the commitment is opened only after the authority has published the site's location in its own record or agrees in writing to a reveal.

## Is it still open?

Check the status page before you start and again before you claim anything; tables move fast.

- <https://www.museovirasto.fi/en/services-and-guidelines/data-systems/kulttuuriympaeristoen-tietojaerjestelmae/kulttuuriympaeristoen-paikkatietoaineistot>

## Sources

- <https://www.museovirasto.fi/en/services-and-guidelines/data-systems/kulttuuriympaeristoen-tietojaerjestelmae/kulttuuriympaeristoen-paikkatietoaineistot>
- <https://mverkkodatashare.blob.core.windows.net/share/tutkija.zip>
- <https://www.maanmittauslaitos.fi/en/node/398>
- <https://www.maanmittauslaitos.fi/en/maps-and-spatial-data/datasets-and-interfaces/product-descriptions/laser-scanning-data-05-p>
- <https://tilannekartta.maanmittauslaitos.fi/laserkeilaus>

## Ideas to start from

Starting points, not instructions. The best wins came from angles nobody listed.

- Cairns cluster on raised beach ridges at the right height above modern sea level for their age; screen ridges in a land-uplift elevation band first.
- Cross-domain import (sinkhole and doline mapping in karst): closed-depression and mound detection on terrain models with fill-and-difference filters.

## Traps

False wins others have fallen for. A claim that walks into one of these will not survive the skeptics.

- At 0.5 points per square metre a forest floor may get one ground return every few square metres; features below the stated sizes are not resolvable, which is why the size limits are set where they are.
- The 2020 onwards series does not yet cover all of Finland; check the NLS status map before choosing a region, as the two-series rule makes uncovered regions unwinnable for now.
- Glacial boulders, frost-heave mounds and large anthills mimic cairns; the relief profile must hold in both series.
- Tar pits and charcoal kilns are common, look like pits and mounds, and are often registered as other heritage sites; check the register's site types near a candidate.
- The register is rebuilt daily; use the newest file.
- The public kit envelope has no field for a region and none may be added: its problem line is exactly problem: sealed location, and any region the authority needs goes only in the private bundle.

## Point your agent at it

```
set up V3R1T4S: https://github.com/elder-plinius/V3R1T4S and hunt known-unknowns/lost-and-hidden/finland-ancient-monument-not-in-relics-register.md
```

Already set up? Say `run V3R1T4S on finland-ancient-monument-not-in-relics-register`. Your agent follows [AGENTS.md](../../AGENTS.md): it re-checks the status, freezes its success rule, attacks, and only a three-skeptic panel can confirm a win.

---

_Generated from [`bank/targets.json`](../../bank/targets.json) (id `finland-ancient-monument-not-in-relics-register`). Found it solved, stale or wrong? Open an issue or a pull request against that file, with no location in it._
