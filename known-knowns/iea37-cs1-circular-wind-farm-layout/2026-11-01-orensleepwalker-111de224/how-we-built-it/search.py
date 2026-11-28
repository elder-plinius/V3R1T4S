"""Bounded, resumable CS1 search from fresh coordinates, using the published model.

Physics: Baker, Stanley, Thomas et al., IEA37 case study 1. Optimization:
SciPy SLSQP with independently derived analytic objective/constraint gradients.
No published layout is used as a starting point.
"""
import argparse
from datetime import datetime, timezone
import hashlib
import json
import math
import os
from pathlib import Path
import time

import numpy as np
import scipy
from scipy.optimize import minimize

N = 16
R = 1300.0
MARGIN = 0.0001
MIN_DISTANCE = 260.0
FREQ = np.array([.025, .024, .029, .036, .063, .065, .100, .122,
                 .063, .038, .039, .083, .213, .046, .032, .022])
ANGLES = np.deg2rad(np.arange(16) * 22.5 - 270)
C = np.cos(ANGLES)[:, None, None]
S = np.sin(ANGLES)[:, None, None]
PAIRS = np.triu_indices(N, 1)
SCALE = N * 3.35 * 8760


def objective(z):
    points = np.asarray(z).reshape(N, 2) * R
    delta = points[:, None, :] - points[None, :, :]
    dx = C * delta[None, :, :, 0] - S * delta[None, :, :, 1]
    dy = S * delta[None, :, :, 0] + C * delta[None, :, :, 1]
    upstream = dx > 0
    width = .0324555 * np.maximum(dx, 0) + 130 / np.sqrt(8)
    radical = np.sqrt(1 - (8 / 9) * 130**2 / (8 * width**2))
    amplitude = 1 - radical
    exponential = np.exp(-.5 * (dy / width)**2)
    deficit = np.where(upstream, amplitude * exponential, 0)
    loss = np.sqrt(np.sum(deficit**2, axis=2))
    speed = 9.8 * (1 - loss)
    ramp = (speed >= 4) & (speed < 9.8)
    rated = (speed >= 9.8) & (speed < 25)
    power = np.where(ramp, 3.35 * ((speed - 4) / 5.8)**3,
                     np.where(rated, 3.35, 0))
    value = float(8760 * np.sum(FREQ[:, None] * power))

    amp_derivative = -(8 / 9) * 130**2 / (8 * width**3 * radical)
    ddef_dx = np.where(upstream, .0324555 * exponential *
                       (amp_derivative + amplitude * dy**2 / width**3), 0)
    ddef_dy = np.where(upstream, -deficit * dy / width**2, 0)
    denergy_dloss = np.where(ramp,
                            -3 * 3.35 * 9.8 * (speed - 4)**2 / 5.8**3,
                            0) * 8760 * FREQ[:, None]
    ratio = np.divide(deficit, loss[:, :, None],
                      out=np.zeros_like(deficit), where=loss[:, :, None] > 0)
    weight = denergy_dloss[:, :, None] * ratio
    gx = weight * (C * ddef_dx + S * ddef_dy)
    gy = weight * (-S * ddef_dx + C * ddef_dy)
    gradient = np.stack([np.sum(gx, axis=(0, 2)) - np.sum(gx, axis=(0, 1)),
                         np.sum(gy, axis=(0, 2)) - np.sum(gy, axis=(0, 1))], axis=1)
    return -value / SCALE, -gradient.ravel() * R / SCALE


def constraints(z):
    p = np.asarray(z).reshape(N, 2)
    separation = p[PAIRS[0]] - p[PAIRS[1]]
    return np.r_[((R - MARGIN) / R)**2 - np.sum(p*p, axis=1),
                 np.sum(separation*separation, axis=1) -
                 ((MIN_DISTANCE + MARGIN) / R)**2]


def constraint_jac(z):
    p = np.asarray(z).reshape(N, 2)
    jac = np.zeros((N + len(PAIRS[0]), N, 2))
    jac[np.arange(N), np.arange(N)] = -2 * p
    delta = 2 * (p[PAIRS[0]] - p[PAIRS[1]])
    rows = N + np.arange(len(PAIRS[0]))
    jac[rows, PAIRS[0]] = delta
    jac[rows, PAIRS[1]] = -delta
    return jac.reshape(len(jac), 2*N)


def geometry(z):
    p = np.asarray(z).reshape(N, 2) * R
    radius = max(math.sqrt(float(x*x+y*y)) for x, y in p)
    distance = min(math.sqrt(float(np.sum((p[i]-p[j])**2)))
                   for i, j in zip(*PAIRS))
    return {"max_radius_m": radius, "min_spacing_m": distance,
            "strictly_feasible": radius <= R and distance >= MIN_DISTANCE}


