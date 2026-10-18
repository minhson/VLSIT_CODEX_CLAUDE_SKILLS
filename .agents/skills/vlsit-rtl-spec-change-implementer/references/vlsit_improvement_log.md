# Improvement log

Append one entry per skill improvement (rule RSC-093). Newest last.

| Date | Reason (observed friction) | Change |
|---|---|---|
| 2026-10-13 | Restructure into rule.md / references / scripts | Moved mandatory requirements to `rule.md` with IDs; added `vlsit_review_template.md`; added `scripts/vlsit_rtl_change_metrics.py` (untested: no Python in authoring environment) |
| 2026-10-16 | User asked for the standard structure (SKILL.md workflow, rule.md with non-duplicating IDs, references, Python scripts with a minimal library set, installation proposal when Python is missing) | The rule file was audited for duplicate IDs and undefined references (0 found); added the Python prerequisite rule (RSC-096) and the stdlib-only script convention; Python installed with the user approval (3.12.10) and every script tested on real input; status columns updated |
| 2026-10-17 | User asked that every skill analyze Excel files with one shared script | Copied `vlsit_analyze_excel.py` into `scripts/`; added rule RSC-097 (use it for all Excel/CSV input, `openpyxl` exemption, propose script updates on problems); SKILL.md and scripts index updated |
