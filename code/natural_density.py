"""Illustration for Theorem 2.3: the sawtooth of the first relevant mean along
the natural density p = theta / (log n)^2.

For n = exp(L) on a grid of L values, the script computes
    F_k = log E X_k = log binom(n, k) + (n - k) log(1 - q^k),   q = 1 - p,
the index s = min{k : F_k >= -sqrt(L)}, and F_s. As n grows, F_s decreases in
small steps, then jumps up by order L^2 when s increases by one. The theorem's
failure window |F_s| < M therefore occupies a vanishing fraction of the
logarithmic range. The script reports the fraction of grid points with
|F_s| < 1, the number of jumps, and the largest decrease between neighbouring
grid points. It also checks, at one value of L, that the jump F_{s+1} - F_s is
of order L^2 and the curvature C_s = 2 log b_{s+1} - log b_s - log b_{s+2}
is close to theta.

This is a numerical illustration on a grid of real n; it proves nothing.
Usage: python natural_density.py [--output results/natural-density.json]
Requires mpmath (tested with 1.3.0).
"""
import argparse
import json
import sys

from mpmath import mp, mpf, loggamma, log1p, exp, expm1, sqrt, log, nstr


def profile(L, theta):
    n = exp(L)
    p = mpf(theta) / L ** 2
    a = -log1p(-p)

    def logb(k):
        return (n - k) * log1p(-exp(-a * k))

    def F(k):
        return loggamma(n + 1) - loggamma(k + 1) - loggamma(n - k + 1) + logb(k)

    k = int(L / a)
    for _ in range(3):  # fixed point of k a = L - log(k L)
        k = int((L - log(k * L)) / a)
    while F(k) >= -sqrt(L):
        k -= 1
    while F(k) < -sqrt(L):
        k += 1
    s = k
    curvature = 2 * logb(s + 1) - logb(s) - logb(s + 2)
    return s, F(s), F(s + 1) - F(s), curvature


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', default=None)
    args = parser.parse_args()
    theta = 1
    mp.dps = 80  # n = e^L with L near 60: log-gamma differences need ~L/2.3 + 50 digits
    L0 = mpf(60)
    s0, F0, jump0, _ = profile(L0, theta)
    eps = mpf(10) ** -12
    s1, F1, _, _ = profile(L0 + eps, theta)
    slope = (F1 - F0) / eps if s1 == s0 else None
    if slope is None or slope >= 0:
        sys.exit('FAIL: F_s not decreasing at L0')
    period = jump0 / (-slope)  # change of L between two increments of s
    points = 1500
    grid = [L0 + 3 * period * j / points for j in range(points + 1)]
    rows = [(L,) + profile(L, theta) for L in grid]
    inside = sum(1 for r in rows if abs(r[2]) < 1)
    jumps = sum(1 for r0, r1 in zip(rows, rows[1:]) if r1[1] != r0[1])
    drops = [r0[2] - r1[2] for r0, r1 in zip(rows, rows[1:]) if r1[1] == r0[1]]
    min_jump = min(r[3] for r in rows)
    curv = [r[4] for r in rows]
    summary = {
        'theta': theta, 'L0': 60,
        'dF_s_dL_at_L0': nstr(slope, 6),
        'jump_F_s_plus_1_minus_F_s_at_L0': nstr(jump0, 6),
        'jump_over_L_squared': nstr(jump0 / L0 ** 2, 6),
        'period_in_L': nstr(period, 6),
        'grid_points': len(rows),
        'index_increments_on_grid': jumps,
        's_first': rows[0][1], 's_last': rows[-1][1],
        'all_steps_decrease_between_increments': all(d > 0 for d in drops),
        'points_with_abs_F_s_below_1': inside,
        'fraction_with_abs_F_s_below_1': float(mpf(inside) / len(rows)),
        'two_over_jump': nstr(2 / jump0, 6),
        'curvature_C_s_min': nstr(min(curv), 6), 'curvature_C_s_max': nstr(max(curv), 6),
    }
    for key, value in summary.items():
        print(f'{key}: {value}')
    ok = (jumps == 3 and summary['all_steps_decrease_between_increments']
          and summary['fraction_with_abs_F_s_below_1'] < 0.01
          and min_jump > L0 ** 2 / 10 and 0 < min(curv) and max(curv) < theta)
    if args.output:
        with open(args.output, 'w') as fh:
            json.dump(summary, fh, indent=1)
    if not ok:
        sys.exit('FAIL natural-density illustration')
    print('PASS natural-density illustration')


if __name__ == '__main__':
    main()
