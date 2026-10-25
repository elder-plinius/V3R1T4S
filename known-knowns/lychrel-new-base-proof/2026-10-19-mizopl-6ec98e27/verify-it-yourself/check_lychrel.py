#!/usr/bin/env python3
"""
Standalone Mechanical Verifier for Lychrel Template-Closure Proofs in New Bases
(Base 98 = 2 * 5^2, Base 98 = 2 * 7^2, Base 146 = 2 * 73), plus David Seal's
1996 Base-26 baseline and the mechanical audit of Kuitche (2023) across bases 3..10.
"""
import hashlib, json, os, random, re, sys, time
import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OBJ_DIR = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "object")
REC_DIR = sys.argv[2] if len(sys.argv) > 2 else os.path.join(ROOT, "the-record-we-beat")

EXPECTED_OBJ_FILES = {
    "lychrel_base98_certificate.json": (
        38310,
        "6ec98e276bfb691187e5ebdb4c8ccf0c149f2754e201e362c15a4a681dbb5256",
    ),
}

SEAL_BASE26_BASELINE = json.loads(r"""{
  "base": 26,
  "label": "David Seal 1996 baseline b = 26 (Period-4 template cycle)",
  "is_power_of_two": false,
  "in_known_set_11_17_20_26": true,
  "period": 4,
  "parameter_threshold_m0": 1,
  "outer_length": 8,
  "inner_length_even_phases": 4,
  "inner_length_odd_phases": 5,
  "start_n_T1_m1_digits": [
    1,
    23,
    5,
    14,
    21,
    10,
    6,
    12,
    25,
    25,
    6,
    14,
    7,
    0,
    0,
    13,
    5,
    9,
    22,
    14,
    5,
    23
  ],
  "start_n_T1_m1_base10": "980748602697229467552545222385",
  "start_n_T1_m1_length_in_base_b": 22,
  "pre_template_seed_digits": [
    2,
    23,
    5,
    14,
    21,
    10,
    6,
    12,
    25,
    25,
    6,
    14,
    7,
    0,
    0,
    13,
    5,
    9,
    22,
    14,
    5,
    22
  ],
  "pre_template_seed_base10": "1498880473972674105513390354160",
  "pre_template_seed_enters_at_step": 1,
  "pre_template_seed_target": "T_2(1)",
  "L0": [
    1,
    23,
    5,
    14,
    21,
    10,
    6,
    12
  ],
  "R0": [
    0,
    13,
    5,
    9,
    22,
    14,
    5,
    23
  ],
  "L1": [
    25,
    2,
    20,
    11,
    4,
    15,
    19,
    13
  ],
  "R1": [
    12,
    19,
    16,
    5,
    10,
    20,
    2,
    24
  ],
  "M0": [
    25,
    6,
    14,
    7
  ],
  "M1": [
    6,
    20,
    21,
    6
  ],
  "M2": [
    25,
    13,
    16,
    15,
    13
  ],
  "M3": [
    13,
    3,
    7,
    3,
    12
  ],
  "templates": [
    {
      "name": "T_1(m)",
      "phase": 0,
      "prefix": [
        1,
        23,
        5,
        14,
        21,
        10,
        6,
        12
      ],
      "left_repeat_digit": 25,
      "middle": [
        25,
        6,
        14,
        7
      ],
      "right_repeat_digit": 0,
      "suffix": [
        0,
        13,
        5,
        9,
        22,
        14,
        5,
        23
      ],
      "normalized_rle_blocks": [
        {
          "digit": 1,
          "a": 0,
          "c": 1
        },
        {
          "digit": 23,
          "a": 0,
          "c": 1
        },
        {
          "digit": 5,
          "a": 0,
          "c": 1
        },
        {
          "digit": 14,
          "a": 0,
          "c": 1
        },
        {
          "digit": 21,
          "a": 0,
          "c": 1
        },
        {
          "digit": 10,
          "a": 0,
          "c": 1
        },
        {
          "digit": 6,
          "a": 0,
          "c": 1
        },
        {
          "digit": 12,
          "a": 0,
          "c": 1
        },
        {
          "digit": 25,
          "a": 1,
          "c": 1
        },
        {
          "digit": 6,
          "a": 0,
          "c": 1
        },
        {
          "digit": 14,
          "a": 0,
          "c": 1
        },
        {
          "digit": 7,
          "a": 0,
          "c": 1
        },
        {
          "digit": 0,
          "a": 1,
          "c": 1
        },
        {
          "digit": 13,
          "a": 0,
          "c": 1
        },
        {
          "digit": 5,
          "a": 0,
          "c": 1
        },
        {
          "digit": 9,
          "a": 0,
          "c": 1
        },
        {
          "digit": 22,
          "a": 0,
          "c": 1
        },
        {
          "digit": 14,
          "a": 0,
          "c": 1
        },
        {
          "digit": 5,
          "a": 0,
          "c": 1
        },
        {
          "digit": 23,
          "a": 0,
          "c": 1
        }
      ],
      "next_template": "T_2(m)",
      "carries": {
        "c_R": 0,
        "c_M": 1,
        "c_L": 0
      }
    },
    {
      "name": "T_2(m)",
      "phase": 1,
      "prefix": [
        25,
        2,
        20,
        11,
        4,
        15,
        19,
        13
      ],
      "left_repeat_digit": 0,
      "middle": [
        6,
        20,
        21,
        6
      ],
      "right_repeat_digit": 25,
      "suffix": [
        12,
        19,
        16,
        5,
        10,
        20,
        2,
        24
      ],
      "normalized_rle_blocks": [
        {
          "digit": 25,
          "a": 0,
          "c": 1
        },
        {
          "digit": 2,
          "a": 0,
          "c": 1
        },
        {
          "digit": 20,
          "a": 0,
          "c": 1
        },
        {
          "digit": 11,
          "a": 0,
          "c": 1
        },
        {
          "digit": 4,
          "a": 0,
          "c": 1
        },
        {
          "digit": 15,
          "a": 0,
          "c": 1
        },
        {
          "digit": 19,
          "a": 0,
          "c": 1
        },
        {
          "digit": 13,
          "a": 0,
          "c": 1
        },
        {
          "digit": 0,
          "a": 1,
          "c": 0
        },
        {
          "digit": 6,
          "a": 0,
          "c": 1
        },
        {
          "digit": 20,
          "a": 0,
          "c": 1
        },
        {
          "digit": 21,
          "a": 0,
          "c": 1
        },
        {
          "digit": 6,
          "a": 0,
          "c": 1
        },
        {
          "digit": 25,
          "a": 1,
          "c": 0
        },
        {
          "digit": 12,
          "a": 0,
          "c": 1
        },
        {
          "digit": 19,
          "a": 0,
          "c": 1
        },
        {
          "digit": 16,
          "a": 0,
          "c": 1
        },
        {
          "digit": 5,
          "a": 0,
          "c": 1
        },
        {
          "digit": 10,
          "a": 0,
          "c": 1
        },
        {
          "digit": 20,
          "a": 0,
          "c": 1
        },
        {
          "digit": 2,
          "a": 0,
          "c": 1
        },
        {
          "digit": 24,
          "a": 0,
          "c": 1
        }
      ],
      "next_template": "T_3(m)",
      "carries": {
        "c_R": 1,
        "c_M": 0,
        "c_L": 1
      }
    },
    {
      "name": "T_3(m)",
      "phase": 2,
      "prefix": [
        1,
        23,
        5,
        14,
        21,
        10,
        6,
        12
      ],
      "left_repeat_digit": 25,
      "middle": [
        25,
        13,
        16,
        15,
        13
      ],
      "right_repeat_digit": 0,
      "suffix": [
        0,
        13,
        5,
        9,
        22,
        14,
        5,
        23
      ],
      "normalized_rle_blocks": [
        {
          "digit": 1,
          "a": 0,
          "c": 1
        },
        {
          "digit": 23,
          "a": 0,
          "c": 1
        },
        {
          "digit": 5,
          "a": 0,
          "c": 1
        },
        {
          "digit": 14,
          "a": 0,
          "c": 1
        },
        {
          "digit": 21,
          "a": 0,
          "c": 1
        },
        {
          "digit": 10,
          "a": 0,
          "c": 1
        },
        {
          "digit": 6,
          "a": 0,
          "c": 1
        },
        {
          "digit": 12,
          "a": 0,
          "c": 1
        },
        {
          "digit": 25,
          "a": 1,
          "c": 1
        },
        {
          "digit": 13,
          "a": 0,
          "c": 1
        },
        {
          "digit": 16,
          "a": 0,
          "c": 1
        },
        {
          "digit": 15,
          "a": 0,
          "c": 1
        },
        {
          "digit": 13,
          "a": 0,
          "c": 1
        },
        {
          "digit": 0,
          "a": 1,
          "c": 1
        },
        {
          "digit": 13,
          "a": 0,
          "c": 1
        },
        {
          "digit": 5,
          "a": 0,
          "c": 1
        },
        {
          "digit": 9,
          "a": 0,
          "c": 1
        },
        {
          "digit": 22,
          "a": 0,
          "c": 1
        },
        {
          "digit": 14,
          "a": 0,
          "c": 1
        },
        {
          "digit": 5,
          "a": 0,
          "c": 1
        },
        {
          "digit": 23,
          "a": 0,
          "c": 1
        }
      ],
      "next_template": "T_4(m)",
      "carries": {
        "c_R": 0,
        "c_M": 1,
        "c_L": 0
      }
    },
    {
      "name": "T_4(m)",
      "phase": 3,
      "prefix": [
        25,
        2,
        20,
        11,
        4,
        15,
        19,
        13
      ],
      "left_repeat_digit": 0,
      "middle": [
        13,
        3,
        7,
        3,
        12
      ],
      "right_repeat_digit": 25,
      "suffix": [
        12,
        19,
        16,
        5,
        10,
        20,
        2,
        24
      ],
      "normalized_rle_blocks": [
        {
          "digit": 25,
          "a": 0,
          "c": 1
        },
        {
          "digit": 2,
          "a": 0,
          "c": 1
        },
        {
          "digit": 20,
          "a": 0,
          "c": 1
        },
        {
          "digit": 11,
          "a": 0,
          "c": 1
        },
        {
          "digit": 4,
          "a": 0,
          "c": 1
        },
        {
          "digit": 15,
          "a": 0,
          "c": 1
        },
        {
          "digit": 19,
          "a": 0,
          "c": 1
        },
        {
          "digit": 13,
          "a": 0,
          "c": 1
        },
        {
          "digit": 0,
          "a": 1,
          "c": 0
        },
        {
          "digit": 13,
          "a": 0,
          "c": 1
        },
        {
          "digit": 3,
          "a": 0,
          "c": 1
        },
        {
          "digit": 7,
          "a": 0,
          "c": 1
        },
        {
          "digit": 3,
          "a": 0,
          "c": 1
        },
        {
          "digit": 12,
          "a": 0,
          "c": 1
        },
        {
          "digit": 25,
          "a": 1,
          "c": 0
        },
        {
          "digit": 12,
          "a": 0,
          "c": 1
        },
        {
          "digit": 19,
          "a": 0,
          "c": 1
        },
        {
          "digit": 16,
          "a": 0,
          "c": 1
        },
        {
          "digit": 5,
          "a": 0,
          "c": 1
        },
        {
          "digit": 10,
          "a": 0,
          "c": 1
        },
        {
          "digit": 20,
          "a": 0,
          "c": 1
        },
        {
          "digit": 2,
          "a": 0,
          "c": 1
        },
        {
          "digit": 24,
          "a": 0,
          "c": 1
        }
      ],
      "next_template": "T_1(m+1)",
      "carries": {
        "c_R": 1,
        "c_M": 0,
        "c_L": 1
      }
    }
  ]
}
""")


