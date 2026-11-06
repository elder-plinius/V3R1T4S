id: integer-chebyshev-constant-unit-interval

# Auswahl
Eigenständige rigorose Nachprüfung einer aktuellen mathematischen Schranke plus Suche nach besserem Faktorprodukt. Exakt prüfbar und als p1 ausdrücklich im Repo zugelassen. Keine bisherigen Legendre-Ergebnisse werden wiederverwendet.

# Success criterion (verbatim)
Either of the following. (A) An explicit integer polynomial P (or a list of integer factors Q_j with positive integer exponents e_j, P = prod Q_j^e_j) with ||P||_[0,1]^(1/deg P) STRICTLY BELOW 0.422684697505 (direction: min), proved by rigorous interval arithmetic: a bisection of [0,1] (or of w = x(1-x) in [0,1/4] for factors symmetric under x -> 1-x) in which every subinterval carries an outward-rounded upper bound on sum_j e_j log|Q_j| / deg P. (B) A certified lower bound STRICTLY ABOVE 0.422228600019 (direction: max): a measure and polynomial library satisfying the hypotheses of Theorem 7 of arXiv:2610.00386 (pairwise distinct, primitive, irreducible Q_j; budget B <= 1; inf A, the leading-coefficient term and every G_i bounded rigorously), or a certificate for Pritsker's (2005) method. In both cases the value is compared with the best bound on either side published at verification time (re-read the abstract page, its version history and the 2026 literature). For (B) the skeptic must also re-derive Theorem 7 from the paper, since it is new and unrefereed. Floating-point maxima without rigorous enclosures do not count.

# Partial wins (verbatim)
[
  {
    "id": "p1",
    "statement": "An independent rigorous re-verification of Niedbala Giraudin's shipped upper certificate (0.422684697505) or lower certificate (0.422228600019). It must use interval or exact arithmetic written from the paper's description, not the ancillary scripts. Report a confirmation or a located error. A located error counts as a win only if the skeptic reproduces it."
  }
]
