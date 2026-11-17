from pathlib import Path
import subprocess,tempfile,shutil,os,sys
S=Path(__file__).resolve().parent;C=S.parent;K=C/'calibration'
def run(cmd,**kw):
 p=subprocess.run(cmd,capture_output=True,text=True,**kw)
 if p.returncode:raise RuntimeError(p.stdout+p.stderr)
 return p.stdout
with tempfile.TemporaryDirectory(prefix='cycle-replay-') as td:
 T=Path(td);shutil.copytree(S/'code',T/'code');shutil.copytree(S/'reference',T/'reference');cc=shutil.which('clang') or shutil.which('cc')
 for name in ['cycle_search','suffix_cycles']:run([cc,'-O3','-std=c11',str(T/'code'/(name+'.c')),'-lm','-o',str(T/name)])
 out=T/'pilot';print(run([str(T/'cycle_search'),str(S/'seed.prefs'),str(out),'600','1301002','2','0.025','-','2673573'],timeout=650),end='')
 for ext,expected in [('prefs','expected_raw.prefs'),('word','expected.word')]:assert Path(str(out)+'.best.'+ext).read_bytes()==(S/expected).read_bytes()
 state=Path(str(out)+'.state').read_text();assert 'proposed=2673573' in state and 'valid=30008' in state and 'rng=2432212175335879719' in state
 out=T/'suffix';text=run([str(T/'suffix_cycles'),str(S/'seed.prefs'),str(out),'120','100000','5','-'],timeout=150);print(text,end='');assert 'evaluated=3 cycle_paths=90 cutoff=0' in text
 for ext,expected in [('prefs','expected_raw.prefs'),('word','expected.word')]:assert Path(str(out)+'.best.'+ext).read_bytes()==(S/expected).read_bytes()
 assert (S/'expected.word').read_bytes()==(C/'construction.word').read_bytes()
 D=T/'cal';D.mkdir()
 for f in ['word_ideals.h','smcount3_copy.c','square_trade.inc']:shutil.copyfile(K/f,D/f)
 src=(K/'word_search.c').read_text();old='while(now_s()-t0<secs){';assert src.count(old)==1;(D/'cal.c').write_text(src.replace(old,'while(proposed<34618){'))
 run([cc,'-O3','-std=c11',str(D/'cal.c'),'-lm','-o',str(D/'cal')]);print(run([str(D/'cal'),str(K/'random_start.prefs'),str(D/'out'),'600','165185'],env=dict(os.environ,WORD_TEMP='0.03',WORD_SQUARE='15'),timeout=120),end='')
 for ext in ['prefs','word']:assert Path(str(D/'out')+'.best.'+ext).read_bytes()==(K/('found85.'+ext)).read_bytes()
print('PASS')
