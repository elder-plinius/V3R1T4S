// Independent Collatz-Wielandt checker for proper q-colourings of the cycle C_m.
// Definition: C[w,w'] = 1 iff w proper cycle colouring, w' proper cycle colouring, w_i != w'_i for all i.
// Certificate v is a function of the orbit under S_q x D_m; we lift it to every proper colouring,
// and for each orbit representative w compute S(w) = sum_{w'} v(orbit(w')) by exhaustive enumeration of w'.
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <pthread.h>
typedef unsigned __int128 u128;
static int q, m;
static uint64_t g[40][8][8];           // g[r][k][l]
static uint64_t cum[40][8][8][9];
static uint64_t N;
static uint64_t *V;                    // dense lifted v, 4 limbs per proper RGS (by lex rank)
static int32_t *idOfRank;
static uint8_t *reps;                  // reps[id*m ..]
static uint32_t nid=0, nfile;
static uint64_t *vfile;                // n*4
static uint64_t *yfile;
static uint64_t (*Sout)[5];

static void tables(void){
  for(int k=1;k<=q;k++) for(int l=0;l<q;l++) g[0][k][l]=(l!=0);
  for(int r=1;r<=m;r++) for(int k=1;k<=q;k++) for(int l=0;l<q;l++){
    uint64_t s=0; int mx = k<q?k:q-1;
    for(int x=0;x<=mx;x++){ if(x==l) continue; int k2 = k>x+1?k:x+1; s+=g[r-1][k2][x]; }
    g[r][k][l]=s;
  }
  for(int r=0;r<=m;r++) for(int k=1;k<=q;k++) for(int l=0;l<q;l++){
    uint64_t s=0;
    for(int lab=0;lab<=q;lab++){
      cum[r][k][l][lab]=s;
      int mx = k<q?k:q-1;
      if(lab<=mx && lab!=l){ int k2=k>lab+1?k:lab+1; s+=g[r][k2][lab]; }
    }
  }
  N=g[m-1][1][0];
}
static uint64_t rank_of(const uint8_t*s){
  uint64_t off=0; int k=1;
  for(int i=1;i<m;i++){ off+=cum[m-1-i][k][s[i-1]][s[i]]; if(s[i]+1>k)k=s[i]+1; }
  return off;
}
static void relabel(const uint8_t*src, uint8_t*dst){
  int mp[8]; for(int i=0;i<8;i++)mp[i]=-1; int k=0;
  for(int i=0;i<m;i++){ if(mp[src[i]]<0) mp[src[i]]=k++; dst[i]=mp[src[i]]; }
}
// build
static uint64_t counter=0;
static uint8_t cur[40];
static void build_rec(int i,int k){
  if(i==m){
    uint64_t rk=counter++;
    // canonical = lex-min over dihedral images
    uint8_t best[40], t[40], u[40]; memcpy(best,cur,m);
    for(int f=0;f<2;f++) for(int r=0;r<m;r++){
      for(int j=0;j<m;j++) t[j]=cur[f? ((r-j)%m+m)%m : (r+j)%m];
      relabel(t,u);
      if(memcmp(u,best,m)<0) memcpy(best,u,m);
    }
    int id;
    if(memcmp(best,cur,m)==0){ id=nid++; if(id>=0){ memcpy(reps+(size_t)id*m,cur,m);} idOfRank[rk]=id; }
    else { uint64_t r2=rank_of(best); if(r2>=rk){fprintf(stderr,"order bug\n");exit(2);} id=idOfRank[r2]; idOfRank[rk]=id; }
    if(id<(int)nfile) memcpy(V+rk*4, vfile+(size_t)id*4, 32);
    else { memset(V+rk*4,0,32); }
    return;
  }
  int mx = k<q?k:q-1;
  for(int x=0;x<=mx;x++){
    if(i>0 && x==cur[i-1]) continue;
    if(i==m-1 && x==0) continue;
    cur[i]=x; build_rec(i+1, k>x+1?k:x+1);
  }
}
// worker
typedef struct { u128 acc[4]; const uint8_t*w; int map[8]; } Ctx;
static void dfs(Ctx*c,int i,int k,int last,int c0,int prevc,uint64_t off){
  for(int col=0;col<q;col++){
    if(col==c->w[i]) continue;
    if(i>0 && col==prevc) continue;
    if(i==m-1 && col==c0) continue;
    int lab=c->map[col]; int isnew=0; int k2=k;
    if(lab<0){ lab=k; c->map[col]=lab; isnew=1; k2=k+1; }
    uint64_t o=off;
    if(i>0) o+=cum[m-1-i][k][last][lab];
    if(i==m-1){ const uint64_t*p=V+o*4; c->acc[0]+=p[0];c->acc[1]+=p[1];c->acc[2]+=p[2];c->acc[3]+=p[3]; }
    else dfs(c,i+1,k2,lab,i==0?col:c0,col,o);
    if(isnew) c->map[col]=-1;
  }
}
static volatile uint32_t nextchunk=0;
static pthread_mutex_t mu=PTHREAD_MUTEX_INITIALIZER;
static uint32_t donecount=0;
static void*worker(void*a){
  for(;;){
    pthread_mutex_lock(&mu); uint32_t s=nextchunk; nextchunk+=16; pthread_mutex_unlock(&mu);
    if(s>=nid) break;
    uint32_t e=s+16; if(e>nid)e=nid;
    for(uint32_t id=s;id<e;id++){
      Ctx c; memset(&c,0,sizeof c); c.w=reps+(size_t)id*m; for(int i=0;i<8;i++)c.map[i]=-1;
      dfs(&c,0,0,0,0,0,0);
      // normalise to 5 limbs
      u128 carry=0; for(int j=0;j<4;j++){ u128 t=c.acc[j]+carry; Sout[id][j]=(uint64_t)t; carry=t>>64; }
      Sout[id][4]=(uint64_t)carry; if((carry>>64)!=0){fprintf(stderr,"overflow\n");exit(3);}
    }
    pthread_mutex_lock(&mu); donecount+=e-s; if((donecount/16)%200==0){fprintf(stderr,"progress %u/%u\n",donecount,nid);} pthread_mutex_unlock(&mu);
  }
  return 0;
}
int main(int argc,char**argv){
  q=atoi(argv[1]); m=atoi(argv[2]); const char*cert=argv[3]; const char*out=argv[4]; int nth=atoi(argv[5]);
  tables();
  fprintf(stderr,"q=%d m=%d proper RGS count N=%llu\n",q,m,(unsigned long long)N);
  FILE*f=fopen(cert,"rb"); uint32_t n; if(fread(&n,4,1,f)!=1)return 1; nfile=n;
  vfile=malloc((size_t)n*32); yfile=malloc((size_t)n*32);
  if(fread(vfile,32,n,f)!=n||fread(yfile,32,n,f)!=n){fprintf(stderr,"short cert\n");return 1;}
  { long pos=ftell(f); fseek(f,0,SEEK_END); if(ftell(f)!=pos){fprintf(stderr,"trailing bytes\n");return 1;} }
  fclose(f);
  V=malloc(N*32); idOfRank=malloc(N*4); reps=malloc((size_t)(n+16)*m*4+1000000);
  // reps size: allocate for max possible orbits count generously
  free(reps); reps=malloc((size_t)(N/ (2*m)+ 100000)*m*2);
  build_rec(0,0);
  if(counter!=N){fprintf(stderr,"count mismatch %llu %llu\n",(unsigned long long)counter,(unsigned long long)N);return 1;}
  fprintf(stderr,"orbits found by own enumeration: %u ; orbits in certificate: %u\n",nid,nfile);
  if(nid!=nfile){fprintf(stderr,"ORBIT COUNT MISMATCH\n");return 1;}
  Sout=malloc((size_t)nid*40);
  pthread_t th[64]; for(int t=0;t<nth;t++)pthread_create(&th[t],0,worker,0);
  for(int t=0;t<nth;t++)pthread_join(th[t],0);
  FILE*o=fopen(out,"w");
  int ymis=0;
  for(uint32_t id=0;id<nid;id++){
    // line: id v_hex S_hex  (hex from limbs, most significant first)
    fprintf(o,"%u ",id);
    for(int j=3;j>=0;j--)fprintf(o,"%016llx",(unsigned long long)vfile[(size_t)id*4+j]);
    fprintf(o," ");
    for(int j=4;j>=0;j--)fprintf(o,"%016llx",(unsigned long long)Sout[id][j]);
    fprintf(o,"\n");
    if(Sout[id][4]!=0||memcmp(Sout[id],yfile+(size_t)id*4,32)!=0)ymis++;
  }
  fclose(o);
  fprintf(stderr,"orbits where own S != certificate y: %d\n",ymis);
  return 0;
}
