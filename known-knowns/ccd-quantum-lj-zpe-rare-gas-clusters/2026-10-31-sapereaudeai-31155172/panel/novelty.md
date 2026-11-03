# Novelty skeptic: ccd-quantum-lj-zpe-rare-gas-clusters, N = 38, Ne (q = 0.095)

context: subagent (Claude Code Agent tool, fresh context)
injection_suspected: none (I saw no instructions in any page or claim file)

Claimed value (claim/CLAIM.md): E_Ne = E_LJ + (0.095/2) sum sqrt(lambda_i) = -108.929936 for `object/N38_Ne.xyz`.
Paths below are relative to claim/; my own work files are in `../panel/novelty_work/` and `../panel/novelty_scripts/`.

## 1. Status fetch (one request, no retries)

- URL: https://www-wales.ch.cam.ac.uk/~florent/LJZPE/table.html
- Time: curl started 2026-10-31T19:37:09Z (`date -u`), server `Date: Sat, 31 Oct 2026 19:37:11 GMT`
- Result: HTTP 200, 27710 bytes, sha256 5e8632e8ab257910961ae596019c6a7fa9335c68e4d7c08e8552f0fb1751177b,
  Last-Modified Mon, 26 Feb 2018. The file is byte-identical to `data/table.html`.
- N = 38 rows as I read them: 38A (Oh) Ne -106.47765; 38B (C1) Ne **-107.42431** (underlined as the Ne global minimum).
- **Lowest tabulated Ne value for N = 38: -107.42431.** The claim's value is 1.505626 below it, which clears the 5e-4 margin.
- Files: `../panel/novelty_work/table.html`, `table_headers.txt`, `fetch_time_start.txt`.

## 2. My own check of the object (needed for the novelty comparison)

I ran an independent numpy evaluator with no polish of the object (`../panel/novelty_scripts/analyse.py`). Results:
E_LJ = -168.984987, |grad| = 1.9e-13, 6 zero modes (|lambda| < 1.1e-13), lowest nonzero eigenvalue 0.810,
sum sqrt(lambda) = 1264.316866, E_Ne = -108.929936. These agree with the claim.
For comparison, the same code on the posted table files (Newton-polished) gives 38A E_Ne -106.477643 and
38B E_Ne -107.424316.

## 3. Published harmonic (classical minimum + harmonic ZPE) Ne38 values found

| source | Ne38 harmonic value (epsilon) | note |
|---|---|---|
| CDW table, row 38B | -107.42431 | lowest published |
| CDW table, row 38A (Oh) | -106.47765 | |
| Predescu et al. 2005, Table I, "HA [3]" column | state 4: -100.639 K/atom = -107.4237; Oh: -99.753 K/atom = -106.4779 | eps = 35.6 K, times 38 atoms; these are the CDW 38B and 38A values repeated |

**I found no published harmonic-ZPE value for N = 38 at q = 0.095 below -107.42431.** The claim's value
-108.929936 is lower than every one of them by at least 1.4943 (needed: 5e-4).

## 4. Sources opened, and what each says about N = 38 Ne harmonic values

1. Status page (above). Its N = 38 Ne entries are -106.47765 and -107.42431.
2. Calvo, Doye, Wales, J. Chem. Phys. 114, 7312 (2001): https://www-wales.ch.cam.ac.uk/pdf/JCP.114.7312.2001.pdf
   - Table I has the same N = 38 rows as the status page.
   - Their method was basin-hopping on E + ZPE at Lambda = 0.095, with 5000 quenches started from the classical global minimum. The authors say this "may be inadequate", so the 38B row comes from a limited search.
   - Their database analysis says "LJ38 shows only one crossover at Lambda = 0.065" (Fig. 8). The isomer behind that crossover is not identified and no Ne value is given for it.
   - For comparison, the claimed object crosses the Oh line at Lambda = 0.0635 and 38B at 0.0808. So the object was probably not in their database, or rounding hides it. Either way, this gives no published value.
