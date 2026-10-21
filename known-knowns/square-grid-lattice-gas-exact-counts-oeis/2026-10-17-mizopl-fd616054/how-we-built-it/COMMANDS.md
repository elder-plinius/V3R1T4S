# Commands that built the object

Pure Python 3 + numpy. No `python3 -I` (it drops the script dir from sys.path and breaks
`import sixvertex`). These are first-party scripts.

```
# reproduction gate: all published terms n=1..14 (~35 s)
python3 reproduce.py

# the two-run computation of a(15) (~12 min): RUN_A forward/closed-form 11 primes <2^20,
# RUN_B reversed-encoding/explicit-walk 12 disjoint primes <2^19; both CRT to the same value
python3 n15.py

# independent self-break: brute force n<=3, non-sector transfer matrix n<=8, independent CRT, growth
python3 break.py ../object/residues.txt
```

Files:
- `sixvertex.py` — core: sector states, two entry builders (closed-form + explicit walk), float64
  modular matpow, CRT.
- `reproduce.py` — reproduction gate checking n=1..14 against the published OEIS terms from
  https://oeis.org/A054759/b054759.txt (sha256 `26a837111876762bf9d1c5892c21ec1a15c36e00b0ee9e45bd2c389741cbfada`;
  optionally takes a local b-file path as an argument).
- `n15.py` — the two-run a(15) driver (writes residues + CRT values + the literal growth line).
- `break.py` — the step-5 self-break (independent methods from the definition).
- `PREREG.md` — the pre-registration frozen before any attack output existed.

PREREG declares `null_test: not needed because` the claim is an explicit exact integer checked by a
deterministic checker (two independent modular runs that agree + reproduction of every published term +
a CRT bound above the entropy-constant estimate), not a search or "beats chance" claim.
