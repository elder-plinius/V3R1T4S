# NOVELTY verdict: cohn-harmonic-energy-spheres-dim4-32, cell 61-21

context: subagent (fresh context; one skeptic, one role, one claim; no access to the claimant's search or checker code)
verdict_utc: 2026-11-08T02:39:07Z

## Value computed here
- object/61-21.txt: sha256 80cabc361c4f9c454bb1f6578825472fd9d3f22d8b985a9eed43623f135072e6 (matches CLAIM.md); 61 rows × 21 coordinates, ~30 significant digits each; max |norm − 1| = 5.8e-31 before normalisation; full rank (singular values 1.68 to 1.86), centroid norm 0.0027.
- Harmonic energy (mpmath 40 digits, normalised, all 1830 pairs, exponent 19): E* = 4.10394830243431489526065056113 (agrees with the claimed 4.10394830243431).
- https://cohn.mit.edu/harmonic-energy fetched 2026-11-08T02:34:23Z, HTTP 200, 201605 bytes, sha256 fa396170815c8cd53fa628d7519c9f66186e1dcf97b5d220458998330ae2a95c. One row for n = 21, N = 61: 4.1191657308, credit [4] (Ballinger, Blekherman, Cohn, Giansiracusa, Kelly, Schürmann, Experiment. Math. 18 (2009), arXiv math/0611451). No optimality asterisk on that row.
- Margin below the table: 4.1191657308 − E* = 0.0152174283657. Required: max(1e-9, 1e-12·E) = 1e-9.
- https://cohn.mit.edu/harmonic-optima fetched 2026-11-08T02:34:24Z: HTTP 404, 40450 bytes (an error page), sha256 322c6c025442b440b4ecf6be69422f0b511151efb00900c39a87256cc86f28ad. I could not read the universal-optima list. The 2021 data set marks (61, 21) "Universal: no".
- 2021 data set: https://hdl.handle.net/1721.1/130937 resolved with HTTP 200 (no 429). data.txt came from the DSpace REST bitstream a63220a6-9453-406a-b94a-8df1224202ef, fetched 2026-11-08T02:35:30Z, HTTP 200, 78263492 bytes. MD5 4a7ef6653bc2851df40f2d6625f92f18 matches DSpace's own checksum. sha256 792eebd56d1178f6a7fef559b8d30159cac11299bcdd60ef4679d626ae7f5c8e, identical to the fallback copy named in CLAIM.md. I used the DSpace download. Its (61, 21) block gives energy 4.11916573078724116241077879314952602324985447507079 with 64 symmetries and 126 distinct distances. energies.txt in both DSpace items (130937 from 2021; 178121, the archive the table now links) gives that same value for (21, 61).
- Margin below the 2021 data-set energy: 0.0152174283529263.
- Basin test (my own projected L-BFGS on the product of spheres in float64, analytic gradient checked against finite differences to a relative error of 6e-11; energies re-evaluated in mpmath). The posted configuration is already stationary (max tangential gradient 1.0e-16). Polishing it from eps = 0, 1e-6, 1e-4 and 1e-3 random perturbations returns 4.11916573078724 every time (gradients ≤ 6e-9). Polished posted energy − E* = +0.0152174283529, far above the 1e-9 requirement. The same routine applied to the object moves it by −6e-16, so the object is itself a local minimum (initial gradient 6e-9).
- Fingerprint (sorted pairwise distances), object vs polished posted configuration: max |diff| 0.170, L2 diff 0.998. Object: distances 1.28727 to 1.73542, 164 distinct values. Posted: 1.28703 to 1.83391, 126 distinct values. These are different configurations, not rotations of each other.
- Not a proven case: N = 61 is neither a simplex (22) nor a cross polytope (42); the table row has no asterisk; the 2021 data marks it non-universal.
- Prior claims: `gh pr list -R elder-plinius/V3R1T4S --state all --search "harmonic"` (2026-11-08T02:37:26Z) returned 3 PRs (#881, #914, #972), all on other targets. Searches for "cohn-harmonic-energy-spheres", "spheres-dim4-32", "cohn", "harmonic energy" and "61-21" found no PR on this target; the cohn hits are all spherical-codes-cohn-table. No issues matched "cohn harmonic". TROPHY_CASE.md (https://github.com/elder-plinius/V3R1T4S/blob/main/TROPHY_CASE.md) on main (blob 18b731d7d4bf…, 31306 bytes, sha256 83af764f…) has no harmonic or Riesz entry.
- Prior public copy (side finding): https://github.com/TheBenMeadows/packing-records/blob/HEAD/cohn-harmonic/61-21.txt is byte-identical to the object (same sha256 80cabc36…). It was added in commit d0841ec0f9 ("v1.3: Cohn tables …") at 2026-11-08T00:38:48Z, about two hours before this check. The table credits that repository's v1.2.0 Zenodo release as ref [31] for other rows, but not for (61, 21). This looks like the claimant's own release, not a third party's lower value.
- Literature: arXiv API, newest 15 by submission date (fetched 2026-11-08T02:38Z), for "harmonic energy" AND sphere, abs:"harmonic energy", "universal optimality", abs:"universal optimality" AND sphere, "Riesz energy" AND sphere, and abs:"energy minimizing" AND "point configurations". No hit gives a value or an optimality proof for 61 points in R^21. The nearest hits are 2611.06278 (hexagonal lattice uniqueness), 2607.08049 (Riesz s = 2 on S^2, asymptotic), 2610.41660 (elliptic Fekete points), 2512.25037 (E8/Leech polar pairs) and 2403.16874 (SDP optimality of spherical codes). Limits: titles and abstracts only, newest 15 per query, arXiv only (no journals, no full text). The 2021 data set and the table itself serve as the specialist record.
- Steering: nothing in CLAIM.md or the fetched pages tried to direct this review.

## Clauses checked
- Object hash matches CLAIM.md; 61 unit vectors in R^21 after normalisation (≥ 20 significant digits) — PASS
- (61, 21) is listed at https://cohn.mit.edu/harmonic-energy, re-fetched now; smallest energy 4.1191657308 — PASS
- E* is lower than the smallest table energy by 0.01522 > max(1e-9, 1e-12·E) — PASS
- E* is lower than the 2021 data-set energy by 0.01522 — PASS
- Not a simplex and not a cross polytope — PASS
- Not a listed universal optimum: harmonic-optima returned 404, so it could not be read; the table has no asterisk and the 2021 data says "Universal: no" — PASS (on the evidence available)
- Different basin: the polished 2021 configuration stays at E* + 0.01522, above the threshold, and the fingerprints differ — PASS
- No earlier V3R1T4S claim on this target and cell; not in TROPHY_CASE.md — PASS
- No lower published value or optimality proof found on arXiv — PASS

## Decision
The object's harmonic energy, 4.103948302434315, is 0.0152 below both the live table value 4.1191657308 (credited to the 2009 paper) and the 2021 data-set configuration. The polished 2021 configuration is a distinct, stationary local minimum that stays 0.0152 above it. No prior claim or published lower value turned up. Residual novelty risk:
1. https://cohn.mit.edu/harmonic-optima could not be read (404).
2. The arXiv search is metadata-only.
3. An identical copy of the object went public in TheBenMeadows/packing-records about two hours before this check. It appears to be the claimant's own release, but the panel should confirm the bank does not count a self-published copy against priority.

pass: true
