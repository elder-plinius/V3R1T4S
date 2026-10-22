from html.parser import HTMLParser
import pathlib,json,re
ROOT=pathlib.Path(__file__).resolve().parent
class Tables(HTMLParser):
 def __init__(self):super().__init__();self.tables=[];self.table=None;self.row=None;self.cell=None;self.sup=0
 def handle_starttag(self,t,a):
  if t=='table':self.table=[]
  elif t=='tr' and self.table is not None:self.row=[]
  elif t in ('td','th') and self.row is not None:self.cell=''
  elif t=='sup':self.sup+=1
 def handle_endtag(self,t):
  if t=='sup':self.sup-=1
  elif t in ('td','th') and self.cell is not None:self.row.append(self.cell.strip());self.cell=None
  elif t=='tr' and self.row is not None:self.table.append(self.row);self.row=None
  elif t=='table' and self.table is not None:self.tables.append(self.table);self.table=None
 def handle_data(self,d):
  if self.cell is not None and not self.sup:self.cell+=d
p=Tables();p.feed((ROOT/'12-echols-html.body').read_text());rows=[]
for tab in p.tables:
 for row in tab:
  if len(row)!=12:continue
  for off in (0,6):
   group=row[off:off+6]
   if all(re.fullmatch(r'[+]?\d+',x) for x in group):rows.append(dict(zip(['n','d','w','prior','M','gain'],map(int,group))))
assert len(rows)==124, len(rows)
(ROOT/'echols-124-rows.json').write_text(json.dumps(rows,indent=2))
raw=(ROOT/'01-brouwer.body').read_text();cells=[]
for d in range(6,19,2):
 start=raw.index('name="d'+str(d)+'"');end=raw.find('<h1><a name="d',start+8);part=raw[start:end if end!=-1 else None]
 p=Tables();p.feed(part)
 for tab in p.tables:
  if tab and tab[0] and 'n\\w' in tab[0][0]:
   weights=list(map(int,tab[0][1:]))
   for row in tab[1:]:
    if row and row[0].isdigit():
     n=int(row[0])
     for w,c in zip(weights,row[1:]):
      m=re.match(r'(\d+)',c)
      if m:cells.append({'n':n,'d':d,'w':w,'M':int(m[1]),'text':c})
(ROOT/'brouwer-grid-cells.json').write_text(json.dumps(cells,indent=2))
B={};origin={}
for c in cells+rows:
 n,d,w,M=[c[x]for x in ['n','d','w','M']];w=min(w,n-w)
 if M>B.get((n,w),0):B[n,w]=M;origin[n,w]={'source':c,'steps':[]}
changed=True
while changed:
 changed=False
 for (n,w),m in list(B.items()):
  if n==0:continue
  for nn,ww,v,rule in [(n-1,w-1,(m*w+n-1)//n,'fix one'),(n-1,w,(m*(n-w)+n-1)//n,'fix zero'),(n+1,w,m,'append zero'),(n+1,w+1,m,'append one')]:
   if not(0<=ww<=nn<=64):continue
   ww=min(ww,nn-ww)
   if v>B.get((nn,ww),0):B[nn,ww]=v;origin[nn,ww]={'source':origin[n,w]['source'],'steps':origin[n,w]['steps']+[rule]};changed=True
out={'target_bound':B[25,11],'origin':origin[25,11],'grid_cells':len(cells),'echols_rows':len(rows),'echols_max_M':max(x['M']for x in rows),'echols_direct_target':[x for x in rows if x['n']==25 and x['d']==6 and x['w']in[11,14]],'scope':'All captured n\\w grids for d>=6 plus Echols124; complement, pigeonhole shortening, constant padding, distance relaxation. Other constructions not exhaustively excluded.'}
(ROOT/'standard-propagation.json').write_text(json.dumps(out,indent=2));print(json.dumps(out))
