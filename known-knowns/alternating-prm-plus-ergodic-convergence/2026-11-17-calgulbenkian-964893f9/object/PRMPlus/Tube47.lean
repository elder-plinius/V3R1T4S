import PRMPlus.Params

namespace PRMPlus

lemma slabs_47 : checkSlabRange tubeParams 184 4 = true := by decide +kernel

lemma tube_slabs_47 : ∀ k, 184 ≤ k → k < 188 → checkSlab tubeParams k = true :=
  checkSlabRange_sound tubeParams 4 184 slabs_47

end PRMPlus
