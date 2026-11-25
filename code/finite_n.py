"""Finite-n evidence for G(n, 1/2): how often do log-concavity (LC) and
ultra-log-concavity (ULC) of the domination sequence fail?

For n <= 6 every labelled graph on [n] is enumerated. For 7 <= n <= 18 a fixed
number of independent samples of G(n, 1/2) is drawn with NumPy's PCG64 generator
from a fixed seed, so the counts are reproducible. All tests use exact integer
arithmetic. For each failing graph the script records the failing indices k,
measured from the domination number gamma (index gamma + 1 is where the paper's
obstruction acts).

These are finite computations. They illustrate the asymptotic theorems and do
not prove them.

Usage: python finite_n.py [--output results/finite-n.json]
Requires NumPy (tested with 2.3.5).
"""
import argparse
import itertools
import json
import math
import sys

import numpy as np

SEED = 20261124
SAMPLES = 20000


def popcounts(n):
    table = np.zeros(1 << n, dtype=np.int64)
    for i in range(n):
        table[1 << i:1 << (i + 1)] = table[0:1 << i] + 1
    return table


def domination_counts(n, closed, pop):
    """X_k for k = 0..n: number of k-sets S with N[S] = [n]."""
    reach = np.zeros(1 << n, dtype=np.int64)
    for i in range(n):
        reach[1 << i:1 << (i + 1)] = reach[0:1 << i] | closed[i]
    dominating = reach == (1 << n) - 1
    return [int(x) for x in np.bincount(pop[dominating], minlength=n + 1)]


def failures(n, X):
    C = [math.comb(n, k) for k in range(n + 1)]
    lc = [k for k in range(1, n) if X[k] ** 2 < X[k - 1] * X[k + 1]]
    ulc = [k for k in range(1, n)
           if X[k] ** 2 * C[k - 1] * C[k + 1] < X[k - 1] * X[k + 1] * C[k] ** 2]
    gamma = next(k for k in range(n + 1) if X[k] > 0)
    return lc, ulc, gamma


def closed_neighbourhoods(n, edges, present):
    closed = [1 << v for v in range(n)]
    for (v, w), e in zip(edges, present):
        if e:
            closed[v] |= 1 << w
            closed[w] |= 1 << v
    return closed


def run():
    rng = np.random.Generator(np.random.PCG64(SEED))
    rows = []
    for n in range(2, 19):
        edges = list(itertools.combinations(range(n), 2))
        pop = popcounts(n)
        if n <= 6:
            mode = 'exhaustive'
            source = (((code >> b) & 1 for b in range(len(edges)))
                      for code in range(1 << len(edges)))
        else:
            mode = 'sample'
            draws = rng.integers(0, 2, size=(SAMPLES, len(edges)))
            source = (row for row in draws)
        total = lc_fail = ulc_fail = 0
        offsets = {}
        lc_offsets = {}
        for present in source:
            X = domination_counts(n, closed_neighbourhoods(n, edges, present), pop)
            lc, ulc, gamma = failures(n, X)
            total += 1
            lc_fail += bool(lc)
            for k in lc:
                lc_offsets[k - gamma] = lc_offsets.get(k - gamma, 0) + 1
            if ulc:
                ulc_fail += 1
                for k in ulc:
                    offsets[k - gamma] = offsets.get(k - gamma, 0) + 1
            # Consistency: an LC failure is always a ULC failure.
            if lc and not ulc:
                sys.exit(f'inconsistent LC/ULC test at n={n}')
        row = {'n': n, 'mode': mode, 'graphs': total, 'lc_failures': lc_fail,
               'ulc_failures': ulc_fail,
               'lc_failing_index_minus_gamma': {str(k): v for k, v in sorted(lc_offsets.items())},
               'ulc_failing_index_minus_gamma': {str(k): v for k, v in sorted(offsets.items())}}
        rows.append(row)
        print(f"n={n:2d} {mode:10s} graphs={total:6d} LC-fail={lc_fail} "
              f"ULC-fail={ulc_fail} LC index-gamma={dict(sorted(lc_offsets.items()))} "
              f"ULC index-gamma={dict(sorted(offsets.items()))}", flush=True)
    return rows


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', default=None)
    args = parser.parse_args()
    rows = run()
    # Fixed facts that the paper quotes; exit nonzero if any changes.
    expected = {5: (0, 5), 6: (0, 636)}
    for row in rows:
        if row['n'] in expected and (row['lc_failures'], row['ulc_failures']) != expected[row['n']]:
            sys.exit(f"unexpected exhaustive count at n={row['n']}")
    result = {'seed': SEED, 'samples_per_n_from_7': SAMPLES, 'edge_probability': '1/2',
              'rows': rows}
    if args.output:
        with open(args.output, 'w') as fh:
            json.dump(result, fh, indent=1)
    print('PASS finite-n table')


if __name__ == '__main__':
    main()
