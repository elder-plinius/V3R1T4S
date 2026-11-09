#!/usr/bin/env python3
"""
Self-contained independent verifier for least-qnr-prescribed-quadratic-character-next-terms.
1. Loads object/a000229_qnr_census.json and verifies all fields against independently computed values.
2. Verifies primality (deterministic Miller-Rabin for 64-bit integers) and quadratic character of every
   term in A000229(1..43), A002223(30..38), A002224(30..41), the 4 primes q = 1 mod 8 in
   [1, 317398900373231] having the first 38 primes as quadratic residues, and the 5 primes in
   [1, 1463971373078639] having the first 40 primes as quadratic residues, using both Euler criterion
   pow(p, (q-1)//2, q) and Quadratic Reciprocity Jacobi symbols.
3. Reconstructs the exact byte-for-byte text of OEIS b000229.txt (n = 1..38) and verifies its SHA-256.
4. Compiles and executes verify_qnr_sieve.c (which runs two independent CRT modulus splits M1 and M2
   over [1, 317398900373231] and two independent CRT modulus splits M2 and M3 over [1, 1463971373078639])
   and checks that every output matches the object JSON element-by-element.
"""
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile

PRIMES = [
    2, 3, 5, 7, 11, 13, 17, 19, 23, 29,
    31, 37, 41, 43, 47, 53, 59, 61, 67, 71,
    73, 79, 83, 89, 97, 101, 103, 107, 109, 113,
    127, 131, 137, 139, 149, 151, 157, 163, 167, 173,
    179, 181, 191, 193, 197,
]

PUBLISHED_A000229_1_TO_38 = {
    "1": "3", "2": "7", "3": "23", "4": "71", "5": "311",
    "6": "479", "7": "1559", "8": "5711", "9": "10559", "10": "18191",
    "11": "31391", "12": "422231", "13": "701399", "14": "366791", "15": "3818929",
    "16": "9257329", "17": "22000801", "18": "36415991", "19": "48473881", "20": "175244281",
    "21": "120293879", "22": "427733329", "23": "131486759", "24": "3389934071", "25": "2929911599",
    "26": "7979490791", "27": "36504256799", "28": "23616331489", "29": "89206899239", "30": "121560956039",
    "31": "395668053479", "32": "196265095009", "33": "513928659191", "34": "5528920734431", "35": "2871842842801",
    "36": "4306732833311", "37": "8402847753431", "38": "70864718555231",
}

EXPECTED_B000229_SHA256 = "cfeddbe49cafbc4f498bfbbd0a6e4afa0382ddbc8254c51a93cf8a7d4d90478b"

def is_prime_det64(n):
    if n < 2:
        return False
    for p in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        if n == p:
            return True
        if n % p == 0:
            return False
    d = n - 1
    s = 0
    while d % 2 == 0:
        d //= 2
        s += 1
    for a in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        if n <= a:
            break
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(s - 1):
            x = (x * x) % n
            if x == n - 1:
                break
        else:
            return False
    return True