3. Predescu, Frantsuzov, Mandelshtam, J. Chem. Phys. 122, 154305 (2005): https://arxiv.org/pdf/physics/0508057
   - Table I gives energies in K/atom (eps_LJ = 35.6 K). Its harmonic column contains only state 4 (= 38B) and Oh (see section 3). States 1-3 and C5v have no harmonic value.
   - The PIMC/VGW energies, for example PIMC state 1 at -105.847 K/atom = -112.99 eps, are fully quantum results. They are not harmonic-ZPE values, so they are not comparable under the criterion.
   - **Caveat for the gate:** the classical energy of their "state 3" minimum is -158.312 K/atom = -168.9847 eps. That equals the object's E_LJ (-168.984987 = -158.31225 K/atom) to the printed precision. The object may therefore be that classical minimum, found in 2005 by quenching PIMC paths.
   - The paper publishes no coordinates and no harmonic or ZPE value for state 3; its HA column shows "-". Its harmonic Ne value is therefore not a published number. The claim does not mention this paper.
   - Two states in the same table, 1 and 2, have classical minima at -169.67, -169.83, -169.36 and -169.38 eps. Their harmonic values are also unpublished.
4. Deckman, Frantsuzov, Mandelshtam, Phys. Rev. E 77, 052102 (2008): https://www.chem.uci.edu/~mandelsh/publ/LJ_Quantum.pdf
   - Harmonic energies for the LJ38 Oh, Mackay and anti-Mackay structures appear only as curves in Fig. 4. They were computed on a 6-Gaussian fit of LJ, and the three lines merge near Lambda ~ 0.073.
   - The paper gives no number at Lambda = 0.095, so there is nothing comparable to test against.
5. Deckman, Mandelshtam, J. Phys. Chem. A 113, 7394 (2009): https://www.chem.uci.edu/~mandelsh/publ/LJ_Quantum2.pdf
   - VGW ground states only; for n = 38 it gives transition Lambda values. No harmonic energies.
6. Mallory, Mandelshtam, J. Chem. Phys. 149, 104305 (2018): https://pubs.aip.org/aip/jcp/article/149/10/104305/196157/ (read with WebFetch, full text)
   - Gives the DMC ground-state energy E0(Ne38) = -113.69(2) eps (anti-Mackay 1) and crossovers at Lambda = 0.0880 and 0.1000.
   - The appendix has the harmonic-frequency formula only. There are no harmonic or ZPE numbers. DMC is not a harmonic-ZPE value.
7. CCD LJ39 point file: https://www-wales.ch.cam.ac.uk/~jon/structures/LJ/points/39 (fetched once, HTTP 200, 2026-10-31T19:44Z)
   - Used for the deletion test in section 5.
8. Seen only as search snippets or abstracts (not opened):
   - Fiorentino & Marzari, arXiv:2606.03405 (2026): its zero-point-driven transition example is LJ27, not Ne38.
   - Structure-resolved population annealing of LJ38, J. Chem. Phys. 164, 214110 (2026) / arXiv:2603.04157: classical only.
   - Georgescu & Mandelshtam, J. Chem. Phys. 137, 144106 (2012) and Brown & Mandelshtam, Chem. Phys. (2016): these report self-consistent-phonon energies, not classical minimum + harmonic ZPE. I did not read the full texts (paywalled).

## 5. Trivial-edit / seeding analysis

- **38A and 38B.** The object is a different minimum from both:
  - E_LJ: -168.984987 for the object, against -173.928427 (38A) and -168.519989 (38B).
  - Lowest nonzero eigenvalue: 0.810, against 10.0 and 2.40.
  - Relabelling, symmetry or a local polish of 38A or 38B returns 38A or 38B, which have Ne values -106.478 and -107.424.
