# Receipts: real output of verify-it-yourself/run_checks.sh

Recorded 2026-10-14T07:37:07Z on the contributor's machine (Linux, 4 cores, 15 GB), PHYSLIB = a Physlib checkout at be0f21e5002d6d73b87f2055530c1e8bf7151546 built with Lean 4 v4.34.1. Machine paths of the checker's scratch folder are shown as [scratch].

## 1. The package as shipped (exit 0, 39 s)

```
physlib commit: be0f21e5002d6d73b87f2055530c1e8bf7151546
object sha256: 8bef4eda0ca4af1b97b2b4911b75917a647fb74d73b3d56273c6779c313dc38d
spec compile: exit 0
candidate compile: exit 0
check file: exit 0
'V3R1T4S_check' depends on axioms: [propext, Classical.choice, Quot.sound]
axioms: ['Classical.choice', 'Quot.sound', 'propext']
PASS
```

## 2. Control: one digit of the object changed (exit 1, 26 s)

The middle ASCII digit of object/RestrictedIsConnected.lean (line 150) was changed from 1 to 0 in a copy, the same corruption repo/kit/check_run.py applies to text objects (it does not scan .lean files itself).

```
physlib commit: be0f21e5002d6d73b87f2055530c1e8bf7151546
object sha256: 12d928c22ea1a24b68e8bd8c73870e919eb1a020237687a14d44933a6c188db8
spec compile: exit 0
candidate compile: exit 1
[scratch]/V3R1T4SClaim.lean:152:40: error: Tactic `rewrite` failed: Did not find an occurrence of the pattern
  (hh w * A) *ᵥ Pi.single i 1
in the target expression
  hh (Pi.single z 1) *ᵥ (hh w * A) *ᵥ Pi.single i 0 = Pi.single i 1

n : ℕ
P : Matrix (Fin n) (Fin n) ℝ → Prop
h1 : P 1
hstep : 1 < n → ∀ (u v : Fin n → ℝ), u ≠ 0 → v ≠ 0 → ∀ B ∈ specialOrthogonalGroup (Fin n) ℝ, P B → P (hh u * hh v * B)
k : ℕ
ih : ∀ A ∈ specialOrthogonalGroup (Fin n) ℝ, (∀ (i : Fin n), k ≤ ↑i → A *ᵥ Pi.single i 1 = Pi.single i 1) → P A
A : Matrix (Fin n) (Fin n) ℝ
hA : A ∈ specialOrthogonalGroup (Fin n) ℝ
hfix : ∀ (i : Fin n), k + 1 ≤ ↑i → A *ᵥ Pi.single i 1 = Pi.single i 1
hAo : A ∈ orthogonalGroup (Fin n) ℝ
hdet : A.det = 1
hk : k < n
kk : Fin n := ⟨k, hk⟩
hkk : kk = ⟨k, hk⟩
a : Fin n → ℝ := A *ᵥ Pi.single kk 1
ha_def : a = A *ᵥ Pi.single kk 1
ha : ¬a = Pi.single kk 1
w : Fin n → ℝ := a - Pi.single kk 1
hw_def : w = a - Pi.single kk 1
hw : w ≠ 0
ha_norm : a ⬝ᵥ a = Pi.single kk 1 ⬝ᵥ Pi.single kk 1
hperp : ∀ (i : Fin n), k + 1 ≤ ↑i → w ⬝ᵥ Pi.single i 1 = 0
hHa : hh w *ᵥ a = Pi.single kk 1
hfixHA : ∀ (i : Fin n), k ≤ ↑i → (hh w * A) *ᵥ Pi.single i 1 = Pi.single i 1
hk0 : k > 0
z : Fin n := ⟨0, ⋯⟩
hz_def : z = ⟨0, ⋯⟩
hz : Pi.single z 1 ≠ 0
A2 : Matrix (Fin n) (Fin n) ℝ := hh (Pi.single z 1) * (hh w * A)
hA2_def : A2 = hh (Pi.single z 1) * (hh w * A)
hdet2 : A2.det = 1
hA2 : A2 ∈ specialOrthogonalGroup (Fin n) ℝ
i : Fin n
hi : k ≤ ↑i
⊢ hh (Pi.single z 1) *ᵥ (hh w * A) *ᵥ Pi.single i 0 = Pi.single i 1
[scratch]/V3R1T4SClaim.lean:165:73: error: Application type mismatch: The argument
  hfix2
has type
  ∀ (i : Fin n), k ≤ ↑i → A2 *ᵥ Pi.single i 0 = Pi.single i 1
but is expected to have type
  ∀ (i : Fin n), k ≤ ↑i → A2 *ᵥ Pi.single i 1 = Pi.single i 1
in the application
  ih A2 hA2 hfix2

problem: candidate does not compile cleanly
FAIL
```
