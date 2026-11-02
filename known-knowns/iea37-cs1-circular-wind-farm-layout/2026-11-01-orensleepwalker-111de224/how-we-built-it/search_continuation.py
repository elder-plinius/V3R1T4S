"""Spatial-compression continuation, always finishing with the exact CS1 model.

The auxiliary objective evaluates spatially compressed coordinates, while constraints
remain on the actual coordinates. This is an exploratory continuation heuristic,
not a claim to implement the published SNOPT+WEC method. Only the final factor-one
objective is scored or exported as a possible physical layout.
"""
import argparse
from datetime import datetime, timezone
import hashlib
from pathlib import Path

import search as engine


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--output", required=True)
    p.add_argument("--deadline", required=True)
    p.add_argument("--seed", type=int, default=20261102)
    p.add_argument("--max-restarts", type=int, default=1000000)
    p.add_argument("--maxiter", type=int, default=350)
    args = p.parse_args()
    output = Path(args.output)
    output.mkdir(parents=True, exist_ok=True)
    engine.write_json(output/"method.json", {
        "utc": datetime.now(timezone.utc).isoformat(),
        "spatial_compression_factors": [3, 2, 1.5, 1],
        "wrapper_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "scope": "Final scores use unmodified factor-one physics; intermediate energies are not claims."})
    original_minimize = engine.minimize

    def continuation(fun, x0, **kwargs):
        points = x0
        for scale in [3, 2, 1.5, 1]:
            def auxiliary(z):
                value, gradient = fun(z/scale)
                return value, gradient/scale
            result = original_minimize(auxiliary, points, **kwargs)
            points = result.x
        return result

    engine.minimize = continuation
    engine.run(args)
