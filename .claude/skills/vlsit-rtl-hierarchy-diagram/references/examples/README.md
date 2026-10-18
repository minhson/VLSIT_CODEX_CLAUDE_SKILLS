# Worked examples (reference only; `rule.md` takes precedence)

| File | What it is |
|---|---|
| `vlsit_can_level1_spec.json` | Spec of the CAN controller (8051 host configuration), level 1: blocks, connectors, boundary pins, clock tree, tables. Input of `scripts/vlsit_drawio_frame_diagram.py`; schema in `references/vlsit_diagram_spec.md`. |
| `vlsit_can_level1_params.txt` | Parameter sets for `scripts/vlsit_layout_search.py` (gaps, seeds, side variants). |
| `vlsit_rtl_analysis.md`, `vlsit_rtl_hierarchy.drawio` | Final report and diagram of the same CAN level-1 run (output of the spec above with the current skill: frame style, one page `01_LEVEL_1`). Format example only. |

Run from the skill folder:

    python scripts/vlsit_drawio_frame_diagram.py references/examples/vlsit_can_level1_spec.json <OUTPUT_DIR>
    python scripts/vlsit_layout_search.py references/examples/vlsit_can_level1_spec.json references/examples/vlsit_can_level1_params.txt <WORK_DIR> --top 3
