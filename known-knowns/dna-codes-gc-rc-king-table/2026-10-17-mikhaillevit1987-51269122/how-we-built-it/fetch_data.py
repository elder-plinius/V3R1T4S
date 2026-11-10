import urllib.request,pathlib,datetime,hashlib,json
p=pathlib.Path('runs/2026-10-17-1337/attempts/linear_codes')
u='https://rambutan.umassmed.edu/king/codes/LinearGCRC.txt'
try:
 r=urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'V3R1T4S research'}),timeout=30);b=r.read();(p/'LinearGCRC.txt').write_bytes(b);print(json.dumps({'url':u,'status':r.status,'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'sha256':hashlib.sha256(b).hexdigest()})); print(b.decode()[:16000])
except Exception as e:print(type(e).__name__,str(e))
