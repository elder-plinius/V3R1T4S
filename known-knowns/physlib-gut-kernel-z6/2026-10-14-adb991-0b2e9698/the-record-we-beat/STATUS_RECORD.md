# The record we beat: Physlib status page

url: https://raw.githubusercontent.com/leanprover-community/physlib/master/Physlib/Particles/BeyondTheStandardModel/GeorgiGlashow/Basic.lean
fetched_utc: 2026-10-14T06:16:29Z
http_status: 200
sha256: 34f66288e28cd4f26f1d2338bf092acb6dc5cd92ecd54fa2c129e3e567152682
physlib_master_at_fetch: be0f21e5002d6d73b87f2055530c1e8bf7151546

Selected response headers (one request, curl with User-Agent "V3R1T4S scout (honest client)"):

```
HTTP/1.1 200 Connection Established
HTTP/2 200
cache-control: max-age=300
content-type: text/plain; charset=utf-8
etag: "a45207d8cc18aec99da72337968255d3073bc176b5c17ce41d7b769b08947932"
x-github-request-id: 0ADC:375FF7:1479C:18CC2:6ACF1E3D
date: Wed, 14 Oct 2026 06:16:29 GMT
source-age: 0
content-length: 1667
```

Extracted status (lines 28-36, 38-44, 46-49 of the fetched file, verbatim):

```
/-- The gauge group of the Georgi-Glashow model, i.e., `SU(5)`. -/
informal_definition GaugeGroupI where
  deps := []
  tag := "6V2WM"

/-- The homomorphism of the Standard Model gauge group into the Georgi-Glashow gauge group, i.e.,
the group homomorphism `SU(3) × SU(2) × U(1) → SU(5)` taking `(h, g, α)` to
`blockdiag (α ^ 3 g, α ^ (-2) h)`.

[line 37 not quoted: a reference link to Baez's GUT notes, page 34]
-/
informal_definition inclSM where
  deps := [``GaugeGroupI, ``StandardModel.GaugeGroupI]
  tag := "6V2WS"

/-- The kernel of the map `inclSM` is equal to the subgroup `StandardModel.gaugeGroupℤ₆SubGroup`.

[line 45 not quoted: a reference link to Baez's GUT notes, page 34]
-/
informal_lemma inclSM_ker where
  deps := [``inclSM]
  tag := "6V2W2"
```

The page itself is not copied here. Its sha256 above can be checked against the file at the commit named: `git -C physlib show be0f21e5002d6d73b87f2055530c1e8bf7151546:Physlib/Particles/BeyondTheStandardModel/GeorgiGlashow/Basic.lean | sha256sum`.
