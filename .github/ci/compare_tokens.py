# SPDX-License-Identifier: MIT
"""Compare a fresh output file with the recorded one under the declared policy.

usage: compare_tokens.py NEW RECORDED

Policy (declared before tagging; the same in README.md, ENVIRONMENT.txt and REPLAY_RECEIPT.md), used for the files with
printed mpmath values (results/audit_checks.stdout, results/check_tuning.stdout, results/natural-density.stdout and
results/natural-density.json):
- the text between numbers is identical;
- integer literals are identical;
- decimal or exponent-form numbers may differ by at most 1e-6 relative.
The exact outputs (results/verify.stdout, results/finite-n.stdout, results/finite-n.json) are compared byte for byte
with cmp, not with this script. Exits 1 on any difference.
"""
import re
import sys

NUM = re.compile(r'[-+]?(?:\d+\.\d*|\.\d+|\d+)(?:[eE][-+]?\d+)?')


def split(text):
    parts, pos = [], 0
    for m in NUM.finditer(text):
        parts.append(('text', text[pos:m.start()]))
        parts.append(('num', m.group()))
        pos = m.end()
    parts.append(('text', text[pos:]))
    return parts


def main():
    new = open(sys.argv[1], encoding='utf-8').read()
    old = open(sys.argv[2], encoding='utf-8').read()
    a, b = split(new), split(old)
    bad, exact, close = [], 0, 0
    if len(a) != len(b):
        bad.append(f'token count {len(a)} vs {len(b)}')
    else:
        for (ka, x), (kb, y) in zip(a, b):
            if ka != kb or (ka == 'text' and x != y):
                bad.append(f'text {x!r} vs {y!r}')
            elif ka == 'num':
                if x == y:
                    exact += 1
                elif re.fullmatch(r'[-+]?\d+', x) or re.fullmatch(r'[-+]?\d+', y):
                    bad.append(f'integer {x} vs {y}')
                elif abs(float(x) - float(y)) > 1e-6 * max(abs(float(x)), abs(float(y))):
                    bad.append(f'{x} vs {y} beyond 1e-6 relative')
                else:
                    close += 1
    if bad:
        print('DIFFERENCES in', sys.argv[2])
        for m in bad[:20]:
            print(' ', m)
        sys.exit(1)
    print(f'OK {sys.argv[2]}: {exact} numbers identical, {close} within 1e-6 relative')


if __name__ == '__main__':
    main()
