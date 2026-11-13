# Disclosure policy

How much of a result we publish depends on what kind of problem it is.

**Open science and record tables** (degree-diameter graphs, constant-weight codes, matrix multiplication, number-theory
bounds, finished verification competitions such as VNN-COMP 2026, public robustness leaderboards such as RobustBench). Objects are published in full, because checking them is the point. The table maintainer is told by a
human, through the channel their page asks for; no maintainer has reviewed or endorsed anything here yet. The sources
we build on are named and credited.

**Live puzzles and challenges with a setter or a solver table** (for example J.-F. Bouchaudy's Cipher Machines
Challenge, MysteryTwister, any contest). We never publish keys, settings, plaintext, the plaintext's language, its
theme, names, places, cribs, or method details specific enough to shortcut the problem. The solution goes privately
to the setter only. This repository holds only a **salted** hash commitment (the salt is kept private) and a link to
the setter's own table. We reveal only with the setter's explicit permission, and even then not while others are
actively competing.

**Prize and bounty challenges.** Commit-only, like live puzzles: we follow the organiser's rules and disclose only
through their channel, submitted by a human.

**Herculaneum scrolls (Vesuvius Challenge).** The data is never redistributed, and readings or images of unread text
are never published anywhere; they go only through the official prize process.

**Sealed locations (wrecks, crash sites, graves, unrecorded archaeological sites).** Commit-only. A public claim
carries only a salted hash commitment of the coordinates and the evidence, and no region at all: its envelope's
problem line is exactly `problem: sealed location` (`kit/SUBMIT.md` section 2). The target id's country-level scope
is the only geographic information a sealed claim shows. The exact place goes privately to the responsible
authority (the heritage agency, the hydrographic office, the naval history or missing-personnel service), sent by a
human; any region the authority needs lives in the private bundle. The commitment is opened in public only after
the authority has published the site's location in its own record or agrees in writing; where no functioning
authority exists, the location stays sealed with the human. Public remote-sensing data only: nobody visits, dives on, digs,
metal-detects, disturbs, recovers or removes anything. Many of these sites are protected by law, and published
coordinates invite looting (`kit/POLICY.md`, Sealed locations).

**Benchmarks with held-out data.** We never publish held-out labels or anything that leaks them, and we follow the
organiser's protocol.

**Historical ciphers with no living setter.** Published only after review by an outside expert.

**Corrections and takedown requests** from setters, maintainers and authors are honoured promptly (see `READ_BEFORE_CITING.md`,
Corrections).
