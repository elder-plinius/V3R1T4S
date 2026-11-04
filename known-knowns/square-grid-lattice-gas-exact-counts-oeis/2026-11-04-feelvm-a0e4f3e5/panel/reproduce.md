# REPRODUCE skeptic report — A054759 a(15) claim

context: subagent

Interpreter for every run below: `<python3>` (Python 3.13.15,
numpy 2.5.4), always with `-I`. All commands were run from the run directory
(parent of claim/) unless stated; nothing in claim/ was modified.

## Environment adaptations (no program or claim file edited)

1. Both programs locate the b-file as `<claim>/../data/A054759_b054759.txt.raw` relative to
   the claim dir's grandparent, i.e. a `data` folder one level ABOVE the run directory
   (`iso_row.py` line 382, `iso_ht.py` line 307: `_ISO.parent.parent / "data" / ...` where
   `_ISO` = claim dir). That location did not exist in this layout (the run's data folder is
   the run dir's own `data/`, i.e. `../data/A054759_b054759.txt.raw` from claim/). The path
   is derived from `__file__`, so cwd cannot change it. Adaptation: created a directory
   junction `data` (at the level the programs expect) pointing at the run directory's own
   `data` folder, so the unmodified programs read the unmodified
   `../data/A054759_b054759.txt.raw`. The b-file on disk ends at n=14 with
   a(14) = 15844635835975276495290739119895808472, as CLAIM.md states.
2. Ladder mode's default output paths live under a non-existent `output` folder inside
   claim/; used the programs' own `--out` flag to write to `../panel/repro_out/` instead
   (`ladder_run1_repro.json`, `ladder_run2_repro.json`).

## 1. CRT recomputation

Command: `<venv>/Scripts/python.exe -I claim/crt_check.py`

Key output (copied):

    run1: CRT -> 4310182149988584261406143524214457416387448  matches value.txt: True; all 14 residues consistent: True; modulus 2^209.5; primes: [32611, 32491, 32401, 32371, 32341, 32251, 32191, 31891, ...] (14 primes, 31231..32611)
    run2: CRT -> 4310182149988584261406143524214457416387448  matches value.txt: True; all 14 residues consistent: True; modulus 2^208.6; primes: [30091, 31081, 31051, ...] (14 primes, 30091..31081)
    prime sets disjoint: True
    OVERALL: PASS

Both CRTs reconstruct exactly the integer in value.txt. Independent re-verification with my
own code (not crt_check.py): all 28 listed numbers are prime, distinct, congruent 1 (mod 15),
> 1000; both "modulus" fields equal the product of their 14 primes (2^209.52 and 2^208.61);
every listed residue equals value.txt mod its prime, in order; prime sets disjoint; the
"bound" field equals 2^15 * 1220^15 = 2^168.79 (matches REPRODUCE.md's rigorous bound
2^168.8). Margins: modulus/bound = 1.83e12 (run1) and 9.70e11 (run2) — both far above the
required 1e6 margin.

## 2. Ladder with run-1's program (isotypic-row, 2^15 states)

Command: `<venv>/Scripts/python.exe -I claim/programs/iso_row.py --mode ladder --out ../panel/repro_out/ladder_run1_repro.json`

Key output (copied, 14/14 OK in 197.1 s):

    n= 1 ref(exact_int)=4 iso(p=101,z=1)=4 OK (0.0s)
    n= 2 ref(exact_int)=18 iso(p=101,z=100)=18 OK (0.0s)
    n= 3 ref(exact_int)=148 iso(p=103,z=46)=45 OK (0.0s)
    n= 4 ref(exact_int)=2970 iso(p=101,z=10)=41 OK (0.0s)
    n= 5 ref(exact_int)=143224 iso(p=101,z=95)=6 OK (0.0s)
    n= 6 ref(exact_int)=16448400 iso(p=103,z=57)=21 OK (0.0s)
    n= 7 ref(exact_int)=4484823396 iso(p=113,z=109)=70 OK (0.1s)
    n= 8 ref(direct_mod(p=17))=13 iso(p=113,z=18)=26 OK (0.1s)
    n= 9 ref(direct_mod(p=19))=15 iso(p=109,z=66)=101 OK (0.1s)
    n=10 ref(direct_mod(p=31))=27 iso(p=101,z=14)=99 OK (0.3s)
    n=11 ref(direct_mod(p=23))=12 iso(p=199,z=61)=100 OK (1.2s)
    n=12 ref(direct_mod(p=37))=29 iso(p=109,z=101)=49 OK (4.8s)
    n=13 ref(direct_mod(p=53))=46 iso(p=131,z=107)=105 OK (28.1s)
    n=14 ref(direct_mod(p=29))=13 iso(p=113,z=7)=70 OK (197.1s)

Comparison: fresh output JSON is field-by-field IDENTICAL to claim/ladder_run1.json for all
n=1..14 (bfile, ref, ref_kind, isotypic_mod, prime_iso, zeta, isotypic_matches). Independent
re-check vs the b-file: for n<=7 the reference is an exact integer computation equal to the
b-file term; for n=8..14 ref == bfile mod the direct_mod prime; and isotypic_mod ==
bfile mod prime_iso for every n. All true.

## 3. Ladder with run-2's program (h-tracked, 2^16 states)

Command: `<venv>/Scripts/python.exe -I claim/programs/iso_ht.py --mode ladder --out ../panel/repro_out/ladder_run2_repro.json`

Key output (copied, 14/14 OK in 43.2 s; a(n) values echo the b-file terms):

    n= 1 a=4 iso(p=101,z=1)=4 OK (0.0s)
    n= 2 a=18 iso(p=101,z=100)=18 OK (0.0s)
    n= 3 a=148 iso(p=103,z=46)=45 OK (0.0s)
    n= 4 a=2970 iso(p=101,z=10)=41 OK (0.0s)
    n= 5 a=143224 iso(p=101,z=95)=6 OK (0.0s)
    n= 6 a=16448400 iso(p=103,z=57)=21 OK (0.0s)
    n= 7 a=4484823396 iso(p=113,z=109)=70 OK (0.0s)
    n= 8 a=2901094068042 iso(p=113,z=18)=26 OK (0.1s)
    n= 9 a=4448410550095612 iso(p=109,z=66)=101 OK (0.1s)
    n=10 a=16178049740086515288 iso(p=101,z=14)=99 OK (0.3s)
    n=11 a=139402641051212392498528 iso(p=199,z=61)=100 OK (0.9s)
    n=12 a=2849295959501939989625992464 iso(p=109,z=101)=49 OK (3.0s)
    n=13 a=137950545200232788276834783781648 iso(p=131,z=107)=105 OK (11.0s)
    n=14 a=15844635835975276495290739119895808472 iso(p=113,z=7)=70 OK (43.2s)

Comparison: fresh output JSON is field-by-field IDENTICAL to claim/ladder_run2.json for all
n=1..14. Independent re-check vs the b-file passes for every n.

## 4. Fresh-prime skeptic check (bank's verification route)

Prime selection was mine, made after reading residues_run1.json/residues_run2.json:
P must be prime, congruent 1 (mod 15), > 1000, and absent from both lists (28 primes,
30091..32611). I first tried P = 32911 (largest fresh such prime > 32611):

- iso_row.py `--mode prime --prime 32911` aborted in 16 s with its own fail-fast exactness
  guard: `assert Mk.max() < 2 ** 15` (iso_row.py line 267). See divergence note 1 below.
  No wrong output was produced; the program refuses rather than risks inexact arithmetic.

Final fresh prime: **P = 29881** — the largest prime < 2^15 congruent 1 (mod 15) that is in
neither list (29881 = 15*1992 + 1; verified prime; not in either residue set; > 1000).
Expected residue computed independently: value.txt mod 29881 = 10495.

Commands and outputs (copied):

    <venv>/Scripts/python.exe -I claim/programs/iso_row.py --mode prime --prime 29881
    n=15 prime=29881 zeta=26142 -> Trace(T^n) mod p = 10495
    claimed a(15) mod p = 10495          (30.4 s)

    <venv>/Scripts/python.exe -I claim/programs/iso_ht.py --mode prime --prime 29881
    n=15 prime=29881 zeta=26142 -> Trace(T2^n) mod p = 10495
    claimed a(15) mod p = 10495          (2m7.2s)

Both independently-encoded programs agree with each other and with value.txt mod 29881 at a
prime neither run used. MATCH.

## 5. Sanity: digit count and growth constant

- value.txt is a single line; len(str(v)) = 43 digits. MATCH (claim says 43).
- ln(a15)/225 = 0.43630912920511505, bit-identical to growth.json's "ln_a15_over_225".
- Lieb constant recomputed: 1.5*ln(4/3) = 0.4315231086776713 = growth.json's "lieb_lnW".
- Literal criterion check (a(N)^(1/N^2) within 1e-3 of the entropy constant): a(15)
  deviates by literal_logdiff = 0.004786020527443757 (recomputed exactly), i.e. the LITERAL
  check FAILS for the claimed a(15). This is consistent and documented in growth.json: the
  published, certainly-correct a(14) fails the same literal check by MORE
  (literal_14_logdiff = 0.005496760494604458, recomputed exactly). So the literal wording of
  the criterion is unsatisfiable at n=14/15 sizes (finite-size correction dominates); the
  claim's growth.json discloses this caveat and additionally shows
  |log_ratio_computed_vs_pred| = 1.354e-4 < 1e-3 against its fitted growth model. This is a
  criterion caveat, not a defect in the arithmetic.

## Divergences / documentation nits found (none affect the arithmetic)

1. REPRODUCE.md says the single-prime route accepts "any prime P = 1 (mod 15), P < 2^31".
   The programs' actual exactness guard requires prime-mode P < 2^15 = 32768 (transfer
   entries and reduced isotypic entries must stay < 2^15 for exact float64 matmul; observed
   assertion failure at P = 32911 in iso_row.py line 267; iso_ht.py carries the identical
   guard at line 235). The claim's own 28 CRT primes are all < 32768, so the claim's
   arithmetic is unaffected; but the documented bound 2^31 is wrong — larger fresh moduli
   must be covered by several < 2^15 primes, as REPRODUCE.md itself notes for non-1-mod-15
   primes.
2. REPRODUCE.md says "both CRT moduli exceed 2^209": run1 is 2^209.52 but run2 is 2^208.61,
   marginally below 2^209. The load-bearing requirement (exceed the rigorous bound 2^168.8
   with >= 1e6 margin) holds for both with ~1e12 margin.
3. growth.json's "log_ratio_computed_vs_pred" = +1.354e-4; my recomputation of
   ln(a15/predicted_a15) = -1.354e-4 (opposite sign convention, identical magnitude, still
   < 1e-3).
4. CLAIM.md quotes Lieb's constant as "ln = 0.431523058..."; the exact value is
   0.431523109... (growth.json uses the correct value). Difference 5e-8, immaterial.

## Verdict

CRT: both reconstructions reproduce value.txt exactly, residues all consistent, prime sets
disjoint, modulus exceeds the rigorous bound with ~1e12 margin. Ladders: 28/28 OK lines,
fresh outputs byte-equivalent (field-by-field identical JSON) to the published ladder_run1.json
and ladder_run2.json. Fresh prime 29881: both programs print 10495 = value.txt mod 29881.
Digit count and growth numbers reproduce exactly; the literal-check FAIL is honestly
documented and matched by the published a(14) failing it harder.

pass: true
