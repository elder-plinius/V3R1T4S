#pragma once
#include <cstdlib>
#include <cstdio>
#include <new>
#include <cstddef>
#include <cstdint>
#include <atomic>
#include <limits>
static std::atomic<size_t> heap_live{0},heap_peak{0};
static constexpr size_t heap_cap=512ull*1024*1024;
static constexpr uint64_t heap_magic=0xb6b44b65cb0743fdULL;
struct alignas(std::max_align_t) HeapHeader { void* raw; size_t cost; uint64_t magic; };
static void* guard_alloc(size_t n,size_t align){
 if(align<alignof(HeapHeader))align=alignof(HeapHeader);
 if((align&(align-1))||align>heap_cap)throw std::bad_alloc();
 if(n>heap_cap-sizeof(HeapHeader)||align-1>heap_cap-n-sizeof(HeapHeader))throw std::bad_alloc();
 size_t cost=n+sizeof(HeapHeader)+align-1,before=heap_live.load();
 do{if(before>heap_cap||cost>heap_cap-before)throw std::bad_alloc();}while(!heap_live.compare_exchange_weak(before,before+cost));
 void* raw=std::malloc(cost);if(!raw){heap_live.fetch_sub(cost);throw std::bad_alloc();}
 auto p=(reinterpret_cast<uintptr_t>(raw)+sizeof(HeapHeader)+align-1)&~uintptr_t(align-1);
 auto h=reinterpret_cast<HeapHeader*>(p)-1;h->raw=raw;h->cost=cost;h->magic=heap_magic;
 size_t peak=heap_peak.load();while(peak<before+cost&&!heap_peak.compare_exchange_weak(peak,before+cost)){}
 return reinterpret_cast<void*>(p);
}
static void guard_free(void*p)noexcept{if(!p)return;auto h=reinterpret_cast<HeapHeader*>(p)-1;if(h->magic!=heap_magic){std::fprintf(stderr,"HEAP_BAD_MAGIC\n");std::abort();}size_t before=heap_live.fetch_sub(h->cost);if(h->cost>before){std::fprintf(stderr,"HEAP_UNDERFLOW\n");std::abort();}h->magic=0;std::free(h->raw);}
void* operator new(size_t n){return guard_alloc(n,alignof(std::max_align_t));}
void* operator new[](size_t n){return ::operator new(n);}
void* operator new(size_t n,std::align_val_t a){return guard_alloc(n,size_t(a));}
void* operator new[](size_t n,std::align_val_t a){return ::operator new(n,a);}
void operator delete(void*p)noexcept{guard_free(p);}
void operator delete[](void*p)noexcept{guard_free(p);}
void operator delete(void*p,size_t)noexcept{guard_free(p);}
void operator delete[](void*p,size_t)noexcept{guard_free(p);}
void operator delete(void*p,std::align_val_t)noexcept{guard_free(p);}
void operator delete[](void*p,std::align_val_t)noexcept{guard_free(p);}
void operator delete(void*p,size_t,std::align_val_t)noexcept{guard_free(p);}
void operator delete[](void*p,size_t,std::align_val_t)noexcept{guard_free(p);}
struct HeapEnd{~HeapEnd(){std::fprintf(stderr,"HEAP live%zu peak%zu cap%zu\n",heap_live.load(),heap_peak.load(),heap_cap);}};
static HeapEnd heap_end;
