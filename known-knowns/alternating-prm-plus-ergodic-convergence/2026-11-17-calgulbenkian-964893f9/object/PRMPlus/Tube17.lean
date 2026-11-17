import PRMPlus.Params

namespace PRMPlus

lemma slabs_17 : checkSlabRange tubeParams 64 4 = true := by decide +kernel

lemma tube_slabs_17 : ∀ k, 64 ≤ k → k < 68 → checkSlab tubeParams k = true :=
  checkSlabRange_sound tubeParams 4 64 slabs_17

end PRMPlus
