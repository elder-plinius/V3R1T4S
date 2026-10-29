/* Greedy redundant-block removal for a (v,k,t) covering (0-based blocks, one per line).
   Usage: prune V K T IN OUT ORDER SEED MAXSEC
   ORDER: 0 = file order, 1 = reverse, 2 = random (SEED), 3 = parts-first: blocks in IN.parts order given by
   lexicographically sorted part label descending (j-high first), then random within.
   Counts: uint8 saturating at 255 if C(v,t) <= 1.2e9, else 2-bit saturating at 3 (stored <= true count, so conservative).
   A block is removed iff every t-subset has stored count >= 2. Single pass is maximal (counts only decrease). */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <time.h>
typedef unsigned long long u64;
static u64 C[128][16]; static int v,k,t; static uint8_t *cnt; static int two;
static inline unsigned get(u64 r){ if(!two) return cnt[r]; return (cnt[r>>2]>>((r&3)*2))&3; }
static inline void inc(u64 r){ if(!two){ if(cnt[r]<255) cnt[r]++; return;} unsigned c=get(r); if(c<3){ cnt[r>>2]+= (uint8_t)(1u<<((r&3)*2)); } }
static inline void dec(u64 r){ if(!two){ cnt[r]--; /* saturated cap: stored=min(true,255) then always decrement => stored<=true (conservative) */ return;} unsigned c=get(r); if(c==3) { cnt[r>>2]-= (uint8_t)(1u<<((r&3)*2)); return;} cnt[r>>2]-= (uint8_t)(1u<<((r&3)*2)); }
/* note: decrementing a saturated 2-bit 3 to 2 keeps stored<=true. uint8 at 255 is left (true>=255 still >=2 after many decs is not guaranteed, but 255 is never reached here; we abort if it is). */
static int sat8=0;
#define FORSUB(blk, BODY) { int idx[16]; for(int i=0;i<t;i++) idx[i]=i; for(;;){ u64 r=0; for(int i=0;i<t;i++) r+=C[blk[idx[i]]][i+1]; BODY; int i=t-1; while(i>=0 && idx[i]==k-t+i) i--; if(i<0) break; idx[i]++; for(int j=i+1;j<t;j++) idx[j]=idx[j-1]+1; } }
static u64 rng; static u64 nxt(void){ rng^=rng<<13; rng^=rng>>7; rng^=rng<<17; return rng; }
int main(int argc,char**argv){
  if(argc!=9){fprintf(stderr,"usage\n");return 2;}
  v=atoi(argv[1]);k=atoi(argv[2]);t=atoi(argv[3]); int order=atoi(argv[6]); rng=strtoull(argv[7],0,10)*2654435761ULL+12345; double maxsec=atof(argv[8]);
  for(int n=0;n<128;n++){C[n][0]=1;for(int r=1;r<16;r++)C[n][r]=(n==0)?0:C[n-1][r-1]+C[n-1][r];}
  FILE*f=fopen(argv[4],"r"); size_t cap=1<<18,nb=0; uint8_t*B=malloc(cap*k); char line[4096];
  while(fgets(line,sizeof line,f)){ char*p=line,*e; int c=0; if(nb==cap){cap*=2;B=realloc(B,cap*k);}
    for(;;){ long x=strtol(p,&e,10); if(e==p)break; B[nb*k+c++]=(uint8_t)x; p=e; } if(c==0) continue; if(c!=k){fprintf(stderr,"bad block\n");return 1;}
    for(int j=1;j<k;j++){uint8_t y=B[nb*k+j];int m=j-1;while(m>=0&&B[nb*k+m]>y){B[nb*k+m+1]=B[nb*k+m];m--;}B[nb*k+m+1]=y;} nb++; }
  fclose(f);
  char **lab=NULL; if(order==3){ char pn[4096]; snprintf(pn,sizeof pn,"%s.parts",argv[4]); FILE*g=fopen(pn,"r"); lab=malloc(nb*sizeof(char*)); for(size_t i=0;i<nb;i++){ if(!fgets(line,sizeof line,g)) {fprintf(stderr,"parts short\n");return 1;} line[strcspn(line,"\n")]=0; lab[i]=strdup(line);} fclose(g); }
  u64 N=C[v][t]; two = N>1200000000ULL; cnt = calloc(two? (N>>2)+1 : N, 1); if(!cnt){fprintf(stderr,"oom\n");return 1;}
  clock_t t0=clock();
  for(size_t i=0;i<nb;i++){ uint8_t*b=B+i*k; FORSUB(b, inc(r)); }
  if(!two){ for(u64 r=0;r<N;r++) if(cnt[r]==255){sat8=1;break;} }
  u64 unc=0; for(u64 r=0;r<N;r++) if(get(r)==0) unc++;
  fprintf(stderr,"loaded nb=%zu N=%llu two=%d sat=%d uncovered=%llu %.1fs\n",nb,N,two,sat8,unc,(double)(clock()-t0)/CLOCKS_PER_SEC);
  size_t *ord=malloc(nb*sizeof(size_t)); for(size_t i=0;i<nb;i++) ord[i]=(order==1)?nb-1-i:i;
  if(order==2||order==3){ for(size_t i=nb-1;i>0;i--){ size_t j=nxt()%(i+1); size_t x=ord[i];ord[i]=ord[j];ord[j]=x; } }
  if(order==3){ /* stable sort by label descending (insertion by buckets) */
    size_t *o2=malloc(nb*sizeof(size_t)), m=0; char seen[64][16]; int ns=0;
    for(size_t i=0;i<nb;i++){ int f2=0; for(int s=0;s<ns;s++) if(!strcmp(seen[s],lab[i])) f2=1; if(!f2&&ns<64) strcpy(seen[ns++],lab[i]); }
    for(int a=0;a<ns;a++) for(int b2=a+1;b2<ns;b2++) if(strcmp(seen[a],seen[b2])<0){ char tmp[16]; strcpy(tmp,seen[a]); strcpy(seen[a],seen[b2]); strcpy(seen[b2],tmp); }
    for(int s=0;s<ns;s++) for(size_t i=0;i<nb;i++) if(!strcmp(lab[ord[i]],seen[s])) o2[m++]=ord[i];
    free(ord); ord=o2; }
  uint8_t *dead=calloc(nb,1); size_t removed=0;
  for(size_t ii=0;ii<nb;ii++){ size_t i=ord[ii]; uint8_t*b=B+i*k; int ok=1;
    FORSUB(b, if(get(r)<2){ok=0;break;});
    if(ok){ FORSUB(b, dec(r)); dead[i]=1; removed++; }
    if((ii&4095)==0 && (double)(clock()-t0)/CLOCKS_PER_SEC>maxsec){ fprintf(stderr,"time cap at ii=%zu\n",ii); break; } }
  FILE*o=fopen(argv[5],"w"); size_t kept=0;
  for(size_t i=0;i<nb;i++) if(!dead[i]){ for(int j=0;j<k;j++) fprintf(o,j?" %d":"%d",B[i*k+j]); fputc('\n',o); kept++; }
  fclose(o);
  printf("prune order=%d seed=%s in=%zu removed=%zu kept=%zu sat=%d secs=%.1f\n",order,argv[7],nb,removed,kept,sat8,(double)(clock()-t0)/CLOCKS_PER_SEC);
  return 0;
}
