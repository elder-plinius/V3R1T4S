import PRMPlus.Params

namespace PRMPlus

lemma slabs_64 : checkSlabRange tubeParams 252 4 = true := by decide +kernel

lemma tube_slabs_64 : ∀ k, 252 ≤ k → k < 256 → checkSlab tubeParams k = true :=
  checkSlabRange_sound tubeParams 4 252 slabs_64

end PRMPlus
