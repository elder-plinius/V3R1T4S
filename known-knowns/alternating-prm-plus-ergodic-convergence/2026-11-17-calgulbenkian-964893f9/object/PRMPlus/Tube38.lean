import PRMPlus.Params

namespace PRMPlus

lemma slabs_38 : checkSlabRange tubeParams 148 4 = true := by decide +kernel

lemma tube_slabs_38 : ∀ k, 148 ≤ k → k < 152 → checkSlab tubeParams k = true :=
  checkSlabRange_sound tubeParams 4 148 slabs_38

end PRMPlus
