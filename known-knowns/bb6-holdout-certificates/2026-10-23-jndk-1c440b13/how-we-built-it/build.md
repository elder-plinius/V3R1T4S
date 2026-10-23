# Build and verification notes

The object is a source-bound arithmetic recurrence and a proof packet for the exact six-state transition table. The candidate packet uses a restricted finite-list interval-tape model, source-checked row schemas, explicit carry induction, grammar-language inclusion, terminal-predicate equality and a finite-reachability induction. Its declared trusted rules are listed in `../object/PROOF.md` and in the compressed proof packet.

All scientific work and proof parsing ran as queued Veritas jobs. Jobs 1761 and 1776 regenerated the proof composition; job 1771 verified the exact runtime; the fresh reproduction panel's jobs 1797 and 1800 independently checked source-AST rows and the grammar/codec link. The package builder removed raw table captures from the proof archive while preserving the proof source and its code manifest. Run the standalone package check with `sh ../verify-it-yourself/run_checks.sh` from the package root.
