---
name: vlsit-rtl-hierarchy-diagram
description: Analyze existing Verilog or SystemVerilog RTL to trace module hierarchy, functional relationships, and protocol interfaces, then create a source-grounded multi-page draw.io diagram using only the bundled VLSIT symbol library. Use when asked to inspect or map a design from its top module to its submodules.
---

# VLSIT RTL Hierarchy Analysis and draw.io Diagram

## Operating contract

1. Read [rule.md](rule.md) completely before doing anything. Its numbered rules (RHD-xxx) are mandatory and rank above everything else.
2. Follow the workflow below. It orders the work; it never relaxes a rule.
3. Consult `references/` for the library guide, templates, and examples. They rank below `rule.md`.
4. Run helpers from `scripts/` (index: [scripts/README.md](scripts/README.md)) instead of repeating manual steps.
5. Apply the self-improvement rules RHD-090..096 at the end of every run.

## Workflow (strictly in this order, RHD-070)

1. **Input (RHD-010..013).** Obtain the explicit RTL directory and the diagram level N (0 = TOP only, 1 = TOP plus one level, ...); ask for both in one message if absent.
2. **Hierarchy analysis (RHD-030..033, 036, 037).** Files, top, instances by depth down to level N, parameters, generate scope; blocks at level N with children are marked `(not expanded)`.
3. **Module function analysis (RHD-034, 071, 080..083).** Main function of each block; for modules with own logic (assign/always/always_ff/always_comb), partition into at most 10 functional groups.
4. **Signal and interface analysis (RHD-035, 072, 073).** Every inter-block signal: meaning, direction, width, level/pulse, type; interface category: standard protocol, handshake, or custom.
5. **Signal grouping (RHD-074, 059, 078).** One group per interface using names from [references/interface_groups.md](references/interface_groups.md), remaining signals grouped by function; flag groups not in the catalog as `(proposed group)`.
6. **Analysis report (RHD-075..077).** Write everything into one `rtl_analysis.md` using [references/analysis_template.md](references/analysis_template.md).
7. **Draw (RHD-020..025, 040..049, 050..059, 079, 084..089; mnemonic labels plus Interface Table; parent as enclosing frame with children packed in 2D, no hierarchy arrows; size shapes per [references/sizing_guide.md](references/sizing_guide.md)).** Read [references/library_usage.md](references/library_usage.md); place blocks first, then add signal-group connectors with interface names. Arrows point from the active (initiating) side (RHD-049); connectors never cross blocks (RHD-056); crossing connectors use `jumpStyle=arc` (RHD-057).
8. **Validate and report (RHD-060..063).** Run `python scripts/library_symbols.py validate --diagram rtl_hierarchy.drawio`, check well-formedness, render a preview if possible.
9. **Improve (RHD-078, 090..096).** Ask the user about any proposed groups; Add scripts (for example an instance-tree or signal-table extractor once the manual step recurs), log changes in `references/improvement_log.md`, and propose rule changes to the user.

## Folder map

| Path | Role | Priority |
|---|---|---|
| `rule.md` | Numbered mandatory rules | 1 (highest) |
| `SKILL.md` | Workflow and routing | 2 |
| `references/` | `library_usage.md`, `analysis_template.md`, `sizing_guide.md`, `interface_groups.md`, `examples/`, improvement log | 3 |
| `assets/` | Bundled symbol library (immutable) | data |
| `scripts/` | `library_symbols.py` and model-added helpers | tool |
