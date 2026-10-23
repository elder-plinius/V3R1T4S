# Replay the recorded construction

Run `python3 rebuild.py`. Expected final line: REBUILD PASS. The standard-library code replays selected constructive decisions using the unchanged discovery circuit primitives and verifies an exact156-addition ordered3x4x5 rank47 schedule. It does not rerun optimization or guarantee serialized-byte identity.

The original warm bridge command was `python3 followup.py --stage bridges --seed 71 --limit 320 --mag 2 --seconds 300 --trials 48 --warm`. Own predecessor circuits, commands, recorded source order and selected decisions are retained. Entire original dictionaries and runtime model-script hashes were not saved, so exact whole-search replay is unavailable. Archived model scripts are labelled post-discovery snapshots. No raw third-party data are distributed. The construction replay was actually run successfully.
