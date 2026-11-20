/* subseq FULL G : checks every clause line of G (after header) is either a line of FULL taken in order (subsequence)
   or a unit clause on a target variable (1..h*w) appearing after all FULL-matched lines. Prints SUBSET_OK or FAIL. */
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
int main(int c,char**v){int hw=atoi(v[3]);FILE*f=fopen(v[1],"r"),*g=fopen(v[2],"r");char a[256],b[256];long n=0,u=0;
 fgets(a,256,f);fgets(b,256,g); int units=0;
 while(fgets(b,256,g)){ int x,z; if(sscanf(b,"%d %d",&x,&z)==2&&z==0&&abs(x)>=1&&abs(x)<=hw&&!strchr(b+0,' ')==0){ /* maybe unit */ }
  char*p=strchr(b,' '); if(p&&strcmp(p," 0\n")==0&&abs(atoi(b))<=hw&&abs(atoi(b))>=1){units=1;u++;continue;}
  if(units){printf("FAIL non-unit after units: %s",b);return 1;}
  int found=0; while(fgets(a,256,f)){ if(strcmp(a,b)==0){found=1;break;} }
  if(!found){printf("FAIL clause not in FULL order: %s",b);return 1;} n++; }
 printf("SUBSET_OK matched=%ld units=%ld\n",n,u);return 0;}
