# Scripts index

Python 3, standard library only (exception: `vlsit_analyze_excel.py` needs `openpyxl`). Before running a helper, locate Python with `vlsit_find_python.ps1` (Windows) or `vlsit_find_python.sh` (Linux/macOS); use its printed path. If absent, ask before installation.

Register every script here (rule V2S-091). Scripts must obey `rule.md` (V2S-092).

| Script | Purpose | Status |
| `vlsit_find_python.ps1`, `vlsit_find_python.sh` | Locate working Python 3 on Windows or Linux/macOS and print its executable path. | Available; not re-tested in this review |
|---|---|---|
| `vlsit_create_rule_matrix.py` | Create an unassessed evidence matrix (`rule_compliance.json`) from `reference/VLSIT_RTL_Design_Rule.md` and record its SHA-256. A document inventory, not a compliance checker. | Tested: 159 NOT_RUN entries created from the bundled rule, SHA-256 recorded |
| `vlsit_analyze_excel.py` | Read-only analyzer for .xlsx/.xlsm/.xltx/.xltm/.xls/.xlsb/.csv: sheet summary, `--range`, `--search`, `--cells` dump, JSON output (V2S-097). Needs `openpyxl`. Maintained in this skill folder; keep the Codex and Claude copies synchronized. | Tested: openpyxl 3.x installed; workbook summary of a representative workbook (13 sheets) OK |

## Adding a script

Create it when a deterministic step recurs (V2S-090), for example a VHDL design-unit inventory or a source-hash manifest. Include a header docstring, English messages, no overwriting of inputs, and no writes outside approved paths. Test on a real input, then add a row above.
