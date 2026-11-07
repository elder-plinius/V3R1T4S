# The record we beat: Physlib status page

url: https://raw.githubusercontent.com/leanprover-community/physlib/master/Physlib/Relativity/LorentzGroup/Restricted/Basic.lean
fetched_utc: 2026-10-14T06:07:15Z
http_status: 200
sha256: e41850ba01879f3a9a6c3934efd85aab5b4a1a48c8d8a4621da63f7c5296f1c9
physlib_master_at_fetch: be0f21e5002d6d73b87f2055530c1e8bf7151546

Selected response headers (one request, curl with User-Agent "V3R1T4S scout (honest client)"):

```
HTTP/1.1 200 Connection Established
HTTP/2 200
cache-control: max-age=300
content-type: text/plain; charset=utf-8
etag: "1fcaed2240e9c4ddb9847dbef3ccec8d4184d2f98f0ca9378f776373f971b960"
x-github-request-id: C6D6:32C6F4:10843A:1B3305:6ACF0E37
date: Wed, 14 Oct 2026 06:07:16 GMT
source-age: 0
content-length: 2937
```

Extracted status (lines 61-63 of the fetched file, verbatim):

```
/-- The restricted Lorentz group is connected. -/
semiformal_result "FXNL5" restricted_isConnected {d : ℕ} :
  IsConnected (restricted d : Set (LorentzGroup d))
```

The page itself is not copied here. Its sha256 above can be checked against the file at the commit named: `git -C physlib show be0f21e5002d6d73b87f2055530c1e8bf7151546:Physlib/Relativity/LorentzGroup/Restricted/Basic.lean | sha256sum`.
