# BB6 holdout 663 #523: complete arithmetic halting equivalence

This replaces [draft PR #627](https://github.com/elder-plinius/V3R1T4S/pull/627) to correct verification documentation and include captured checker output. The proof object and scientific claim are unchanged.

## What

For `1RB1LC_1LC0RD_0LE1LA_0RF1RA_1LA0LA_---0RB` on blank0 in state A, halting is equivalent, relative to the explicit custom checker TCB, to the recurrence in `object/counter_core.py` from its empty front state reaching a front state with z=1 and either first token `(1,2-or-None)` or marker `(1,1)` followed by a prefix `(2,1)^r(2,2-or-None)` for some r>=0.

## Check it yourself

From the package directory, run:

```sh
sh verify-it-yourself/run_checks.sh
```

Requirements: **CPython 3.12.15**, **SymPy 1.14.0**, a POSIX shell, and a **C11 compiler available as `cc`** (for example, GCC or Clang). Expected final line: `PASS`.

Budget a few minutes on a modern laptop (rough estimate, not a laptop benchmark). The previous clean check on the queued server took 41 seconds. The check is offline and performs no package installation. `RUN_IT_YOURSELF.md` gives the full prerequisites and optional proof-reconstruction commands; `verify-it-yourself/RECEIPTS.md` contains captured output.

## Compared to

The public [Holdouts lists](https://wiki.bbchallenge.org/wiki/Holdouts_lists) capture requested at 2026-10-23T13:59:08.537414Z linked the informal `BB6_holdouts_663.txt`, dated October 16, 2026, by mxdys. The fresh HTTP 200 [file capture](https://wiki.bbchallenge.org/w/images/6/69/BB6_holdouts_663.txt), requested at 2026-10-23T13:59:24.308397Z, has SHA256 `cfb2540f8101f2f2f20a14f9bc848252e34e45de2920fdd6b257096093844ee9`; this machine is line 523.

Full current public wiki text and relevant normalized proof sources and PR metadata were reviewed. No equivalent complete reduction was found within that documented source coverage. Completed human Discord searches are attributed as human-reported evidence, with their original dates; no new agent access is claimed. The dated comparison and access limits are in `panel/novelty.md` and `how-we-built-it/PUBLIC-NOVELTY-AUDIT.md`.

## Not claimed

This is partial win **p2** only. It does not decide whether the arithmetic terminal pattern is reached, whether the machine halts, or the value of BB(6). The custom source, symbolic, list, automata, word, path and logic checker TCB is substantial and explicit in `object/PROOF.md`; this is not a Lean/Rocq foundational proof. No worldwide historical priority or complete private/deleted-source coverage is claimed. BB6 research remains retired.

## Credits

The Busy Beaver Challenge collaboration and mxdys provide the semantics and public inventories. This builds on the earlier [seven-rule p1 PR #362](https://github.com/elder-plinius/V3R1T4S/pull/362). [geoAlpine's July 4 census, section 5d](https://github.com/geoAlpine/busybeaver/blob/c4c012a5070295f732b5fefb6b92e99f166a0bf2/BB6_TYPE_IV_CENSUS_2026-07-04.md) already gives the same-machine local `00` halting-entry gate; the complete recurrence and blank-start iff are the additional object here.

Arithmetic and stacked-block reduction methodology is prior work, including [Dos Santos et al.](https://arxiv.org/html/2610.22603v2), [Cryptids](https://github.com/google-deepmind/cryptids), and [BusyCoq](https://github.com/ccz181078/busycoq/tree/BB6). [SymPy](https://www.sympy.org) supplies exact algebra. Full credits and source limits are preserved in `how-we-built-it/`.
