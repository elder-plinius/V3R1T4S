import PRMPlus.Params

namespace PRMPlus

lemma slabs_26 : checkSlabRange tubeParams 100 4 = true := by decide +kernel

lemma tube_slabs_26 : ∀ k, 100 ≤ k → k < 104 → checkSlab tubeParams k = true :=
  checkSlabRange_sound tubeParams 4 100 slabs_26

end PRMPlus