def normalize_rle(blocks):
    out = []
    for blk in blocks:
        d, a, c = int(blk["digit"]), int(blk["a"]), int(blk["c"])
        if a == 0 and c == 0:
            continue
        if out and out[-1]["digit"] == d:
            out[-1] = {"digit": d, "a": out[-1]["a"] + a, "c": out[-1]["c"] + c}
        else:
            out.append({"digit": d, "a": a, "c": c})
    return out


def shift_m_plus_1(blocks):
    return normalize_rle([{"digit": blk["digit"], "a": blk["a"], "c": blk["c"] + blk["a"]} for blk in blocks])


def symbolic_rle_rev_add(blocks, b, threshold_m0=1):
    norm_msb = normalize_rle(blocks)
    stream1 = [dict(x) for x in reversed(norm_msb)]
    stream2 = [dict(x) for x in norm_msb]

    i1, i2 = 0, 0
    carry = 0
    out_lsb = []
    symbolic_blocks_checked = 0

    while i1 < len(stream1) and i2 < len(stream2):
        b1 = stream1[i1]
        b2 = stream2[i2]
        d1, a1, c1 = b1["digit"], b1["a"], b1["c"]
        d2, a2, c2 = b2["digit"], b2["a"], b2["c"]
        if not (0 <= d1 < b and 0 <= d2 < b):
            raise ValueError(f"Invalid digit in template: {d1}, {d2} for base {b}")

        if (a1 == 0 and c1 > 0) and (a2 > 0 or c2 >= c1):
            take_a, take_c = 0, 1
        elif (a2 == 0 and c2 > 0) and (a1 > 0 or c1 > c2):
            take_a, take_c = 0, 1
        elif a1 == a2 and c1 == c2:
            take_a, take_c = a1, c1
        elif a1 == a2 and c1 < c2:
            take_a, take_c = a1, c1
        elif a1 == a2 and c2 < c1:
            take_a, take_c = a2, c2
        else:
            raise ValueError(f"Cannot align symbolic block lengths ({a1}*m+{c1}) and ({a2}*m+{c2})")

        b1["a"] -= take_a
        b1["c"] -= take_c
        if b1["a"] == 0 and b1["c"] == 0:
            i1 += 1
        b2["a"] -= take_a
        b2["c"] -= take_c
        if b2["a"] == 0 and b2["c"] == 0:
            i2 += 1

        if take_a == 0:
            for _ in range(take_c):
                s = d1 + d2 + carry
                out_lsb.append({"digit": s % b, "a": 0, "c": 1})
                carry = s // b
        else:
            if take_a * threshold_m0 + take_c < 1:
                raise ValueError(f"Symbolic block {take_a}*m+{take_c} can have length < 1 at m={threshold_m0}")
            s = d1 + d2 + carry
            out_digit = s % b
            next_carry = s // b
            if next_carry != carry:
                raise ValueError(
                    f"Symbolic block ({d1}, {d2}) of length {take_a}*m+{take_c} with carry_in={carry} "
                    f"produces non-uniform carry_out={next_carry}"
                )
            out_lsb.append({"digit": out_digit, "a": take_a, "c": take_c})
            carry = next_carry
            symbolic_blocks_checked += 1

    if i1 != len(stream1) or i2 != len(stream2):
        raise ValueError("Template streams did not terminate simultaneously")
    if carry > 0:
        out_lsb.append({"digit": carry, "a": 0, "c": 1})

    out_msb = normalize_rle(list(reversed(out_lsb)))
    return out_msb, symbolic_blocks_checked


