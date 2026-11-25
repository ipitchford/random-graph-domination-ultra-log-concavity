"""Exact, self-contained checks for the mean formula and the deterministic tail bound.

Run with Python 3.10+ and its standard library. These finite checks exercise the
identities in the proof. They do not establish the asymptotic theorems.
"""
from fractions import Fraction
from itertools import combinations
from math import comb



def check(condition, message):
    """Fail loudly even under python -O (assert statements are stripped there)."""
    if not condition:
        raise SystemExit('CHECK FAILED: ' + message)

def profiles(n, closed):
    full = (1 << n) - 1
    neighbours = [0] * (1 << n)
    counts = [0] * (n + 1)
    for mask in range(1, 1 << n):
        bit = mask & -mask
        neighbours[mask] = neighbours[mask ^ bit] | closed[bit.bit_length() - 1]
        if neighbours[mask] == full:
            counts[mask.bit_count()] += 1
    return counts


def check_averages():
    for n in range(1, 6):
        edges = list(combinations(range(n), 2))
        graphs = 1 << len(edges)
        totals = [0] * (n + 1)
        for graph in range(graphs):
            closed = [1 << v for v in range(n)]
            for bit, (v, w) in enumerate(edges):
                if graph & (1 << bit):
                    closed[v] |= 1 << w
                    closed[w] |= 1 << v
            counts = profiles(n, closed)
            for k, value in enumerate(counts):
                totals[k] += value
        means = [Fraction(t, graphs) for t in totals]
        formula = [Fraction(comb(n, k)) * (1-Fraction(1, 2**k))**(n-k)
                   for k in range(n + 1)]
        check(means == formula, 'verify.py check 1')
        print(f'n={n}, {graphs} labelled graphs, exact mean:', *map(str, means))


def check_tail():
    # Nonempty distinct B_i suffice here. Empty sets contribute nothing at k>=2.
    for n in range(2, 7):
        tested = 0
        all_sets = list(range(1, 1 << n))
        for family in combinations(all_sets, 3):
            sizes = [b.bit_count() for b in family]
            rho = max(Fraction((b & c).bit_count(), b.bit_count())
                      for b in family for c in family if b != c)
            if rho == 1:
                continue
            d = n - max(sizes)
            failures = [0] * (n + 1)
            for mask in range(1 << n):
                if any(mask & b == mask for b in family):
                    failures[mask.bit_count()] += 1
            c = [Fraction(z, comb(n, j)) for j, z in enumerate(failures)]
            for k in range(2, n):
                h = Fraction(sum(comb(b, k - 1) for b in sizes), comb(n, k - 1))
                bound = h * (Fraction(d * (d - 1), n * (n - 1)) - 2 * rho**(k - 1))
                check(c[k-1] - 2*c[k] + c[k+1] >= bound, 'verify.py check 2')
                tested += 1
        print(f'n={n}, {tested} exact tail comparisons across three-set families')


if __name__ == '__main__':
    check_averages()
    check_tail()
