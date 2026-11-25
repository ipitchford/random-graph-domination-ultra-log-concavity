# When is the domination polynomial of a random graph ultra-log-concave?

Version 0.1.0-candidate, 25 November 2026. DOI [10.5281/zenodo.24540957](https://doi.org/10.5281/zenodo.24540957)
(all versions: [10.5281/zenodo.24540956](https://doi.org/10.5281/zenodo.24540956)). Author: Anonymous.
Release page: https://evidencepress.org/releases/random-graph-domination-ultra-log-concavity/

**Status: unrefereed research candidate.** The results have written proofs that were checked by internal AI-assisted
review, with finite computer checks. No human referee has assessed them.

## What this is about

In a network, a *dominating set* is a set of nodes such that every node is either in the set or linked to a node in it,
like guards placed so that every site is watched. Counting the dominating sets of each size gives a sequence of numbers,
the coefficients of the *domination polynomial*. A sequence is *log-concave* if each term squared is at least the
product of its two neighbours. A log-concave sequence of positive numbers rises to one peak and then falls, with no
second hump.

Cameron checked every network with at most nine nodes in 2019. Exactly one fails log-concavity: its counts begin
1, 7, 50, and 7 × 7 is less than 1 × 50. He asked whether almost all networks have log-concave counts. (The stronger
claim that every domination polynomial has a single peak is now known to be false for some very large networks:
[10.5281/zenodo.24511988](https://doi.org/10.5281/zenodo.24511988).)

## What the paper shows

1. **Yes, almost always.** In a random network on n nodes where each link is present independently with probability p,
   the counts are log-concave with probability tending to one, and so are the *proportions* of sets of each size that
   dominate (the stronger property called ultra-log-concavity). This holds when p stays below 1 − ε and p(log n)²
   tends to infinity. Taking p = 1/2, which is a uniformly random network, shows that almost all networks have this
   property, whether nodes are labelled or networks are counted up to relabelling. This answers Cameron's question.
2. **The density scale is the right one.** When p(log n)² stays bounded, there are carefully tuned densities at which
   log-concavity fails with an explicit probability. Whether it fails is decided by the number of smallest dominating
   sets, which behaves like a Poisson count: for example, one tuning gives probability 1/2.
3. **Natural sparse densities do not settle.** For p = θ/(log n)², the probability of log-concavity is close to one for
   almost every n but drops well below one for infinitely many n.
4. **A consequence.** The size of a randomly chosen dominating set (weighted by size in any of the natural ways) is at
   least as concentrated as a binomial variable with the same mean.

Small computations at p = 1/2 agree with the picture: ultra-log-concavity fails for 636 of the 32,768 labelled networks
on 6 nodes and for 11 of 20,000 sampled networks on 18 nodes, and nearly every failure is at the second nonzero count,
the same place where Cameron's example fails.

**Limits.** The results are asymptotic: they give no explicit n beyond which they hold. Very dense networks (p close to
one) and sparser ones (p(log n)² tending to zero) are not covered. Convergence at the boundary scale is slow. The finite
computations illustrate the theorems; they do not prove them.

## Contents

| File | What it is |
|---|---|
| [manuscript.pdf](manuscript.pdf), [manuscript.tex](manuscript.tex) | The paper (14 pages); Section 1 is a plain introduction with a roadmap |
| [code/verify.py](code/verify.py) | Exact checks (standard library): the mean formula for n ≤ 5; the deterministic tail inequality (Lemma 5.1) on all three-set families for n ≤ 6 |
| [code/audit_checks.py](code/audit_checks.py) | Exhaustive counts and exact averages for n ≤ 6; 1904 hypergeometric identities; integer-boundary thresholds at n = 2^128, 2^512, 2^2048 (mpmath) |
| [code/check_tuning.py](code/check_tuning.py) | The tuned densities of Theorem 2.3 at log n = 100, 500, 1000 (mpmath) |
| [code/finite_n.py](code/finite_n.py) | Table 1: failures of log-concavity and ultra-log-concavity in G(n, 1/2), exhaustive for n ≤ 6, 20,000 seeded samples for 7 ≤ n ≤ 18 (NumPy) |
| [code/natural_density.py](code/natural_density.py) | The slow-convergence illustration for p = 1/(log n)² near log n = 60 (mpmath) |
| [results/](results) | Recorded outputs of the five scripts |
| [AI_INDEX.md](AI_INDEX.md) | Machine-oriented map of claims, evidence and limits |
| [REVIEW_SUMMARY.md](REVIEW_SUMMARY.md) | What internal checking was done and how objections were handled |
| [RESEARCH_GATES.json](RESEARCH_GATES.json) | Prior-art and limitation record |
| [REPLAY_RECEIPT.md](REPLAY_RECEIPT.md), [ENVIRONMENT.txt](ENVIRONMENT.txt) | Replay runs and environment |
| [refs.bib](refs.bib) | Bibliography of the paper |
| [CITATION.cff](CITATION.cff), [LICENSE.md](LICENSE.md), [MANIFEST.sha256](MANIFEST.sha256) | Citation, licences, hashes |

## Replay (about two minutes)

From the package root, with [uv](https://docs.astral.sh/uv/):

```sh
uv run --python 3.12 --with mpmath==1.3.0 python3 -I -B -O code/verify.py        # = results/verify.stdout
uv run --python 3.12 --with mpmath==1.3.0 python3 -I -B -O code/audit_checks.py  # = results/audit_checks.stdout
uv run --python 3.12 --with mpmath==1.3.0 python3 -I -B -O code/check_tuning.py  # = results/check_tuning.stdout
uv run --python 3.12 --with numpy==2.3.5 python3 -I -B -O code/finite_n.py --output results/finite-n.json
uv run --python 3.12 --with mpmath==1.3.0 python3 -I -B -O code/natural_density.py --output results/natural-density.json
```

Every check raises an error with a nonzero exit status on failure, also under `python -O`. Comparison policy (declared
before tagging; also in CI, ENVIRONMENT.txt and REPLAY_RECEIPT.md): `verify.stdout`, `finite-n.stdout` and
`finite-n.json` are exact and must be byte-identical; in `audit_checks.stdout`, `check_tuning.stdout`,
`natural-density.stdout` and `natural-density.json` (mpmath values printed to 6-10 significant digits) the text and
integers must be identical and decimal numbers must agree within 1e-6 relative. GitHub Actions runs all five scripts on
Linux, compares under this policy and runs two negative controls.

## Assurance

Internal AI-assisted review only: a combined five-role Claude review panel, one revision round with extensions, a
verification re-review with a proof audit of every new or rewritten proof, and clean replays with negative controls.
No Astra/Codex review took place. This is not peer review, independent reproduction or formal verification.

## Licence and citation

Text, paper, recorded outputs and records: CC0-1.0. Code: MIT. See [LICENSE.md](LICENSE.md). Cite as: Anonymous,
*When is the domination polynomial of a random graph ultra-log-concave?*, Evidence Press, version 0.1.0-candidate (2026),
https://doi.org/10.5281/zenodo.24540957.