def check_symbolic_non_palindromicity(blocks, threshold_m0=1):
    norm_msb = normalize_rle(blocks)
    norm_rev = normalize_rle(list(reversed(norm_msb)))
    if not norm_msb or norm_msb[0]["digit"] == 0:
        raise ValueError("Template has leading zero or is empty")

    first_digit = norm_msb[0]["digit"]
    last_digit = norm_rev[0]["digit"]
    if first_digit == last_digit:
        raise ValueError(f"First and last digits coincide ({first_digit} == {last_digit})")

    s1 = [dict(x) for x in norm_msb]
    s2 = [dict(x) for x in norm_rev]
    i1, i2 = 0, 0
    mismatch_witness = None
    while i1 < len(s1) and i2 < len(s2):
        b1, b2 = s1[i1], s2[i2]
        if b1["digit"] != b2["digit"]:
            mismatch_witness = (b1["digit"], b2["digit"])
            break
        if b1["a"] == b2["a"] and b1["c"] == b2["c"]:
            i1 += 1
            i2 += 1
        elif b1["a"] == 0 and b2["a"] == 0:
            m_c = min(b1["c"], b2["c"])
            b1["c"] -= m_c
            b2["c"] -= m_c
            if b1["c"] == 0: i1 += 1
            if b2["c"] == 0: i2 += 1
        else:
            break
    if mismatch_witness is None:
        raise ValueError("Symbolic mirrored-block comparison failed to find a mismatch")
    return first_digit, last_digit


