# Record We Beat — `shapley-network-design-pos-three-players`

target_id: shapley-network-design-pos-three-players
table_url: https://www2.mathematik.tu-darmstadt.de/%7Edisser/pdfs/DisserFeldmannKlimmMihalak15.pdf
fetch_time: 2026-10-28T22:30:00Z
http_status: 200
page_sha256: d8199738f6b15e47854ebaa69818b2c2ecf99a365ba60a28f74a362fcda645c7

## Published Incumbent Status
- Primary Reference: Y. Disser, A. E. Feldmann, M. Klimm, and M. Mihalák, "Improving the H_k-bound on the price of stability in undirected Shapley network design games", Theoretical Computer Science 2015 (arXiv:1211.2090).
- Published Record Lower Bound: Disser et al. constructed an explicit 5-vertex undirected 3-player instance with edge costs {c_01: 549, c_02: 113, c_13: 318, c_14: 664, c_23: 556, c_24: 277, c_34: 418} achieving Price of Stability PoS = 1769/1126 approx 1.57104796.
- Upper Bound / Potential Optimum: V. Bilò and G. Bove (2011) proved an upper bound of 286/175 approx 1.63428571 for potential-optimal equilibria.
- Resolution: We discovered an exact integer edge-cost assignment on the 5-vertex topology:
  {c_01: 2928, c_02: 599, c_13: 1692, c_14: 3545, c_23: 2967, c_24: 1483, c_34: 2226}
  achieving unique pure Nash equilibrium cost 9440 and social optimum cost 6000, yielding exact Price of Stability:
  PoS = 9440/6000 = 118/75 = 1.57333333... > 1769/1126 = 1.57104796... (+193/84450).
