/* benzB64.c - (benzB128.c with u64 overflow-aborting counts and load factor 0.9, to halve memory) second, independently written counter for stones-and-bones tilings of the (a,b)-benzel.
   Region: Propp's geometric definition (cells = unit hexagons centred at lattice points u + v*w, w = e^{2 pi i/3},
   that lie fully inside the hexagon with vertices aw+b, -aw^2-b, aw^2+bw, -a-bw, a+bw^2, -aw-bw^2).
   Tiles: triples of cells c, c+d, c+2d (|d|^2 = 3: bones) and pairwise-adjacent triples (stones).
   Sweep: cells ordered by the line coordinate k (ascending), then by i descending - a different line family and order
   from program A. Frontier DP over 64-bit masks, u64 counts with overflow detection (abort on overflow).
   Pruning (sound): a state is discarded only if an exhaustive search shows that the free cells of the next Z
   lines cannot all be covered by tiles made of free cells. Usage: benzB a b Z every [nodelimit]                   */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <omp.h>
#include <time.h>
typedef uint64_t u64; typedef unsigned __int128 u128;
typedef struct { long u, v; } Pt;
static long crs(Pt o, Pt p, Pt q){ return (p.u-o.u)*(q.v-o.v)-(q.u-o.u)*(p.v-o.v); }
static long nrm(long u,long v){ return u*u-u*v+v*v; }
static int A_,B_,Z_,EV_,LIM_=3000;
static int NC; static long *cu,*cv; static int *line, *lstart, NL;
static int NT; static int (*tc)[3];
static int *opts_off,*opts; /* tiles containing each cell */
static int *fst_off; static int (*fst)[2]; /* tiles by first (lowest-index) cell: offsets */
static int WIN=0;
typedef struct { u64 key; u64 cnt; } Slot; /* benzB64: u64 counts, every addition overflow-checked; any overflow aborts the run */
typedef struct { Slot *s; unsigned char *used; size_t cap, n; } Tab;
static int OVF=0;
static size_t hidx(u64 k, size_t cap){ k ^= k>>33; k *= 0xff51afd7ed558ccdULL; k ^= k>>33; k *= 0xc4ceb9fe1a85ec53ULL; k ^= k>>33; return (size_t)k & (cap-1); }
static void tnew(Tab*t,size_t cap){ t->cap=cap; t->n=0; t->s=malloc(cap*sizeof(Slot)); t->used=calloc(cap,1); if(!t->s||!t->used){fprintf(stderr,"out of memory\n"); exit(2);} }
static void tdel(Tab*t){ free(t->s); free(t->used); }
static Slot* tget(Tab*t,u64 k){ size_t h=hidx(k,t->cap); while(t->used[h]){ if(t->s[h].key==k) return &t->s[h]; h=(h+1)&(t->cap-1);} return 0; }
static void tadd(Tab*t,u64 k,u64 c);
static void tgrow(Tab*t){ Tab o=*t; tnew(t,o.cap*2); for(size_t h=0;h<o.cap;h++) if(o.used[h]) tadd(t,o.s[h].key,o.s[h].cnt); tdel(&o); }
static void tadd(Tab*t,u64 k,u64 c){ if(10*(t->n+1)>9*t->cap) tgrow(t); /* load factor 0.9 (memory) */ size_t h=hidx(k,t->cap);
  while(t->used[h]){ if(t->s[h].key==k){ u64 o=t->s[h].cnt; t->s[h].cnt=o+c; if(t->s[h].cnt<o) OVF=1; return; } h=(h+1)&(t->cap-1); }
  t->used[h]=1; t->s[h].key=k; t->s[h].cnt=c; t->n++; }
