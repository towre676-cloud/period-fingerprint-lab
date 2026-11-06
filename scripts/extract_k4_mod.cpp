// Independent exact K=4 factorial-valuation kernel mod prime q.
// Outputs nonzero weights and coefficients modulo q in 0..q-1.
// Compile: g++ -std=c++20 -O3 -Wall -Wextra -o extract_k4_mod scripts/extract_k4_mod.cpp
#include <algorithm>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <vector>
using namespace std;
uint64_t powmod(uint64_t a,uint64_t n,uint64_t p){uint64_t r=1;for(;n;n>>=1,a=a*a%p)if(n&1)r=r*a%p;return r;}
int val(int n,int p){int s=0;for(;n;n/=p)s+=n/p;return s;}
vector<int> primes_to(int n){vector<uint8_t> sieve(n+1,1);sieve[0]=sieve[1]=0;for(int p=2;p*p<=n;p++)if(sieve[p])for(int i=p*p;i<=n;i+=p)sieve[i]=0;vector<int> p;for(int i=2;i<=n;i++)if(sieve[i])p.push_back(i);return p;}
int main(int argc,char**argv){
 if(argc!=2){cerr<<"Usage: extract_k4_mod prime\n";return 2;}
 const uint64_t q=strtoull(argv[1],nullptr,10);
 if(q<1000||q>1000000289){cerr<<"prime modulus out of bounds\n";return 2;}
 constexpr int M=1692,K=4;
 const auto primes=primes_to(K*M);const int P=primes.size(),R=1+K*P;
 vector<vector<uint32_t>> pivots(R),repr(R);
 vector<uint32_t> vec(R),comb(M);
 for(int a=1;a<=M;a++){
  fill(vec.begin(),vec.end(),0);fill(comb.begin(),comb.end(),0);comb[a-1]=1;vec[0]=a%q;
  for(int m=1;m<=K;m++)for(int i=0;i<P&&primes[i]<=a*m;i++)vec[1+(m-1)*P+i]=val(m*a,primes[i])%q;
  bool independent=false;
  for(int j=R-1;j>=0;j--){const uint64_t c=vec[j];if(!c)continue;
   if(pivots[j].empty()){
    uint64_t inverse=powmod(c,q-2,q);
    for(int k=0;k<=j;k++)vec[k]=uint64_t(vec[k])*inverse%q;
    for(int k=0;k<a;k++)comb[k]=uint64_t(comb[k])*inverse%q;
    pivots[j].assign(vec.begin(),vec.begin()+j+1);
    repr[j].assign(comb.begin(),comb.begin()+a);
    independent=true;break;
   }
   for(int k=0;k<j;k++)vec[k]=(vec[k]+q-c*pivots[j][k]%q)%q;
   vec[j]=0;
   for(size_t k=0;k<repr[j].size();k++)comb[k]=(comb[k]+q-c*repr[j][k]%q)%q;
  }
  if(!independent){
   if(a!=M){cerr<<"dependency earlier than 1692 at "<<a<<"\n";return 3;}
   for(int k=0;k<a;k++)if(comb[k])cout<<k+1<<' '<<comb[k]<<'\n';
   cerr<<"modulus="<<q<<" first_kernel_weight="<<a<<"\n";
   return 0;
  }
 }
 cerr<<"No kernel at maximum weight 1692\n";return 4;
}
