# Parser test for the repaired claim/code/prove.py (appended after prove.py + RULES_JSON, like main_proofs.py).
ok = True
t = parse_pattern("A0 1^(2k-1) 00", k, 0)
print("1^(2k-1) ->", t[2][2]); ok &= sp.expand(t[2][2] - (2*k - 1)) == 0
t = parse_pattern("A0 1^(2k-1) 00", sp.Integer(3), 0); print("k=3 ->", t[2][2]); ok &= t[2][2] == 5
for bad in ["A0 1^(2j-1) 00", "A0 1^(2j) 00", "A0 1^j 00"]:
    try:
        parse_pattern(bad, k, 0); print("NOT REJECTED", bad); ok = False
    except ValueError as e:
        print("rejected:", e)
for bad in ["2j+1", "12j^2"]:
    try:
        steps_sym(bad); print("NOT REJECTED steps", bad); ok = False
    except ValueError as e:
        print("rejected steps:", e)
print("steps 12k^2+13k ->", steps_sym("12k^2+13k"))
print("parser test pass:", ok)
