# Reproduce

Run from a copy of this folder. Needs only Python 3 (standard library; no numpy). `PY` is the Python. On a 2018
desktop, every step takes under a minute.

## 0. Integrity
    python -c "import hashlib;[print('BAD',l.split()[1]) for l in open('MANIFEST.sha256') if hashlib.sha256(open(l.split()[1],'rb').read()).hexdigest()!=l.split()[0]];print('manifest checked')"

## 1. The certificate (exact)
    $PY code/cert.py 4433/10000 3 bound_check.json
Expected (outputs/cert_output.txt):
    depth 0: worst margin -1.207390163e-03 ... -> fail
    depth 1: worst margin -4.498328179e-05 ... -> fail
    depth 2: worst margin 1.362252386e-04 ... -> PASS
    depth 3: worst margin 1.658527535e-04 ... -> PASS
    certified p_c >= 5567/10000: True
bound_check.json must equal result/bound.json, including the exact fractions.

## 2. The independent implementation (exact, no rounding, does not import window.py)
    $PY code/independent/indep.py margins 3 4433/10000
Expected (outputs/indep_margins_output.txt): depth 2 exact worst margin 1.362252387e-04, and depth 3
1.658527536e-04. The window.py values differ only in the last printed digit, because of its outward rounding (2^-40
grid), which can only lower a margin.

## 3. Depth 0 is the 1996 paper
    $PY code/vdbe1996.py
Expected: "table rows reproduced: 13 of 13" and "CERTIFIED (exact rational check at p = 444/1000): p_c^site(Z^2) >= 0.556: True".
    $PY code/window.py 0 4/10 4442/10000
Expected: "depth 0: check passes for p >= 443917087/1000000000, so p_c(S) >= 1 - p = 0.556082913".

## 4. Consistency checks
    $PY code/validate.py 4433/10000 300 2
Expected: root step worst margin 1.470119e-02 over 166 increasing events, and "random explicit trees: ... OK".

## 5. Optional: best bound per depth
    $PY code/window.py 3
Expected: the depth-3 line "check passes for p >= 443214911/1000000000, so p_c(S) >= 1 - p = 0.556785089".