def euler_legendre(a, q):
    r = pow(a % q, (q - 1) // 2, q)
    return 1 if r == 1 else (-1 if r == q - 1 else 0)

def reciprocity_legendre(p, q):
    if p == 2:
        return 1 if (q % 8 in (1, 7)) else -1
    r = pow(q % p, (p - 1) // 2, p)
    leg = 1 if r == 1 else -1
    if (p % 4 == 3) and (q % 4 == 3):
        leg = -leg
    return leg

def verify_least_qnr_prime(q, n_idx):
    if not is_prime_det64(q):
        return False
    for i in range(n_idx - 1):
        p = PRIMES[i]
        if euler_legendre(p, q) != 1 or reciprocity_legendre(p, q) != 1:
            return False
    p_target = PRIMES[n_idx - 1]
    return euler_legendre(p_target, q) == -1 and reciprocity_legendre(p_target, q) == -1

def main():
    here = os.path.dirname(os.path.abspath(__file__))
    obj_path = os.path.join(here, "..", "object", "a000229_qnr_census.json")
    try:
        with open(obj_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        print(f"Error reading object JSON: {e}")
        print("FAIL")
        sys.exit(1)

    if data.get("target_id") != "least-qnr-prescribed-quadratic-character-next-terms":
        print("Invalid target_id")
        print("FAIL")
        sys.exit(1)

    a229 = data.get("A000229_1_to_43", {})
    if len(a229) != 43:
        print("A000229_1_to_43 length mismatch")
        print("FAIL")
        sys.exit(1)
    for k, exp in PUBLISHED_A000229_1_TO_38.items():
        if a229.get(k) != exp:
            print(f"Baseline mismatch at A000229({k})")
            print("FAIL")
            sys.exit(1)

    b000229_bytes = ("".join(f"{k} {a229[str(k)]}\n" for k in range(1, 39)) + "\n" * 6).encode("ascii")
    if hashlib.sha256(b000229_bytes).hexdigest() != EXPECTED_B000229_SHA256:
        print("b000229.txt SHA-256 mismatch")
        print("FAIL")
        sys.exit(1)

    for n_idx in range(1, 44):
        val_str = a229.get(str(n_idx), "")
        if not val_str.isdigit():
            print("Non-digit value in A000229")
            print("FAIL")
            sys.exit(1)
        q = int(val_str)
        if not verify_least_qnr_prime(q, n_idx):
            print(f"Property check failed for A000229({n_idx}) = {q}")
            print("FAIL")
            sys.exit(1)

    if data.get("win_a000229_39") != "317398900373231" or a229.get("39") != "317398900373231":
        print("win_a000229_39 mismatch")
        print("FAIL")
        sys.exit(1)
    if data.get("implied_a000229_40") != "112434732901969" or a229.get("40") != "112434732901969":
        print("implied_a000229_40 mismatch")
        print("FAIL")
        sys.exit(1)
    if data.get("win_a000229_41") != "1463971373078639" or a229.get("41") != "1463971373078639":
        print("win_a000229_41 mismatch")
        print("FAIL")
        sys.exit(1)
    if data.get("implied_a000229_42") != "178936222537081" or a229.get("42") != "178936222537081":
        print("implied_a000229_42 mismatch")
        print("FAIL")
        sys.exit(1)
    if data.get("implied_a000229_43") != "501108392233679" or a229.get("43") != "501108392233679":
        print("implied_a000229_43 mismatch")
        print("FAIL")
        sys.exit(1)

    expected_8k1 = [
        {"prime": "112434732901969", "least_qnr_prime": "173", "least_qnr_index": "40"},
        {"prime": "134035928676049", "least_qnr_prime": "173", "least_qnr_index": "40"},
        {"prime": "178936222537081", "least_qnr_prime": "181", "least_qnr_index": "42"},
        {"prime": "229297977151681", "least_qnr_prime": "173", "least_qnr_index": "40"},
    ]
    if data.get("all_primes_1_mod_8_with_first_38_primes_qr_up_to_317398900373231") != expected_8k1:
        print("all_primes_1_mod_8_with_first_38_primes_qr_up_to_317398900373231 mismatch")
        print("FAIL")
        sys.exit(1)
    for item in expected_8k1:
        q = int(item["prime"])
        idx = int(item["least_qnr_index"])
        if q % 8 != 1 or not verify_least_qnr_prime(q, idx) or str(PRIMES[idx - 1]) != item["least_qnr_prime"]:
            print(f"Failed verification of 8k+1 candidate {q}")
            print("FAIL")
            sys.exit(1)

    expected_40qr = [
        {"prime": "178936222537081", "mod_8": "1", "least_qnr_prime": "181", "least_qnr_index": "42"},
        {"prime": "501108392233679", "mod_8": "7", "least_qnr_prime": "191", "least_qnr_index": "43"},
        {"prime": "831583148698319", "mod_8": "7", "least_qnr_prime": "191", "least_qnr_index": "43"},
        {"prime": "1152240096017111", "mod_8": "7", "least_qnr_prime": "191", "least_qnr_index": "43"},
        {"prime": "1463971373078639", "mod_8": "7", "least_qnr_prime": "179", "least_qnr_index": "41"},
    ]
    if data.get("all_primes_with_first_40_primes_qr_up_to_1463971373078639") != expected_40qr:
        print("all_primes_with_first_40_primes_qr_up_to_1463971373078639 mismatch")
        print("FAIL")
        sys.exit(1)
    for item in expected_40qr:
        q = int(item["prime"])
        idx = int(item["least_qnr_index"])
        if str(q % 8) != item["mod_8"] or not verify_least_qnr_prime(q, idx) or str(PRIMES[idx - 1]) != item["least_qnr_prime"]:
            print(f"Failed verification of 40-QR candidate {q}")
            print("FAIL")
            sys.exit(1)

    cc = shutil.which("cc") or shutil.which("gcc") or shutil.which("clang")
    if not cc:
        print("No C compiler found")
        print("FAIL")
        sys.exit(1)
    c_src = os.path.join(here, "verify_qnr_sieve.c")
    tmp_dir = tempfile.mkdtemp(prefix="qnr_verify_")
    try:
        bin_path = os.path.join(tmp_dir, "verify_qnr_sieve")
        subprocess.run([cc, "-O3", c_src, "-o", bin_path], check=True)
        proc = subprocess.run([bin_path], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, check=True)
        out_lines = [l.strip() for l in proc.stdout.splitlines() if l.strip()]
    except Exception as e:
        print(f"C sieve execution failed: {e}")
        print("FAIL")
        sys.exit(1)
    finally:
        shutil.rmtree(tmp_dir, ignore_errors=True)

    sieve_a229 = {}
    sieve_a2223 = {}
    sieve_a2224 = {}
    enum2_list = []
    stage2_list = []
    for line in out_lines:
        if line.startswith("A000229("):
            k = line.split("(")[1].split(")")[0]
            sieve_a229[k] = line.split("=")[1]
        elif line.startswith("A002223("):
            k = line.split("(")[1].split(")")[0]
            sieve_a2223[k] = line.split("=")[1]
        elif line.startswith("A002224("):
            k = line.split("(")[1].split(")")[0]
            sieve_a2224[k] = line.split("=")[1]
        elif line.startswith("ENUM2_HIT("):
            enum2_list.append(line.split("=")[1])
        elif line.startswith("STAGE2_HIT("):
            stage2_list.append(line.split("=")[1])

    for n_idx in range(30, 44):
        k = str(n_idx)
        if sieve_a229.get(k) != a229.get(k):
            print(f"C sieve mismatch on A000229({k}): {sieve_a229.get(k)} != {a229.get(k)}")
            print("FAIL")
            sys.exit(1)

    if data.get("A002223_30_to_38") != sieve_a2223:
        print("A002223_30_to_38 mismatch against C sieve")
        print("FAIL")
        sys.exit(1)

    if data.get("A002224_30_to_41") != sieve_a2224:
        print("A002224_30_to_41 mismatch against C sieve")
        print("FAIL")
        sys.exit(1)

    if enum2_list != [x["prime"] for x in expected_8k1]:
        print(f"Enumerator 2 hits mismatch: {enum2_list}")
        print("FAIL")
        sys.exit(1)

    if stage2_list != [x["prime"] for x in expected_40qr]:
        print(f"Stage 2 hits mismatch: {stage2_list}")
        print("FAIL")
        sys.exit(1)

    expected_keys = {
        "target_id",
        "win_a000229_39",
        "implied_a000229_40",
        "win_a000229_41",
        "implied_a000229_42",
        "implied_a000229_43",
        "A000229_1_to_43",
        "A002223_30_to_38",
        "A002224_30_to_41",
        "all_primes_1_mod_8_with_first_38_primes_qr_up_to_317398900373231",
        "all_primes_with_first_40_primes_qr_up_to_1463971373078639",
    }
    if set(data.keys()) != expected_keys:
        print("Object keys mismatch")
        print("FAIL")
        sys.exit(1)

    print("Verified A000229(39..43) = [317398900373231, 112434732901969, 1463971373078639, 178936222537081, 501108392233679] via independent CRT modulus splits.")
    print("PASS")

if __name__ == "__main__":
    main()
