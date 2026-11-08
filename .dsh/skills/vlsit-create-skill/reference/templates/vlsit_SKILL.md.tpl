---
name: {{NAME}}
description: {{DESCRIPTION}}
{{#SCRIPTS}}
compatibility: Python 3.8 or later using the standard library only, on Windows or Linux. Windows PowerShell 5.1 (Windows) or POSIX sh (Linux, macOS) is used only to locate or install Python. TODO(fill) - add network access or other needs, or delete this sentence.
{{/SCRIPTS}}
---

# {{TITLE}}

TODO(fill): two or three sentences - what this skill does and what it deliberately does not do.

Reply to the user in the language they use.

If instructions differ, follow them in this order: [rule.md](rule.md) first, then this file, then the files in `reference/`.

## Workflow

### 1. Read the rules

Read [rule.md](rule.md) completely before doing anything else. Every rule in it is mandatory.

{{#SCRIPTS}}
### 2. Find Python

Every script in `scripts/` is Python 3 and uses only the standard library. Locate a working Python before running any of them:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File "<skill folder>\scripts\vlsit_find_python.ps1"
```

```sh
sh "<skill folder>/scripts/vlsit_find_python.sh"
```

The first line is for Windows, the second for Linux and macOS. The locator prints the full path of a working Python 3 (called `<python>` below) and exits 0, or prints `NOT FOUND` and exits 3. Do not continue without Python and do not guess a path. Tell the user that Python 3 is needed and let them choose: install it themselves (python.org, or `vlsit_find_python.sh --options` for the command of each Linux family), or let you install it with `vlsit_find_python.ps1 -Install` (uses winget) or `vlsit_find_python.sh --install` (uses the system package manager). Run the install only after they agree, then run the locator again.

{{/SCRIPTS}}
### 2. TODO(fill): first working step

TODO(fill): what to do, in order. Ask the user for any required input that is missing instead of guessing it. Explain why a step matters when the reason is not obvious.

### 3. Verify against the rules

Check the result against every rule ID in [rule.md](rule.md). Run the checks that name a script, and inspect the rest by hand. Report which rules were verified and how, and say plainly what could not be verified.

## Reference

Read a file only when the step needs it.

| File | Read it when |
|---|---|
| TODO(fill) | TODO(fill) |

## Scripts

{{#SCRIPTS}}
Run each script as `<python> "<skill folder>/scripts/<script>.py" <action>` (use `\` in the path on Windows). A Python script runs the same way on both systems; a script in any other language needs a twin for the other system.

| Script | Run it when |
|---|---|
| `scripts/vlsit_find_python.ps1` (Windows) and `scripts/vlsit_find_python.sh` (Linux, macOS) | Before the first Python script, and again after Python was installed |
| `scripts/{{SCRIPT}}` | TODO(fill) |
{{/SCRIPTS}}
{{#NOSCRIPTS}}
TODO(fill): list each script in `scripts/` and when to run it, or delete this section if the skill needs none. Write scripts in Python, and add the "Find Python" step from the house template when you add the first one.
{{/NOSCRIPTS}}

## Output

TODO(fill): where results are saved, how files are named, and what to report back to the user.
