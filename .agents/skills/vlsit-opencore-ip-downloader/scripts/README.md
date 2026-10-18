# Scripts index

Python 3, standard library only (exception: `vlsit_analyze_excel.py` needs `openpyxl`). Check `python --version` first; if Python is missing, propose the installation to the user and wait for approval.

Register every script here (rule OCI-091). Scripts must obey `rule.md` (OCI-092).

| Script | Purpose | Status |
|---|---|---|
| `vlsit_verify_archive.py` | Pre-extraction check of a zip/tar archive: integrity, unsafe paths, link escape, license/README presence, SHA-256. Read-only. | Tested: a valid zip passes (SHA-256, license and README detected); a zip with a `../` member is reported (exit 1) |
| `vlsit_analyze_excel.py` | Read-only analyzer for .xlsx/.xlsm/.xltx/.xltm/.xls/.xlsb/.csv: sheet summary, `--range`, `--search`, `--cells` dump, JSON output (OCI-097). Needs `openpyxl`. Master copy: `C:\HQuan\002_FTEL\002_FTEL_FU3\003_Architecture\vlsit_analyze_excel.py`. | Tested: openpyxl 3.x installed; workbook summary of FTEL_FU3_Common_Spec_v2.1.xlsx (13 sheets) OK |
| `vlsit_ip_search.py` | Searches GitHub and Gitee, reads each README and scores evidence of tapeout, FPGA validation, verification and licence (QUALIFIED or EXCLUDED); `evaluate URL` scores any page including Chinese pages. Read only, nothing is downloaded (OCI-025). Standard library only; needs network access. | Tested: GitHub search `tilelink apb` returned 3 candidates, 0 qualified; Gitee API returned 0 results for one query |

## Adding a script

Create it when a deterministic step recurs (OCI-090). Include a header docstring, English messages, and no writes outside approved paths. Test on a real input, then add a row above.
