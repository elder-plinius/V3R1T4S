/* Compact C port of method A (histogram recurrence, Cheng-Xu Thm 3.2) for d-regular
 * unlabeled graph counting, working modulo a 62-bit prime.
 *
 * Computes, for a given degree D and prime P, the Burnside residue
 *   S(N) = sum_{lambda |- N} (N!/z_lambda) * F_D(lambda)   (mod P)
 * for all even N up to NMAX, and prints "N S" per line. U_D(N) = S(N)/N! is recovered
 * by the Python driver via inv(N!) mod P and CRT across several primes.
 *
 * State H = sorted-desc multiset of (a, r, count): a=cycle length, r=residual degree
 * (1..D), count>0. Phi(H) memoized in a global open-addressing hash table (per prime).
 *
 * Pivot order flag: --pivot max (default, largest (a,r) first, matches Python) or
 * --pivot min (smallest first) -> same final answer, a second traversal of the same
 * recurrence (invariance check, NOT an independent method).
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <sys/resource.h>
#include <time.h>
static int STATS=0;
static long maxrss_kb(void){ struct rusage r; getrusage(RUSAGE_SELF,&r); return r.ru_maxrss; }

typedef unsigned __int128 u128;
typedef uint64_t u64;

static u64 P;          /* prime modulus */
static int D;          /* degree */
static int PIVOT_MIN;  /* 0 = pivot largest (a,r), 1 = pivot smallest */

static inline u64 mulmod(u64 a, u64 b){ return (u64)(( (u128)a * b) % P); }
static inline u64 addmod(u64 a, u64 b){ a+=b; if(a>=P)a-=P; return a; }

/* ---- Ia tables: Ia[a][u], u=0..D, # internal edge-orbit choices of internal deg u.
 * P_a(x) = (1+x^2)^floor((a-1)/2) * (1+x)^[a even].  (exact small integers) */
static int NMAX;
static u64 **Ia;       /* Ia[a][0..D] mod P */
static void build_Ia(void){
    Ia = calloc(NMAX+1, sizeof(u64*));
    for(int a=1;a<=NMAX;a++){
        /* build polynomial coefficients exactly as 64-bit (small) then reduce */
        long poly[64]; int plen=1; poly[0]=1;
        int half=(a-1)/2;
        for(int t=0;t<half;t++){ /* multiply by (1+x^2) */
            long np[64]; int nl=plen+2; for(int i=0;i<nl;i++)np[i]=0;
            for(int i=0;i<plen;i++){ np[i]+=poly[i]; np[i+2]+=poly[i]; }
            memcpy(poly,np,nl*sizeof(long)); plen=nl;
        }
        if(a%2==0){ /* multiply by (1+x) */
            long np[64]; int nl=plen+1; for(int i=0;i<nl;i++)np[i]=0;
            for(int i=0;i<plen;i++){ np[i]+=poly[i]; np[i+1]+=poly[i]; }
            memcpy(poly,np,nl*sizeof(long)); plen=nl;
        }
        Ia[a]=calloc(D+1,sizeof(u64));
        for(int u=0;u<=D;u++){ long c = (u<plen)?poly[u]:0; Ia[a][u]=(u64)(c % P); }
    }
}

/* ---- binomial C(n,k) mod P for small n (<= ~D and <= cycle counts up to NMAX) ---- */
static u64 **BIN; /* BIN[n][k] mod P, n up to NMAX */
static void build_bin(void){
    BIN=calloc(NMAX+1,sizeof(u64*));
    for(int n=0;n<=NMAX;n++){ BIN[n]=calloc(NMAX+1,sizeof(u64));
        BIN[n][0]=1%P; for(int k=1;k<=n;k++) BIN[n][k]=addmod(BIN[n-1][k-1],BIN[n-1][k]); }
}
static inline u64 binom(int n,int k){ if(k<0||k>n) return 0; return BIN[n][k]; }

/* gcd */
static int igcd(int a,int b){ while(b){int t=a%b;a=b;b=t;} return a; }

/* ---------------- state key: packed bytes, sorted desc ----------------
 * A state is an array of triples (a,r,c). We store it canonically as a byte string:
 * uint16 a, uint8 r, uint16 c  (5 bytes each), triples sorted descending by (a,r).
 * Max triples small (distinct (a,r) pairs). */
typedef struct { uint16_t a; uint8_t r; uint16_t c; } Tri;

