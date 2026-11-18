# Verification Receipts (`RECEIPTS.md`)

- Verifier script: `verify-it-yourself/verify.py` (`sha256: 8cd6e40c4333ee55034766b67030374b33d0a3fd6d69a1be7f00c1eb3eea62c8`)
- Unified certificate JSON: `object/00_nist_aes_gd10_and_barriers_certificate.json` (`sha256: 717e3701dc2a42b9966c099120b68c41b1633773141617d0cf8f97674554305d`)
- `object/aes-invmixcols-xor92-depth10.circ.txt`: `sha256: 4e19fc9a8d5760e80e94a6c33b1576e00d18eac15ef1f2865cd982e019138e44`
- `object/aes-invmixcols-xor92-depth10-alt.circ.txt`: `sha256: b3bc80eef37100bd092e9b3e01df7f53ddaadb8a476944bd4f4d5bd638ce8ae0`
- `object/aes-invsbox-a57-ad4-g152-gd10-xx95-25.circ.txt`: `sha256: 3cea2983de3590acc3d5755055f28e8f74306d1101ab9b18a598c451aad0fed6`
- `object/aes-invsbox-a56-ad4-g155-gd10-xx99-26.circ.txt`: `sha256: c83ba275b29dddeb4b435b3a3c6a1e41fd51d93ab3023a62fe70e699de0629b6`
- `object/aes-invsbox-a33-ad4-g111-gd14-xx78-39.circ.txt`: `sha256: aa18325ecb4675691d77c177623191086acf36ba935d78541ce14afff788633e`
- `object/aes-invsbox-a34-ad4-g111-gd14-xx77-41.circ.txt`: `sha256: 7dad433aafaf21e6e97ebd345ba71efefd1ec45c3943dc863a6ba7e5bf9749ab`
- `object/aes-invsbox-a33-ad4-g109-gd15-xx76-36.circ.txt`: `sha256: 71c604e3f0f3b4c4bfb2c0d11dcc18ba14f1cececb193febb29c1cbf1e1217ab`
- `object/aes-invsbox-a35-ad4-g129-gd13-xx94-42.circ.txt`: `sha256: 0a0d9bcc0073d04c4a6369e44db22360a5583502cf02f364b94b3046621107a1`
- `object/aes-sbox-a37-ad4-g119-gd14-xx82-33.circ.txt`: `sha256: 3380e6da4f6a7dc3886d6cdecd51b996d0552b28911e8d718e91a32875d61df3`
- `object/aes-invsbox-a32-ad5-g116-gd16-xx84-46.circ.txt`: `sha256: 92b64b24cef66820514f05f5fab3c12f9938ae1451adda0b0675946cccb7cb8f`
- `object/aes-invsbox-a32-ad5-g114-gd19-xx82-17.circ.txt`: `sha256: 7cb05a3d51323bf9f24152aec35d6141e7334534af91803706eecc3db040b885`
- `object/aes-invsbox-a28-ad4-g143-gd16-xx115-59.circ.txt`: `sha256: 44eb1bf275f5c385ca51c7125d446510824fd689295dc83cbf6337e0d6f0bfad`
- `object/aes-invsbox-a28-ad4-g134-gd19-xx106-46.circ.txt`: `sha256: e9faba1333a24b23bce7137d111b26f9987fd402382fb49cf95e9cd15a932e54`

## 1. Clean Package Execution (`exit 0`)

```sh
sh verify-it-yourself/run_checks.sh
```

```text
VERIFICATION SUMMARY: Verified 13/13 NCFF-0.1-2026 AES circuits (2/2 pure-XOR InvMixColumns 92@10 [p3, overlap=72/92, symdiff=40], 2/2 zero-NOT GD=10 InvS-box 152@10 & 155@10 [p4], and 9/9 zero-NOT [Inv]S-box witnesses across 8 4D Pareto cells led by 33/4/111/14, 109@15, 129@13, 119@14; 0 NOT, 0 constants, 0 self-inputs, 0 dead gates) + T1..T6 exact algebraic tightness & 2,040-conjugate checks in 0.241s
PASS
```

Exit status: `0`

## 2. Adversarial `--corrupt` Negative Control (`exit 1`)

```sh
sh verify-it-yourself/run_checks.sh --corrupt
```

```text
VERIFICATION ERROR: aes-invmixcols-xor92-depth10.circ.txt: LINEAR_MAP_MISMATCH on output y3 (got 0xadef2d62, expected 0xa9eb2d67)
FAIL
```

Exit status: `1`
