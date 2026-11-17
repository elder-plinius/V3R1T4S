import PRMPlus.Params

namespace PRMPlus

lemma slabs_56 : checkSlabRange tubeParams 220 4 = true := by decide +kernel

lemma tube_slabs_56 : ∀ k, 220 ≤ k → k < 224 → checkSlab tubeParams k = true :=
  checkSlabRange_sound tubeParams 4 220 slabs_56

end PRMPlus
