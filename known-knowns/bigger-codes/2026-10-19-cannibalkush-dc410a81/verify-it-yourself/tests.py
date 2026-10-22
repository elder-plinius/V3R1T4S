from verify import check
from pathlib import Path
import tempfile
p=Path(__file__).resolve().parents[1]/'attempts/construction/output'
positive='111111'+'0'*29
cases={'positive':positive+'\n','wrong_width':positive[:-1]+'\n','wrong_weight':'1'*5+'0'*30+'\n','duplicate':positive+'\n'+positive+'\n','bad_distance':positive+'\n'+'1111101'+'0'*28+'\n','invalid_character':'x'+positive[1:]+'\n'}
with tempfile.TemporaryDirectory() as d:
 for name,s in cases.items():
  f=Path(d)/'code.txt';f.write_text(s)
  try:check(f);accepted=True
  except ValueError:accepted=False
  assert accepted==(name=='positive'),name
  print(name,'accepted' if accepted else 'rejected')
print('PASS')
