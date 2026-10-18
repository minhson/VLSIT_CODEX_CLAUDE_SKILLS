# Improvement log

Append one entry per skill improvement (rule V2S-093). Newest last.

| Date | Reason (observed friction) | Change |
|---|---|---|
| 2026-10-13 | Restructure into rule.md / reference / scripts | Moved mandatory requirements from `SKILL.md` to `rule.md` with IDs; `VLSIT_RTL_Design_Rule.md` kept in `reference/` and made normative by V2S-010 |
| 2026-10-16 | User asked for the standard structure (SKILL.md workflow, rule.md with non-duplicating IDs, reference, Python scripts with a minimal library set, installation proposal when Python is missing) | The rule file was audited for duplicate IDs and undefined references (0 found); added the Python prerequisite rule (V2S-096) and the stdlib-only script convention; Python installed with the user approval (3.12.10) and every script tested on real input; status columns updated |
| 2026-10-17 | User asked that every skill analyze Excel files with one shared script | Copied `vlsit_analyze_excel.py` into `scripts/`; added rule V2S-097 (use it for all Excel/CSV input, `openpyxl` exemption, propose script updates on problems); SKILL.md and scripts index updated |
