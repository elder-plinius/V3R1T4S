/* glab: find a graceful labeling for each graph6 line on stdin (connected cubic expected, works for any simple graph).
   Output: "<graph6> f0 f1 ... f(n-1)" per line, or "FAIL <graph6>" if the per-graph node budget is exhausted.
   Edge-driven backtracking: differences D = q, q-1, ..., 1 are realised in turn; randomised restarts with
   growing node limits (Luby-like); a final complete (uncapped) run if -c is given.                          */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#define MAXN 64
#define MAXQ 128
static int n, q, deg[MAXN], adj[MAXN][MAXN];
static int lab[MAXN], owner[MAXQ+1];
static unsigned char dused[MAXQ+1];
static long long nodes, limit;
static uint64_t rng = 88172645463325252ULL;
static inline uint64_t rnd(void){ rng ^= rng<<13; rng ^= rng>>7; rng ^= rng<<17; return rng; }
static int perm[MAXN];           /* search order of vertices (random) */
static int stk[MAXN*4], sp;      /* undo stack of differences set */

static int assign(int v, int l){ /* returns 1 ok (diffs pushed), 0 conflict (nothing changed) */
  int base = sp;
  for(int i=0;i<deg[v];i++){ int w=adj[v][i]; if(lab[w]<0) continue;
    int d = l>lab[w]? l-lab[w] : lab[w]-l;
    if(d==0 || dused[d]){ while(sp>base){ dused[stk[--sp]]=0; } return 0; }
    dused[d]=1; stk[sp++]=d; }
  lab[v]=l; owner[l]=v; stk[sp++] = -1-v; /* marker */
  return 1;
}
static void unassign_to(int base){
  while(sp>base){ int x=stk[--sp]; if(x<0){ int v=-1-x; owner[lab[v]]=-1; lab[v]=-1; } else dused[x]=0; }
}
static int search(int D){
  while(D>=1 && dused[D]) D--;
  if(D==0) return 1;
  if(++nodes > limit) return -1;
  int base=sp, r;
  /* (A) labeled x with unlabeled neighbour y */
  int ord0 = rnd()%n;
  for(int k=0;k<n;k++){ int x=perm[(k+ord0)%n]; if(lab[x]<0) continue;
    for(int i=0;i<deg[x];i++){ int y=adj[x][i]; if(lab[y]>=0) continue;
      int s = rnd()&1;
      for(int t=0;t<2;t++){ int l = ((t^s)? lab[x]+D : lab[x]-D); if(l<0||l>q||owner[l]>=0) continue;
        if(assign(y,l)){ r=search(D-1); if(r) return r; unassign_to(base); } } } }
  /* (B) edge with both ends unlabeled gets labels (a,a+D) */
  int a0 = rnd()%(q-D+1);
  for(int aa=0; aa<=q-D; aa++){ int a=(aa+a0)%(q-D+1); if(owner[a]>=0||owner[a+D]>=0) continue;
    for(int k=0;k<n;k++){ int u=perm[k]; if(lab[u]>=0) continue;
      for(int i=0;i<deg[u];i++){ int v=adj[u][i]; if(lab[v]>=0) continue;
        if(assign(u,a)){ if(assign(v,a+D)){ r=search(D-1); if(r) return r; } unassign_to(base); } } } }
  return 0;
}
static int g6decode(const char *s){
  int nn = s[0]-63; const char *p=s+1; if(nn>MAXN-1||nn<1) return -1;
  n=nn; memset(deg,0,sizeof deg); int bit=0, k=0, val=0; q=0;
  for(int j=1;j<n;j++) for(int i=0;i<j;i++){
    if(bit==0){ val = p[k++]-63; bit=6; }
    bit--; if((val>>bit)&1){ adj[i][deg[i]++]=j; adj[j][deg[j]++]=i; q++; } }
  return n;
}
int main(int argc,char**argv){
  long long base_limit = 2000; int complete=0;
  for(int i=1;i<argc;i++){ if(!strcmp(argv[i],"-c")) complete=1; else if(!strcmp(argv[i],"-s")) rng ^= strtoull(argv[++i],0,10)*0x9E3779B97F4A7C15ULL; else base_limit=atoll(argv[i]); }
  char line[4096]; long long tot=0, fails=0, totnodes=0, maxnodes=0;
  while(fgets(line,sizeof line,stdin)){
    int L=strlen(line); while(L&&(line[L-1]=='\n'||line[L-1]=='\r')) line[--L]=0; if(!L) continue;
    if(line[0]=='>') continue;
    if(g6decode(line)<0){ printf("FAIL %s\n",line); fails++; continue; }
    if(q>MAXQ){ printf("FAIL %s\n",line); fails++; continue; }
    tot++; int ok=0; long long gnodes=0;
    for(int attempt=0; attempt<60 && !ok; attempt++){
      for(int v=0;v<n;v++){ lab[v]=-1; perm[v]=v; } for(int l=0;l<=q;l++){ owner[l]=-1; dused[l]=0; } sp=0;
      for(int v=n-1;v>0;v--){ int j=rnd()%(v+1); int t=perm[v]; perm[v]=perm[j]; perm[j]=t; }
      nodes=0; limit = base_limit << (attempt/3 < 20 ? attempt/3 : 20);
      if(complete && attempt==59) limit = (long long)4e18;
      int r = search(q); gnodes += nodes; if(r==1) ok=1;
      else if(r==0){ break; } /* complete search exhausted: no labeling */
    }
    totnodes+=gnodes; if(gnodes>maxnodes) maxnodes=gnodes;
    if(ok){ printf("%s",line); for(int v=0;v<n;v++) printf(" %d",lab[v]); printf("\n"); }
    else { printf("FAIL %s\n",line); fails++; }
  }
  fprintf(stderr,"glab: graphs=%lld fails=%lld totnodes=%lld maxnodes=%lld\n",tot,fails,totnodes,maxnodes);
  return 0;
}
