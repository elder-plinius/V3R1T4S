# Prereg, written 2026-11-01T00:28:46Z
Criterion: verbatim in target.md (lower-bound main win). Bar: strictly above sqrt(3)/4 + 0.0153 = 0.44831270189.
Statistic: gain G such that B >= sqrt(3)/4 + G, from a dichotomy on |a3| at a threshold eta: near branch certified gain G_near(eta) at a radius r1(eta) with positivity certified on r0<=|z|<=r1; away branch certified at r0 by covering all (a2,a3) with |a3|>=eta (or excluding them) with a centre witness.
Rungs, largest closed by BOTH branches is claimed: G in {0.0156, 0.0155, 0.01545, 0.0154, 0.01535, 0.01531}. Only rungs >= 0.01531 count.
Pass only if: every inequality is checked by rigorous ball or directed-rounding interval arithmetic; every minorant, the |a3| bound and every near cut is rebuilt from stored multipliers by Theorem 3.2 in Arb at two precisions; a separate covering script confirms the leaves cover the whole domain; failure tests pass (a removed leaf is caught; a raised T fails on a real box; explicit members of B, among them the Bonk extremal, are not violated by any minorant). Any failure at a rung: no claim at that rung.
Multipliers reused from Wikstrom's archive (doi:10.5281/zenodo.21975862) are data; his programs are not run. Hashes: data/wikstrom_hashes.txt.
A different rung set or statistic gets PREREG.v2.md, stated in the report.
null_test: not needed because the claim is a deterministic certificate of an explicit inequality, not a search or statistical result.
