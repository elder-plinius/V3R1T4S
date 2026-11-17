import Mathlib

/-! Frozen NEGATION (a counterexample claim) for target erdos-677-lcm-blocks (Justin Sun Prize JSP-000550).
`Finset.lcmInterval` copied verbatim from google-deepmind/formal-conjectures,
FormalConjecturesForMathlib/Algebra/GCDMonoid/Finset.lean; the body of `Erdos677.erdos_677` copied verbatim from
FormalConjectures/ErdosProblems/677.lean (both fetched 2026-10-15T07:25Z from main; repository head 2c24ebe7). -/

namespace Finset

/-- The least common multiple of ${n+1, \dotsc, n+k}$. -/
def lcmInterval {α : Type*} [CommSemiring α] [NormalizedGCDMonoid α]
    [Preorder α] [LocallyFiniteOrder α] (n k : α) : α := (Finset.Ioc n (n + k)).lcm id

end Finset

open Finset

namespace V3R1T4S

def spec : Prop :=
  ¬ ∀ (m n k : ℕ), k > 0 → m ≥ n + k → lcmInterval m k ≠ lcmInterval n k

end V3R1T4S