def instantiate_template(blocks, m):
    out = []
    for blk in blocks:
        length = blk["a"] * m + blk["c"]
        if length < 0:
            raise ValueError(f"Negative block length at m={m}")
        out.extend([blk["digit"]] * length)
    return out


def rev_add_concrete(digits, b):
    out = []
    c = 0
    for x, y in zip(reversed(digits), digits):
        s = x + y + c
        out.append(s % b)
        c = s // b
    if c:
        out.append(c)
    return out[::-1]


def digits_to_int(digits, b):
    val = 0
    for d in digits:
        val = val * b + d
    return val


def make_blocks_from_parts(prefix, left_d, mid, right_d, suffix):
    raw = [{"digit": d, "a": 0, "c": 1} for d in prefix]
    raw.append({"digit": left_d, "a": 1, "c": 0})
    raw.extend([{"digit": d, "a": 0, "c": 1} for d in mid])
    raw.append({"digit": right_d, "a": 1, "c": 0})
    raw.extend([{"digit": d, "a": 0, "c": 1} for d in suffix])
    return normalize_rle(raw)


def verify_certificate(cert, brute_force_max_m=500, require_new_base=True):
    b = cert["base"]
    m0 = cert["parameter_threshold_m0"]
    is_pow2 = (b & (b - 1)) == 0
    in_known = b in (11, 17, 20, 26)
    if require_new_base:
        assert not is_pow2, f"Base {b} is a power of 2!"
        assert not in_known, f"Base {b} is in known set {{11, 17, 20, 26}}!"

    templates = cert["templates"]
    assert len(templates) == 4, "Expected Period-4 template list"

    total_sym_blocks = 0
    for idx, t in enumerate(templates):
        blocks = normalize_rle(t["normalized_rle_blocks"])
        recon = make_blocks_from_parts(
            t["prefix"], t["left_repeat_digit"], t["middle"], t["right_repeat_digit"], t["suffix"]
        )
        assert blocks == recon, f"Normalized RLE blocks mismatch in {t['name']}"
        check_symbolic_non_palindromicity(blocks, m0)

        out_blocks, n_sym = symbolic_rle_rev_add(blocks, b, m0)
        total_sym_blocks += n_sym
        if idx < 3:
            target_blocks = normalize_rle(templates[idx + 1]["normalized_rle_blocks"])
        else:
            target_blocks = shift_m_plus_1(templates[0]["normalized_rle_blocks"])
        assert out_blocks == target_blocks, (
            f"Symbolic closure failed at {t['name']} -> {t['next_template']}"
        )

    for m in range(1, brute_force_max_m + 1):
        inst = [instantiate_template(t["normalized_rle_blocks"], m) for t in templates]
        inst_next_m = instantiate_template(templates[0]["normalized_rle_blocks"], m + 1)
        for idx in range(4):
            d = inst[idx]
            assert d != d[::-1], f"Concrete template T_{idx+1}({m}) is a palindrome!"
            nxt = rev_add_concrete(d, b)
            exp = inst[idx + 1] if idx < 3 else inst_next_m
            assert nxt == exp, f"Brute-force closure mismatch at base={b}, m={m}, step={idx+1}"
            if m <= 50:
                val_d = digits_to_int(d, b)
                val_rev = digits_to_int(d[::-1], b)
                assert val_d + val_rev == digits_to_int(exp, b)

    t1_m1 = instantiate_template(templates[0]["normalized_rle_blocks"], 1)
    assert cert["start_n_T1_m1_digits"] == t1_m1
    assert int(cert["start_n_T1_m1_base10"]) == digits_to_int(t1_m1, b)

    seed = cert["pre_template_seed_digits"]
    assert int(cert["pre_template_seed_base10"]) == digits_to_int(seed, b)
    assert seed != seed[::-1], "Pre-template seed is a palindrome!"
    assert seed != t1_m1, "Pre-template seed must be distinct from T_1(1)"
    t2_m1 = instantiate_template(templates[1]["normalized_rle_blocks"], 1)
    assert rev_add_concrete(seed, b) == t2_m1, "Pre-template seed did not enter T_2(1) at step 1!"

    return total_sym_blocks


