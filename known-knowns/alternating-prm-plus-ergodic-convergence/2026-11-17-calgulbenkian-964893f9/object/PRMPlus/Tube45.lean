import PRMPlus.Params

namespace PRMPlus

lemma slabs_45 : checkSlabRange tubeParams 176 4 = true := by decide +kernel

lemma tube_slabs_45 : ∀ k, 176 ≤ k → k < 180 → checkSlab tubeParams k = true :=
  checkSlabRange_sound tubeParams 4 176 slabs_45

end PRMPlus
