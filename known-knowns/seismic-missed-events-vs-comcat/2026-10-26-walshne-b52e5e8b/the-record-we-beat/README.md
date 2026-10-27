# The record

record.json holds, for each request: the URL, UTC fetch time, HTTP status, selected headers, byte count and sha256 of
the response. The pages themselves are not copied in.

| what | URL | fetched (UTC) | HTTP | extracted value |
|---|---|---|---|---|
| status source (ComCat FDSN event service page) | https://earthquake.usgs.gov/fdsnws/event/1/ | 2026-10-26T22:01:46Z | 200 | service up (sha256 8a771019eaae55f35cf94a2cfa5f4265a9c1e3430ae2654b35a65d5a8403d9af) |
| ComCat, +/-30 s, 50 km, all types | https://earthquake.usgs.gov/fdsnws/event/1/query?format=csv&starttime=2024-12-09T23:19:43&endtime=2024-12-09T23:20:44&latitude=39.1635&longitude=-119.0459&maxradiuskm=50 | 2026-10-26T22:01:46Z | 200 | 0 events (header only, 160 bytes, sha256 d0011b19654d4069505c5263bdbd23d0992301571b783f489577472ebd3a7f17) |
| ISC, +/-30 s, 0.45 deg | https://www.isc.ac.uk/fdsnws/event/1/query?starttime=2024-12-09T23:19:43&endtime=2024-12-09T23:20:44&latitude=39.1635&longitude=-119.0459&maxradius=0.45&format=text | 2026-10-26T22:01:47Z | 204 | no event |

Earlier fetches of the same ComCat query returned the identical 160-byte header: 2026-10-26T17:29:28Z and 19:13:26Z
(how-we-built-it/data/fetchlog_absence.jsonl).
