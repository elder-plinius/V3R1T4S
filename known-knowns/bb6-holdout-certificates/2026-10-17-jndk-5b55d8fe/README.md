# BB(6) holdout 663 #523: a verified macro-rule reduction (partial win p1)

## What

For 1RB1LC_1LC0RD_0LE1LA_0RF1RA_1LA0LA_---0RB (line 523 of BB6_holdouts_663.txt, the newest BB(6) file on Holdouts_lists, whose saved wiki pages and annotated-sheet notes as fetched 2026-10-17T17:10Z contain no rule set), the seven context-preserving parametric rules in result/rules.json are proved for every parameter value in their stated domains by the sympy-based checker code/prove.py (block-copy induction for even/odd/Eodd/Dstep, k-induction for the three drains), and all 8,365,935 occurrences of their input patterns starting at steps 0..1e8 of the blank-tape run match naive single-step simulation; this is a partial acceleration only and says nothing about whether the machine halts.

Panel: three fresh skeptics (REPRODUCE, NOVELTY, CRITERION) all passed; gate status CONFIRMED_PARTIAL (partial win p1
of bank target bb6-holdout-certificates). See panel/.

The object is object/rules.json: seven context-preserving parametric rules (even, odd, Eodd, even_drain, Dstep,
Ddrain1, Ddrain3) for the 6-state machine `1RB1LC_1LC0RD_0LE1LA_0RF1RA_1LA0LA_---0RB`. Example: `0^k A0 1^(2k) 00 ->
A000 1^(3k)` in 6k^2+3k steps, for every k >= 0.

## Check it yourself

    sh verify-it-yourself/run_checks.sh

Needs Python 3 with sympy (set PYTHON=... to choose one) and a C compiler. Expected last line: `PASS`. About one
minute on a laptop-class CPU (49 s measured on a 4-core server). Real output: verify-it-yourself/RECEIPTS.md.

## Compared to

| table | cell | value | URL | fetched (UTC) |
|---|---|---|---|---|
| bbchallenge Holdouts_lists, newest BB(6) file BB6_holdouts_663.txt (October 16th, 2026, @mxdys) | line 523 | undecided holdout; annotated sheet "Quadratic Mess" with empty Status/Notes/Sources; no accelerated rule set in the wiki/holdout notes | https://wiki.bbchallenge.org/wiki/Holdouts_lists | 2026-10-17T17:10:25Z (re-fetched by NOVELTY 17:13:38Z) |

Snapshot with sha256 values: the-record-we-beat/record.md.

## Not claimed

- The machine's halting status. This is not a non-halting certificate and not a halting proof; the full success
  criterion of the bank target is not met.
- A closed rule system: naive steps remain between rule applications (about 15,800 in the first 1e8 steps).
- Anything about the bbchallenge Discord beyond the workspace human's manual searches (exact string, mirror string,
  attachments since 2026-09-30, one Oct 1 list), which found no rule set; cosearch.bbchallenge.org was unreachable
  (HTTP 502) at check time.
- A formal (Lean/Rocq) proof: the symbolic checker is custom Python with sympy, which p1 allows.

## Credits

- The Busy Beaver Challenge (bbchallenge) collaboration: semantics, wiki and holdout lists, https://bbchallenge.org,
  https://wiki.bbchallenge.org/wiki/Holdouts_lists.
- @mxdys for the BB(6) holdout lists, including BB6_holdouts_663.txt.
- The maintainers of the annotated BB(6) holdout spreadsheet linked from the BB(6) wiki page.
- Heiner Marxen and Juergen Buntrock for the BB(5) champion used to validate the simulator (bbchallenge, "BB(5)",
  https://wiki.bbchallenge.org/wiki/BB(5)).
- SymPy (https://www.sympy.org), used by the symbolic checker.
- Checked for prior work, nothing found for this machine: ccz181078/busycoq (https://github.com/ccz181078/busycoq),
  google-deepmind/cryptids (https://github.com/google-deepmind/cryptids).
- Produced with V3R1T4S (https://github.com/elder-plinius/V3R1T4S) by AI agents across several runs, contributed by
  jndk.
