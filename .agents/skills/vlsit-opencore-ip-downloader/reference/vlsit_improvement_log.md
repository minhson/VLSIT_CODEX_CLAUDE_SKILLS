# Improvement log

Append one entry per skill improvement (rule OCI-093). Newest last.

| Date | Reason (observed friction) | Change |
|---|---|---|
| 2026-10-13 | Restructure into rule.md / reference / scripts | Moved mandatory requirements to `rule.md` with IDs; added `vlsit_readme_template.md`; added `scripts/vlsit_verify_archive.py` (untested: no Python in authoring environment) |
| 2026-10-16 | User asked for the standard structure (SKILL.md workflow, rule.md with non-duplicating IDs, reference, Python scripts with a minimal library set, installation proposal when Python is missing) | The rule file was audited for duplicate IDs and undefined references (0 found); added the Python prerequisite rule (OCI-096) and the stdlib-only script convention; Python installed with the user approval (3.12.10) and every script tested on real input; status columns updated |
| 2026-10-17 | User asked that every skill analyze Excel files with one shared script | Copied `vlsit_analyze_excel.py` into `scripts/`; added rule OCI-097 (use it for all Excel/CSV input, `openpyxl` exemption, propose script updates on problems); SKILL.md and scripts index updated |
| 2026-10-18 | User asked that IP from Chinese sites may be downloaded when it is truly good for ASIC tapeout and free | Added rule OCI-025 (conditions, approval and English summary); copied `scripts/vlsit_ip_search.py` (GitHub and Gitee search with evidence scoring); SKILL.md step 2 and the scripts index updated |