def fresh_start(rng, kind):
    if kind < 8:
        outer = [10, 11, 12, 13, 14, 15, 16, 12][kind]
        angles = np.arange(outer) * 2*np.pi/outer + rng.uniform(0, 2*np.pi)
        angles += rng.normal(0, .025, outer)
        radial = np.full(outer, (R - .01) / R)
        if kind == 7:
            radial -= rng.uniform(0, .1, outer)
        points = list(zip(radial*np.cos(angles), radial*np.sin(angles)))
    else:
        points = []
    tries = 0
    while len(points) < N:
        tries += 1
        if tries > 10000:
            return fresh_start(rng, 8)
        radius = math.sqrt(rng.uniform(0, .99**2))
        angle = rng.uniform(0, 2*np.pi)
        candidate = (radius*math.cos(angle), radius*math.sin(angle))
        if all(math.dist(candidate, x) > (MIN_DISTANCE+.01)/R for x in points):
            points.append(candidate)
    return np.array(points).ravel()


def write_json(path, data):
    temporary = path.with_suffix(path.suffix + ".new")
    temporary.write_text(json.dumps(data, indent=2, allow_nan=False) + "\n")
    temporary.replace(path)


def run(args):
    out = Path(args.output)
    out.mkdir(parents=True, exist_ok=True)
    write_json(out / "process.json", {"pid": os.getpid(), "deadline": args.deadline,
                                     "utc": datetime.now(timezone.utc).isoformat()})
    rng = np.random.default_rng(args.seed)
    checkpoint_path = out / "checkpoint.json"
    best = None
    iteration = 0
    resumed = False
    if checkpoint_path.exists():
        state = json.loads(checkpoint_path.read_text())
        best, iteration = state["best"], state["restarts"]
        rng.bit_generator.state = state["rng_state"]
        resumed = True
    print(json.dumps({"event": "start", "utc": datetime.now(timezone.utc).isoformat(),
                      "pid": os.getpid(), "numpy": np.__version__, "scipy": scipy.__version__,
                      "seed": args.seed, "deadline": args.deadline,
                      "resumed": resumed}), flush=True)
    deadline = datetime.fromisoformat(args.deadline).timestamp()
    started = time.monotonic()
    last_save = 0.0
    while time.time() < deadline and iteration < args.max_restarts:
        kind = iteration % 10
        start = fresh_start(rng, kind)
        # Unpublished own results may be perturbed; published coordinates are never loaded.
        if best and kind == 9:
            start = np.array(best["coordinates_m"]).ravel()/R + rng.normal(0, .035, N*2)
        result = minimize(objective, start, jac=True, method="SLSQP",
                          constraints={"type": "ineq", "fun": constraints,
                                       "jac": constraint_jac},
                          options={"maxiter": args.maxiter, "ftol": 1e-11})
        iteration += 1
        g = geometry(result.x)
        energy = -objective(result.x)[0] * SCALE
        if g["strictly_feasible"] and (not best or energy > best["aep_MWh"]):
            best = {"aep_MWh": energy, "coordinates_m": (result.x.reshape(N, 2)*R).tolist(),
                    "geometry": g, "restart": iteration, "kind": kind,
                    "solver_success": bool(result.success), "iterations": int(result.nit),
                    "utc": datetime.now(timezone.utc).isoformat(), "seed": args.seed}
            write_json(out/"best.json", best)
            print(json.dumps({"event": "best", **{k:v for k,v in best.items()
                                                     if k != "coordinates_m"}}), flush=True)
        if time.monotonic()-last_save > 30 or iteration == args.max_restarts:
            state = {"restarts": iteration, "best": best,
                     "rng_state": rng.bit_generator.state,
                     "utc": datetime.now(timezone.utc).isoformat(),
                     "elapsed_seconds_this_process": time.monotonic()-started,
                     "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
            write_json(checkpoint_path, state)
            print(json.dumps({"event": "checkpoint", "restarts": iteration,
                              "best_MWh": best["aep_MWh"] if best else None,
                              "utc": state["utc"]}), flush=True)
            last_save = time.monotonic()
    print(json.dumps({"event": "complete", "utc": datetime.now(timezone.utc).isoformat(),
                      "restarts": iteration, "best_MWh": best["aep_MWh"] if best else None}), flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    parser.add_argument("--deadline", required=True)
    parser.add_argument("--seed", type=int, default=20261031)
    parser.add_argument("--max-restarts", type=int, default=1000000)
    parser.add_argument("--maxiter", type=int, default=350)
    run(parser.parse_args())
