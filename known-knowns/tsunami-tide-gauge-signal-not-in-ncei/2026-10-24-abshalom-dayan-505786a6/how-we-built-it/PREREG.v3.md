# PREREG v3 (frozen 2026-10-24T19:45:43Z, date -u). Adds one rule; changes nothing in PREREG.md or PREREG.v2.md. Written while the map runs and before any map result was read (only progress lines with class names were seen in the logs).

null_test: required

Main-win candidates from the map: any quake of the p3 map that is not LISTED (no NCEI event of any validity or cause
within +/- 1 day and 1000 km, NCEI events fetched 19:20Z) and has >= 2 PASSING sites at the real origin is a main-win
candidate. Each gets exactly the PREREG.md section 5 network null (frozen site list = every site in scope USABLE at the
real origin; 400 control origins uniform on minutes in [o-40 d, o-2 d] U [o+3 d, o+40 d], seed 20261024; real-window rule
only; score = (K detecting sites, S second-largest r), lexicographic; the real score must beat every control). A
candidate that beats every control gets the live NCEI events and runups re-fetch, then the three-skeptic panel. Fetching
for the null uses one long window per code, [floor_h(o-41 d), ceil_h(o+41 d)], split into requests of at most 20 days.
