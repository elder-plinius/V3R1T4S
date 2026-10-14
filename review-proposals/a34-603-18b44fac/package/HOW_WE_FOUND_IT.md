# How we found it

Contributor text, unverified.

An independent C++ implementation of V3R1T4S's blocker-guided plateau / exchange strategy was warm-started from that repository's 602-word code. A complete census of all 5,379,616 weight-7 binary vectors showed that no outside word could be inserted directly. The method then performed equal-cardinality exchanges to move between valid 602-word codes, searching each reached neighborhood for a cardinality-increasing exchange. Twenty plateau transitions led to a two-for-three exchange, yielding the 603-word witness. The final two-for-three change applies to the 19th saved 602-word checkpoint, *not* directly to the public 602-word seed. The portable, auditable parent-to-result certificate contains 38 removals and 39 additions. The search run reported 970,989 attempted neighborhoods and 25.3494 seconds on its original environment; those counts are not claims of global exhaustiveness.

No novel general construction method or optimality proof is claimed; rerunning the search is optional because the complete finite witness and exact parent-to-result certificate are included. See the saved code and logs under how-we-built-it/.
