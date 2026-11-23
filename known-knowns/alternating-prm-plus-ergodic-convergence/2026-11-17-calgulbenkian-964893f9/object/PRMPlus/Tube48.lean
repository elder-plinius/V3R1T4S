import PRMPlus.Params

namespace PRMPlus

lemma slabs_48 : checkSlabRange tubeParams 188 4 = true := by decide +kernel

lemma tube_slabs_48 : ∀ k, 188 ≤ k → k < 192 → checkSlab tubeParams k = true :=
  checkSlabRange_sound tubeParams 4 188 slabs_48

end PRMPlus
