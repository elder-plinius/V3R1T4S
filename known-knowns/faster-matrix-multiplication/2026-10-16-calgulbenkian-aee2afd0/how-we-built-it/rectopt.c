/* rectopt: randomized iterated RECTANGLE-greedy CSE for a ternary linear map (rows = target forms).
   A rectangle is a row set R and a signed column set C with M[r,c] = sigma_r * tau_c for all r in R, c in C.
   Extracting it creates s = sum_c tau_c x_c (|C|-1 additions) and replaces M[r,C] by sigma_r * s:
   saving (|R|-1)(|C|-1). Column pairs (|C|=2) are classic pair CSE; row pairs (|R|=2) are what pair CSE on the
   transposed map finds. usage: rectopt in.mat out.graph seed seconds [eps] [log_every_s]
   output format as slpopt. Written by opus-add (addcomp). */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/time.h>

static double now(void){ struct timeval t; gettimeofday(&t,0); return t.tv_sec+1e-6*t.tv_usec; }
static unsigned long long rs;
static inline unsigned long long rnd(void){ rs ^= rs<<13; rs ^= rs>>7; rs ^= rs<<17; return rs; }
static inline int rndint(int n){ return (int)(rnd()%(unsigned long long)n); }
static inline double rnd01(void){ return (rnd()>>11)*(1.0/9007199254740992.0); }

static int K, N, D, VMAX;
static signed char *X, *DX;
static int *drow_of, *dsign, *triv_var, *triv_sign;
static int *rl, *rv; static signed char *rsg; static signed char *dense; /* D x VMAX */
static int *occ, *occn; /* VMAX x D */
static int *cnt, *touched, ntouched;
/* step records */
static int *stC, *stT, *stLen, *stOff, nst, stUsed; /* C vars, tau signs, per step */
static int *bstC, *bstT, *bstLen, *bstOff, bnst, bstUsed, bestCost;
static int *tmpR, *tmpS, *tmpC, *tmpT, *bR, *bS, *bC, *bT;

static void load_rows(void){
    memset(dense,0,(size_t)D*VMAX);
    for(int d=0; d<D; d++){ int L=0; for(int j=0;j<N;j++) if(DX[d*N+j]){ rv[d*VMAX+L]=j; rsg[d*VMAX+L]=DX[d*N+j]; dense[(size_t)d*VMAX+j]=DX[d*N+j]; L++; } rl[d]=L; }
}
static void build_occ(int nv){
    for(int v=0; v<nv; v++) occn[v]=0;
    for(int d=0; d<D; d++) for(int t=0;t<rl[d];t++){ int v=rv[d*VMAX+t]; occ[(size_t)v*D+occn[v]++]=d; }
}
/* rows consistent with signed column set (C,T): returns count, fills R,S */
static int rows_for(int *C, int *T, int nc, int *R, int *S){
    int c0=C[0]; for(int i=1;i<nc;i++) if(occn[C[i]]<occn[c0]) c0=C[i];
    int i0=0; for(int i=0;i<nc;i++) if(C[i]==c0) i0=i;
    int nr=0;
    for(int k=0;k<occn[c0];k++){ int r=occ[(size_t)c0*D+k]; signed char *dr=dense+(size_t)r*VMAX; int sg=dr[c0]*T[i0]; int ok=1;
        for(int i=0;i<nc;i++) if(dr[C[i]]!=sg*T[i]){ ok=0; break; }
        if(ok){ R[nr]=r; S[nr]=sg; nr++; } }
    return nr;
}
static int apply(int *C, int *T, int nc, int nv){
    int nr=rows_for(C,T,nc,tmpR,tmpS);
    if(nr<2) return 0;
    int s=nv;
    for(int k=0;k<nr;k++){ int r=tmpR[k]; int *v=rv+r*VMAX; signed char *g=rsg+r*VMAX; signed char *dr=dense+(size_t)r*VMAX; int w=0;
        for(int p=0;p<rl[r];p++){ if(dr[v[p]] && ({int in=0; for(int i=0;i<nc;i++) if(C[i]==v[p]){in=1;break;} in;})) continue; v[w]=v[p]; g[w]=g[p]; w++; }
        for(int i=0;i<nc;i++) dr[C[i]]=0;
        v[w]=s; g[w]=tmpS[k]; dr[s]=tmpS[k]; w++; rl[r]=w; }
    stOff[nst]=stUsed; stLen[nst]=nc; for(int i=0;i<nc;i++){ stC[stUsed+i]=C[i]; stT[stUsed+i]=T[i]; } stUsed+=nc; nst++;
    return 1;
}

