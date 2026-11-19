// Exact union-of-rectangles enclosure of E={M mu>=1} in the period cell. See object/PROOF.md for the proof.
#include "common.h"
typedef struct { i64 x0,x1,y0,y1,S; } Rect;
typedef struct { Rect*r; size_t n,cap; } RV;
static void push(RV*v,Rect r){ if(v->n==v->cap){v->cap=v->cap?v->cap*2:1024;v->r=realloc(v->r,v->cap*sizeof(Rect));if(!v->r)die("oom");} v->r[v->n++]=r; }
static int cmp64(const void*a,const void*b){i64 x=*(i64*)a,y=*(i64*)b;return x<y?-1:x>y;}
static size_t uniq(i64*a,size_t m){qsort(a,m,8,cmp64);size_t k=0;for(size_t i=0;i<m;i++)if(!k||a[k-1]!=a[i])a[k++]=a[i];return k;}
static void emit(RV*v,i64 x0,i64 x1,i64 y0,i64 y1,i64 S){
  // all lattice translates meeting the cell, clipped to it
  i64 i=(x1-1>=0?(x1-1)/LX:-((-(x1-1)+LX-1)/LX));
  for(;;i--){ i64 a=x0-i*LX,bb=x1-i*LX; if(bb<=0) break; if(a<LX){ if(a<0)a=0; if(bb>LX)bb=LX;
      i64 j=(y1-1>=0?(y1-1)/LY:-((-(y1-1)+LY-1)/LY));
      for(;;j--){ i64 c=y0-j*LY,d=y1-j*LY; if(d<=0) break; if(c<LY){ if(c<0)c=0; if(d>LY)d=LY;
          if(a<bb&&c<d){Rect r={a,bb,c,d,S};push(v,r);} } }
    } }
}
typedef struct { i64 x; int lo,hi,t; } Ev;
static int cmpev(const void*a,const void*b){i64 x=((Ev*)a)->x,y=((Ev*)b)->x;return x<y?-1:x>y;}
static int *cnt; static i64 *len; static i64 *Yc;
static void upd(int nd,int l,int r,int a,int b,int t){
  if(a<=l&&r<=b) cnt[nd]+=t;
  else { int m=(l+r)/2; if(a<m)upd(2*nd,l,m,a,b,t); if(b>m)upd(2*nd+1,m,r,a,b,t); }
  if(cnt[nd]>0) len[nd]=Yc[r]-Yc[l]; else if(r-l==1) len[nd]=0; else len[nd]=len[2*nd]+len[2*nd+1];
}
static int lowerb(i64*a,int m,i64 v){int l=0,h=m;while(l<h){int k=(l+h)/2;if(a[k]<v)l=k+1;else h=k;}return l;}
static u128 union_area(RV*v){
  size_t m=v->n; if(!m) return 0;
  i64*ys=malloc(8*2*m); Ev*ev=malloc(sizeof(Ev)*2*m);
  for(size_t i=0;i<m;i++){ys[2*i]=v->r[i].y0;ys[2*i+1]=v->r[i].y1;}
  int ny=(int)uniq(ys,2*m); Yc=ys;
  for(size_t i=0;i<m;i++){int lo=lowerb(ys,ny,v->r[i].y0),hi=lowerb(ys,ny,v->r[i].y1);
    ev[2*i]=(Ev){v->r[i].x0,lo,hi,1}; ev[2*i+1]=(Ev){v->r[i].x1,lo,hi,-1};}
  qsort(ev,2*m,sizeof(Ev),cmpev);
  cnt=calloc(4*(size_t)ny,sizeof(int)); len=calloc(4*(size_t)ny,8);
  u128 area=0; i64 px=ev[0].x;
  for(size_t i=0;i<2*m;i++){ if(ev[i].x!=px){area+=(u128)(uint64_t)(ev[i].x-px)*(u128)(uint64_t)len[1];px=ev[i].x;}
    upd(1,0,ny-1,ev[i].lo,ev[i].hi,ev[i].t);}
  free(ys);free(ev);free(cnt);free(len);
  return area;
}
int main(int ac,char**av){
  if(ac<2) die("usage");
  parse(av[1]);
  i64 Sraw=tail_side_raw(), SU=Sraw<<KBITS; int shift=bits+2*KBITS;
  // images with coordinates in [0, cell+S*]
  size_t cap=(size_t)n*4096; i64*xs=malloc(8*cap),*ys=malloc(8*cap); size_t nx=0,ny=0;
  for(int i=0;i<n;i++){ for(i64 x=A[i].x<<KBITS;x<=LX+SU;x+=LX){ xs[nx++]=x; if(nx>=cap)die("cap"); }
                        for(i64 y=A[i].y<<KBITS;y<=LY+SU;y+=LY){ ys[ny++]=y; if(ny>=cap)die("cap"); } }
  nx=uniq(xs,nx); ny=uniq(ys,ny);
  size_t W=(nx+1)*(ny+1); i64*P=calloc(W,8); if(!P)die("oom");
  #define PP(i,j) P[(size_t)(i)*(ny+1)+(j)]
  for(int i=0;i<n;i++) for(i64 x=A[i].x<<KBITS;x<=LX+SU;x+=LX) for(i64 y=A[i].y<<KBITS;y<=LY+SU;y+=LY){
    int ix=lowerb(xs,(int)nx,x), iy=lowerb(ys,(int)ny,y); PP(ix+1,iy+1)+=A[i].m; }
  for(size_t i=1;i<=nx;i++) for(size_t j=1;j<=ny;j++) PP(i,j)+=PP(i-1,j)+PP(i,j-1)-PP(i-1,j-1);
  #define BOX(i0,i1,j0,j1) (PP((i1)+1,(j1)+1)-PP(i0,(j1)+1)-PP((i1)+1,j0)+PP(i0,j0))
  RV in={0},out={0}; unsigned long long boxes=0,tight=0,nonempty=0; i64 maxS=0;
  for(size_t ia=0;ia<nx&&xs[ia]<LX;ia++) for(size_t ic=0;ic<ny&&ys[ic]<LY;ic++){
    for(size_t ib=ia;ib<nx&&xs[ib]-xs[ia]<SU;ib++){ i64 w=xs[ib]-xs[ia];
      for(size_t id=ic;id<ny&&ys[id]-ys[ic]<SU;id++){ i64 h=ys[id]-ys[ic]; boxes++;
        if(BOX(ia,ia,ic,id)==0||BOX(ib,ib,ic,id)==0||BOX(ia,ib,ic,ic)==0||BOX(ia,ib,id,id)==0) continue;
        tight++;
        i64 m=BOX(ia,ib,ic,id); u128 v=((u128)(uint64_t)m)<<shift; i64 mx=w>h?w:h;
        if(v<=(u128)(uint64_t)mx*(u128)(uint64_t)mx) continue; // sqrt(v)<=max(w,h): true rectangle has zero area
        nonempty++;
        i64 Sf=(i64)isqrt128(v); i64 Si=Sf&~1LL; i64 So=(((u128)Si*(u128)Si==v))?Si:Si+2;
        if((u128)Si*(u128)Si>v||(u128)So*(u128)So<v) die("sqrt check");
        i64 a=xs[ia],b=xs[ib],c=ys[ic],d=ys[id];
        if(So>maxS) maxS=So;
        if(Si>mx) emit(&in,b-Si/2,a+Si/2,d-Si/2,c+Si/2,Si);
        if(So>mx) emit(&out,b-So/2,a+So/2,d-So/2,c+So/2,So);
      } } }
  // spot-verify a pseudo-random subset of inner rectangles directly from the definition, by full image list:
  // {atoms inside Q(x,S/2) for every x of the rectangle} = atoms inside Q at all four corners (convexity).
  i64 hw=SU; unsigned long long st=0x1234567ULL; int checked=0;
  size_t nimg=0; Atom*im=malloc(sizeof(Atom)*(size_t)n*4096);
  for(int i=0;i<n;i++) for(i64 p=-16;p<=16;p++) for(i64 q=-16;q<=16;q++){ i64 x=(A[i].x<<KBITS)+p*LX,y=(A[i].y<<KBITS)+q*LY;
     if(x>=-hw&&x<=LX+hw&&y>=-hw&&y<=LY+hw) im[nimg++]=(Atom){x,y,A[i].m}; }
  int ntest=in.n<3000?(int)in.n:3000;
  for(int t=0;t<ntest;t++){ st=st*6364136223846793005ULL+1442695040888963407ULL; Rect r=in.r[(st>>20)%in.n];
    i64 mass=0; for(size_t i=0;i<nimg;i++){ i64 ax=im[i].x,ay=im[i].y;
      if(iabs64(ax-r.x0)<=r.S/2&&iabs64(ax-r.x1)<=r.S/2&&iabs64(ay-r.y0)<=r.S/2&&iabs64(ay-r.y1)<=r.S/2) mass+=im[i].m; }
    if((((u128)(uint64_t)mass)<<shift)<(u128)r.S*(u128)r.S) die("spot verification FAILED"); checked++; }
  // pointwise cross-check: exact decision from the definition vs rectangle membership, on uniform points and on points
  // pushed just to either side of edges of random rectangles (where a missed or wrong rectangle would show).
  if(ac>2 && in.n){ long Np=atol(av[2]); long bad=0,inn=0,outo=0,neither=0,trueE=0; typedef struct{i64 d,m;}DM;
    DM*w=malloc(sizeof(DM)*nimg); unsigned long long s2=0xABCDEF01ULL;
    #define RNG() (s2=s2*6364136223846793005ULL+1442695040888963407ULL,(s2>>16))
    for(long t=0;t<Np;t++){ i64 x,y;
      if(t%2==0){ x=(i64)(RNG()%(uint64_t)LX); y=(i64)(RNG()%(uint64_t)LY); }
      else { Rect r=in.r[RNG()%in.n]; i64 eps=1LL<<(RNG()%34); int side=(int)(RNG()%4); i64 sg=(RNG()&1)?eps:-eps;
        x=r.x0+(i64)(RNG()%(uint64_t)(r.x1-r.x0)); y=r.y0+(i64)(RNG()%(uint64_t)(r.y1-r.y0));
        if(side==0)x=r.x0+sg; else if(side==1)x=r.x1+sg; else if(side==2)y=r.y0+sg; else y=r.y1+sg;
        x=((x%LX)+LX)%LX; y=((y%LY)+LY)%LY; }
      size_t m=0; for(size_t i=0;i<nimg;i++){ i64 dx=iabs64(im[i].x-x),dy=iabs64(im[i].y-y),d=dx>dy?dx:dy; if(d<=SU/2+1){w[m].d=d;w[m].m=im[i].m;m++;} }
      for(size_t i=1;i<m;i++){DM z=w[i];size_t j=i;while(j>0&&w[j-1].d>z.d){w[j]=w[j-1];j--;}w[j]=z;}
      i64 Wc=0; int inE=0; for(size_t k=0;k<m;k++){ Wc+=w[k].m; if((((u128)(uint64_t)Wc)<<shift)>=(u128)(uint64_t)(2*w[k].d)*(u128)(uint64_t)(2*w[k].d)){inE=1;break;} }
      int I=0,O=0; for(size_t i=0;i<in.n&&!I;i++){ Rect*r=&in.r[i]; if(x>=r->x0&&x<=r->x1&&y>=r->y0&&y<=r->y1) I=1; }
      for(size_t i=0;i<out.n&&!O;i++){ Rect*r=&out.r[i]; if(x>=r->x0&&x<=r->x1&&y>=r->y0&&y<=r->y1) O=1; }
      inn+=I; outo+=O; trueE+=inE; if(!O)neither++;
      if((I&&!inE)||(inE&&!O)) bad++;
    }
    printf("pointwise_check points %ld truly_in_E %ld in_inner %ld in_outer %ld in_neither %ld violations %ld\n",Np,trueE,inn,outo,neither,bad);
  }
  size_t nin=in.n,nout=out.n;
  u128 Ain=union_area(&in), Aout=union_area(&out);
  printf("bits %d kbits %d Lx %lld Ly %lld M %lld n %d\n",bits,KBITS,(long long)Lx,(long long)Ly,(long long)Mtot,n);
  printf("tail_S_raw %lld grid %zu x %zu boxes %llu tight %llu nonempty %llu rects_inner %zu rects_outer %zu maxS_raw_over %lld spot_verified %d\n",
     (long long)Sraw,nx,ny,boxes,tight,nonempty,nin,nout,(long long)(maxS>>KBITS)+1,checked);
  printf("area_inner_U2 ");pr128(stdout,Ain);printf("\narea_outer_U2 ");pr128(stdout,Aout);printf("\n");
  return 0;
}
