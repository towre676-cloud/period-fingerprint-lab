// Independent modular rank checker for K=4, max individual weight 1691.
// This is a finite-field certificate of rational independence, NOT an
// integer collision witness at weight 1692.
// Compile: g++ -O3 -std=c++20 -Wall -Wextra -o /tmp/weight_rank scripts/verify_k4_rank.cpp
// Run: /tmp/weight_rank 1691 4
#include <algorithm>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <stdexcept>
#include <vector>
using namespace std;
static constexpr uint64_t prime_modulus=65521;

uint64_t inverse(uint64_t x) {
    if(!x)throw runtime_error("zero inverse");
    uint64_t result=1, e=prime_modulus-2;
    while(e) {
        if(e&1)result=result*x%prime_modulus;
        x=x*x%prime_modulus;
        e>>=1;
    }
    return result;
}
int legendre(int n,int p) {
    int result=0;
    while(n) { n/=p; result+=n; }
    return result;
}
vector<int> sieve_primes(int n) {
    vector<bool> is_prime(n+1,true);
    is_prime[0]=is_prime[1]=false;
    for(int i=2;i*i<=n;++i)if(is_prime[i])
        for(int j=i*i;j<=n;j+=i)is_prime[j]=false;
    vector<int> primes;
    for(int i=2;i<=n;++i)if(is_prime[i])primes.push_back(i);
    return primes;
}
int main(int argc,char**argv) {
    int M=argc>1?atoi(argv[1]):1691;
    int K=argc>2?atoi(argv[2]):4;
    if(M<2||M>2000||K<1||K>5) {
        cerr<<"Usage: verify_k4_rank [max_weight 2..2000] [prefix 1..5]\n";
        return 2;
    }
    auto primes=sieve_primes(K*M);
    int P=(int)primes.size(),R=1+K*P;
    vector<vector<uint32_t>> basis(R);
    vector<uint32_t> column(R,0);
    int rank=0, first_dependency=0;
    for(int a=1;a<=M;++a) {
        fill(column.begin(),column.end(),0);
        column[0]=a%prime_modulus;
        for(int m=1;m<=K;++m)
            for(int i=0;i<P&&primes[i]<=m*a;++i)
                column[1+(m-1)*P+i]=legendre(m*a,primes[i])%prime_modulus;
        bool independent=false;
        for(int j=R-1;j>=0;--j) {
            uint64_t coeff=column[j];
            if(!coeff)continue;
            if(basis[j].empty()) {
                uint64_t inv=inverse(coeff);
                for(int k=0;k<=j;++k)
                    column[k]=(uint64_t(column[k])*inv)%prime_modulus;
                basis[j].assign(column.begin(),column.begin()+j+1);
                independent=true;
                ++rank;
                break;
            }
            auto & b=basis[j];
            for(int k=0;k<j;++k)
                column[k]=(column[k]+prime_modulus-(coeff*b[k])%prime_modulus)%prime_modulus;
            column[j]=0;
        }
        if(!independent) { first_dependency=a; break; }
    }
    cout<<"modulus="<<prime_modulus<<" prefix="<<K
        <<" bound="<<M<<" rank="<<rank
        <<" first_modular_dependency="<<first_dependency<<"\n";
    if(M==1691&&K==4&&rank!=1691)return 3;
    if(M==1692&&K==4&&first_dependency!=1692)return 4;
    return 0;
}
