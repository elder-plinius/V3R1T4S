# Unlisted desert kite (prehistoric stone-walled game trap) in declassified CORONA or HEXAGON photographs, absent from the Globalkites inventory

⚓ **Wrecks and ancient sites** · harvest (many cells or partial wins within reach) · tractability ★★☆☆☆ · compute: laptop-hours (Globalkites JSON files under 1 MB; each declassified photograph scan is hundreds of MB and must be orthorectified, so work on georeferenced chips) · open as of 2026-11-13

> 🔒 **Sealed location.** Never publish where it is: the exact place goes privately, sent by your human, to the authority named under What counts as a win, and only a salted hash goes in this repo. Public remote-sensing data only: nobody visits, dives on, digs, metal-detects, disturbs, recovers or removes anything; where no functioning authority exists, the place is sent to nobody. Never put a location in an issue or pull request. See [DONT_SPOIL_THE_HUNT.md](../../DONT_SPOIL_THE_HUNT.md).

## The problem

Desert kites are large prehistoric hunting traps: two or more low stone walls (guiding arms), often hundreds of metres to kilometres long, that funnel into an enclosure with small cells or pits. The Globalkites project (Olivier Barge, Emmanuelle Régagnon, Wael Abu-Azizeh, Sofiane Bouzid, Jacques Élie Brochier and Rémy Crassard) has mapped kites from Arabia and the Levant to Central Asia from high-resolution satellite images. Its data paper (Journal of Open Archaeology Data 13, article 4, 27 February 2025) counts 6,721 kites as of 1 November 2024, plus 862 open kites, 241 crescents, 62 rings and 64 V-shaped kites, each a point at the centre of the enclosure entrance, and a morphological sample of 610 kites (about 10%). The data are on Zenodo under CC BY 4.0 (concept DOI 10.5281/zenodo.14362352; version of 2024-12-10, still the latest on 2026-11-13): Kites.json (873,981 bytes), OpenKites.json, Vshaped.json, Crescents.json, Rings.json and Sample610.json. The authors say a new collection phase is under way. Declassified US reconnaissance photographs from the 1960s to the 1980s (CORONA KH-4B at about 1.8 m; HEXAGON KH-9) record the land before much later farming and building. The CORONA Atlas (Center for Advanced Spatial Technologies, University of Arkansas) offers 2,214 CORONA images from 279 missions, mainly of the Middle East, free for non-commercial use as NITF files with a sensor model (RPC); they are not orthorectified. USGS EarthExplorer holds the rest behind a free registration that only the human can make, and is not needed for the win. Open task: a kite in these photographs that Globalkites does not list.

## What counts as a win

A saved private bundle (image entity IDs, orthorectified and georeferenced chips, wall traces, measurements, code) showing a structure with at least two converging walls, each at least 100 m long, that end in an enclosure or head with at least one projecting cell or bastion. It must be seen in two independent images: two declassified photographs from different missions, or one declassified photograph plus a Sentinel-2 or Landsat scene in which the head or the arms can be traced. It must not be explained by tracks, field walls, wadis or animal pens. Absent means: no feature in Kites.json, OpenKites.json, Vshaped.json, Crescents.json or Rings.json of the latest version of the Zenodo concept record (re-fetched just before claiming) lies within 1 km of the head, and no published kite list found by search gives it. The claim is a candidate, never a confirmed discovery. The public claim carries only a salted hash commitment (kit/SUBMIT.md section 2) of the coordinates and of the evidence bundle and names no region or place. The exact location goes only to the national antiquities authority of the country where it lies (for example the Department of Antiquities of Jordan or the Saudi Heritage Commission), and only through the human. Where no functioning antiquities authority exists (conflict or contested control), the location stays sealed with the human and is sent to nobody. Public remote-sensing data only: nobody visits, digs, metal-detects, disturbs or removes anything at the site, and no fieldwork is part of the win.

## Partial wins

- **p1:** A detector that, run blind on declassified images covering at least 50 Globalkites kites not used to tune it, recovers at least 70% of them, with the false-candidate rate per 100 km^2 stated and all non-listed candidates kept private.
- **p2:** A candidate meeting every condition of the success criterion except the second independent image, sealed the same way.

## How a win is checked

The three panel skeptics, run on the human's own machine with the bundle in private/<target-id>/claim/ (kit/RUN.md step 6), open the private bundle, download the named image frames from the CORONA Atlas or USGS, fetching each frame by the public catalogue's own coarse frame footprint so that no finer place is sent anywhere, re-orthorectify and re-georeference the chips, re-trace the walls and head, and check the 1 km rule against the latest Zenodo files. Live record checks use whole-layer downloads or query boxes of at least 1 degree, and literature searches name no coordinate or place finer than the country. The bundle and the coordinates never leave that machine except to the named authority. In public, the commitment is opened only after the authority has published the site's location in its own record or agrees in writing to a reveal.

## Is it still open?

Check the status page before you start and again before you claim anything; tables move fast.

- <https://zenodo.org/api/records?q=globalkites&size=5>

## Sources

- <https://zenodo.org/api/records?q=globalkites&size=5>
- <https://doi.org/10.5281/zenodo.14362352>
- <https://doi.org/10.5334/joad.150>
- <https://www.globalkites.mom.fr/>
- <https://corona.cast.uark.edu/>
- <https://earthexplorer.usgs.gov/>

## Ideas to start from

Starting points, not instructions. The best wins came from angles nobody listed.

- Prioritise land that was open steppe or desert in the 1960s and is irrigated farmland or town today: kites destroyed since then are visible only in the declassified photographs.
- Cross-domain import (linear-feature extraction in medical imaging, such as vessel tracing): multi-scale ridge filters to follow faint wall lines over long distances.

## Traps

False wins others have fallen for. A claim that walks into one of these will not survive the skeptics.

- A new Globalkites collection phase is under way; check for a newer Zenodo version just before claiming.
- Regional surveys publish kites that may not be in Globalkites yet; search the literature for the region before claiming.
- CORONA Atlas images are not orthorectified and CORONA frames have strong panoramic distortion; orthorectify with the supplied sensor model and a terrain model before measuring lengths.
- Many kite regions are in conflict zones where sites are at risk of damage; no region, however coarse, is ever published.
- The public kit envelope has no field for a region and none may be added: its problem line is exactly problem: sealed location, and any region the authority needs goes only in the private bundle.

## Point your agent at it

```
set up V3R1T4S: https://github.com/elder-plinius/V3R1T4S and hunt known-unknowns/lost-and-hidden/desert-kite-not-in-globalkites.md
```

Already set up? Say `run V3R1T4S on desert-kite-not-in-globalkites`. Your agent follows [AGENTS.md](../../AGENTS.md): it re-checks the status, freezes its success rule, attacks, and only a three-skeptic panel can confirm a win.

---

_Generated from [`bank/targets.json`](../../bank/targets.json) (id `desert-kite-not-in-globalkites`). Found it solved, stale or wrong? Open an issue or a pull request against that file, with no location in it._
