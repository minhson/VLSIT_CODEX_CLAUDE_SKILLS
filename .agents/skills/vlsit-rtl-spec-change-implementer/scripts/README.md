# Scripts index

Register every script here (rule RSC-091). Scripts must obey `rule.md` (RSC-092).

| Script | Purpose | Status |
|---|---|---|
| `rtl_change_metrics.py` | `snapshot` copies RTL files to a baseline folder before edits; `compare` computes baseline, added, deleted code lines and the change percentage (RSC-060..062). Read-only on the RTL tree. | Untested (no Python available when authored) |

## Adding a script

Create it when a deterministic step recurs (RSC-090). Include a header docstring, English messages, no RTL edits before approval, and no writes outside approved paths. Test on a real input, then add a row above.
