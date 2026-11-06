// Find the first M where RAW prime-row counting guarantees a K=5
// factorial-valuation relation. Sharpness is ONLY for this counting
// criterion; it does not rule out integer relations at smaller M.
// Standard library C++, exact Eratosthenes sieve and prefix sums.
// g++ -O3 -std=c++20 -Wall -Wextra -o /tmp/k5_threshold scripts/verify_k5_counting_threshold.cpp
// /tmp/k5_threshold
#include <algorithm>
#include <cstdint>
#include <iostream>
#include <vector>
using namespace std;
int main(){
  constexpr int K=5, CAP=2866599, N=K*CAP;
  vector<uint8_t> prime(N+1,1);
  prime[0]=prime[1]=0;
  for(int p=2;1LL*p*p<=N;p++)
    if(prime[p])
      for(int j=p*p;j<=N;j+=p)prime[j]=0;
  vector<int> pi(N+1,0);
  for(int i=1;i<=N;i++)pi[i]=pi[i-1]+prime[i];
  int first_any=0,first_same_dimension=0;
  for(int M=2;M<=CAP;M++){
    int sum=0;
    for(int m=1;m<=K;m++)sum+=pi[m*M];
    int lower_nullity=M-1-sum;
    if(lower_nullity>0 && !first_any)first_any=M;
    if(lower_nullity>1 && !first_same_dimension)first_same_dimension=M;
  }
  cout<<"first_any="<<first_any
      <<" first_same_dimension="<<first_same_dimension<<"\n";
  for(int M:{2866588,2866589,2866598,2866599}){
    int sum=0;
    cout<<"M="<<M<<" counts=";
    for(int m=1;m<=K;m++){
      int c=pi[m*M];sum+=c;
      cout<<(m==1?"":",")<<c;
    }
    cout<<" rows="<<(1+sum)
        <<" nullity_at_least="<<(M-1-sum)<<"\n";
  }
  if(first_any!=2866589||first_same_dimension!=2866599)return 2;
  return 0;
}
