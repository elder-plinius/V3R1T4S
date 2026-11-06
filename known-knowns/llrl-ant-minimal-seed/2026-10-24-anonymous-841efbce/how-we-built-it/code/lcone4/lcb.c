/* lcb.c — checker B (independent of hsearch.c; written separately, sparse hash grid, no shared code).
 * Fixed-depth light-cone DFS over the colours of first-read cells (non-zero costs 1, budget K) to depth T.
 * At depth T-1 (VIOLATION) and T (MIN): for each phase p of the highway word W (read colours; obtained here from our
 * own blank-grid simulation), force the ant's reads to follow W from phase p: a known cell must hold the required
 * colour; an unknown cell is assigned it (non-zero costs 1).  After J forced periods (J = 1,2,4,..,JMAX) the now fully
 * specified state (unknown = 0) is tested with the exact translate certificate: if pose(t+P)=pose(t)+D and
 * s_{t+P}(c+D)=s_t(c) on the forward tube of the period's read cells, and that period's reads equal W, the
 * configuration is on the highway from depth (proof: attempts/sim/CERT.md).  No certificate by JMAX -> FLAG (abort).
 * Conventions: y down, 0:N 1:E 2:S 3:W, R=+1; colour c -> turn rule[c], write c+1 mod n.
 * usage: lcb RULE K T [split W wid]  ; blank highway word found from blank simulation of NB steps. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
static char *rule; static int n;
/* ---- sparse grid: open addressing, key = packed (x,y) ---- */
#define HB 22
#define HN (1u<<HB)
typedef struct{ uint64_t k; uint8_t c, kn, used; } E;
static E *tab;
static inline uint64_t key(int x,int y){ return ((uint64_t)(uint32_t)x<<32)|(uint32_t)y; }
static inline uint32_t hh(uint64_t k){ k^=k>>33; k*=0xff51afd7ed558ccdULL; k^=k>>33; return (uint32_t)k&(HN-1); }
static E* slot(int x,int y){ uint64_t k=key(x,y); uint32_t i=hh(k); while(tab[i].used && tab[i].k!=k) i=(i+1)&(HN-1);
  if(!tab[i].used){ tab[i].used=1; tab[i].k=k; tab[i].c=0; tab[i].kn=0; } return &tab[i]; }
