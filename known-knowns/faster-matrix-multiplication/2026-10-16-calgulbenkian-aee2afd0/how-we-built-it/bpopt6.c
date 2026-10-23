/* bpopt: Boyar-Peralta-style distance-guided SLP search with cancellation, ternary vectors (N <= 64 inputs).
   Base set S starts with the unit vectors; each step adds one element s = a + sigma b (a, b in S) that is a
   ternary vector. Targets at distance 1 are added at once; otherwise a helper is chosen to maximise the number
   of targets whose distance drops (exact distances up to 3; >= 4 tracked loosely). Iterated with random ties.
   usage: bpopt in.mat out.graph seed seconds [log_every_s]      (output format as slpopt)
   Written by opus-add (addcomp). */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <sys/time.h>

typedef struct { uint64_t p, n; } vec;
static double now(void){ struct timeval t; gettimeofday(&t,0); return t.tv_sec+1e-6*t.tv_usec; }
static unsigned long long rs;
static inline unsigned long long rnd(void){ rs^=rs<<13; rs^=rs>>7; rs^=rs<<17; return rs; }
static inline int rndint(int n){ return (int)(rnd()%(unsigned long long)n); }
static inline double rnd01(void){ return (rnd()>>11)*(1.0/9007199254740992.0); }

static inline vec neg(vec a){ vec r={a.n,a.p}; return r; }
static inline int addok(vec a, vec b){ return !(a.p&b.p) && !(a.n&b.n); }
static inline vec add(vec a, vec b){ vec r; r.p=(a.p^b.p)&~(a.n|b.n); r.n=(a.n^b.n)&~(a.p|b.p); return r; }
static inline int iszero(vec a){ return !(a.p|a.n); }
static inline int veq(vec a, vec b){ return a.p==b.p && a.n==b.n; }
static inline int wt(vec a){ return __builtin_popcountll(a.p)+__builtin_popcountll(a.n); }
/* canonical up to sign: the lowest nonzero coordinate is +1 */
static inline vec canon(vec a, int *sg){ uint64_t u=a.p|a.n; uint64_t lo=u&(~u+1); int s=(a.p&lo)?1:-1; if(sg) *sg=s; return s>0?a:neg(a); }

typedef struct { vec k; int v; int used; } slot;
typedef struct { slot *t; size_t cap, n; } table;
static inline size_t hsh(vec k){ unsigned long long h=k.p*0x9E3779B97F4A7C15ULL ^ (k.n+0x632BE59BD9B4E019ULL)*0xC2B2AE3D27D4EB4FULL; h^=h>>29; h*=0xBF58476D1CE4E5B9ULL; h^=h>>32; return (size_t)h; }
static void tinit(table *T, size_t cap){ T->cap=cap; T->n=0; T->t=calloc(cap,sizeof(slot)); }
static void tclear(table *T){ memset(T->t,0,T->cap*sizeof(slot)); T->n=0; }
static int tget(table *T, vec k, int *v){ size_t i=hsh(k)&(T->cap-1); while(T->t[i].used){ if(veq(T->t[i].k,k)){ if(v)*v=T->t[i].v; return 1; } i=(i+1)&(T->cap-1);} return 0; }
static void tput(table *T, vec k, int v){ size_t i=hsh(k)&(T->cap-1); while(T->t[i].used){ if(veq(T->t[i].k,k)) return; i=(i+1)&(T->cap-1);} T->t[i].used=1; T->t[i].k=k; T->t[i].v=v; T->n++; }

static int K, N, D;
static vec *tg; static int *drow_of, *dsign, *triv_var, *triv_sign;
static vec *S; static int *Sa, *Sb, *Ssg; static int nS, SMAX;
static table HS, HP, HC;
static int *PA, *PB, *PS, nP, PMAX;
static int *dist, *done;
static int *bestA, *bestB, *bestS, bestN, bestCost;
static int *cscore, *csec, ncand, CMAX; static vec *cvec; static int fbmode=1; static int strict=0;

static inline int inS(vec v){ vec c=canon(v,0); return tget(&HS,c,0); }
static inline int inP(vec v){ vec c=canon(v,0); return tget(&HP,c,0)||tget(&HS,c,0); }

