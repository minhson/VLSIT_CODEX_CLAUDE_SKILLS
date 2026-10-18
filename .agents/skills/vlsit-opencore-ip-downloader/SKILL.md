---
name: vlsit-opencore-ip-downloader
description: Search OpenCores and its linked public repositories for open-source hardware IP, download each project with its RTL, documentation, license, and related collateral, then write a README that compares the IPs' features, functions, status, FPGA capability, and ASIC tapeout readiness with special notes. Use when asked to find, collect, or evaluate existing IP cores; not for designing a new core.
---

# VLSIT OpenCores IP Search and Download

## Operating contract

1. Read [rule.md](rule.md) completely before doing anything. Its numbered rules (OCI-xxx) are mandatory and rank above everything else.
2. Follow the workflow below. It orders the work; it never relaxes a rule.
3. Consult `reference/` for templates and examples when needed. They rank below `rule.md`.
4. Prerequisite (OCI-096): run `python --version`; if Python is missing, propose installing it (Windows: `winget install Python.Python.3.12`) and wait for approval.
5. Run helpers from `scripts/` (index: [scripts/README.md](scripts/README.md)) instead of repeating manual steps.
6. Excel or CSV input (OCI-097): analyze it with `scripts/vlsit_analyze_excel.py` (needs `openpyxl`); report any script problem and propose an update to the script.
7. Apply the self-improvement rules OCI-090..096 at the end of every run.

## Workflow

1. **Intake (OCI-010..013).** Confirm IP type, count, and absolute destination; ask for all gaps in one message and wait.
2. **Search and select (OCI-020..025).** Search OpenCores and aliases, open candidate pages, verify function and license, remove duplicates and mirrors. When OpenCores has no suitable IP, search GitHub and Gitee with `python scripts/vlsit_ip_search.py search "<keywords>" --source both` and apply OCI-025 to Chinese-language sources.
3. **Download (OCI-030..032).** Fetch the complete project package from the official link or the upstream repository.
4. **Verify and store (OCI-040..043, OCI-060).** Run `python scripts/vlsit_verify_archive.py <ARCHIVE>` before extraction, extract into a per-project folder, write `DOWNLOAD_INFO.md` per project and update `CATALOG.md`.
5. **Evaluate (OCI-050..057).** Write the bilingual `README.md` using [reference/vlsit_readme_template.md](reference/vlsit_readme_template.md).
6. **Report (OCI-061..062).** Summarize per OCI-061 without claiming validation.
7. **Improve (OCI-090..096).** Add or fix scripts and reference files, log the change in `reference/vlsit_improvement_log.md`, and propose any rule changes to the user.

## Folder map

| Path | Role | Priority |
|---|---|---|
| `rule.md` | Numbered mandatory rules | 1 (highest) |
| `SKILL.md` | Workflow and routing | 2 |
| `reference/` | Templates, examples, improvement log | 3 |
| `scripts/` | Helper scripts, grown by the model per OCI-090 | tool |
