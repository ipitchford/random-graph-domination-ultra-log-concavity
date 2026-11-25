# AI index: When is the domination polynomial of a random graph ultra-log-concave? (v0.1.0-candidate)

Machine-oriented map of claims, evidence and limits. Human readers should start with [README.md](README.md) ("What
this is about") and the paper [manuscript.pdf](manuscript.pdf) (source [manuscript.tex](manuscript.tex); Section 1 is
a plain introduction with the question, prior work, the results, the mechanism and a roadmap).
DOI 10.5281/zenodo.24540957 (concept 10.5281/zenodo.24540956). Status: unrefereed candidate; internal AI-assisted
review and finite computation only.

## Normalisation

G(n,p): vertex set [n], each edge independently with probability p; q = 1 - p, a = -log q, L = log n (natural).
S dominating: every vertex outside S has a neighbour in S. X_k = number of dominating k-sets; D_G(z) = sum_k X_k z^k.
R_k = X_k / C(n,k). LC: X_k^2 >= X_{k-1} X_{k+1}. ULC (of order n): R_k^2 >= R_{k-1} R_{k+1} for 1 <= k < n; ULC implies
LC. gamma = domination number, delta = minimum degree. b_k = E R_k = (1 - q^k)^(n-k), mu_k = E X_k = C(n,k) b_k.
whp = with probability tending to one as n -> infinity.

## Claims and where they are proved

| ID | Claim | Location | Status / credit |
|---|---|---|---|
| A (main) | If p <= 1 - eps and p L^2 -> infinity, whp D_G is ULC at every 1 <= k < n, strictly exactly for gamma <= k <= n - delta; X_k^2 > X_{k-1} X_{k+1} for gamma < k < n | Theorem 2.1 | written proof (Sections 3-5) |
| B | At p = 1/2: almost all labelled graphs and almost all isomorphism classes have a ULC (hence LC) domination polynomial; answers Cameron's question (thesis 2019, Section 6.5) | Theorem 2.1, Corollary 2.2 | written proof (Burnside-type count for unlabelled graphs) |
| C | For each theta in [0, inf) and lambda > 0, tuned p with E X_r = lambda (r = floor(L^3/theta), or floor(L^4) at theta = 0) has p L^2 -> theta and P(ULC) and P(LC) -> P{Pois(lambda) < lambda e^theta} (theta > 0) or P{Pois(lambda) <= lambda} (theta = 0); at theta = 0, lambda = log 2 the limit is 1/2; other tunings give LC but not ULC with limit e^-lambda lambda^m / m! | Theorem 2.3 | written proof (Section 6) |
| D | p = theta/L^2: P(ULC) -> 1 along a set of n of natural density one; along infinitely many n, P(LC) and P(ULC) -> P{Pois(lambda) < lambda e^theta}; limsup 1, liminf <= exp(-e^-theta) < 1 | Theorem 2.5, Proposition 6.1 | written proof |
| E | Second moment for k near L/a with an e^{-Omega(L^2)}/mu_k term; Poisson limit of X_k when mu_k -> lambda (monotone coupling, Ross 2011 Theorem 4.14) | Lemma 3.1, Corollary 3.2 | written proof; large-mean bounds are standard (Wieland-Godbole, Glebov-Liebenau-Szabo, Mitsche-Perez-Gimenez-Pralat) |
| F | Deterministic second-difference inequality for the probability that a random k-set lies in one of B_1..B_m | Lemma 5.1 | written proof; exact checks |
| G | Binomial convex order for the size of a z^{|S|}-weighted random dominating set on the event of A; Var <= n y(1 - y) | Corollary 2.6 | written proof (standard; compare Daly 2016 Theorem 4.2) |
| H | Finite data at p = 1/2: ULC fails for 5 of 1,024 (n = 5), 636 of 32,768 (n = 6), 11 of 20,000 sampled (n = 18); LC failures only at n = 14 and 16 (one each, at gamma + 1); every failing graph fails one comparison, within three of gamma | Section 8, Table 1 | computation (exhaustive n <= 6; seeded samples 7 <= n <= 18) |

## Evidence

| Check | Script | Output | Arithmetic |
|---|---|---|---|
| Exact mean of X_k over all labelled graphs n <= 5 equals formula (eq. 3); Lemma 5.1 on all three-set families (3,270 comparisons at n = 5, 56,000 at n = 6) | [code/verify.py](code/verify.py) | [results/verify.stdout](results/verify.stdout) | exact (fractions) |
| Exhaustive n <= 6: exact averages and ULC failure counts (5, 636); 1904 hypergeometric identities (eq. 9); integer-boundary sides at theta = 0, 1 for n = 2^128, 2^512, 2^2048 | [code/audit_checks.py](code/audit_checks.py) | [results/audit_checks.stdout](results/audit_checks.stdout) | exact integers; mpmath at 2*power + 256 bits |
| Tuned densities (eq. 11), lambda = 0.7: curvature C_r = 0.58213441 (log n = 100), 0.92689013 (log n = 1000) at theta = 1 | [code/check_tuning.py](code/check_tuning.py) | [results/check_tuning.stdout](results/check_tuning.stdout) | mpmath, about log n / log 10 + 80 digits |
| Table 1 (all rows, offsets from gamma) | [code/finite_n.py](code/finite_n.py) | [results/finite-n.json](results/finite-n.json), [results/finite-n.stdout](results/finite-n.stdout) | exact integer tests; NumPy PCG64 seed 20261124 |
| p = 1/L^2 near L = 60: C_s 0.600732-0.6009; dF_s/dL = -1.90863e7; jump 2211.23 = 0.614231 L^2 | [code/natural_density.py](code/natural_density.py) | [results/natural-density.json](results/natural-density.json), [results/natural-density.stdout](results/natural-density.stdout) | mpmath, 80 digits |

Numbers quoted on the release page and in its audio: nine nodes; 7 x 7 < 1 x 50; 317,440 nodes (related release
10.5281/zenodo.24511988); 636 of 32,768 at 6 nodes; 11 of 20,000 at 18 nodes (about 1 in 1,800); p = 1/2;
p about 1/(log n)^2; limiting probability 1/2 at lambda = log 2, theta = 0. All are proved in the paper, reproduced by
the scripts or taken from the cited sources.

## Limits

Asymptotic results; constants not explicit, so no specific n is given. Theorem 2.1 assumes p <= 1 - eps; Theorems 2.3
and 2.5 concern polylogarithmic densities; p -> 1 and p L^2 -> 0 are open (Section 8, open problems 1-2). Convergence
at the boundary scale is slow. The finite computations do not certify the limit theorems.

## Replay and records

Replay commands and the comparison policy (verify.stdout, finite-n.stdout, finite-n.json byte-identical; files with
printed mpmath values compared number by number, decimals within 1e-6 relative): [README.md](README.md),
[ENVIRONMENT.txt](ENVIRONMENT.txt), [REPLAY_RECEIPT.md](REPLAY_RECEIPT.md), CI
[.github/workflows/replay.yml](.github/workflows/replay.yml) with [.github/ci/compare_tokens.py](.github/ci/compare_tokens.py).
Review: [REVIEW_SUMMARY.md](REVIEW_SUMMARY.md). Prior art and limitation triage: [RESEARCH_GATES.json](RESEARCH_GATES.json).
Bibliography: [refs.bib](refs.bib). Licences: [LICENSE.md](LICENSE.md). Citation: [CITATION.cff](CITATION.cff).
Hashes: [MANIFEST.sha256](MANIFEST.sha256).
