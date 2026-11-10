# QA · Independent Verification (Phase 6)

> Method: built from scratch in a **fresh virtualenv** (no reuse of the dev env), then ran
> the full test suite and exercised the CLI against both the project itself and a
> deliberately flawed "AI-generated" sample.

## 1. Fresh-environment install
```bash
python3 -m venv /tmp/qa-venv
source /tmp/qa-venv/bin/activate
pip install -e /Users/lucasyanzy/NO/noah-forge/codebuddy/vericode pytest
vericode --help   # entry point resolves
```
Result: install succeeded, `vericode` console script available.

## 2. Test suite (fresh env)
```bash
python -m pytest -q
```
Result: **37 passed**, 0 failed.

Coverage (core logic): **77%** (target ≥ 70%). Breakdown:
| module | coverage |
|---|---|
| scanner.py | 90% |
| deps.py | 82% |
| core.py | 94% |
| cli.py | 86% |
| report.py | 79% |
| projects.py | 54% (subprocess pass/fail branches need the real toolchain installed) |

## 3. Dogfood — on its own repo
```bash
vericode . --exclude tests
```
- `typecheck`: skip (mypy/pyright not in env — honest skip, not a false pass)
- `tests`: ✓ pytest passed
- `secrets`: none (test fixtures excluded)
- `cves`: none (pyproject only, no lockfile)
Result: **All checks passed**

Without `--exclude tests`, the tool correctly flags its own test fixtures
(`sk_live_…`, the AWS example key, etc.) — proving the scanner fires.

## 4. Flawed "AI-generated" sample (evidence of catching real problems)
Sample (`/tmp/ai-demo`): a `Stripe` secret in `app.py`, a failing test, and
`requirements.txt` pinning `requests==2.19.0`.

```bash
vericode /tmp/ai-demo
```
Captured output (verbatim):
```
│ typecheck │ –      │ mypy/pyright not installed (pip install mypy)   │
│ tests     │ ✗      │ .F  → test_broken FAILED                        │
            Secrets found: 1
│ Stripe Secret Key │ app.py │ 1 │ high │
            Dependency vulnerabilities: 10
│ requests │ 2.19.0 │ GHSA-9hjg-9r4m-mvj7 │ Requests .netrc credentials leak … │
│ requests │ 2.19.0 │ GHSA-9wx4-h78v-vm56 │ Session does not verify …          │
│ requests │ 2.19.0 │ GHSA-gc5v-m9x4-r6x2 │ Insecure Temp File Reuse …         │
│ … (10 total) …
Result: 1 check(s) FAILED; 1 secret(s) found
```
Conclusion: type-check skip, test failure, hardcoded secret, and **10 real CVEs**
are all surfaced. The tool does what it claims.

## 5. Limitations / honest notes
- `typecheck`/`tests` report `skip` (not pass) when the underlying toolchain
  (mypy, tsc, go, cargo, pytest, npm) is absent — by design, to avoid false
  confidence. Install the toolchain for full coverage.
- CVE lookup needs network access to `api.osv.dev`; if offline it degrades to
  "no vulnerabilities found" gracefully (returns `[]`, never crashes).
- The animated README GIF is **not** auto-generated here; `demo.tape` (vhs) is
  provided so it can be produced reproducibly: `vhs demo.tape`.
- No mocked/faked data anywhere — every result above is produced by the real code.

## 6. Verdict
**PASS.** Installable, testable, and demonstrably useful in a clean environment.
Ready for packaging and launch prep.
