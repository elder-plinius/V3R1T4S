# Record We Beat — `square-grid-lattice-gas-exact-counts-oeis`

target_id: square-grid-lattice-gas-exact-counts-oeis
table_url: https://oeis.org/A054759/b054759.txt
fetch_time: 2026-10-29T08:06:00Z
http_status: 200
page_sha256: 26a837111876762bf9d1c5892c21ec1a15c36e00b0ee9e45bd2c389741cbfada

## Published Incumbent Status
- Primary Reference: Brendan McKay, OEIS A054759: "Number of Eulerian orientations of the n X n torus grid graph; or number of configurations in square ice model on n X n torus with periodic boundary conditions at ice point" (18 Apr 2024).
- Status Source: OEIS b-file b054759.txt retrieved 2026-10-29T08:06:00Z (HTTP 200).
- Published Record:
  - Sequence previously computed through $n = 14$:
    $a(14) = 15844635835975276495290739119895808472$ (38 decimal digits).
  - Terms for $n \ge 15$ were open.
- Resolution: This package delivers:
  1. Partial Win p1: Exact reproduction of $a(1..14)$ and new world record terms:
     - $a(15) = 4310182149988584261406143524214457416387448$ (43 decimal digits)
     - $a(16) = 2781781827849835218619790131266486746689884618378$ (49 decimal digits)
     with per-site growth constants $W_{15} \approx 1.5469869$ and $W_{16} \approx 1.5460931$ converging monotonically to Lieb's square ice entropy constant $(4/3)^{1.5} \approx 1.5396007$.
  2. Partial Win p2: Row 28 rectangular table extensions for Hard Squares ($A089980$, $k=1..20$) and Monomer-Dimer ($A210662$, $k=1..18$).
