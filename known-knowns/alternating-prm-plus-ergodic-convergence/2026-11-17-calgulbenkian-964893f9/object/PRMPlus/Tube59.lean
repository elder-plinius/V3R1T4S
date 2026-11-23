import PRMPlus.Params

namespace PRMPlus

lemma slabs_59 : checkSlabRange tubeParams 232 4 = true := by decide +kernel

lemma tube_slabs_59 : ∀ k, 232 ≤ k → k < 236 → checkSlab tubeParams k = true :=
  checkSlabRange_sound tubeParams 4 232 slabs_59

end PRMPlus
