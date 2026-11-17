import PRMPlus.Params

namespace PRMPlus

lemma slabs_41 : checkSlabRange tubeParams 160 4 = true := by decide +kernel

lemma tube_slabs_41 : ∀ k, 160 ≤ k → k < 164 → checkSlab tubeParams k = true :=
  checkSlabRange_sound tubeParams 4 160 slabs_41

end PRMPlus
