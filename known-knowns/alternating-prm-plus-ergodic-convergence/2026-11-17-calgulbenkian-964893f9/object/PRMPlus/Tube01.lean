import PRMPlus.Params

namespace PRMPlus

lemma slabs_01 : checkSlabRange tubeParams 0 4 = true := by decide +kernel

lemma tube_slabs_01 : ∀ k, 0 ≤ k → k < 4 → checkSlab tubeParams k = true :=
  checkSlabRange_sound tubeParams 4 0 slabs_01

end PRMPlus
