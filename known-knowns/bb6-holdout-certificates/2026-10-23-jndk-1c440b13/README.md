# BB6 holdout663 #523: complete arithmetic halting equivalence

## What

For `1RB1LC_1LC0RD_0LE1LA_0RF1RA_1LA0LA_---0RB` on blank0 in state A, halting is equivalent, relative to the explicit custom checker TCB, to the recurrence in `object/counter_core.py` from its empty front state reaching a front state with z=1 and either first token `(1,2-or-None)` or marker `(1,1)` followed by a prefix `(2,1)^r(2,2-or-None)` for some r>=0.

## Check it yourself

Run `sh verify-it-yourself/run_checks.sh` from this folder with CPython3.12.15, SymPy1.14.0 and a C compiler. Expected final line: `PASS`. The compressed proof object is unchanged from the original packet; current source/reproduction receipts are described below.

## Compared to

The current public Holdouts_lists capture at2026-10-23T13:59:08.537414Z links the16October2026 informal BB6_holdouts_663.txt. Its fresh HTTP200 file capture at2026-10-23T13:59:24.308397Z has SHA256 `cfb2540f8101f2f2f20a14f9bc848252e34e45de2920fdd6b257096093844ee9`; this machine is line523. Full current public wiki text and relevant normalized proof sources/PR metadata were reviewed; no equivalent complete reduction was found in that documented scope. Human Discord searches are carried as human-reported evidence, not newly claimed agent access. See panel/novelty.md and how-we-built-it/PUBLIC-NOVELTY-AUDIT.md.

## Not claimed

This is p2 only. It does not decide whether the arithmetic terminal pattern is reached, whether the machine halts, or the value of BB6. The custom symbolic/source/list/automata/word/path/logic checker TCB is substantial and explicit; this is not a Lean/Rocq foundational proof. No global historical priority or complete private/deleted-source coverage is claimed. BB6 research remains retired.

## Credits

Busy Beaver Challenge and mxdys provide semantics and public inventories. This builds on the earlier [seven-rule p1 PR362](https://github.com/elder-plinius/V3R1T4S/pull/362). [geoAlpine's July4 census section5d](https://github.com/geoAlpine/busybeaver/blob/c4c012a5070295f732b5fefb6b92e99f166a0bf2/BB6_TYPE_IV_CENSUS_2026-07-04.md) already gives the same-machine local00 halting-entry gate; the complete recurrence/blank iff is the additional object here. Arithmetic and stacked-block reduction methodology is prior work, including [Dos Santos et al.](https://arxiv.org/html/2610.22603v2), [Cryptids](https://github.com/google-deepmind/cryptids), and [BusyCoq](https://github.com/ccz181078/busycoq/tree/BB6). [SymPy](https://www.sympy.org) supplies exact algebra. Full credits and source limits are preserved in how-we-built-it/.
