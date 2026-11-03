"""Targeted proposals using only this run's unpublished own 36-point best."""
import argparse
from datetime import datetime,timezone
import hashlib
import json
from pathlib import Path
import numpy as np
from search36 import engine

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',required=True)
    p.add_argument('--own-seed',required=True);p.add_argument('--deadline',required=True)
    p.add_argument('--seed',type=int,default=20261138)
    p.add_argument('--max-restarts',type=int,default=1000000);p.add_argument('--maxiter',type=int,default=350)
    args=p.parse_args();out=Path(args.output);out.mkdir(parents=True,exist_ok=True)
    seed=Path(args.own_seed);original=json.loads(seed.read_text())
    engine.write_json(out/'starting-own-best.json',original)
    engine.write_json(out/'provenance.json',{'own_seed_sha256':hashlib.sha256(seed.read_bytes()).hexdigest(),
                      'source':'Own current-run fresh ring/continuation output; no published coordinates',
                      'utc':datetime.now(timezone.utc).isoformat()})
    fresh=engine.fresh_start
    def proposals(rng,kind):
        if kind==8:return fresh(rng,8)
        current=json.loads((out/'best.json').read_text()) if (out/'best.json').exists() else original
        points=np.array(current['coordinates_m'])/engine.R
        if kind<6:
            for index in rng.choice(36,size=[1,1,2,2,3,4][kind],replace=False):
                angle=rng.uniform(0,2*np.pi);radius=np.sqrt(rng.uniform(0,.999**2))
                points[index]=radius*np.array([np.cos(angle),np.sin(angle)])
        elif kind==6:
            a=rng.normal(0,.12);co,si=np.cos(a),np.sin(a)
            points=points @ np.array([[co,si],[-si,co]])
        else:points+=rng.normal(0,.07,points.shape)
        return points.ravel()
    engine.fresh_start=proposals
    engine.run(args)
