# Novelty skeptic: three-body-equal-mass-rigorous-stability-beyond-eight, partial win p1

context: subagent (fresh context)
role: NOVELTY skeptic (V3R1T4S three-skeptic panel). Read only the claim package (CLAIM.md, status_record.md,
target.md, PROOF.md, the head of data/ics_971_100_num.txt), the repo's TROPHY_CASE.md and known-knowns/, and
the repo's pull requests. Proof correctness is not judged here (that is for the other skeptics).

## Status fetch (one request, no retries)

- URL: https://arxiv.org/abs/2510.22802
- command: curl with User-Agent `V3R1T4S-novelty-skeptic/1.0 (research audit)`
- HTTP: 200
- time: Sun Nov 22 22:30:59 UTC 2026 (`date -u`, before and after)
- shows: title "An extensive search for stable periodic orbits of the equal-mass zero angular momentum three-body
  problem"; submission history only [v1] Sun, 26 Oct 2025 19:20:46 UTC; abstract: "971 verified initial conditions
  for linearly stable periodic collisionless orbits ... should be considered as candidates for KAM-stable orbits".
  No v2, no claim of a rigorous (interval) proof. Matches the claim's status record. No text addressed to agents.
- status: OPEN (no rigorous linear-stability result in the status source).

## Identity of the object

Row 2 of ics_971_100_num.txt: vx = 0.46444517..., vy = 0.39606001..., T = 14.89430517...
This is Moth I (Suvakov and Dmitrasinovic, PRL 110 (2013) 114301; label IVa.2.A in Dmitrasinovic, Hudomal,
Shibayama, Sugita, J. Phys. A 2018, arXiv 1705.03728). Check: that paper's table of linearly stable orbits gives
moth I stability angles 0.159013 and 0.491881, which equal the claim's certified frequencies 0.1590129389... and
0.4918813053... to all six printed digits. The paper says its arguments are numerical, "without rigorous proofs".

## Searched (2026-11-22/23)

- Web (standard + extended): computer-assisted / interval proofs of linear or KAM stability for equal-mass
  three-body orbits other than the figure-eight; "Moth I" stability proof; Suvakov-Dmitrasinovic orbits
  (moth, bumblebee, butterfly) rigorous; Hristov-Hristova-Tanikawa follow-ups; Roberts symmetry-reduction work
  2024-2026; GitHub interval/CAPD/arb three-body stability code.
- arXiv API (https, same User-Agent): au:Kapela (newest: 2021, no new three-body paper); "three-body" AND
  "computer-assisted" sorted by date (newest 2026-08: restricted problem, Arnold diffusion; none on Moth I or the
  971 list); abs moth AND three-body (no hits); periodic orbit + three-body + interval; figure-eight +
  computer assisted (only Kapela-Simo 1105.3235); choreography + stability + proof.
- Kapela's publication page (ww2.ii.uj.edu.pl/~kapela/papers/papers.html, HTTP 200): three-body stability work is
  Kapela-Simo Nonlinearity 20 (2007) (figure-eight) and Nonlinearity 30 (2017) = arXiv 1105.3235 (figure-eight and
  two rotating Eights, non-zero angular momentum). Nothing on Moth I.
- GitHub (gh, read-only): Foundation-0/certified-orbits (README "Status: not started"; the Hristov list row of its
  table reads "none yet"; release v1.0.0 2026-11-11 has no assets; open PRs 8-12 are scaffolding, none certifies an
  orbit). Rexyysilent/three-body-moth13-cap (release v1.0.0-rc1, 2026-08-11, assets checked by name): existence only
  of a Moth-I^13 orbit with masses (1, 1, 1001/1000), no stability; different masses and topology, not this cell.
  Ma1achy/Principia: downloads the 971 list, no proofs. Code search "3bodystab971", "Krawczyk three-body
  monodromy": no stability certificate found.
- Other near neighbours: Hudomal et al. 2018 and Hristov et al. 2025 (numerical); Fenucci-Gronchi arXiv 1801.06429
  (interval proofs of INSTABILITY, Platonic N-body); Simmons arXiv 1903.08981 (Broucke isosceles, collision orbit,
  not in the list); arXiv 2406.17564 (Marchal conjecture, figure-eight continuation family); Ross et al. arXiv
  2606.29189 (restricted problem cyclers, numerical); Li comment arXiv 1312.6796 (no Moth I).
- This repo: TROPHY_CASE.md has no three-body entry; known-knowns/ has no three-body family; PR searches
  (three-body, hristov, figure-eight, moth, orbit, stability, KAM, Kapela, 3bodystab971, equal-mass, the target id)
  found no prior claim on this target.

## Comparison with published objects (same cell and neighbours)

Published rigorous objects in this cell (equal-mass planar three-body, rigorous existence + linear/KAM stability):
the figure-eight only (zero angular momentum), and two rotating Eights (non-zero angular momentum, neighbour cell).
Moth I is a different periodic orbit (different free-group/topological class, period, and stability angles), not
obtainable from the figure-eight or rotating Eights by deletion, restriction, relabelling of bodies, a symmetry of the
problem (rotation, reflection, time reversal, scaling), a valid propagation rule, or local numerical polish. The claim
is seeded from the Hristov-Hristova-Tanikawa initial condition, which is a numerical (non-rigorous) object and which
the claim names; the new content (Krawczyk existence box and certified ellipticity of the reduced monodromy) is not
given by any edit of that numerical row. The unequal-mass Moth-I^13 existence proof is a different orbit at different
masses and has no stability statement. This is not a tie: before this claim no rigorous linear-stability proof was
found for any orbit of the 971-row list other than the figure-eight.

Residual risk: a paper or thesis not indexed by the searches above (for example an unindexed 2026 journal article)
cannot be excluded. novelty is judged only for the p1 statement (existence + linear stability), not KAM.

novelty: CONFIRMED (no prior rigorous existence + linear-stability proof found for Moth I / row 2)
pass: true
