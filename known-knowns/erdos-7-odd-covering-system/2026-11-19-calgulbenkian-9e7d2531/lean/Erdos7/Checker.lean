/-
Stage 2: the certificate checker.  Core Lean only (no Mathlib), natural-number arithmetic with
cleared denominators, structural recursion only, so that the kernel can evaluate it.

A band profile is a list of exponents `es` (exponent `es[m]` on the m-th odd prime `oddP m`) with a
parallel list `caps`: `caps[m] = 0` means coordinate `m` is a "pure deletion" (uniform) coordinate,
`caps[m] = c > 0` means it is a capped coordinate with cap `C_m = c/32`.
-/
namespace Erdos7

/-- The first odd primes (`0` beyond the table; the checker rejects any profile reaching a `0`). -/
def oddP : Nat → Nat
  | 0 => 3 | 1 => 5 | 2 => 7 | 3 => 11 | 4 => 13 | 5 => 17 | 6 => 19 | 7 => 23 | 8 => 29
  | 9 => 31 | 10 => 37 | 11 => 41 | 12 => 43 | 13 => 47 | _ => 0

/-- `geom p e = 1 + p + ... + p^(e-1) = (p^e - 1)/(p - 1)`. -/
def geom (p : Nat) : Nat → Nat
  | 0 => 0
  | e + 1 => p * geom p e + 1

/-- Common denominator of the tail probabilities of a coordinate. -/
def den (p e cap : Nat) : Nat := if cap = 0 then p ^ e - geom p e else 32 * p ^ e

/-- Numerator (over `den`) of the tail bound `Q(t)`:
uniform coordinate: `p^(e-t) / s`, `s = p^e - geom p e`;
capped coordinate: `min(1, C / p^t)`, `C = cap/32`. `Q(0) = 1`, `Q(t) = 0` for `t > e`. -/
def Qn (p e cap t : Nat) : Nat :=
  if t = 0 then den p e cap else if e < t then 0 else
  if cap = 0 then p ^ (e - t) else Nat.min (32 * p ^ e) (cap * p ^ (e - t))

/-- Point weights `q(t) = Q(t) - Q(t+1)`, `t = 0..e`, as numerators over `den`. -/
def qlist (p e cap : Nat) : List Nat :=
  (List.range (e + 1)).map (fun t => Qn p e cap t - Qn p e cap (t + 1))

/-- Stage loss numerator as a function of the multiplier `M = prod (1 + T_m)`:
uniform: `theta * (M - 1)`; capped: `C * (rho * M - delta)_+`. -/
def gnum (p e cap M : Nat) : Nat :=
  if cap = 0 then geom p e * (M - 1)
  else cap * (p ^ e - 1) * M - (cap - 32) * (p - 1) * p ^ e

/-- Stage loss denominator. -/
def gden (p e cap : Nat) : Nat :=
  if cap = 0 then p ^ e - geom p e else 32 * (p - 1) * p ^ e

/-- Side conditions of a coordinate. -/
def coordOK (p e cap : Nat) : Bool :=
  Nat.ble 3 p && Nat.ble 1 e && Nat.blt 0 (den p e cap) &&
  (List.range (e + 1)).all (fun t => Nat.ble (Qn p e cap (t + 1)) (Qn p e cap t)) &&
  (Nat.beq cap 0 ||
    (Nat.blt 32 cap && Nat.ble (cap * (p ^ e - 1)) ((cap - 32) * (p - 1) * p ^ e)))

/-- `wsum ws k F = sum_j ws[j] * F (k + j)`. -/
def wsum : List Nat → Nat → (Nat → Nat) → Nat
  | [], _, _ => 0
  | w :: ws, k, F => w * F k + wsum ws (k + 1) F

/-- Integer expectation of `g (M * prod (1 + T_m))` over the independent levels, as a numerator
over the product of the coordinate denominators. -/
def etL (g : Nat → Nat) : List (List Nat) → Nat → Nat
  | [], M => g M
  | q :: qs, M => wsum q 1 (fun k => etL g qs (M * k))

/-- Sum the stage losses as a running fraction `A / B` and test `A / B < 1`. -/
def stages : List Nat → List Nat → Nat → List (List Nat) → Nat → Nat → Nat → Bool
  | [], [], _, _, _, A, B => Nat.blt A B
  | e :: es, cap :: caps, i, rev, D, A, B =>
    coordOK (oddP i) e cap &&
    stages es caps (i + 1) (qlist (oddP i) e cap :: rev) (D * den (oddP i) e cap)
      (A * (D * gden (oddP i) e cap) + etL (gnum (oddP i) e cap) rev 1 * B)
      (B * (D * gden (oddP i) e cap))
  | _, _, _, _, _, _, _ => false

/-- The certificate check of one band profile. -/
def checkEntry (x : List Nat × List Nat) : Bool := stages x.1 x.2 0 [] 1 0 1

def checkAll (l : List (List Nat × List Nat)) : Bool := l.all checkEntry

end Erdos7
