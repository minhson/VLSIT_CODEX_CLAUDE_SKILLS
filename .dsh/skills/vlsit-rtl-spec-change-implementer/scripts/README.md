# Scripts index

Python 3, standard library only (exception: `vlsit_analyze_excel.py` needs `openpyxl`). Before running a helper, locate Python with `vlsit_find_python.ps1` (Windows) or `vlsit_find_python.sh` (Linux/macOS); use its printed path. If absent, ask before installation.

Register every script here (rule RSC-091). Scripts must obey `rule.md` (RSC-092).

| Script | Purpose | Status |
| `vlsit_find_python.ps1`, `vlsit_find_python.sh` | Locate working Python 3 on Windows or Linux/macOS and print its executable path. | Available; not re-tested in this review |
|---|---|---|
| `vlsit_rtl_change_metrics.py` | `snapshot` copies RTL files to a baseline folder before edits; `compare` computes baseline, added, deleted code lines and the change percentage (RSC-060..062). Read-only on the RTL tree. | Tested: snapshot of one file, 2 added code lines on 16 baseline lines gives 12.50% |
| `vlsit_analyze_excel.py` | Read-only analyzer for .xlsx/.xlsm/.xltx/.xltm/.xls/.xlsb/.csv: sheet summary, `--range`, `--search`, `--cells` dump, JSON output (RSC-097). Needs `openpyxl`. Maintained in this skill folder; keep the Codex and Claude copies synchronized. | Tested: openpyxl 3.x installed; workbook summary of a representative workbook (13 sheets) OK |

## Adding a script

Create it when a deterministic step recurs (RSC-090). Include a header docstring, English messages, no RTL edits before approval, and no writes outside approved paths. Test on a real input, then add a row above.
