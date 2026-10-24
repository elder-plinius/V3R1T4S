# Continuation pre-registration

Frozen: 2026-10-15 14:27:53 UTC

> a feasible solution strictly better than the best known objective of an instance in class 06
> (portfolio optimisation: multi-period, transaction costs, short selling) of the Quantum Optimization Benchmarking
> Library, in the objective sense the class defines, where the bar is the better of the library's best-known table and
> any value posted in an open pull request to the library (#44, #64 and #87 when this was written). Class 01 (market
> split) is out: its instances' generating solutions are published, so no object claim is possible there.

This is a prospective review protocol for an existing disclosed lead, not a claim that its candidate was unknown before this freeze. The dossier reports -1654188; the prior X3 dry run independently checked the public bar -1090282. Neither candidate is newly discovered here. One claim cell only: po_a400_t10_s00, B=100, lambda=1/100.

Statistic: exact integer objective of the published bqp_u3_c10.zpl, with each rational coefficient rounded half away from zero, canonical slot encoding, all feasibility constraints checked. Threshold: strictly below the best public same-cell objective; currently -1090282, i.e. at most -1090283. If a better public bar appears, use it; ties fail. The existing object is frozen for its panel; optimization output, if any, remains a separate unpanelled lead.

null_test: not needed because an explicit deterministic feasible object is checked against a published integer table/PR objective; no statistical or beats-chance claim is made.

Calibration: known reference, false objective, invalid budget/capital, malformed counts, and literal slot polynomial comparisons. Review: independent checker, source/parameter audit, and three fresh skeptics. No global optimality claim.
