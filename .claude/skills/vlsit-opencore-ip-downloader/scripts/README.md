# Scripts index

Register every script here (rule OCI-091). Scripts must obey `rule.md` (OCI-092).

| Script | Purpose | Status |
|---|---|---|
| `verify_archive.py` | Pre-extraction check of a zip/tar archive: integrity, unsafe paths, link escape, license/README presence, SHA-256. Read-only. | Untested (no Python available when authored) |

## Adding a script

Create it when a deterministic step recurs (OCI-090). Include a header docstring, English messages, and no writes outside approved paths. Test on a real input, then add a row above.
