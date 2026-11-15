/* lant4.c - multithreaded CPU solver. Output format identical to ref/lant_ref.c (lant2):
 *   <mask> <T_cap> <vx> <vy> <dir> <steps> <CAP|UNCAPTURED_WITHIN_CAP|OUT_OF_BOUNDS>
 * usage: lant4 W H START END CAP [THREADS]      (masks START..END-1, W x H box, bit b -> cell (b%W-(W-1)/2, b/W-(H-1)/2))
 * Masks that overflow the 1024x1024 window are printed as  "<mask> -1 0 0 0 <steps> WINDOW_OVERFLOW";
 * scripts/run_chunk.sh and scripts/verify.sh replace those lines by the reference program's output. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <pthread.h>
#include "lant_core.h"
typedef struct { long tc; long steps; int vx,vy,dc,r; } Res;
static int W,H; static uint64_t ST,EN; static long CAP; static Res*res; static volatile uint64_t nextblk; static pthread_mutex_t mu=PTHREAD_MUTEX_INITIALIZER;
#define BLK 256
static void* worker(void*arg){
  (void)arg; Ant slot[KK]; Ant*A[KK];
  for(int k=0;k<KK;k++){ slot[k].G=calloc(1,PLANE_BYTES); slot[k].P=calloc(1,PLANE_BYTES); slot[k].R=malloc(sizeof(Ring)); slot[k].status=0; slot[k].idx=-1; A[k]=&slot[k]; }
  for(;;){
    pthread_mutex_lock(&mu); uint64_t b=nextblk; nextblk+=BLK; pthread_mutex_unlock(&mu);
    if(b>=EN-ST) break; uint64_t e=b+BLK<EN-ST?b+BLK:EN-ST, nx=b;
    for(;;){
      int running=0;
      for(int k=0;k<KK;k++){
        if(slot[k].status!=-1){                        /* slot free or just finished */
          if(slot[k].idx>=0){ Res*q=&res[slot[k].idx]; q->tc=slot[k].tcap;q->vx=slot[k].vx;q->vy=slot[k].vy;q->dc=slot[k].dc;q->steps=slot[k].steps;q->r=slot[k].status; slot[k].idx=-1; }
          if(nx<e){ ant_start(&slot[k],W,H,ST+nx,CAP,(long)nx); nx++; }
        }
        if(slot[k].status==-1) running++;
      }
      if(!running) break;
      ant_burst(A,4096);
    }
  }
  for(int k=0;k<KK;k++){free(slot[k].G);free(slot[k].P);free(slot[k].R);} return 0;
}
int main(int argc,char**argv){
  if(argc<6){fprintf(stderr,"usage: lant4 W H START END CAP [THREADS]\n");return 1;}
  W=atoi(argv[1]);H=atoi(argv[2]);ST=strtoull(argv[3],0,10);EN=strtoull(argv[4],0,10);CAP=atol(argv[5]);
  int T=argc>6?atoi(argv[6]):4; if(T<1)T=1; if(EN<=ST) return 0;
  res=malloc(sizeof(Res)*(EN-ST)); nextblk=0;
  pthread_t th[256]; for(int i=0;i<T&&i<256;i++) pthread_create(&th[i],0,worker,0);
  for(int i=0;i<T&&i<256;i++) pthread_join(th[i],0);
  for(uint64_t i=0;i<EN-ST;i++) printf("%llu %ld %d %d %d %ld %s\n",(unsigned long long)(ST+i),res[i].tc,res[i].vx,res[i].vy,res[i].dc,res[i].steps,lant_status_name(res[i].r));
  return 0;
}
