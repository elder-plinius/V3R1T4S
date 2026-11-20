/-
Shared definitions used by the interfaces between the stages.
-/
import Mathlib
import Erdos7.Checker
import Erdos7.Cert.Table

namespace Erdos7

/-- The largest excluded value of the lcm. The theorem is `B0 < L`. -/
def B0 : ℕ := 168131152814624

/-- `valFrom i [e_0, e_1, ...] = oddP i ^ e_0 * oddP (i+1) ^ e_1 * ...`;
the profile value is `valFrom 0 es`. -/
def valFrom (i : ℕ) : List ℕ → ℕ
  | [] => 1
  | e :: es => oddP i ^ e * valFrom (i + 1) es

/-- `sigFrom i [e_0, e_1, ...] = prod_k (1 + p + ... + p^(e_k))` with `p = oddP (i+k)`:
this is `σ(valFrom i es)` (sum of divisors), written multiplicatively. -/
def sigFrom (i : ℕ) : List ℕ → ℕ
  | [] => 1
  | e :: es => geom (oddP i) (e + 1) * sigFrom (i + 1) es

/-- The `m`-th coordinate space of the profile `es`: residues modulo `oddP m ^ es[m]`
(a one-point type for `m ≥ es.length`). -/
abbrev Cell (es : List ℕ) (m : ℕ) : Type := Fin (oddP m ^ es.getD m 0)

end Erdos7
