/* ant.c — exact generalised-ant simulator + highway certificate (run 2026-10-24-1428).
 * Conventions (PREREG): y down, headings 0:N(0,-1) 1:E 2:S 3:W, R = +1 (clockwise), L = -1.
 * On colour c: turn rule[c], write c+1 mod n, step. Ant at (0,0) facing N.
 * usage: ant RULE NSTEPS [seedfile|-] [PMAX] [wordout]
 *   seedfile lines "x y colour". Prints the onset t0 (least t with read sequence P-periodic from t, checked on
 *   [t, NSTEPS)), period P (least), drift D, and the translate-certificate verdict at t0 (CERT OK = proof that
 *   the run is periodic forever from t0) and at t0-1 (must fail). Writes the period word (read colours from t0) to wordout. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define LG 12
#define SZ (1<<LG)
#define C0 (SZ/2)
static const int DX[4]={0,1,0,-1}, DY[4]={-1,0,1,0};
static unsigned char *G0;
static char rule[32]; static int n;
static long NS; static unsigned char *r; static int *X,*Y; static unsigned char *H;
static void load(unsigned char *g,const char*f){ memset(g,0,(size_t)SZ*SZ); if(!f||!strcmp(f,"-"))return; FILE*F=fopen(f,"r"); int x,y,c; while(fscanf(F,"%d %d %d",&x,&y,&c)==3) g[(size_t)(y+C0)*SZ+x+C0]=c; fclose(F);}
static void step(unsigned char*g,int*x,int*y,int*h,unsigned char*rd){ size_t i=(size_t)*y*SZ+*x; int c=g[i]; if(rd)*rd=c; *h=(*h+(rule[c]=='R'?1:3))&3; g[i]=(c+1)%n; *x+=DX[*h]; *y+=DY[*h]; if(*x<4||*y<4||*x>SZ-5||*y>SZ-5){fprintf(stderr,"EDGE\n");exit(3);} }
/* translate certificate at time t with period P: returns 1 if it holds */
static int cert(const char*seed,long t,long P){
  unsigned char *S0=malloc((size_t)SZ*SZ),*S1=malloc((size_t)SZ*SZ); load(S0,seed);
  int x=C0,y=C0,h=0; for(long u=0;u<t;u++) step(S0,&x,&y,&h,0);
  memcpy(S1,S0,(size_t)SZ*SZ); int x0=x,y0=y,h0=h;
  int *ax=malloc(sizeof(int)*P),*ay=malloc(sizeof(int)*P);
  for(long u=0;u<P;u++){ax[u]=x;ay[u]=y; step(S1,&x,&y,&h,0);}
  int Dx=x-x0,Dy=y-y0; int ok=(h==h0)&&(Dx||Dy);
  long mp=-(1L<<60); /* max projection of support of S0,S1 */
  for(size_t i=0;i<(size_t)SZ*SZ;i++) if(S0[i]||S1[i]){ long q=(long)((int)(i%SZ)-C0)*Dx+(long)((int)(i/SZ)-C0)*Dy; if(q>mp)mp=q; }
  long checked=0;
  for(long u=0;ok&&u<P;u++){ int cx=ax[u],cy=ay[u];
    for(;;){ long q=(long)(cx-C0)*Dx+(long)(cy-C0)*Dy; if(q>mp) break; /* both states zero from here on along the tube */
      if(S1[(size_t)(cy+Dy)*SZ+cx+Dx]!=S0[(size_t)cy*SZ+cx]){ok=0;break;} checked++;
      cx+=Dx; cy+=Dy; } }
  fprintf(stderr,"cert t=%ld P=%ld D=(%d,%d) heading %d->%d checked=%ld : %s\n",t,P,Dx,Dy,h0,h,checked,ok?"OK":"FAIL");
  free(S0);free(S1);free(ax);free(ay); return ok;
}
int main(int argc,char**argv){
  strcpy(rule,argv[1]); n=strlen(rule); NS=atol(argv[2]); const char*seed=argc>3?argv[3]:"-"; int PMAX=argc>4?atoi(argv[4]):2000;
  G0=malloc((size_t)SZ*SZ); load(G0,seed); r=malloc(NS); X=malloc(sizeof(int)*(NS+1)); Y=malloc(sizeof(int)*(NS+1)); H=malloc(NS+1);
  int x=C0,y=C0,h=0; for(long u=0;u<NS;u++){X[u]=x;Y[u]=y;H[u]=h; step(G0,&x,&y,&h,&r[u]);}
  X[NS]=x;Y[NS]=y;H[NS]=h;
  long P=-1; for(int p=1;p<=PMAX;p++){ long lo=NS-4L*PMAX; if(lo<0)lo=0; int ok=1; for(long u=lo;u+p<NS;u++) if(r[u]!=r[u+p]){ok=0;break;} if(ok){P=p;break;} }
  if(P<0){ printf("RESULT rule=%s N=%ld NO_PERIOD(<=%d in tail)\n",rule,NS,PMAX); return 0; }
  long t0=NS-P; while(t0>0 && r[t0-1]==r[t0-1+P]) t0--;
  int Dx=X[t0+P]-X[t0],Dy=Y[t0+P]-Y[t0];
  if(Dx==0&&Dy==0){ printf("RESULT rule=%s N=%ld PERIODIC_NO_DRIFT P=%ld t0=%ld\n",rule,NS,P,t0); return 0; }
  int c1=cert(seed,t0,P); int c0= t0>0? cert(seed,t0-1,P) : 0;
  /* canonical class: least rotation of the period word */
  long best=0; for(long s=1;s<P;s++){ for(long i=0;i<P;i++){ int a=r[t0+(s+i)%P], b=r[t0+(best+i)%P]; if(a!=b){ if(a<b) best=s; break; } } }
  unsigned long hsh=1469598103934665603UL; for(long i=0;i<P;i++){hsh^=r[t0+(best+i)%P]; hsh*=1099511628211UL;}
  printf("RESULT rule=%s N=%ld onset=%ld P=%ld D=(%d,%d) heading_at_onset=%d cert_at_onset=%s cert_at_onset-1=%s class=%016lx\n",rule,NS,t0,P,Dx,Dy,H[t0],c1?"OK":"FAIL",c0?"OK":"FAIL",hsh);
  if(argc>5){ FILE*F=fopen(argv[5],"w"); for(long i=0;i<P;i++) fputc('0'+r[t0+i],F); fputc('\n',F); fclose(F); }
  return 0;
}