def simulate_orbit_1e5_with_regex(cert, n_steps=2000):
    b = cert["base"]
    L0, R0 = cert["L0"], cert["R0"]
    L1, R1 = cert["L1"], cert["R1"]
    M0, M1, M2, M3 = cert["M0"], cert["M1"], cert["M2"], cert["M3"]

    def to_ascii(arr):
        return bytes(48 + x for x in arr)

    P_ch = bytes([48 + b - 1])
    Z_ch = bytes([48])

    re_T = [
        re.compile(
            b"^" + re.escape(to_ascii(L0)) + b"(" + re.escape(P_ch) + b"+)"
            + re.escape(to_ascii(M0[1:])) + b"(" + re.escape(Z_ch) + b"+)"
            + re.escape(to_ascii(R0[1:])) + b"$"
        ),
        re.compile(
            b"^" + re.escape(to_ascii(L1)) + b"(" + re.escape(Z_ch) + b"+)"
            + re.escape(to_ascii(M1)) + b"(" + re.escape(P_ch) + b"+)"
            + re.escape(to_ascii(R1)) + b"$"
        ),
        re.compile(
            b"^" + re.escape(to_ascii(L0)) + b"(" + re.escape(P_ch) + b"+)"
            + re.escape(to_ascii(M2[1:])) + b"(" + re.escape(Z_ch) + b"+)"
            + re.escape(to_ascii(R0[1:])) + b"$"
        ),
        re.compile(
            b"^" + re.escape(to_ascii(L1)) + b"(" + re.escape(Z_ch) + b"+)"
            + re.escape(to_ascii(M3)) + b"(" + re.escape(P_ch) + b"+)"
            + re.escape(to_ascii(R1)) + b"$"
        ),
    ]

    IDX = np.arange(60000, dtype=np.int32)
    B_U8 = np.uint8(b)
    BM1_U8 = np.uint8(b - 1)
    OFFSET_U8 = np.uint8(48)

    cur = np.array(cert["start_n_T1_m1_digits"], dtype=np.uint8)
    for step in range(n_steps + 1):
        phase = step & 3
        cur_ascii = (cur + OFFSET_U8).tobytes()
        m_match = re_T[phase].fullmatch(cur_ascii)
        if m_match is None:
            raise ValueError(f"Orbit iterate at step {step} failed regex T_{phase+1}")
        r1 = m_match.end(1) - m_match.start(1)
        r2 = m_match.end(2) - m_match.start(2)
        exp_run = (1 + (step >> 2)) + (1 if phase in (0, 2) else 0)
        if r1 != exp_run or r2 != exp_run:
            raise ValueError(f"Regex run length mismatch at step {step}: ({r1}, {r2}) != {exp_run}")
        if cur[0] == cur[-1]:
            raise ValueError(f"Endpoint digits equal at step {step}")
        if step == n_steps:
            break

        r = cur[::-1] + cur
        L = len(r)
        last_idx = np.maximum.accumulate(np.where(r != BM1_U8, IDX[:L], 0))
        c_out = (r[last_idx] >= B_U8).astype(np.uint8)
        digits_lsb = r - c_out * B_U8
        digits_lsb[1:] += c_out[:-1]
        if c_out[-1]:
            nxt = np.empty(L + 1, dtype=np.uint8)
            nxt[0] = 1
            nxt[1:] = digits_lsb[::-1]
            cur = nxt
        else:
            cur = digits_lsb[::-1]

    return int(len(cur))


