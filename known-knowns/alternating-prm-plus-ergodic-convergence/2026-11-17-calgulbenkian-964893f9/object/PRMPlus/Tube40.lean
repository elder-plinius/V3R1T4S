import PRMPlus.Params

namespace PRMPlus

lemma slabs_40 : checkSlabRange tubeParams 156 4 = true := by decide +kernel

lemma tube_slabs_40 : ∀ k, 156 ≤ k → k < 160 → checkSlab tubeParams k = true :=
  checkSlabRange_sound tubeParams 4 156 slabs_40

end PRMPlus
