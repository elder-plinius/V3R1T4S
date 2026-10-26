# The record we beat

Record: p_c^site(Z^3) > 0.2522, A. Georgakopoulos and C. Panagiotis. It comes from their inequality
a(Z^3) >= f(r(p_c)), with f(r) = (1+r)^(1+r) / r^r and r(p) = (1-p)/p, together with Barequet and Shalah's
site-animal growth bound a(Z^3) < 9.3835. That gives p_c > 1/(1 + f^-1(9.3835)) = 0.252265..., stated as 0.2522.

Fetches (one plain request each):
- Journal version, Combin. Probab. Comput. 32 (2023) 912-955, doi 10.1017/S0963548323000214:
  https://www.cambridge.org/core/services/aop-cambridge-core/content/view/96D87E5F67E90E4E781BDE8108513657/S0963548323000214a.pdf/on-the-exponential-growth-rates-of-lattice-animals-and-interfaces.pdf
  - fetched about 2026-10-19T09:10Z by the NOVELTY skeptic (web-fetch tool), HTTP 200, 878014 bytes;
  - sha256 f474eb138f13fd22073b49a7f7e21a4d9297db7144ae417caa5c2b3892be38d2.
  - Extracted:
    - abstract: "We obtain the rigorous lower bound pc(Z3) > 0.2522 for 3-dimensional site percolation.";
    - Section 7, eq. (11) and Theorem 7.1: "We have pc(Z3) > 0.2522."
- arXiv version (Part II), https://arxiv.org/pdf/2107.06272:
  - fetched 2026-10-19T09:19:59Z by the run, HTTP 200, 229028 bytes;
  - sha256 0299c673233a5c95b76b6196592d0cc3a70a1365717976d8d448bc3397b8d016.
  - Extracted: eq. (16), "pc(Z3) > ... > 0.2522", described as "the best rigorous lower bound known".
- Gate re-fetch (the panel's fetches were more than 6 hours old), https://arxiv.org/abs/2107.06272:
  - fetched 2026-10-19T19:07:43Z, HTTP 200, 39546 bytes;
  - sha256 6bef351eb63405ef70afc759d677dc383b96e42dfc57f15a679f66c3fcd2cb6f.
  - Only version v1 is listed, and the abstract still states 0.2522.

Other bounds named for context:
- Torquato and Jiao, arXiv:1302.0332, https://arxiv.org/pdf/1302.0332:
  - fetched 2026-10-19T06:29:14Z, HTTP 200;
  - sha256 b71fb7eaacb2a804c5460c1c41b9f68d05522c410f96aeff2fb5c470500aaf16.
  - Table III, site percolation, d = 3: 0.2631578947 (5/19, Eq. (43)), 0.2 (Eq. (37)) and 0.1666666666 (Eq. (29)).
  - Only Eq. (29) is proved there. The others are left for "a future publication".
- Poenitz and Tittmann, EJC 7 (2000) R21, https://www.combinatorics.org/ojs/index.php/eljc/article/download/v7i1r21/pdf:
  - fetched 2026-10-19T06:29:12Z, HTTP 200;
  - sha256 ccd467b28d9d371d12a3e8187dfba8ea35acc0a724e4b490e45c324fdc6d224f.
  - mu(Z^3) <= 4.7387, so p_c >= 1/mu = 0.21102... (the older bound).

The NOVELTY skeptic's search (panel/novelty.md) covered:
- arXiv through 2026-10;
- polycube growth-constant bounds, which would move the record;
- proofs of 5/19;
- this repository's TROPHY_CASE.md and open pull requests.
It found nothing at or above 0.263376.