/* ---- feasibility search ---- */
typedef struct { unsigned char *fr; int lo, hi; long budget; } Srch;
static int cover(Srch*S){ /* 1 = coverable, 0 = impossible, -1 = gave up */
  if(--S->budget<0) return -1;
  int pick=-1, np=1000;
  for(int x=S->lo; x<S->hi; x++){ if(!S->fr[x]) continue; int c=0;
    for(int q=opts_off[x]; q<opts_off[x+1]; q++){ int*t=tc[opts[q]]; if(S->fr[t[0]]&&S->fr[t[1]]&&S->fr[t[2]]) c++; }
    if(c==0) return 0; if(c<np){ np=c; pick=x; if(c==1) break; } }
  if(pick<0) return 1;
  int gave=0;
  for(int q=opts_off[pick]; q<opts_off[pick+1]; q++){ int*t=tc[opts[q]]; if(!(S->fr[t[0]]&&S->fr[t[1]]&&S->fr[t[2]])) continue;
    S->fr[t[0]]=S->fr[t[1]]=S->fr[t[2]]=0; int r=cover(S); S->fr[t[0]]=S->fr[t[1]]=S->fr[t[2]]=1;
    if(r==1) return 1; if(r<0){ gave=1; break; } }
  return gave? -1 : 0; }
static int keep(unsigned char*fr,int p,u64 m){ /* state m at position p */
  if(p>=NC) return m==0;
  if(p%EV_) return 1;
  int L=line[p]; int hi = (L+Z_+1<NL)? lstart[L+Z_+1] : NC; int top=(L+Z_+3<NL)? lstart[L+Z_+3] : NC;
  for(int x=p;x<top;x++){ int o=x-p; fr[x]= (o<64 && ((m>>o)&1))? 0:1; }
  Srch S={fr,p,hi,LIM_}; int r=cover(&S);
  for(int x=p;x<top;x++) fr[x]=0;
  return r!=0; }
