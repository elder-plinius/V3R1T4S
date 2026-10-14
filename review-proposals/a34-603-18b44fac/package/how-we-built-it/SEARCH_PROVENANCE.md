# Reproducibility provenance

Source: `engine.cpp`, `scan.cpp` and related data preserved from previous research run, without editing. Original source witness SHA-256: `1a1d0958047e78b8d29752ccb0210518b170663b6862f84d57669c7b0c02d81e`. Target SHA-256: `18b44fac5d5ff1d4895fd9de1240669eb71543b3e15599f7f864e090aa1491ad`.

Input provenance: [upstream exact seed](https://github.com/elder-plinius/V3R1T4S/blob/7aca3835635e5323b48cdf3b5b59fcde502cab28/known-knowns/bigger-codes/codes/A34_8_7_602.txt). Output provenance: `how-we-built-it/seed_to_result_delta.json`. Twenty saved plateau checkpoints exist in the larger evidence archive but only the final checkpoint and selected logs are included here to keep package minimal. Earlier negative search neighborhoods are not a proof of nonexistence.

The preserved source code may depend on GCC/libstdc++ choices; verified target and delta do not. All code and data in this folder are contributor provenance, not verified mathematical assumptions.

The optional replay wrapper `reproduce_search.sh` is adapted to this package's directory layout. `original_reproduce_search.sh` is preserved byte-for-byte from the research archive. Original `check_code.py` and `check_subsets.py` are included so the replay wrapper runs without referring to missing paths.
