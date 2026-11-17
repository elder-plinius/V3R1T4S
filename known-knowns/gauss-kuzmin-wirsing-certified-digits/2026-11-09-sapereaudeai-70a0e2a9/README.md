# C_83 (Gauss-Kuzmin-Wirsing constant): 842 certified decimals

## What

Rerunning the bundle's python-flint (Arb) certifier at 3900 and 4300 bits reproduces a rigorous enclosure of the GKW operator's second eigenvalue on H^2(|z - 3/5| < 4/5) with |lambda_2 - mu| <= 4.5491e-843 (decimal hull half-width 4.5536e-843 < 10^-842), isolated by resolvent bounds and an independent Gershgorin count, so C_83 = |lambda_2| has D = 842 certified decimals, which is strictly greater than the 175 on the 83a status page (unchanged at 2026-11-09T08:47:36Z, with no open PR touching constants/83a.md), and its centre agrees with Nisoli's 175-digit centre to 4.10e-176, within the two radii.

C_83 = |lambda_2| lies in the interval of object/C83_enclosure.txt (outward-rounded decimal endpoints to 860 places,
half-width < 10^-842):

    C_83 = 0.30366300289873265859744812190155623311087735225365789518824548146722699529424691098434081193436363681109827226371061693847461485974580131606526538181823787913244613989647642974095044629375949048702977287725110583351759220444724086591196507781055892957918671475292565364259184412178423449205725529426910040657788006767324303643964013896927671340737822867115349154354621128484197179686161434058977584991088315085544113211472674475135919927789084165033930626951545887882271890169391267356789089140566774663933094421129160160015708093412250123836578269879427693397410968338466148350983894423750860631165686164677660511537576857649906960832615797017073881580659620272287752927050913248907340377068595232825669090689724161003520178885561167121566025331218400953802471423913121137624716607708954986776761330402815937353171151468805168384381380703445...

(the two endpoints agree on these 842 decimals; the enclosure radius is below 10^-842.)

Route: rigorous residual of the true operator for a degree-2799 approximate eigenvector in the Hardy space H^2 of the
disc |z - 3/5| < 4/5, isolation and identification of lambda_2 by small-gain resolvent bounds for an 80 x 80 section,
all in Arb ball arithmetic (python-flint); proof in object/PROOF.md (Remark 0 and 13 lemmas). The centre
object/mu_N2800.txt is the Rayleigh quotient of the vector itself; PROOF.md Remark 0 explains why its origin does not
matter. This package supersedes the unsubmitted packages 2026-11-09-sapereaudeai-c7e57e15 (601 decimals, N = 2000) and
2026-11-08-sapereaudeai-3cb2629e (300 decimals, N = 1000) of the same route.

## Check it yourself

    PYTHON=python3 sh verify-it-yourself/run_checks.sh

Needs Python 3 with python-flint 0.9.0 (`pip install python-flint==0.9.0`); set PYTHON to any interpreter that has it
(without it the script tries python3, python, `py -3` and a nearby .venv, and says plainly if none can import flint).
Expected last line `PASS`, about 160 s on a 2026 desktop (one thread, about 0.85 GB). More in RUN_IT_YOURSELF.md.

## Compared to

| table | cell | value | URL | fetched |
|---|---|---|---|---|
| Tao's optimization constants, 83a | certified decimals of C_83 | 175 (Nisoli, arXiv 2602.19435) | https://teorth.github.io/optimizationproblems/constants/83a.html | 2026-11-09T08:58:22Z (gate re-fetch; also 07:59:19Z, 08:27:32Z and by the panel) |

Open PRs touching constants/83a.md at 2026-11-09T08:58:23Z: none (81 open PRs read). Non-certified expansions are
shorter in print (469 printed decimals, Briggs 2003; 382 in the OEIS A038517 b-file); the newest validated result we
found, Pollicott 2026 (arXiv 2606.13958), gives 67 places.

## Not claimed

- No claim about other eigenvalues (partial win p1 was not attempted) or about digits beyond the radius.
- The N = 2400 certificate of the same run (721 decimals) is not part of this package.
- The 649 non-certified decimals of an earlier computation are used only as a comparison; the centre does not come from
  them, so their agreement with this enclosure is an independent consistency check.
- Correctness rests on Arb's ball arithmetic and verified eigenvalue isolation (cross-checked by a Gershgorin count) and
  on the cited standard facts (Kato's continuity of Riesz projections, Gershgorin's theorem).
- Panel history: the first panel round failed REPRODUCE on a documentation slip only (740 vs 860 places for the
  enclosure file); the bundle's two documents were corrected and a second, fresh panel passed 3/3. Both rounds' files
  are in panel/ (round 1 in panel/round1/), and panel/gate.md describes the repair.

## Credits

- Isaia Nisoli, Certified spectral approximation of transfer operators and the Gauss map, arXiv 2602.19435
  (https://arxiv.org/abs/2602.19435), and https://github.com/orkolorko/GKWExperiments.jl: the 175-digit record and the
  resolvent-bridge idea used here for isolation.
- Terence Tao and contributors, https://teorth.github.io/optimizationproblems/ (constant 83a).
- Keith Briggs (2003, http://keithbriggs.info/documents/wirsing.pdf) and OEIS A038517 (https://oeis.org/A038517).
- M. Pollicott, Validated numerics for the Gauss problem on continued fractions, arXiv 2606.13958
  (https://arxiv.org/abs/2606.13958).
- Dieter Mayer and Gert Roepstorff (1987), first certified bounds; Eduard Wirsing (1974).
- Fredrik Johansson et al., Arb / FLINT (https://flintlib.org) and python-flint.
