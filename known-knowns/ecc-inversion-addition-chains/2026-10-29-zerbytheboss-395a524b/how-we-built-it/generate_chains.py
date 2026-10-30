#!/usr/bin/env python3
import os
import re

class ChainBuilder:
    def __init__(self):
        self.ops = [] # list of ('dbl', j) or ('add', j, k)
        self.vals = [1]
        self.named_vars = {'1': 0}

    def dbl(self, j):
        val = self.vals[j] * 2
        self.ops.append(('dbl', j))
        self.vals.append(val)
        return len(self.vals) - 1

    def add(self, j, k):
        val = self.vals[j] + self.vals[k]
        self.ops.append(('add', j, k))
        self.vals.append(val)
        return len(self.vals) - 1

    def shift_add(self, r_high, shift, r_low):
        cur = r_high
        for _ in range(shift):
            cur = self.dbl(cur)
        return self.add(cur, r_low)

    def shift(self, r, s):
        cur = r
        for _ in range(s):
            cur = self.dbl(cur)
        return cur

def tokenize(text):
    tokens = []
    i = 0
    while i < len(text):
        if text[i].isspace():
            i += 1
        elif text[i] in '()+*=':
            tokens.append(text[i])
            i += 1
        elif text[i:i+2] == '<<':
            tokens.append('<<')
            i += 2
        else:
            start = i
            while i < len(text) and (text[i].isalnum() or text[i] == '_'):
                i += 1
            tokens.append(text[start:i])
    return tokens

class Parser:
    def __init__(self, builder):
        self.b = builder

    def parse_expr(self, tokens):
        val = self.parse_term(tokens)
        while tokens and tokens[0] == '+':
            tokens.pop(0)
            right = self.parse_term(tokens)
            val = self.b.add(val, right)
        return val

    def parse_term(self, tokens):
        if tokens and tokens[0] == '2' and len(tokens) > 1 and tokens[1] == '*':
            tokens.pop(0)
            tokens.pop(0)
            val = self.b.dbl(self.parse_factor(tokens))
        else:
            val = self.parse_factor(tokens)
            
        while tokens and tokens[0] in ('<<', '*'):
            op = tokens.pop(0)
            if op == '<<':
                s = int(tokens.pop(0))
                val = self.b.shift(val, s)
            elif op == '*':
                num = int(tokens.pop(0))
                assert num == 2
                val = self.b.dbl(val)
        return val

    def parse_factor(self, tokens):
        tok = tokens.pop(0)
        if tok == '(':
            val = self.parse_expr(tokens)
            assert tokens.pop(0) == ')'
            return val
        elif tok == '1':
            return 0
        else:
            return self.b.named_vars[tok]

    def parse_line(self, line):
        tokens = tokenize(line)
        if not tokens: return None
        if tokens[0] == 'return':
            tokens.pop(0)
            return self.parse_expr(tokens)
        else:
            var_name = tokens.pop(0)
            assert tokens.pop(0) == '='
            val = self.parse_expr(tokens)
            self.b.named_vars[var_name] = val
            return None

def build_from_lines(lines):
    b = ChainBuilder()
    p = Parser(b)
    ret = None
    for l in lines:
        res = p.parse_line(l)
        if res is not None: ret = res
    return b

def build_djb_curve25519():
    b = ChainBuilder()
    _1 = 0
    _10 = b.dbl(_1)
    _1001 = b.shift_add(_10, 2, _1)
    _1011 = b.add(_1001, _10)
    x5 = b.shift_add(_1011, 1, _1001)
    x10 = b.shift_add(x5, 5, x5)
    x20 = b.shift_add(x10, 10, x10)
    x40 = b.shift_add(x20, 20, x20)
    x50 = b.shift_add(x40, 10, x10)
    x100 = b.shift_add(x50, 50, x50)
    t1 = b.shift_add(x100, 100, x100)
    t2 = b.shift_add(t1, 50, x50)
    b.shift_add(t2, 5, _1011)
    return b

def build_briansmith_p384():
    b = ChainBuilder()
    x1 = 0
    x2 = b.shift_add(x1, 1, x1)
    x3 = b.shift_add(x2, 1, x1)
    x6 = b.shift_add(x3, 3, x3)
    x12 = b.shift_add(x6, 6, x6)
    x15 = b.shift_add(x12, 3, x3)
    x30 = b.shift_add(x15, 15, x15)
    x60 = b.shift_add(x30, 30, x30)
    x120 = b.shift_add(x60, 60, x60)
    cur = b.shift_add(x120, 120, x120)
    cur = b.shift_add(cur, 15, x15)
    cur = b.shift_add(cur, 31, x30)
    cur = b.shift_add(cur, 2, x2)
    cur = b.shift_add(cur, 94, x30)
    b.shift(cur, 2)
    return b

def build_our_m383():
    b = ChainBuilder()
    R = {}
    R[1] = 0
    R[2] = b.shift_add(R[1], 1, R[1])
    R[4] = b.shift_add(R[2], 2, R[2])
    R[8] = b.shift_add(R[4], 4, R[4])
    R[16] = b.shift_add(R[8], 8, R[8])
    R[24] = b.shift_add(R[16], 8, R[8])
    R[25] = b.shift_add(R[24], 1, R[1])
    R[50] = b.shift_add(R[25], 25, R[25])
    R[100] = b.shift_add(R[50], 50, R[50])
    R[125] = b.shift_add(R[100], 25, R[25])
    R[250] = b.shift_add(R[125], 125, R[125])
    R[375] = b.shift_add(R[250], 125, R[125])
    t1 = b.shift_add(R[375], 2, R[1])
    b.shift_add(t1, 6, R[2])
    return b