static int greedy(int nforced, double eps, int rowpairs){
    load_rows(); nst=0; stUsed=0; int nv=N;
    for(int f=0; f<nforced && nv<VMAX; f++){
        int nc=bstLen[f]; int *C=bstC+bstOff[f], *T=bstT+bstOff[f]; int ok=1;
        for(int i=0;i<nc;i++) if(C[i]>=nv) ok=0;
        if(!ok) continue;
        build_occ(nv);
        if(apply(C,T,nc,nv)) nv++;
    }
    while(nv<VMAX){
        build_occ(nv);
        int bestv=0, nb=0; /* reservoir among best */
        /* column pairs */
        ntouched=0; int maxc=1;
        for(int d=0; d<D; d++){ int L=rl[d]; int *v=rv+d*VMAX; signed char *g=rsg+d*VMAX;
            for(int p=0;p<L;p++) for(int q=p+1;q<L;q++){ int x=v[p], y=v[q]; int sg=(g[p]==g[q])?0:1; if(x>y){int t=x;x=y;y=t;}
                int id=(x*VMAX+y)*2+sg; if(cnt[id]==0) touched[ntouched++]=id; cnt[id]++; if(cnt[id]>maxc) maxc=cnt[id]; } }
        int thrc = (maxc>2 && rnd01()<eps)? maxc-1 : maxc;
        /* evaluate column-pair rectangles with count >= 2 (expand C over its rows) */
        for(int i=0;i<ntouched;i++){ int id=touched[i]; int c=cnt[id]; cnt[id]=0; if(c<2) continue;
            if(c < thrc && c < 3) continue; /* cheap prune: small pairs only matter when they are the max */
            int s=(id&1)?-1:1; int xy=id>>1; int a=xy/VMAX, b=xy%VMAX;
            int C2[2]={a,b}, T2[2]={1,s};
            int nr=rows_for(C2,T2,2,tmpR,tmpS);
            /* expand C: columns of first row consistent in all rows */
            int nc=0; int r0=tmpR[0]; signed char *d0=dense+(size_t)r0*VMAX;
            tmpC[nc]=a; tmpT[nc]=1; nc++; tmpC[nc]=b; tmpT[nc]=s; nc++;
            for(int p=0;p<rl[r0];p++){ int c2=rv[r0*VMAX+p]; if(c2==a||c2==b) continue; int tau=d0[c2]*tmpS[0]; int ok=1;
                for(int k=1;k<nr;k++){ if(dense[(size_t)tmpR[k]*VMAX+c2]!=tmpS[k]*tau){ok=0;break;} }
                if(ok){ tmpC[nc]=c2; tmpT[nc]=tau; nc++; } }
            int val=(nr-1)*(nc-1);
            if(val>bestv){ bestv=val; nb=0; }
            if(val==bestv && val>0){ nb++; if(rndint(nb)==0){ memcpy(bC,tmpC,sizeof(int)*nc); memcpy(bT,tmpT,sizeof(int)*nc); bC[VMAX]=nc; } }
        }
        /* row pairs with >= 3 consistent common columns */
        if(rowpairs) for(int i=0;i<D;i++){ int Li=rl[i]; if(Li<3) continue; int *vi=rv+i*VMAX; signed char *gi=rsg+i*VMAX;
            for(int j=i+1;j<D;j++){ if(rl[j]<3) continue; signed char *dj=dense+(size_t)j*VMAX; int np=0, nm=0;
                for(int p=0;p<Li;p++){ int c=vi[p]; if(dj[c]){ if(dj[c]==gi[p]) np++; else nm++; } }
                for(int pass=0; pass<2; pass++){ int want = pass? nm: np; if(want<3) continue;
                    int nc=0; for(int p=0;p<Li;p++){ int c=vi[p]; if(dj[c] && ((dj[c]==gi[p])==(pass==0))){ tmpC[nc]=c; tmpT[nc]=gi[p]; nc++; } }
                    /* quick upper bound check: value >= (2-1)(nc-1) */
                    int nr=rows_for(tmpC,tmpT,nc,tmpR,tmpS);
                    int val=(nr-1)*(nc-1);
                    if(val>bestv){ bestv=val; nb=0; }
                    if(val==bestv && val>0){ nb++; if(rndint(nb)==0){ memcpy(bC,tmpC,sizeof(int)*nc); memcpy(bT,tmpT,sizeof(int)*nc); bC[VMAX]=nc; } }
                } } }
        if(bestv<1) break;
        if(!apply(bC,bT,bC[VMAX],nv)) break;
        nv++;
    }
    int c=0; for(int s=0;s<nst;s++) c+=stLen[s]-1; for(int d=0; d<D; d++) c+=rl[d]-1;
    return c;
}