/* undo journal */
typedef struct{ E* e; uint8_t c,kn; } J; static J *jr; static long jn=0;
static inline void put(E*e,uint8_t c,uint8_t kn){ jr[jn].e=e; jr[jn].c=e->c; jr[jn].kn=e->kn; jn++; e->c=c; e->kn=kn; }
static void rollback(long m){ while(jn>m){ jn--; jr[jn].e->c=jr[jn].c; jr[jn].e->kn=jr[jn].kn; } }
static const int mx[4]={0,1,0,-1}, my[4]={-1,0,1,0};
static inline int trn(int h,int c){ return rule[c]=='R' ? (h+1)&3 : (h+3)&3; }
static int P; static uint8_t *Wd; static int K,T,SPL=1,WID=0,JMAX=64;
static long viol=0,mins=0,leaves=0,flags=0;
static int bx[64],by[64],bc[64],nb=0;
/* blank word */
static void blankword(long NB){
  uint8_t *rd=malloc(NB); int x=0,y=0,h=0;
  for(long u=0;u<NB;u++){ E*e=slot(x,y); int c=e->c; rd[u]=c; e->c=(c+1)%n; h=trn(h,c); x+=mx[h]; y+=my[h]; }
  P=0; for(int p=1;p<=4000 && !P;p++){ int ok=1; for(long u=NB-12000;u+p<NB;u++) if(rd[u]!=rd[u+p]){ok=0;break;} if(ok)P=p; }
  if(!P){fprintf(stderr,"no blank period\n");exit(2);} long t0=NB-P; while(t0>0&&rd[t0-1]==rd[t0-1+P]) t0--;
  Wd=malloc(P); memcpy(Wd,rd+t0,P); fprintf(stderr,"blank: onset %ld period %d\n",t0,P);
  memset(tab,0,sizeof(E)*HN); free(rd);
}
/* certificate on fully specified current table (unknown cells = 0): from pose (x,y,h), period P, word phase q */
typedef struct{int x,y; uint8_t c;} CE; static CE *snap; static int *rx,*ry;
static int certify(int x,int y,int h,int q,long *cost,int budget, CE*asg,int*na){
  /* simulate one period, assigning unknown cells to 0 (they ARE 0 in the specified configuration) */
  long m=jn; int x0=x,y0=y,h0=h; int ok=1;
  for(int u=0;u<P;u++){ rx[u]=x; ry[u]=y; E*e=slot(x,y); int c=e->c; if(c!=Wd[(q+u)%P]){ok=0;break;} put(e,(c+1)%n,1); h=trn(h,c); x+=mx[h]; y+=my[h]; }
  int Dx=x-x0,Dy=y-y0; if(ok && (h!=h0 || (!Dx&&!Dy))) ok=0;
  if(ok){ /* support projection max over before (journal old values) and after (table) states */
    long mp=-(1L<<62);
    for(uint32_t i=0;i<HN;i++) if(tab[i].used && tab[i].c){ int X=(int)(int32_t)(tab[i].k>>32), Y=(int)(int32_t)(uint32_t)tab[i].k; long pj=(long)X*Dx+(long)Y*Dy; if(pj>mp)mp=pj; }
    for(long j=m;j<jn;j++) if(jr[j].c){ E*e=jr[j].e; int X=(int)(int32_t)(e->k>>32), Y=(int)(int32_t)(uint32_t)e->k; long pj=(long)X*Dx+(long)Y*Dy; if(pj>mp)mp=pj; }
    /* before-state value of a cell: oldest journal entry since m, else current */
    for(int u=0;u<P && ok;u++){ int cx=rx[u],cy=ry[u];
      while((long)cx*Dx+(long)cy*Dy<=mp){
        /* s_t(c) */ int before=-1; for(long j=m;j<jn;j++){ E*e=jr[j].e; if(e->k==key(cx,cy)){ before=jr[j].c; break; } }
        if(before<0){ E*e=slot(cx,cy); before=e->c; }
        E*f=slot(cx+Dx,cy+Dy); if(f->c!=before){ok=0;break;}
        cx+=Dx; cy+=Dy; } }
  }
  rollback(m); (void)cost;(void)budget;(void)asg;(void)na; return ok;
}
static void test(int t,int x,int y,int h,int used){
  leaves++;
  for(int p=0;p<P;p++){
    long m=jn; int cost=used, ok=1, cx=x,cy=y,ch=h; int nas=0; static int ax[64],ay[64],ac[64];
    int certified=0; long u=0;
    for(int Jp=1; Jp<=JMAX && ok && !certified; Jp*=2){
      for(; u<(long)Jp*P; u++){ E*e=slot(cx,cy); int rq=Wd[(p+u)%P];
        if(e->kn){ if(e->c!=rq){ok=0;break;} }
        else { if(rq){ if(++cost>K){ok=0;break;} ax[nas]=cx;ay[nas]=cy;ac[nas]=rq;nas++; } }
        put(e,(rq+1)%n,1); ch=trn(ch,rq); cx+=mx[ch]; cy+=my[ch]; }
      if(ok) certified=certify(cx,cy,ch,(int)((p+u)%P),0,0,0,0);
    }
    if(ok && !certified){ flags++; fprintf(stderr,"FLAG no certificate t=%d p=%d\n",t,p); }
    if(ok && certified){
      if(t==T-1) viol++; else mins++;
      printf("%s t=%d p=%d k=%d cells:",t==T-1?"VIOLATION":"MIN",t,p,cost);
      for(int i=0;i<nb;i++) printf(" (%d,%d,%d)",bx[i],by[i],bc[i]);
      for(int i=0;i<nas;i++) printf(" (%d,%d,%d)*",ax[i],ay[i],ac[i]);
      printf("\n"); }
    rollback(m);
  }
}
static long splitc=0;
static void dfs(int t,int x,int y,int h,int used){
  if(t==10 && (splitc++)%SPL!=WID) return;
  if(t>=T-1) test(t,x,y,h,used);
  if(t==T) return;
  E*e=slot(x,y);
  if(e->kn){ long m=jn; int c=e->c; put(e,(c+1)%n,1); int nh=trn(h,c); dfs(t+1,x+mx[nh],y+my[nh],nh,used); rollback(m); return; }
  for(int c=0;c<n;c++){ if(c && used>=K) break; long m=jn;
    if(c){ bx[nb]=x;by[nb]=y;bc[nb]=c;nb++; }
    put(e,(c+1)%n,1); int nh=trn(h,c); dfs(t+1,x+mx[nh],y+my[nh],nh,used+(c!=0));
    if(c) nb--; rollback(m); }
}
int main(int argc,char**argv){
  rule=argv[1]; n=strlen(rule); K=atoi(argv[2]); T=atoi(argv[3]); if(argc>5){SPL=atoi(argv[4]);WID=atoi(argv[5]);}
  long NB = argc>6? atol(argv[6]) : 400000;
  tab=calloc(HN,sizeof(E)); jr=malloc(sizeof(J)*20000000); snap=0; rx=malloc(sizeof(int)*8192); ry=malloc(sizeof(int)*8192);
  blankword(NB);
  if(T==0){ if(WID==0) test(0,0,0,0,0); }
  else dfs(0,0,0,0,0);
  printf("DONE rule=%s K=%d T=%d wid=%d/%d leaves=%ld viol=%ld mins=%ld flags=%ld\n",rule,K,T,WID,SPL,leaves,viol,mins,flags);
  return 0; }