static void addS(int a, int b, int s, vec v){
    int i=nS++; S[i]=v; Sa[i]=a; Sb[i]=b; Ssg[i]=s;
    int sg; vec c=canon(v,&sg); tput(&HS,c,i);
    for(int j=0;j<i;j++){ for(int t=-1;t<=1;t+=2){ vec w = t>0? S[j]: neg(S[j]); if(!addok(v,w)) continue; vec x=add(v,w); if(iszero(x)) continue;
            vec cx=canon(x,0); if(tget(&HS,cx,0)||tget(&HP,cx,0)) continue;
            if(nP>=PMAX) continue; PA[nP]=i; PB[nP]=j; PS[nP]=t; tput(&HP,cx,nP); nP++; } }
}
/* (a,b,s) with S[a]+s*S[b] = +-v; returns 1 if v is one step away */
static int pairof(vec v, int *a, int *b, int *s){
    vec c=canon(v,0); int id;
    if(tget(&HP,c,&id)){ *a=PA[id]; *b=PB[id]; *s=PS[id]; return 1; }
    return 0;
}
static void cand_add(vec e, int sec){
    vec c=canon(e,0); if(tget(&HS,c,0)) return; if(!tget(&HP,c,0)) return;
    int id; if(tget(&HC,c,&id)){ cscore[id]++; csec[id]+=sec; return; }
    if(ncand>=CMAX) return; id=ncand++; cvec[id]=c; cscore[id]=1; csec[id]=sec; tput(&HC,c,id);
}

