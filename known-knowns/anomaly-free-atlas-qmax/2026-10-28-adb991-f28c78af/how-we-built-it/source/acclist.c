/* acclist.c -- explicit listing of inequivalent bounded integer solutions of the six ACCs
 * (all-left-handed basis, BRIEF.md), SM (5 species) or SMnuR (6 species).
 *
 * Usage: acclist QMAX NU(0|1) [COUNT_ONLY(0|1)] [MODE]   > stdout (pipe through gzip -1)
 * Output: one canonical solution per line, in strictly increasing lexicographic order.
 * MODE (alternative conventions, for hypothesis testing; default 0):
 *   0 = per-species permutations, sign identified, primitive (gcd 1), nonzero  [main convention]
 *   1 = as 0 but keep both signs (no sign identification)
 *   2 = as 0 but include non-primitive solutions (gcd > 1)
 *   3 = as 0 but also count/list the zero solution (all charges 0)
 *
 * Algorithm (meet in the middle):
 *   Linear ACCs give, with sQ = sum Q, sU = sum u:  sum d = -2sQ - sU, sum L = -3sQ, sum e = 2sQ - sU,
 *   sum nu = 4sQ + sU  (SM: sum nu = 0, i.e. sU = -4sQ).
 *   Half A = (Q,u,d), half B = (L,e,nu). Quadratic: quadA + quadB = 0 with quadA = Q2 - 2u2 + d2,
 *   quadB = -L2 + e2 (nu absent). Cubic: cubA + cubB = 0, cubA = 6Q3 + 3u3 + 3d3, cubB = 2L3 + e3 + nu3.
 *   For every block (sQ,sU) the B half is built once: all (L,e,nu) sorted triples with the
 *   required sums, sorted by (key, lex index). Half A is iterated in lex order (Q, then u, then d),
 *   and matching B entries come out in lex order, so the output is globally sorted.
 *   Canonical sign: F is kept iff F >= -F (lex, after re-sorting each species); decided at the first
 *   species whose triple is not symmetric under negation.
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <time.h>

typedef long long ll;
static int Q, NU, COUNT_ONLY, MODE;
static int NT;                 /* number of sorted triples */
static int *ta, *tb, *tc, *tsum, *tg, *tcmp; /* tcmp: sign of lex compare of triple vs its negation */
static ll *tsq, *tcu;
static int **byS; static int *nbyS;  /* triples with given sum, index s+3Q, in lex order */

typedef struct { ll key; int L, e, n; } Bent;
typedef struct { Bent *v; ll n; int built; } Block;
static Block *blocks; static int nSQ, nSU;
static ll totalB = 0;

static int gcd(int a, int b){ if(a<0)a=-a; if(b<0)b=-b; while(b){int t=a%b;a=b;b=t;} return a; }

static int cmpB(const void *x, const void *y){
  const Bent *a=x,*b=y;
  if(a->key!=b->key) return a->key<b->key?-1:1;
  if(a->L!=b->L) return a->L<b->L?-1:1;
  if(a->e!=b->e) return a->e<b->e?-1:1;
  if(a->n!=b->n) return a->n<b->n?-1:1;
  return 0;
}
static inline ll mkkey(ll quad, ll cub){ return quad*4294967296LL + cub; }
static int inrange(int s){ return s>=-3*Q && s<=3*Q; }

static Block *getblock(int sQ, int sU){
  Block *b=&blocks[(sQ+Q)*nSU + (sU+3*Q)];
  if(b->built) return b;
  b->built=1;
  int sL=-3*sQ, sE=2*sQ-sU, sN=4*sQ+sU;
  if(!NU) sN=0;
  if(!inrange(sL)||!inrange(sE)||(NU&&!inrange(sN))){ b->n=0; b->v=NULL; return b; }
  int *Ll=byS[sL+3*Q], nL=nbyS[sL+3*Q];
  int *El=byS[sE+3*Q], nE=nbyS[sE+3*Q];
  int *Nl=NULL, nN=1;
  if(NU){ Nl=byS[sN+3*Q]; nN=nbyS[sN+3*Q]; }
  ll cnt=(ll)nL*nE*nN;
  b->n=cnt; b->v = cnt? malloc(sizeof(Bent)*cnt):NULL;
  ll k=0;
  for(int i=0;i<nL;i++){int l=Ll[i];
    for(int j=0;j<nE;j++){int e=El[j];
      ll quad=-tsq[l]+tsq[e]; ll cb=2*tcu[l]+tcu[e];
      for(int m=0;m<nN;m++){int n= NU? Nl[m] : -1;
        Bent *x=&b->v[k++]; x->L=l; x->e=e; x->n=n;
        x->key=mkkey(quad, cb + (NU? tcu[n]:0));
      }}}
  qsort(b->v,cnt,sizeof(Bent),cmpB);
  totalB+=cnt;
  return b;
}

/* output buffer */
static char obuf[1<<20]; static int opos=0;
static inline void flushout(void){ fwrite(obuf,1,opos,stdout); opos=0; }
static inline void putint(int x){
  if(x<0){obuf[opos++]='-'; x=-x;}
  if(x>=10){ obuf[opos++]='0'+x/10; obuf[opos++]='0'+x%10; }
  else obuf[opos++]='0'+x;
}
static inline void puttrip(int t, int first){
  if(!first) obuf[opos++]=' ';
  putint(ta[t]); obuf[opos++]=' '; putint(tb[t]); obuf[opos++]=' '; putint(tc[t]);
}

