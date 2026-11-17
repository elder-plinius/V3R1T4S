import PRMPlus.Params

namespace PRMPlus

lemma slabs_46 : checkSlabRange tubeParams 180 4 = true := by decide +kernel

lemma tube_slabs_46 : ∀ k, 180 ≤ k → k < 184 → checkSlab tubeParams k = true :=
  checkSlabRange_sound tubeParams 4 180 slabs_46

end PRMPlus
