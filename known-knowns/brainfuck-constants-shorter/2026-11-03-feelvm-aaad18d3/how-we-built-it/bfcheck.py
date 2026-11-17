#!/usr/bin/env python3
"""Reference Brainfuck checker for the esolangs 'Brainfuck constants' table.

Semantics (from the page's stated conventions):
  * tape starts at cell 0, all cells zero, unbounded to the right
  * cells are 8-bit and wrap (mod 256) if wrap=True; otherwise arbitrary integers
  * the program must never move left of cell 0
  * at halt, the cell under the pointer holds the constant
  * loops skip when the current cell is 0
Output: ('OK', value) or ('ERR:<why>', None)
"""
import sys

def run(prog, wrap=True, limit=10_000_000, check_left=True):
    tape = [0] * 64          # grow on demand to the right
    ptr = 0
    pc = 0
    steps = 0
    # precompute bracket matches
    stack, match = [], {}
    for i, ch in enumerate(prog):
        if ch == '[':
            stack.append(i)
        elif ch == ']':
            if not stack:
                return ('ERR:unbalanced ]', None)
            j = stack.pop()
            match[i] = j
            match[j] = i
    if stack:
        return ('ERR:unbalanced [', None)
    n = len(prog)
    while pc < n:
        steps += 1
        if steps > limit:
            return ('ERR:step limit', None)
        ch = prog[pc]
        if ch == '+':
            tape[ptr] += 1
            if wrap:
                tape[ptr] &= 255
        elif ch == '-':
            tape[ptr] -= 1
            if wrap:
                tape[ptr] &= 255
        elif ch == '>':
            ptr += 1
            if ptr == len(tape):
                tape.append(0)
        elif ch == '<':
            ptr -= 1
            if ptr < 0:
                if check_left:
                    return ('ERR:left of origin', None)
                return ('ERR:left of origin', None)
        elif ch == '[':
            if tape[ptr] == 0:
                pc = match[pc]
        elif ch == ']':
            if tape[ptr] != 0:
                pc = match[pc]
        elif ch == '.':
            pass
        elif ch == ',':
            tape[ptr] = 0
        else:
            return ('ERR:bad char %r' % ch, None)
        pc += 1
    return ('OK', tape[ptr])

def check(prog, n, wrap):
    # never left of origin is impossible to observe after the fact, so re-run intrusive:
    st, val = run(prog, wrap=wrap)
    if st != 'OK':
        return st, val
    return ('OK' if val == n else 'ERR:value %d != %d' % (val, n)), val

if __name__ == '__main__':
    if len(sys.argv) >= 4:
        prog, n, mode = sys.argv[1], int(sys.argv[2]), sys.argv[3]
        st, val = check(prog, n, wrap=(mode == 'wrap'))
        print(st, val, len(prog))
