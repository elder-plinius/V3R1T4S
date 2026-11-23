import PRMPlus.Params

namespace PRMPlus

lemma slabs_42 : checkSlabRange tubeParams 164 4 = true := by decide +kernel

lemma tube_slabs_42 : ∀ k, 164 ≤ k → k < 168 → checkSlab tubeParams k = true :=
  checkSlabRange_sound tubeParams 4 164 slabs_42

end PRMPlus
