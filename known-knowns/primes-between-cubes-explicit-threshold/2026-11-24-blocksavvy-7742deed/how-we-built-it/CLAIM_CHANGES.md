# claim_v2: post-panel errata (claim/ is kept exactly as the panel judged it)
Panel (runs/2026-11-24-0730/panel/, reproduce/novelty/criterion all pass: true) asked for credit and variant fixes. None changes
the main claim n >= exp(exp(29.735)): out/main_prec128.txt, main_prec256.txt, standalone_main.txt, null_tests_out.txt,
replay_ch_out.txt and mutation_out.txt regenerate byte-identical to claim/out/.

(a) Credit, RULES 13 (novelty 4.1): CLAIM.md and PROOF.md now cite rStation paper 130 (u/span_of_dilates, §2.3, v2 posted
    08 Nov 2026, https://rstation.ai/problems/riemann_hypothesis/papers/130) as the prior non-rigorous anticipation
    (~30.07, "model, not a theorem", Bellotti Thm 1.3 with Ford's c, not Yang's 51.34), and say what is new.
(b) Credit (novelty 4.2): 32.76 is credited to Mossinghoff, Trudgian & Yang, Res. Number Theory 10 (2024),
    doi:10.1007/s40993-023-00498-y (OEIS A060199 kept only as where it is recorded). 32.537 (Cully-Hugill thesis Thm 4.3) stays
    the comparison value; CLAIM.md adds a cautious note that it may use Ford's c = 51.82 below its stated range T0 = exp(exp(33))
    (criterion concern 2; unproven, does not affect the claim).
(c) Journal-only variant (criterion concern 1): the zero-free constant actually in data/ is 54.004 (arXiv:2306.10680v1 Thm 1.2),
    not 53.989. Recomputed with the certificate code: c = 54.004 + Bellotti Thm 1.1 -> Y = 29.907 (arb prec 128 and 256 PASS,
    29.906 FAIL with Phi = 1.0961; standalone mpmath.iv PASS at 29.907): out/journal_zfr_54.004_prec256.txt,
    out/journal_zfr_54.004_29.906_expect_FAIL.txt, out/standalone_journal_zfr_54.004.txt. No-preprint/thesis row: 32.676 -> 32.677.
    The 53.989 rows (29.906 / 32.676) stay in out/scan_out.txt labelled as the journal value quoted by Yang's thesis Table 4.1.
    code/scan.py now scans c = 54.004 too; code/run_all.sh writes the three new out/ files.
(d) PREREG.md copied in, byte-identical to the run's frozen file (sha256 11805ff40210ed97477c31340d516d28e922ba080e24464d0b7a42b90f56a8bb)
    (reproduce note: CLAIM.md cited it but it was missing from claim/).
(e) data/fetch_log.txt: appended a User-Agent audit (history unchanged). The generic 'Mozilla/5.0' UA was used only for the first
    07:30-07:32Z PDF fetches (all re-fetched honestly at 07:42Z) and for scratch HTML not in data/; the OEIS status fetch at 07:34:04Z
    used "V3R1T4S research agent (BlockSavvy)"; the novelty skeptic's 07:53:27Z re-fetch was byte-identical (sha256 d132575b...).
