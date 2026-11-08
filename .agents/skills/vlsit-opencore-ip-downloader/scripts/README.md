# Scripts index

Python 3, standard library only (exception: `vlsit_analyze_excel.py` needs `openpyxl`). Before running a helper, locate Python with `vlsit_find_python.ps1` (Windows) or `vlsit_find_python.sh` (Linux/macOS); use its printed path. If absent, ask before installation.

Register every script here (rule OCI-091). Scripts must obey `rule.md` (OCI-092).

| Script | Purpose | Status |
| `vlsit_find_python.ps1`, `vlsit_find_python.sh` | Locate working Python 3 on Windows or Linux/macOS and print its executable path. | Available; not re-tested in this review |
|---|---|---|
| `vlsit_verify_archive.py` | Pre-extraction check of a zip/tar archive: integrity, unsafe paths, link escape, license/README presence, SHA-256. Read-only. | Tested: a valid zip passes (SHA-256, license and README detected); a zip with a `../` member is reported (exit 1) |
| `vlsit_analyze_excel.py` | Read-only analyzer for .xlsx/.xlsm/.xltx/.xltm/.xls/.xlsb/.csv: sheet summary, `--range`, `--search`, `--cells` dump, JSON output (OCI-097). Needs `openpyxl`. Maintained in this skill folder; keep the Codex and Claude copies synchronized. | Tested: openpyxl 3.x installed; workbook summary of a representative workbook (13 sheets) OK |
| `vlsit_ip_search.py` | Searches GitHub and Gitee, reads each README and scores evidence of tapeout, FPGA validation, verification and licence (QUALIFIED or EXCLUDED); `evaluate URL` scores any page including Chinese pages. Read only, nothing is downloaded (OCI-025). Standard library only; needs network access. | Tested: GitHub search `tilelink apb` returned 3 candidates, 0 qualified; Gitee API returned 0 results for one query |
| `vlsit_fetch_ip.py` | Fetches an OpenCores project from the anonymous SVN HTTP view (the OpenCores download button needs a login) or a GitHub repository at one commit, extracts safely, writes DOWNLOAD_INFO.md; `oc-info` and `gh-info` print license, status and size. GET requests only to opencores.org and github hosts. | Tested: 11 GitHub projects (including OpenTitan 14k files and Caliptra) and 6 OpenCores projects downloaded and extracted; OpenCores server errors needed retries and one project (mod_sim_exp) failed 3 times |

## Adding a script

Create it when a deterministic step recurs (OCI-090). Include a header docstring, English messages, and no writes outside approved paths. Test on a real input, then add a row above.
