# VLSIT skills for Claude Code, Codex, and DeepSeek Harness / Bộ skill VLSIT cho Claude Code, Codex và DeepSeek Harness

**EN:** Nine ready-to-use skills for ASIC/RTL work: write and convert design specifications, generate and check RTL, add approved RTL features, write a testbench with protocol assertions, draw diagrams and waveforms, convert VHDL, and find open-source IP. Every skill exists in three synchronized trees: `.claude/skills/` (Claude Code), `.agents/skills/` (Codex), and `.dsh/skills/` (DeepSeek Harness).

**VI:** Chín skill dùng ngay cho công việc ASIC/RTL: viết và chuyển đổi đặc tả thiết kế, sinh và kiểm RTL, thêm tính năng RTL đã duyệt, viết testbench có assertion giao thức, vẽ sơ đồ và waveform, chuyển VHDL, tìm IP mã nguồn mở. Mỗi skill có ba bản đồng bộ: `.claude/skills/` (Claude Code), `.agents/skills/` (Codex) và `.dsh/skills/` (DeepSeek Harness).

**EN:** The `.claude/skills/`, `.agents/skills/`, and `.dsh/skills/` trees contain the same skill files. The DeepSeek Harness path follows this repository’s harness setup.

**VI:** Ba cây `.claude/skills/`, `.agents/skills/` và `.dsh/skills/` chứa cùng bộ file skill. Đường dẫn DeepSeek Harness tuân theo cấu hình harness của repository này.

---

## 1. Start in 3 steps / Bắt đầu trong 3 bước

| Step | Do this / Làm | Note / Ghi chú |
|---|---|---|
| 1 | Clone the repository and open the folder as the workspace in **Claude Code**, **Codex**, or **DeepSeek Harness**. / Clone repository rồi mở thư mục làm workspace trong **Claude Code**, **Codex** hoặc **DeepSeek Harness**. | The tool finds the skills by itself. / Công cụ tự nhận skill. |
| 2 | Check Python 3: `python --version` (Windows install: `winget install Python.Python.3.12`). / Kiểm tra Python 3. | Most core scripts use the standard library; feature-specific packages are listed under Tools and installed only after approval. / Script chính dùng thư viện chuẩn; công cụ và gói tùy chọn chỉ cài khi được đồng ý. |
| 3 | Call a skill: Claude Code `/vlsit-rtl-generator`, Codex `$vlsit-rtl-generator`, DeepSeek Harness `/vlsit-rtl-generator`, or just describe the job. / Gọi skill hoặc mô tả công việc. | `/skills` lists the loaded skills; restart the tool if a new one is missing. / `/skills` liệt kê skill đã nạp; nếu thiếu thì khởi động lại công cụ. |

Each skill asks you the questions it needs (with options and examples) and waits for your answer. Answer briefly, for example `1A 2B 3: my own idea`. / Mỗi skill tự hỏi những gì cần (có phương án và ví dụ) và chờ bạn trả lời. Trả lời ngắn, ví dụ `1A 2B 3: ý của tôi`.

## 2. Which skill for which job / Việc nào dùng skill nào

| I want to... / Tôi muốn... | Skill | Say, for example / Ví dụ câu lệnh |
|---|---|---|
| Write the design specification of an IP / Viết đặc tả thiết kế IP | `vlsit-asic-ip-microspec` | "Write the spec of an APB4 to TL-UL bridge" |
| Convert an existing Markdown spec to the VLSIT DOCX template / Chuyển spec Markdown có sẵn sang template DOCX VLSIT | `vlsit-spec-to-docx` | "Convert `<spec.md>` to the VLSIT DOCX template" |
| Generate RTL from a spec, or fix RTL under the VLSIT rules / Sinh RTL từ spec hoặc sửa RTL theo rule VLSIT | `vlsit-rtl-generator` | "Generate the RTL of this spec: `<spec.md>`" |
| Add a feature to existing RTL with an approved plan / Thêm tính năng cho RTL có sẵn, có duyệt kế hoạch | `vlsit-rtl-spec-change-implementer` | "Add `<feature>` to the RTL in `<folder>`" |
| Convert VHDL to SystemVerilog / Chuyển VHDL sang SystemVerilog | `vlsit-vhdl-to-systemverilog` | "Convert the VHDL design in `<folder>`" |
| Draw the module hierarchy as Draw.io / Vẽ sơ đồ hierarchy RTL bằng Draw.io | `vlsit-rtl-hierarchy-diagram` | "Draw the hierarchy of `<top module>`" |
| Draw a timing waveform from text, VCD or an image / Vẽ waveform | `vlsit-wavedrom-waveform` | "Draw the waveform of this VCD" |
| Find open-source IP with RTL and compare it / Tìm và so sánh IP mã nguồn mở | `vlsit-opencore-ip-downloader` | "Find a UART IP with FPGA proof" |
| Make a new skill in this house format / Tạo skill mới theo chuẩn | `vlsit-create-skill` | "Create a skill that..." |

Per-skill details: the `README.md` inside each skill folder. / Chi tiết từng skill: `README.md` trong thư mục skill.

