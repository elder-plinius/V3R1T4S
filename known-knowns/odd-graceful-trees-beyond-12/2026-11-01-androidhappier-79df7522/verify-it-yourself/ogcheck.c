/* Checker K (independent of the searcher and of networkx):
   (1) regenerates all free trees on n vertices by adding a leaf to every vertex of every tree on n-1 vertices
       (starting from the 1-vertex tree), deduplicating by a canonical code = min over the tree's centres of the
       rooted AHU code (bit string "1 children 0", children sorted by (length, value)); (2) prints the count per order
       (to compare with A000055); (3) reads a certificate file for order n: lines "<p_1 ... p_{n-1}> | <f_0 ... f_{n-1}>",
       checks each line is a tree on n vertices, labels are distinct integers in [0, 2n-3], and the edge differences are
       exactly {1, 3, ..., 2n-3}; (4) checks the multiset of canonical codes of the certificate equals the regenerated
       set (no missing, duplicate or extra tree).
   usage: ogcheck n [certfile]     (n <= 31)   prints PASS/FAIL lines */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
typedef uint64_t u64;
#define MAXN 32
typedef struct { int len; u64 bits; } Code;
static int cmpc(const void*a,const void*b){ const Code*x=a,*y=b; if(x->len!=y->len) return x->len<y->len?-1:1; return x->bits<y->bits?-1:(x->bits>y->bits); }
static int cmpu(const void*a,const void*b){ u64 x=*(const u64*)a,y=*(const u64*)b; return x<y?-1:(x>y); }
typedef struct { int n, deg[MAXN], adj[MAXN][MAXN]; } T;
static Code rooted(const T*t,int v,int parent){
  Code ch[MAXN]; int m=0;
  for(int k=0;k<t->deg[v];k++){ int w=t->adj[v][k]; if(w==parent) continue; ch[m++]=rooted(t,w,v); }
  qsort(ch,m,sizeof(Code),cmpc);
  Code r; r.len=1; r.bits=1;
  for(int i=0;i<m;i++){ r.bits=(r.bits<<ch[i].len)|ch[i].bits; r.len+=ch[i].len; }
  r.bits<<=1; r.len+=1; return r;
}
static u64 freecode(const T*t){
  int n=t->n; if(n==1) return 2; /* "10" */
  int deg[MAXN], rem=n, alive[MAXN], leaves[MAXN], nl=0;
  for(int v=0;v<n;v++){ deg[v]=t->deg[v]; alive[v]=1; if(deg[v]<=1) leaves[nl++]=v; }
  while(rem>2){
    int nn=0, nxt[MAXN];
    for(int i=0;i<nl;i++){ int v=leaves[i]; alive[v]=0; rem--; for(int k=0;k<t->deg[v];k++){ int w=t->adj[v][k]; if(alive[w] && --deg[w]==1) nxt[nn++]=w; } }
    memcpy(leaves,nxt,nn*sizeof(int)); nl=nn;
  }
  u64 best=~0ULL;
  for(int v=0;v<n;v++) if(alive[v]){ Code c=rooted(t,v,-1); if(c.len!=2*n){fprintf(stderr,"len bug\n");exit(9);} if(c.bits<best) best=c.bits; }
  return best;
}
static void decode(u64 bits,int n,T*t){ /* bits: 2n bits, MSB first */
  memset(t,0,sizeof *t); t->n=n; int stack[MAXN],sp=0,cnt=0;
  for(int i=2*n-1;i>=0;i--){ int b=(bits>>i)&1;
    if(b){ int v=cnt++; if(sp){ int p=stack[sp-1]; t->adj[p][t->deg[p]++]=v; t->adj[v][t->deg[v]++]=p; } stack[sp++]=v; }
    else sp--; }
  if(cnt!=n){fprintf(stderr,"decode bug\n");exit(9);}
}
static u64* gen(int n,size_t*count){
  u64 *cur=malloc(8); cur[0]=2; size_t nc=1;
  for(int m=2;m<=n;m++){
    size_t cap=nc*(m-1); u64*cand=malloc(cap*8);
    #pragma omp parallel for schedule(dynamic,256)
    for(size_t i=0;i<nc;i++){
      T t; decode(cur[i],m-1,&t);
      for(int v=0;v<m-1;v++){ T u=t; u.n=m; u.adj[v][u.deg[v]++]=m-1; u.adj[m-1][u.deg[m-1]++]=v; cand[i*(m-1)+v]=freecode(&u); }
    }
    qsort(cand,cap,8,cmpu); size_t k=0; for(size_t i=0;i<cap;i++) if(!k||cand[i]!=cand[k-1]) cand[k++]=cand[i];
    free(cur); cur=realloc(cand,k*8); nc=k;
    fprintf(stderr,"regenerated order %d: %zu trees\n",m,nc);
  }
  *count=nc; return cur;
}
int main(int argc,char**argv){
  int n=atoi(argv[1]); if(n<1||n>=MAXN) return 1;
  size_t ng; u64*G=gen(n,&ng);
  printf("order %d: regenerated %zu trees\n",n,ng);
  if(argc<3) return 0;
  FILE*f=strcmp(argv[2],"-")? fopen(argv[2],"r") : stdin; if(!f){printf("FAIL cannot open\n");return 2;}
  size_t cap=ng+16, nc=0; u64*C=malloc(cap*8); char *line=malloc(1<<16); long bad=0, lineno=0;
  while(fgets(line,1<<16,f)){
    lineno++; char*bar=strchr(line,'|'); if(!bar){ if(!bad) printf("FAIL line %ld: no '|'\n",lineno); bad++; continue; }
    T t; memset(&t,0,sizeof t); t.n=n; char*p=line; int par[MAXN]; int ok=1;
    for(int i=1;i<n;i++){ char*e; long x=strtol(p,&e,10); if(e==p||x<0||x>=n||x==i){ok=0;break;} par[i]=(int)x; p=e; }
    /* union-find: n-1 edges, connected => tree */
    int uf[MAXN]; for(int i=0;i<n;i++) uf[i]=i;
    #define FIND(x) ({int _x=(x); while(uf[_x]!=_x) _x=uf[_x]=uf[uf[_x]]; _x;})
    if(ok) for(int i=1;i<n;i++){ int a=FIND(i), b=FIND(par[i]); if(a==b){ok=0;break;} uf[a]=b; t.adj[i][t.deg[i]++]=par[i]; t.adj[par[i]][t.deg[par[i]]++]=i; }
    int lab[MAXN]; p=bar+1;
    if(ok) for(int v=0;v<n;v++){ char*e; long x=strtol(p,&e,10); if(e==p){ok=0;break;} lab[v]=(int)x; p=e; }
    if(ok){ while(*p==' '||*p=='\t'||*p=='\n'||*p=='\r') p++; if(*p) ok=0; }
    if(ok){ int L=2*(n-1)-1; unsigned char used[2*MAXN]={0}, dif[2*MAXN]={0};
      for(int v=0;v<n;v++){ if(lab[v]<0||lab[v]>L||used[lab[v]]){ok=0;break;} used[lab[v]]=1; }
      if(ok) for(int i=1;i<n;i++){ int d=abs(lab[i]-lab[par[i]]); if(d<1||d>L||!(d&1)||dif[d]){ok=0;break;} dif[d]=1; }
      if(ok) for(int d=1;d<=L;d+=2) if(!dif[d]){ok=0;break;}
    }
    if(!ok){ if(bad<5) printf("FAIL line %ld: invalid tree or labeling\n",lineno); bad++; continue; }
    if(nc==cap){ cap*=2; C=realloc(C,cap*8); }
    C[nc++]=freecode(&t);
  }
  fclose(f);
  qsort(C,nc,8,cmpu);
  long dup=0; for(size_t i=1;i<nc;i++) if(C[i]==C[i-1]) dup++;
  long missing=0, extra=0; size_t i=0,j=0;
  while(i<ng||j<nc){
    if(j<nc && j>0 && C[j]==C[j-1]){ j++; continue; }
    if(i<ng && (j>=nc || G[i]<C[j])){ missing++; i++; }
    else if(j<nc && (i>=ng || C[j]<G[i])){ extra++; j++; }
    else { i++; j++; }
  }
  printf("order %d: certificate lines %ld, valid labelings %zu, invalid %ld, duplicate trees %ld, missing trees %ld, extra trees %ld\n",n,lineno,nc,bad,dup,missing,extra);
  int pass = bad==0 && dup==0 && missing==0 && extra==0 && nc==ng;
  printf("%s order %d\n", pass?"PASS":"FAIL", n);
  return pass?0:1;
}
