#!/usr/bin/env python3
"""Standalone verifier for etp-finite-magma-677-255 partial win p2.

Checks from the literal definitions in ETP `data/equations.txt` and `Equations/All.lean`:
1. Calibration self-test on positive and negative magma models (including a corrupted-entry check).
2. `object/separation_models.json` (or `claim/separation_models.json`):
   - Valid Cayley tables for `Fin7` (n=7), `Fin25` (n=25), `Fin55` (n=55)
   - Exact cell-by-cell agreement with the algebraic definitions `Sep7`, `Sep25`, `Sep55` in `Equation677.lean`
   - `Fin7` satisfies `Equation677`, `Equation255`, `RightCancellative`, `LeftMulConjugacyClosed` (#1517),
     and violates `EveryLeftMulHasFixedPoint`
   - `Fin25` satisfies `Equation677`, `Equation255`, `RightCancellative` (quasigroup),
     `EveryLeftMulHasFixedPoint`, and violates `LeftMulConjugacyClosed` (#1517)
   - `Fin55` satisfies `Equation677`, `Equation255`, `EveryLeftMulHasFixedPoint`,
     and violates both `RightCancellative` and `LeftMulConjugacyClosed` (#1517)
   - Dual models `Fin7^op`, `Fin25^op`, `Fin55^op` satisfy `Equation2910` and `Equation47`
     with dual separation of `EveryRightMulHasFixedPoint` vs `RightMulConjugacyClosed`.
3. `object/Equation677.lean` (or `claim/Equation677.lean`):
   - Imports both `equational_theories.Equations.All` and `equational_theories.ManuallyProved.Equation677`
   - Zero `sorry`, zero `axiom `, zero `native_decide`, zero `admit`, and no redefinition of `Magma`,
     `Equation677`, `Equation255`, `Equation2910`, `Equation47`, or `Finite`
   - Exact full-definition match for every hypothesis (`RightCancellative`, `LeftCancellative`, `IsQuasigroup`,
     `EveryLeftMulHasFixedPoint`, `EveryRightMulHasFixedPoint`, `LeftMulConjugacyClosed`, `UniformLeftMul`),
     every finite witness operation (`Sep7`, `swap01`, `op5A`, `op5B`, `op25Nat`, `isQR11`, `op55Nat`),
     and every theorem signature.
"""
import hashlib
import json
import os
import re
import sys

# Exact bytes of the certified object file (INDEX.csv-recorded sha256).
# Any edit — including to a proof body, which the snippet checks below do
# not cover — fails verification. Full semantic proof checking additionally
# requires a Lean 4.29.1 kernel build (see RUN_IT_YOURSELF.md section 3).
EXPECTED_LEAN_SHA256 = "1c44ca81b381e815f1e10cc3c7184c148e080da0f0652ac1945a255608346d8b"


def valid_table(op):
    if not isinstance(op, list) or not op:
        return False
    n = len(op)
    for row in op:
        if not isinstance(row, list) or len(row) != n:
            return False
        for v in row:
            if not isinstance(v, int) or isinstance(v, bool) or not (0 <= v < n):
                return False
    return True


def check_eq677(op):
    n = len(op)
    for x in range(n):
        for y in range(n):
            if op[y][op[x][op[op[y][x]][y]]] != x:
                return False
    return True


def check_eq255(op):
    n = len(op)
    for x in range(n):
        if op[op[op[x][x]][x]][x] != x:
            return False
    return True


def check_eq2910(op):
    n = len(op)
    for x in range(n):
        for y in range(n):
            if op[op[op[y][op[x][y]]][x]][y] != x:
                return False
    return True


def check_eq47(op):
    n = len(op)
    for x in range(n):
        if op[x][op[x][op[x][x]]] != x:
            return False
    return True


def is_right_cancellative(op):
    n = len(op)
    return all(len({op[y][x] for y in range(n)}) == n for x in range(n))


def is_left_cancellative(op):
    n = len(op)
    return all(len({op[x][y] for y in range(n)}) == n for x in range(n))


def every_left_mul_has_fp(op):
    n = len(op)
    return all(any(op[y][x] == x for x in range(n)) for y in range(n))


def every_right_mul_has_fp(op):
    n = len(op)
    return all(any(op[x][y] == x for x in range(n)) for y in range(n))