## 3. From idea to checked RTL, step by step / Từ ý tưởng đến RTL đã kiểm, từng bước

| Step | What you do / Bạn làm | What you get / Bạn nhận |
|---|---|---|
| 1 | Run `vlsit-asic-ip-microspec` and describe the IP. Answer its questions. / Chạy skill và mô tả IP, trả lời câu hỏi. | An authoritative Markdown specification (22 sections, TeX math, numbered requirements), with optional DOCX/PDF exports, a draw.io block diagram and key waveforms. / Spec Markdown gốc (22 mục, công thức TeX, requirement đánh số), có thể xuất DOCX/PDF, kèm sơ đồ draw.io và waveform. |
| 2 | Read the spec, settle the open items (section 20). / Đọc spec, chốt các mục còn mở (mục 20). | A spec without open points. / Spec không còn điểm mở. |
| 3 | Run `vlsit-rtl-generator` with the spec file, the project and author name, and the output folder. / Chạy skill với file spec, tên project, tên tác giả, thư mục output. | `.sv` files, `filelist.f`, rule-check report and lint logs, reported by rule ID. / File `.sv`, `filelist.f`, báo cáo rule và log lint theo ID rule. |
| 4 | Ask for a testbench: "write a testbench with protocol assertions". / Yêu cầu testbench có assertion giao thức. | A self-checking testbench with 20+ assertions per protocol, derived from the spec and the standards, never from the RTL. / Testbench tự kiểm có từ 20 assertion mỗi giao thức, suy ra từ spec và chuẩn, không từ RTL. |
| 5 | If a check fails and the cause is unclear, the skill shows you the spec, the RTL and the test side by side; you decide. / Nếu có FAIL chưa rõ nguyên nhân, skill đưa spec, RTL, test để bạn quyết định. | A decision, then exactly that change. / Quyết định của bạn, rồi đúng thay đổi đó. |

For a new design, follow the five-step flow below. When an existing Markdown specification must be mapped into the VLSIT DOCX template, run `vlsit-spec-to-docx` after the source specification is ready and review its gap list before document generation. / Với thiết kế mới, thực hiện quy trình năm bước bên dưới. Nếu cần ánh xạ đặc tả Markdown có sẵn vào template DOCX VLSIT, chạy `vlsit-spec-to-docx` sau khi có đặc tả nguồn và xem lại danh sách thiếu trước khi tạo tài liệu.

A finished example of all five steps (APB4 to TL-UL bridge): [example/apb_tlul_bridge](example/apb_tlul_bridge) — spec, figures, `rtl/`, `verification/`, `sanity/` (logs and reports) and the design log [apb_tlul_bridge_design_process_log.md](example/apb_tlul_bridge/apb_tlul_bridge_design_process_log.md). To rerun its checks:

Ví dụ hoàn chỉnh cả năm bước (cầu APB4 sang TL-UL) nằm ở [example/apb_tlul_bridge](example/apb_tlul_bridge). Chạy lại các kiểm tra của ví dụ:

```sh
cd example/apb_tlul_bridge
make all          # rule check + lint + simulation (default and narrow parameters)
```

