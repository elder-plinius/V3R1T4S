# NOVELTY review: claim/ (three XHSTT-2014 solutions)
context: fresh subagent started for this claim only

Reviewer work folder: panel/work-novelty/ (fetch/, dl/, lit/, scripts/). Nothing under claim/ was modified. HSEval, KHE and other binaries were not run. No contact, posting or GitHub write action was made.

Costs are written (infeasibility, objective) and compared hierarchically: lower infeasibility first, then lower objective.

## 1. Re-fetch of the status sources (2026-11-28, UTC)

Each URL was fetched once with a generic user agent, at 09:06:39Z to 09:06:43Z. The sha256 values were compared with claim/data/fetch.json (frozen 08:57:12Z).

| file | URL | HTTP | time (UTC) | sha256 vs frozen |
|---|---|---|---|---|
| overview.html | https://www.utwente.nl/en/eemcs/dmmp/hstt/archives/XHSTT-2014/overview.html | 200 | 09:06:40Z | b3f6718b... identical |
| AU-BG-98 page | https://www.utwente.nl/en/eemcs/dmmp/hstt/datasets/Australia/BGHS98/ | 200 | 09:06:40Z | 201ae2e4... identical |
| DK-HG-12 page | https://www.utwente.nl/en/eemcs/dmmp/hstt/datasets/Denmark/HasserisGymnasium2012/ | 200 | 09:06:40Z | c4e74c4b... identical |
| DK-VG-09 page | https://www.utwente.nl/en/eemcs/dmmp/hstt/datasets/Denmark/VejenGymnasium2009/ | 200 | 09:06:40Z | d33bbaec... identical |
| AustraliaBGHS98.xml | .../datasets/Australia/BGHS98/AustraliaBGHS98.xml | 200 | 09:06:41Z | b172c3db... identical |
| DenmarkHasserisGymnasium2012.xml | .../HasserisGymnasium2012/DenmarkHasserisGymnasium2012.xml | 200 | 09:06:42Z | 9abb1e9b... identical |
| DenmarkVejenGymnasium2009.xml | .../VejenGymnasium2009/DenmarkVejenGymnasium2009.xml | 200 | 09:06:43Z | 6970f763... identical |
| target_live.md | raw.githubusercontent.com/elder-plinius/V3R1T4S/main/known-unknowns/optimization-benchmarks/xhstt-2014-high-school-timetabling-bks.md | 200 | 09:19:55Z | 5404776a... identical (last commit f3b19b4750, 2026-10-30) |

All 8 files are byte-identical to the frozen copies.

**Live values (quoted from the re-fetched pages):**

- **Overview** (page footer "Last update 11 Nov 2026"). Columns: Best, LB, Last best date.
  - AU-BG-98: 126, 0.0, April 17, 2017
  - DK-HG-12: 12.2330, 7.0, April 17, 2017
  - DK-VG-09: 2.2323, 2.0, April 17, 2017
- **Dataset pages.**
  - AU-BG-98: the best stored group is "GOAL team - Dec 8, 2016", 0 / 128, received April 17, 2017.
  - DK-HG-12: the best is "GOAL team Dec 8 2016", 12 / 2330, received April 17, 2017. The page gives LB 7.0.
  - DK-VG-09: the best is "GOAL team Dec 8 2016", 2 / 2323, with LB (2,0).
  - No stored value on any of the three pages is at or below ours: (0, 91), (12, 2326), (2, 2322).
- **Rows that changed elsewhere on the overview.** Some rows have moved since the bank target was written: DK-FG-12 is 1020, NL-KP-03 102, NL-KP-05 399 and NL-KP-09 665, all dated October 28, 2026. UK-SP-06 is 2.802 (October 6, 2026). ES-SS-08 is now 335/335, so it is closed. None of these changes touches the three claimed rows, which are still dated April 17, 2017.

**Other archive pages checked:**