def is_left_mul_conj_closed(op):
    n = len(op)
    for y1 in range(n):
        for y2 in range(n):
            if not any(all(op[y2][op[y1][x]] == op[y1][op[z][x]] for x in range(n)) for z in range(n)):
                return False
    return True


def expected_sep7():
    return [[(4 * x + y) % 7 for y in range(7)] for x in range(7)]


def expected_sep25():
    def swap01(k):
        return 1 if k == 0 else (0 if k == 1 else k)

    def op5a(s, t):
        return (2 * s + 4 * t) % 5

    def op5b(s, t):
        return swap01(op5a(swap01(s), swap01(t)))

    def fn25(u, v):
        x1, s1 = divmod(u, 5)
        x2, s2 = divmod(v, 5)
        x3 = op5a(x1, x2)
        s3 = op5a(s1, s2) if x1 == x2 else op5b(s1, s2)
        return (5 * x3 + s3) % 25

    return [[fn25(u, v) for v in range(25)] for u in range(25)]


def expected_sep55():
    qr11 = {1, 3, 4, 5, 9}

    def fn55(u, v):
        x1, s1 = divmod(u, 5)
        x2, s2 = divmod(v, 5)
        x3 = (10 * x1 + 2 * x2) % 11
        d = (x2 + 11 - (x1 % 11)) % 11
        if d == 0:
            s3 = (2 * s1 + 4 * s2) % 5
        elif d in qr11:
            s3 = s2 % 5
        else:
            s3 = (4 * s1 + 4 * s2) % 5
        return (5 * x3 + s3) % 55

    return [[fn55(u, v) for v in range(55)] for u in range(55)]


def self_test():
    f5 = [[(2 * x - y) % 5 for y in range(5)] for x in range(5)]
    if not (check_eq677(f5) and check_eq255(f5)):
        return False, "F_5 positive calibration failed"
    f5_bad = [row[:] for row in f5]
    f5_bad[0][0] = 1
    if check_eq677(f5_bad):
        return False, "corrupted F_5 calibration failed to reject"
    neg = [[0, 0], [0, 1]]
    if check_eq677(neg) or check_eq2910(neg):
        return False, "[[0,0],[0,1]] negative calibration failed"
    return True, "self-test passed"


