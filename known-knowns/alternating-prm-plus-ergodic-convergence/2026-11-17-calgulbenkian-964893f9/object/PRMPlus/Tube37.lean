import PRMPlus.Params

namespace PRMPlus

lemma slabs_37 : checkSlabRange tubeParams 144 4 = true := by decide +kernel

lemma tube_slabs_37 : ∀ k, 144 ≤ k → k < 148 → checkSlab tubeParams k = true :=
  checkSlabRange_sound tubeParams 4 144 slabs_37

end PRMPlus
