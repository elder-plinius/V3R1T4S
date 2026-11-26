// Batched random-start relaxation for the Thomson problem on the GPU.
// One block per replica, positions in shared memory, FP32 Barzilai-Borwein projected gradient descent,
// then FP64 energy of the relaxed configuration. Usage: thomson_bb N R iters rounds seed outprefix
#include <cstdio>
#include <cstdlib>
#include <cstdint>
#include <vector>
#include <algorithm>
#include <cuda_runtime.h>
#include <chrono>
#define MAXN 1024
__device__ float blockSum(float v, float* red){
  int t=threadIdx.x; red[t]=v; __syncthreads();
  for(int w=blockDim.x/2;w>0;w>>=1){ if(t<w) red[t]+=red[t+w]; __syncthreads(); }
  float r=red[0]; __syncthreads(); return r;
}
__device__ double blockSumD(double v, double* red){
  int t=threadIdx.x; red[t]=v; __syncthreads();
  for(int w=blockDim.x/2;w>0;w>>=1){ if(t<w) red[t]+=red[t+w]; __syncthreads(); }
  double r=red[0]; __syncthreads(); return r;
}
__device__ uint32_t xs(uint32_t &s){s^=s<<13;s^=s>>17;s^=s<<5;return s;}
__global__ void relax(int N,int iters,unsigned seed,float* out,double* Eout,float* gout,const float* seedX,float pk,float sig){
  __shared__ float x[MAXN],y[MAXN],z[MAXN];
  __shared__ float red[MAXN];
  __shared__ double redd[MAXN];
  int i=threadIdx.x; int r=blockIdx.x;
  uint32_t s=seed*2654435761u+r*7919u+i*104729u+12345u; xs(s);xs(s);
  float px=0,py=0,pz=0;
  if(i<N){
    bool rnd=true;
    if(seedX){ px=seedX[3*i];py=seedX[3*i+1];pz=seedX[3*i+2]; rnd=((xs(s)&0xffffff)/16777216.0f)<pk;
      if(!rnd){ float sp=3.5f*rsqrtf((float)N); px+=sig*sp*((xs(s)&0xffff)/32768.f-1.f); py+=sig*sp*((xs(s)&0xffff)/32768.f-1.f); pz+=sig*sp*((xs(s)&0xffff)/32768.f-1.f);
        float n=rsqrtf(px*px+py*py+pz*pz); px*=n;py*=n;pz*=n; } }
    if(rnd){ float u=(xs(s)&0xffffff)/16777216.0f*2.f-1.f; float ph=(xs(s)&0xffffff)/16777216.0f*6.2831853f;
    float q=sqrtf(fmaxf(0.f,1.f-u*u)); px=q*cosf(ph); py=q*sinf(ph); pz=u; } }
  x[i]=px;y[i]=py;z[i]=pz; __syncthreads();
  float gx0=0,gy0=0,gz0=0,ox=px,oy=py,oz=pz; float alpha=1e-4f;
  for(int it=0;it<iters;it++){
    float gx=0,gy=0,gz=0;
    if(i<N){
      for(int j=0;j<N;j++){ if(j==i) continue; float dx=px-x[j],dy=py-y[j],dz=pz-z[j];
        float r2=dx*dx+dy*dy+dz*dz; float ir=rsqrtf(r2); float ir3=ir*ir*ir; gx-=dx*ir3; gy-=dy*ir3; gz-=dz*ir3; }
      float d=gx*px+gy*py+gz*pz; gx-=d*px; gy-=d*py; gz-=d*pz; // tangent gradient
    }
    // BB step
    float sx=px-ox,sy=py-oy,sz=pz-oz,yx=gx-gx0,yy=gy-gy0,yz=gz-gz0;
    float ss=blockSum(i<N?sx*sx+sy*sy+sz*sz:0.f,red);
    float sy_=blockSum(i<N?sx*yx+sy*yy+sz*yz:0.f,red);
    float gg=blockSum(i<N?gx*gx+gy*gy+gz*gz:0.f,red);
    if(it>0 && sy_>0) alpha=ss/sy_;
    float spacing=3.5f*rsqrtf((float)N);
    float maxg=sqrtf(gg/N)*3.f+1e-30f;
    float step=fminf(alpha, 0.1f*spacing/maxg);
    ox=px;oy=py;oz=pz; gx0=gx;gy0=gy;gz0=gz;
    if(i<N){ px-=step*gx; py-=step*gy; pz-=step*gz; float n=rsqrtf(px*px+py*py+pz*pz); px*=n;py*=n;pz*=n; }
    __syncthreads(); x[i]=px;y[i]=py;z[i]=pz; __syncthreads();
    if(it==iters-1 && i==0) gout[r]=sqrtf(gg);
  }
  // FP64 energy
  double e=0;
  if(i<N){ double X=px,Y=py,Z=pz; double nn=sqrt(X*X+Y*Y+Z*Z); X/=nn;Y/=nn;Z/=nn;
    for(int j=i+1;j<N;j++){ double a=x[j],b=y[j],c=z[j]; double m=sqrt(a*a+b*b+c*c); a/=m;b/=m;c/=m;
      double dx=X-a,dy=Y-b,dz=Z-c; e+=1.0/sqrt(dx*dx+dy*dy+dz*dz);} }
  double E=blockSumD(e,redd);
  if(i==0) Eout[r]=E;
  if(i<N){ out[((size_t)r*N+i)*3]=px; out[((size_t)r*N+i)*3+1]=py; out[((size_t)r*N+i)*3+2]=pz; }
}
int main(int argc,char**argv){
  int N=atoi(argv[1]),R=atoi(argv[2]),iters=atoi(argv[3]),rounds=atoi(argv[4]); unsigned seed=atoi(argv[5]); const char* pre=argv[6];
  cudaSetDeviceFlags(cudaDeviceScheduleBlockingSync); int th=32; while(th<N) th*=2;
  float* dX; double* dE; float* dG; float* dS=nullptr;
  const char* sf=getenv("SEED"); float pk=getenv("PK")?atof(getenv("PK")):0.005f; float sig=getenv("SIG")?atof(getenv("SIG")):0.0f;
  if(sf){ std::vector<float> h(N*3); FILE* f=fopen(sf,"r"); for(int k=0;k<N*3;k++){double v; if(fscanf(f,"%lf",&v)!=1){printf("seed read fail\n");return 1;} h[k]=(float)v;} fclose(f);
    cudaMalloc(&dS,N*3*sizeof(float)); cudaMemcpy(dS,h.data(),N*3*sizeof(float),cudaMemcpyHostToDevice); } cudaMalloc(&dX,(size_t)R*N*3*sizeof(float)); cudaMalloc(&dE,R*sizeof(double)); cudaMalloc(&dG,R*sizeof(float));
  std::vector<double> all; double best=1e300; std::vector<float> bestX(N*3), hX((size_t)R*N*3); std::vector<double> hE(R); std::vector<float> hG(R);
  auto t0=std::chrono::high_resolution_clock::now();
  for(int rd=0;rd<rounds;rd++){
    relax<<<R,th>>>(N,iters,seed+rd*100003u,dX,dE,dG,dS,pk,sig); cudaDeviceSynchronize();
    cudaError_t err=cudaGetLastError(); if(err){printf("err %s\n",cudaGetErrorString(err));return 1;}
    cudaMemcpy(hE.data(),dE,R*sizeof(double),cudaMemcpyDeviceToHost);
    cudaMemcpy(hG.data(),dG,R*sizeof(float),cudaMemcpyDeviceToHost);
    cudaMemcpy(hX.data(),dX,(size_t)R*N*3*sizeof(float),cudaMemcpyDeviceToHost);
    for(int r=0;r<R;r++){ all.push_back(hE[r]); if(hE[r]<best){best=hE[r]; std::copy(hX.begin()+(size_t)r*N*3,hX.begin()+(size_t)(r+1)*N*3,bestX.begin());} }
  }
  auto t1=std::chrono::high_resolution_clock::now(); double sec=std::chrono::duration<double>(t1-t0).count();
  std::sort(all.begin(),all.end());
  printf("N=%d relaxations=%zu time=%.1fs (%.1f relax/s) median |g| last round=%.2e\n",N,all.size(),sec,all.size()/sec,hG[R/2]);
  printf("best FP64 energies (pre-polish):"); for(int k=0;k<10 && k<(int)all.size();k++) printf(" %.7f",all[k]); printf("\n");
  int cnt=0; double thr=atof(getenv("THR")?getenv("THR"):"1e300"); for(double e:all) if(e<thr) cnt++; printf("count below THR=%g: %d\n",thr,cnt);
  char fn[512]; snprintf(fn,512,"%s_best.xyz",pre); FILE*f=fopen(fn,"w"); for(int i=0;i<N;i++) fprintf(f,"%.9f %.9f %.9f\n",bestX[3*i],bestX[3*i+1],bestX[3*i+2]); fclose(f);
  return 0;
}