int main(int argc,char**argv){
  if(argc<5){ fprintf(stderr,"usage: benzB a b Z every [limit]\n"); return 1; }
  A_=atoi(argv[1]); B_=atoi(argv[2]); Z_=atoi(argv[3]); EV_=atoi(argv[4]); if(argc>5) LIM_=atoi(argv[5]);
  long a=A_, b=B_;
  /* hexagon vertices in (u,v), point = u + v w, w^2 = -1 - w */
  Pt V[6]={{b,a},{a-b,a},{-a,b-a},{-a,-b},{a-b,-b},{b,b-a}};
  /* recompute exactly: aw+b=(b,a); -aw^2-b = a+aw-b=(a-b,a); aw^2+bw = -a-aw+bw=(-a,b-a); -a-bw=(-a,-b); a+bw^2=a-b-bw=(a-b,-b); -aw-bw^2 = -aw+b+bw=(b,b-a) */
  long sg = crs(V[0],V[1],V[2])>0 ? 1 : -1;
  long Rr=3*(a+b)+3; int cap=(int)((2*Rr+1)*(2*Rr+1));
  long *U=malloc(sizeof(long)*cap),*Vv=malloc(sizeof(long)*cap),*Kc=malloc(sizeof(long)*cap),*Ic=malloc(sizeof(long)*cap); int n=0;
  Pt cn[6]={{1,0},{-1,0},{0,1},{0,-1},{-1,-1},{1,1}};
  for(long i=-Rr;i<=Rr;i++) for(long j=-Rr;j<=Rr;j++){ long k=1-i-j; Pt c={i-k,j-k}; int in=1;
    for(int d=0; d<6 && in; d++){ Pt p={c.u+cn[d].u, c.v+cn[d].v}; for(int e=0;e<6;e++) if(sg*crs(V[e],V[(e+1)%6],p)<0){ in=0; break; } }
    if(in){ U[n]=c.u; Vv[n]=c.v; Kc[n]=k; Ic[n]=i; n++; } }
  NC=n;
  /* order: k ascending, then i descending (insertion sort on index array) */
  int *ord=malloc(sizeof(int)*n); for(int x=0;x<n;x++) ord[x]=x;
  for(int x=1;x<n;x++){ int y=ord[x], z=x-1; while(z>=0 && (Kc[ord[z]]>Kc[y] || (Kc[ord[z]]==Kc[y] && Ic[ord[z]]<Ic[y]))){ ord[z+1]=ord[z]; z--; } ord[z+1]=y; }
  cu=malloc(sizeof(long)*n); cv=malloc(sizeof(long)*n); line=malloc(sizeof(int)*n); lstart=malloc(sizeof(int)*(n+1)); NL=0;
  long *kk=malloc(sizeof(long)*n);
  for(int x=0;x<n;x++){ cu[x]=U[ord[x]]; cv[x]=Vv[ord[x]]; kk[x]=Kc[ord[x]]; if(x==0||kk[x]!=kk[x-1]) lstart[NL++]=x; line[x]=NL-1; }
  /* lookup by coordinates */
  long off=4*Rr+4, side=2*off+1; int *look=malloc(sizeof(int)*side*side); for(long q=0;q<side*side;q++) look[q]=-1;
  for(int x=0;x<n;x++) look[(cu[x]+off)*side+(cv[x]+off)]=x;
  #define LOOK(uu,vv) ((labs(uu)<off&&labs(vv)<off)? look[((uu)+off)*side+((vv)+off)] : -1)
  Pt nb[6]; int nn=0; for(long du=-2;du<=2;du++) for(long dv=-2;dv<=2;dv++) if(nrm(du,dv)==3){ nb[nn].u=du; nb[nn].v=dv; nn++; }
  if(nn!=6){ fprintf(stderr,"neighbour vectors %d\n",nn); return 3; }
  tc=malloc(sizeof(int)*3*n*12); NT=0; int nbone=0,nstone=0;
  for(int x=0;x<n;x++){
    for(int d=0;d<6;d++){ int y=LOOK(cu[x]+nb[d].u,cv[x]+nb[d].v), z=LOOK(cu[x]+2*nb[d].u,cv[x]+2*nb[d].v);
      if(y>x && z>x){ tc[NT][0]=x; tc[NT][1]=y; tc[NT][2]=z; NT++; nbone++; } }
    for(int d=0;d<6;d++) for(int e=d+1;e<6;e++){ if(nrm(nb[d].u-nb[e].u,nb[d].v-nb[e].v)!=3) continue;
      int y=LOOK(cu[x]+nb[d].u,cv[x]+nb[d].v), z=LOOK(cu[x]+nb[e].u,cv[x]+nb[e].v);
      if(y>x && z>x){ tc[NT][0]=x; tc[NT][1]=y; tc[NT][2]=z; NT++; nstone++; } } }
  /* every tile is recorded exactly once, at its lowest-index cell x (other two have larger index) */
  opts_off=calloc(n+1,sizeof(int)); for(int t=0;t<NT;t++) for(int r=0;r<3;r++) opts_off[tc[t][r]+1]++;
  for(int x=0;x<n;x++) opts_off[x+1]+=opts_off[x]; opts=malloc(sizeof(int)*opts_off[n]); int *fill=calloc(n,sizeof(int));
  for(int t=0;t<NT;t++) for(int r=0;r<3;r++){ int x=tc[t][r]; opts[opts_off[x]+fill[x]++]=t; }
  fst_off=calloc(n+1,sizeof(int)); for(int t=0;t<NT;t++) fst_off[tc[t][0]+1]++; for(int x=0;x<n;x++) fst_off[x+1]+=fst_off[x];
  fst=malloc(sizeof(int)*2*NT); memset(fill,0,sizeof(int)*n);
  for(int t=0;t<NT;t++){ int x=tc[t][0]; int q=fst_off[x]+fill[x]++; fst[q][0]=tc[t][1]-x; fst[q][1]=tc[t][2]-x; if(fst[q][0]+1>WIN) WIN=fst[q][0]+1; if(fst[q][1]+1>WIN) WIN=fst[q][1]+1; }
  fprintf(stderr,"(%d,%d): cells %d lines %d bones %d stones %d window %d Z %d every %d\n",A_,B_,n,NL,nbone,nstone,WIN,Z_,EV_);
  if(WIN>64){ fprintf(stderr,"window too wide\n"); return 4; }
  if(n%3){ printf("0\n"); return 0; }
  int P=omp_get_max_threads(); unsigned char **FR=malloc(sizeof(void*)*P); for(int p=0;p<P;p++) FR[p]=calloc(n+8,1);
  Tab *cur=calloc(P,sizeof(Tab)), *nxt=calloc(P,sizeof(Tab)); for(int p=0;p<P;p++){ tnew(&cur[p],256); tnew(&nxt[p],256); }
  /* optional checkpoint (env BENZB_CKPT file, BENZB_CKPT_SEC seconds): header a,b,Z,every,pos,count then Slots */
  const char*ck=getenv("BENZB_CKPT"); double cks=getenv("BENZB_CKPT_SEC")?atof(getenv("BENZB_CKPT_SEC")):600; int pos0=0; time_t lastck=time(NULL);
  if(ck){ FILE*f=fopen(ck,"rb"); if(f){ int h[5]; size_t cntn; if(fread(h,sizeof(int),5,f)==5 && fread(&cntn,sizeof(size_t),1,f)==1 && h[0]==A_ && h[1]==B_ && h[2]==Z_ && h[3]==EV_){
        for(size_t q=0;q<cntn;q++){ Slot sl; if(fread(&sl,sizeof(Slot),1,f)!=1){ fprintf(stderr,"bad checkpoint\n"); return 7; } tadd(&cur[hidx(sl.key,1u<<16)%P],sl.key,sl.cnt); }
        pos0=h[4]; fprintf(stderr,"resumed pos %d states %zu\n",pos0,cntn); } fclose(f); } }
  if(pos0==0) tadd(&cur[hidx(0,1u<<16)%P],0,1); size_t mx=0;
  for(int pos=pos0; pos<n; pos++){
    #pragma omp parallel num_threads(P)
    { int me=omp_get_thread_num(); Tab*T=&nxt[me]; if(T->cap<cur[me].cap){ tdel(T); tnew(T,cur[me].cap);} else { memset(T->used,0,T->cap); T->n=0; }
      #pragma omp barrier
      for(int q=0;q<P;q++){ Tab*C=&cur[q]; for(size_t h=0;h<C->cap;h++){ if(!C->used[h]) continue; u64 m=C->s[h].key; u64 c=C->s[h].cnt;
        if(m&1){ u64 nm=m>>1; if((int)(hidx(nm,1u<<16)%P)!=me) continue; Slot*e=tget(T,nm); if(e){ u64 o=e->cnt; e->cnt+=c; if(e->cnt<o) OVF=1; } else if(keep(FR[me],pos+1,nm)) tadd(T,nm,c); continue; }
        for(int f=fst_off[pos]; f<fst_off[pos+1]; f++){ u64 tm=(1ULL<<fst[f][0])|(1ULL<<fst[f][1]); if(m&tm) continue; u64 nm=(m|tm)>>1;
          if((int)(hidx(nm,1u<<16)%P)!=me) continue; Slot*e=tget(T,nm); if(e){ u64 o=e->cnt; e->cnt+=c; if(e->cnt<o) OVF=1; } else if(keep(FR[me],pos+1,nm)) tadd(T,nm,c); } } }
    }
    Tab*sw=cur; cur=nxt; nxt=sw; size_t tot=0; for(int p=0;p<P;p++) tot+=cur[p].n; if(tot>mx) mx=tot;
    if(pos%50==0) fprintf(stderr,"pos %d/%d states %zu\n",pos,n,tot);
    if(ck && pos+1<n && difftime(time(NULL),lastck)>=cks){ char tmp[4096]; snprintf(tmp,sizeof tmp,"%s.tmp",ck); FILE*f=fopen(tmp,"wb"); int h[5]={A_,B_,Z_,EV_,pos+1};
      fwrite(h,sizeof(int),5,f); fwrite(&tot,sizeof(size_t),1,f); for(int p=0;p<P;p++) for(size_t q=0;q<cur[p].cap;q++) if(cur[p].used[q]) fwrite(&cur[p].s[q],sizeof(Slot),1,f);
      fclose(f); rename(tmp,ck); lastck=time(NULL); fprintf(stderr,"checkpoint pos %d states %zu\n",pos+1,tot); }
  }
  u128 res=0; for(int p=0;p<P;p++){ Slot*e=tget(&cur[p],0); if(e) res=e->cnt; }
  fprintf(stderr,"max states %zu overflow %d\n",mx,OVF);
  if(OVF){ printf("OVERFLOW\n"); return 5; }
  { char buf[64]; int p=63; buf[p]=0; if(!res) buf[--p]='0'; while(res){ buf[--p]='0'+(int)(res%10); res/=10; } printf("%s\n",buf+p); } return 0; }
