/* slpopt: randomized iterated pair-greedy CSE for a ternary linear map (rows = target forms).
   usage: slpopt in.mat out.graph seed seconds [eps] [log_every_s]
   in.mat : "k N" then k*N integers in {-1,0,1}
   out.graph: best program found, as a linear graph:
     G N K M
     n d src sgn ... (M internal nodes, ids N..N+M-1, topological)
     o d src sgn ... (K sinks, one per input row, in order)
   cost = sum over internal and sink vertices of (d-1).  Written by opus-add (addcomp). */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <sys/time.h>

static double now(void){ struct timeval t; gettimeofday(&t,0); return t.tv_sec+1e-6*t.tv_usec; }
static unsigned long long rs;
static inline unsigned long long rnd(void){ rs ^= rs<<13; rs ^= rs>>7; rs ^= rs<<17; return rs; }
static inline int rndint(int n){ return (int)(rnd()%(unsigned long long)n); }
static inline double rnd01(void){ return (rnd()>>11)*(1.0/9007199254740992.0); }

static int K, N;            /* original rows, cols */
static signed char *X;      /* K x N */
static int D;               /* distinct nontrivial rows */
static int *drow_of;        /* K: index of distinct row, or -1 trivial (single input), -2 zero */
static int *dsign;          /* sign relation original = sign * distinct */
static int *triv_var, *triv_sign;
static signed char *DX;     /* D x N distinct rows (canonical sign: first nonzero positive) */
static int VMAX;

/* working state */
static int *rl;     /* row lengths */
static int *rv;     /* D x VMAX vars */
static signed char *rsg; /* D x VMAX signs */
static int *defa, *defb, *defs; /* new var defs */
static int nnew;
static int *cnt;    /* VMAX*VMAX*2 */
static int *touched; static int ntouched;
static int *cand; /* candidate triples */

static int *bestA, *bestB, *bestS, bestN, bestCost;
static int *curA, *curB, *curS;

static int greedy(int *fa, int *fb, int *fs, int nforced, double eps){
    /* reset rows */
    for(int d=0; d<D; d++){ int L=0; for(int j=0;j<N;j++) if(DX[d*N+j]){ rv[d*VMAX+L]=j; rsg[d*VMAX+L]=DX[d*N+j]; L++; } rl[d]=L; }
    nnew=0; int nv=N; int fi=0;
    while(nv < VMAX){
        int a=-1,b=-1,s=0;
        if(fi < nforced){
            a=fa[fi]; b=fb[fi]; s=fs[fi]; fi++;
            if(a>=nv||b>=nv) continue;
            int hits=0;
            for(int d=0; d<D; d++){ int ia=-1, ib=-1; for(int t=0;t<rl[d];t++){ if(rv[d*VMAX+t]==a) ia=t; else if(rv[d*VMAX+t]==b) ib=t; }
                if(ia>=0&&ib>=0&& rsg[d*VMAX+ib]*rsg[d*VMAX+ia]==s) hits++; }
            if(hits<2) continue;
        } else {
            int best=1; ntouched=0;
            for(int d=0; d<D; d++){ int L=rl[d]; int *v=rv+d*VMAX; signed char *g=rsg+d*VMAX;
                for(int p=0;p<L;p++) for(int q=p+1;q<L;q++){ int x=v[p], y=v[q]; int sg = (g[p]==g[q])?0:1; if(x>y){int t=x;x=y;y=t;}
                    int id=(x*VMAX+y)*2+sg; if(cnt[id]==0) touched[ntouched++]=id; cnt[id]++; if(cnt[id]>best) best=cnt[id]; } }
            if(best<2){ for(int i=0;i<ntouched;i++) cnt[touched[i]]=0; break; }
            int thr=best; if(best>2 && rnd01()<eps) thr=best-1;
            int nc=0;
            for(int i=0;i<ntouched;i++){ int id=touched[i]; if(cnt[id]>=thr) cand[nc++]=id; cnt[id]=0; }
            int id=cand[rndint(nc)];
            s = (id&1)? -1: 1; int xy=id>>1; a=xy/VMAX; b=xy%VMAX;
        }
        /* new var t = x_a + s*x_b */
        int t=nv++; defa[nnew]=a; defb[nnew]=b; defs[nnew]=s; nnew++;
        for(int d=0; d<D; d++){ int L=rl[d]; int *v=rv+d*VMAX; signed char *g=rsg+d*VMAX; int ia=-1, ib=-1;
            for(int p=0;p<L;p++){ if(v[p]==a) ia=p; else if(v[p]==b) ib=p; }
            if(ia<0||ib<0||g[ib]*g[ia]!=s) continue;
            int sa=g[ia];
            /* remove ia, ib; append t with sign sa */
            int w=0; for(int p=0;p<L;p++){ if(p==ia||p==ib) continue; v[w]=v[p]; g[w]=g[p]; w++; }
            v[w]=t; g[w]=sa; w++; rl[d]=w; }
    }
    int c=nnew; for(int d=0; d<D; d++) c += rl[d]-1;
    return c;
}

