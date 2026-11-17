import PRMPlus.Params

namespace PRMPlus

lemma slabs_04 : checkSlabRange tubeParams 12 4 = true := by decide +kernel

lemma tube_slabs_04 : ∀ k, 12 ≤ k → k < 16 → checkSlab tubeParams k = true :=
  checkSlabRange_sound tubeParams 4 12 slabs_04

end PRMPlus
