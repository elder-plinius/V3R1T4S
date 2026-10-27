# NOVELTY skeptic verdict: seismic-missed-events-vs-comcat, partial win p1

context: subagent (fresh Claude Code Agent context, sees only claim/)

**Claim under test:** an earthquake at 2024-12-09T23:20:13.27 UTC, 39.1635 N, 119.0459 W, depth 7.0 km, ML 1.59-1.72,
an aftershock 11.7 min after the Mw 5.7 Parker Butte, Nevada mainshock (nn00888580), is listed in no known catalogue.
For a missed-event target, "strictly beats everything known" means that no known catalogue, publication or earlier
claim already lists this event.

**Lane:** this verdict covers novelty only, meaning absence from the status source, from other catalogues and from
earlier claims. It does not re-test the location, the null, Mc, magnitude or the blast checks; those belong to the
CRITERION and REPRODUCE skeptics.

## 1. Status source (one plain GET each, no retries, User-Agent "V3R1T4S-novelty-skeptic/1.0 (read-only research verification)")

| fetch time (UTC) | URL | HTTP | value seen |
|---|---|---|---|
| 2026-10-26T19:22:06Z | https://earthquake.usgs.gov/fdsnws/event/1/ | 200 | service page "API Documentation - Earthquake Catalog", 34,773 bytes (work/fetch/status_page.html) |
| 2026-10-26T19:22:07Z | https://earthquake.usgs.gov/fdsnws/event/1/query?format=csv&starttime=2024-12-09T23:19:43&endtime=2024-12-09T23:20:44&latitude=39.1635&longitude=-119.0459&maxradiuskm=50 | 200 | header row only, 160 bytes, **0 events** (work/fetch/absence_comcat.csv) |
| 2026-10-26T19:22:07Z | the same query with `&includedeleted=true` | 200 | header row only, **0 events** (work/fetch/absence_comcat_deleted.csv) |
| 2026-10-26T19:22:07Z | https://www.isc.ac.uk/fdsnws/event/1/query?starttime=2024-12-09T23:19:43&endtime=2024-12-09T23:20:44&latitude=39.1635&longitude=-119.0459&maxradius=0.45&format=text | 204 | no content, **0 events** (work/fetch/absence_isc.txt) |
| 2026-10-26T19:22:17Z | https://earthquake.usgs.gov/fdsnws/event/1/query?format=csv&starttime=2024-12-09T23:15:00&endtime=2024-12-09T23:25:00&latitude=39.1635&longitude=-119.0459&maxradiuskm=50 | 200 | sanity check (are the queries working?): **6 nn events** (nn00888571, 573, 575, 578, 581, 889380). The nearest are nn00888575 at 23:18:12.804 (ml 2.6, -120.5 s) and nn00888578 at 23:21:19.903 (ml 2.3, +66.6 s). Nothing within +/-30 s. (work/fetch/sanity_10min.csv) |

| 2026-10-26T19:25:17Z | https://www.isc.ac.uk/fdsnws/event/1/query?starttime=2024-12-09T23:15:00&endtime=2024-12-09T23:25:00&latitude=39.1635&longitude=-119.0459&maxradius=0.45&format=text | 200 | ISC sanity check (a separate query, not a retry): **4 NEIC events** at 23:15:17.7 (ML 3.3), 23:16:33.6 (3.1), 23:18:13.0 (2.7) and 23:22:27.3 (2.9). ComCat's ml 2.3 (23:21:19.9) and ml 2.2 (23:23:59.4) are **not** in ISC. (work/fetch/isc_sanity_10min.txt) |

- **Window:** 23:19:43 to 23:20:44 covers the claimed origin -30.27 s to +30.73 s, within 50 km.
- **Result:** the live ComCat service and ISC both return no event there. These agree with the claimant's logged queries
  of 17:29Z and 19:13Z.
- **Sanity check:** the 10-min query returns the neighbouring events, so the empty result is not caused by a broken
  query or a coverage gap.
- **ISC's limit:** ISC is reachable, but here it lists only the NEIC-forwarded events of M about 2.7 and above. Its
  absence result is therefore informative only down to that level, not for an ML 1.6 event. The claim's novelty against
  the comprehensive catalogues rests on ComCat (the status source) and on the Bogolub and Trugman catalogue.
- **Log:** every request is in work/fetch/fetchlog.txt.

