# CRITERION skeptic: claim tsunami-tide-gauge-signal-not-in-ncei, partial win p3

context: subagent (Claude Agent tool, fresh context, model claude-opus-5-5)

Read: only claim/ (CLAIM.md, REPRODUCE.md, PREREG.md to PREREG.v6.md, PREREG.sha256, result/, result_v4/, and the
code and data under claim/ that they name), plus the operating system's Webster's Second International word list (web2)
as the independent dictionary. Nothing else in the run folder was read. Scratch scripts and outputs are in
panel/work_criterion/ (recount.py, extra.py, extra2.py, the rerun/ and rerun_v4/ folders, and their *_out.txt files). claim/ was not
modified: no file in it has a modification time after the review started, and no bytecode was written.

## Bottom line

The result meets partial win p3 once each word of p3 is read as the bank's own criterion and pitfalls define it. The numbers
recount exactly, the map reruns byte for byte offline, the stated denominator is the bank's 264, and the fake-origin null
is fair and is beaten under every rule set, including the pre-registered one. Two limits go into the scope. The numerator
is the fraction that passes the target's strict per-gauge test, not "any tsunami signal" in the everyday sense. "Open
gauges" means IOC SLSMF (the UNESCO Intergovernmental Oceanographic Commission's Sea Level Station Monitoring Facility)
coastal gauges within 1000 km only. One post-hoc rule, the 24 h overlap exclusion, raises the headline from 0.118 to 0.138.
The claim discloses this, and the scope below gives both values next to the pre-registered 0.158.

## 1. Rules fixed before the result?

- PREREG.sha256: all six hashes match the files now (shasum -a 256 run by me). The freeze times (PREREG.md 19:30:15Z, v2
  19:34:52Z, v3 19:45:43Z, v4 19:52:52Z, v5 20:23:43Z, v6 20:56:56Z) are self-reported. Nothing in claim/, such as a
  git commit or an external timestamp, lets me check them on my own.
- PREREG.md to v3 come before any map result, as their text states. v4 changes no scoring rule (data access and a budget
  stop) and was written after the class lines of 114 quakes had been printed. It says so itself.
- PREREG.v5.md calls itself "a post-hoc repair, declared as such", written after the v4 map and the self-break. CLAIM.md
  says the same in its one-sentence claim ("a post-hoc repaired version (PREREG.v5 ...)") and in its rules history.
- PREREG.v6.md lists three implementation corrections, made after panel round 1, and changes no rule. My recount finds 0
  class changes between the as-run v5 map and the corrected one (map_summary.txt "as-run v5 -> v6": 0 / 0 / 0, and my
  rerun reproduces that file exactly).

### Does the post-hoc change move the headline in the claim's favour? (recounted from result/ and result_v4/)

| rule set | SIGNAL / scored | fake rate | best of 400 | adversarial worst-case fake catalogue | real beats all |
|---|---|---|---|---|---|
| pre-registered v4 (v6 code) | 35 / 221 = 0.1584 | 0.0526 | 0.0780 | 19 / 218 = 0.0872 | yes |
| v5 rules 1-2 only (no overlap rule) | 26 / 221 = 0.1176 | 14 / 437 = 0.0320 | 0.0550 | 13 SIGNALs | yes |
| v5 claimed (with overlap rule 3) | 26 / 188 = 0.1383 | 11 / 407 = 0.0270 | 0.0495 | 11 / 202 = 0.0545 | yes |

- Going from v4 to v5, no quake that was not a SIGNAL becomes one. My cross-tab of result_v4/map.csv against result/map.csv shows
  0 such quakes: 26 stay SIGNAL, 7 become NO_SIGNAL and 2 become OVERLAP. So rules 1 and 2 only remove SIGNALs, as declared.
- Rule 3 (OVERLAP) removes 34 origins from the denominator (32 NO_SIGNAL, 1 SIGNAL_UNDECIDED, 1 NO_DATA) and no SIGNAL.
  It raises the fraction from 0.118 to 0.138 and lowers the fake rate from 0.032 to 0.027. So it does move the headline
  in the claim's favour. That is disclosed: CLAIM.md gives 26/221 = 0.118 and its fake rate in the one-sentence claim, and
  result/no_overlap.txt reruns the same way.
