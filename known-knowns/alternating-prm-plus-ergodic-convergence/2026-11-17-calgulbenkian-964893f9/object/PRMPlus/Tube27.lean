import PRMPlus.Params

namespace PRMPlus

lemma slabs_27 : checkSlabRange tubeParams 104 4 = true := by decide +kernel

lemma tube_slabs_27 : ∀ k, 104 ≤ k → k < 108 → checkSlab tubeParams k = true :=
  checkSlabRange_sound tubeParams 4 104 slabs_27

end PRMPlus
