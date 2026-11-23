import PRMPlus.Params

namespace PRMPlus

lemma slabs_05 : checkSlabRange tubeParams 16 4 = true := by decide +kernel

lemma tube_slabs_05 : ∀ k, 16 ≤ k → k < 20 → checkSlab tubeParams k = true :=
  checkSlabRange_sound tubeParams 4 16 slabs_05

end PRMPlus
