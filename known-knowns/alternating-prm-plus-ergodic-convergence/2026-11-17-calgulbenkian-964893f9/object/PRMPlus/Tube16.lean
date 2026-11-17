import PRMPlus.Params

namespace PRMPlus

lemma slabs_16 : checkSlabRange tubeParams 60 4 = true := by decide +kernel

lemma tube_slabs_16 : ∀ k, 60 ≤ k → k < 64 → checkSlab tubeParams k = true :=
  checkSlabRange_sound tubeParams 4 60 slabs_16

end PRMPlus
