# Review summary (internal, AI-assisted)

This is a rating-free public summary of the internal checking of version 0.1.0-candidate. It is not peer review,
independent reproduction or formal verification. No human referee has assessed the paper.

## What was done (24 November 2026)

1. **Combined five-role review panel** (one Claude subagent taking the roles of editor, methodology and proof audit,
   domain and literature, significance and extensions, and devil's advocate) on the first draft, with the cited sources
   read. The panel replayed the scripts and recomputed the load-bearing numbers (the coefficient 11 in the tuning
   expansion, the sign at theta = 0, the thresholds on both sides of an integer). It found no mathematical error and no
   critical issue. Its major items concerned context, framing, credit and finite-n evidence.
2. **One revision round with extensions.** A context-first introduction and roadmap; the word "sharp" replaced by the
   precise statement that the scale is the right one for a guarantee valid along every density sequence; a new theorem
   for natural densities p = theta/(log n)^2 (Theorem 2.5) in place of a suggested remark; a quantitative form for
   general densities at the boundary scale (Proposition 6.1); the transfer to unlabelled graphs (Corollary 2.2), so the
   paper answers Cameron's question as he posed it; finite-n evidence (Table 1) and a slow-convergence illustration;
   citations to Du-Heilman-Panova and to Ross (Stein's method) added; credit for the standard large-mean second-moment
   bounds; explicit checks in place of assert in every script, with negative controls.
3. **Verification re-review and proof audit** of every new or rewritten proof (Lemma 3.1, Corollary 3.2, Lemma 4.1,
   Proposition 6.1, Theorem 2.5 and the restated Theorems 2.1 and 2.3), with independent recomputation of the
   slow-convergence numbers. Items raised were applied (a missing factor in an error term, the step bound in the
   natural-density proof, notation, table caption, crediting the nine-vertex graph also to Beaton-Brown, and the
   unlabelled case). No open correctness issue remained. The one proof added after that round (Corollary 2.2) is
   elementary and was audited line by line by the lead.
4. **Clean replay** of the scripts from fresh copies with negative controls, by the lead and again by the publisher
   (see [REPLAY_RECEIPT.md](REPLAY_RECEIPT.md)).

No Astra/Codex second-model review took place: that route reported the model as unsupported for the account.

## Main objections and how they were handled

| Objection | Disposition |
|---|---|
| "The threshold is called sharp, but a fixed density at the boundary scale works for most n." | Correct; the framing was changed. Theorem 2.3 concerns densities tuned to n, and Remark 2.4 says so. Theorem 2.5 proves that for p = theta/(log n)^2 the probability tends to one along a density-one set of n, but has liminf below one. |
| "The second-moment bounds are standard." | For counts with mean at least e^{cL^2} they are (Wieland-Godbole, Glebov-Liebenau-Szabo, Mitsche-Perez-Gimenez-Pralat), and the paper says so. The new ingredient is the e^{-Omega(L^2)}/mu_k term, which keeps the estimate useful when the mean is bounded. |
| "Cameron counted graphs up to isomorphism." | Corollary 2.2 transfers the result to isomorphism classes with a self-contained count of graphs with nontrivial automorphisms. |
| "Is ultra-log-concavity really stronger in practice?" | Table 1: at small n ultra-log-concavity fails far more often than log-concavity (636 graphs at n = 6 against none), and Theorem 2.3 has tunings that separate the two properties. |
| "Prior work on random graphs?" | Du-Heilman-Panova (2026) note that the Beaton-Brown argument does not reach sparse random graphs and ask about log-concavity for random graphs; they are cited, and no earlier result on log-concavity for a single random graph was found. |
| "Reliance on asymptotics." | Stated in Section 8: no explicit n, slow convergence at the boundary scale (curvature 0.58 at log n = 100), finite computations are illustrations only. |
| Not addressed | The dense regime p -> 1 was attempted and is stated as open problem 1; sparser densities and real-rootedness are open problems 2 and 3. |

## Scope of assurance

Internal AI-assisted review only: written proofs checked by AI reviewers, finite computer checks replayed, sources
read. No human specialist review, no independent reproduction by an unaffiliated party, no proof-assistant
formalisation. Literature searches were of limited scope (see [RESEARCH_GATES.json](RESEARCH_GATES.json)).
