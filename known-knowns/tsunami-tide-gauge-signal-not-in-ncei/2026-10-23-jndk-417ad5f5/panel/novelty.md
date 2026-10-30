# Novelty skeptic: tsunami-tide-gauge-signal-not-in-ncei, partial win p1 (NCEI event 5942)

context: subagent (Claude Code Agent tool, fresh context)

Inputs read: claim/CLAIM.md, claim/REPRODUCE.md, claim/data/observations.csv, claim/data/ncei_event_5942.json. No code was run; only fetches, reading and text tools (jq, grep, sha256sum).
Fetched files are saved in claim/mine/. Each URL was fetched once with plain curl and User-Agent "V3R1T4S novelty skeptic (verification panel)", with no retries.

## 1. NCEI status fetch (the bar)

**Runups for the event (primary)**
- URL: https://www.ngdc.noaa.gov/hazel/hazard-service/api/v1/tsunamis/runups?tsunamiEventId=5942
- Fetch time (`date -u`): 2026-10-23T23:04:33Z
- HTTP status: 200. Size: 1085 bytes.
- sha256: 64268edc6e5201f3016cdae999b24ee94bcc5e34a05220159732046713cec7ae. This is byte-identical to the scout record in CLAIM.md.
- Saved as: claim/mine/ncei_runups_5942.json
- Response metadata: totalItems 2, totalPages 1, itemsPerPage 200.

| id | locationName | lat | lon | typeMeasurementId | runupHt (m) | max-wave arrival (UTC) | distFromSource (km) |
|---|---|---|---|---|---|---|---|
| 38852 | LENAKEL, TANNA | -19.53256 | 169.26595 | 2 (tide gauge) | 0.17 | 12-17 02:54 | 242.2 |
| 38853 | PORT VILA, EFATE ISLAND | -17.7553 | 168.3077 | 2 (tide gauge) | 0.25 | 12-17 02:15 | 30.0 |

Neither the runups body nor the events body contains the strings ESPIRITU, LUGANVILLE, LIFOU, LOYALTY or SANTO. Both rows have country VANUATU, and no row has country NEW CALEDONIA. The claimed gauges are Luganville (-15.516, 167.189) and Lifou (-20.918, 167.279). By hand arithmetic, the nearest NCEI rows are about 276 km away (Port Vila) and about 258 km away (Lenakel), which agrees with CLAIM.md.

**Events for 2024 (to check for a second event holding these rows)**
- URL: https://www.ngdc.noaa.gov/hazel/hazard-service/api/v1/tsunamis/events?minYear=2024&maxYear=2024
- Fetch time: 2026-10-23T23:04:34Z
- HTTP status: 200. Size: 6361 bytes.
- sha256: 28b489b08cd9ca050e19d6afcfca2bdddf2f4912b8628fe95251eebcd86a4c8f
- Saved as: claim/mine/ncei_events_2024.json
- Contents: 14 events in 2024. Four are in December:
  - 5940: 12-05, N. California.
  - 5942: 12-17 01:47, VANUATU ISLANDS, -17.686 168.034, validity 4, numRunups 2. This matches claim/data/ncei_event_5942.json.
  - 5947: 12-17, WHITEHORSE, YUKON, Canada, causeCode 8, validity 3, numRunups 0.
  - 5945: 12-27, Peru-Ecuador-Chile, numRunups 0.
- No other event falls within +/-1 day in the Vanuatu–New Caledonia region, under any validity code. So the rows are not listed under a second event or a different source time.

**Supplementary fetch (inconclusive)**
- URL: https://www.ngdc.noaa.gov/hazel/hazard-service/api/v1/tsunamis/runups?minYear=2024&maxYear=2024
- Fetch time: 2026-10-23T23:04:54Z. HTTP status: 200.
- sha256: 7bef4fb899d8f0fdb3a0ace35466c61fa10a7596e8da491a64e9f60dc84f2bb0
- Saved as: claim/mine/ncei_runups_2024.json
- The API ignored the year filters: it returned totalItems 35129 over 176 pages, and page 1 holds years -1610 to 1687. I did not page through it, so it adds nothing for or against the claim. The event-id query and the events list above are the decisive checks.

No 401, 403, 429 or 503 response and no challenge page was returned.

## 2. Literature and web (last 24 months)

