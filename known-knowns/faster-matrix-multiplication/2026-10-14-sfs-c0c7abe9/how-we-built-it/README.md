# Replay the recorded construction

Run `python3 rebuild.py`. Expected final line: REBUILD PASS. Standard-library code replays the selected constructive operations using the discovery circuit primitives and verifies an exact 354-addition ordered 5x5x5 rank-93 program. It does not rerun optimization or promise serialized-byte identity.

Actual search events, selected records, own warm predecessors, code snapshots and recorded hashes are included. Some original dictionaries and earlier runtime state were not retained; exact replay of the complete discovery history is unavailable and unclaimed. The final archive hashes are distinguished from observed runtime hashes in discovery-manifest.json. No raw public source data are distributed.
