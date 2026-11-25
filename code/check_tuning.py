"""Numerical cross-check of the tuned sparse sequence. Requires mpmath."""
from mpmath import mp



def check(condition, message):
    """Fail loudly even under python -O (assert statements are stripped there)."""
    if not condition:
        raise SystemExit('CHECK FAILED: ' + message)

def evaluate(logn, theta, intensity):
    # Resolving differences of log-gamma values for n of order exp(logn)
    # costs roughly logn/log(10) decimal digits; retain 80 in reserve.
    with mp.workdps(int(logn / mp.log(10)) + 80):
        lam = mp.mpf(intensity)
        n = int(mp.exp(logn))
        L = mp.log(n)
        r = int(L**3 / theta if theta else L**4)
        log_binom = mp.loggamma(n+1) - mp.loggamma(r+1) - mp.loggamma(n-r+1)
        u = -mp.expm1((mp.log(lam) - log_binom) / (n-r))
        a = -mp.log(u) / r
        p = -mp.expm1(-a)
        f = [(n-r-i)*mp.log1p(-u*mp.exp(-i*a)) for i in range(3)]
        curvature = 2*f[1] - f[0] - f[2]
        check(abs(log_binom + f[0] - mp.log(lam)) < mp.mpf('1e-30'), 'check_tuning.py check 1')
        if theta:
            check(0 < curvature < theta, 'check_tuning.py check 2')
        else:
            check(curvature > 0, 'check_tuning.py check 3')
        return mp.nstr(p*L**2, 8), mp.nstr(curvature, 8), mp.nstr(lam*mp.exp(curvature), 8)


if __name__ == '__main__':
    print('theta log(n) p*log(n)^2  log-curvature  expected normalized threshold')
    for theta in (0, 1):
        for logn in (100, 500, 1000):
            print(theta, logn, *evaluate(logn, theta, '0.7'))
