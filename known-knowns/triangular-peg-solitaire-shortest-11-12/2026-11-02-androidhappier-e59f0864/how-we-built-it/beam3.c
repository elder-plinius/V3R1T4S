/* Beam search over moves for triangular peg solitaire Triangle(n), n <= 14.
   State = board bitmask (u128). Layer k = boards reachable in k moves. Children = every chain of jumps by one peg.
   Rank: key = W*filled_merson(child) + pegs(child)  (lower is better); keep top B distinct boards (canonical under
   the 6 triangle symmetries). Parent pointers + move strings are kept to print the solution.
   usage: beam n B W [maxmoves] [start_hole_index|-1]  */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
typedef unsigned __int128 u128;
static int n,N; static int R_[200],C_[200]; static int idx[20][20];
static int nj; static int jf[2000],jo[2000],jt[2000]; static int jstart[200],jcnt[200];
static int perm[6][200];
static int nreg; static u128 regmask[200];
static int W; static long PF=8; static int V=0; static unsigned seed=0; static u128 nbm[200];
static inline int popc(u128 x){return __builtin_popcountll((uint64_t)x)+__builtin_popcountll((uint64_t)(x>>64));}
static inline u128 bit(int i){return ((u128)1)<<i;}
static u128 xform(u128 b,int s){u128 r=0;for(int i=0;i<N;i++) if(b>>i&1) r|=bit(perm[s][i]);return r;}
static u128 canon(u128 b){u128 m=b;for(int s=1;s<6;s++){u128 t=xform(b,s);if(t<m)m=t;}return m;}
static int filled(u128 b){int f=0;for(int r=0;r<nreg;r++) if((b&regmask[r])==regmask[r]) f++;return f;}
/* ---- state store ---- */
typedef struct {u128 b; int parent; int key; char *mv;} St;
static St *st; static long nst,cap;
static long addst(u128 b,int parent,int key,const char*mv){ if(nst==cap){cap=cap?cap*2:1<<20; st=realloc(st,cap*sizeof(St));}
  st[nst].b=b;st[nst].parent=parent;st[nst].key=key;st[nst].mv=strdup(mv);return nst++;}
/* hash set of canonical boards for a layer */
static u128 *hk; static int *hv; static long hcap;
static void hclear(long need){ long c=1; while(c<need*2)c<<=1; if(c!=hcap){free(hk);free(hv);hcap=c;hk=malloc(c*sizeof(u128));hv=malloc(c*sizeof(int));}
  memset(hv,-1,hcap*sizeof(int)); }
static int *hslot(u128 k){ uint64_t h=(uint64_t)k*0x9E3779B97F4A7C15ULL ^ (uint64_t)(k>>64)*0xC2B2AE3D27D4EB4FULL; long i=(h^(h>>29))&(hcap-1);
  while(hv[i]!=-1 && hk[i]!=k) i=(i+1)&(hcap-1); hk[i]=k; return &hv[i]; }