/* comparison for descending sort by (a,r) [then r]; matches Python tuple reverse */
static int tri_cmp_desc(const void*x,const void*y){
    const Tri*p=x,*q=y;
    if(p->a!=q->a) return (p->a<q->a)?1:-1;
    if(p->r!=q->r) return (p->r<q->r)?1:-1;
    return 0;
}

/* ---------------- global hash table (Phi memo), per prime ---------------- */
typedef struct { uint8_t* key; int klen; u64 val; } Slot;
static Slot* HT; static size_t HTcap, HTcnt;
/* chunked bump arena: existing data never moves, so stored key pointers stay valid */
#define ARENA_CHUNK (16u<<20)
static uint8_t** ACHUNKS; static int ANCH, ACAP; static size_t ARENA_used; static uint8_t* ARENA;
static uint8_t* arena_dup(const uint8_t* b,int n){
    if(!ARENA || ARENA_used+(size_t)n>ARENA_CHUNK){
        if(ANCH==ACAP){ ACAP=ACAP?ACAP*2:16; ACHUNKS=realloc(ACHUNKS,ACAP*sizeof(uint8_t*)); }
        ARENA=malloc(ARENA_CHUNK); ACHUNKS[ANCH++]=ARENA; ARENA_used=0;
    }
    uint8_t* p=ARENA+ARENA_used; memcpy(p,b,n); ARENA_used+=n; return p;
}
static u64 fnv(const uint8_t*b,int n){ u64 h=1469598103934665603ULL; for(int i=0;i<n;i++){h^=b[i];h*=1099511628211ULL;} return h; }

static void ht_init(size_t cap){ HTcap=cap; HTcnt=0; HT=calloc(HTcap,sizeof(Slot));
    ACHUNKS=NULL; ANCH=0; ACAP=0; ARENA=NULL; ARENA_used=0; }
static void ht_free(void){ free(HT); HT=NULL; for(int i=0;i<ANCH;i++) free(ACHUNKS[i]); free(ACHUNKS); ACHUNKS=NULL; ANCH=ACAP=0; ARENA=NULL; ARENA_used=0; }
static void ht_grow(void);
/* find slot for key; returns index; sets *found */
static size_t ht_find(const uint8_t*key,int klen,int*found){
    u64 h=fnv(key,klen); size_t mask=HTcap-1; size_t i=h&mask;
    while(HT[i].key){ if(HT[i].klen==klen && memcmp(HT[i].key,key,klen)==0){*found=1;return i;} i=(i+1)&mask; }
    *found=0; return i;
}
static int ht_get(const uint8_t*key,int klen,u64*out){ int f; size_t i=ht_find(key,klen,&f); if(f){*out=HT[i].val;return 1;} return 0; }
static void ht_put(const uint8_t*key,int klen,u64 val){
    if((HTcnt+1)*10 >= HTcap*7) ht_grow();
    int f; size_t i=ht_find(key,klen,&f);
    if(!f){ HT[i].key=arena_dup(key,klen); HT[i].klen=klen; HTcnt++; }
    HT[i].val=val;
}
static void ht_grow(void){
    size_t oldcap=HTcap; Slot*old=HT; HTcap*=2; HT=calloc(HTcap,sizeof(Slot)); HTcnt=0;
    for(size_t i=0;i<oldcap;i++) if(old[i].key){ int f; size_t j=ht_find(old[i].key,old[i].klen,&f);
        HT[j]=old[i]; HTcnt++; }
    free(old);
}

/* serialize a Tri array (already canonical sorted desc, c>0) to key buffer; returns len */
static int serialize(const Tri*t,int n,uint8_t*buf){
    int p=0; for(int i=0;i<n;i++){ buf[p++]=t[i].a&0xff; buf[p++]=(t[i].a>>8)&0xff; buf[p++]=t[i].r;
        buf[p++]=t[i].c&0xff; buf[p++]=(t[i].c>>8)&0xff; } return p;
}

/* ---------------- Phi recurrence ---------------- */
/* canonicalize: sort desc, drop c<=0, merge equal (a,r). */
static int canon(Tri*t,int n){
    /* merge equal (a,r) */
    for(int i=0;i<n;i++){ if(t[i].c==0) continue;
        for(int j=i+1;j<n;j++){ if(t[j].c && t[j].a==t[i].a && t[j].r==t[i].r){ t[i].c+=t[j].c; t[j].c=0; } } }
    int m=0; for(int i=0;i<n;i++) if(t[i].c>0) t[m++]=t[i];
    qsort(t,m,sizeof(Tri),tri_cmp_desc);
    return m;
}

static u64 Phi(Tri*H,int n);  /* forward */

