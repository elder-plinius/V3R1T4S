# Build and verification notes

The object is a source-bound arithmetic recurrence and a proof packet for the exact six-state transition table. It uses a restricted finite-list interval-tape model, source-checked row schemas, explicit carry induction, grammar-language inclusion, terminal-predicate equality and finite-reachability induction. Its custom trusted rules are listed in `object/PROOF.md` and the compressed proof packet.

Scientific work and proof parsing ran as queued remote jobs. The original proof composition and independent source/grammar audits are preserved in the unchanged proof bundle. Raw table pages were excluded from that mathematical bundle. The replacement corrects documentation and receipt presentation; it does not modify those scientific objects or the frozen panel reports.

From the **package root**, run:

```sh
sh verify-it-yourself/run_checks.sh
```

Use CPython 3.12.15, SymPy 1.14.0, a POSIX shell, and a C11 compiler available as `cc`. Expected final line: `PASS`. See `RUN_IT_YOURSELF.md` for manual reconstruction and fresh proof-judgment regeneration. The complete check is offline; all installation and environment preparation occur beforehand.
