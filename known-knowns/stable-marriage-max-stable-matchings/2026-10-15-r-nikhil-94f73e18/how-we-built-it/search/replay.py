from pathlib import Path
import tempfile,subprocess,shutil,os,json,sys,hashlib
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
 assert hashlib.sha256((S/(last['book']+'.expected.word')).read_bytes()).hexdigest()==json.loads((C/'construction.word').read_text())['source_word_sha256']
 # Replace only the historical calibration wall-clock stop with its proposal cutoff.
 D=T/'cal';D.mkdir()
 for f in ['word_ideals.h','smcount3_copy.c','square_trade.inc']:shutil.copyfile(K/f,D/f)
 src=(K/'word_search.c').read_text();old='while(now_s()-t0<secs){';assert src.count(old)==1
 (D/'cal.c').write_text(src.replace(old,'while(proposed<34618){'))
 run([cc,'-O3','-std=c11',str(D/'cal.c'),'-lm','-o',str(D/'cal')])
 txt=run([str(D/'cal'),str(K/'random_start.prefs'),str(D/'out'),'3600','165185'],env=dict(os.environ,WORD_TEMP='0.03',WORD_SQUARE='15'),timeout=120);print(txt,end='')
 for ext in ['prefs','word']:assert Path(str(D/'out')+'.best.'+ext).read_bytes()==(K/('found85.'+ext)).read_bytes()
 print('calibration exact 85')
with tempfile.TemporaryDirectory(prefix='suffix-replay-') as td:
 T=Path(td);cc=shutil.which('clang') or shutil.which('cc');shutil.copyfile(S/'suffix_extend.py',T/'suffix_extend.py')
 run([cc,'-O3','-std=c11',str(S/'smcount3_copy.c'),'-lm','-o',str(T/'smcount')])
 plan=json.loads((S/'suffix_plan.json').read_text());out=T/'suffix'
 print(run([sys.executable,str(T/'suffix_extend.py'),str(S/plan['source_word']),str(out),'180',str(plan['maxdepth'])],timeout=240),end='')
 result=json.loads(Path(str(out)+'.results.json').read_text())
 for field in ['best','nodes','maxdepth','cutoff']:
  expected=plan['count'] if field=='best' else plan[field];assert result[field]==expected,(field,result[field],expected)
 stem=str(out)+'.n23.c'+str(plan['count'])
 assert Path(stem+'.prefs').read_bytes()==(S/'suffix.expected.prefs').read_bytes()
 assert Path(stem+'.json').read_bytes()==(C/'construction.word').read_bytes()
 print('suffix complete and exact',plan['count'],plan['nodes'])
print('PASS')
