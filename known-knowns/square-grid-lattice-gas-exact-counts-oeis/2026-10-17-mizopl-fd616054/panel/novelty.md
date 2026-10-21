# NOVELTY panel verdict — A054759(15)

context: subagent (general-purpose)

## Scope

I am the NOVELTY skeptic. I checked ONLY whether the claimed term genuinely
extends what is published (index 15 unpublished). I did NOT verify the
numerical correctness of the value — that is another panelist's job.

## Primary status source — fetched ONCE, no retries

- URL: https://oeis.org/A054759/b054759.txt
- HTTP status: HTTP 200
- UTC time of fetch: 2026-10-17 13:01:03 UTC (run of `date -u` immediately after the curl)
- User-Agent used: "V3R1T4S-agent (research; honest client)"
- Page sha256: `26a837111876762bf9d1c5892c21ec1a15c36e00b0ee9e45bd2c389741cbfada`
- Largest index present in b-file: **14**
- Value at index 14: **15844635835975276495290739119895808472**
- Index 15: **NOT present** in the b-file.

I also fetched the sequence page https://oeis.org/A054759 (HTTP 200). Its DATA
line ends at a(14) = 15844635835975276495290739119895808472; the claimed 43-digit
value 4310182149988584261406143524214457416387448 does NOT appear on the page.
The extension note credits a(14) to Brendan McKay, Apr 18 2024 — within the last
~24 months — and no a(15) has followed.

### Cross-check against package snapshot

The fetched b-file https://oeis.org/A054759/b054759.txt has sha256
`26a837111876762bf9d1c5892c21ec1a15c36e00b0ee9e45bd2c389741cbfada`, matching the
snapshot metadata recorded in `the-record-we-beat/snapshot.md`, and its tail ends
at index 14.

## Literature search (~last 24 months)

Searched arXiv, OEIS pages/links, GitHub and the open web:
- Exact 43-digit value "4310182149988584261406143524214457416387448": zero relevant hits anywhere.
- "Eulerian orientations 15x15 square torus" / "A054759 a(15)": no paper, preprint,
  GitHub repo, or OEIS extension gives a 15th term.
- Related work (Isaev–McKay–Zhang cumulant expansion, arXiv 2309.15473; Lieb/Baxter
  asymptotics; OEIS A298119/A298201) discusses the model but publishes no a(15).

No prior publication of A054759(15) or of the number of Eulerian orientations of
the 15×15 torus was found.

## Verdict

The largest published index for A054759 is 14; index 15 is genuinely unpublished.
The claimed a(15) strictly extends the known range (one term past the published
b-file and DATA). On the NOVELTY dimension only, this passes. (No tie, no
already-published value.)

pass: true
