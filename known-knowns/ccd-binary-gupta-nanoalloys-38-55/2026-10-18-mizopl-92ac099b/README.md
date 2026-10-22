# Binary Gupta 55-Atom Cu_n Ag_{55-n} Nanoalloy Global Minima (Cu39Ag16 dE = -1.18984440 eV + 7 Additional Compositions)

## What

Eight certified 55-atom Cu_n Ag_{55-n} Gupta nanoalloy local minima in claim/ headlined by claim/Cu39Ag16_improved.txt (6,149 bytes, sha256 92ac099b6963dcaedd5dbc1000731a5a87c99fc6e208b30475c6850e420a991d, E* = -163.8021426482 eV vs archive -162.6122982488 eV, dE = -1.18984440 eV) along with claim/Cu34Ag21_improved.txt (-0.95474003 eV), claim/Cu33Ag22_improved.txt (-0.92199695 eV), claim/Cu31Ag24_improved.txt (-0.79798867 eV), claim/Cu22Ag33_improved.txt (-0.23167311 eV), claim/Cu20Ag35_improved.txt (-0.12881511 eV), claim/Cu15Ag40_improved.txt (-0.12624733 eV), and claim/Cu17Ag38_improved.txt (-0.06457801 eV), calibrated across all 56 files of claim/CuAg_55.rar to 4.890e-09 eV (within the 1e-6 eV tolerance), polished in 30-digit mpmath to gradient norm at most 6.34e-23 (below the 1e-10 threshold), verified by 165x165 analytical Hessians with 6 zero modes (magnitude at most 2.51e-15, below 1e-6) and 0 negative eigenvalues, and separated from the polished archive structures by at least 0.06457801 eV (above the 1e-4 eV threshold).

Path note: the sentence above is quoted word for word from `panel/gate.md`, and it names the panel's `claim/` folder. In this package the same files, with identical bytes, are in `object/` (headlined by `object/Cu39Ag16_improved.txt`).

## Check it yourself

From this package folder, run:

```sh
sh verify-it-yourself/run_checks.sh
```

- **Requirements**: `python3` with `numpy`, `scipy`, `mpmath`, and `bsdtar`.
- **Rough laptop time**: about 6 seconds.
- **Expected last line**: `ALL CHECKS PASS`

## Compared to

| Source | Cell | Listed value (eV) | Ours (eV) | Delta E (eV) | URL | UTC fetch time |
|---|---|---:|---:|---:|---|---|
| CCD `CuAg_55.rar` (Lai, Huang & Xu 2011) | `Cu39Ag16` | `-162.61229825` | `-163.80214265` | `-1.18984440` | https://www-wales.ch.cam.ac.uk/~wales/CCD/CuAg_55.rar | 2026-10-18T21:14:16Z |
| CCD `CuAg_55.rar` (Lai, Huang & Xu 2011) | `Cu34Ag21` | `-160.81218484` | `-161.76692486` | `-0.95474003` | https://www-wales.ch.cam.ac.uk/~wales/CCD/CuAg_55.rar | 2026-10-18T21:14:16Z |
| CCD `CuAg_55.rar` (Lai, Huang & Xu 2011) | `Cu33Ag22` | `-160.43136967` | `-161.35336662` | `-0.92199695` | https://www-wales.ch.cam.ac.uk/~wales/CCD/CuAg_55.rar | 2026-10-18T21:14:16Z |
| CCD `CuAg_55.rar` (Lai, Huang & Xu 2011) | `Cu31Ag24` | `-159.69487106` | `-160.49285973` | `-0.79798867` | https://www-wales.ch.cam.ac.uk/~wales/CCD/CuAg_55.rar | 2026-10-18T21:14:16Z |
| CCD `CuAg_55.rar` (Lai, Huang & Xu 2011) | `Cu22Ag33` | `-156.38507389` | `-156.61674699` | `-0.23167311` | https://www-wales.ch.cam.ac.uk/~wales/CCD/CuAg_55.rar | 2026-10-18T21:14:16Z |
| CCD `CuAg_55.rar` (Lai, Huang & Xu 2011) | `Cu20Ag35` | `-155.56958143` | `-155.69839654` | `-0.12881511` | https://www-wales.ch.cam.ac.uk/~wales/CCD/CuAg_55.rar | 2026-10-18T21:14:16Z |
| CCD `CuAg_55.rar` (Lai, Huang & Xu 2011) | `Cu15Ag40` | `-153.49887624` | `-153.62512358` | `-0.12624733` | https://www-wales.ch.cam.ac.uk/~wales/CCD/CuAg_55.rar | 2026-10-18T21:14:16Z |
| CCD `CuAg_55.rar` (Lai, Huang & Xu 2011) | `Cu17Ag38` | `-154.40077125` | `-154.46534927` | `-0.06457801` | https://www-wales.ch.cam.ac.uk/~wales/CCD/CuAg_55.rar | 2026-10-18T21:14:16Z |

Snapshot metadata, with HTTP status and page sha256: `the-record-we-beat/README.md`.

## Not claimed

- Global optimality on the continuous non-convex potential energy surface is not proved; these are certified lower-energy putative global minima (strict local minima verified by 30-digit `mpmath` stationarity and positive-definite $165 \times 165$ analytical Hessians modulo the 6 rigid-body zero modes).
- Not peer reviewed. Checked by a three-skeptic panel (`panel/`) and by the standalone checker shipped here.

## Credits

- **Xiangjing Lai, Wenqi Huang, and Ruchu Xu**, *J. Chem. Phys.* **135**, 164109 (2011), authors of the Cambridge Cluster Database `CuAg_55.rar` archive compared against: https://www-wales.ch.cam.ac.uk/~wales/CCD/CuAg_55.rar.
- **S. Nunez and Roy L. Johnston**, *J. Phys. Chem. C* **114**, 13255–13266 (2010), and **A. Rapallo, G. Rossi, R. Ferrando, A. Fortunelli, B. C. Curley, L. D. Lloyd, G. M. Tarbuck, and R. L. Johnston**, *J. Chem. Phys.* **122**, 194308 (2005), source of the Cu-Ag Gupta parameterization cited in `CuAg55/reference.txt`.
- **David J. Wales et al.**, the Cambridge Cluster Database: https://www-wales.ch.cam.ac.uk/CCD.html.
- Contributor credit: `mizopl`.
