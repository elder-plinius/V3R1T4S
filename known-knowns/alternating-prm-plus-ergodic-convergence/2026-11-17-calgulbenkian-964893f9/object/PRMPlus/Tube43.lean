import PRMPlus.Params

namespace PRMPlus

lemma slabs_43 : checkSlabRange tubeParams 168 4 = true := by decide +kernel

lemma tube_slabs_43 : ∀ k, 168 ≤ k → k < 172 → checkSlab tubeParams k = true :=
  checkSlabRange_sound tubeParams 4 168 slabs_43

end PRMPlus