static int run(double eps, int nforced){
    int step=0;
    tclear(&HS); tclear(&HP); nS=0; nP=0;
    for(int j=0;j<N;j++){ vec u={1ULL<<j,0}; addS(-1,-1,0,u); }
    for(int d=0; d<D; d++){ done[d]=0; dist[d]=wt(tg[d])-1; if(dist[d]>4) dist[d]=4; }
    int remaining=D;
    while(remaining>0){
        if(nS>=SMAX) return 1<<29;
        for(int d=0; d<D; d++){ if(done[d]) continue; if(dist[d]==0 || inS(tg[d])){ done[d]=1; remaining--; } }
        if(remaining==0) break;
        int ea,eb,es;
        vec e;
        if(step<nforced){ ea=bestA[step]; eb=bestB[step]; es=bestS[step]; goto apply_step; }
        int ones=0, pick=-1;
        for(int d=0; d<D; d++) if(!done[d] && dist[d]==1){ ones++; if(rndint(ones)==0) pick=d; }
        if(pick>=0){ e=tg[pick]; }
        else {
            if(HC.n > HC.cap/4) tclear(&HC); else tclear(&HC);
            ncand=0;
            for(int d=0; d<D; d++){ if(done[d]) continue; vec t=tg[d];
                if(dist[d]==2){ for(int a=0;a<nS;a++) for(int s=-1;s<=1;s+=2){ vec w=s>0?neg(S[a]):S[a]; if(!addok(t,w)) continue; vec y=add(t,w); if(iszero(y)) continue; cand_add(y,1); } }
                else if(dist[d]==3){
                    for(int a=0;a<nS;a++) for(int s=-1;s<=1;s+=2){ vec w=s>0?neg(S[a]):S[a]; if(!addok(t,w)) continue; vec y=add(t,w); if(iszero(y)) continue;
                        for(int b=a+1;b<nS;b++) for(int u=-1;u<=1;u+=2){ vec z=u>0?neg(S[b]):S[b]; if(!addok(y,z)) continue; vec q=add(y,z); if(iszero(q)) continue;
                            if(inP(q)){ cand_add(q,0); vec nw=neg(w), nz=neg(z); if(addok(nw,nz)) cand_add(add(nw,nz),0); } } } } }
            int best=-1, bs=-1, bsec=-1, nb=0;
            for(int i=0;i<ncand;i++){ if(cscore[i]>bs || (cscore[i]==bs && csec[i]>bsec)){ bs=cscore[i]; bsec=csec[i]; } }
            if(ncand>0){
                int loose = (rnd01()<eps);
                for(int i=0;i<ncand;i++){ int ok = loose? (cscore[i]>=bs-1 && cscore[i]>=1) : (cscore[i]==bs && csec[i]==bsec); if(ok){ nb++; if(rndint(nb)==0) best=i; } }
                e=cvec[best];
            } else {
                /* fallback A (bpopt5): greedy decomposition of every remaining target over +-S WITH cancellation
                   (each term maximises the weight drop of the remainder, remainder stays ternary); then count the
                   pairwise sums of decomposition terms over all targets and add the most frequent one. */
                if(fbmode){
                    tclear(&HC); ncand=0;
                    static vec terms[128];
                    for(int d=0; d<D; d++){ if(done[d]) continue; vec rem=tg[d]; int nt=0;
                        while(!iszero(rem) && nt<128){ int bg=0, nbg=0; vec bx2={0,0};
                            for(int a=0;a<nS;a++) for(int sg=-1;sg<=1;sg+=2){ vec x=sg>0?S[a]:neg(S[a]);
                                /* rem - x must be ternary: no position where x has the opposite sign of rem */
                                if((x.p&rem.n)||(x.n&rem.p)) continue;
                                vec r2=add(rem,neg(x)); int g=wt(rem)-wt(r2);
                                if(g<=0) continue;
                                if(g>bg){ bg=g; nbg=0; } if(g==bg){ nbg++; if(rndint(nbg)==0) bx2=x; } }
                            if(bg<=0) break;
                            terms[nt++]=bx2; rem=add(rem,neg(bx2)); }
                        if(!iszero(rem)) continue;
                        for(int i=0;i<nt;i++) for(int j=i+1;j<nt;j++){ if(!addok(terms[i],terms[j])) continue; vec z=add(terms[i],terms[j]); if(iszero(z)) continue; cand_add(z,0); } }
                    int bs2=0, nb2=0, bi=-1;
                    for(int i=0;i<ncand;i++){ if(cscore[i]>bs2){ bs2=cscore[i]; nb2=0; } if(cscore[i]==bs2){ nb2++; if(rndint(nb2)==0) bi=i; } }
                    if(bi>=0){ e=cvec[bi]; goto have_e; }
                }
                /* fallback: greedy cancellation-free chunk decomposition of each remaining target over S;
                   take the target with fewest chunks and combine its two largest chunks */
                int bd=-1, bc=1<<30; vec bx={0,0}, by={0,0}; int found=0;
                for(int d=0; d<D; d++){ if(done[d]) continue; vec rem=tg[d]; int nch=0; vec c1={0,0}, c2={0,0}; int w1=0, w2=0;
                    while(!iszero(rem)){ int bw=0, nbw=0; vec bxx={0,0};
                        for(int a=0;a<nS;a++){ int w=wt(S[a]); if(w<bw) continue;
                            for(int sg=-1;sg<=1;sg+=2){ vec x=sg>0?S[a]:neg(S[a]); if((x.p&~rem.p)||(x.n&~rem.n)) continue;
                                if(w>bw){ bw=w; nbw=0; } nbw++; if(rndint(nbw)==0) bxx=x; } }
                        if(bw==0) break;
                        rem.p&=~bxx.p; rem.n&=~bxx.n; nch++;
                        if(bw>w1){ c2=c1; w2=w1; c1=bxx; w1=bw; } else if(bw>w2){ c2=bxx; w2=bw; } }
                    int key=nch*4+rndint(4);
                    if(nch>=2 && key<bc){ vec z=add(c1,c2); if(!inS(z)){ bc=key; bd=d; bx=c1; by=c2; } } }
                vec t = bd>=0? tg[bd] : tg[0];
                if(bd>=0){ e=add(bx,by); found=1; }
                else { for(int d=0; d<D; d++) if(!done[d]){ t=tg[d]; break; } }
                if(!found){
                    int idx[64], sgv[64], k=0; for(int j=0;j<N;j++){ if(t.p>>j&1){idx[k]=j;sgv[k]=1;k++;} else if(t.n>>j&1){idx[k]=j;sgv[k]=-1;k++;} }
                    for(int tries=0; tries<2000 && !found; tries++){ int i=rndint(k), j=rndint(k); if(i==j) continue; vec z={0,0};
                        if(sgv[i]>0) z.p|=1ULL<<idx[i]; else z.n|=1ULL<<idx[i]; if(sgv[j]>0) z.p|=1ULL<<idx[j]; else z.n|=1ULL<<idx[j];
                        if(!inS(z)){ e=z; found=1; } }
                    if(!found) return 1<<29; }
            }
        }
        have_e: ;
        if(!pairof(e,&ea,&eb,&es)) return 1<<29;
        apply_step: ;
        step++;
        vec v = add(S[ea], es>0? S[eb]: neg(S[eb]));
        addS(ea,eb,es,v);
        for(int d=0; d<D; d++){ if(done[d]) continue; vec t=tg[d];
            if(inS(t)){ dist[d]=0; continue; }
            if(dist[d]<=1) continue;
            int dec=0;
            for(int s=-1;s<=1 && !dec;s+=2){ vec w=s>0?neg(v):v; if(!addok(t,w)) continue; vec y=add(t,w);
                if(dist[d]==2){ if(inS(y)) dec=1; }
                else if(dist[d]==3){ if(inP(y)) dec=1; }
                else {
                    if(inP(y)){ dec=2; break; }
                    for(int a=0;a<nS && !dec;a++) for(int u=-1;u<=1;u+=2){ vec z=u>0?neg(S[a]):S[a]; if(!addok(y,z)) continue; vec q=add(y,z); if(!iszero(q)&&inP(q)){ dec=1; break; } } } }
            if(dec==2) dist[d]=2;
            else if(dec==1){ if(dist[d]>=4) dist[d]=3; else dist[d]--; }
        }
    }
    /* count only nodes that some target uses (unused helpers are pruned from the output program) */
    static char *mark=0; if(!mark) mark=malloc(SMAX);
    memset(mark,0,nS);
    for(int d=0; d<D; d++){ int id; if(tget(&HS,canon(tg[d],0),&id)) mark[id]=1; }
    int used=0;
    for(int i=nS-1;i>=N;i--) if(mark[i]){ used++; mark[Sa[i]]=1; mark[Sb[i]]=1; }
    if(strict){
        /* transposed-program ternarity: signed path counts from every used node to every sink must be in {-1,0,1} */
        static short *P=0; static int Pcap=0;
        if(Pcap < SMAX*K){ free(P); Pcap=SMAX*K; P=malloc(sizeof(short)*Pcap); }
        memset(P,0,sizeof(short)*nS*K);
        for(int k=0;k<K;k++){ if(drow_of[k]<0) continue; int id; tget(&HS,canon(tg[drow_of[k]],0),&id);
            /* sink k = dsign[k] * tg = dsign[k] * sgn * S[id] where S[id] = sgn*tg */
            int sg = veq(S[id],tg[drow_of[k]]) ? 1 : -1; P[(size_t)id*K+k] += sg*dsign[k]; }
        for(int i=nS-1;i>=N;i--){ if(!mark[i]) continue; short *pi=P+(size_t)i*K;
            for(int k=0;k<K;k++){ if(pi[k]>1||pi[k]<-1) return 1<<28; }
            short *pa=P+(size_t)Sa[i]*K, *pb=P+(size_t)Sb[i]*K; int sb=Ssg[i];
            for(int k=0;k<K;k++){ pa[k]+=pi[k]; pb[k]+=sb*pi[k]; } }
    }
    return used;
}

