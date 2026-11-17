import PRMPlus.Params

namespace PRMPlus

lemma slabs_54 : checkSlabRange tubeParams 212 4 = true := by decide +kernel

lemma tube_slabs_54 : ∀ k, 212 ≤ k → k < 216 → checkSlab tubeParams k = true :=
  checkSlabRange_sound tubeParams 4 212 slabs_54

end PRMPlus
