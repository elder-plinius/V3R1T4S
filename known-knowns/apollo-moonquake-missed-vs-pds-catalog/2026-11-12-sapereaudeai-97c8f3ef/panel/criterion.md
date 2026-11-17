# Panel: CRITERION skeptic (apollo-moonquake-missed-vs-pds-catalog, partial win p2)

context: subagent (fresh context, Claude Code Agent tool, subagent_type criterion)
date: 2026-11-12
scope read: the claim package only (CLAIM.md, prereg/, results/, baseline/, code/, data/, frozen/, waveforms/, REPRODUCE.md) plus the bank's local copy (bank/targets.json). Files are named relative to the claim folder.

## Binding text

- data/target_bank_entry.md and the success criterion and partial wins quoted in CLAIM.md and prereg/PREREG.md match the bank entry in bank/targets.json word for word (checked against the JSON).
- p2 (bank): "Recovery of >= 90% of one nest's catalogued events in one year with a measured false-alarm rate, saved and re-runnable."
- The full criterion is not claimed and is not met: no new event, one station only. p1 and p3 are not claimed. Only p2 is judged here.

## Literal reading of p2, clause by clause

1. "one nest": A1 (levent.1008weber.csv T2 = A, N2 = 1), a catalogued nest. Met.
2. "catalogued events ... in one year": calendar year 1971. The denominator does not shrink under a looser match. Stripping whitespace on T2, N2 and Y still gives 67 rows. All 26 rows labelled A1 in the original T1/N1 columns are among the 67, and no 1971 row with N2 = 1 has another type. The other PDS tables (Nakamura 2005 deep-moonquake arrivals and locations, Weber 2011 S picks) are per-nest tables, not event lists, so levent is the only event list. 1971 has the most A1 rows of any year (67; 1977: 59, 1970: 58, 1973: 57, 1976: 57, 1972: 54), so the year is not a favourable pick from the scored data.
3. ">= 90% recovery": 63 of 67 = 0.9403. All 67 lie in scanned data, so R2-primary equals all events; there is no gap exclusion. The bar needs 61 of 67, which leaves a margin of 2.
4. "with a measured false-alarm rate": 400 declustered detections >= theta on time-reversed 1971 data over 334.544 scanned day-equivalents = 1.196 per scanned day. That is the bank's own null, with the same templates over the full span. p2 sets no ceiling on the rate, and the rate is measured and reported. Met.
5. "saved and re-runnable": the package contains the waveforms (1254 files; all 1254 pass sha256sum -c against waveforms/SHA256SUMS_waveforms.txt), the PDS file URLs (data/urls_s12_1971.txt, data/urls_s12_dev1972.txt), the decoder, preprocessing, scan and scoring code, the frozen templates, the saved scan and REPRODUCE.md. I re-ran it (see below). Met. PDS file URLs stand in for the FDSN URLs, which only the full criterion asks for. The bank-entry access note discloses the substitution.

## Hidden quantifiers and stretched definitions checked

- Recovery window (R1, onset within +/- 5 min of the catalogued start). This is the bank's own identity window and is not stretched. Recovered onsets sit a median of +104 s after the catalogued start, consistent with the S arrival: the nest table gives S-P of about 92 s at S12 for A1. Only 2 of 63 are more than 120 s from the dev median offset of +93 s. Under a stricter window of +/- 120 s centred on +93 s, recall is still 61/67 = 0.910.
- Threshold choice. Theta = 0.10898 comes from the dev rule (<= 1 reversed-data false alarm per scanned dev day). Under the strictest reading, a threshold above the maximum of the 1971 time-reversed null (max 0.1376; theta 0.14, 0 reversed false alarms), recall is 61/67 = 0.910. At theta 0.12 (0.143 false alarms per day) and at 0.13 (0.015 per day) it is 62/67. The 90% bar holds at every fair threshold reading.
- Circularity with the catalogue's template-matched rows. 19 of the 67 rows have no stop time and amplitude -1 or blank. They look like the Bulow et al. cross-correlation additions, and all 19 are recovered. On the 48 rows with a stop time (visual catalogue), recall is 44/48 = 0.917, so the bar does not rest on events found by template matching in the first place. The bank wording counts all catalogued events in any case.
- Forward false alarms (not required; checked as a sanity test of the reversed null). There are 444 forward detections >= theta in 1971. 94 lie within +/- 5 min of some 1971 levent row; the other 350 (1.05 per scanned day) do not. That agrees with the reversed-data rate of 1.196 per day, so the reported rate is not optimistic. Precision against A1 is low (63 of 444), but p2 asks for a measured false-alarm rate, not a precision bar.
- Null model for chance recovery. At about 1.3 forward detections per day, a 10-minute window catches a chance detection about 0.9% of the time, so about 0.6 of the 63 recoveries are expected by chance. score_p2.py's 200 shifted-catalogue draws give mean 0.0095 and max 0.068. The 400 shifted-catalogue controls in results/null_test.md (PREREG.v6) give best 0.0484 against a real 0.9403.

