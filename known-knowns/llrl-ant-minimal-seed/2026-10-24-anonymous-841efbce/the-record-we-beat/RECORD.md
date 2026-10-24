# Record compared against
No record table exists for this quantity (least highway onset of LLRL with at most k non-zero cells).
Status source: GLR, "Ants on the highway", https://arxiv.org/abs/2409.10124 , fetched 2026-10-24T16:05:56Z, HTTP 200,
page sha256 989c0e4e904a8098de855f23183a88c41d22ebf2253b15f5facc03f08363534b (v1, submitted 16 Sep 2024; identical to
the 2026-10-24T14:28:57Z fetch). Page not included here.
Extracted cell compared: g(0): GLR say the blank-grid LLRL ant reaches the period-384 highway "after 256100 steps";
our exact value is 256241 (a rounded figure there, consistent). GLR give no seeds and no least-onset values for k >= 1.
Other checks (see panel/novelty.md): OEIS (no match for 555,318,245,195,174 or "LLRL"), arXiv 2506.10482 (LLLR minimal
seeds, a different rule), Wikipedia, and a fresh literature search by the novelty reviewer.
The novelty reviewer also found the exact blank onset "256,241 steps" in a YouTube video transcript
(https://www.youtube.com/watch?v=22dfYC_q_ho , 2026-10-15) and a 13-cell onset-0 H384 snapshot in Lutfalla's simulator
(lutfalla.fr/ant/js/highway.js). Neither gives g(1..5) or a seed with fewer than 12 non-zero cells. g(0) is not claimed as new.
