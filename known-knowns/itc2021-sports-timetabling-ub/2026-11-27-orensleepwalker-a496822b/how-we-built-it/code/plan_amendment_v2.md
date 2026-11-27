# Plan amendment v2 (Andy, 2026-11-26T01:05Z; dated, plan.json v1 kept unchanged)

Survivor rule v1 ("share of window solves not proven optimal >= 0.20, or >= 5 equal-score moves") cannot discriminate: the adaptive window
sizes deliberately grow until windows reach the edge of what solves in 15 s, so about a quarter of window solves end unresolved on every
instance. In round 1 of the fixed-pattern method all 9 group-D instances passed it with zero improvements and 0-2 equal-score moves; keeping
it would spend the whole night on fixed-pattern rounds 2-3 and never reach the open-pattern method or group E, against Boss's intent
("survivors ... you consider there is reason to run again").

Rule v2 (applies from now, to every round and method): survivor = not a win, and (at least one improvement in the run, or at least 5
equal-score moves to a different timetable). Under v2 no fixed-pattern round-1 instance survives; the programme continues with the
open-pattern method, round 1, all 9 group-D instances, then group E as planned. The aborted start of fixed round 2 on Middle 9 (about 3
minutes, no result) is kept in out/aborted/. Everything else in plan.json is unchanged.
