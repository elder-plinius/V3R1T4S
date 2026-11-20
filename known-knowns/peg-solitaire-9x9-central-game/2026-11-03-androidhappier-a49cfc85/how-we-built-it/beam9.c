/* Beam search over MOVES for 9x9 square peg solitaire (orthogonal jumps only).
   Board bit index i = r*9+c, r=0..8 is row 1..9, c=0..8 is column a..i. Centre e5 = index 40.
   Layer k = boards reachable in k moves (a move = any nonempty chain of jumps by one peg; every prefix is a child).
   key = 4*(W*filled_regions + pegs + V*isolated_pegs + E*edge_pegs) (+ seed noise), computed on the D4-canonical board.
   Keep top B distinct canonical boards per layer. Success = exactly one peg, at TARGET (default 40).
   usage: beam9 B W [maxmoves]   env: BEAM_V, BEAM_E, BEAM_SEED, START=<81 chars 0/1 row1 a..i first>, TARGET */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
typedef unsigned __int128 u128;
#define N 81
static int nj, jo[400], jt[400], jstart[N], jcnt[N];
static int perm[8][N]; static int nreg; static u128 regmask[64]; static u128 nbm[N], edgem;
static int W, V=0, E=0; static unsigned seed=0; static long PF=8; static int TARGET=40;
static inline int popc(u128 x){return __builtin_popcountll((uint64_t)x)+__builtin_popcountll((uint64_t)(x>>64));}
static inline u128 bit(int i){return ((u128)1)<<i;}
static u128 xform(u128 b,int s){u128 r=0; while(b){int i; uint64_t lo=(uint64_t)b; if(lo){i=__builtin_ctzll(lo);} else {i=64+__builtin_ctzll((uint64_t)(b>>64));} b&=~bit(i); r|=bit(perm[s][i]);} return r;}
static u128 canon(u128 b){u128 m=b;for(int s=1;s<8;s++){u128 t=xform(b,s);if(t<m)m=t;}return m;}
static int filled(u128 b){int f=0;for(int r=0;r<nreg;r++) if((b&regmask[r])==regmask[r]) f++;return f;}
typedef struct {u128 b; long parent; char *mv;} St;
static St *st; static long nst,cap;
static long addst(u128 b,long parent,const char*mv){ if(nst==cap){cap=cap?cap*2:1<<20; st=realloc(st,cap*sizeof(St));}
  st[nst].b=b;st[nst].parent=parent;st[nst].mv=strdup(mv);return nst++;}
static u128 *hk; static long *hv; static long hcap;
static void hclear(long need){ long c=1; while(c<need*2)c<<=1; if(c!=hcap){free(hk);free(hv);hcap=c;hk=malloc(c*sizeof(u128));hv=malloc(c*sizeof(long));}
  memset(hv,-1,hcap*sizeof(long)); }
static long *hslot(u128 k){ uint64_t h=(uint64_t)k*0x9E3779B97F4A7C15ULL ^ (uint64_t)(k>>64)*0xC2B2AE3D27D4EB4FULL; long i=(h^(h>>29))&(hcap-1);
  while(hv[i]!=-1 && hk[i]!=k) i=(i+1)&(hcap-1); hk[i]=k; return &hv[i]; }
