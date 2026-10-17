# Scripts index

Python 3, standard library only (exception: `analyze_excel.py` needs `openpyxl`). Check `python --version` first; if Python is missing, propose the installation to the user and wait for approval.

Register every script here (rule RSC-091). Scripts must obey `rule.md` (RSC-092).

| Script | Purpose | Status |
|---|---|---|
| `rtl_change_metrics.py` | `snapshot` copies RTL files to a baseline folder before edits; `compare` computes baseline, added, deleted code lines and the change percentage (RSC-060..062). Read-only on the RTL tree. | Tested: snapshot of one file, 2 added code lines on 16 baseline lines gives 12.50% |
| `analyze_excel.py` | Read-only analyzer for .xlsx/.xlsm/.xltx/.xltm/.xls/.xlsb/.csv: sheet summary, `--range`, `--search`, `--cells` dump, JSON output (RSC-097). Needs `openpyxl`. Master copy: `C:\HQuan\002_FTEL\002_FTEL_FU3\003_Architecture\analyze_excel.py`. | Tested: openpyxl 3.x installed; workbook summary of FTEL_FU3_Common_Spec_v2.1.xlsx (13 sheets) OK |

## Adding a script

Create it when a deterministic step recurs (RSC-090). Include a header docstring, English messages, no RTL edits before approval, and no writes outside approved paths. Test on a real input, then add a row above.
