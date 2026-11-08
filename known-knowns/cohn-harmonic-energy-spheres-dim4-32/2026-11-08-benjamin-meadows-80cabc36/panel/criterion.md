# CRITERION verdict: cohn-harmonic-energy-spheres-dim4-32, cell 61-21

context: subagent (fresh context; one skeptic, one role, one claim; no access to the claimant's search or checker code)
verdict_utc: 2026-11-08T02:41:42Z

## Value computed here
- object/61-21.txt: sha256 80cabc361c4f9c454bb1f6578825472fd9d3f22d8b985a9eed43623f135072e6 (matches CLAIM.md). 61 rows x 21 comma-separated coordinates, one `#` header line. Coordinates carry 27 to 30 significant digits; max |norm - 1| before normalisation is 5.8e-31.
- E* (mpmath, dps 40, each row normalised in mpmath, s = n - 2 = 19) = 4.103948302434314895260650561126879053670. This agrees with the claimed 4.10394830243431 (the object header agrees to about 2.5e-30). Minimum pairwise distance is 1.28726854123, so there are no coincident points.
- Threshold max(1e-9, 1e-12 E*) = 1.0e-9.
- https://cohn.mit.edu/harmonic-energy: GET 2026-11-08T02:35:14Z, HTTP 200, sha256 fa396170815c8cd53fa628d7519c9f66186e1dcf97b5d220458998330ae2a95c. It has exactly one row for (n, N) = (21, 61): 4.1191657308, ref [4], no asterisk. Asterisked rows for n = 21 are N = 22, 42, 112 and 162 only.
- https://cohn.mit.edu/harmonic-optima: GET 2026-11-08T02:35:14Z, HTTP 404 (sha256 322c6c02…f28ad, a "not found" page). https://cohn.mit.edu/data/ (HTTP 200, sha256 c229f475…988d) no longer links to it. Wayback lookups failed: archive.org returned 429 and the CDX endpoint returned 504.
- 2021 data set https://hdl.handle.net/1721.1/130937: the handle page returned HTTP 200 at 2026-11-08T02:35:23Z. The DSpace REST bundle listing (HTTP 200) gives data.txt as 78263492 bytes with MD5 4a7ef6653bc2851df40f2d6625f92f18. The direct bitstream GET at 2026-11-08T02:35:56Z returned HTTP 429. I therefore used the copy named in CLAIM.md. Its sha256 is 792eebd56d1178f6a7fef559b8d30159cac11299bcdd60ef4679d626ae7f5c8e, as stated, and its MD5 4a7ef6653bc2851df40f2d6625f92f18 and size 78263492 match the values DSpace itself publishes, so the copy is byte-identical to the archived file.
- Data-set block "61 points in R^21": header energy 4.11916573078724116241…, Universal: no, Design: 0, Distances: 126 of 1830. 64-digit coordinates. My mpmath dps-40 energy is 4.119165730787241162410778793149526023, which matches the header. My count of distinct inner products is 126, which matches the header. The polished claim has 168 distinct inner products, so its distance pattern differs from the data-set configuration.
- Polishing (L-BFGS-B on the radial projection, float64, gtol 1e-13, then energy re-evaluated in mpmath at dps 40):
  - Data set: 0 iterations, |grad| 3.5e-15, E = 4.119165730787241162….
  - Claim: 2 iterations, |grad| 3.0e-8, E = 4.103948302434314252.
  - Eight further restarts of the data-set configuration, perturbed by Gaussian noise at 1e-6, 1e-4, 1e-3 and 1e-2, all returned to 4.11916573078724 (±1e-14).
- arXiv (GET, all HTTP 200 unless noted):
  - export API at 2026-11-08T02:38:35–49Z: "harmonic energy" AND sphere (5 hits); "universal optimality" (60 most recent); "universally optimal" AND sphere (10); "Riesz energy" AND sphere AND dimensional (7). A fifth API query and the follow-up abstract fetches got HTTP 429.
  - arxiv.org/search at 2026-11-08T02:40:36–41:03Z: "harmonic energy" spheres (4); "minimizing harmonic energy" (0); "energy-minimizing point configurations" (1: math/0611451); "universally optimal" spherical (15); "Riesz energy" "high dimensions" (0).
  - Abstracts read: 2403.16874 (new optimal codes 56/20, 50/21, 77/21, Kerdock codes, universal optimality of 288 points in R^16) and 2512.25037 (universal polar dual pairs in E8/Leech, 1408 lines in RP^21).
  - None of these concerns 61 points in R^21, and none reports a harmonic energy for (61, 21).
- Cohn and Kumar, arXiv math/0607446v2 (GET 2026-11-08T02:41:15Z, HTTP 200, sha256 b0d9edd5…f289). Table 1 lists the known sharp configurations. In n = 21 these are 22 and 42 (from the general rows), 162 (kissing), and 112 (isotropic subspaces, q = 3). N = 61 is not listed.
- V3R1T4S prior claims: TROPHY_CASE.md on main (HTTP 200, sha256 83af764f…6113) has no harmonic or Cohn entry. A GitHub PR search for "cohn-harmonic-energy-spheres" returned 0 results, and a search for "harmonic" returned 3 unrelated PRs.
- No steering text found in claim/.

## Clauses checked
- Clause (a): n in 4..32 and >= 20 significant digits. **PASS.** n = 21; every coordinate has at least 27 significant digits; 61 x 21 entries.
- Clause (b): (N, n) is listed at https://cohn.mit.edu/harmonic-energy, re-fetched before judging. **PASS.** Row "21 61 4.1191657308 [4]" is present in the 2026-11-08T02:35:14Z fetch, and it is the only row for this pair.
- Clause (c): E* is strictly below the smallest table energy by at least max(1e-9, 1e-12 E). **PASS.** 4.1191657308 - 4.103948302434314895 = 0.0152174283657, against a threshold of 1.0e-9. The table value is rounded to 10 decimals, which shifts the gap by at most 5e-11. Against the data set's exact 4.119165730787241, the gap is 0.0152174283529.
- Clause (d1): not a simplex (N = n + 1 = 22). **PASS.** N = 61.
- Clause (d2): not a cross polytope (N = 2n = 42). **PASS.** N = 61.
- Clause (d3): not a universal optimum on https://cohn.mit.edu/harmonic-optima. **NOT CHECKABLE AS NAMED** (HTTP 404, no archive reachable). I consider it settled by the other evidence. The live harmonic-energy table marks known optima with an asterisk, and (21, 61) has none, while 22, 42, 112 and 162 do. Cohn–Kumar Table 1 has no 61-point code in R^21. The data set records "Universal: no" and "Design: 0" for this cell. A universally optimal code must be a spherical design, and the claimed energy beats the table value, so that configuration was not optimal in any case.
- Clause (d4): not proven optimal for harmonic energy in any paper found in an arXiv check. **PASS.** The searches listed above found no optimality proof for 61 points in R^21. The new optimality results for R^21 (2403.16874) are for 50 and 77 points, as optimal codes.
- Clause (e): different basin: polishing the data-set coordinates stays above E* + max(1e-9, 1e-12 E). **PASS.**
  - Source: the 2021 data set via the CLAIM.md copy, verified against the DSpace MD5.
  - Polished data-set E = 4.119165730787241, which exceeds E* + 1e-9 by 0.0152174273529.
  - It stays there under eight perturbed restarts.
  - The polished claim stays at 4.103948302434314; the two configurations have 168 vs 126 distinct inner products.
- Clause (f): no lower published value found in an arXiv search. **PASS.**
  - No arXiv hit gives a (61, 21) harmonic energy, at or below E*.
  - The table cites [4], whose value of 4.1191657308 is higher.
  - There are no prior V3R1T4S claims for this target.
  - Caveat: arXiv's API rate-limited part of the search (HTTP 429), so coverage came from the arxiv.org/search front end instead.
- Where my procedure differs from the bank's checker:
  - My polish is float64 L-BFGS followed by an mpmath energy re-evaluation; I did not run an mpmath Newton step. Both configurations are already critical points: |grad| is 3.5e-15 for the data set and 3e-8 for the claim, and the claim's energy moved by less than 1e-15 when polished. A Newton step cannot close a 0.015 gap.
  - I added perturbed restarts of the data-set configuration, which the bank's method does not do.
  - The harmonic-optima check used substitute sources, because the page returns 404.

## Decision
Every clause I could compute passes by a wide margin. E* = 4.1039483024343148953 is 0.01522 below the only table entry for (61, 21), which is seven orders of magnitude above the 1e-9 threshold. The 2021 data-set configuration, verified byte-identical to the DSpace file by its MD5, is a stable local minimum at 4.1191657308, in a different basin. The only unverifiable source is the harmonic-optima page (HTTP 404). The live table's optimality asterisks, Cohn–Kumar Table 1, and the data set's "Universal: no" together settle that clause.

pass: true
