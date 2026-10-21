/* mc2: min-conflicts local search for families of m distinct binary vectors of length n whose pairwise ORs are distinct.
   usage: mc2 n m seconds seed outfile [initfile]   ; writes outfile on success (cost 0) and checkpoints best to outfile.best */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <time.h>
#include <math.h>
static uint64_t rs; static inline uint64_t rnd(){rs^=rs<<13;rs^=rs>>7;rs^=rs<<17;return rs;}
#define HB 23
#define HS (1u<<HB)
static uint32_t *hk; static int32_t *hc;
static inline uint32_t hh(uint32_t k){return (uint32_t)((k*2654435761u)^(k>>13))&(HS-1);}
static int32_t *slot(uint32_t k){uint32_t h=hh(k);while(hc[h]>=0&&hk[h]!=k){h=(h+1)&(HS-1);} return &hc[h];}
static int32_t getc_(uint32_t k){uint32_t h=hh(k);while(hc[h]>=0){if(hk[h]==k)return hc[h];h=(h+1)&(HS-1);}return 0;}
static void addk(uint32_t k,int d){uint32_t h=hh(k);while(hc[h]>=0&&hk[h]!=k)h=(h+1)&(HS-1);if(hc[h]<0){hk[h]=k;hc[h]=0;}hc[h]+=d;}
int n,m; uint32_t *x; long cost;
static void rem(int i){for(int j=0;j<m;j++)if(j!=i){uint32_t u=x[i]|x[j];int c=getc_(u);if(c>=2)cost-=1;addk(u,-1);}}
static void add(int i){for(int j=0;j<m;j++)if(j!=i){uint32_t u=x[i]|x[j];int c=getc_(u);if(c>=1)cost+=1;addk(u,1);}}
static int cmpu(const void*a,const void*b){uint32_t p=*(uint32_t*)a,q=*(uint32_t*)b;return p<q?-1:p>q;}
static uint32_t *tmp;
static long addcost(int i,uint32_t y){long c=0;int t=0;for(int j=0;j<m;j++)if(j!=i){uint32_t u=y|x[j];c+=getc_(u)>0;tmp[t++]=u;}
  qsort(tmp,t,4,cmpu);for(int a=1;a<t;a++)if(tmp[a]==tmp[a-1])c++;return c;}
static long conf(int i){long c=0;for(int j=0;j<m;j++)if(j!=i)c+=getc_(x[i]|x[j])>1;return c;}
int main(int argc,char**argv){n=atoi(argv[1]);m=atoi(argv[2]);double secs=atof(argv[3]);rs=0x9E3779B97F4A7C15ull^atoll(argv[4]);char*out=argv[5];
  hk=malloc(4u*HS);hc=malloc(4u*HS);memset(hc,0xff,4u*HS);x=malloc(4*m);tmp=malloc(4*m);
  uint32_t M=(n==32)?0xffffffffu:((1u<<n)-1);int k0=0;
  if(argc>6){FILE*f=fopen(argv[6],"r");char s[64];while(k0<m&&fscanf(f," %63[01]",s)==1){x[k0++]=(uint32_t)strtoul(s,0,2);int ch;while((ch=fgetc(f))!=EOF&&ch!='0'&&ch!='1');if(ch!=EOF)ungetc(ch,f);}fclose(f);}
  for(int i=k0;i<m;i++)x[i]=(uint32_t)rnd()&M&(uint32_t)rnd();
  memset(hc,0xff,4u*HS);cost=0;
  for(int i=0;i<m;i++)for(int j=i+1;j<m;j++){uint32_t u=x[i]|x[j];if(getc_(u)>=1)cost++;addk(u,1);}
  long best=cost;time_t t0=time(0);long it=0;double T=0.6;FILE*lg=fopen(strcat(strcpy(malloc(strlen(out)+8),out),".log"),"a");
  fprintf(lg,"start n=%d m=%d cost=%ld\n",n,m,cost);fflush(lg);
  while(cost>0&&difftime(time(0),t0)<secs){it++;
    int i=rnd()%m;for(int r=0;r<4;r++){int j=rnd()%m;if(conf(j)>conf(i))i=j;}
    rem(i);uint32_t old=x[i];long bc=1L<<60;uint32_t by=old;int nb=0;
    for(int b=0;b<n+6;b++){uint32_t y=(b<n)?(old^(1u<<b)):((uint32_t)rnd()&M&(uint32_t)rnd());long c=addcost(i,y);
      if(c<bc){bc=c;by=y;nb=1;}else if(c==bc&&rnd()%(++nb)==0)by=y;}
    long c0=addcost(i,old);
    if(bc<=c0||exp(-(double)(bc-c0)/T)>(rnd()%1000000)/1e6)x[i]=by;else x[i]=old;
    add(i);
    if(cost<best){best=cost;FILE*f=fopen(strcat(strcpy(malloc(strlen(out)+8),out),".best"),"w");for(int a=0;a<m;a++){for(int b=n-1;b>=0;b--)fputc('0'+((x[a]>>b)&1),f);fputc('\n',f);}fclose(f);}
    if(it%200000==0){fprintf(lg,"it=%ld cost=%ld best=%ld t=%.0f\n",it,cost,best,difftime(time(0),t0));fflush(lg);}
  }
  fprintf(lg,"end it=%ld cost=%ld best=%ld t=%.0f %s\n",it,cost,best,difftime(time(0),t0),cost==0?"FOUND":"no");fclose(lg);
  if(cost==0){FILE*f=fopen(out,"w");for(int a=0;a<m;a++){for(int b=n-1;b>=0;b--)fputc('0'+((x[a]>>b)&1),f);fputc('\n',f);}fclose(f);printf("FOUND\n");return 0;}
  printf("best cost %ld\n",best);return 1;}
