/* benzZ.c - exact count of stones-and-bones tilings (T113) of the (a,b)-benzel (Propp, arXiv:2206.06472).
   Row-sweep frontier DP (state = covered-bit mask of the next W cells, 64-bit) with exact unsigned __int128
   counts (overflow-checked) and SOUND pruning: a successor state is dropped only if a complete MRV exact-cover
   search proves that the uncovered cells of the next K rows cannot all be covered by tiles lying inside the
   uncovered part of the region (a necessary condition for completing the tiling). Undecided searches
   (node limit) keep the state. Pruning therefore never changes the count.
   Usage: benzZ a b K [nodelimit] */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <omp.h>
#include <time.h>
typedef unsigned __int128 u128; typedef uint64_t u64;
static int A,B,K,NL=4000;
static int inb(int i,int j){int k=1-i-j;int x=j-i,y=k-j,z=i-k;return x>=-(A-1)&&x<=B-1&&y>=-(A-1)&&y<=B-1&&z>=-(A-1)&&z<=B-1;}
typedef struct{int i,j;} Cell; static Cell*cells; static int nc,R,*gidx;
static int cmpc(const void*p,const void*q){const Cell*x=p,*y=q;if(x->i!=y->i)return x->i-y->i;return x->j-y->j;}
static int gid(int i,int j){if(i<-R||i>R||j<-R||j>R)return -1;return gidx[(i+R)*(2*R+1)+(j+R)];}
static int (*TL)[3]; static int nt; static int *covs,*covn; /* cov lists: covs[x*20+..] */
static int *rowof,*rowstart,nrows; static int *cnt; static int (*ts)[2];
typedef struct{uint8_t*fr;long long nodes,checks,kills,undec;int zend;} Ctx;
static int rec(Ctx*c,int t){
 uint8_t*fr=c->fr; if(++c->nodes>NL)return 2;
 int best=-1,bn=99,bo[20];
 for(int x=t;x<c->zend;x++){ if(!fr[x])continue; int o[20],n=0; int *cl=covs+x*20;
   for(int q=0;q<covn[x];q++){int k=cl[q];if(fr[TL[k][0]]&&fr[TL[k][1]]&&fr[TL[k][2]])o[n++]=k;}
   if(n==0)return 0; if(n<bn){bn=n;best=x;memcpy(bo,o,sizeof(int)*n);if(n==1)break;} }
 if(best<0)return 1;
 int und=0;
 for(int q=0;q<bn;q++){int k=bo[q];fr[TL[k][0]]=fr[TL[k][1]]=fr[TL[k][2]]=0;int r=rec(c,t);fr[TL[k][0]]=fr[TL[k][1]]=fr[TL[k][2]]=1;
   if(r==1)return 1; if(r==2){und=1;break;}}
 return und?2:0;}
static int W;
static int MSTEP=1;
static int check(Ctx*c,int t,u64 s){ /* state s at step t (bit q = cell t+q covered) */
 if(t>=nc)return s==0; if(t%MSTEP)return 1; uint8_t*fr=c->fr;
 c->checks++; int r0=rowof[t]; int zr=r0+K; c->zend=(zr+1>=nrows)?nc:rowstart[zr+1];
 int fend=(zr+3>=nrows)?nc:rowstart[zr+3];
 for(int x=t;x<fend;x++){int q=x-t;fr[x]=!(q<W&&((s>>q)&1));}
 c->nodes=0;int r=rec(c,t);
 for(int x=t;x<fend;x++)fr[x]=0;
 if(r==0)c->kills++; if(r==2)c->undec++;
 return r!=0;}
