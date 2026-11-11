# The Record We Beat — `laminar-ef1-four-agent-key-matroids`

## Published Literature Record
- Source: `https://arxiv.org/abs/2608.31121`
- Fetched UTC: `2026-10-28T00:31:55Z`
- Source SHA-256: `4e05efb1c740dd4a99ee9951a054b3bfbbb731da89e5cd800d05eedc1be9a278`
- Target: Size-8 Key Matroid ($G_1=\{1,2,3\}, G_2=\{4,5,6\}, G_3=\{7,8\}$ with bundle size $\le 2$ and group capacity $\le 1$)
- Published status: Open (Cookson & Shah, arXiv:2608.31121v1, Section 5 & Appendix B)

## Why This Resolves the Open Question
Cookson & Shah reduced fair division under 4-colorable laminar matroids to finding an EF1 allocation with ordered no-envy under two finite key matroids of size 8 and size 12. In Appendix B, they proved that their 3-agent technique (top-good separation) fails (Lemma 12), but left open whether an allocation with EF1 and ordered no-envy always exists.

This submission resolves the size-8 key matroid question by providing an exact rational $4 \times 8$ valuation matrix with prescribed agent order $1 \prec 2 \prec 3 \prec 4$ under which **every single one of the 864 complete feasible allocations strictly violates either ordered no-envy or EF1**. This refutes the ordered no-envy reduction conjecture for the size-8 key matroid with an exact obstruction certificate.
