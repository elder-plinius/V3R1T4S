#!/usr/bin/env python3
"""Standalone checker for the claim: 41-instruction Brainfuck program for 114514.

Semantics from the page's conventions for n > 255: unbounded right tape, cells hold
arbitrary-precision integers (no wrapping), pointer starts at cell 0 and may never move
left of it, at halt the cell under the pointer must hold the target exactly.

Usage: python3 checker.py object/program.bf 114514
Exit 0 and last line PASS on success; exit 1 and FAIL otherwise.
"""
import sys

def check(prog, target, limit=10_000_000):
    tape = [0] * 64
    ptr = 0
    pc = 0
    steps = 0
    mincell = 0
    stack = []
    jump = {}
    for i, ch in enumerate(prog):
        if ch == '[':
            stack.append(i)
        elif ch == ']':
            if not stack:
                return ('FAIL', 'unbalanced ]', steps)
            j = stack.pop()
            jump[i] = j
            jump[j] = i
    if stack:
        return ('FAIL', 'unbalanced [', steps)
    n = len(prog)
    while pc < n:
        if steps >= limit:
            return ('FAIL', 'step limit', steps)
        steps += 1
        ch = prog[pc]
        if ch == '+':
            tape[ptr] += 1
        elif ch == '-':
            tape[ptr] -= 1
        elif ch == '>':
            ptr += 1
            if ptr == len(tape):
                tape.append(0)
        elif ch == '<':
            ptr -= 1
            if ptr < 0:
                return ('FAIL', 'left of origin', steps)
        elif ch == '[':
            if tape[ptr] == 0:
                pc = jump[pc]
        elif ch == ']':
            if tape[ptr] != 0:
                pc = jump[pc]
        elif ch in '.,':
            pass
        else:
            return ('FAIL', 'bad character %r' % ch, steps)
        if tape[ptr] < mincell:
            mincell = tape[ptr]
        pc += 1
    val = tape[ptr]
    if val != target:
        return ('FAIL', 'value %d != %d' % (val, target), steps)
    if mincell < 0:
        return ('FAIL', 'negative cell reached: %d' % mincell, steps)
    return ('PASS', 'len=%d value=%d steps=%d mincell=%d' % (len(prog), val, steps, mincell), steps)

def main():
    if len(sys.argv) != 3:
        print('usage: python3 checker.py <program-file> <target>')
        return 2
    prog = open(sys.argv[1], encoding='utf-8').read().rstrip('\r\n')
    target = int(sys.argv[2])
    status, detail, _ = check(prog, target)
    print('%s %s' % (status, detail))
    return 0 if status == 'PASS' else 1

if __name__ == '__main__':
    sys.exit(main())
