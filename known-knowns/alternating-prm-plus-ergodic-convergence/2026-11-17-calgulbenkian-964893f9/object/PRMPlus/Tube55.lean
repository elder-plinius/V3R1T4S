import PRMPlus.Params

namespace PRMPlus

lemma slabs_55 : checkSlabRange tubeParams 216 4 = true := by decide +kernel

lemma tube_slabs_55 : ∀ k, 216 ≤ k → k < 220 → checkSlab tubeParams k = true :=
  checkSlabRange_sound tubeParams 4 216 slabs_55

end PRMPlus
