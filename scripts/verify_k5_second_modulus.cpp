// Independent second-modulus K=5 factorial-valuation rank checker.
// Uses F_65519 rather than the original F_65521 implementation.
// Full column rank modulo a prime implies rank over Q and Z.
// Modular dependence does NOT assert an exact integer factorial relation.
// Build: g++ -std=c++20 -O3 -Wall -Wextra -o /tmp/k5_second_mod scripts/verify_k5_second_modulus.cpp
// Run: /tmp/k5_second_mod 25810 5
#include <algorithm>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <vector>
using namespace std;
static constexpr uint64_t Q=65519;
uint64_t inverse(uint64_t x){
  uint64_t z=1,e=Q-2;
  while(e){if(e&1)z=z*x%Q;x=x*x%Q;e>>=1;}
  return z;
}
int valuation(int n,int p){
  int s=0;
  while(n){n/=p;s+=n;}
  return s;
}
vector<int> prime_list(int n){
  vector<uint8_t> b(n+1,1);b[0]=b[1]=0;
  for(int p=2;p*p<=n;p++)if(b[p])
    for(int j=p*p;j<=n;j+=p)b[j]=0;
  vector<int> v;
  for(int p=2;p<=n;p++)if(b[p])v.push_back(p);
  return v;
}
int main(int argc,char**argv){
  int M=argc>1?atoi(argv[1]):25810;
  int K=argc>2?atoi(argv[2]):5;
  if(M<2||M>26000||K!=5){
    cerr<<"Usage: verify_k5_second_modulus [M=2..26000] [K=5]\n";return 2;
  }
  auto primes=prime_list(K*M);
  const int P=primes.size(),R=1+K*P;
  vector<vector<uint16_t>> basis(R);
  vector<uint16_t> column(R,0);
  int rank=0,first_dependent=0;
  for(int a=1;a<=M;a++){
    fill(column.begin(),column.end(),0);
    column[0]=a%Q;
    for(int m=1;m<=K;m++)
      for(int i=0;i<P&&primes[i]<=m*a;i++)
        column[1+(m-1)*P+i]=valuation(m*a,primes[i])%Q;
    bool independent=false;
    for(int j=R-1;j>=0;j--){
      uint64_t c=column[j];
      if(!c)continue;
      if(basis[j].empty()){
        auto inv=inverse(c);
        for(int k=0;k<=j;k++)
          column[k]=uint64_t(column[k])*inv%Q;
        basis[j].assign(column.begin(),column.begin()+j+1);
        rank++;independent=true;break;
      }
      auto &pivot=basis[j];
      for(int k=0;k<j;k++)
        column[k]=(column[k]+Q-c*pivot[k]%Q)%Q;
      column[j]=0;
    }
    if(!independent&&first_dependent==0)
      first_dependent=a;
  }
  cout<<"modulus="<<Q<<" K="<<K<<" max_weight="<<M
      <<" rank="<<rank<<" first_dependent="<<first_dependent<<"\n";
  if(M==25810&&!(rank==25809&&first_dependent==25809))return 3;
  if(M==25808&&rank!=25808)return 4;
  return 0;
}