- **J. Patton (earthjay.com), Luganville tide-gauge plot, Dec 2024.**
  - URL: https://earthjay.com/earthquakes/20241217_vanuatu/20241217_vanuatu_tide_gage_plot_luganville.pdf
  - The plot reads "Tide Gage - Luganville, Max Amplitude 5.6 cm, Max Wave Height 11.1 cm", with a window of 12/17/2024 00:00 to 12:00 UTC.
  - So the Luganville tsunami trace was already shown in public before this claim. It is a personal website, not NCEI.
  - The same series also has plots for Port Vila and Hienghene.
  - The plot's numbers differ from claim/data/observations.csv (peak 7.8 cm, peak-to-trough 13.6 cm), presumably because the filtering differs. That difference is for the reproducibility and method skeptics; it is not a novelty issue.
- **J. Roger (GNS Science), EGU25-7588.**
  - URL: https://meetingorganizer.copernicus.org/EGU25/EGU25-7588.html
  - Quote: "the tsunami was recorded on ... other Vanuatu gauges and in New Caledonia, including the Loyalty Islands."
  - Quote: "Apart from VANU and LENA ... the records do not show maximum tsunami amplitude greater than 10 cm."
  - The abstract names no Luganville or Lifou station and gives no value for either.
- **INGV CAT news page.**
  - URL: https://cat.ingv.it/index.php/en/media-and-documents/news-en/451-17-12-24-tsunami-in-the-vanuatu-islands-pacific-ocean
  - It names only the Port Vila gauge.
- **Other searches.**
  - I searched for a PTWC bulletin, for "Lifou marégraphe", and for 2025 journal papers.
  - None found a published Lifou gauge amplitude or arrival time for this event, and none found a peer-reviewed paper on these records.
  - The French press (e.g. https://www.lnc.nc/article/nouvelle-caledonie/environnement/un-seisme-d-une-magnitude-7-3-enregistre-au-vanuatu-l-alerte-tsunami-levee-sur-l-ensemble-de-la-caledonie) reports only that the alert was raised and lifted for the Loyalty Islands.

**Does this make the claim not new?**
The claim is not that the signal was never seen. It is that NCEI's runup table has no row for these stations, and the p1 wording ("where NCEI has no runup rows for those stations") is about NCEI only.
- Luganville: earthjay published its trace earlier. So "first public observation" would be false for Luganville, but the earlier plot does not put a row into NCEI.
- Lifou: I found no prior public amplitude or arrival time. EGU25 says only, in general terms, that the tsunami was recorded in the Loyalty Islands.

The bank target page's traps list nothing that excludes observations published outside NCEI. So the prior reports do not defeat p1 as defined. Any write-up must credit earthjay for Luganville and not call the Luganville observation a first.

## 3. Repo and pull requests

- **TROPHY_CASE.md** (local read-only copy, 100 lines): no mention of tsunami, NCEI, tide gauge, Vanuatu, Luganville or Lifou.
- **known-knowns/**: 23 entries; none mentions tsunami, NCEI, Vanuatu, Luganville or Lifou.
- **Open PRs**, `gh pr list -R elder-plinius/V3R1T4S --state open --search tsunami` (same result for `--search NCEI`):
  - The only hit is #371 (DRAFT), "[bank] tsunami-tide-gauge-signal-not-in-ncei: travel-time model error, p3 denominator (refs #253)".
  - It changes the bank's pitfalls and makes no win claim. Its body does not mention Vanuatu or event 5942.
- **All PRs, any state**: searches for Vanuatu, 5942, Luganville and Lifou returned nothing.
- **Issues**: the only hit is #253, a bank-rule issue about timing and the p3 denominator. It is not a prior claim.

## Reasoning

What p1 has to beat is NCEI's current table. A live re-fetch, byte-identical to the scout's, shows NCEI lists exactly 2 tide-gauge rows for event 5942 (Port Vila, Lenakel). It has none for Luganville or Lifou under any name. No second NCEI event within +/-1 day holds them.

The claim adds observations at 2 distinct sites; lifo and lifo2 are one site and count once. That beats what NCEI lists for those stations, which is nothing, so it is not a tie.

No earlier V3R1T4S claim, trophy, known-known or PR covers this event. Earlier public material does exist: a Luganville trace on earthjay, and a general EGU25 mention of the Loyalty Islands. It counts against calling the observations unseen, not against the NCEI-gap claim that p1 defines.

Out of scope for this panel seat (signal reality, the +/-10 min timing rule, control days): the Luganville onset is 7.6 min early relative to the model. Those belong to the other skeptics.

Verdict on novelty: the NCEI gap is confirmed live, and there is no prior claim in the repo. The Luganville observation is not a first public observation, and the write-up must say so.

pass: true
