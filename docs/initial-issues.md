# Initial issues to open at launch (≥ 5 "good first issue")

Each of these is a self-contained, small task suitable for new contributors.

### 1. [good first issue] Add a `vericode --version` flag
The CLI has no `--version`. Add it via `click.version_option(__version__)`
(import from `vericode.__init__`). Add a unit test asserting it prints the version.

### 2. [good first issue] Support scanning a single file
Today `vericode` only takes a directory. Allow `vericode path/to/file.py`
by reusing `scanner.scan_text` on that file. Add a test.

### 3. [good first issue] Add a Terraform / HCL secret rule
Extend `SECRET_PATTERNS` in `scanner.py` with a Terraform `aws_secret` style
pattern and a test in `test_scanner.py`.

### 4. [good first issue] Document `--exclude` with examples in README
Show excluding `migrations/`, `fixtures/`, etc. Add a short section + example
output.

### 5. [good first issue] Cache OSV responses to disk
CVE lookups repeat across runs. Add a small TTL cache (e.g. `~/.cache/vericode`)
keyed by `ecosystem:name:version`. Cover with a test using `tmp_path`.

### 6. [enhancement] SARIF output for GitHub code scanning
Add `--sarif out.sarif` that emits findings in SARIF 2.1.0 so VeriCode can be
wired into GitHub code scanning as a workflow step.

### 7. [enhancement] HTML report
`--html report.html` rendering the same data as the terminal report, for CI artifacts.