- The win does not depend on the post-hoc rules. The pre-registered v4 map alone beats every fake catalogue, and also the
  adversarial one, where each quake gets whichever fake origin gives the most SIGNALs, which I found exactly by Dinkelbach
  iteration (0.087 < 0.158).

## 2. Each word of p3, read literally

p3: "A completeness map: fraction of M >= 6.5 shallow subsea earthquakes 2015-2025 with any tsunami signal on open gauges
vs NCEI listing, reproducible from saved code."

Dictionary check, run by extra2.py on the web2 word list with 1-2 letter entries dropped except common words: of the 23
word tokens in p3, only "M" and "NCEI" are not in the list. "shallow", "subsea", "completeness", "gauge", "listing",
"tsunami", "signal" and "reproducible" are all in it. Every token of the confirmed scope that is missing from the list is
an acronym, a unit or a short form: ComCat (the USGS earthquake catalogue), ETOPO (NOAA's global relief model), IOC,
SLSMF, NCEI (NOAA's National Centers for Environmental Information, which keeps the tsunami database), RMS, USGS, km, h,
arcmin, pre-, post hoc, v4, byte, offline, and "epicentre" (the list has the US spelling "epicenter").

- **M >= 6.5, 2015-2025**: data/comcat/m65_d70_2015_2025.csv has 343 rows, all type earthquake, magnitude min 6.5, depth max
  70.0, times 2015-01-07 to 2025-12-27. I could not re-query ComCat itself (no network).
- **shallow**: depth <= 70 km. This is the standard seismological depth class (shallow 0-70 km, as USGS uses it), and the
  bank pitfall uses the same bound. Not stretched.
- **subsea**: the ETOPO1 2-arcmin cell nearest the epicentre has altitude < 0. My own lookup on data/bathy gives 264 subsea and 79
  land, matching the bank pitfall's 264. Sensitivity: 248 if all 3x3 neighbouring cells must be water, 274 if any one
  may be. 11 subsea epicentres sit within 50 m of sea level, all coastal (for example us6000nith, Hyuganada, alt -5 m).
  None falls in a land basin below sea level (I checked boxes for the Caspian, Dead Sea, Danakil, Turfan, Qattara, Death
  Valley and Salton). The bank defines the word this way, so it is not stretched. Kaikoura and Palu, NCEI-listed with
  land epicentres, are in result/land_listed.txt (25 land-epicentre quakes are listed) and are outside the denominator,
  as the pitfall warns.
- **fraction, with the stated denominator the pitfall asks for**: map.csv has 264 rows. The ids match my 264 exactly. Classes:
  NO_GAUGE 25, NO_DATA 17, OVERLAP 34, NO_SIGNAL 162, SIGNAL 26. Headline 26/188 = 0.1383 (Wilson 0.096-0.195),
  26/264 = 0.0985, upper bound 102/264 = 0.3864. The pitfall's station counts reproduce from data/ioc_stationlist.json:
  6 subsea quakes have no IOC station of any status within 1500 km and 42 none within 500 km (and 21 none within 1000 km).
  Quakes without usable open-gauge data are counted explicitly, as the pitfall requires.
- **any tsunami signal**: SIGNAL means at least one site passes, on every usable tied sensor, the criterion's per-gauge test:
  peak > 5 x RMS24 in the band, arrival within +/-10 min of the model travel time, and no r > 5 in the same hours on any
  of >= 10 usable control days. That is exactly the criterion's definition of a signal, and the human's rule keeps the
  5x bar and the +/-10 min rule "unchanged for every claim". I re-derived pass / detect / undecided for every code at every
  origin from the per-sensor r, arrival and control-day values in result/quakes/: 0 mismatches. So "any" reads as "at
  one or more gauges", and "tsunami signal" as the criterion's test. The claim says plainly that this is a test-pass
  fraction, and it is a strict one:
  - The travel-time model puts 0.468 of held-out 2015-2026 NCEI tide-gauge arrivals outside +/-10 min (79 rows, 25
    events; attempts/evaluator-first/out/calibrate.txt).
  - The 2025 M8.8 Kamchatka quake (us6000qw60) is NO_SIGNAL. At petr, r = 10.796 but the arrival is 21.8 min after the
    model time (I checked this in its JSON).
  - Looser readings, my extra.py, real minus fake: "r > 5 at some site" gives an excess of 0.262 (82/188 vs 71/407).
    "Detects with no control-day rule" gives 0.126 (32/188 vs 18/407). The claimed SIGNAL excess is 0.111. So the test
    catches well under half of the excess that real origins show over fake ones in raw r > 5. The scope must say "passed
    the test", not "had a tsunami signal".
  - Minor: the band is a 120-min high-pass on a 1-min grid. The 2-min edge is the grid's Nyquist limit, with no
    anti-alias filter. This applies to real and fake origins alike.
- **on open gauges**: IOC SLSMF codes with a sea-level sensor, DART stations excluded, within 1000 km and with a model
  travel time of 10-150 min. Signals at farther or other open networks are not counted. This is a hidden restriction of
  "open gauges", and the scope names it.
- **vs NCEI listing**: I recomputed LISTED from the saved NCEI events (230 unique events): 0 disagreements with map.csv,
  also for validity 4. Over the 188 scored quakes: SIGNAL & listed 24, SIGNAL & unlisted 2, NO_SIGNAL & listed 62,
  NO_SIGNAL & unlisted 100. 86 of 188 (0.457) are listed. LISTED is generous: any validity, any cause, +/-1 calendar day,
  1000 km. With validity 4 and cause "earthquake" only, the table is 22 / 4 / 56 / 106. The 2 unlisted SIGNALs are
  usd000j5jt (ouve, r 7.362, 575.5 km) and us7000nhjw (alofi, r 7.497, 324.5 km), both single-site. Chance predicts 2.76
  among the 102 unlisted scored quakes (P(X >= 2) = 0.766). So the map finds no NCEI omission beyond chance, and the
  claim does not assert one. The listing is the 2026-10-24T19:20Z snapshot (sha256 in CLAIM.md). I could not re-fetch it
  (no network). p3's own wording does not require the live re-fetch that the main win needs.
- **map**: the deliverable is a per-quake table with coordinates (result/map.csv), the 30-degree longitude-band table and
  the 2 x 2 tables, not a drawn figure. I read p3's colon as defining the map as this fraction, so I accept it.
- **reproducible from saved code**: I reran attempts/completeness-map-v6/code/p3_map_v6.py offline (V3_OFFLINE=1) for the v5
  rules (2 shards) and the v4 rules, with output to panel/work_criterion/. Then I ran summarize_v6.py and no_overlap.py.
  Results: 0 OFFLINE_MISS lines. All 264 v5 quake JSONs and all 264 v4 quake JSONs are byte-identical to result/quakes
  and result_v4/quakes. map.csv, null.json, map_summary.txt, listed_rows.txt, land_listed.txt and no_overlap.txt are
  byte-identical to result/. The reruns read 4447 distinct raw IOC files. All 4447 are in data/ioc_provenance.tsv
  (HTTP 200), and their sha256 matches the fetch log for all 4447 (0 differ). Peak memory was 0.32 GB per process.

## 3. Is the null model fair?

- Fake origins at o-5 h and o-7 h use the same codes, travel times and rules, their own control days, and the same overlap rule.
  Their peak windows end by o-0.5 h at the latest, so the real tsunami cannot leak in. This is a fair estimate of the test's
  false-positive rate.
- Recount: fake SIGNALs 6/202 (o-5 h) and 5/205 (o-7 h), pooled 0.0270, expected 5.08 among the 188. The 400 catalogues
  (seed 20261024) give mean 0.0271 and max 0.0495, identical to null.json. The resampling uses only two fake runs per
  quake, so I also computed the exact adversarial catalogue: 11/202 = 0.0545 < 0.1383. Binomial tail
  P(X >= 26 | 188, 0.0270) = 1.30e-11. Paired by quake: 25 quakes have a real SIGNAL and no fake one, and 6 have a fake
  SIGNAL and no real one.
- Conservative quirks that raise the fake rate: 2 of the 11 fake SIGNALs are tsunamis of other quakes inside the fake
  window (us7000dfk3 at o-5 h, us7000dffl 46 min later; us20003kfj at o-7 h, Illapel 119 min later). One fake pass at
  adak2 has r = 237.6.
- What the null does not model is ground shaking or a coseismic step at the real origin only. I checked this: the earliest
  passing arrival at any real origin is 11.08 min after origin (abur, us6000nith). Shaking from a source within 1000 km
  arrives within a few minutes. No SIGNAL quake rests only on arrivals before 16 min.
- Single-site SIGNALs: 19/188 = 0.101 against a fake rate of 0.027 (binomial P = 1.05e-06). Their passing r is higher than
  that of the fake passes (Mann-Whitney one-sided p = 0.016). Still, about 5 of the 26 are expected by chance. All 11 fake
  SIGNALs are single-site, and all 7 real multi-site SIGNALs are NCEI-listed (us20003k7a 14 sites, us6000417i 4,
  us10007b88 3, and us1000i2gt, us7000jkbd, us7000lgwp, us6000nith with 2 each).

## 4. Hidden quantifiers and stretched definitions found

1. "any tsunami signal" means a pass of a strict fixed test, at one or more sites and on every usable tied sensor. That
   is a test-pass fraction, which I estimate captures well under half of the real-origin excess in raw r > 5. It is
   disclosed and goes into the scope.
2. "open gauges" means IOC SLSMF non-DART gauges, within 1000 km, with a model travel time of 10-150 min. It is
   disclosed and goes into the scope.
3. The denominator excludes 34 overlap origins under a post-hoc rule that raises the fraction. It is disclosed, and the
   scope gives 0.118 and the pre-registered 0.158 next to 0.138.
4. "NCEI listing" means any NCEI event of any validity or cause within +/-1 day and 1000 km, from a same-day snapshot.
   It is disclosed and goes into the scope.
5. "subsea" uses the nearest ETOPO1 cell, as the bank defines it (248-274 under neighbour variants). Accepted.

The rules, the freeze times and the post-hoc steps are reported honestly, and nothing above widens the claim beyond its
own scope paragraph. I cannot confirm offline that p3 has not already been taken. CLAIM.md's scout record (GitHub, 19:20Z)
reports no p3 claim in TROPHY_CASE.md, known-knowns/ or any PR, and issue #253 holds only an unpanelled map posted as data.

confirmed_scope: In a map that reruns byte-for-byte offline from the saved code and data, of the 264 USGS ComCat M >= 6.5, depth <= 70 km earthquakes of 2015-2025 whose epicentre lies in an ETOPO1 2-arcmin water cell, 188 could be scored at open IOC SLSMF tide gauges within 1000 km (model travel time 10-150 min, at least one usable site, and no other M >= 6.5, depth <= 70 km ComCat earthquake, land or sea, within 1000 km in the preceding 24 h; 25 had no gauge in scope, 17 had no usable data and 34 were set aside by that post-hoc 24 h rule), and 26 of the 188 (0.138, Wilson 95 % 0.096-0.195; 26 of 221 = 0.118 without the post-hoc 24 h rule; 35 of 221 = 0.158 under the pre-registered v4 rules) passed, at one or more sites and on every usable tied sensor, the target's per-gauge test (band-passed peak above 5 times the preceding 24 h RMS, arrival within +/-10 min of a model travel time that puts 0.468 of held-out NCEI tide-gauge arrivals outside +/-10 min, and no peak above 5 times RMS in the same hours on any of at least 10 usable control days), which is a test-pass fraction and not the fraction with any observable tsunami signal, against a fake-origin chance rate of 0.027 (best of 400 fake catalogues 0.0495), with 24 of the 26 listed by NCEI (an NCEI event of any validity or cause within +/-1 day and 1000 km, events snapshot of 2026-10-24T19:20Z) and the 2 unlisted ones passing at a single site, as many as chance predicts (2.8 expected among the 102 unlisted scored quakes).

pass: true
