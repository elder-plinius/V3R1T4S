# The record we beat (table snapshot)

Sequence: OEIS A054759, "Number of Eulerian orientations of the n X n square lattice (with
wrap-around), i.e., number of arrow configurations on n X n grid that satisfy the square ice rule."
OFFSET 1,1.

| what | value |
|---|---|
| URL | https://oeis.org/A054759 (entry), https://oeis.org/A054759/b054759.txt (b-file) |
| fetch 1 (scout) | 2026-11-04T17:31:03Z, HTTP 200, entry sha256 cf230a3fe4a4d3d989df8ee637165ec6fcc8f73dedd8a704cdc1d0e339e86094, b-file sha256 26a837111876762bf9d1c5892c21ec1a15c36e00b0ee9e45bd2c389741cbfada |
| fetch 2 (pre-claim) | 2026-11-04T18:09:53Z, HTTP 200, entry sha256 92676015f44762902bebd7d7a05791c70854b87a3b53583e34b31b6eb5eb540f |
| panel fetch (novelty lane) | 2026-11-04, HTTP 200 (see panel/novelty.md) |
| published frontier (the cell we beat) | a(14) = 15844635835975276495290739119895808472 (Brendan McKay, Apr 18 2024) |
| published DATA (the extracted cells) | 4, 18, 148, 2970, 143224, 16448400, 4484823396, 2901094068042, 4448410550095612, 16178049740086515288, 139402641051212392498528, 2849295959501939989625992464, 137950545200232788276834783781648, 15844635835975276495290739119895808472 (n = 1..14) |
| the claimed cell before the claim | a(15): ABSENT from live DATA and b-file (verified in all fetches above) |
| growth constant (quoted in the entry) | lim a(n)^(1/n^2) = (4/3)^(3/2) (Lieb); ln = 0.431523058... |

Never the pages themselves; the extracted cells and the fetch facts only.
