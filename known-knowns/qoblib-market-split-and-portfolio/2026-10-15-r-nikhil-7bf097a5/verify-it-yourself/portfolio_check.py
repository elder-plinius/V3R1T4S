"""Independent exact evaluation of QOBLIB bqp_u3_c10.zpl canonical schedules.

Written from the saved Zimpl model and public format definition, without
reading existing evaluator implementations. Standard library only; no search.
All decimals are exact rationals, with round-half-away-from-zero.
"""
from __future__ import annotations
import argparse
from collections import defaultdict
from dataclasses import dataclass
from fractions import Fraction as F
import gzip
import json
from pathlib import Path
import re


def require(condition, message):
    if not condition:
        raise ValueError(message)


def rnd(x):
    x = F(x)
    n, d = abs(x.numerator), x.denominator
    a = (2 * n + d) // (2 * d)
    return -a if x < 0 else a


def records(path):
    op = gzip.open if str(path).endswith('.gz') else open
    with op(path, 'rt', encoding='utf-8') as f:
        for line in f:
            row = line.split('#', 1)[0].split()
            if row:
                yield row


@dataclass
class Schedule:
    instance: str
    budget: int
    lam: F
    objective: int | None
    positions: dict


def read_schedule(path):
    head, pos = {}, {}
    for r in records(path):
        if len(r) == 2 and r[0] in ('instance', 'budget', 'lambda', 'objective'):
            require(r[0] not in head, 'duplicate header')
            head[r[0]] = r[1]
        else:
            require(len(r) == 4, 'malformed position/header')
            t, asset, long, short = int(r[0]), r[1], int(r[2]), int(r[3])
            require((t, asset) not in pos, 'duplicate position')
            require(0 <= long <= 3 and 0 <= short <= 3, 'count outside 0..3')
            pos[t, asset] = long, short
    require('budget' in head and 'lambda' in head, 'budget and lambda required')
    b, lam = int(head['budget']), F(head['lambda'])
    require(b >= 0 and lam >= 0, 'negative budget/risk weight')
    obj = F(head['objective']) if 'objective' in head else None
    require(obj is None or obj.denominator == 1, 'noninteger objective')
    return Schedule(head.get('instance', ''), b, lam,
                    None if obj is None else int(obj), pos)


def read_prices(path):
    raw = {}
    for r in records(path):
        require(len(r) == 3, 'malformed price row')
        t, a, p = int(r[0]), r[1], F(r[2])
        require((t, a) not in raw and p > 0, 'duplicate/nonpositive price')
        raw[t, a] = p
    require(raw, 'empty prices')
    times, assets = {t for t, _ in raw}, {a for _, a in raw}
    T = max(times) + 1
    require(T >= 2 and times == set(range(T)), 'noncontiguous/too few periods')
    require(len(raw) == T * len(assets), 'incomplete price rectangle')
    return {(t, a): p * 100000 / raw[0, a] for (t, a), p in raw.items()}, T, assets


def feasibility(s, T, assets):
    require(all(0 <= t < T and a in assets for t, a in s.positions),
            'unknown symbol or out-of-range period')
    rows = []
    for t in range(T):
        total = sum(l + h for (tt, a), (l, h) in s.positions.items() if tt == t)
        net = sum(l - h for (tt, a), (l, h) in s.positions.items() if tt == t)
        cash, slack = 10 - net, s.budget - total
        require(0 <= cash <= 15, f'capital constraint t={t}')
        require(0 <= slack <= 127, f'budget constraint t={t}')
        rows.append(dict(t=t, total=total, net=net, cash_slack=cash, budget_slack=slack))
    return rows


def required_covariance(s, T):
    active = defaultdict(list)
    for (t, a), (l, h) in s.positions.items():
        if l != h:
            active[t].append(a)
    return {(t, a, b) for t in range(T) for a in active[t] for b in active[t]}


def read_covariance(path, required, T, assets):
    # Stream the complete public file; keep only coefficients used by this
    # object. Irrelevant values have zero multiplier and need no rounding.
    cov = {}
    for r in records(path):
        require(len(r) == 4, 'malformed covariance row')
        t, a, b = int(r[0]), r[1], r[2]
        require(0 <= t < T and a in assets and b in assets, 'unknown covariance index')
        key = t, a, b
        if key in required:
            require(key not in cov, 'duplicate required covariance')
            cov[key] = F(r[3])
    require(set(cov) == required, 'missing required covariance')
    return cov


def evaluate(s, prices, T, assets, cov):
    rows = feasibility(s, T, assets)
    values = dict(risk=0, returns=0, transactions=0, cash_interest=0,
                  short_cost=0, liquidation=0)
    for t, a, b in required_covariance(s, T):
        la, ha = s.positions[t, a]
        lb, hb = s.positions[t, b]
        # Round is odd: sign-dependent rounded coefficients collapse exactly
        # to the product of net counts. Both ordered (a,b) and (b,a) occur.
        values['risk'] += rnd(s.lam * cov[t, a, b] * prices[t, a] * prices[t, b]) * (la-ha) * (lb-hb)
    for row in rows:
        c = row['cash_slack']
        values['cash_interest'] -= sum(rnd(F(1, 10000) * 100000 * (1 << k)) * ((c >> k) & 1) for k in range(4))
    for t in range(T):
        for a in assets:
            long, short = s.positions.get((t, a), (0, 0))
            price = prices[t, a]
            values['short_cost'] += rnd(F(1, 40000) * price) * short
            if t < T - 1:
                values['returns'] -= rnd(prices[t+1, a] - price) * (long-short)
            if t == 0:
                values['transactions'] += rnd(price / 1000) * (long+short)
            elif t < T - 1:
                old_l, old_h = s.positions.get((t-1, a), (0, 0))
                values['transactions'] += rnd(price / 1000) * (abs(long-old_l)+abs(short-old_h))
            else:
                values['liquidation'] += rnd(price / 1000) * (long+short)
    total = sum(values.values())
    require(s.objective is None or s.objective == total,
            f'claimed objective mismatch: claimed={s.objective} computed={total}')
    return dict(feasible=True, objective=total, components=values, periods=rows)


def check(prices_path, cov_path, solution_path, instance, budget, lam):
    s = read_schedule(solution_path)
    require(s.instance == instance, 'instance header mismatch')
    require(s.budget == budget and s.lam == F(lam), 'budget/lambda cell mismatch')
    prices, T, assets = read_prices(prices_path)
    key = re.fullmatch(r'po_a(\d+)_t(\d+)_(?:orig|s\d+)', instance)
    require(key is not None, 'unsupported instance key')
    require(len(assets) == int(key[1]) and T == int(key[2]), 'instance dimensions mismatch')
    feasibility(s, T, assets)
    cov = read_covariance(cov_path, required_covariance(s, T), T, assets)
    return evaluate(s, prices, T, assets, cov)


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('prices'); p.add_argument('covariance'); p.add_argument('solution')
    p.add_argument('--instance', required=True)
    p.add_argument('--budget', required=True, type=int)
    p.add_argument('--lam', required=True)
    a = p.parse_args()
    try:
        result = check(a.prices, a.covariance, a.solution, a.instance, a.budget, a.lam)
        print(json.dumps(result, sort_keys=True, indent=2))
        print('PORTFOLIO_CHECK: PASS')
    except (ValueError, KeyError, OSError, EOFError) as e:
        print('PORTFOLIO_CHECK: FAIL:', e)
        raise SystemExit(1)
