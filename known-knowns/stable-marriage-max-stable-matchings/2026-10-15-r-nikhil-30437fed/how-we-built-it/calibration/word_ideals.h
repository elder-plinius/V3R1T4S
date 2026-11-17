/* Independent direct heap-of-swaps ideal counter; no existing rotation code used.
   Strict chronological men/reverse chronological women, no repeated pair.
   Include in C/C++ and call wi_count(n,len,initial,gates); check wi_error.
   gates is a flat array of 2*len zero-based man labels. Not thread-safe. */
#ifndef WORD_IDEALS_H
#define WORD_IDEALS_H
#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#include <limits.h>
#define WI_MAX 512
#define WI_WORDS 8
#define WI_CAP (1u<<18)
typedef struct {uint64_t b[WI_WORDS];} WISet;
typedef struct {WISet key;uint64_t value;uint32_t stamp;} WIEntry;
static WISet wi_anc[WI_MAX],wi_desc[WI_MAX];
static WIEntry *wi_table=NULL;
static int wi_words,wi_len,wi_error;
static uint32_t wi_stamp=0;
static uint64_t wi_calls,wi_states;
static int wi_empty(WISet x){for(int j=0;j<wi_words;j++)if(x.b[j])return 0;return 1;}
static uint64_t wi_hash(WISet x){uint64_t h=UINT64_C(0x9e3779b97f4a7c15);for(int j=0;j<wi_words;j++){uint64_t z=x.b[j];z^=z>>30;z*=UINT64_C(0xbf58476d1ce4e5b9);z^=z>>27;z*=UINT64_C(0x94d049bb133111eb);h^=z^(z>>31);h=(h<<17)|(h>>47);}return h;}
static int wi_equal(WISet a,WISet b){for(int j=0;j<wi_words;j++)if(a.b[j]!=b.b[j])return 0;return 1;}
static uint64_t wi_dp(WISet live){
 wi_calls++;if(wi_error)return 0;if(wi_empty(live))return 1;
 unsigned slot=(unsigned)wi_hash(live)&(WI_CAP-1),probes=0;
 while(wi_table[slot].stamp==wi_stamp){if(wi_equal(wi_table[slot].key,live))return wi_table[slot].value;slot=(slot+1)&(WI_CAP-1);if(++probes==WI_CAP){wi_error=3;return 0;}}
 uint64_t total=0;WISet component={{0}},frontier={{0}};int first=-1;
 for(int j=0;j<wi_words;j++)if(live.b[j]){first=64*j+__builtin_ctzll(live.b[j]);break;}
 component.b[first/64]=frontier.b[first/64]=UINT64_C(1)<<(first%64);
 while(!wi_empty(frontier)){
  WISet next={{0}};
  for(int block=0;block<wi_words;block++){uint64_t bits=frontier.b[block];while(bits){int k=64*block+__builtin_ctzll(bits);bits&=bits-1;for(int j=0;j<wi_words;j++)next.b[j]|=(wi_anc[k].b[j]|wi_desc[k].b[j])&live.b[j]&~component.b[j];}}
  for(int j=0;j<wi_words;j++)component.b[j]|=next.b[j];frontier=next;
 }
 if(!wi_equal(component,live)){
  WISet rest=live;for(int j=0;j<wi_words;j++)rest.b[j]&=~component.b[j];
  uint64_t a=wi_dp(component),b=wi_dp(rest);if(b&&a>UINT64_MAX/b){wi_error=2;return 0;}total=a*b;
 }else{
 int pivot=-1,balance=-1,product=-1;
 for(int block=0;block<wi_words;block++){uint64_t bits=live.b[block];while(bits){int k=block*64+__builtin_ctzll(bits);bits&=bits-1;int a=0,d=0;for(int j=0;j<wi_words;j++){a+=__builtin_popcountll(live.b[j]&wi_anc[k].b[j]);d+=__builtin_popcountll(live.b[j]&wi_desc[k].b[j]);}int b=a<d?a:d;if(b>balance||(b==balance&&a*d>product)){pivot=k;balance=b;product=a*d;}}}
 WISet yes=live,no=live;for(int j=0;j<wi_words;j++){yes.b[j]&=~wi_anc[pivot].b[j];no.b[j]&=~wi_desc[pivot].b[j];}
 uint64_t a=wi_dp(yes),b=wi_dp(no);if(UINT64_MAX-a<b){wi_error=2;return 0;}total=a+b;
 }
 /* Recursive insertions may occupy the previously found empty slot. */
 slot=(unsigned)wi_hash(live)&(WI_CAP-1);probes=0;
 while(wi_table[slot].stamp==wi_stamp){if(wi_equal(wi_table[slot].key,live))return wi_table[slot].value;slot=(slot+1)&(WI_CAP-1);if(++probes==WI_CAP){wi_error=3;return 0;}}
 wi_table[slot].key=live;wi_table[slot].value=total;wi_table[slot].stamp=wi_stamp;wi_states++;return total;
}
static uint64_t wi_count(int n,int len,const int*initial,const int*gates){
 wi_error=0;wi_calls=wi_states=0;if(n<1||n>63||len<0||len>WI_MAX){wi_error=1;return 0;}
 int current[64],last[64],lastw[64];uint64_t seen[64],all=0;
 for(int i=0;i<n;i++){int w=initial[i];if(w<0||w>=n||(all&(UINT64_C(1)<<w))){wi_error=1;return 0;}all|=UINT64_C(1)<<w;current[i]=w;seen[i]=UINT64_C(1)<<w;last[i]=lastw[i]=-1;}
 memset(wi_anc,0,sizeof wi_anc);memset(wi_desc,0,sizeof wi_desc);wi_words=(len+63)/64;wi_len=len;
 for(int k=0;k<len;k++){
  int a=gates[2*k],b=gates[2*k+1];if(a<0||a>=n||b<0||b>=n||a==b){wi_error=1;return 0;}
  int x=current[a],y=current[b];if((seen[a]&(UINT64_C(1)<<y))||(seen[b]&(UINT64_C(1)<<x))){wi_error=1;return 0;}
  /* Every previous event on these women is exactly the previous event on her holder. */
  if(lastw[x]!=last[a]||lastw[y]!=last[b]){wi_error=4;return 0;}
  wi_anc[k].b[k/64]|=UINT64_C(1)<<(k%64);
  for(int j=0;j<wi_words;j++){if(last[a]>=0)wi_anc[k].b[j]|=wi_anc[last[a]].b[j];if(last[b]>=0)wi_anc[k].b[j]|=wi_anc[last[b]].b[j];}
  last[a]=last[b]=lastw[x]=lastw[y]=k;current[a]=y;current[b]=x;seen[a]|=UINT64_C(1)<<y;seen[b]|=UINT64_C(1)<<x;
 }
 for(int i=0;i<n;i++)last[i]=-1;
 for(int k=len-1;k>=0;k--){int a=gates[2*k],b=gates[2*k+1];wi_desc[k].b[k/64]|=UINT64_C(1)<<(k%64);for(int j=0;j<wi_words;j++){if(last[a]>=0)wi_desc[k].b[j]|=wi_desc[last[a]].b[j];if(last[b]>=0)wi_desc[k].b[j]|=wi_desc[last[b]].b[j];}last[a]=last[b]=k;}
 if(!wi_table){wi_table=(WIEntry*)calloc(WI_CAP,sizeof(WIEntry));if(!wi_table){wi_error=5;return 0;}}
 if(++wi_stamp==0){memset(wi_table,0,WI_CAP*sizeof(WIEntry));wi_stamp=1;}
 WISet live={{0}};for(int k=0;k<len;k++)live.b[k/64]|=UINT64_C(1)<<(k%64);return wi_dp(live);
}
#endif