static void hname(int i,char*o){sprintf(o,"%c%d",'a'+i%9,i/9+1);}
typedef struct {u128 b; long parent; int key; long mv;} Cand;
static char *arena; static long alen,acap;
static long astr(const char*m){long L=strlen(m)+1; if(alen+L>acap){acap=acap?acap*2:1<<24; while(alen+L>acap)acap*=2; arena=realloc(arena,acap);} memcpy(arena+alen,m,L); long o=alen; alen+=L; return o;}
static Cand *cand; static long ncand,ccap; static long B;
static int cmpc(const void*a,const void*b){int x=((Cand*)a)->key,y=((Cand*)b)->key;return x<y?-1:x>y;}
static void push(u128 b,long parent,const char*mv){
  u128 c=canon(b); long *s=hslot(c);
  int iso=0; if(V){ u128 t=c; for(int i=0;i<N;i++) if((t>>i&1) && !(t&nbm[i])) iso++; }
  int key=4*(W*filled(c)+popc(c)+V*iso+E*popc(c&edgem));
  if(seed){uint64_t h=(uint64_t)c*(0x9E3779B97F4A7C15ULL+seed) ^ (uint64_t)(c>>64)*0xD6E8FEB86659FD93ULL; h^=h>>31; key+=(int)(h&3);}
  if(*s!=-1){ if(cand[*s].key<=key) return; cand[*s].b=b;cand[*s].parent=parent;cand[*s].key=key;cand[*s].mv=astr(mv);return;}
  if(ncand==ccap){ccap=ccap?ccap*2:1<<20;cand=realloc(cand,ccap*sizeof(Cand));}
  *s=ncand; cand[ncand].b=b;cand[ncand].parent=parent;cand[ncand].key=key;cand[ncand].mv=astr(mv);ncand++;
}
static long curparent; static char path[1024]; static int plen;
static void chain(u128 b,int pos){
  for(int k=jstart[pos];k<jstart[pos]+jcnt[pos];k++){ int o=jo[k],t=jt[k];
    if((b>>o&1) && !(b>>t&1)){ u128 nb=(b&~bit(pos)&~bit(o))|bit(t); int sv=plen; char h[8]; hname(t,h);
      plen+=sprintf(path+plen,"-%s",h); if(plen<1000){ push(nb,curparent,path); chain(nb,t);} plen=sv; path[plen]=0; } }
}
int main(int argc,char**argv){
  B=atol(argv[1]); W=atoi(argv[2]); int maxm=argc>3?atoi(argv[3]):60;
  if(getenv("BEAM_V"))V=atoi(getenv("BEAM_V")); if(getenv("BEAM_E"))E=atoi(getenv("BEAM_E"));
  if(getenv("BEAM_SEED"))seed=atoi(getenv("BEAM_SEED")); if(getenv("TARGET"))TARGET=atoi(getenv("TARGET"));
  int dr[4]={0,0,1,-1},dc[4]={1,-1,0,0};
  for(int i=0;i<N;i++){int r=i/9,c=i%9; jstart[i]=nj;jcnt[i]=0; nbm[i]=0;
    for(int d=0;d<4;d++){int r1=r+dr[d],c1=c+dc[d],r2=r+2*dr[d],c2=c+2*dc[d];
      if(r1>=0&&r1<9&&c1>=0&&c1<9) nbm[i]|=bit(r1*9+c1);
      if(r2>=0&&r2<9&&c2>=0&&c2<9){jo[nj]=r1*9+c1;jt[nj]=r2*9+c2;nj++;jcnt[i]++;}}
    if(r==0||r==8||c==0||c==8) edgem|=bit(i);}
  for(int s=0;s<8;s++)for(int i=0;i<N;i++){int r=i/9,c=i%9,x=c,y=r;
    if(s&4){int t=x;x=y;y=t;} if(s&1)x=8-x; if(s&2)y=8-y; perm[s][i]=y*9+x;}
  /* Merson-type regions (pegs inside can only be removed by a move starting inside when region is full):
     2x2 blocks on rows/cols {0-1,2-3,4-5,6-7}, edge pairs on row 8 and col 8, single corner (8,8). */
  for(int R=0;R<8;R+=2)for(int C=0;C<8;C+=2) regmask[nreg++]=bit(R*9+C)|bit(R*9+C+1)|bit((R+1)*9+C)|bit((R+1)*9+C+1);
  for(int C=0;C<8;C+=2) regmask[nreg++]=bit(8*9+C)|bit(8*9+C+1);
  for(int R=0;R<8;R+=2) regmask[nreg++]=bit(R*9+8)|bit((R+1)*9+8);
  regmask[nreg++]=bit(80);
  u128 full=0; for(int i=0;i<N;i++) full|=bit(i);
  u128 b0=full&~bit(40); const char*S=getenv("START");
  if(S){ b0=0; for(int i=0;i<N;i++) if(S[i]=='1') b0|=bit(i); }
  fprintf(stderr,"jumps=%d regions=%d B=%ld W=%d V=%d E=%d seed=%u start_pegs=%d target=%d\n",nj,nreg,B,W,V,E,seed,popc(b0),TARGET);
  long *layer=malloc(sizeof(long)); long nl=0; layer[nl++]=addst(b0,-1,"start");
  for(int k=1;k<=maxm;k++){
    ncand=0; alen=0; hclear(B*PF*2+1024);
    for(long q=0;q<nl;q++){ curparent=layer[q]; u128 b=st[layer[q]].b;
      for(int p=0;p<N;p++) if(b>>p&1){ char h[8];hname(p,h); plen=sprintf(path,"%s",h); chain(b,p);}
      if(ncand>B*PF){ qsort(cand,ncand,sizeof(Cand),cmpc); ncand=B*2; hclear(B*PF*2+1024); for(long i=0;i<ncand;i++){long*s=hslot(canon(cand[i].b));*s=i;} }
    }
    qsort(cand,ncand,sizeof(Cand),cmpc);
    long keep=ncand<B?ncand:B; int best=1<<30; long nb1=-1;
    nl=0; layer=realloc(layer,sizeof(long)*(keep+1));
    for(long i=0;i<keep;i++){ int pc=popc(cand[i].b); if(pc<best)best=pc;
      if(pc==1 && !((cand[i].b>>TARGET)&1)) { /* single peg off-centre: dead end for central game, drop */ continue; }
      long id=addst(cand[i].b,cand[i].parent,arena+cand[i].mv); layer[nl++]=id; if(pc==1&&nb1<0)nb1=id; }
    fprintf(stderr,"layer %d: cand=%ld kept=%ld minpegs=%d keyrange=%d..%d\n",k,ncand,nl,best,keep?cand[0].key:-1,keep?cand[keep-1].key:-1);
    if(nb1>=0){ long cv[200];int L=0; for(long x=nb1;x>=0;x=st[x].parent) cv[L++]=x;
      printf("SOLVED moves=%d\n",k); for(int i=L-2;i>=0;i--) printf("%s\n",st[cv[i]].mv); fflush(stdout); return 0; }
    if(nl==0)break;
  }
  printf("NOT SOLVED within %d moves\n",maxm); return 1;
}
