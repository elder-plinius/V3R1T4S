import Mathlib.Data.Fin.VecNotation
import Mathlib.InformationTheory.Hamming

/-!
An explicit sixteen-word DNA code of length 20 with GC content 10, Hamming
distance at least 15, and distance at least 15 from every reverse complement
(self-pairs included). Alphabet order is A,T,C,G; complement is A↔T, C↔G.
All checks are by `decide` (kernel evaluation, no `native_decide`).
-/
namespace DnaCode20_15

abbrev Base := Fin 4

def comp (b : Base) : Base := ![1,0,3,2] b

/-- Reverse complement: position `i` reads the complement of position `19 - i`. -/
def rcStd (w : Fin 20 → Base) : Fin 20 → Base := fun i => comp (w i.rev)

/-- GC content: number of positions holding C or G (letters 2 and 3). -/
def gc (w : Fin 20 → Base) : ℕ := (Finset.univ.filter fun i => 2 ≤ (w i).val).card

/-- GAACCTTGACTGATCCTGTC, CTTGAGGTACTGCGAAACAG, TCCATCCAACTGGCTTGTGA,
AGGTGAACACTGTAGGCACT, GAACGAACTGAGGCTTACAG, CTTGTCCATGAGTAGGTGTC,
TCCAAGGTTGAGATCCCACT, AGGTCTTGTGAGCGAAGTGA, GTCTACTCAACCACAGAGGT,
CAGACAGAAACCCACTTCCA, TGAGGTCTAACCGTGACTTG, ACTCTGAGAACCTGTCGAAC,
GTCTTGAGTTGCGTGATCCA, CAGAGTCTTTGCTGTCAGGT, TGAGCAGATTGCACAGGAAC,
ACTCACTCTTGCCACTCTTG. -/
def code : Fin 16 → Fin 20 → Base := ![
  ![3,0,0,2,2,1,1,3,0,2,1,3,0,1,2,2,1,3,1,2],
  ![2,1,1,3,0,3,3,1,0,2,1,3,2,3,0,0,0,2,0,3],
  ![1,2,2,0,1,2,2,0,0,2,1,3,3,2,1,1,3,1,3,0],
  ![0,3,3,1,3,0,0,2,0,2,1,3,1,0,3,3,2,0,2,1],
  ![3,0,0,2,3,0,0,2,1,3,0,3,3,2,1,1,0,2,0,3],
  ![2,1,1,3,1,2,2,0,1,3,0,3,1,0,3,3,1,3,1,2],
  ![1,2,2,0,0,3,3,1,1,3,0,3,0,1,2,2,2,0,2,1],
  ![0,3,3,1,2,1,1,3,1,3,0,3,2,3,0,0,3,1,3,0],
  ![3,1,2,1,0,2,1,2,0,0,2,2,0,2,0,3,0,3,3,1],
  ![2,0,3,0,2,0,3,0,0,0,2,2,2,0,2,1,1,2,2,0],
  ![1,3,0,3,3,1,2,1,0,0,2,2,3,1,3,0,2,1,1,3],
  ![0,2,1,2,1,3,0,3,0,0,2,2,1,3,1,2,3,0,0,2],
  ![3,1,2,1,1,3,0,3,1,1,3,2,3,1,3,0,1,2,2,0],
  ![2,0,3,0,3,1,2,1,1,1,3,2,1,3,1,2,0,3,3,1],
  ![1,3,0,3,2,0,3,0,1,1,3,2,0,2,0,3,3,0,0,2],
  ![0,2,1,2,0,2,1,2,1,1,3,2,2,0,2,1,2,1,1,3]]

theorem code_injective : Function.Injective code := by decide

theorem code_gc : ∀ i, gc (code i) = 10 := by decide

theorem code_dist : ∀ i j, i ≠ j → 15 ≤ hammingDist (code i) (code j) := by decide

theorem code_rc : ∀ i j, 15 ≤ hammingDist (code i) (rcStd (code j)) := by decide

/-- `A_4^{GC,RC}(20,15,10) ≥ 16`. -/
theorem lower_bound :
    ∃ C : Finset (Fin 20 → Base), C.card = 16 ∧ (∀ x ∈ C, gc x = 10) ∧
      (∀ x ∈ C, ∀ y ∈ C, x ≠ y → 15 ≤ hammingDist x y) ∧
      (∀ x ∈ C, ∀ y ∈ C, 15 ≤ hammingDist x (rcStd y)) := by
  refine ⟨Finset.univ.map ⟨code, code_injective⟩, by simp, ?_, ?_, ?_⟩
  · simp only [Finset.mem_map, Finset.mem_univ, true_and, Function.Embedding.coeFn_mk]
    rintro _ ⟨i, rfl⟩
    exact code_gc i
  · simp only [Finset.mem_map, Finset.mem_univ, true_and, Function.Embedding.coeFn_mk]
    rintro _ ⟨i, rfl⟩ _ ⟨j, rfl⟩ hne
    exact code_dist i j fun h => hne (h ▸ rfl)
  · simp only [Finset.mem_map, Finset.mem_univ, true_and, Function.Embedding.coeFn_mk]
    rintro _ ⟨i, rfl⟩ _ ⟨j, rfl⟩
    exact code_rc i j

end DnaCode20_15