def build_our_m511():
    b = ChainBuilder()
    R = {}
    R[1] = 0
    R[2] = b.shift_add(R[1], 1, R[1])
    R[4] = b.shift_add(R[2], 2, R[2])
    R[8] = b.shift_add(R[4], 4, R[4])
    R[16] = b.shift_add(R[8], 8, R[8])
    R[32] = b.shift_add(R[16], 16, R[16])
    R[64] = b.shift_add(R[32], 32, R[32])
    R[96] = b.shift_add(R[64], 32, R[32])
    R[100] = b.shift_add(R[96], 4, R[4])
    R[101] = b.shift_add(R[100], 1, R[1])
    R[201] = b.shift_add(R[101], 100, R[100])
    R[402] = b.shift_add(R[201], 201, R[201])
    R[503] = b.shift_add(R[402], 101, R[101])
    t1 = b.shift_add(R[503], 2, R[1])
    b.shift_add(t1, 6, R[2])
    return b

def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    md_path = os.path.join(base_dir, '..', '..', 'data', 'addchain_results.md')
    with open(md_path) as f:
        lines = f.readlines()

    in_go = False
    cur_curve = ''
    curves = {}
    for line in lines:
        if line.startswith('## '):
            cur_curve = line[3:].strip()
            curves[cur_curve] = []
        elif line.startswith('```go'):
            in_go = True
        elif line.startswith('```') and in_go:
            in_go = False
        elif in_go:
            l = line.strip()
            if l: curves[cur_curve].append(l)

    # Name mapping between targets.rs and addchain_results.md:
    name_map = {
        'Curve25519 Field': 'DJB_SPECIAL',
        'NIST P-256 Field': 'NIST P-256 Field Inversion',
        'NIST P-384 Field': 'BRIAN_SMITH_SPECIAL',
        'secp256k1 Field': 'secp256k1 (Bitcoin) Field Inversion',
        'Curve25519 Scalar': 'Curve25519 Scalar Inversion',
        'NIST P-256 Scalar': 'NIST P-256 Scalar Inversion',
        'NIST P-384 Scalar': 'NIST P-384 Scalar Inversion',
        'secp256k1 Scalar': 'secp256k1 (Bitcoin) Scalar Inversion',
        'M-221': 'M-221 Field Inversion',
        'E-222': 'E-222 Field Inversion',
        'Curve1174': 'Curve1174 Field Inversion',
        'E-382': 'E-382 Field Inversion',
        'M-383': 'OUR_M383_SPECIAL',
        'Curve41417': 'Curve41417 Field Inversion',
        'M-511': 'OUR_M511_SPECIAL',
        'NIST P-192': 'NIST P-192 Field Inversion',
        'NIST P-224': 'NIST P-224 Field Inversion',
        'Goldilocks': 'Goldilocks Field Inversion',
        'secp192k1': 'secp192k1 Field Inversion',
        'secp224k1': 'secp224k1 Field Inversion',
    }

    out_file = os.path.join(base_dir, 'src', 'chains_data.rs')
    with open(out_file, 'w') as f:
        f.write('// Autogenerated addition chains for all 20 elliptic curve targets.\n')
        f.write('use crate::chain::{AdditionChain, Op};\n\n')
        
        for tgt_name, src_key in name_map.items():
            fn_name = 'build_' + re.sub(r'[^a-zA-Z0-9]', '_', tgt_name).lower()
            if src_key == 'DJB_SPECIAL':
                b = build_djb_curve25519()
            elif src_key == 'BRIAN_SMITH_SPECIAL':
                b = build_briansmith_p384()
            elif src_key == 'OUR_M383_SPECIAL':
                b = build_our_m383()
            elif src_key == 'OUR_M511_SPECIAL':
                b = build_our_m511()
            else:
                b = build_from_lines(curves[src_key])
                
            print(f"Target {tgt_name:20s}: {len(b.ops):3d} ops")
            
            f.write(f'pub fn {fn_name}() -> AdditionChain {{\n')
            f.write('    AdditionChain {\n')
            f.write('        ops: vec![\n')
            for op, *args in b.ops:
                if op == 'dbl':
                    f.write(f'            Op::Double({args[0]}),\n')
                else:
                    f.write(f'            Op::Add({args[0]}, {args[1]}),\n')
            f.write('        ],\n')
            f.write('    }\n')
            f.write('}\n\n')
            
        f.write('pub fn get_chain_by_name(name: &str) -> Option<AdditionChain> {\n')
        f.write('    match name {\n')
        for tgt_name in name_map.keys():
            fn_name = 'build_' + re.sub(r'[^a-zA-Z0-9]', '_', tgt_name).lower()
            f.write(f'        "{tgt_name}" => Some({fn_name}()),\n')
        f.write('        _ => None,\n')
        f.write('    }\n')
        f.write('}\n')

    print(f"Wrote {out_file} successfully!")

if __name__ == '__main__':
    main()