static void hname(int i,char*o){sprintf(o,"%c%d",'a'+C_[i]-1,R_[i]);}
/* candidate list */
typedef struct {u128 b; int parent; int key; long mv;} Cand;
static char *arena; static long alen,acap;
static long astr(const char*m){long L=strlen(m)+1; if(alen+L>acap){acap=acap?acap*2:1<<24; while(alen+L>acap)acap*=2; arena=realloc(arena,acap);} memcpy(arena+alen,m,L); long o=alen; alen+=L; return o;}
static Cand *cand; static long ncand,ccap; static long B;
static int cmpc(const void*a,const void*b){int x=((Cand*)a)->key,y=((Cand*)b)->key;return x<y?-1:x>y;}
static void push(u128 b,int parent,const char*mv){
  u128 c=canon(b); int *s=hslot(c);
  int iso=0; if(V){ for(int i=0;i<N;i++) if((b>>i&1) && !(b&nbm[i])) iso++; }
  int key=4*(W*filled(b)+popc(b)+V*iso); if(seed){uint64_t h=(uint64_t)c*(0x9E3779B97F4A7C15ULL+seed); h^=h>>31; key+= (int)(h&3);}
  if(*s!=-1){ if(cand[*s].key<=key) return; cand[*s].b=b;cand[*s].parent=parent;cand[*s].key=key;cand[*s].mv=astr(mv);return;}
  if(ncand==ccap){ccap=ccap?ccap*2:1<<20;cand=realloc(cand,ccap*sizeof(Cand));}
  *s=ncand; cand[ncand].b=b;cand[ncand].parent=parent;cand[ncand].key=key;cand[ncand].mv=astr(mv);ncand++;
}
static int curparent; static char path[400]; static int plen;
static void chain(u128 b,int pos){ /* peg at pos, try every jump; after each jump record child and continue */
  for(int k=jstart[pos];k<jstart[pos]+jcnt[pos];k++){ int o=jo[k],t=jt[k];
    if((b>>o&1) && !(b>>t&1)){ u128 nb=(b&~bit(pos)&~bit(o))|bit(t); int sv=plen; char h[8]; hname(t,h);
      plen+=sprintf(path+plen,"-%s",h); if(plen<190){ push(nb,curparent,path); chain(nb,t);} plen=sv; path[plen]=0; } }
}
int main(int argc,char**argv){
  n=atoi(argv[1]); B=atol(argv[2]); W=atoi(argv[3]); if(getenv("BEAM_V"))V=atoi(getenv("BEAM_V")); if(getenv("BEAM_SEED"))seed=atoi(getenv("BEAM_SEED")); int maxm=argc>4?atoi(argv[4]):99; int sh=argc>5?atoi(argv[5]):-1;
  N=0; for(int r=1;r<=n;r++)for(int c=1;c<=r;c++){idx[r][c]=N;R_[N]=r;C_[N]=c;N++;}
  int dr[6]={0,0,1,-1,1,-1},dc[6]={1,-1,0,0,1,-1};
  for(int i=0;i<N;i++){jstart[i]=nj;jcnt[i]=0;for(int d=0;d<6;d++){int r2=R_[i]+2*dr[d],c2=C_[i]+2*dc[d];if(c2>=1&&c2<=r2&&r2<=n){jf[nj]=i;jo[nj]=idx[R_[i]+dr[d]][C_[i]+dc[d]];jt[nj]=idx[r2][c2];nj++;jcnt[i]++;}}}
  for(int i=0;i<N;i++){nbm[i]=0;for(int d=0;d<6;d++){int r2=R_[i]+dr[d],c2=C_[i]+dc[d];if(c2>=1&&c2<=r2&&r2<=n)nbm[i]|=bit(idx[r2][c2]);}}
  /* symmetries via barycentric coords (x=c-1, y=r-c, z=n-r) permutations */
  int P[6][3]={{0,1,2},{1,2,0},{2,0,1},{1,0,2},{0,2,1},{2,1,0}};
  for(int s=0;s<6;s++)for(int i=0;i<N;i++){int v[3]={C_[i]-1,R_[i]-C_[i],n-R_[i]};int x=v[P[s][0]],y=v[P[s][1]]; int c=x+1,r=y+c; perm[s][i]=idx[r][c];}
  /* Merson regions: greedy - corners, edge pairs, then interior 7-hexagons, all disjoint */
  int used[200]={0};
  int corners[3]={idx[1][1],idx[n][1],idx[n][n]}; for(int k=0;k<3;k++){regmask[nreg++]=bit(corners[k]);used[corners[k]]=1;}
  for(int i=0;i<N;i++){ if(used[i])continue; int r=R_[i],c=C_[i]; int edge=(c==1)||(c==r)||(r==n); if(!edge)continue;
    int cand2[3][2]={{r+1,c},{r,c+1},{r+1,c+1}}; for(int k=0;k<3;k++){int r2=cand2[k][0],c2=cand2[k][1]; if(c2<1||c2>r2||r2>n)continue; int j=idx[r2][c2];
      int e2=(c2==1)||(c2==r2)||(r2==n); int sameedge=((c==1&&c2==1)||(c==r&&c2==r2)||(r==n&&r2==n)); if(!used[j]&&e2&&sameedge){regmask[nreg++]=bit(i)|bit(j);used[i]=used[j]=1;break;}}}
  for(int i=0;i<N;i++){ int r=R_[i],c=C_[i]; if(used[i])continue; int ok=1; u128 m=bit(i);
    for(int d=0;d<6;d++){int r2=r+dr[d],c2=c+dc[d]; if(c2<1||c2>r2||r2>n||used[idx[r2][c2]]||c2==1||c2==r2||r2==n){ok=0;break;} m|=bit(idx[r2][c2]);}
    if(ok){regmask[nreg++]=m; for(int j=0;j<N;j++) if(m>>j&1) used[j]=1;}}
  int unc=0; for(int i=0;i<N;i++) if(!used[i]) unc++;
  fprintf(stderr,"n=%d holes=%d jumps=%d regions=%d uncovered=%d B=%ld W=%d\n",n,N,nj,nreg,unc,B,W);
  u128 full=0; for(int i=0;i<N;i++) full|=bit(i);
  /* layer 0 */
  long *layer=malloc(sizeof(long)*1); long nl=0; hclear(1024); ncand=0;
  for(int i=0;i<N;i++){ if(sh>=0 && i!=sh) continue; u128 b=full&~bit(i); u128 c=canon(b); int*s=hslot(c); if(*s!=-1)continue; *s=0; char h[8];hname(i,h); char m[32]; sprintf(m,"start %s",h);
    layer=realloc(layer,sizeof(long)*(nl+1)); layer[nl++]=addst(b,-1,0,m);}
  for(int k=1;k<=maxm;k++){
    ncand=0; alen=0; hclear(B*PF*2+1024);
    for(long q=0;q<nl;q++){ curparent=layer[q]; u128 b=st[layer[q]].b;
      for(int p=0;p<N;p++) if(b>>p&1){ char h[8];hname(p,h); plen=sprintf(path,"%s",h); chain(b,p);} 
      if(ncand>B*PF){ /* prune mid-layer to bound memory */ qsort(cand,ncand,sizeof(Cand),cmpc); ncand=B*2; hclear(B*PF*2+1024); for(long i=0;i<ncand;i++){int*s=hslot(canon(cand[i].b));*s=i;} }
    }
    qsort(cand,ncand,sizeof(Cand),cmpc);
    long keep=ncand<B?ncand:B; int best=1<<30; long nb1=-1;
    nl=0; layer=realloc(layer,sizeof(long)*keep);
    for(long i=0;i<keep;i++){ long id=addst(cand[i].b,cand[i].parent,cand[i].key,arena+cand[i].mv); layer[nl++]=id; int pc=popc(cand[i].b); if(pc<best)best=pc; if(pc==1&&nb1<0)nb1=id; }
    fprintf(stderr,"layer %d: cand=%ld kept=%ld minpegs=%d keyrange=%d..%d\n",k,ncand,keep,best,keep?cand[0].key:-1,keep?cand[keep-1].key:-1);
    if(nb1>=0){ long chainv[200];int L=0; for(long x=nb1;x>=0;x=st[x].parent) chainv[L++]=x;
      printf("SOLVED n=%d moves=%d\n",n,k); for(int i=L-1;i>=0;i--) printf("%s%s",st[chainv[i]].mv,i==0?"\n":(i==L-1?"\n":", ")); fflush(stdout); return 0; }
    if(nl==0)break;
  }
  printf("NOT SOLVED within %d moves\n",maxm); return 1;
}
