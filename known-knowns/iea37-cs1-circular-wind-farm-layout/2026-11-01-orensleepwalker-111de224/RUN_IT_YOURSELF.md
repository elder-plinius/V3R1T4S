# Verify the fixed object

From this package folder, run:
```sh
sh verify-it-yourself/run_checks.sh
```
Expected scalar AEP:421304.60329359624MWh, maximum radius1299.999900000054m, minimum spacing580.4318820195579m, and16 assigned distances strictly above50m for each of the two comparators. Last output line:PASS. The checker first checks the frozen-object hash, then strict geometry and energy, then hash-pinned reference assignments with primal-dual certificates. It verifies numerical eligibility; the dated independent panel covers live comparator completeness and bounded novelty.

The checker requires internet access for its first two public reference downloads. It never retries a denied request or executes fetched data. The built-in REFERENCES mapping states both exact URLs and SHA256 values. To verify offline after obtaining those exact files separately, place them together with filenames iea37-par12-opt16.yaml and pr578-layout16.json, then use:
```sh
python3 verify-it-yourself/check_layout.py --reference-dir reference-files
```
The standard-library verifier has no NumPy/SciPy/PyYAML dependency. Third-party source pages, PDFs, or datasets are not bundled.

# Rebuild the candidate
The generator alone needs the pinned NumPy and SciPy versions in how-we-built-it/requirements.txt. In a separate environment, install those requirements and run from how-we-built-it/:
```sh
python3 search_continuation.py --output generated --deadline 2099-01-01T00:00:00+00:00 --seed 20261102 --max-restarts 80 --maxiter 350
```
The count cap stops after80 restarts; the distant deadline merely avoids time expiry during a finite replay. Output generated/best.json should reproduce the same basin and AEP to numerical precision. Floating-point optimizer trajectories can vary across library/platform versions; the frozen object is authoritative. Independent replay in the saved review environment reproduced the exact coordinates in one fresh context and within1.12e-10m in another. The provided author log is corroborating history, not independent timestamp attestation.
