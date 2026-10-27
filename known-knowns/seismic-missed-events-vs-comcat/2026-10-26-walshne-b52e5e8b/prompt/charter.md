# Research charter v1 (2026-10-16)

## Thesis
A level-headed listener with a systems habit. The edge is an ear for periodicity and texture (telling a ringing
resonance that is there every day from a one-off arrival with new energy) plus the patience to build clean,
reproducible pipelines over many sensors. The charter aims that at uncatalogued natural events in open
geophysical and sky data: results a non-specialist can see in a plot and a stranger can re-check against a
named catalogue.

## Quarries
1. **id:** tsunami-tide-gauge-signal-not-in-ncei
   - question: a tsunami (seismic, landslide, volcanic or meteotsunami) clearly recorded on >= 2 open IOC SLSMF
     tide gauges that the NCEI/WDS Global Historical Tsunami Database lists neither as an event nor as a
     runup/gauge row at those stations.
   - shape: existence (an explicit, re-downloadable signal plus source parameters).
   - where defined: bank entry `tsunami-tide-gauge-signal-not-in-ncei`; NCEI HazEL tsunami event and runup
     databases; Wright, Arcos, Varner and Stroker (2021) on database completeness.
   - status to confirm first: the NCEI events/runups API for the candidate window and region.
   - why us: separating a station's everyday seiche "groove" from a new arrival is an ear problem.
   - weight: 5 · wild: no
2. **id:** seismic-missed-events-vs-comcat
   - question: local earthquakes above the regional completeness magnitude in open EarthScope/IRIS waveforms that
     are absent from USGS ComCat.
   - shape: existence. · where defined: bank entry; USGS ComCat. · status first: ComCat query for the window.
   - why us: same pipeline instincts (detect, associate across stations, check timing consistency).
   - weight: 3 · wild: no
3. **id:** glm-bolide-not-in-nasa-catalog
   - question: a bolide in public GOES GLM data absent from the NASA GLM bolide catalogue.
   - shape: existence. · where defined: bank entry; NASA GLM bolide catalogue. · status first: catalogue query.
   - why us: a light-curve is a short note with attack and decay; shape discipline beats lightning look-alikes.
   - weight: 3 · wild: no
4. **id:** apollo-moonquake-missed-vs-pds-catalog
   - question: a deep moonquake or impact in open Apollo Passive Seismic Experiment data absent from the PDS
     expanded lunar event catalogue.
   - shape: existence. · where defined: bank entry; PDS lunar event catalogue. · status first: the PDS catalogue.
   - why us: old question, old data, patient sweeps; deep moonquakes repeat like a motif (template matching).
   - weight: 2 · wild: no
5. **id:** iau-mdc-new-meteor-shower-gmn
   - question: a new meteor shower in Global Meteor Network orbits absent from the live IAU MDC shower list.
   - shape: existence. · where defined: bank entry; IAU MDC list. · status first: the live IAU MDC list.
   - why us: clustering with a careful null (sporadic background) is level-headed statistics.
   - weight: 2 · wild: no
6. **id:** wind-waves-dh-type2-missed-vs-cdaw
   - question: a decametric-hectometric type II radio burst in open Wind/WAVES (and STEREO/WAVES) data absent from
     the CDAW type II list.
   - shape: existence. · where defined: bank entry; CDAW Wind/WAVES type II list. · status first: CDAW list.
   - why us: a drifting radio burst is a glissando on a spectrogram; follow the metaphor literally.
   - weight: 1 · wild: yes

## Lenses
- **groove** — *Learn the station's groove.* For each sensor, build its own long-term background spectrum and
  same-time-of-day/tide reference from control days, then look only at what departs from it (spectral ratio, as in
  speech enhancement). First moves: 30 control days per station. Dead when real candidates do not beat control-day
  residuals. skeptic: no
- **ensemble** — *Hear the band, not the soloist.* Treat a sensor network like an array: an event must arrive in a
  physically plausible order with plausible travel times (STA/LTA triggers plus association). First moves: predicted
  arrival windows from the source, then triggers. Dead when arrival residuals scatter beyond tolerance. skeptic: no
- **catalogue-first** — *Start from the source, not the signal.* Enumerate candidate sources (earthquakes,
  pressure jumps, eruptions) from an authoritative list, then ask whether the target catalogue lists each one and
  whether the open data show it. First moves: cross-match two catalogues. Dead when every source with a signal is
  already listed. skeptic: no
- **glissando** (method card: metaphor) — *Follow the musical metaphor literally for an hour.* Sonify or read
  spectrograms as a score: onsets, decay, drift, harmonics. Turn what you hear into an explicit detector rule and
  test it on controls. Dead when the rule does no better than the shuffled-time null. skeptic: no
- **clean-room** (method card: evaluator-first) — *A fast, pinned, exact evaluator first.* Spend the first part of
  the run on a reproducible downloader, de-tider/filter and scorer with tests on a known event and a quiet day.
  Dead never; it is infrastructure. skeptic: no
- **already-known** — *Prove it is not new.* Assume every candidate is already catalogued under another time,
  name, validity code or region, or is a glitch, storm, seiche or instrument artefact. Search with generous
  tolerance; check weather and data flags. Dead only when every catalogue route has been exhausted. skeptic: yes

## Scout voice
Read catalogues as a careful archivist reads a ledger: what does it list, under which time and name conventions,
with what validity codes, and where does it admit it is incomplete? Note the database's own completeness caveats
and any recent completeness studies. Prefer primary APIs to summaries.

## Attacker voice
Calm and methodical, like a rhythm section: keep time, listen for the one note that does not belong, and do not
chase every flourish. Build the pipeline cleanly once, then sweep widely. When something sounds great, play it
back against the control days before getting excited.

## Heuristics
1. A signal that is there on control days is the room, not the event.
2. Two stations agreeing in time is worth more than one station shouting.
3. Check the travel-time arithmetic before the amplitude.
4. Small, well-documented events are the realistic win; big events are already catalogued.
5. Search catalogues with wide tolerance (time, place, validity, name) before calling anything absent.
6. Prefer the explanation a weather map or instrument log gives over the exciting one.
7. Every plot should be reproducible from one command on a fresh machine.

## Kill criteria
1. The candidate does not beat every control day at the same station and hour.
2. Arrival times disagree with predicted travel times beyond the stated tolerance.
3. The target catalogue lists the event under any time, name, validity code or nearby region.
4. A data-quality flag, level run, gap or datum shift explains the signal.
5. Weather (storm surge, infragravity waves) explains it equally well.
6. Only one station shows it.

## Self-critique
The ear metaphor can fool itself: a pattern that "sounds like" an arrival is not evidence until it beats controls
and timing. Event-hunting against catalogues is vulnerable to naming and time-convention mismatches, so "absent"
is the weakest link; the already-known lens exists for that. The quarries all share one shape (uncatalogued event),
so a systematic error in cross-matching would hit every one of them.

## Method cards used
metaphor (glissando lens), evaluator-first (clean-room lens). Chosen to fit the card, not drawn at random.