static void write_graph(const char *path, int rowpairs){
    int c=greedy(bnst,0.0,rowpairs);
    if(c!=bestCost) fprintf(stderr,"rebuild mismatch %d vs %d\n",c,bestCost);
    int *rowvert=malloc(sizeof(int)*D), *rowsign=malloc(sizeof(int)*D);
    int M=nst; for(int d=0; d<D; d++){ if(rl[d]>=2){ rowvert[d]=N+M; rowsign[d]=1; M++; } else { rowvert[d]=rv[d*VMAX]; rowsign[d]=rsg[d*VMAX]; } }
    FILE *f=fopen(path,"w"); fprintf(f,"G %d %d %d\n",N,K,M);
    for(int s=0;s<nst;s++){ fprintf(f,"n %d",stLen[s]); for(int i=0;i<stLen[s];i++) fprintf(f," %d %d",stC[stOff[s]+i],stT[stOff[s]+i]); fprintf(f,"\n"); }
    for(int d=0; d<D; d++) if(rl[d]>=2){ fprintf(f,"n %d",rl[d]); for(int p=0;p<rl[d];p++) fprintf(f," %d %d",rv[d*VMAX+p],rsg[d*VMAX+p]); fprintf(f,"\n"); }
    for(int k=0;k<K;k++){ if(drow_of[k]==-1) fprintf(f,"o 1 %d %d\n",triv_var[k],triv_sign[k]); else if(drow_of[k]==-2) fprintf(f,"o 0\n");
        else { int d=drow_of[k]; fprintf(f,"o 1 %d %d\n",rowvert[d],rowsign[d]*dsign[k]); } }
    fclose(f); free(rowvert); free(rowsign);
}