/* _distribute: allocate pivot (length pa) joining-orbits to classes[idx..n), consuming
 * exactly `budget`. Accumulate into Phi via callback style: we build newH for each full
 * assignment and add iu*weight*Phi(newH). To mirror Python, we enumerate class_options
 * per class and recurse. moves are applied onto a working copy `base` (the rest-without-pivot
 * histogram) producing newH. */

/* class_options enumeration for (pa,b,s,h): calls cb(consumed,weight,movelist...) inline.
 * We implement by recursion over k=1..Kmax as in Python. Instead of materializing option
 * lists, we fold directly into the distribute recursion. */

/* We implement distribute with an explicit recursion that, for each class, iterates its
 * options (consumed, weight, and the resulting per-class residual moves), then recurses. */

typedef struct { Tri* base; int bn; Tri* work; int wn; int pa; u64 iu; int budget_total; } DistCtx;

/* apply: given we've chosen, for class original (b,s,h), a set of nu_k (k=1..K) with
 * remaining = h - sum nu_k staying at (b,s): we add moves (b, s-k*beta, nu_k) and
 * (b,s,remaining). We accumulate these into a temporary move buffer. */

/* To keep it simple and faithful, we enumerate options per class into arrays, then do a
 * cartesian recursion across classes (like Python _distribute with tails_cache but without
 * caching, which is fine for small class counts). */

#define MAXOPT 16384
#define MAXDEPTH 80
typedef struct { int consumed; u64 weight; Tri mv[8]; int mvn; } Opt;
static Opt* OPTPOOL[MAXDEPTH];   /* per-recursion-depth option buffer */
static void optpool_init(void){ for(int i=0;i<MAXDEPTH;i++) OPTPOOL[i]=malloc(sizeof(Opt)*MAXOPT); }

static int class_options(int pa,int b,int s,int h,Opt*out){
    int g=igcd(pa,b); int alpha=b/g; int beta=pa/g;
    int Kmax=g; if(alpha){ int t=D/alpha; if(t<Kmax)Kmax=t;} if(beta){ int t=s/beta; if(t<Kmax)Kmax=t;}
    if(!alpha) Kmax=0; /* alpha=0 impossible since b>=1 */
    int no=0;
    /* recursion over k=1..Kmax choosing nu_k, tracking remaining h, consumed, weight, moves */
    /* iterative DFS via explicit stack is messy; use recursion helper */
    /* We'll do recursion with a local function emulation through an explicit struct-less
       recursive static function below. */
    extern int co_rec(int,int,int,int,int,int,int,int,u64,Tri*,int,Opt*,int);
    no = co_rec(1,Kmax,h,0,1 /*weight placeholder set below*/,b,s,beta,1ULL%P,NULL,0,out,0);
    (void)alpha;(void)g;
    return no;
}
/* recursive builder: k current, Kmax, remaining cycles, consumed, (weight passed as u64),
 * b,s,beta, weight, moves[], movesn, out[], count */
int co_rec(int k,int Kmax,int remaining,int consumed,int b_dummy,
           int b,int s,int beta,u64 weight,Tri*moves,int movesn,Opt*out,int count){
    (void)b_dummy;
    if(k>Kmax){
        if(count>=MAXOPT){ fprintf(stderr,"MAXOPT overflow\n"); exit(9); }
        Opt*o=&out[count];
        o->consumed=consumed; o->weight=weight; o->mvn=0;
        for(int i=0;i<movesn;i++) o->mv[o->mvn++]=moves[i];
        if(remaining>0){ o->mv[o->mvn].a=b; o->mv[o->mvn].r=s; o->mv[o->mvn].c=remaining; o->mvn++; }
        return count+1;
    }
    int new_s=s-k*beta;
    int g_for_ck; /* need C(g,k): recompute g from alpha? we passed beta only. Recompute via stored globals? */
    /* We need g = gcd(pa,b). Recompute here: but pa not passed. Store pa globally for this. */
    extern int CO_pa, CO_alpha, CO_g;
    g_for_ck=CO_g;
    u64 ck = binom(g_for_ck,k);
    Tri local[8];
    for(int nu=0;nu<=remaining;nu++){
        if(nu==0){
            count=co_rec(k+1,Kmax,remaining,consumed,0,b,s,beta,weight,moves,movesn,out,count);
        } else {
            if(new_s<0) break;
            /* weight *= C(remaining,nu) * ck^nu */
            u64 w=weight; w=mulmod(w, binom(remaining,nu));
            u64 cp=1%P; for(int e=0;e<nu;e++) cp=mulmod(cp,ck);
            w=mulmod(w,cp);
            int ln=movesn; for(int i=0;i<movesn;i++) local[i]=moves[i];
            if(new_s>0){ local[ln].a=b; local[ln].r=new_s; local[ln].c=nu; ln++; }
            count=co_rec(k+1,Kmax,remaining-nu,consumed+ (CO_alpha)*k*nu,0,b,s,beta,w,local,ln,out,count);
        }
    }
    return count;
}
int CO_pa=0, CO_alpha=0, CO_g=0;

