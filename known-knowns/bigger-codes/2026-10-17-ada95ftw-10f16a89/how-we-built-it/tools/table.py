import re,sys,json
h=open(sys.argv[1] if len(sys.argv)>1 else 'data/Andw.html',encoding='latin-1').read()
out={}
secs=re.split(r'<h1><a name="d(\d+)">',h)
for i in range(1,len(secs),2):
    d=int(secs[i]); body=secs[i+1].split('<h1>')[0]
    for row in re.findall(r'<tr>(.*?)</tr>',body,re.S):
        m=re.search(r'<th>(\d+)</th>',row)
        if not m: continue
        n=int(m.group(1))
        cells=re.findall(r'<td[^>]*>(.*?)</td>',row,re.S)
        for j,c in enumerate(cells):
            t=re.sub(r'<sup>.*?</sup>','',c,flags=re.S); t=re.sub(r'<[^>]*>','',t).strip()
            nums=re.findall(r'\d+',t)
            if not nums: continue
            w=d//2+1+j
            out[f"{n},{d},{w}"]={'lo':int(nums[0]),'hi':int(nums[-1]),'raw':t}
json.dump(out,open('data/cells.json','w'),indent=0)
print(len(out))
