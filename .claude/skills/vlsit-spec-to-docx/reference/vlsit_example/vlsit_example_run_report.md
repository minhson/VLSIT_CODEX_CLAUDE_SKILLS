# Run report — APB2TLUL specification to DOCX

Date: 2026-11-07 · Skill: `vlsit-spec-to-docx` · Source: `common_rtl/007_APB2TLUL_Bridge/APB2TLUL_Bridge_Design_Specification.md`

## 1. Input inventory (R-001)

The input folder holds 43 files: the 741-line specification (79 KB), `figures/` with 10 SVG, 10 WaveJSON, 1 PNG and 1 TeX source, `rtl/` with three SystemVerilog modules and a file list, `verification/` with a testbench and a 36-assertion protocol checker, `sanity/` with lint and simulation logs, and `research/`.

The folder has no `.drawio` file and no raster image other than `figures/block_diagram.png`.

## 2. Template probe

`heading=73 level1=17 tables=45 figures=6`; the probe map is `template_map.json`.

## 3. Gaps and how each was answered (R-002, R-004)

| Gap | Answer | Recorded at |
|---|---|---|
| Section 9 SDC has no numeric period or boundary delay | State that the period and the delays are owned by the SoC integrator (OI-004) and that the exception inventory is empty; no numeric value invented | `_updated.md` §23.1 |
| Section 4 has no worked example | Use the worked example derived from sections 6.2, 9 and 10.2 (write 0xDEADBEEF to 0x0000_1000, aligned read, local error 4'b1011) | `_updated.md` §23.2 |
| Template section 6 CSR does not apply | N/A with the source reason | `_updated.md` §23.3 |
| Template section 7 Software Programming does not apply | N/A in full, no software-visible register | `_updated.md` §23.3 |
| Template section 13 Power does not apply | N/A with the source reason | `_updated.md` §23.3 |

The original specification file was not modified (its hash is unchanged); every addition is in
`APB2TLUL_Bridge_Design_Specification_updated.md` with the marker `[added: user, 2026-11-07]`.

## 4. Files written

| File | Content |
|---|---|
| `APB2TLUL_Bridge_Design_Specification_updated.md` | source plus section 23 (781 lines) |
| `content.json` | 39 section entries, 4 functions, 2 interfaces, 11 table fills, 1 figure |
| `figures_out/block_diagram_diagram.png` | the block diagram, diagram-only |
| `APB2TLUL_Bridge_Design_Specification.docx` | the filled document (187 KB) |
| `gaps.json`, `template_map.json` | scan and probe evidence |

## 5. Verification (R-013, R-015)

| Check | Result |
|---|---|
| `vlsit_content_check.py` | `RESULT: PASS (0 errors, 6 warnings)` — warnings are 4 functions without a figure and two references to TBD-002 |
| `vlsit_docx_check.py` | `RESULT: PASS (0 errors, 2 warnings)` — 17 sections, 58 tables, 0 placeholders, 24 guidance paragraphs left in subsections that have no content |
| Table count | 45 to 58, expected: the function subsection was cloned three times (4 tables each) and the interface subsection once (1 table) |
| Render | **Not performed.** LibreOffice is not installed on this machine and the user chose structure-only verification (F2 B). No page was inspected. |
| Content spot-check | Overview, IP Description, Features, the N/A paragraphs and the function block read correctly; the N/A paragraphs are present for sections 6, 7 and 13. |

## 6. Known limitations of this run

1. **Function figures.** The four function sections have no figure: the only raster asset in the
   folder is the block diagram, and the nine waveform figures are SVG, which python-docx cannot
   insert; no SVG-to-PNG converter (LibreOffice, ImageMagick, Inkscape, cairosvg) is available and
   the sandbox blocks the browser-based fallback. R-007 is therefore only partly met for the figure
   part; the waveform behaviour is described in prose and in the cycle table.
2. **Layout unverified.** Without a renderer, table overflow and pagination were not inspected.
3. **Tables left to the writer.** Tables 6 to 9, 11 to 25 and 29 to 43 keep their template header
   rows and no data rows, because the source does not provide a one-to-one row set for them or the
   content is carried by prose instead.
4. **Environment.** `common_rtl` is not writable in this sandbox, so all outputs live under
   `exports/007_APB2TLUL_Bridge/` instead of beside the specification.