/* distribute recursion: classes = base histogram (rest-without-pivot), idx, budget.
 * For each class we enumerate options; combine moves across classes; at the end build
 * newH = base with (b,s) residuals updated by all moves, then add iu*weight*Phi(newH). */
static u64 distribute(Tri*classes,int ncl,int idx,int budget,int pa,u64 weight_acc,
                      Tri*accmoves,int accn,int depth){
    if(idx==ncl){
        if(budget!=0) return 0;
        /* newH = merge of all accmoves (each class fully re-expressed by its moves). */
        Tri nb[256]; int nn=0;
        for(int i=0;i<accn;i++) nb[nn++]=accmoves[i];
        nn=canon(nb,nn);
        u64 ph=Phi(nb,nn);
        return mulmod(weight_acc,ph);
    }
    int b=classes[idx].a, s=classes[idx].r, h=classes[idx].c;
    CO_pa=pa; CO_g=igcd(pa,b); CO_alpha=b/CO_g;
    int no=class_options(pa,b,s,h,OPTPOOL[0]);
    /* copy options to a local buffer so nested Phi/distribute calls can reuse the pool */
    Opt* opts=malloc(sizeof(Opt)*(no>0?no:1));
    memcpy(opts,OPTPOOL[0],sizeof(Opt)*no);
    u64 total=0;
    for(int i=0;i<no;i++){
        if(opts[i].consumed>budget) continue;
        int rem=budget-opts[i].consumed;
        Tri nm[256]; int nmn=accn; for(int j=0;j<accn;j++) nm[j]=accmoves[j];
        for(int j=0;j<opts[i].mvn;j++) nm[nmn++]=opts[i].mv[j];
        u64 w=mulmod(weight_acc,opts[i].weight);
        total=addmod(total, distribute(classes,ncl,idx+1,rem,pa,w,nm,nmn,depth+1));
    }
    free(opts);
    return total;
}

static u64 Phi(Tri*H,int n){
    if(n==0) return 1%P;
    /* canonical already expected; compute key */
    uint8_t key[2048]; int klen=serialize(H,n,key);
    u64 memo; if(ht_get(key,klen,&memo)) return memo;
    /* pick pivot: index 0 (largest) by default, or last (smallest) if PIVOT_MIN */
    int pidx = PIVOT_MIN ? (n-1) : 0;
    int pa=H[pidx].a, pr=H[pidx].r;
    /* rest = H minus one copy of pivot */
    Tri rest[256]; int rn=0;
    for(int i=0;i<n;i++){ rest[rn]=H[i]; if(i==pidx){ rest[rn].c -= 1; } if(rest[rn].c>0) rn++; }
    /* rest stays canonical (sorted desc, pivot decrement preserves order) */
    u64 total=0;
    for(int u=0;u<=pr && u<=D;u++){
        u64 iu=Ia[pa][u]; if(iu==0) continue;
        int budget=pr-u;
        Tri acc[256];
        u64 part=distribute(rest,rn,0,budget,pa,1%P,acc,0,0);
        total=addmod(total, mulmod(iu,part));
    }
    ht_put(key,klen,total);
    return total;
}

/* F_A(lambda): lambda given as multiset of cycle lengths -> H = {(a,D,mult)} */
static u64 F_A_from_type(int*cyc,int t){
    /* count multiplicities */
    Tri H[256]; int n=0;
    for(int i=0;i<t;i++){ int a=cyc[i]; int found=-1;
        for(int j=0;j<n;j++) if(H[j].a==a){found=j;break;}
        if(found<0){ H[n].a=a; H[n].r=D; H[n].c=1; n++; } else H[found].c++; }
    n=canon(H,n);
    return Phi(H,n);
}

/* ---- partitions of N, Burnside residue S(N) = sum (N!/z_lambda) * F_A(lambda) mod P ----
 * We generate partitions and compute N!/z_lambda mod P on the fly.
 * z_lambda = prod a^{m_a} * m_a! ; N!/z_lambda is an integer (class size), we reduce mod P.
 * Since P is prime > N, factorials & inverses are fine mod P. */
