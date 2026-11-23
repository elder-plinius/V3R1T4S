import PRMPlus.Params

namespace PRMPlus

lemma slabs_60 : checkSlabRange tubeParams 236 4 = true := by decide +kernel

lemma tube_slabs_60 : ∀ k, 236 ≤ k → k < 240 → checkSlab tubeParams k = true :=
  checkSlabRange_sound tubeParams 4 236 slabs_60

end PRMPlus
