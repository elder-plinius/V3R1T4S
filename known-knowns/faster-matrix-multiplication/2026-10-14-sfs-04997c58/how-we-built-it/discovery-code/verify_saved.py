#!/usr/bin/env python3
"""Run symbolic and all-basis verification and corrupt-sign controls on artifacts."""
import argparse, copy, datetime, hashlib, json, os, resource, signal, sys, time
import synth
sys.path.insert(0,str(synth.ROOT/'tools'))
import basis_check

ap=argparse.ArgumentParser(); ap.add_argument('--tag',default='verification'); ap.add_argument('--seconds',type=int,default=240)
args=ap.parse_args(); start=time.monotonic()
resource.setrlimit(resource.RLIMIT_CPU,(args.seconds+1,args.seconds+2)); resource.setrlimit(resource.RLIMIT_NOFILE,(128,128))
signal.signal(signal.SIGALRM,lambda a,b:(_ for _ in ()).throw(TimeoutError('hard verification cap'))); signal.alarm(args.seconds)
out=synth.HERE/'output'; records=[]
(out/(args.tag+'_pid.json')).write_text(json.dumps({'pid':os.getpid(),'nice':os.getpriority(os.PRIO_PROCESS,0),'started_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'hard_seconds':args.seconds})+'\n')
try:
 for p in sorted((synth.HERE/'result').glob('*.json')):
    s=json.loads(p.read_text()); record={'file':p.name,'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'exact':synth.exact_check.verify(s),'basis':basis_check.check(s)}
    expanded=synth.exact_check.factors(s)
    record['maximum_expanded_factor_coefficients']={k:max(abs(c) for row in rows for c in row.values()) for k,rows in zip('uvw',expanded)}
    assert all(c==1 for c in record['maximum_expanded_factor_coefficients'].values())
    if p.name.startswith('best_'):
        original=synth.ROOT/'sources/schemes'/p.name[len('best_'):]
        record['factors_match_pinned_source']=synth.exact_check.factors(s)==synth.exact_check.factors(json.loads(original.read_text()))
        assert record['factors_match_pinned_source']
    elif s.get('research_parent_source'):
        parent_source=synth.ROOT/s['research_parent_source']
        record['factors_match_attributed_parent']=synth.exact_check.factors(s)==synth.exact_check.factors(json.loads(parent_source.read_text()))
        assert record['factors_match_attributed_parent']
    bad=copy.deepcopy(s)
    row=next(r for r in bad['w'] if r); row[0]['value']*=-1
    control={}
    for name,fn in [('exact',synth.exact_check.verify),('basis',basis_check.check)]:
        try: fn(bad)
        except Exception as e: control[name]={'rejected':True,'error':str(e)}
        else: control[name]={'rejected':False}
    record['corrupt_output_sign']=control; assert all(x['rejected'] for x in control.values())
    records.append(record); print(json.dumps(record),flush=True)
    (out/(args.tag+'_checkpoint.json')).write_text(json.dumps(records,indent=2)+'\n')
finally:
 signal.alarm(0)
 (out/(args.tag+'.json')).write_text(json.dumps({'records':records,'elapsed_seconds':time.monotonic()-start,'ended_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()},indent=2)+'\n')
 print(json.dumps({'event':'verification_finish','records':len(records),'elapsed_seconds':time.monotonic()-start}),flush=True)
