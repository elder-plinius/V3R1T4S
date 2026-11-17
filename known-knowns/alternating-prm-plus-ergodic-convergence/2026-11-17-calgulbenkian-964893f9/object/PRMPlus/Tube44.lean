import PRMPlus.Params

namespace PRMPlus

lemma slabs_44 : checkSlabRange tubeParams 172 4 = true := by decide +kernel

lemma tube_slabs_44 : ∀ k, 172 ≤ k → k < 176 → checkSlab tubeParams k = true :=
  checkSlabRange_sound tubeParams 4 172 slabs_44

end PRMPlus
