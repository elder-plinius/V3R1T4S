# driver appended after prove.py and RULES_JSON
import copy, hashlib
DATA = json.loads(RULES_JSON)
print("rules.json sha256 (of embedded text):", hashlib.sha256(RULES_JSON.encode()).hexdigest())
assert DATA["machine"] == MACHINE
RULES = DATA["rules"]
proved = run_all(RULES, PROOFS, "REAL RULES")
print("SUMMARY REAL:", proved)