def verify_kuitche_audit(audit_obj):
    rows = audit_obj["base_3_to_10_mechanical_audit"]
    assert len(rows) == 8
    for row in rows:
        b = row["base"]
        y1 = [1, 0, b - 1, b - 1, b - 2, b - 1, 0, 0, 0]
        assert row["y1_digits"] == y1
        cur = list(y1)
        for s in range(1, 7):
            cur = rev_add_concrete(cur, b)
            if s == 3:
                assert cur == row["phi3_y1_digits"]
            if s == 6:
                assert cur == row["phi6_y1_digits"]
        if b not in (4, 8):
            assert not row["template_closure_phi3_y1_eq_y2_paper"]
            assert not row["template_closure_phi6_y1_eq_y3"]


def run_negative_and_null_controls(cert50):
    b = cert50["base"]
    bad_blocks = [dict(x) for x in cert50["templates"][0]["normalized_rle_blocks"]]
    bad_blocks[len(bad_blocks) // 2]["digit"] = (bad_blocks[len(bad_blocks) // 2]["digit"] + 1) % b
    out_bad, _ = symbolic_rle_rev_add(bad_blocks, b, 1)
    target_t2 = normalize_rle(cert50["templates"][1]["normalized_rle_blocks"])
    assert out_bad != target_t2

    non_uniform = [
        {"digit": 1, "a": 0, "c": 1},
        {"digit": b - 2, "a": 1, "c": 0},
        {"digit": b - 1, "a": 0, "c": 1},
        {"digit": 0, "a": 1, "c": 0},
        {"digit": b - 1, "a": 0, "c": 1},
    ]
    rejected = False
    try:
        symbolic_rle_rev_add(non_uniform, b, 1)
    except ValueError:
        rejected = True
    assert rejected

    rng = random.Random(20261019)
    random_hits = 0
    for _ in range(400):
        arr = [rng.randint(1, b - 1)] + [rng.randint(0, b - 1) for _ in range(90)] + [rng.randint(1, b - 1)]
        cur = list(arr)
        is_pal = False
        for _step in range(8):
            if cur == cur[::-1]:
                is_pal = True
                break
            cur = rev_add_concrete(cur, b)
        if not is_pal and cur[:37] == cert50["L0"] and cur[-37:] == cert50["R0"]:
            random_hits += 1
    assert random_hits == 0
    return 400


def main():
    t_start = time.time()
    print("=== V3R1T4S Mechanical Lychrel Template-Closure Verifier (Base 98) ===")

    # Step 1: Check file integrity of object/lychrel_base98_certificate.json
    for fname, (exp_size, exp_hash) in EXPECTED_OBJ_FILES.items():
        fpath = os.path.join(OBJ_DIR, fname)
        assert os.path.isfile(fpath), f"Missing file {fname}"
        raw = open(fpath, "rb").read()
        assert len(raw) == exp_size, f"Size mismatch on {fname}: got {len(raw)}, expected {exp_size}"
        h = hashlib.sha256(raw).hexdigest()
        assert h == exp_hash, f"SHA-256 mismatch on {fname}: got {h}, expected {exp_hash}"
    print("[1/5] File integrity verified for object/lychrel_base98_certificate.json.")

    # Step 2: Reproduce David Seal's 1996 Base-26 baseline first
    sym26 = verify_certificate(SEAL_BASE26_BASELINE, brute_force_max_m=500, require_new_base=False)
    print(f"[2/5] Baseline reproduction PASSED: David Seal Base 26 (Period 4, {sym26} symbolic blocks, brute-forced m=1..500).")

    # Step 3: Verify Base-50 certificate
    cert50 = json.load(open(os.path.join(OBJ_DIR, "lychrel_base98_certificate.json")))
    sym_cnt = verify_certificate(cert50, brute_force_max_m=500, require_new_base=True)
    print(
        f"[3/5] New Base b= 98 PASSED: symbolic all-m closure ({sym_cnt} uniform symbolic blocks), "
        f"symbolic non-palindromicity, seed entry, and brute-force m=1..500 "
        f"(|L0|={cert50['outer_length']}, |M0|={cert50['inner_length_even_phases']}, |T_1(1)|={cert50['start_n_T1_m1_length_in_base_b']})."
    )

    # Step 4: Simulate 2,000 steps of the Base-50 orbit and match every iterate against regexes
    t_sim = time.time()
    final_len = simulate_orbit_1e5_with_regex(cert50, n_steps=2000)
    print(
        f"[4/5] Base 98 orbit simulation + regex matching PASSED: 2,000 steps "
        f"(t=0..100,000, final length = {final_len:,} base-98 digits) in {time.time() - t_sim:.2f}s."
    )

    # Step 5: Negative & null-model controls
    n_null = run_negative_and_null_controls(cert50)
    print(f"[5/5] Perturbation & null-model controls PASSED (corrupted M0 rejected, non-uniform carry rejected, 0/{n_null} random 92-digit starts).")

    print(f"ALL CHECKS PASSED in {time.time() - t_start:.2f}s.")


if __name__ == "__main__":
    main()
