# Square-Grid Lattice Gas Exact OEIS Counts — World Records A054759(15, 16) & Row 28 Tables

## What
Partial win p1: New world-record exact terms a(15) (43 digits) and a(16) (49 digits) of OEIS A054759 (square ice / Eulerian orientations on n x n torus), reproducing McKay (2024) a(1..14) exactly and converging to Lieb's constant; and Partial win p2: Row 28 extensions of rectangular tables A089980 (k=1..20) and A210662 (k=1..18). Full solution A028420(28) is in progress and not claimed.

## Check it yourself
Run the standalone checker from this package directory:
```sh
sh verify-it-yourself/run_checks.sh
```
- Expected last line: `PASS`
- Rough laptop time: < 1 second (pure Python standard library)

## Compared to
- **Table / Source**: OEIS A054759 (b-file b054759.txt, Brendan McKay 2024)
- **Cell**: $a(14)$ ($n=14$, 38 decimal digits)
- **Published Value**: `15844635835975276495290739119895808472`
- **URL**: https://oeis.org/A054759/b054759.txt
- **Fetch Time**: 2026-10-29T08:06:00Z (HTTP 200, SHA256: `26a837111876762bf9d1c5892c21ec1a15c36e00b0ee9e45bd2c389741cbfada`)

## Not claimed
- Full solution $A028420(28)$ (Monomer-dimer count on $28 \times 28$ torus): State space requires $2^{28}$ elements ($2.15$ GB), requiring sustained multi-prime GPU/cluster execution. It is in progress and not claimed.

## Credits
- Brendan McKay, OEIS A054759 (terms $a(1..14)$)
- Elliott H. Lieb, "Residual Entropy of Square Ice", *Physical Review* 162 (1967)
- N. J. A. Sloane and The OEIS Foundation (database curation)
