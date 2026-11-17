import PRMPlus.Params

namespace PRMPlus

lemma slabs_13 : checkSlabRange tubeParams 48 4 = true := by decide +kernel

lemma tube_slabs_13 : ∀ k, 48 ≤ k → k < 52 → checkSlab tubeParams k = true :=
  checkSlabRange_sound tubeParams 4 48 slabs_13

end PRMPlus