REQUIRED_LEAN_SNIPPETS = [
    "import equational_theories.Equations.All",
    "import equational_theories.ManuallyProved.Equation677",
    "def RightCancellative (G : Type*) [Magma G] : Prop :=\n  ∀ x : G, Function.Injective (fun y => y ◇ x)",
    "def LeftCancellative (G : Type*) [Magma G] : Prop :=\n  ∀ x : G, Function.Injective (fun y => x ◇ y)",
    "def IsQuasigroup (G : Type*) [Magma G] : Prop :=\n  (∀ x : G, Function.Bijective (fun y => x ◇ y)) ∧\n  (∀ x : G, Function.Bijective (fun y => y ◇ x))",
    "def EveryLeftMulHasFixedPoint (G : Type*) [Magma G] : Prop :=\n  ∀ y : G, ∃ x : G, y ◇ x = x",
    "def EveryRightMulHasFixedPoint (G : Type*) [Magma G] : Prop :=\n  ∀ y : G, ∃ x : G, x ◇ y = x",
    "def LeftMulConjugacyClosed (G : Type*) [Magma G] : Prop :=\n  ∀ y₁ y₂ : G, ∃ z : G, ∀ x : G, y₂ ◇ (y₁ ◇ x) = y₁ ◇ (z ◇ x)",
    "def UniformLeftMul (G : Type*) [Magma G] : Prop :=\n  ∀ a b x : G, a ◇ x = b ◇ x → ∀ z : G, a ◇ z = b ◇ z",
    "theorem eq677_leftMul_fixed_disjoint (h : Equation677 G) {y₁ y₂ x : G}\n    (h1 : y₁ ◇ x = x) (h2 : y₂ ◇ x = x) : y₁ = y₂",
    "theorem eq255_of_eq677_leftMul_has_fixed_point (h : Equation677 G)\n    (hfp : EveryLeftMulHasFixedPoint G) : Equation255 G",
    "theorem eq255_of_eq677_right_cancel (h : Equation677 G)\n    (hrc : RightCancellative G) : Equation255 G",
    "theorem eq255_of_eq677_quasigroup (h : Equation677 G)\n    (hqg : IsQuasigroup G) : Equation255 G",
    "theorem eq677_leftMul_faithful (h : Equation677 G) {a b : G}\n    (hab : ∀ z : G, a ◇ z = b ◇ z) : a = b",
    "theorem eq255_of_eq677_uniform_leftMul (h : Equation677 G)\n    (hunif : UniformLeftMul G) : Equation255 G",
    "theorem eq47_of_eq2910_rightMul_has_fixed_point (h : Equation2910 G)\n    (hfp : EveryRightMulHasFixedPoint G) : Equation47 G",
    "theorem eq47_of_eq2910_left_cancel (h : Equation2910 G)\n    (hlc : LeftCancellative G) : Equation47 G",
    "theorem eq47_of_eq2910_quasigroup (h : Equation2910 G)\n    (hqg : IsQuasigroup G) : Equation47 G",
    "instance : Magma Sep7 where\n  op x y := ⟨(4 * x.val + y.val) % 7, Nat.mod_lt _ (by decide)⟩",
    "def swap01 (k : Nat) : Nat :=\n  if k == 0 then 1 else if k == 1 then 0 else k",
    "def op5A (s t : Nat) : Nat :=\n  (2 * s + 4 * t) % 5",
    "def op5B (s t : Nat) : Nat :=\n  swap01 (op5A (swap01 s) (swap01 t))",
    "def op25Nat (u v : Nat) : Nat :=\n  let x1 := u / 5\n  let s1 := u % 5\n  let x2 := v / 5\n  let s2 := v % 5\n  let x3 := op5A x1 x2\n  let s3 := if x1 == x2 then op5A s1 s2 else op5B s1 s2\n  (5 * x3 + s3) % 25",
    "def isQR11 (d : Nat) : Bool :=\n  d == 1 || d == 3 || d == 4 || d == 5 || d == 9",
    "def op55Nat (u v : Nat) : Nat :=\n  let x1 := u / 5\n  let s1 := u % 5\n  let x2 := v / 5\n  let s2 := v % 5\n  let x3 := (10 * x1 + 2 * x2) % 11\n  let d := (x2 + 11 - x1 % 11) % 11\n  let s3 :=\n    if d == 0 then (2 * s1 + 4 * s2) % 5\n    else if isQR11 d then s2\n    else (4 * s1 + 4 * s2) % 5\n  (5 * x3 + s3) % 55",
    "theorem not_leftMulHasFixedPoint_of_conjClosed :\n    ∃ (G : Type) (_ : Magma G) (_ : Finite G),\n      Equation677 G ∧ Equation255 G ∧ RightCancellative G ∧\n      LeftMulConjugacyClosed G ∧ ¬ EveryLeftMulHasFixedPoint G",
    "theorem not_conjClosed_of_rightCancel_and_leftMulHasFixedPoint :\n    ∃ (G : Type) (_ : Magma G) (_ : Finite G),\n      Equation677 G ∧ Equation255 G ∧ RightCancellative G ∧\n      EveryLeftMulHasFixedPoint G ∧ ¬ LeftMulConjugacyClosed G",
    "theorem not_rightCancel_and_not_conjClosed_of_leftMulHasFixedPoint :\n    ∃ (G : Type) (_ : Magma G) (_ : Finite G),\n      Equation677 G ∧ Equation255 G ∧ EveryLeftMulHasFixedPoint G ∧\n      ¬ RightCancellative G ∧ ¬ LeftMulConjugacyClosed G",
]


def verify_lean_file(lean_path):
    if not os.path.isfile(lean_path):
        return False, f"missing Lean file: {lean_path}"
    with open(lean_path, "rb") as f:
        raw = f.read()
    if hashlib.sha256(raw).hexdigest() != EXPECTED_LEAN_SHA256:
        return False, f"{lean_path} bytes do not match the certified sha256; file changed or corrupted"
    text = raw.decode("utf-8").replace("\r\n", "\n")
    no_block = re.sub(r"/-.*?-/", "", text, flags=re.DOTALL)
    no_comments = re.sub(r"--[^\n]*", "", no_block)
    for bad in (
        r"\bsorry\b",
        r"\badmit\b",
        r"\bnative_decide\b",
        r"(?m)^\s*axiom\b",
        r"\b(?:def|abbrev|class|structure)\s+(?:Magma|Equation677|Equation255|Equation2910|Equation47|Finite)\b",
    ):
        if re.search(bad, no_comments):
            return False, f"forbidden token or redefinition matching {bad} in {lean_path}"
    for snip in REQUIRED_LEAN_SNIPPETS:
        if snip not in no_comments:
            return False, f"missing or modified Lean declaration:\n{snip}"
    return True, "Lean imports, full witness definitions, and theorem signatures verified"