## Pre-registration (readings and thresholds before scored data)

- File times cannot settle the order. Every file in prereg/ has the same mtime, 2026-11-12 21:05:36Z, which is the time the package was copied, not when the files were written. Only the timestamps inside the files are available.
- Internal timestamps: PREREG.md was frozen at 18:50:58Z, before any 1971 waveform was read. It fixes R1-R3 (the readings in CLAIM.md are verbatim from it) and the p2 bar ">= 0.90 R2-primary". PREREG.v2.md was frozen at 19:18:57Z, before any 1971 waveform was opened. It fixes the band, whitening, L = 450 s, S12 MH1/MH2/MHZ, theta = 0.10897762490606308 and the template sha256. PREREG.v6.md (19:28:36Z) was written after a code test on the first 30 scanned 1971 days, which it discloses. It only adds the shifted-catalogue null test and changes no reading, threshold or design. The timeline is coherent: the scout fetch was at 18:42Z, 365 days at about 15-20 s each runs from about 19:20Z to 21:00Z, and the package was copied at 21:04Z.
- Independent support that theta and the templates did not come from 1971: I re-ran code/scripts/dev_eval.py (0.25 1.0 450 0.1 s12) on the 1972 dev days alone. It reproduces the frozen templates, the 21 members, the LOO values and theta bit for bit (max |difference| 0). No dev window reaches a 1971 day; the earliest dev event is 1972-013. frozen/A1_s12_dev1972_templates.npz has the sha256 that PREREG.v2.md records (4b079480...).
- Code drift, not disclosed. Four files in the claim do not match the "Frozen code (sha256)" list in PREREG.v2.md: code/tools/apollo_lib.py, code/scripts/score_scan.py, code/scripts/score_p2.py and code/scripts/candidates.py. The other five tools match. The visible differences are path lines (the APOLLO_WF environment variable and relative paths). The mtimes fit packaging-time path edits: these files carry 21:04:54Z, after the results were copied at 21:04:25Z. PREREG.v2.md requires any change to the frozen code to be listed, and CLAIM.md does not list this one. It changes no scored number. The edited code reproduces the saved scan exactly for all 365 days (forward peaks, reversed peaks, coverage; max |dD| = 0) and reproduces results/p2.json, results/p2.md and results/null_test.md byte for byte. This should be disclosed before filing, but it does not change the verdict.
- Packaging gap: the run folder holds PREREG.v3, v4, v5 and v7, which are not in claim/prereg/. Within my scope I did not read them. The p2 numbers depend only on the readings in PREREG.md and the threshold and templates frozen in PREREG.v2.md, all verified above. The package should include every prereg version, or say why some are left out.

## Do the claim's numbers follow from results/?

Yes. In my scratch folder, with one FFT worker:
- score_p2.py on results/scan_s12_A1_1971.jsonl gives output identical to results/p2.json and results/p2.md: 63/67, theta 0.10898, 400 reversed detections, 334.544 day-equivalents, 1.1957 per day, p2_met true.
- p2_null.py gives output identical to results/null_test.md.
- My own recount from the raw scan, without their scoring script, gives 63/67 again.
- score_scan.py with 0 controls reproduces the saved scan for all 365 days.
- Small errors: PREREG.md says 52 dev days, but 49 of them hold events (the 46.9 scanned day-equivalents match the 49). The command line in results/null_test.md cites paths outside the package (attempts/...). Both are cosmetic.

## Baseline record

baseline/README.md says no published baseline applies and none was reproduced. That fits the claim: p2 is an absolute bar (>= 90% with a measured false-alarm rate), and the claim reports no comparison with any baseline, so there is no data, split or metric to mismatch. Bulow et al. (2005) template-matched A1, but the bank's p2 asks for a saved, re-runnable recovery package, and an older method does not subsume that. This is the first claim on this target, and the package's repo PR search found no earlier one. Novelty is the novelty skeptic's question.

## Verdict

p2 is met literally and robustly. 63/67 = 0.940 is at least 0.90 at the frozen theta, and stays at or above 0.90 under every stricter fair reading I tried (threshold above the reversed-null maximum; narrow onset window; visual-catalogue subset). The false-alarm rate is measured on the bank's own time-reversed null. The detector was fixed on 1972 data alone, and the whole chain from waveforms to the p2 numbers re-runs exactly. Before filing, CLAIM.md should disclose the frozen-code hash mismatch (path-only, no effect on numbers) and the prereg versions left out of the package. Neither changes a scored number.

confirmed_scope: With templates and threshold (theta = 0.10898) fixed on 1972 data alone, the saved three-component S12 long-period template detector re-runs to recover 63 of the 67 nest-A1 deep moonquakes catalogued for 1971 in levent.1008weber.csv (94.0%, detection onset within +/- 5 min of the catalogued start), at a measured false-alarm rate of 1.196 declustered detections per scanned day on the time-reversed 1971 data (400 over 334.54 scanned day-equivalents).

pass: true
