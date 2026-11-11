/* Searcher S1: odd-graceful labelings of trees, largest-difference-first randomized backtracking with connected
   growth (each odd difference d = 2q-1, 2q-3, ..., 1 labels one new vertex adjacent to the labelled subtree),
   node budget + random restarts. Reads parent arrays (one tree per line, vertex 0 = root), writes
   "<parents> | <labels>". A tree that exhausts all restarts is written as "<parents> | FAIL".
   usage: oglabel n [restarts] [budget]   (stdin -> stdout), OpenMP over batches. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#define MAXN 64
typedef struct { int n, q, deg[MAXN], adj[MAXN][MAXN]; int lab[MAXN]; unsigned char used[2*MAXN]; uint64_t rng; long budget; } S;
static inline uint64_t xr(uint64_t*s){ uint64_t x=*s; x^=x<<13; x^=x>>7; x^=x<<17; return *s=x; }
static int nlab; 
static int dfs(S*s,int d,int cnt){
  if(d<1) return 1;
  if(--s->budget<0) return 0;
  /* collect candidates: (v unlabeled, neighbour u labeled, newlabel = lab[u]+-d) */
  int cv[2*MAXN*2], cl[2*MAXN*2], nc=0; int L=2*s->q-1;
  for(int u=0;u<s->n;u++) if(s->lab[u]>=0){
    for(int k=0;k<s->deg[u];k++){ int v=s->adj[u][k]; if(s->lab[v]>=0) continue;
      int a=s->lab[u]+d, b=s->lab[u]-d;
      if(a<=L && !s->used[a]){ cv[nc]=v; cl[nc]=a; nc++; }
      if(b>=0 && !s->used[b]){ cv[nc]=v; cl[nc]=b; nc++; }
    }
  }
  /* random order */
  for(int i=nc-1;i>0;i--){ int j=xr(&s->rng)%(i+1); int t=cv[i];cv[i]=cv[j];cv[j]=t; t=cl[i];cl[i]=cl[j];cl[j]=t; }
  for(int i=0;i<nc;i++){
    int v=cv[i], l=cl[i];
    if(s->lab[v]>=0 || s->used[l]) continue;
    s->lab[v]=l; s->used[l]=1;
    if(dfs(s,d-2,cnt+1)) return 1;
    s->lab[v]=-1; s->used[l]=0;
    if(s->budget<0) return 0;
  }
  return 0;
}
static int solve(S*s,int restarts,long budget,uint64_t seed){
  int L=2*s->q-1;
  for(int r=0;r<restarts;r++){
    s->rng=seed*0x9E3779B97F4A7C15ULL+r*7919+1;
    for(int v=0;v<s->n;v++) s->lab[v]=-1; memset(s->used,0,sizeof s->used);
    /* first edge gets labels 0 and L: pick a random edge and orientation */
    int v=1+xr(&s->rng)%(s->n-1); int u=-1; /* parent of v */
    for(int k=0;k<s->deg[v];k++){ int w=s->adj[v][k]; if(w<v){u=w;break;} }
    if(u<0) u=s->adj[v][0];
    if(xr(&s->rng)&1){ int t=u;u=v;v=t; }
    s->lab[u]=0; s->lab[v]=L; s->used[0]=1; s->used[L]=1;
    s->budget=budget;
    if(dfs(s,L-2,2)) return 1;
  }
  return 0;
}
int main(int argc,char**argv){
  int n=atoi(argv[1]); int restarts=argc>2?atoi(argv[2]):200; long budget=argc>3?atol(argv[3]):20000;
  if(n<2||n>MAXN) return 1;
  size_t cap=1<<16; char **lines=malloc(cap*sizeof(char*)); char **outl=malloc(cap*sizeof(char*));
  char buf[4096]; long fails=0, total=0;
  for(;;){
    size_t m=0;
    while(m<cap && fgets(buf,sizeof buf,stdin)){ buf[strcspn(buf,"\n")]=0; lines[m++]=strdup(buf); }
    if(!m) break;
    #pragma omp parallel for schedule(dynamic,64) reduction(+:fails)
    for(size_t t=0;t<m;t++){
      S s; s.n=n; s.q=n-1; memset(s.deg,0,sizeof s.deg);
      int par[MAXN]; char*p=lines[t];
      for(int i=1;i<n;i++){ par[i]=(int)strtol(p,&p,10); s.adj[i][s.deg[i]++]=par[i]; s.adj[par[i]][s.deg[par[i]]++]=i; }
      int ok=solve(&s,restarts,budget,(uint64_t)(total+t)+12345);
      char *o=malloc(strlen(lines[t])+8*MAXN+16); int k=sprintf(o,"%s |",lines[t]);
      if(ok) for(int v=0;v<n;v++) k+=sprintf(o+k," %d",s.lab[v]); else { k+=sprintf(o+k," FAIL"); fails++; }
      outl[t]=o;
    }
    for(size_t t=0;t<m;t++){ puts(outl[t]); free(outl[t]); free(lines[t]); }
    total+=m;
  }
  fprintf(stderr,"n=%d trees=%ld fails=%ld\n",n,total,fails);
  return 0;
}