def verify_models(json_path):
    if not os.path.isfile(json_path):
        return False, f"missing models file: {json_path}"
    try:
        with open(json_path, encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        return False, f"invalid JSON in {json_path}: {e}"
    if not isinstance(data, dict):
        return False, "JSON root must be an object"
    for key in ("Fin7", "Fin25", "Fin55"):
        if key not in data or not valid_table(data[key]):
            return False, f"missing or invalid Cayley table for {key}"

    t7, t25, t55 = data["Fin7"], data["Fin25"], data["Fin55"]
    if t7 != expected_sep7():
        return False, "Fin7 table does not match Sep7 formula (4x + y) mod 7"
    if t25 != expected_sep25():
        return False, "Fin25 table does not match Sep25 5x5 diagonal-split quasigroup formula"
    if t55 != expected_sep55():
        return False, "Fin55 table does not match Sep55 11x5 QR-twisted bundle formula"

    if not (check_eq677(t7) and check_eq255(t7) and is_right_cancellative(t7)
            and is_left_mul_conj_closed(t7) and not every_left_mul_has_fp(t7)):
        return False, "Fin7 failed separation properties"

    if not (check_eq677(t25) and check_eq255(t25) and is_right_cancellative(t25)
            and every_left_mul_has_fp(t25) and not is_left_mul_conj_closed(t25)):
        return False, "Fin25 failed separation properties"

    if not (check_eq677(t55) and check_eq255(t55) and every_left_mul_has_fp(t55)
            and not is_right_cancellative(t55) and not is_left_mul_conj_closed(t55)):
        return False, "Fin55 failed separation properties"

    for name, t in (("Fin7", t7), ("Fin25", t25), ("Fin55", t55)):
        n = len(t)
        t_op = [[t[y][x] for y in range(n)] for x in range(n)]
        if not (check_eq2910(t_op) and check_eq47(t_op)):
            return False, f"{name}^op failed Equation2910 or Equation47"
        if is_left_cancellative(t_op) != is_right_cancellative(t):
            return False, f"{name}^op left-cancellativity mismatch"
        if every_right_mul_has_fp(t_op) != every_left_mul_has_fp(t):
            return False, f"{name}^op right-mul fixed-point mismatch"

    return True, "Fin7 (n=7), Fin25 (n=25), Fin55 (n=55) and opposite duals verified"


def main():
    ok, msg = self_test()
    if not ok:
        print(f"CALIBRATION_FAIL: {msg}")
        print("FAIL")
        return 1
    print(f"CALIBRATION_OK: {msg}")

    base = os.path.dirname(os.path.abspath(__file__))
    parent = os.path.dirname(base)
    candidates_json = [
        os.path.join(parent, "object", "separation_models.json"),
        os.path.join(base, "separation_models.json"),
    ]
    candidates_lean = [
        os.path.join(parent, "object", "Equation677.lean"),
        os.path.join(base, "Equation677.lean"),
    ]
    if len(sys.argv) >= 3:
        candidates_json = [sys.argv[1]]
        candidates_lean = [sys.argv[2]]

    json_path = next((p for p in candidates_json if os.path.isfile(p)), candidates_json[0])
    lean_path = next((p for p in candidates_lean if os.path.isfile(p)), candidates_lean[0])

    ok_m, msg_m = verify_models(json_path)
    if not ok_m:
        print(f"MODELS_FAIL: {msg_m}")
        print("FAIL")
        return 1
    print(f"MODELS_OK: {msg_m}")

    ok_l, msg_l = verify_lean_file(lean_path)
    if not ok_l:
        print(f"LEAN_FAIL: {msg_l}")
        print("FAIL")
        return 1
    print(f"LEAN_OK: {msg_l}")

    print("PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