typedef struct{u64 k;u64 v;} Ent; /* u64 counts; every addition is overflow-checked, run aborts on overflow */
typedef struct{Ent*T;uint8_t*U;size_t cap,n;} Map;
static inline size_t hsh(u64 k,size_t cap){u64 h=k*0x9E3779B97F4A7C15ULL;h^=h>>31;h*=0xBF58476D1CE4E5B9ULL;h^=h>>29;return h&(cap-1);}
static void minit(Map*m,size_t cap){m->cap=cap;m->n=0;m->T=malloc(sizeof(Ent)*cap);m->U=calloc(cap,1);if(!m->T||!m->U){fprintf(stderr,"OOM\n");exit(2);}}
static void mfree(Map*m){free(m->T);free(m->U);}
static int overflow=0;
static Ent* mfind(Map*m,u64 k){size_t h=hsh(k,m->cap);while(m->U[h]){if(m->T[h].k==k)return &m->T[h];h=(h+1)&(m->cap-1);}return NULL;}
static void mput(Map*m,u64 k,u64 v);
static void mgrow(Map*m){Map o=*m;minit(m,o.cap*2);for(size_t x=0;x<o.cap;x++)if(o.U[x])mput(m,o.T[x].k,o.T[x].v);mfree(&o);}
static void mput(Map*m,u64 k,u64 v){if((m->n+1)*20>m->cap*17)mgrow(m);size_t h=hsh(k,m->cap);while(m->U[h]){if(m->T[h].k==k){u64 o=m->T[h].v;m->T[h].v=o+v;if(m->T[h].v<o)overflow=1;return;}h=(h+1)&(m->cap-1);}m->U[h]=1;m->T[h].k=k;m->T[h].v=v;m->n++;}
static void pr128(u128 x){char s[64];int p=63;s[p]=0;if(!x){printf("0");return;}while(x){s[--p]='0'+(int)(x%10);x/=10;}printf("%s",s+p);}
int main(int argc,char**argv){
 A=atoi(argv[1]);B=atoi(argv[2]);K=atoi(argv[3]);if(argc>4)NL=atoi(argv[4]);
 R=2*(A+B)+4;gidx=malloc(sizeof(int)*(2*R+1)*(2*R+1));cells=malloc(sizeof(Cell)*(2*R+1)*(2*R+1));nc=0;
 for(int i=-R;i<=R;i++)for(int j=-R;j<=R;j++)if(inb(i,j)){cells[nc].i=i;cells[nc].j=j;nc++;}
 qsort(cells,nc,sizeof(Cell),cmpc);for(int x=0;x<(2*R+1)*(2*R+1);x++)gidx[x]=-1;for(int x=0;x<nc;x++)gidx[(cells[x].i+R)*(2*R+1)+(cells[x].j+R)]=x;
 rowof=malloc(sizeof(int)*nc);rowstart=malloc(sizeof(int)*(nc+1));nrows=0;for(int x=0;x<nc;x++){if(x==0||cells[x].i!=cells[x-1].i)rowstart[nrows++]=x;rowof[x]=nrows-1;}
 /* tiles: bones c,c+d,c+2d for d in {(1,-1),(1,0),(0,1)}; stones: the two triangle shapes {c,c+(0,1),c+(1,0)} and {c,c+(1,-1),c+(1,0)} */
 TL=malloc(sizeof(int)*3*nc*5);nt=0;int sh[5][2][2]={{{1,-1},{2,-2}},{{1,0},{2,0}},{{0,1},{0,2}},{{0,1},{1,0}},{{1,-1},{1,0}}};
 for(int x=0;x<nc;x++)for(int s=0;s<5;s++){int y=gid(cells[x].i+sh[s][0][0],cells[x].j+sh[s][0][1]),z=gid(cells[x].i+sh[s][1][0],cells[x].j+sh[s][1][1]);if(y>=0&&z>=0){TL[nt][0]=x;TL[nt][1]=y;TL[nt][2]=z;nt++;}}
 covs=malloc(sizeof(int)*nc*20);covn=calloc(nc,sizeof(int));
 for(int k=0;k<nt;k++)for(int u=0;u<3;u++){int x=TL[k][u];if(covn[x]>=20){fprintf(stderr,"cov overflow\n");return 4;}covs[x*20+covn[x]++]=k;}
 W=0;cnt=calloc(nc+1,sizeof(int));for(int k=0;k<nt;k++){int mn=TL[k][0],a1=TL[k][1],a2=TL[k][2];/* x is min? */
   int m=mn;if(a1<m)m=a1;if(a2<m)m=a2;if(m!=mn){fprintf(stderr,"min order\n");return 5;} if(a1-mn+1>W)W=a1-mn+1;if(a2-mn+1>W)W=a2-mn+1;cnt[mn+1]++;}
 for(int x=0;x<nc;x++)cnt[x+1]+=cnt[x];ts=malloc(sizeof(int)*2*nt);int*pos=calloc(nc,sizeof(int));for(int k=0;k<nt;k++){int a0=TL[k][0];int p=cnt[a0]+pos[a0]++;ts[p][0]=TL[k][1]-a0;ts[p][1]=TL[k][2]-a0;}
 fprintf(stderr,"a=%d b=%d cells=%d rows=%d tiles=%d window=%d K=%d NL=%d\n",A,B,nc,nrows,nt,W,K,NL);
 if(W>64){fprintf(stderr,"window>64\n");return 3;} if(nc%3){printf("0\n");return 0;}
 if(getenv("BENZ_M"))MSTEP=atoi(getenv("BENZ_M")); int P=omp_get_max_threads(); Ctx*ctx=calloc(P,sizeof(Ctx)); for(int p=0;p<P;p++)ctx[p].fr=calloc(nc+8,1);
 Map*cur=calloc(P,sizeof(Map)),*nxt=calloc(P,sizeof(Map)); for(int p=0;p<P;p++){minit(&cur[p],1024);minit(&nxt[p],1024);}
 int t0=0; const char*ck=getenv("BENZ_CKPT"); double ckint=getenv("BENZ_CKPT_SEC")?atof(getenv("BENZ_CKPT_SEC")):600; 
 if(ck){FILE*f=fopen(ck,"rb"); if(f){int a_,b_,K_,t_;size_t n_; if(fread(&a_,4,1,f)==1&&fread(&b_,4,1,f)==1&&fread(&K_,4,1,f)==1&&fread(&t_,4,1,f)==1&&fread(&n_,8,1,f)==1&&a_==A&&b_==B){
   for(size_t q=0;q<n_;q++){Ent e;if(fread(&e,sizeof(Ent),1,f)!=1){fprintf(stderr,"bad ckpt\n");return 7;} mput(&cur[hsh(e.k,1ULL<<20)%P],e.k,e.v);} t0=t_; fprintf(stderr,"resumed t=%d states=%zu\n",t0,n_);} fclose(f);} }
 if(t0==0) mput(&cur[hsh(0,1ULL<<20)%P],0,1);
 size_t peak=1,sum=0; time_t lastck=time(NULL);
 for(int t=t0;t<nc;t++){
  #pragma omp parallel num_threads(P)
  { int p=omp_get_thread_num(); Map*m=&nxt[p]; size_t want=cur[p].cap; if(m->cap<want){mfree(m);minit(m,want);}else{memset(m->U,0,m->cap);m->n=0;}
   #pragma omp barrier
   for(int q=0;q<P;q++){Map*c=&cur[q]; for(size_t h=0;h<c->cap;h++)if(c->U[h]){u64 s=c->T[h].k;u64 v=c->T[h].v;
     if(s&1){u64 ns=s>>1; if((int)(hsh(ns,1ULL<<20)%P)!=p)continue; Ent*e=mfind(m,ns);if(e){u64 o=e->v;e->v+=v;if(e->v<o)overflow=1;}else if(check(&ctx[p],t+1,ns))mput(m,ns,v);continue;}
     for(int pp=cnt[t];pp<cnt[t+1];pp++){u64 mk=((u64)1<<ts[pp][0])|((u64)1<<ts[pp][1]);if(s&mk)continue;u64 ns=(s|mk)>>1; if((int)(hsh(ns,1ULL<<20)%P)!=p)continue;
       Ent*e=mfind(m,ns);if(e){u64 o=e->v;e->v+=v;if(e->v<o)overflow=1;}else if(check(&ctx[p],t+1,ns))mput(m,ns,v);}}}
  }
  Map*tm=cur;cur=nxt;nxt=tm; size_t tot=0;for(int p=0;p<P;p++)tot+=cur[p].n; if(tot>peak)peak=tot;sum+=tot;
  long long ch=0,ki=0,un=0;for(int p=0;p<P;p++){ch+=ctx[p].checks;ki+=ctx[p].kills;un+=ctx[p].undec;}
  if(t%25==0)fprintf(stderr,"t=%d/%d states=%zu checks=%lld kills=%lld undec=%lld\n",t,nc,tot,ch,ki,un);
  if(ck && difftime(time(NULL),lastck)>=ckint && t+1<nc){ char tmp[4096];snprintf(tmp,sizeof tmp,"%s.tmp",ck);FILE*f=fopen(tmp,"wb");int tn=t+1;
    fwrite(&A,4,1,f);fwrite(&B,4,1,f);fwrite(&K,4,1,f);fwrite(&tn,4,1,f);fwrite(&tot,8,1,f);
    for(int p=0;p<P;p++)for(size_t h=0;h<cur[p].cap;h++)if(cur[p].U[h])fwrite(&cur[p].T[h],sizeof(Ent),1,f);
    fclose(f);rename(tmp,ck);lastck=time(NULL);fprintf(stderr,"checkpoint t=%d states=%zu\n",tn,tot);}
 }
 long long ch=0,ki=0,un=0;for(int p=0;p<P;p++){ch+=ctx[p].checks;ki+=ctx[p].kills;un+=ctx[p].undec;}
 long long checks=ch,kills=ki,undec=un; Ent*e=NULL; for(int p=0;p<P&&!e;p++)e=mfind(&cur[p],0);
u128 ans=e?(u128)e->v:0;
 fprintf(stderr,"peak_states=%zu sum_states=%zu checks=%lld kills=%lld undecided=%lld overflow=%d\n",peak,sum,checks,kills,undec,overflow);
 if(overflow){printf("OVERFLOW\n");return 6;}
 pr128(ans);printf("\n");return 0;}
