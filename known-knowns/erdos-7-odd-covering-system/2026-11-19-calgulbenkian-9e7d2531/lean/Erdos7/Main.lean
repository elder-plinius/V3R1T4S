/-
Final assembly: from an odd covering system of `ℤ` with `lcm ≤ B0` to a covering family of boxes
on the cells of a band profile, contradicting `box_no_cover` (Stage 4 core) via
`box_cover_abundant` (counting), `band_complete` (Stage 3) and `Cert.table_ok` (Stage 2).
-/
import Erdos7.Statement
import Erdos7.Defs
import Erdos7.Box
import Erdos7.Enum
import Erdos7.Replacement
import Erdos7.Abundance

namespace Erdos7

/-- Lemma 2 (existence of the `3^k` scaling), for an arbitrary bound. -/
theorem exists_scale (B V : ℕ) (hV : 0 < V) : ∃ k, B < 3 ^ (k + 1) * V := by
  refine ⟨B, ?_⟩
  have h1 : B + 1 < 3 ^ (B + 1) := Nat.lt_pow_self (by norm_num)
  have h2 : 3 ^ (B + 1) ≤ 3 ^ (B + 1) * V := Nat.le_mul_of_pos_right _ hV
  omega

/-- The combinatorial core of the assembly, with the prime factorisation data of the lcm
abstracted: `q 0 < ... < q (r-1)` are the odd primes dividing the moduli, `e m` bounds the
exponent of `q m` in every modulus. -/
theorem covering_core (S : Finset (ℤ × ℕ)) (hS : IsOddCovering S) (r : ℕ) (hr : 1 ≤ r)
    (q e : ℕ → ℕ)
    (hq : ∀ m, m < r → (q m).Prime)
    (hqinj : ∀ m, m < r → ∀ m', m' < r → q m = q m' → m = m')
    (hle : ∀ m, m < r → oddP m ≤ q m)
    (h3 : ∀ m, m < r → 3 ≤ oddP m)
    (he1 : ∀ m, m < r → 1 ≤ e m)
    (hV0 : ∏ m ∈ Finset.range r, oddP m ^ e m ≤ B0)
    (hfac : ∀ c ∈ S, ∀ m, m < r → c.2.factorization (q m) ≤ e m)
    (hsupp : ∀ c ∈ S, ∀ p : ℕ, p.Prime → p ∣ c.2 → ∃ m, m < r ∧ p = q m) : False := by
  classical
  set V0 := ∏ m ∈ Finset.range r, oddP m ^ e m with hV0def
  have hV0pos : 0 < V0 := by
    apply Finset.prod_pos
    intro m hm
    rw [Finset.mem_range] at hm
    exact pow_pos (by have := h3 m hm; omega) _
  -- Lemma 2: scale by `3^k` into the band
  have hex : ∃ k, B0 < 3 ^ (k + 1) * V0 := exists_scale B0 V0 hV0pos
  let k := Nat.find hex
  have hk1 : B0 < 3 ^ (k + 1) * V0 := Nat.find_spec hex
  have hk2 : 3 ^ k * V0 ≤ B0 := by
    by_cases hk : k = 0
    · rw [hk]; simpa using hV0
    · have := Nat.find_min hex (m := k - 1) (by omega)
      rw [Nat.sub_add_cancel (by omega)] at this
      omega
  -- the band profile
  let eL : ℕ → ℕ := fun m => if m < r then e m + (if m = 0 then k else 0) else 0
  let es : List ℕ := (List.range r).map eL
  have hlen : es.length = r := by simp [es]
  have hget : ∀ m, es.getD m 0 = eL m := by
    intro m
    by_cases hm : m < r
    · simp [es, List.getD_eq_getElem?_getD, List.getElem?_map, List.getElem?_range hm]
    · have h1 : es.getD m 0 = 0 := by
        rw [List.getD_eq_getElem?_getD, List.getElem?_eq_none (by omega)]; rfl
      rw [h1]; simp [eL, hm]
  have hval : valFrom 0 es = 3 ^ k * V0 := by
    rw [valFrom_eq_prod, hlen]
    simp only [Nat.zero_add]
    have h1 : ∀ m ∈ Finset.range r, oddP m ^ es.getD m 0 =
        oddP m ^ e m * oddP m ^ (if m = 0 then k else 0) := by
      intro m hm
      rw [Finset.mem_range] at hm
      rw [hget, ← pow_add]
      simp [eL, hm]
    rw [Finset.prod_congr rfl h1, Finset.prod_mul_distrib, mul_comm]
    congr 1
    rw [Finset.prod_eq_single 0]
    · simp [oddP]
    · intro m _ hm0; simp [hm0]
    · intro h; exact absurd (Finset.mem_range.2 (by omega)) h
  have hlo : B0 < 3 * valFrom 0 es := by
    rw [hval, ← mul_assoc, ← pow_succ']; exact hk1
  have hhi : valFrom 0 es ≤ B0 := by rw [hval]; exact hk2
  -- the box family
  let lev : ℤ × ℕ → ℕ → ℕ := fun c m => if m < r then c.2.factorization (q m) else 0
  let side : ℤ × ℕ → (m : ℕ) → Finset (Cell es m) := fun c m =>
    Finset.univ.filter (fun u : Fin (oddP m ^ es.getD m 0) =>
      ((q m : ℤ) ^ (lev c m)) ∣ (dig (oddP m) (q m) (es.getD m 0) u.val : ℤ) - c.1)
  have hlev0 : ∀ j ∈ S, ∀ m, es.length ≤ m → lev j m = 0 := by
    intro j _ m hm
    rw [hlen] at hm
    simp [lev, Nat.not_lt.2 hm]
  have heLge : ∀ m, m < r → e m ≤ es.getD m 0 := by
    intro m hm
    rw [hget]; simp [eL, hm]
  have hlevle : ∀ j ∈ S, ∀ m, lev j m ≤ es.getD m 0 := by
    intro j hj m
    by_cases hm : m < r
    · have : lev j m = j.2.factorization (q m) := by simp [lev, hm]
      rw [this]
      exact le_trans (hfac j hj m hm) (heLge m hm)
    · simp [lev, hm]
  have hc0 : ∀ c ∈ S, c.2 ≠ 0 := fun c hc => by have := hS.one_lt c hc; omega
  have hnz : ∀ j ∈ S, ∃ m, lev j m ≠ 0 := by
    intro j hj
    obtain ⟨p, hp, hpd⟩ := Nat.exists_prime_and_dvd (by have := hS.one_lt j hj; omega : j.2 ≠ 1)
    obtain ⟨m, hm, rfl⟩ := hsupp j hj p hp hpd
    refine ⟨m, ?_⟩
    have : lev j m = j.2.factorization (q m) := by simp [lev, hm]
    rw [this]
    exact (hp.factorization_pos_of_dvd (hc0 j hj) hpd).ne'
  have hinj : ∀ j ∈ S, ∀ j' ∈ S, lev j = lev j' → j = j' := by
    intro j hj j' hj' h
    apply hS.distinct j hj j' hj'
    apply Nat.eq_of_factorization_eq (hc0 j hj) (hc0 j' hj')
    intro p
    have key : ∀ m, m < r → j.2.factorization (q m) = j'.2.factorization (q m) := by
      intro m hm
      have := congrFun h m
      simpa [lev, hm] using this
    by_cases hp : p.Prime
    · by_cases hd : p ∣ j.2
      · obtain ⟨m, hm, rfl⟩ := hsupp j hj p hp hd
        exact key m hm
      · by_cases hd' : p ∣ j'.2
        · obtain ⟨m, hm, rfl⟩ := hsupp j' hj' p hp hd'
          exact key m hm
        · rw [Nat.factorization_eq_zero_of_not_dvd hd, Nat.factorization_eq_zero_of_not_dvd hd']
    · rw [Nat.factorization_eq_zero_of_not_prime _ hp, Nat.factorization_eq_zero_of_not_prime _ hp]
  have hsize : ∀ j ∈ S, ∀ m, m < es.length →
      (side j m).card * oddP m ^ lev j m ≤ oddP m ^ es.getD m 0 := by
    intro j hj m hm
    rw [hlen] at hm
    exact dig_class_card (oddP m) (q m) (by have := h3 m hm; omega) (hle m hm) (es.getD m 0)
      (lev j m) (hlevle j hj m) j.1
  have hpos : ∀ m, m < es.length → 0 < oddP m := by
    intro m hm
    rw [hlen] at hm
    have := h3 m hm; omega
  -- the boxes cover (Chinese remainder theorem + the covering property of `S`)
  have hcover : ∀ x : (m : ℕ) → Cell es m,
      ∃ j ∈ S, ∀ m, m < es.length → lev j m ≠ 0 → x m ∈ side j m := by
    intro x
    let a : ℕ → ℕ := fun m => dig (oddP m) (q m) (es.getD m 0) (x m).val
    let s : ℕ → ℕ := fun m => q m ^ e m
    have hs : ∀ i ∈ Finset.range r, s i ≠ 0 := by
      intro i hi
      rw [Finset.mem_range] at hi
      exact pow_ne_zero _ (hq i hi).ne_zero
    have pp : Set.Pairwise (Finset.range r : Set ℕ) (Function.onFun Nat.Coprime s) := by
      intro i hi i' hi' hne
      rw [Finset.mem_coe, Finset.mem_range] at hi hi'
      apply Nat.Coprime.pow
      rw [Nat.coprime_primes (hq i hi) (hq i' hi')]
      intro h
      exact hne (hqinj i hi i' hi' h)
    obtain ⟨z, hz⟩ := Nat.chineseRemainderOfFinset a s (Finset.range r) hs pp
    obtain ⟨c, hc, hcd⟩ := hS.covers (z : ℤ)
    refine ⟨c, hc, ?_⟩
    intro m hm _
    rw [hlen] at hm
    have hlevm : lev c m = c.2.factorization (q m) := by simp [lev, hm]
    show x m ∈ Finset.univ.filter _
    rw [Finset.mem_filter]
    refine ⟨Finset.mem_univ _, ?_⟩
    rw [hlevm]
    have h1 : ((q m : ℤ) ^ c.2.factorization (q m)) ∣ (z : ℤ) - c.1 := by
      have : ((q m ^ c.2.factorization (q m) : ℕ) : ℤ) ∣ (c.2 : ℤ) :=
        Int.natCast_dvd_natCast.2 (Nat.ordProj_dvd c.2 (q m))
      rw [Nat.cast_pow] at this
      exact this.trans hcd
    have h2 : ((q m : ℤ) ^ c.2.factorization (q m)) ∣ (a m : ℤ) - (z : ℤ) := by
      have hz' := (Nat.modEq_iff_dvd.1 (hz m (Finset.mem_range.2 hm)))
      have : ((q m : ℤ) ^ c.2.factorization (q m)) ∣ ((s m : ℕ) : ℤ) := by
        show _ ∣ ((q m ^ e m : ℕ) : ℤ)
        rw [Nat.cast_pow]
        exact pow_dvd_pow _ (hfac c hc m hm)
      exact this.trans hz'
    have h3' := dvd_add h2 h1
    have heq : (a m : ℤ) - (z : ℤ) + ((z : ℤ) - c.1) = (a m : ℤ) - c.1 := by ring
    rw [heq] at h3'
    exact h3'
  -- abundance, table membership, certificate, contradiction
  have hab : 2 * valFrom 0 es ≤ sigFrom 0 es :=
    box_cover_abundant es S lev side hlev0 hlevle hnz hinj hsize hpos hcover
  have hespos : ∀ t ∈ es, 1 ≤ t := by
    intro t ht
    simp only [es, List.mem_map, List.mem_range] at ht
    obtain ⟨m, hm, rfl⟩ := ht
    have := he1 m hm
    simp only [eL, hm, ite_true]
    omega
  have hne : es ≠ [] := by
    intro h
    have := hlen
    rw [h] at this
    simp at this
    omega
  have hmem := band_complete es hespos hne hlo hhi hab
  rw [List.mem_map] at hmem
  obtain ⟨⟨es', caps⟩, hx, hx1⟩ := hmem
  simp only at hx1
  subst hx1
  have hchk : checkEntry (es, caps) = true := Cert.table_ok _ hx
  obtain ⟨y, hy⟩ := box_no_cover es caps hchk S lev side hlev0 hlevle hnz hinj hsize
  obtain ⟨c, hc, hcy⟩ := hcover y
  obtain ⟨m, hm, hne0, hnot⟩ := hy c hc
  exact hnot (hcy m hm hne0)

theorem prod_oddP_14 : B0 < ∏ m ∈ Finset.range 14, oddP m := by
  simp [Finset.prod_range_succ, oddP, B0]

/-- **Main theorem.** Every covering of `ℤ` by finitely many congruences with pairwise distinct odd
moduli `> 1` has lcm of the moduli at least `168,131,152,814,625`. -/
theorem odd_covering_lcm_lower_bound : MainStatement := by
  classical
  intro S hS
  by_contra hcon
  have hLB : lcmModuli S ≤ B0 := by unfold B0; omega
  set L := lcmModuli S with hLdef
  have hc0 : ∀ c ∈ S, c.2 ≠ 0 := fun c hc => by have := hS.one_lt c hc; omega
  have hL0 : L ≠ 0 := by
    intro h
    rw [hLdef, lcmModuli, Finset.lcm_eq_zero_iff] at h
    obtain ⟨c, hc, h0⟩ := h
    exact hc0 c hc h0
  have hdvd : ∀ c ∈ S, c.2 ∣ L := fun c hc => Finset.dvd_lcm hc
  have hLodd : Odd L := by
    have h1 : L ∣ ∏ c ∈ S, c.2 := Finset.lcm_dvd (fun c hc => Finset.dvd_prod_of_mem _ hc)
    have h2 : Odd (∏ c ∈ S, c.2) :=
      Finset.prod_induction _ Odd (fun a b ha hb => ha.mul hb) odd_one (fun c hc => hS.odd c hc)
    exact Odd.of_dvd_nat h2 h1
  obtain ⟨c0, hc0S, -⟩ := hS.covers 0
  set P := L.primeFactors with hP
  set r := P.card with hrdef
  let emb := P.orderEmbOfFin (rfl : P.card = r)
  let q : ℕ → ℕ := fun m => if h : m < r then emb ⟨m, h⟩ else 0
  have hqemb : ∀ i : Fin r, q i = emb i := by
    intro i
    simp [q, i.isLt]
  have hqmem : ∀ m, m < r → q m ∈ P := by
    intro m hm
    have := hqemb ⟨m, hm⟩
    simp only at this
    rw [this]
    exact Finset.orderEmbOfFin_mem P rfl _
  have hq : ∀ m, m < r → (q m).Prime := fun m hm => Nat.prime_of_mem_primeFactors (hqmem m hm)
  have hqdvd : ∀ m, m < r → q m ∣ L := fun m hm => Nat.dvd_of_mem_primeFactors (hqmem m hm)
  have hqodd : ∀ m, m < r → Odd (q m) := fun m hm => Odd.of_dvd_nat hLodd (hqdvd m hm)
  have hqmono : ∀ m, m + 1 < r → q m < q (m + 1) := by
    intro m hm
    have h1 := hqemb ⟨m, by omega⟩
    have h2 := hqemb ⟨m + 1, hm⟩
    simp only at h1 h2
    rw [h1, h2]
    exact emb.strictMono (by simp [Fin.lt_def])
  have hqinj : ∀ m, m < r → ∀ m', m' < r → q m = q m' → m = m' := by
    intro m hm m' hm' h
    have h1 := hqemb ⟨m, hm⟩
    have h2 := hqemb ⟨m', hm'⟩
    simp only at h1 h2
    rw [h1, h2] at h
    have := emb.injective h
    exact Fin.mk.inj this
  have hle : ∀ m, m < r → oddP m ≤ q m := oddP_le_of_strictMono q r hq hqodd hqmono
  let e : ℕ → ℕ := fun m => L.factorization (q m)
  have he1 : ∀ m, m < r → 1 ≤ e m := fun m hm =>
    (hq m hm).factorization_pos_of_dvd hL0 (hqdvd m hm)
  -- the product formula for L
  have hLprod : L = ∏ m ∈ Finset.range r, q m ^ e m := by
    have h1 : L.factorization.prod (· ^ ·) = L := Nat.prod_factorization_pow_eq_self hL0
    rw [Finsupp.prod, Nat.support_factorization] at h1
    rw [← Fin.prod_univ_eq_prod_range (fun m => q m ^ e m) r]
    conv_lhs => rw [← h1]
    rw [← Finset.image_orderEmbOfFin_univ L.primeFactors (rfl : P.card = r),
      Finset.prod_image (fun i _ j _ h => (P.orderEmbOfFin rfl).injective h)]
    apply Finset.prod_congr rfl
    intro i _
    show emb i ^ L.factorization (emb i) = q i ^ L.factorization (q i)
    rw [hqemb i]
  -- at most 13 primes
  have hr13 : r < 14 := by
    by_contra h
    have h14 : 14 ≤ r := by omega
    have h1 : ∏ m ∈ Finset.range 14, oddP m ≤ ∏ m ∈ Finset.range 14, q m :=
      Finset.prod_le_prod (fun m hm => hle m (by rw [Finset.mem_range] at hm; omega))
    have h2 : ∏ m ∈ Finset.range 14, q m ≤ ∏ m ∈ Finset.range r, q m := by
      apply Finset.prod_le_prod_of_subset_of_one_le
      · intro m hm; rw [Finset.mem_range] at hm ⊢; omega
      · intro m hm _
        rw [Finset.mem_range] at hm
        exact (hq m hm).one_le
    have h3 : ∏ m ∈ Finset.range r, q m ≤ ∏ m ∈ Finset.range r, q m ^ e m := by
      apply Finset.prod_le_prod
      intro m hm
      rw [Finset.mem_range] at hm
      exact Nat.le_self_pow (by have := he1 m hm; omega) _
    have := prod_oddP_14
    rw [← hLprod] at h3
    omega
  have h3 : ∀ m, m < r → 3 ≤ oddP m := fun m hm => three_le_oddP (by omega)
  have hr1 : 1 ≤ r := by
    obtain ⟨p, hp, hpd⟩ := Nat.exists_prime_and_dvd (by have := hS.one_lt c0 hc0S; omega : c0.2 ≠ 1)
    have : p ∈ P := Nat.mem_primeFactors.2 ⟨hp, hpd.trans (hdvd c0 hc0S), hL0⟩
    exact Finset.card_pos.2 ⟨p, this⟩
  have hV0 : ∏ m ∈ Finset.range r, oddP m ^ e m ≤ B0 := by
    refine le_trans ?_ hLB
    rw [hLprod]
    apply Finset.prod_le_prod
    intro m hm
    rw [Finset.mem_range] at hm
    exact Nat.pow_le_pow_left (hle m hm) _
  have hfac : ∀ c ∈ S, ∀ m, m < r → c.2.factorization (q m) ≤ e m := by
    intro c hc m _
    exact (Nat.factorization_le_iff_dvd (hc0 c hc) hL0).2 (hdvd c hc) (q m)
  have hsupp : ∀ c ∈ S, ∀ p : ℕ, p.Prime → p ∣ c.2 → ∃ m, m < r ∧ p = q m := by
    intro c hc p hp hpd
    have hpP : p ∈ P := Nat.mem_primeFactors.2 ⟨hp, hpd.trans (hdvd c hc), hL0⟩
    rw [← Finset.image_orderEmbOfFin_univ P (rfl : P.card = r), Finset.mem_image] at hpP
    obtain ⟨i, _, hi⟩ := hpP
    exact ⟨i, i.isLt, by rw [hqemb i]; exact hi.symm⟩
  exact covering_core S hS r hr1 q e hq hqinj hle h3 he1 hV0 hfac hsupp

end Erdos7

#print axioms Erdos7.odd_covering_lcm_lower_bound
