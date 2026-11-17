import PRMPlus.Params

namespace PRMPlus

lemma slabs_33 : checkSlabRange tubeParams 128 4 = true := by decide +kernel

lemma tube_slabs_33 : ∀ k, 128 ≤ k → k < 132 → checkSlab tubeParams k = true :=
  checkSlabRange_sound tubeParams 4 128 slabs_33

end PRMPlus
