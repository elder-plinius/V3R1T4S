import PRMPlus.Params

namespace PRMPlus

lemma slabs_36 : checkSlabRange tubeParams 140 4 = true := by decide +kernel

lemma tube_slabs_36 : ∀ k, 140 ≤ k → k < 144 → checkSlab tubeParams k = true :=
  checkSlabRange_sound tubeParams 4 140 slabs_36

end PRMPlus
