# Verification Receipts

Command: `sh verify-it-yourself/run_checks.sh`

Only the 11 new putative global minimum structures (`Mo_75`, `Mo_90`, `Fe_86`, `Fe_87`, `Fe_90`, `Fe_91`, `Fe_92`, `Fe_96`, `Fe_97`, `Fe_98`, `Fe_100`) are recomputed from their coordinates; the calibration, polished-CCD energies, and 196-row audit are stored values checked against hashes, and reproducing them from coordinates requires the cited `points.tgz` archives.

```
Checked stored calibration/audit rows for Mo (98 files, max |dE|=9.77e-11 eV) and Fe (98 files, max |dE|=9.42e-11 eV) < 1e-7 eV (reproducing from coordinates needs cited points.tgz archives).
Recomputed Mo_75 : E* = -439.5640256673 eV (CCD = -439.4197932305, dE =  -0.144232 eV, ||g||_f64=1.23e-13, ||g||_dec=9.18e-28, ||H Q0||=9.03e-15)
Recomputed Mo_90 : E* = -533.2142178271 eV (CCD = -532.7899433214, dE =  -0.424275 eV, ||g||_f64=1.26e-13, ||g||_dec=1.20e-27, ||H Q0||=8.62e-15)
Recomputed Fe_86 : E* = -312.7609188697 eV (CCD = -312.6006513052, dE =  -0.160268 eV, ||g||_f64=2.36e-14, ||g||_dec=1.10e-28, ||H Q0||=5.75e-15)
Recomputed Fe_87 : E* = -316.6115843892 eV (CCD = -316.4759023549, dE =  -0.135682 eV, ||g||_f64=2.30e-14, ||g||_dec=9.84e-29, ||H Q0||=5.81e-15)
Recomputed Fe_90 : E* = -327.9864583540 eV (CCD = -327.8503707653, dE =  -0.136088 eV, ||g||_f64=2.86e-14, ||g||_dec=1.01e-28, ||H Q0||=5.93e-15)
Recomputed Fe_91 : E* = -332.0252838865 eV (CCD = -331.9072022873, dE =  -0.118082 eV, ||g||_f64=2.36e-14, ||g||_dec=1.01e-28, ||H Q0||=5.73e-15)
Recomputed Fe_92 : E* = -335.9470373457 eV (CCD = -335.9034309081, dE =  -0.043606 eV, ||g||_f64=2.76e-14, ||g||_dec=1.07e-28, ||H Q0||=5.39e-15)
Recomputed Fe_96 : E* = -351.2401491626 eV (CCD = -351.2027399452, dE =  -0.037409 eV, ||g||_f64=2.38e-14, ||g||_dec=1.14e-28, ||H Q0||=5.73e-15)
Recomputed Fe_97 : E* = -355.1385265715 eV (CCD = -354.9919830214, dE =  -0.146544 eV, ||g||_f64=2.76e-14, ||g||_dec=1.18e-28, ||H Q0||=5.98e-15)
Recomputed Fe_98 : E* = -359.0082985625 eV (CCD = -358.8031191667, dE =  -0.205179 eV, ||g||_f64=2.26e-14, ||g||_dec=1.00e-28, ||H Q0||=5.57e-15)
Recomputed Fe_100: E* = -366.6082856510 eV (CCD = -366.5806583336, dE =  -0.027627 eV, ||g||_f64=2.64e-14, ||g||_dec=1.14e-28, ||H Q0||=5.55e-15)
Recomputed only the 11 new Finnis-Sinclair putative global minimum structures; calibration, polished-CCD energies, and 196-row audit are stored values checked against hashes (reproducing them needs the cited points.tgz archives).
PASS
```
