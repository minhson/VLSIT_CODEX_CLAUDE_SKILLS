# Scripts index

Register every script here (rule RHD-091). Scripts must obey `rule.md` (RHD-092).

| Script | Purpose | Status |
|---|---|---|
| `library_symbols.py` | Parse the bundled VLSIT library and validate a generated `.drawio` for symbol provenance, shapes, groups, and styling. Does not prove RTL correctness or visual quality. Allows `jumpStyle`/`jumpSize` edits (RHD-057) and skips native table cells tagged `vlsit_native_table="1"` (RHD-023). | Pre-existing; jump-style and native-table edits untested (no Python) |

## Adding a script

Create it when a deterministic step recurs (RHD-090), for example an instance-tree extractor. Include a header docstring, English messages, no RTL modification, and no writes outside approved paths. Test on a real input, then add a row above.