static u64 *FACT, *IFACT;
static u64 powmod(u64 b,u64 e){ u64 r=1%P; b%=P; while(e){ if(e&1) r=mulmod(r,b); b=mulmod(b,b); e>>=1;} return r; }
static void build_fact(void){ FACT=calloc(NMAX+1,sizeof(u64)); IFACT=calloc(NMAX+1,sizeof(u64));
    FACT[0]=1%P; for(int i=1;i<=NMAX;i++) FACT[i]=mulmod(FACT[i-1],i);
    IFACT[NMAX]=powmod(FACT[NMAX],P-2); for(int i=NMAX;i>0;i--) IFACT[i-1]=mulmod(IFACT[i],i); }

/* class size N!/z_lambda mod P, given multiplicities m[a] */
static u64 classsize(int N,int*mult){ /* mult indexed by part length */
    u64 z=1%P;
    for(int a=1;a<=N;a++) if(mult[a]){ z=mulmod(z, powmod(a%P,mult[a])); z=mulmod(z,FACT[mult[a]]); }
    return mulmod(FACT[N], powmod(z,P-2));
}

static u64 Ssum;
static int curN;
static int cyc_buf[128];
static void gen_part(int N,int maxpart,int t,int*mult){
    if(N==0){
        /* evaluate this partition */
        u64 f=F_A_from_type(cyc_buf,t);
        if(f){ u64 cs=classsize(curN,mult); Ssum=addmod(Ssum, mulmod(cs,f)); }
        return;
    }
    int top = maxpart<N?maxpart:N;
    for(int k=top;k>=1;k--){
        cyc_buf[t]=k; mult[k]++;
        gen_part(N-k,k,t+1,mult);
        mult[k]--;
    }
}

int main(int argc,char**argv){
    D=3; NMAX=40; P=4611686018427387847ULL; PIVOT_MIN=0; int from=2;
    for(int i=1;i<argc;i++){
        if(!strcmp(argv[i],"--deg")) D=atoi(argv[++i]);
        else if(!strcmp(argv[i],"--nmax")) NMAX=atoi(argv[++i]);
        else if(!strcmp(argv[i],"--from")) from=atoi(argv[++i]);
        else if(!strcmp(argv[i],"--prime")) P=strtoull(argv[++i],0,10);
        else if(!strcmp(argv[i],"--pivot")) PIVOT_MIN = (!strcmp(argv[++i],"min"));
        else if(!strcmp(argv[i],"--stats")) STATS=1;
    }
    build_Ia(); build_bin(); build_fact(); optpool_init();
    ht_init(1u<<20);
    /* debug: --ftype "a b c ..." prints F_A(type) mod P */
    for(int i=1;i<argc;i++) if(!strcmp(argv[i],"--ftype")){
        int cyc[128],t=0; char*s=argv[i+1]; char*tok=strtok(s," ");
        while(tok){ cyc[t++]=atoi(tok); tok=strtok(NULL," "); }
        printf("%llu\n",(unsigned long long)F_A_from_type(cyc,t)); return 0;
    }
    for(int i=1;i<argc;i++) if(!strcmp(argv[i],"--phi")){
        /* --phi "a r c a r c ..." */
        int v[128],t=0; char*s=argv[i+1]; char*tok=strtok(s," ");
        while(tok){ v[t++]=atoi(tok); tok=strtok(NULL," "); }
        Tri H[64]; int n=0; for(int j=0;j+2<t+1 && j+2<=t;j+=3){ H[n].a=v[j];H[n].r=v[j+1];H[n].c=v[j+2];n++; }
        n=canon(H,n);
        printf("%llu\n",(unsigned long long)Phi(H,n)); return 0;
    }
    int*mult=calloc(NMAX+2,sizeof(int));
    for(int N=from;N<=NMAX;N++){
        if((D*N)%2!=0){ printf("%d 0\n",N); continue; }
        Ssum=0; curN=N;
        double t0=(double)clock()/CLOCKS_PER_SEC;
        gen_part(N,N,0,mult);
        double t1=(double)clock()/CLOCKS_PER_SEC;
        printf("%d %llu\n",N,(unsigned long long)Ssum);
        fflush(stdout);
        if(STATS) fprintf(stderr,"N=%d states=%zu maxRSS=%ldMB dt=%.1fs\n",N,HTcnt,maxrss_kb()/1024,t1-t0);
    }
    free(mult); ht_free();
    return 0;
}
