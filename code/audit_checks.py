"""Independent finite checks for the domination polynomial proof.
Standard library for exhaustive graphs. mpmath for the high-precision tuning check.
"""
from fractions import Fraction
from itertools import combinations
from math import comb
from mpmath import mp


def check(condition, message):
    """Fail loudly even under python -O (assert statements are stripped there)."""
    if not condition:
        raise SystemExit('CHECK FAILED: ' + message)

def small_graphs(n):
    edges=list(combinations(range(n),2))
    binoms=[comb(n,k) for k in range(n+1)]
    sums=[0]*(n+1)
    mask=(1<<n)-1
    count=1<<len(edges)
    misses=0
    for code in range(count):
        closed=[1<<v for v in range(n)]
        for i,(v,w) in enumerate(edges):
            if code>>i&1:
                closed[v]|=1<<w
                closed[w]|=1<<v
        reached=[0]*(1<<n)
        counts=[0]*(n+1)
        for S in range(1,1<<n):
            b=S&-S
            reached[S]=reached[S^b] | closed[b.bit_length()-1]
            if reached[S]==mask:
                counts[S.bit_count()]+=1
        for k in range(n+1):
            sums[k]+=counts[k]
        if any(counts[k]**2 * binoms[k-1]*binoms[k+1] <
               counts[k-1]*counts[k+1]*binoms[k]**2 for k in range(1,n)):
            misses+=1
    for k in range(n+1):
        expected=binoms[k]*(1-Fraction(1,2)**k)**(n-k)
        check(Fraction(sums[k],count)==expected, 'audit_checks.py check 1')
    print(f'n={n}, labelled graphs={count}, exact mean verified, failures of ultra-log-concavity={misses}')

def hypergeometric_checks():
    cases=0
    for n in range(3,19):
        for k in range(2,n):
            for b in range(n+1):
                h=lambda j:Fraction(comb(b,j),comb(n,j))
                rhs=h(k-1)*Fraction((n-b)*(n-b-1),(n-k+1)*(n-k))
                check(h(k-1)-2*h(k)+h(k+1)==rhs, 'audit_checks.py check 2')
                cases+=1
    print(f'{cases} exact hypergeometric curvature identities verified')

def check_scales():
    for theta in [0,1]:
        for power in [128,512,2048]:
            with mp.workprec(2*power+256):
                n=2**power
                L=mp.log(n)
                r=int(L**(3 if theta else 4))
                lam=mp.exp(-theta)    # integer boundary at lambda exp(theta)=1
                def logchoose(k):
                    return mp.loggamma(n+1)-mp.loggamma(k+1)-mp.loggamma(n-k+1)
                u=-mp.expm1((mp.log(lam)-logchoose(r))/(n-r))
                q=mp.exp(mp.log(u)/r)
                p=1-q
                logb=lambda j:(n-r-j)*mp.log1p(-u*q**j)
                check(abs(logchoose(r)+logb(0)-mp.log(lam)) < mp.mpf('1e-25'), 'audit_checks.py check 3')
                curvature=2*logb(1)-logb(0)-logb(2)
                b=lam*mp.exp(curvature)
                c=b*(1+mp.mpf(1)/(r+1))*(1+mp.mpf(1)/(n-r-1))
                check((c<1 if theta==1 else b>1), 'audit_checks.py check 4')
                print('theta',theta,'n=2^'+str(power),'p(log n)^2',mp.nstr(p*L**2,8),
                      'ULC threshold',mp.nstr(b,10),'ordinary threshold',mp.nstr(c,10))
if __name__=='__main__':
    for n in range(2,7): small_graphs(n)
    hypergeometric_checks()
    check_scales()
