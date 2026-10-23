#!/usr/bin/env python3
"""External wall-time watchdog; signals only its exact recorded child PID."""
import argparse,datetime,json,os,pathlib,subprocess,sys,time
ap=argparse.ArgumentParser();ap.add_argument('--seconds',type=int,required=True);ap.add_argument('--tag',required=True);ap.add_argument('command',nargs=argparse.REMAINDER);args=ap.parse_args()
here=pathlib.Path(__file__).resolve().parents[1];out=here/'output';segment=json.loads((here.parents[1]/'data/segment.json').read_text())
cutoff=datetime.datetime.fromisoformat(segment['line_start_cutoff_utc']);now=datetime.datetime.now(datetime.timezone.utc);seconds=min(args.seconds,max(1,int((cutoff-now).total_seconds())-10))
command=args.command[1:] if args.command and args.command[0]=='--' else args.command
assert command and command[0]=='python3'
start=time.monotonic();child=subprocess.Popen(command)
record={'supervisor_pid':os.getpid(),'child_pid':child.pid,'nice':os.getpriority(os.PRIO_PROCESS,0),'started_utc':now.isoformat(),'hard_wall_seconds':seconds,'command':command}
path=out/(args.tag+'_watchdog.json');path.write_text(json.dumps(record,indent=2)+'\n');print(json.dumps({'event':'watchdog_start',**record}),flush=True)
try:
 code=child.wait(timeout=seconds);record['terminated_by_watchdog']=False
except subprocess.TimeoutExpired:
 child.terminate();record['terminated_by_watchdog']=True;record['signal']='SIGTERM'
 try:code=child.wait(timeout=2)
 except subprocess.TimeoutExpired:child.kill();record['signal']='SIGKILL';code=child.wait(timeout=2)
record.update({'child_exit_code':code,'elapsed_wall_seconds':time.monotonic()-start,'ended_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()});path.write_text(json.dumps(record,indent=2)+'\n');print(json.dumps({'event':'watchdog_finish',**record}),flush=True)
sys.exit(0 if code==0 or record['terminated_by_watchdog'] else 1)
