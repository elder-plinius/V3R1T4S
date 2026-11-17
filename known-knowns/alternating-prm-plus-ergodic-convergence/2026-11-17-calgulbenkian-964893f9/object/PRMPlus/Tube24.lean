import PRMPlus.Params

namespace PRMPlus

lemma slabs_24 : checkSlabRange tubeParams 92 4 = true := by decide +kernel

lemma tube_slabs_24 : ∀ k, 92 ≤ k → k < 96 → checkSlab tubeParams k = true :=
  checkSlabRange_sound tubeParams 4 92 slabs_24

end PRMPlus
