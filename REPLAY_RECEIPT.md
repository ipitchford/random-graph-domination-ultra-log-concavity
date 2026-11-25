# Replay receipt (v0.1.0-candidate, 25 November 2026)

Release replay by the publisher from fresh copies of the approved candidate (code and requirements only; results
regenerated), working directory = package root, macOS arm64. Interpreters as printed inside the runs: CPython 3.12.11,
mpmath 1.3.0, NumPy 2.3.5 (see [ENVIRONMENT.txt](ENVIRONMENT.txt)).

| Run | Command | Exit | Output vs recorded |
|---|---|---|---|
| verify -O | `uv run --python 3.12 --with mpmath==1.3.0 python3 -I -B -O code/verify.py` | 0 | identical |
| audit_checks -O | `uv run --python 3.12 --with mpmath==1.3.0 python3 -I -B -O code/audit_checks.py` | 0 | identical |
| check_tuning -O | `uv run --python 3.12 --with mpmath==1.3.0 python3 -I -B -O code/check_tuning.py` | 0 | identical |
| finite_n -O | `uv run --python 3.12 --with numpy==2.3.5 python3 -I -B -O code/finite_n.py --output results/finite-n.json` | 0 | finite-n.json and stdout identical ("PASS finite-n table") |
| natural_density -O | `uv run --python 3.12 --with mpmath==1.3.0 python3 -I -B -O code/natural_density.py --output results/natural-density.json` | 0 | natural-density.json and stdout identical ("PASS natural-density illustration") |
| verify, audit_checks, check_tuning without -O | as above without -O | 0, 0, 0 | identical |
| Negative control 1 | verify.py with the tail bound made too strong (`- 2 * rho**(k - 1))` replaced by `+ 1)`), under -O | 1 | `CHECK FAILED: verify.py check 2` |
| Negative control 2 | check_tuning.py with a negative tolerance (`mp.mpf('1e-30')` replaced by `mp.mpf('-1')`), under -O | 1 | `CHECK FAILED: check_tuning.py check 1` |

stderr was empty for every passing run. The lead's earlier clean replay (24 November 2026, CPython 3.14.7 through the
uv shim) also produced byte-identical outputs. After the replay only the title-page DOI line of manuscript.tex, the
rebuilt PDF and the release records changed; code/ and results/ are byte-identical to the replayed candidate.

Comparison policy for other platforms (declared before tagging; also in CI, README.md and ENVIRONMENT.txt):
verify.stdout, finite-n.stdout and finite-n.json byte-identical; the four files with printed mpmath values compared
number by number, with text and integers identical and decimal numbers within 1e-6 relative.