- **HSTT home page and news** (https://www.utwente.nl/en/eemcs/dmmp/hstt/). The newest items, from 2026-10-06, are Chernikov (DK-FG-12, Kottenpark2003/2005/2009), Dudek (All11, All15, Kottenpark2008, StPaul, SpainSchool LB) and Brazil Instance7. None of them is for AU-BG-98, DK-HG-12 or DK-VG-09.
- **Older news page** ("old news.html"). The last item that touches these instances is "July 21, 2017. George Fonseca submitted ... 9 new best solutions to instances of XHSTT-2014 along with 3 new lowerbounds". The page also notes the March 4, 2016 change to the Australian instances.
- **Archives index.** ALL_INSTANCES is "Version: November 16, 2022".
- **ALL_INSTANCES.zip** (HTTP 200, sha256 1d55957f...). Its three files are byte-identical to claim/data/inst/ (same sha256 as above), so there is no hidden newer solution group.
- **GOAL-UFOP_2016-12-08.zip**, the research solution group on the XHSTT-2014 page (sha256 acc58411...). Its own Report elements give AU-BG-98 0 / 126, DK-HG-12 12 / 2330 and DK-VG-09 2 / 2323.
  - This explains the overview's 126 against the page's 128: 126 is the team's self-reported value.
  - The claim's evaluator scores that same AU-BG-98 solution at (0, 128), the archive's value.
  - Either way, 91 is below both.
- **Sequence-basedHH.zip** (Kheiri and Keedwell). It gives 0.520 on AU-BG-98 (an older instance version), 12.2628 on DK-HG-12 and 2.2731 on DK-VG-09. All are above ours.
- **XHSTT-2014.zip** holds instances only (dated 2016-03-04).
- **Lower bounds.** The LBs (AU-BG-98 0, DK-HG-12 7.0, DK-VG-09 (2,0)) are all at or below ours, so nothing contradicts the claimed costs.

## 2. Literature and code search

Each source is listed with what it says about these three instances, compared hierarchically with ours: AU-BG-98 (0, 91), DK-HG-12 (12, 2326), DK-VG-09 (2, 2322).

- **Fonseca, Santos, Carrano, Stidsen, "Integer programming techniques for educational timetabling", EJOR 262(1) 28-39, 2017, doi 10.1016/j.ejor.2017.03.020.** Read in full (DTU preprint, backend.orbit.dtu.dk/ws/files/138357287/elsarticle_template_num.pdf, sha256 cb20d82d...).
  - Table 5, "New best known lower (LB) and upper (UB) bounds obtained using the new formulation F2", columns LB, UB, New LB, New UB:
    - AU-BG-98: 0 / 415 / 0 / **129**
    - DK-HG-12: (7, 0) / (12, 2611) / (7, 0) / **(12, 2356)**
    - DK-VG-09: (0, 0) / (2, 2718) / (2, 0) / **(2, 2329)**
  - All three are above ours. This paper is the source of the Dec 2016 solutions. The archived values 128 (self-reported 126), 12.2330 and 2.2323 are lower than the paper's, and ours are lower still.
- **Fonseca, Santos, Carrano, "Integrating matheuristics and metaheuristics for timetabling", COR 2016, doi 10.1016/j.cor.2016.04.016.** Full text NOT read: ScienceDirect, ResearchGate and CORE all returned 403.
  - Indirect evidence: its experiments predate the EJOR 2017 paper. The EJOR "UB" column (the best known before EJOR, i.e. GOAL's 2015 values) is 415, (12, 2611) and (2, 2718). A search-engine excerpt also quotes (12, 3124) and (12, 2611) for DK-HG-12 from this paper.
  - Nothing suggests a value at or below ours.
- **Ceschia, Di Gaspero, Schaerf, "Educational Timetabling: Problems, Benchmarks, and State-of-the-Art Results", arXiv 2201.07525 (2022).** Read; Table 15, "Results on the XHSTT-2014 benchmarks".
  - It compiles Demirović-Musliu 2017, Demirović-Stuckey 2018, Teixeira et al. 2018, Fonseca et al. 2017 and Kheiri-Keedwell 2017.
  - AU-BG-98: (3, 514), 493, LB 0, UB 128. DK-HG-12: (12, 2356), (12, 2628), LB 7, UB (12, 2330). DK-VG-09: (2, 2329), (2, 2720), LB (2, 0), UB (2, 2323).
  - Nothing is at or below ours.
- **Kheiri and Keedwell, "A Hidden Markov Model approach ... high school timetabling", Evolutionary Computation 25(3), 2017.** Read (EVCO2016.pdf); SSHH avg/best and SSHH-L avg/best tables.
  - Australia-BGHS98: best 0,520 / 0,493. Hasseris: best 12,2628 / 12,2641. Vejen: best 2,2731 / 2,2720.
  - All above ours.
- **Kristiansen, Sørensen, Stidsen, "Integer programming for the generalized high school timetabling problem", J. Scheduling 18(4) 2015.** Read (DTU preprint); Table 3, older pre-2014 instance versions.
  - BGHS98 (3, 494); Hasseris2012 (293, 32111); Vejen2009 (20, 18966), with LB (2, -).
  - Far above ours; no alternative-formulation run on these instances.
- **Demirović and Musliu, "MaxSAT-based large neighborhood search for high school timetabling", COR 78, 2017.** Read (author PDF). Tables 1-3 do not include AU-BG-98, DK-HG-12 or DK-VG-09: they model 27 of 39 instances, and these three are not among them. No values.
- **Demirović PhD thesis "SAT-based approaches for the general high school timetabling problem"** (TU Wien, dbai.tuwien.ac.at/staff/musliu/emird.pdf). Read (text search). It does not report these three instances.
- **Demirović and Stuckey, CPAIOR 2018 (CP scheduling-based model with hot starts).** Full text NOT read (paywalled). The survey's Table 15 carries its average, (3, 514), on AU-BG-98 and nothing for the Danish rows.
- **Teixeira et al. 2018 (adaptive VNS / skewed GVNS, ICVNS).** Not read; the survey shows no values for these three rows.
- **Kingston, KHE14 (PATAT 2014 paper, khe14.pdf).** Read.
  - AU-BG-98: 12.00764, 13.00520 and 4.00752 ... DK-HG-12: 13.05467, 14.05094, 12.03956 ... DK-VG-09: 2.04393, 3.04433, 7.07526 ...
  - All above ours.
- **KHE home page.** Posted solutions are AU-BG-98 3.00400 / 3.00311 / 2.00340 / 1.00386, DK-HG-12 12.03124 and DK-VG-09 2.04097. All above ours.
- **KHE User's Guide 2026_11_15** (857 pages, read by text search). It mentions AU-BG-98 and BGHS98 only in run-time remarks, with no cost tables.
- **Kingston's tt_papers page.** His papers since 2018 are on nurse rostering. No new high-school results.
- **ITC2011 results (ResultsITC2011.pdf, utwente).** BGHS98 only, old version: (7,433), (3,494). Hasseris and Vejen are not in ITC2011. Above ours.
- **Krystallidis and Ruiz-Torrubiano, arXiv 2407.16898 (2024), "Introducing Individuality into Students' High School Timetables".** Read (arXiv HTML). The paper extends XHSTT and runs on German instances; it reports no values on these three.
  - A search-engine summary attributed "new best known solutions in 9 cases" to this paper. That statement is not in its text; the wording matches the EJOR 2017 abstract.
- **ter Braak, MSc thesis (Twente).** Read by text search; no values on these instances.
- **PUC-Rio thesis 27073 and WUR edepot 637835** (returned by searches). Read by text search; no mention of these instances.
- **GitHub.**
  - Repository search "XHSTT" and "high school timetabling", plus code search for HasserisGymnasium2012, BGHS98, VejenGymnasium2009 and DK-HG-12.
  - patromi/School-Timetabling-Problem-Solver (2026) runs on AU-BG-98. Its results are hard-infeasible, e.g. (72397, 3021) after 600 s and a best cost of 36049002330 in its 500k-iteration log. Far above ours.
  - IMC-UAS-Krems/modularXHSTT holds only artificially modified BGHS98 variants. biwecka/gax holds instance copies only.
  - georgehgfonseca/itcgoal (pushed 2015) and georgehgfonseca/SATTimetabling (a 2011 SBPO project) contain no solution files for these instances.
  - No GitHub file has a cost at or below ours.
- **Chernikov (Alrevion) and Dudek.** Only the HSTT news items were found (other instances). No paper, repository or value on these three.
- **General web searches** covered XHSTT-2014 new best 2019-2026, CP-SAT/LNS XHSTT 2025-2026, Hasseris, Vejen and BGHS98. They found nothing newer than the archive for these rows.

**Not read in full:**

- Fonseca et al. COR 2016 (403 everywhere; covered indirectly by EJOR 2017 Table 5 and the archive history).
- Demirović-Stuckey CPAIOR 2018 (paywalled; survey value only).
- Teixeira et al. 2018.
- Fonseca's PhD thesis (UFOP; not located online).
- Sørensen and Dahms, COR 2014 (Danish instances, pre-2014 versions; not fetched).
- Tan et al. 2021 survey (not fetched).
- Saviniec's USP thesis 2018 (not fetched).

Each of these predates the archive's April 2017 values or is summarised by the 2022 survey. None is known to report a value below the archive.

## 3. Trivial-edit check (object vs the stored record)

Scripts: panel/work-novelty/scripts/diff_solutions.py, detail.py and overlap.py. They use read_solution/evaluate from claim/code/xhstt_eval.py, read-only. Each object was compared with every stored solution group in claim/data/inst/{instance}.xml and with the GOAL-UFOP research zip copy, which evaluates identically to the stored record.

| instance | object cost | events | identical events vs record | differ in time only / resources only / both | free events at same time as record | baseline: record vs previous GOAL solution | relabelling test |
|---|---|---|---|---|---|---|---|
| AU-BG-98 | (0, 91) | 387 | 37 | 57 / 43 / 250 (22 with changed splits) | 60 / 367 | 278 / 367 | no consistent time map (781 conflicts) or resource map (381 conflicts); 199 of 346 free teacher and 263 of 320 free room assignments differ |
| DK-HG-12 | (12, 2326) | 1235 | 134 | 50 / 698 / 353 | 832 / 1235 | 335 / 1235 | no consistent time map (471 conflicts) or room map (1092 conflicts); 1051 of 1235 room assignments differ |
| DK-VG-09 | (2, 2322) | 918 | 8 | 27 / 164 / 719 | 172 / 918 | 125 / 918 | no consistent time map (773 conflicts) or room map (854 conflicts); 883 of 918 room assignments differ |

**Findings:**

- No object is a copy, a relabelling (time, day or resource permutation) or a symmetry image of any stored solution.
- AU-BG-98 and DK-VG-09 are far from the record: 84% and 81% of free events are at different times.
- DK-HG-12 shares 832 of 1235 event times (67%) with the GOAL record. Two independent GOAL solutions share only 335 (27%). This object is therefore very likely seeded from, or converged near, the GOAL Dec 2016 record. It still re-times 403 events and reassigns 1051 rooms, and no relabelling explains it, so it is not a trivial edit.
- provenance/README.md does not state the seed. Under the kit's rule ("one seeded from a published object must name it"), the write-up should name the GOAL record as the probable seed of DK-HG-12 and say whether AU-BG-98 and DK-VG-09 were started from it too.
  - I did not read attempts/ (outside my remit), so the seeding itself is not verified here.
  - This is a disclosure item, not a novelty failure.

## 4. V3R1T4S check (read-only gh)

Done at 2026-11-28T09:20Z. Searched PRs and issues of elder-plinius/V3R1T4S for xhstt, XHSTT, timetabling, "high school", AU-BG-98, DK-HG-12, DK-VG-09, Hasseris, BGHS98 and Vejen. Also listed all 1211 PRs and 55 issues and filtered titles and branches for xhstt, hstt, school and timetabl.

- The only hits are the ITC2007 (#1094, #1092), TimPassLib (#1122) and ITC2021 (#1257, #1258) claims. None is an XHSTT claim.
- Code search for "xhstt" in the repo finds only the bank target file and the optimization-benchmarks README.
- TROPHY_CASE.md has no XHSTT or timetabling entry, and known-knowns/ has no XHSTT folder.
- The newest PR is #1266 (2026-11-28T05:46Z, unrelated).

No earlier or competing V3R1T4S claim exists.

## 5. Verdict per row

| instance | best published or posted value found | ours | verdict |
|---|---|---|---|
| AU-BG-98 | (0, 126), the GOAL self-report on the overview. The page has (0, 128). Paper values: EJOR 2017 129, Kheiri-Keedwell 493 | (0, 91) | new: pass |
| DK-HG-12 | (12, 2330), archive (GOAL Dec 2016). Paper values: EJOR 2017 (12, 2356), Kheiri-Keedwell (12, 2628) | (12, 2326) | new: pass (disclose the probable seeding from the GOAL record, 67% of event times shared) |
| DK-VG-09 | (2, 2323), archive (GOAL Dec 2016). Paper values: EJOR 2017 (2, 2329), Kheiri-Keedwell (2, 2720) | (2, 2322) | new: pass (margin of 1 objective unit; infeasibility 2 equals the LB) |

No published or posted value is at or below ours on any row, and no object is a trivial edit of a published solution.

pass: true