static void write_graph(const char *path){
    FILE *f=fopen(path,"w"); fprintf(f,"G %d %d %d\n",N,K,bestN);
    for(int i=0;i<bestN;i++) fprintf(f,"n 2 %d 1 %d %d\n",bestA[i],bestB[i],bestS[i]);
    vec *SV=malloc(sizeof(vec)*(N+bestN)); for(int j=0;j<N;j++){ vec u={1ULL<<j,0}; SV[j]=u; }
    for(int i=0;i<bestN;i++) SV[N+i]=add(SV[bestA[i]], bestS[i]>0?SV[bestB[i]]:neg(SV[bestB[i]]));
    for(int k=0;k<K;k++){
        if(drow_of[k]==-1){ fprintf(f,"o 1 %d %d\n",triv_var[k],triv_sign[k]); continue; }
        if(drow_of[k]==-2){ fprintf(f,"o 0\n"); continue; }
        vec t=tg[drow_of[k]]; int found=-1, sg=0;
        for(int i=0;i<N+bestN;i++){ if(veq(SV[i],t)){found=i;sg=1;break;} if(veq(SV[i],neg(t))){found=i;sg=-1;break;} }
        if(found<0){ fprintf(stderr,"target not found\n"); exit(2); }
        fprintf(f,"o 1 %d %d\n",found,sg*dsign[k]);
    }
    fclose(f); free(SV);
}

