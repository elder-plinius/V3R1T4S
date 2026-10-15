// Written from GAME.md and mathematical certificate format before inspecting author code.
// Quoted definition: "The loser transfers the smaller of the two pre-round stacks
// to the winner. Stop at the first zero stack." Each ordered winner/loser has probability 1/6.
// Uses only evaluated vertex stacks, not author's affine-state implementation.
#include <array>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <stdexcept>
#include <algorithm>
#include <chrono>
using I=std::int64_t;
constexpr int MAXV=8;
struct State { I v[3][MAXV]{}; };
struct Bound { I lo,hi; };
I six[19];
int nv;
std::uint64_t calls=0;

Bound enclose(const State& s,int depth) {
    ++calls;
    if(!depth) return {0,4}; // denominator 5: 0 <= f <= 4/5.
    Bound result{0,0};
    for(int i=0;i<3;++i) for(int j=i+1;j<3;++j) {
        bool positive=false,negative=false;
        for(int k=0;k<nv;++k) {
            positive |= s.v[i][k]>s.v[j][k];
            negative |= s.v[i][k]<s.v[j][k];
        }
        if(positive && negative) {
            // One pair's two outcomes: unresolved orientation. At most one live successor.
            result.hi+=(i==0 ? 9:4)*six[depth-1];
        } else if(!positive && !negative) {
            // Identically tied pair: both outcomes terminate; one eliminates player 1 iff in pair.
            if(i==0) result.lo+=5*six[depth-1], result.hi+=5*six[depth-1];
        } else {
            int poor=positive?j:i, rich=positive?i:j;
            // Poorer loses: immediate absorption.
            if(poor==0) result.lo+=5*six[depth-1], result.hi+=5*six[depth-1];
            // Poorer wins: the unique live successor.
            State t=s;
            for(int k=0;k<nv;++k) {
                t.v[poor][k]=2*s.v[poor][k];
                t.v[rich][k]=s.v[rich][k]-s.v[poor][k];
            }
            Bound b=enclose(t,depth-1);
            result.lo+=b.lo; result.hi+=b.hi;
        }
    }
    // All terms have denominator 5*6^(depth-1); divide the probability sum by 6.
    return result;
}

int main(int argc,char** argv) try {
    if(argc!=2) throw std::runtime_error("usage: independent tasks.txt");
    six[0]=1; for(int d=1;d<=18;++d) six[d]=6*six[d-1];
    std::ifstream in(argv[1]); int count;
    if(!(in>>count) || count<1) throw std::runtime_error("missing workload");
    auto start=std::chrono::steady_clock::now();
    I min_num=0,min_den=1; int min_id=-1;
    for(int leaf=0;leaf<count;++leaf) {
        int id,d; if(!(in>>id>>d>>nv) || d<0 || d>18 || nv<1 || nv>MAXV) throw std::runtime_error("bad task header");
        State a,b;
        for(State* s:{&a,&b}) for(int j=0;j<3;++j) for(int k=0;k<nv;++k) {
            if(!(in>>s->v[j][k]) || s->v[j][k]<0 || s->v[j][k]>(I(1)<<(60-d))) throw std::runtime_error("invalid or oversized coordinate");
        }
        I want[4]; for(I& w:want) if(!(in>>w)) throw std::runtime_error("missing bounds");
        Bound ba=enclose(a,d),bb=enclose(b,d); I got[]={ba.lo,ba.hi,bb.lo,bb.hi};
        for(int k=0;k<4;++k) if(got[k]!=want[k]) {
            std::cerr<<"MISMATCH node "<<id<<" field "<<k<<" expected "<<want[k]<<" actual "<<got[k]<<"\n";
            return 1;
        }
        I gap=ba.lo-bb.hi,den=5*six[d];
        if(gap<=0) throw std::runtime_error("nonpositive gap");
        if(min_id<0 || (__int128)gap*min_den<(__int128)min_num*den) min_num=gap,min_den=den,min_id=id;
        // Deterministic per-leaf transcript permits exact repeat comparison.
        std::cout<<id<<" "<<d<<" "<<ba.lo<<" "<<ba.hi<<" "<<bb.lo<<" "<<bb.hi<<"\n";
        if((leaf+1)%100==0 || leaf+1==count) {
            double elapsed=std::chrono::duration<double>(std::chrono::steady_clock::now()-start).count();
            std::cerr<<"checked "<<leaf+1<<"/"<<count<<" calls "<<calls<<" seconds "<<elapsed<<"\n";
        }
    }
    std::string extra; if(in>>extra) throw std::runtime_error("extra task data");
    std::cout<<"ALL_VERIFIED "<<count<<" MIN_NODE "<<min_id<<" MIN_RAW "<<min_num<<"/"<<min_den<<"\n";
    return 0;
} catch(const std::exception& e) { std::cerr<<"FAIL "<<e.what()<<"\n"; return 1; }