- **Deletion from the published neighbour, the LJ39 global minimum (-180.033185).** I deleted each atom in turn and Newton-polished the result (`../panel/novelty_scripts/deletions.py`). The best certified result is E_LJ -173.134317 with Ne -106.841800. The C5v Mackay LJ38 at -173.252378 gives Ne -106.724354. Both are far above -108.929936.
- **Other neighbouring cells.**
  - The table has no N = 39 row. Making a 38 from a 37 needs an added atom, which is not a trivial edit.
  - In the other species columns for N = 38 the object does not set a record: Ar -150.020 against -152.628 (38A), and Xe -162.663 against -166.828. This does not matter for the Ne claim.
- **Seeding.** The claim names no seed. The only possible precursor I found is the 2005 "state 3" classical minimum (section 4.3), which has no published coordinates and no published harmonic value.

## 6. Repository checks

- TROPHY_CASE.md: no match for zpe / zero-point / lennard / LJ38 / Ne38 / neon / ccd-quantum.
- known-knowns/: the only LJ-related entry is lennard-jones-ccd-doye-table/, which is classical CCD; its files have no zpe, zero-point, neon, quantum or LJZPE mentions. Nothing for this target.
- GitHub PR search (one plain request each, all HTTP 200, around 2026-10-31T19:38Z):
  - `repo:elder-plinius/V3R1T4S is:pr zpe`: 0 results.
  - `... ccd-quantum`: 0 results.
  - `... lennard`: 5 results (#799, #376, #333, #202, #399). All concern classical or binary LJ / CCD errata; none mentions ZPE or neon.
  - `... zero-point`: 28 results, all on unrelated targets (codes, graphs, poker and so on). None concerns LJ-ZPE.

## 7. Searches that found nothing relevant (no published Ne38 harmonic value below -107.42431)

- "Ne38 harmonic zero-point energy Lennard-Jones global minimum quantum Calvo Doye Wales 2001"
- "Predescu Frantsuzov Mandelshtam 2005 Ne38 thermodynamics equilibrium structure quantum versus classical"
- "Mallory Mandelshtam 2018 Lennard-Jones clusters quantum delocalization neon structures"
- "Calvo Doye Wales Quantum partition functions from classical distributions rare-gas clusters pdf"
- "Quantum-induced solid-solid transitions and melting in the Lennard-Jones LJ38 cluster harmonic approximation minima energies"
- "neon cluster Ne38 zero-point corrected energy global optimization harmonic disordered minimum 2024 OR 2025 OR 2026" (last 24 months: nothing on Ne38 harmonic values)
- "arXiv 2606.03405 Quantum annealing for materials Lennard-Jones zero-point energy structural transition"
- "Georgescu Mandelshtam self-consistent phonons Lennard-Jones clusters quantum LJ38 harmonic approximation Lambda 0.095"
- "Ne38 OR Ne_38 harmonic superposition zero-point energy minima database anti-Mackay energy epsilon"

## 8. Verdict

The claim beats every published harmonic-ZPE Ne38 value I found by 1.4943 or more. The best of those values is -107.42431, given by both the live table and Predescu et al. 2005. The object is not a trivial edit of any published N = 38 object, or of the LJ39 global minimum by deletion.

Caveats for the gate:
1. The object's E_LJ matches, to printed precision, the classical energy of "state 3" in Predescu et al. 2005. That paper published neither coordinates nor a harmonic value for it, and the claim does not cite it. The structure may therefore not be new, but its harmonic Ne value is not published.
2. Harmonic values in Deckman et al. 2008 exist only as figure curves on a Gaussian-fit potential and cannot be compared.
3. Quantum (DMC/PIMC/VGW) ground-state energies are lower (about -113 eps) but do not fall under the criterion's harmonic convention.

On the criterion as written, the value strictly beats everything known, with margin.

novelty: PASS (1.4943 below the lowest published harmonic Ne38 value, -107.42431; possible prior classical-only report of the same minimum flagged above)
pass: true
