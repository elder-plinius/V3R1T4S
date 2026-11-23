import PRMPlus.Params

namespace PRMPlus

lemma slabs_34 : checkSlabRange tubeParams 132 4 = true := by decide +kernel

lemma tube_slabs_34 : ∀ k, 132 ≤ k → k < 136 → checkSlab tubeParams k = true :=
  checkSlabRange_sound tubeParams 4 132 slabs_34

end PRMPlus
