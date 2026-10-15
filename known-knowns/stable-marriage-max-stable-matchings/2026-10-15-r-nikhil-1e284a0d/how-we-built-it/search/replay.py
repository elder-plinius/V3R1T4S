from pathlib import Path
import tempfile,subprocess,shutil,os,json,sys
S=Path(__file__).resolve().parent;C=S.parent;K=C/'calibration'
def run(cmd,**kw):
 p=subprocess.run(cmd,text=True,capture_output=True,**kw)
 if p.returncode:raise RuntimeError(p.stdout+p.stderr)
 return p.stdout
with tempfile.TemporaryDirectory(prefix='discovery-replay-') as td:
 T=Path(td); cc=shutil.which('clang') or shutil.which('cc')
 for f in ['word_repair.c','word_ideals.h','smcount3_copy.c','square_trade.inc']:shutil.copyfile(S/f,T/f)
 print(run([cc,'-O3','-std=c11',str(T/'word_repair.c'),'-lm','-o',str(T/'search')]),end='')
 for phase in json.loads((S/'replay_plan.json').read_text()):
  out=T/phase['book'];env=dict(os.environ,WORD_TEMP=phase['temp'],WORD_SQUARE='30',MAX_PROPOSALS=str(phase['cutoff']))
  txt=run([str(T/'search'),str(S/phase['input']),str(out),'3600',str(phase['seed'])],env=env,timeout=900)
  print(txt,end='')
  for ext in ['prefs','word']:
   assert Path(str(out)+'.best.'+ext).read_bytes()==(S/(phase['book']+'.expected.'+ext)).read_bytes(),phase
  print('phase exact',phase['book'],phase['count'],phase['cutoff'])
 last=json.loads((S/'replay_plan.json').read_text())[-1]
 assert (S/(last['book']+'.expected.word')).read_bytes()==(C/'construction.word').read_bytes()
 # Replace only the historical calibration wall-clock stop with its proposal cutoff.
 D=T/'cal';D.mkdir()
 for f in ['word_ideals.h','smcount3_copy.c','square_trade.inc']:shutil.copyfile(K/f,D/f)
 src=(K/'word_search.c').read_text();old='while(now_s()-t0<secs){';assert src.count(old)==1
 (D/'cal.c').write_text(src.replace(old,'while(proposed<34618){'))
 run([cc,'-O3','-std=c11',str(D/'cal.c'),'-lm','-o',str(D/'cal')])
 txt=run([str(D/'cal'),str(K/'random_start.prefs'),str(D/'out'),'3600','165185'],env=dict(os.environ,WORD_TEMP='0.03',WORD_SQUARE='15'),timeout=120);print(txt,end='')
 for ext in ['prefs','word']:assert Path(str(D/'out')+'.best.'+ext).read_bytes()==(K/('found85.'+ext)).read_bytes()
 print('calibration exact 85')
print('PASS')
