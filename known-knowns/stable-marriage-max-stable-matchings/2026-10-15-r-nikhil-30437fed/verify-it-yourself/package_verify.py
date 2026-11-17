from pathlib import Path
import shutil,subprocess,tempfile,sys
P=Path(__file__).resolve().parents[1]
with tempfile.TemporaryDirectory(prefix='stable-verification-') as tmp:
 d=Path(tmp)
 for f in ['object.prefs','construction.word','object.json']:shutil.copyfile(P/'object'/f,d/f)
 for f in ['arc_count.cpp','verify.py','rebuild.py']:shutil.copyfile(P/'verify-it-yourself'/f,d/f)
 result=subprocess.run([sys.executable,str(d/'verify.py')],cwd=d)
 sys.exit(result.returncode)
