# Writing scripts

Guidance only; the mandatory requirements are in [rule.md](../rule.md). The starter
script is [templates/script.py.tpl](templates/script.py.tpl), created by
`skillkit.py new --with-script`, together with a copy of
[find-python.ps1](../scripts/find-python.ps1).

## What belongs in a script

A step is a script candidate when its result does not depend on judgment: scaffold a
folder, parse or validate a file, convert a format, download and verify, copy and
compare. The assistant then runs one command and reads a few lines instead of
reasoning through the step each time. Keep judgment (choosing, drafting, deciding
what the result means) in SKILL.md.

## Interface pattern

- One script per topic, with `argparse` sub-commands (`check`, `run`, ...).
- A read-only `check` action that reports `READY` or `NOT READY` plus a `missing:`
  line, so SKILL.md can branch on it.
- Output: one verdict line, then numbered problems. Summarize; do not echo whole
  files or lists. Offer `--json` only if another program consumes the output.
- Exit codes: `0` success, `1` error (message on the last line), and a distinct code
  for each outcome that SKILL.md handles differently (for example `3` prerequisite
  missing). Document them in the docstring and in SKILL.md.
- Destructive actions are opt-in: stop when the output exists, overwrite only with
  `--force`.
- Print the path of every file written.

## Python on Windows

- **Standard library only.** It covers most needs. `urllib.request` (HTTP), `json`,
  `csv`, `zipfile` and `xml.etree` (Word and Excel files are zip archives of XML),
  `hashlib`, `re`, `pathlib`, `shutil`, `subprocess`, `argparse`, `difflib`,
  `sqlite3`, `tempfile`, `datetime`. Reach for a package only when none of these can
  do the job, then ask the user, name the package and its version in
  `compatibility`, and pass `--allow-package <name>` to `validate`.
- **Explicit UTF-8.** Python on Windows opens text files in the local code page, so
  Vietnamese text is corrupted silently. Always write `open(path, encoding="utf-8")`,
  `path.read_text(encoding="utf-8")` and `path.write_text(text, encoding="utf-8")`.
  Start `main()` with `sys.stdout.reconfigure(encoding="utf-8")` so that printing
  accented text does not raise `UnicodeEncodeError` in a console or a pipe. When
  writing a file that must have no byte-order mark (SKILL.md), `encoding="utf-8"` is
  correct; `utf-8-sig` would add one.
- **Stay compatible with Python 3.8.** No `match` statements, no `X | Y` type hints,
  no `str.removeprefix`; `sys.stdlib_module_names` exists only from 3.10, so guard it
  with `getattr`.
- **Paths with `pathlib`**, and `subprocess.run([...])` with a list, never
  `shell=True` with user text inside.
- **No hidden state.** Do not write outside the folders the user named, except the
  temporary folder, and clean that up.

## Finding and installing Python

The `python` command on a Windows PATH is often the Microsoft Store shortcut, which
prints an error instead of running Python; and a python.org install is often not on
PATH. `find-python.ps1` therefore tries `py -3`, then `python` and `python3`, then the
default install folders, and accepts a candidate only if it really runs and reports
3.8 or later. It is the one non-Python script, because it must work before Python
exists, and each skill with scripts carries its own copy so the skill folder stays
self-contained. It is ASCII-only PowerShell 5.1.

When it prints `NOT FOUND`:

1. Tell the user in one or two sentences that Python 3 is needed and why.
2. Offer the two ways: they install it (python.org downloads page, or the Microsoft
   Store), or you install it with `find-python.ps1 -Install`, which runs
   `winget install --id Python.Python.3.13 --exact`. The python.org installer
   normally installs for the current user, but Windows may still ask for approval.
3. Install only after they say yes. Then run the locator again; it searches the
   default folders, so it finds the new Python even though the PATH of the running
   session has not been refreshed.
4. If winget is missing or the install fails, fall back to the first way.

## Testing

Run every script on a small sample input: once to see the output and the exit code,
and once more on the same output location to confirm that it refuses to overwrite.
Run the failure paths too (missing input, missing prerequisite) so the message is one
the assistant can act on. Run `validate` again after editing a script: it parses each
`.py` file, lists imports outside the standard library and flags text files opened
without an encoding. Record in the final report what was run and what could not be
run.

## Another runtime

Use PowerShell, Node.js or another runtime only if the user asks for it, or Python
cannot do the task. Confirm that it is installed before writing code for it, state
the requirement in `compatibility`, and keep the same interface pattern. PowerShell
files must be ASCII-only (R-025): Windows PowerShell 5.1 reads a file without a
byte-order mark in the local code page.
