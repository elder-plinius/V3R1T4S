"""Fresh concentric starts and continuation, always ending with exact CS1."""
import argparse
import math
import numpy as np
from search36 import engine

PATTERNS=[(16,12,8),(20,12,4),(24,8,4),(28,8,0),(12,16,8),
          (18,12,6),(22,10,4),(14,14,8),(36,0,0)]
original_start=engine.fresh_start


def fresh_rings(rng,kind):
    if kind==9:return original_start(rng,8)
    points=[]
    for count,radius in zip(PATTERNS[kind],[.999995,.64,.29]):
        if count==0:continue
        theta=rng.uniform(0,2*math.pi)+np.arange(count)*2*math.pi/count
        theta+=rng.normal(0,.015,count)
        r=radius if radius>.99 else radius+rng.uniform(-.025,.025)
        points.extend(zip(r*np.cos(theta),r*np.sin(theta)))
    return np.asarray(points).ravel()


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',required=True)
    p.add_argument('--deadline',required=True);p.add_argument('--seed',type=int,default=20261137)
    p.add_argument('--max-restarts',type=int,default=1000000)
    p.add_argument('--maxiter',type=int,default=350)
    args=p.parse_args()
    engine.fresh_start=fresh_rings
    original_minimize=engine.minimize
    def continuation(fun,x0,**kwargs):
        x=x0
        for scale in [3,2,1.5,1]:
            def aux(z):
                f,g=fun(z/scale)
                return f,g/scale
            result=original_minimize(aux,x,**kwargs);x=result.x
        return result
    engine.minimize=continuation
    engine.run(args)
