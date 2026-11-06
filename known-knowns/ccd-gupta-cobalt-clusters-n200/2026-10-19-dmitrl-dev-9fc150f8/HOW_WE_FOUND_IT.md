# How we found it (contributor text, unverified)

The bank lists an audit of this table as partial win p1. The table page gives no potential parameters, so the first
step was calibration: the Cleri-Rosato cobalt values, in units of r0, reproduce the ten Co.zip energies of
Co/Energy.txt to their six printed decimals. The posted table coordinates have six decimals and are not stationary
points (gradient norms up to about 2e-2), which is why eight of them miss their posted energy by more than 1e-5 eV as
posted, while all of them land on it after a local polish.

We also tried to beat the table (one-atom growth and etching from every neighbour, monotonic basin hopping for the
largest sizes, and carrying the decahedral motif of the Co.zip improvements to nearby sizes) for about one hour on a
laptop. Nothing beat it; the closest misses were N = 177 (0.00058 eV above) and N = 161 (0.0018 eV above). The logs
are in how-we-built-it/logs/.