int main(int argc, char **argv){
    if(argc<5){ fprintf(stderr,"usage\n"); return 1; }
    FILE *f=fopen(argv[1],"r"); if(!f) return 1; if(fscanf(f,"%d %d",&K,&N)!=2) return 1;
    if(N>64){ fprintf(stderr,"N>64 unsupported\n"); return 1; }
    signed char *X=malloc(K*N); for(int i=0;i<K*N;i++){ int v; if(fscanf(f,"%d",&v)!=1) return 1; X[i]=(signed char)v; } fclose(f);
    rs=0x9E3779B97F4A7C15ULL ^ (unsigned long long)atoll(argv[3])*2654435761ULL; for(int i=0;i<10;i++) rnd();
    double secs=atof(argv[4]); double logev=argc>5?atof(argv[5]):30; double pforce=argc>6?atof(argv[6]):0.8; fbmode=argc>7?atoi(argv[7]):1; strict=argc>8?atoi(argv[8]):0;
    drow_of=malloc(sizeof(int)*K); dsign=malloc(sizeof(int)*K); triv_var=malloc(sizeof(int)*K); triv_sign=malloc(sizeof(int)*K);
    tg=malloc(sizeof(vec)*K); D=0; int nnz=0;
    for(int k=0;k<K;k++){ vec v={0,0}; int L=0, first=-1; for(int j=0;j<N;j++){ int x=X[k*N+j]; if(x){ L++; if(first<0) first=j; if(x>0) v.p|=1ULL<<j; else v.n|=1ULL<<j; } }
        if(L==0){ drow_of[k]=-2; continue; } if(L==1){ drow_of[k]=-1; triv_var[k]=first; triv_sign[k]=X[k*N+first]; continue; }
        int sg; vec c=canon(v,&sg); int found=-1; for(int d=0; d<D; d++) if(veq(tg[d],c)){found=d;break;}
        if(found<0){ tg[D]=c; found=D++; nnz+=L; } drow_of[k]=found; dsign[k]=sg; }
    SMAX=N+nnz+8; PMAX=SMAX*SMAX*2+16; CMAX=PMAX;
    S=malloc(sizeof(vec)*SMAX); Sa=malloc(sizeof(int)*SMAX); Sb=malloc(sizeof(int)*SMAX); Ssg=malloc(sizeof(int)*SMAX);
    size_t cap=1; while(cap<(size_t)PMAX*2) cap<<=1; tinit(&HP,cap);
    size_t cc=1; while(cc<(size_t)PMAX/4+1024) cc<<=1; tinit(&HC,cc); CMAX=(int)(cc/2);
    size_t cs=1; while(cs<(size_t)SMAX*4) cs<<=1; tinit(&HS,cs);
    PA=malloc(sizeof(int)*PMAX); PB=malloc(sizeof(int)*PMAX); PS=malloc(sizeof(int)*PMAX);
    cscore=malloc(sizeof(int)*CMAX); csec=malloc(sizeof(int)*CMAX); cvec=malloc(sizeof(vec)*CMAX);
    dist=malloc(sizeof(int)*D); done=malloc(sizeof(int)*D);
    bestA=malloc(sizeof(int)*SMAX); bestB=malloc(sizeof(int)*SMAX); bestS=malloc(sizeof(int)*SMAX); bestCost=1<<30; bestN=0;
    double t0=now(), tl=t0+logev; long it=0; double epsset[3]={0.0,0.1,0.3};
    while(1){
        int nf = (bestN>0 && rnd01()<pforce)? rndint(bestN) : 0;
        int c=run(epsset[rndint(3)], nf); it++;
        if(c<=bestCost){ if(c<bestCost) fprintf(stderr,"[%.1fs] it %ld cost %d (nf %d)\n",now()-t0,it,c,nf); bestCost=c; bestN=nS-N; for(int i=0;i<bestN;i++){ bestA[i]=Sa[N+i]; bestB[i]=Sb[N+i]; bestS[i]=Ssg[N+i]; }
            }
        double tn=now(); if(tn>tl && bestN>0){ write_graph(argv[2]); tl=tn+logev; }
        if(tn-t0>secs) break;
    }
    write_graph(argv[2]);
    printf("best %d iters %ld K %d N %d D %d\n",bestCost,it,K,N,D);
    return 0;
}
