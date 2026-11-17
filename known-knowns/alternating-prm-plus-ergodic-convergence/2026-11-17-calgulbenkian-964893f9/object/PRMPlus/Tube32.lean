import PRMPlus.Params

namespace PRMPlus

lemma slabs_32 : checkSlabRange tubeParams 124 4 = true := by decide +kernel

lemma tube_slabs_32 : ∀ k, 124 ≤ k → k < 128 → checkSlab tubeParams k = true :=
  checkSlabRange_sound tubeParams 4 124 slabs_32

end PRMPlus
