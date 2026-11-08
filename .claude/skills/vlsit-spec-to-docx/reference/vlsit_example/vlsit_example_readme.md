# Worked example: APB4 to TL-UL bridge

This folder is one complete run of the skill, kept as the reference for what a good result looks
like. It was produced on 2026-11-07 from the specification of `common_rtl/007_APB2TLUL_Bridge`.

| File | What it is |
|---|---|
| `vlsit_example_spec.md` | the input, the 741-line specification in the 22-section VLSIT template |
| `vlsit_example_content.json` | the intermediate that the run wrote and validated (39 section entries, 4 functions, 2 interfaces, 11 table fills, 1 figure) |
| `vlsit_example_output.docx` | the output, the filled template: 17 headings, 58 tables, 187 KB |
| `vlsit_example_run_report.md` | the run report: gaps, answers, checks, open items |

## What to look at first

1. `vlsit_example_output.docx`, section 1: prose written for a reader, not a table dump.
2. Section 4: four functions, each with purpose, trigger, inputs, cycle behaviour and a worked
   numeric example.
3. Sections 6, 7 and 13: the three confirmed `N/A` statements, each one paragraph starting
   `Not applicable.`
4. Section 9: the SDC tables state the owner of each constraint and invent no numeric value.
5. Appendix tables: Table 2 (parameters), Table 10 twice (APB and TL-UL signals), Table 26 to 28
   (constraints), Table 44 (acronyms).

## Known limits of this example

- The four function subsections carry no waveform figure: the source folder holds only one raster
  image (the block diagram) and the nine waveforms are SVG, which the fill step cannot insert.
  Step 9b of the skill exists to draw one when the user asks.
- The run was verified structurally only; no page was rendered, because LibreOffice was not
  installed on that machine.
- `vlsit_example_content.json` keeps the figure path `figures_out/block_diagram_diagram.png`
  relative to the original run folder. When reproducing the run elsewhere, prepare the figure
  again and update that path.

## Reproducing it

```powershell
<python> "<skill folder>\scripts\vlsit_template_probe.py" "<skill folder>\reference\vlsit_spec_template.docx" --out template_map.json
<python> "<skill folder>\scripts\vlsit_spec_scan.py" "vlsit_example_spec.md" --folder <input folder> --out gaps.json
<python> "<skill folder>\scripts\vlsit_content_check.py" "vlsit_example_content.json" --template-map template_map.json
<python> "<skill folder>\scripts\vlsit_docx_fill.py" --template "<skill folder>\reference\vlsit_spec_template.docx" --content "vlsit_example_content.json" --out "example_copy.docx"
<python> "<skill folder>\scripts\vlsit_docx_check.py" "example_copy.docx" --template-map template_map.json
```

The content file references one image; the fill step reports it as missing until the figure is
prepared, and every other section fills exactly as in the delivered document.