The Makefile header lists the tools it needs (GNU make, Icarus Verilog, Verilator and/or slang, Python 3; the [OSS CAD Suite](https://github.com/YosysHQ/oss-cad-suite-build) has all of them) and the Windows and Linux options. / Phần đầu Makefile ghi các công cụ cần có và cách dùng trên Windows, Linux.

## 4. Tools / Công cụ

| Need / Cần | For / Dùng cho | Required? / Bắt buộc? |
|---|---|---|
| Python 3 | all skill scripts / mọi script của skill | Yes / Có |
| Verilator or slang | RTL lint (without it the skill says "lint not run") / lint RTL | No / Không |
| Icarus Verilog + GNU make | simulation of the example / mô phỏng ví dụ | No / Không |
| `openpyxl`, `PyMuPDF` | CSR workbook, PDF input conversion and PDF rendering / workbook CSR, chuyển PDF đầu vào và kết xuất PDF | Only for that feature; asked first / Chỉ khi cần tính năng đó; hỏi trước |
| `python-docx`, `lxml` | Fill the VLSIT DOCX specification template / Điền template đặc tả DOCX VLSIT | Required by `vlsit-spec-to-docx`; install only after explicit approval / Skill chỉ cài sau khi được đồng ý rõ ràng |
| `Pillow`, `PyMuPDF`, LibreOffice | Optional figure cropping, page images and DOCX layout rendering / Cắt hình, xuất ảnh trang và render bố cục DOCX | Only for those steps; asked first / Chỉ khi cần bước đó; hỏi trước |
| Pandoc | Export Markdown specifications to DOCX / Xuất spec Markdown sang DOCX | Optional; asked first / Tùy chọn; hỏi trước |
| Typst (recommended) or another Pandoc PDF engine | Export Markdown specifications to PDF / Xuất spec Markdown sang PDF | Optional; asked first / Tùy chọn; hỏi trước |
| `tectonic` or another LaTeX engine | Optional TikZ block-diagram fallback / Phương án dự phòng cho sơ đồ TikZ | Only if needed; asked first / Chỉ khi cần; hỏi trước |

Standards under copyright (for example the Arm APB specification) are not shipped. The specification skill names the file, the source and the licence and asks your approval before it downloads one. / Tiêu chuẩn có bản quyền (ví dụ đặc tả APB của Arm) không đi kèm. Skill đặc tả báo tên file, nguồn, giấy phép và xin phép trước khi tải.

## 5. Use the skills in another project or machine / Dùng skill ở project hoặc máy khác

Copy the **whole** skill folder (keep `SKILL.md` where it is). / Chép **toàn bộ** thư mục skill, giữ nguyên vị trí `SKILL.md`.

| Where / Đâu | Claude Code | Codex | DeepSeek Harness |
|---|---|---|---|
| One project / Một project | `<project>/.claude/skills/<skill>/` | `<project>/.agents/skills/<skill>/` | `<project>/.dsh/skills/<skill>/` |
| Your account / Tài khoản cá nhân | `~/.claude/skills/<skill>/` | `~/.agents/skills/<skill>/` (some installs: `~/.codex/skills/<skill>/`) | `~/.dsh/skills/<skill>/` |

```sh
# Claude Code, one skill for all your projects (Linux/macOS/Git Bash)
cp -r .claude/skills/vlsit-rtl-generator ~/.claude/skills/
```

```powershell
# Claude Code, one skill for all your projects (PowerShell)
Copy-Item -Recurse .claude\skills\vlsit-rtl-generator "$HOME\.claude\skills\"
```

```powershell
# DeepSeek Harness, one skill for all your projects (PowerShell)
Copy-Item -Recurse .dsh\skills\vlsit-rtl-generator "$HOME\.dsh\skills\"
```

Other ways: `claude --add-dir <this repository>` loads Claude skills for one session; Codex can install from GitHub with `$skill-installer` (give the owner/repository and `.agents/skills/<skill>`). DeepSeek Harness discovers the project copy in `.dsh/skills/`. If a destination exists, compare it before replacing. / Cách khác: `claude --add-dir <repository>` nạp skill cho một phiên Claude; Codex cài từ GitHub bằng `$skill-installer` và đường dẫn `.agents/skills/<skill>`. DeepSeek Harness tự tìm bản project trong `.dsh/skills/`. Nếu thư mục đích đã có, hãy so sánh trước khi ghi đè.

## 6. How the skills are built / Cấu trúc skill

| Path / Đường dẫn | Role / Vai trò |
|---|---|
| `SKILL.md` | The workflow; always reads `rule.md` first. / Quy trình; luôn đọc `rule.md` trước. |
| `rule.md` | Numbered mandatory rules; highest priority. / Rule bắt buộc có ID; ưu tiên cao nhất. |
| `reference/` | Guides, templates, examples (for RTL: `reference/rtl_example/`). / Hướng dẫn, mẫu, ví dụ. |
| `scripts/` | Python 3 helpers (and a `.ps1`/`.sh` pair to locate Python). / Script Python 3 và cặp `.ps1`/`.sh` tìm Python. |
| `.claude/skills/`, `.agents/skills/`, `.dsh/skills/` | Three synchronized discovery trees for Claude Code, Codex, and DeepSeek Harness. / Ba cây skill đồng bộ cho Claude Code, Codex và DeepSeek Harness. |

File names inside a skill start with `vlsit_` (except `SKILL.md`, `rule.md`, `README.md`, `LICENSE`, third-party files). Skill instructions are in precise English; the READMEs are bilingual. A skill changes its own `rule.md` only with your explicit approval. / Tên file trong skill bắt đầu bằng `vlsit_` (trừ `SKILL.md`, `rule.md`, `README.md`, `LICENSE`, file bên thứ ba). Hướng dẫn skill viết bằng tiếng Anh kỹ thuật; README song ngữ. Skill chỉ sửa `rule.md` của mình khi bạn đồng ý rõ ràng.

To update a skill, edit its canonical `.claude/skills/<skill>/` folder, then mirror and check it with the bundled script: / Để cập nhật skill, sửa thư mục chuẩn `.claude/skills/<skill>/`, sau đó đồng bộ và kiểm tra bằng script đi kèm:

```powershell
python .claude\skills\vlsit-create-skill\scripts\vlsit_skillkit.py mirror .claude\skills\<skill>
python .claude\skills\vlsit-create-skill\scripts\vlsit_skillkit.py mirror .claude\skills\<skill> --check
```

This writes the `.agents/skills/` and `.dsh/skills/` copies; `--check` reports drift without writing files. / Lệnh đầu cập nhật bản `.agents/skills/` và `.dsh/skills/`; `--check` chỉ báo lệch, không ghi file.

## Documentation / Tài liệu chính thức

- [Codex skills](https://developers.openai.com/codex/skills) · [Codex plugins](https://developers.openai.com/plugins/build/plugins)
- [Claude Code skills](https://code.claude.com/docs/en/skills) · [Claude Code plugins](https://code.claude.com/docs/en/plugins/overview)