int main(int argc, char **argv){
  if(argc<3){fprintf(stderr,"usage: acclist QMAX NU [COUNT_ONLY] [MODE]\n");return 1;}
  Q=atoi(argv[1]); NU=atoi(argv[2]); COUNT_ONLY=argc>3?atoi(argv[3]):0; MODE=argc>4?atoi(argv[4]):0;
  if(Q>99){fprintf(stderr,"Q too big for putint\n");return 1;}
  time_t t0=time(NULL);
  int W=2*Q+1; int maxT=W*W*W;
  ta=malloc(sizeof(int)*maxT); tb=malloc(sizeof(int)*maxT); tc=malloc(sizeof(int)*maxT);
  tsum=malloc(sizeof(int)*maxT); tg=malloc(sizeof(int)*maxT); tcmp=malloc(sizeof(int)*maxT);
  tsq=malloc(sizeof(ll)*maxT); tcu=malloc(sizeof(ll)*maxT);
  NT=0;
  for(int a=-Q;a<=Q;a++)for(int b=a;b<=Q;b++)for(int c=b;c<=Q;c++){
    ta[NT]=a;tb[NT]=b;tc[NT]=c;tsum[NT]=a+b+c;tg[NT]=gcd(gcd(a,b),c);
    tsq[NT]=(ll)a*a+(ll)b*b+(ll)c*c; tcu[NT]=(ll)a*a*a+(ll)b*b*b+(ll)c*c*c;
    int na=-c,nb=-b,nc=-a; int r=0;
    if(a!=na) r=a>na?1:-1; else if(b!=nb) r=b>nb?1:-1; else if(c!=nc) r=c>nc?1:-1;
    tcmp[NT]=r; NT++;
  }
  int nS=6*Q+1;
  byS=calloc(nS,sizeof(int*)); nbyS=calloc(nS,sizeof(int));
  for(int t=0;t<NT;t++) nbyS[tsum[t]+3*Q]++;
  for(int s=0;s<nS;s++){ byS[s]=malloc(sizeof(int)*(nbyS[s]+1)); nbyS[s]=0; }
  for(int t=0;t<NT;t++){ int s=tsum[t]+3*Q; byS[s][nbyS[s]++]=t; }
  nSQ=2*Q+1; nSU=6*Q+1;
  blocks=calloc((size_t)nSQ*nSU,sizeof(Block));
  fprintf(stderr,"Q=%d NU=%d MODE=%d triples=%d\n",Q,NU,MODE,NT);

  ll count=0, rawA=0;
  for(int qi=0;qi<NT;qi++){
    int cQ=tcmp[qi];
    if(cQ<0 && MODE!=1) continue;
    int sQ=tsum[qi];
    if(sQ<-Q||sQ>Q) continue;            /* sum L = -3 sQ must be reachable */
    for(int ui=0;ui<NT;ui++){
      int sU=tsum[ui];
      if(!NU && sU!=-4*sQ) continue;
      int sD=-2*sQ-sU, sE=2*sQ-sU, sN=4*sQ+sU;
      if(!inrange(sD)||!inrange(sE)||(NU&&!inrange(sN))) continue;
      int cU = cQ!=0? cQ : tcmp[ui];
      if(cU<0 && MODE!=1) continue;
      Block *B=getblock(sQ,sU);
      if(B->n==0) continue;
      int gQU=gcd(tg[qi],tg[ui]);
      ll qQU=tsq[qi]-2*tsq[ui], cQU=6*tcu[qi]+3*tcu[ui];
      int *Dl=byS[sD+3*Q], nD=nbyS[sD+3*Q];
      for(int di=0;di<nD;di++){
        int d=Dl[di];
        int cD = cU!=0? cU : tcmp[d];
        if(cD<0 && MODE!=1) continue;
        rawA++;
        ll want=mkkey(-(qQU+tsq[d]), -(cQU+3*tcu[d]));
        /* lower bound */
        ll lo=0,hi=B->n;
        while(lo<hi){ ll mid=(lo+hi)>>1; if(B->v[mid].key<want) lo=mid+1; else hi=mid; }
        int gQUD=gcd(gQU,tg[d]);
        for(ll k=lo;k<B->n && B->v[k].key==want;k++){
          Bent *x=&B->v[k];
          int c=cD;
          if(c==0) c=tcmp[x->L];
          if(c==0) c=tcmp[x->e];
          if(c==0 && NU) c=tcmp[x->n];
          if(c<0 && MODE!=1) continue;
          int g=gcd(gQUD,gcd(tg[x->L],tg[x->e])); if(NU) g=gcd(g,tg[x->n]);
          if(g==0 && MODE!=3) continue;     /* zero solution */
          if(g!=1 && MODE!=2 && !(MODE==3 && g==0)) continue;
          count++;
          if(!COUNT_ONLY){
            puttrip(qi,1); puttrip(ui,0); puttrip(d,0); puttrip(x->L,0); puttrip(x->e,0);
            if(NU) puttrip(x->n,0);
            obuf[opos++]='\n';
            if(opos > (1<<20)-200) flushout();
          }
        }
      }
    }
    if((qi & 63)==0) fprintf(stderr,"progress Qtriple %d/%d count=%lld Bentries=%lld elapsed=%lds\n",
                             qi,NT,count,totalB,(long)(time(NULL)-t0));
  }
  if(!COUNT_ONLY) flushout();
  fflush(stdout);
  fprintf(stderr,"DONE Q=%d NU=%d MODE=%d count=%lld rawA=%lld Bentries=%lld Bbytes=%lld elapsed=%lds\n",
          Q,NU,MODE,count,rawA,totalB,totalB*(ll)sizeof(Bent),(long)(time(NULL)-t0));
  return 0;
}