static void write_graph(const char *path){
    /* rerun best forced sequence fully to rebuild state */
    int c = greedy(bestA,bestB,bestS,bestN,0.0);
    if(c!=bestCost){ fprintf(stderr,"rebuild mismatch %d vs %d\n", c, bestCost); }
    /* internal nodes: new vars (ids N..N+nnew-1), then row vertices for distinct rows with L>=2 */
    int *rowvert = malloc(sizeof(int)*D); int *rowsign = malloc(sizeof(int)*D);
    int M = nnew; for(int d=0; d<D; d++){ if(rl[d]>=2){ rowvert[d]=N+M; rowsign[d]=1; M++; } else { rowvert[d]=rv[d*VMAX]; rowsign[d]=rsg[d*VMAX]; } }
    FILE *f=fopen(path,"w");
    fprintf(f,"G %d %d %d\n", N, K, M);
    for(int i=0;i<nnew;i++) fprintf(f,"n 2 %d 1 %d %d\n", defa[i], defb[i], defs[i]);
    for(int d=0; d<D; d++) if(rl[d]>=2){ fprintf(f,"n %d", rl[d]); for(int p=0;p<rl[d];p++) fprintf(f," %d %d", rv[d*VMAX+p], rsg[d*VMAX+p]); fprintf(f,"\n"); }
    for(int k=0;k<K;k++){
        if(drow_of[k]==-1) fprintf(f,"o 1 %d %d\n", triv_var[k], triv_sign[k]);
        else if(drow_of[k]==-2) fprintf(f,"o 0\n");
        else { int d=drow_of[k]; fprintf(f,"o 1 %d %d\n", rowvert[d], rowsign[d]*dsign[k]); }
    }
    fclose(f); free(rowvert); free(rowsign);
}

int main(int argc, char **argv){
    if(argc<5){ fprintf(stderr,"usage\n"); return 1; }
    FILE *f=fopen(argv[1],"r"); if(!f) return 1;
    if(fscanf(f,"%d %d",&K,&N)!=2) return 1;
    X=malloc(K*N); for(int i=0;i<K*N;i++){ int v; if(fscanf(f,"%d",&v)!=1) return 1; X[i]=(signed char)v; } fclose(f);
    rs = 0x9E3779B97F4A7C15ULL ^ (unsigned long long)atoll(argv[3])*2654435761ULL; for(int i=0;i<10;i++) rnd();
    double secs=atof(argv[4]); double eps = argc>5? atof(argv[5]) : -1; double logev = argc>6? atof(argv[6]) : 30;
    /* dedupe */
    drow_of=malloc(sizeof(int)*K); dsign=malloc(sizeof(int)*K); triv_var=malloc(sizeof(int)*K); triv_sign=malloc(sizeof(int)*K);
    DX=malloc(K*N); D=0; int nnz=0;
    for(int k=0;k<K;k++){ int L=0, first=-1; for(int j=0;j<N;j++) if(X[k*N+j]){ L++; if(first<0) first=j; }
        if(L==0){ drow_of[k]=-2; continue; }
        if(L==1){ drow_of[k]=-1; triv_var[k]=first; triv_sign[k]=X[k*N+first]; continue; }
        int sg = X[k*N+first]>0?1:-1; int found=-1;
        for(int d=0; d<D; d++){ int eq=1; for(int j=0;j<N;j++) if(DX[d*N+j]!=sg*X[k*N+j]){eq=0;break;} if(eq){found=d;break;} }
        if(found<0){ for(int j=0;j<N;j++) DX[D*N+j]=sg*X[k*N+j]; found=D++; nnz+=L; }
        drow_of[k]=found; dsign[k]=sg; }
    VMAX = N + nnz + 2;
    rl=malloc(sizeof(int)*D); rv=malloc(sizeof(int)*D*VMAX); rsg=malloc(D*VMAX);
    defa=malloc(sizeof(int)*VMAX); defb=malloc(sizeof(int)*VMAX); defs=malloc(sizeof(int)*VMAX);
    cnt=calloc((size_t)VMAX*VMAX*2,sizeof(int));
    { size_t pb=16; for(int d=0; d<D; d++){ size_t L=0; for(int j=0;j<N;j++) if(DX[d*N+j]) L++; pb+=L*(L-1)/2; }
      touched=malloc(sizeof(int)*pb); cand=malloc(sizeof(int)*pb); }
    bestA=malloc(sizeof(int)*VMAX); bestB=malloc(sizeof(int)*VMAX); bestS=malloc(sizeof(int)*VMAX);
    curA=malloc(sizeof(int)*VMAX); curB=malloc(sizeof(int)*VMAX); curS=malloc(sizeof(int)*VMAX);
    double t0=now(), tl=t0+logev; long iters=0;
    bestCost=1<<30; bestN=0;
    double epsset[4]={0.0,0.05,0.15,0.3};
    while(1){
        double e = eps>=0? eps : epsset[rndint(4)];
        int nf = 0;
        if(bestN>0 && rnd01()>0.05) nf = rndint(bestN);
        int c = greedy(bestA,bestB,bestS,nf,e);
        iters++;
        if(c<=bestCost){
            if(c<bestCost){ fprintf(stderr,"[%.1fs] it %ld cost %d\n", now()-t0, iters, c); }
            bestCost=c; bestN=nnew; memcpy(bestA,defa,sizeof(int)*nnew); memcpy(bestB,defb,sizeof(int)*nnew); memcpy(bestS,defs,sizeof(int)*nnew);
        }
        double tn=now();
        if(tn>tl){ write_graph(argv[2]); tl=tn+logev; }
        if(tn-t0>secs) break;
    }
    write_graph(argv[2]);
    printf("best %d iters %ld K %d N %d D %d\n", bestCost, iters, K, N, D);
    return 0;
}