int main(int argc, char **argv){
    if(argc<5){ fprintf(stderr,"usage\n"); return 1; }
    FILE *f=fopen(argv[1],"r"); if(!f) return 1; if(fscanf(f,"%d %d",&K,&N)!=2) return 1;
    X=malloc(K*N); for(int i=0;i<K*N;i++){ int v; if(fscanf(f,"%d",&v)!=1) return 1; X[i]=(signed char)v; } fclose(f);
    rs=0x9E3779B97F4A7C15ULL ^ (unsigned long long)atoll(argv[3])*2654435761ULL; for(int i=0;i<10;i++) rnd();
    double secs=atof(argv[4]); double eps=argc>5?atof(argv[5]):-1; double logev=argc>6?atof(argv[6]):30;
    int rowpairs = argc>7? atoi(argv[7]) : 1;
    drow_of=malloc(sizeof(int)*K); dsign=malloc(sizeof(int)*K); triv_var=malloc(sizeof(int)*K); triv_sign=malloc(sizeof(int)*K);
    DX=malloc(K*N); D=0; int nnz=0;
    for(int k=0;k<K;k++){ int L=0, first=-1; for(int j=0;j<N;j++) if(X[k*N+j]){ L++; if(first<0) first=j; }
        if(L==0){ drow_of[k]=-2; continue; } if(L==1){ drow_of[k]=-1; triv_var[k]=first; triv_sign[k]=X[k*N+first]; continue; }
        int sg=X[k*N+first]>0?1:-1; int found=-1;
        for(int d=0; d<D; d++){ int eq=1; for(int j=0;j<N;j++) if(DX[d*N+j]!=sg*X[k*N+j]){eq=0;break;} if(eq){found=d;break;} }
        if(found<0){ for(int j=0;j<N;j++) DX[D*N+j]=sg*X[k*N+j]; found=D++; nnz+=L; }
        drow_of[k]=found; dsign[k]=sg; }
    VMAX=N+nnz+2;
    rl=malloc(sizeof(int)*D); rv=malloc(sizeof(int)*D*VMAX); rsg=malloc(D*VMAX); dense=malloc((size_t)D*VMAX);
    occ=malloc(sizeof(int)*(size_t)VMAX*D); occn=malloc(sizeof(int)*VMAX);
    cnt=calloc((size_t)VMAX*VMAX*2,sizeof(int));
    { size_t pb=16; for(int d=0; d<D; d++){ size_t L=0; for(int j=0;j<N;j++) if(DX[d*N+j]) L++; pb+=L*(L-1)/2; } touched=malloc(sizeof(int)*pb); }
    size_t SM=(size_t)VMAX*(N+4)+16;
    stC=malloc(sizeof(int)*SM); stT=malloc(sizeof(int)*SM); stLen=malloc(sizeof(int)*VMAX); stOff=malloc(sizeof(int)*VMAX);
    bstC=malloc(sizeof(int)*SM); bstT=malloc(sizeof(int)*SM); bstLen=malloc(sizeof(int)*VMAX); bstOff=malloc(sizeof(int)*VMAX);
    tmpR=malloc(sizeof(int)*(D+1)); tmpS=malloc(sizeof(int)*(D+1)); bR=malloc(sizeof(int)*(D+1)); bS=malloc(sizeof(int)*(D+1));
    tmpC=malloc(sizeof(int)*(VMAX+1)); tmpT=malloc(sizeof(int)*(VMAX+1)); bC=malloc(sizeof(int)*(VMAX+1)); bT=malloc(sizeof(int)*(VMAX+1));
    double t0=now(), tl=t0+logev; long it=0; bestCost=1<<30; bnst=0;
    double epsset[4]={0.0,0.05,0.15,0.3};
    while(1){
        double e=eps>=0?eps:epsset[rndint(4)];
        int nf=0; if(bnst>0 && rnd01()>0.05) nf=rndint(bnst);
        int c=greedy(nf,e,rowpairs); it++;
        if(c<=bestCost){ if(c<bestCost) fprintf(stderr,"[%.1fs] it %ld cost %d\n",now()-t0,it,c);
            bestCost=c; bnst=nst; bstUsed=stUsed; memcpy(bstC,stC,sizeof(int)*stUsed); memcpy(bstT,stT,sizeof(int)*stUsed); memcpy(bstLen,stLen,sizeof(int)*nst); memcpy(bstOff,stOff,sizeof(int)*nst); }
        double tn=now(); if(tn>tl){ write_graph(argv[2],rowpairs); tl=tn+logev; }
        if(tn-t0>secs) break;
    }
    write_graph(argv[2],rowpairs);
    printf("best %d iters %ld K %d N %d D %d\n",bestCost,it,K,N,D);
    return 0;
}