## 2. Published enhanced catalogue
- **Zenodo record:** https://zenodo.org/api/records/15644553 (fetched 2026-10-26T19:23:00Z, HTTP 200). It is "Parker
  Butte Earthquake Catalog", published 2025-06-12. It holds a single version (is_last true) and one file,
  Parker_Butte_Catalog.csv, with md5 f7e02c8ff479187fccef028bceb4a9f4.
- **Shipped copy:** claim/data/Parker_Butte_Catalog.csv has the same md5 (f7e02c8ff479187fccef028bceb4a9f4), so it is
  the published file, unaltered.
- **My own scan:** I scanned that file independently (1,301 events, matching the paper's count; times are UTC and match ComCat to about 0.1 s). No
  event lies within +/-30 s of 23:20:13.27. Within +/-300 s there are six events, all of them ComCat events:
  - 888571 at -295.5 s
  - 888573 at -219.7 s
  - 888575 at -120.4 s
  - 888578 at +66.7 s
  - 888581 at +133.9 s
  - 889380 at +226.2 s

## 3. Literature, last 24 months (web searches on 2026-10-26)
- **Searches run:**
  - "Parker Butte" with catalogue, template matching, machine learning, PhaseNet/EQTransformer and 2026 preprint.
  - Walker Lane / western Nevada ML catalogues 2024-2026.
  - Bogolub et al. SRL.
- **Found:**
  - Bogolub et al., SRL, doi:10.1785/0220250203: 1,301 events from 1 Dec 2024 to 10 May 2025. It is a GrowClust
    relocation of the NSL catalogue, and its data release is the Zenodo file above.
  - Koehler et al. (2025, Seismica): surface fracturing; it has no event catalogue.
  - Trugman (2024, SRL): Nevada 2008-2023; ends before this event.
  - Chatterjee et al.: Nevada focal mechanisms 2008-2023; ends before this event.
  - Monte Cristo Range ML catalogues: a different sequence (2020).
  - A 2026 SCEC abstract on the 2026 Lake Lahontan M5.7: a different sequence.
- **Not found:** no template-matching or deep-learning enhanced catalogue of the Parker Butte sequence, and no other
  publication that lists an event at 23:20:13 on 2024-12-09.

## 4. This repository (elder-plinius/V3R1T4S, read-only gh, 2026-10-26T19:22Z)
- **TROPHY_CASE.md (main, 31,235 bytes):** no seismology family, and no mention of seismic, ComCat, earthquake,
  Parker Butte, Nevada or missed events.
- **Open pull requests (328):** the only earthquake-related titles are #642 and #736 (tsunami-tide-gauge-signal-not-in-ncei),
  which is a different target.
- **All-state PR searches** for "seismic-missed-events-vs-comcat", "Parker Butte" and "seismic": no results. "ComCat"
  and "earthquake" match only the tsunami PRs #642, #736 and #371.
- **The claimant's earlier runs:** claim.md discloses two earlier runs on this same event (2026-10-23-1839 and
  2026-10-24-0604). Both were the claimant's own attempts, and both got panel 2/3. Neither left a PR or a TROPHY_CASE.md
  entry, so they are earlier attempts on this event, not an earlier record of it.
- **Conclusion:** no earlier claim of this event or this target exists in the repository.

## 5. Caveats (not grounds for failure)
- **Novelty is sequence-specific:** missing early aftershocks of an M5.7 in the first minutes, when catalogues are
  incomplete, is routine. This target's p1 explicitly admits such events: M >= Mc - 0.3 in an authoritative region. The
  event is novel as a catalogue entry, not as a kind of finding.
- **Absence covers known catalogues only:** an unpublished NSL internal or ML catalogue could hold it. No such
  catalogue is public, so it cannot be checked.
- **"Strictly beats" is a binary test here:** for a missed-event target, the test is whether the event is listed
  anywhere. It is listed nowhere I can find, so this is not a tie.

## Verdict
- **Status source:** read live (HTTP 200) at 2026-10-26T19:22:07Z, with 0 events within +/-30 s and 50 km.
- **Other sources, all absent:**
  - ISC: HTTP 204. This is informative only for M >= about 2.7 here, since ISC also lacks ComCat's nearby ml 2.3 and
    ml 2.2 events.
  - The only published enhanced catalogue: absent, and the shipped file's md5 matches Zenodo.
  - Literature of the last 24 months: no listing.
  - TROPHY_CASE.md and the pull requests: no earlier claim.
- **Result:** on novelty, the claimed event is absent from everything known.

novelty: CONFIRMED (absent from live ComCat and from the Bogolub and Trugman 2025 catalogue; ISC 204 but ISC holds only M >= ~2.7 here; no prior repo claim)
pass: true
