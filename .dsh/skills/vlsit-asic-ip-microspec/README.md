# vlsit-asic-ip-microspec

Discusses and writes an ASIC IP micro-architecture specification in the VLSIT template. The editable source is Markdown with TeX math and relative figure links; `vlsit_spec_export.py` uses Pandoc to create optional DOCX and PDF copies. PDF output requires a Pandoc PDF engine (Typst by default). The workflow asks questions with options and examples, grounds protocol statements in converted standards, studies evidence-backed reference IP, plans registers and fills the CSR workbook, draws a VLSIT-library draw.io block diagram, describes every port, and produces user-confirmed waveforms and the mandatory programming/use flow in section 11.2. A worked APB-to-TL-UL bridge is in `example/apb_tlul_bridge/`.

The spec format files are bundled in `reference/templates/` (specification template, CSR workbook, RTL rules, original README) and the draw.io library with the reference diagram in `reference/drawio/`.

Requirements: Python 3. `openpyxl` and `PyMuPDF` (AGPL-3.0, used only by the PDF input/render scripts) are optional. Pandoc is required for DOCX export; Pandoc plus Typst (recommended) or another installed PDF engine is required for PDF export. Install optional tools or packages only after approval. LaTeX is used only by the optional TikZ diagram fallback; draw.io is the default. Standards with a redistribution-forbidden licence are kept only as Markdown and must stay out of version control.

Các file format spec nằm trong `reference/templates/` và thư viện draw.io cùng sơ đồ tham chiếu nằm trong `reference/drawio/`.

Đặc tả vi kiến trúc ASIC IP theo template VLSIT. Nguồn chính là Markdown, công thức dùng TeX; Pandoc xuất thêm DOCX và PDF khi được chọn (PDF cần Typst hoặc PDF engine khác). Skill hỗ trợ hỏi đáp có phương án và ví dụ, tra cứu protocol, CSR workbook, sơ đồ draw.io, bảng port, waveform và flow sử dụng bắt buộc ở mục 11.2. Ví dụ nằm trong `example/apb_tlul_bridge/`. Tài liệu chuẩn không cho phép phân phối chỉ được giữ dưới dạng Markdown và không được commit.

Claude Code: `/vlsit-asic-ip-microspec`; Codex: `$vlsit-asic-ip-microspec`; DeepSeek Harness: `/vlsit-asic-ip-microspec`; or describe the task naturally. / Claude Code: `/vlsit-asic-ip-microspec`; Codex: `$vlsit-asic-ip-microspec`; DeepSeek Harness: `/vlsit-asic-ip-microspec`; hoặc mô tả trực tiếp yêu cầu.
