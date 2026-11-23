import PRMPlus.Params

namespace PRMPlus

lemma slabs_51 : checkSlabRange tubeParams 200 4 = true := by decide +kernel

lemma tube_slabs_51 : ∀ k, 200 ≤ k → k < 204 → checkSlab tubeParams k = true :=
  checkSlabRange_sound tubeParams 4 200 slabs_51

end PRMPlus
