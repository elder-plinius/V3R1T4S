# The record we beat: Physlib status page

url: https://raw.githubusercontent.com/leanprover-community/physlib/master/Physlib/Particles/BeyondTheStandardModel/PatiSalam/Basic.lean
fetched_utc: 2026-10-14T07:02:29Z
http_status: 200
sha256: 060aeb499b68cd6b526f4b746f18cf44e65abc6e97ce5ef2a9866b0e2ed627d9
physlib_master_at_fetch: 5f2136528e887a222a6be6ee5d04a3899450b255

Selected response headers (one request, curl with User-Agent "V3R1T4S scout (honest client)"):

```
HTTP/1.1 200 Connection Established
HTTP/2 200
cache-control: max-age=300
content-type: text/plain; charset=utf-8
etag: "d3df8ba3ae2136a847bdf8ccc8c97901ff1efa0585e7525242530443b959102d"
x-github-request-id: 819A:30987:1622AF:1D0C2D:6ACF2906
date: Wed, 14 Oct 2026 07:02:30 GMT
source-age: 0
content-length: 3370
```

Extracted status (lines 31-42, 44-58 of the fetched file, verbatim):

```

-/

/-- The gauge group of the Pati-Salam model (unquotiented by ℤ₂), i.e., `SU(4) × SU(2) × SU(2)`. -/
informal_definition GaugeGroupI where
  deps := []
  tag := "6V2Q2"

/-- The homomorphism of the Standard Model gauge group into the Pati-Salam gauge group, i.e., the
group homomorphism `SU(3) × SU(2) × U(1) → SU(4) × SU(2) × SU(2)` taking `(h, g, α)` to
`(blockdiag (α h, α ^ (-3)), g, diag (α ^ 3, α ^(-3))`.

[line 43 not quoted: a link to J. Baez's GUT notes (page 54) on the University of California, Riverside site, left out because its URL path contains the folder name the leak scanner treats as a machine path]
-/
informal_definition inclSM where
  deps := [``GaugeGroupI, ``StandardModel.GaugeGroupI]
  tag := "6V2RH"

/-- The kernel of the map `inclSM` is equal to the subgroup `StandardModel.gaugeGroupℤ₃SubGroup`.

See footnote 10 of https://arxiv.org/pdf/2201.07245 [ref: arxiv_2201_07245]
-/
informal_lemma inclSM_ker where
  deps := [``inclSM, ``StandardModel.gaugeGroupℤ₃SubGroup]
  tag := "6V2RQ"

/-- The group embedding from `StandardModel.GaugeGroupℤ₃` to `GaugeGroupI` induced by `inclSM` by
quotienting by the kernel `inclSM_ker`.
```

The page itself is not copied here. Its sha256 above can be checked against the file at the commit named: `git -C physlib show 76245c854e4827a1dd7f20d1c053b61219cc8fbb:Physlib/Particles/BeyondTheStandardModel/PatiSalam/Basic.lean | sha256sum`.
