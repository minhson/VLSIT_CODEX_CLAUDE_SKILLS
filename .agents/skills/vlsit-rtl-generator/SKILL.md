---
name: vlsit-rtl-generator
description: Generate synthesizable SystemVerilog RTL from a design specification written in the VLSIT ASIC IP template, or modify existing RTL after the designer approves a change plan, under VLSIT_RTL_Design_Rule.md, then verify it with a rule checker and lint. Use when the user asks to write, generate, create or fix RTL from a specification, or to bring RTL into line with the VLSIT RTL rules.
compatibility: Python 3.8 or later using the standard library only, on Windows or Linux, offline. Windows PowerShell 5.1 (Windows) or POSIX sh (Linux, macOS) is used only to locate or install Python. Lint needs Verilator or slang, found in PATH or in an OSS CAD Suite folder; without one the skill still runs the rule check and reports that lint was not run. Nothing is installed without the user's agreement.
---

# VLSIT RTL generator

This skill writes synthesizable SystemVerilog design RTL from a specification that follows the VLSIT ASIC IP specification template, or changes existing RTL after the designer approves a plan. Every file follows the VLSIT RTL design rules, and the result is checked by a rule-check script and by lint. It does not write testbenches, assertions or other verification code, and it never decides an open point of the specification by itself: it asks the designer.

Reply to the user in the language they use.

If instructions differ, follow them in this order: [rule.md](rule.md) first, then this file, then the files in `reference/`.

## Workflow

### 1. Read the rules

Read [rule.md](rule.md) completely before doing anything else. Every rule in it is mandatory, and step 9 checks the result against them by ID.

### 2. Find Python

Every script in `scripts/` is Python 3 and uses only the standard library. Locate a working Python before running any of them.

Windows:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File "<skill folder>\scripts\vlsit_find_python.ps1"
```

Linux and macOS:

```sh
sh "<skill folder>/scripts/vlsit_find_python.sh"
```

It prints the full path of a working Python 3 (called `<python>` below) and exits 0, or prints `NOT FOUND` and exits 3. Do not continue without Python and do not guess a path. Tell the user that Python 3 is needed and let them choose: install it themselves, or let you install it with `vlsit_find_python.ps1 -Install` (winget) or `vlsit_find_python.sh --install` (the system package manager). Run the install only after they agree, then run the locator again. `vlsit_find_python.sh --options` prints the install command for each Linux family.

### 3. Collect the inputs

Decide the mode from the request, and ask once for everything that is missing:

- **Generate** new RTL: the specification file (it must follow the specification template), the rule file path (see R-003), the output folder, the project name and the user name for the file headers (R-007).
- **Modify** existing RTL: the RTL folder, the request or the new specification, the old specification if there is one, the rule file path, the output folder and the same header values. Read [reference/vlsit_modify_existing_rtl.md](reference/vlsit_modify_existing_rtl.md) and continue at step 4b.

Read the rule file now (R-003). If the request is unclear about which mode applies, ask.

### 4a. Scan the specification and ask (generate mode)

```powershell
<python> "<skill folder>\scripts\vlsit_spec_gaps.py" gaps "<spec.md>"
```

It lists the unresolved items as numbered gaps and exits 2 when a BLOCK gap exists. Show the BLOCK gaps to the designer and ask about each one that changes behavior, with the question format of [reference/vlsit_question_format.md](reference/vlsit_question_format.md) (R-005, R-006). Do not write RTL for an item that is still open. Repeat the scan after the answers until no BLOCK gap is left or the designer has declared the item not applicable. Use `vlsit_spec_gaps.py facts` to print the port, parameter, clock, reset and hierarchy tables when you need them; [reference/vlsit_spec_to_rtl_map.md](reference/vlsit_spec_to_rtl_map.md) says which section feeds which RTL decision.

Then write the module list with its port tables in the chat and ask for a yes before you write code.

### 4b. Plan the change (modify mode)

Follow [reference/vlsit_modify_existing_rtl.md](reference/vlsit_modify_existing_rtl.md): baseline check, snapshot of the originals, a change plan, and the designer's approval before the first edit (R-008). When a sibling skill named `vlsit-rtl-spec-change-implementer` is installed, use its plan and gate.

### 5. Write the RTL

Write the modules leaf first and the top last, one module per file, into the output folder (R-009, R-018). Start each file from [reference/templates/vlsit_rtl_skeletons.md](reference/templates/vlsit_rtl_skeletons.md) and follow the rule file. After each module run the rule check and correct it before the next one:

```powershell
<python> "<skill folder>\scripts\vlsit_rtl_check.py" check "<output folder>"
```

Fix every ERROR (R-012). Keep a list of the WARN and INFO findings for the report (R-013). Do not generate testbenches or assertions (R-010).

### 6. Make the filelist and lint

```powershell
<python> "<skill folder>\scripts\vlsit_lint_rtl.py" filelist "<output folder>" --out "<output folder>\filelist.f" --top <top module>
<python> "<skill folder>\scripts\vlsit_lint_rtl.py" lint "<output folder>\filelist.f" --top <top module>
```

Fix every lint error and run lint again (R-014). When the script exits with 3 there is no lint tool: continue, mark lint as not run, give the designer the install options it printed, and install nothing unasked (R-015). Read [reference/vlsit_lint_and_install.md](reference/vlsit_lint_and_install.md) to judge the warnings.

### 7. Check the whole set

Run `vlsit_rtl_check.py check` once more on the final folder, with `--report` if the designer wants a file, and run `vlsit_rtl_check.py coverage` to list the rules that only a person can check. Go through those manual rules on the code and note the result of each one.

### 8. Record deviations

Write the reason in the module header for every deviation from a SHOULD rule (R-011).

### 9. Verify against the rules and report

Check the result against every rule ID in [rule.md](rule.md). Run the checks that name a script, and inspect the rest by hand. Report by rule ID (R-016): rules failed, justified, clean by script, covered by lint, inspected by hand, and what was not run, with the commands the designer can repeat. Say plainly if lint did not run (R-001, R-015).

## Reference

Read a file only when the step needs it.

| File | Read it when |
|---|---|
| [reference/vlsit_spec_to_rtl_map.md](reference/vlsit_spec_to_rtl_map.md) | Step 4a: which specification section decides which part of the RTL, and typical gaps |
| [reference/vlsit_question_format.md](reference/vlsit_question_format.md) | Step 4a: wording of a question with options and examples |
| [reference/vlsit_modify_existing_rtl.md](reference/vlsit_modify_existing_rtl.md) | Step 3 and 4b: the mode and the procedure for existing RTL |
| [reference/templates/vlsit_rtl_skeletons.md](reference/templates/vlsit_rtl_skeletons.md) | Step 5: header, leaf module, FSM and top skeletons |
| [reference/vlsit_lint_and_install.md](reference/vlsit_lint_and_install.md) | Step 6: running lint, reading warnings, install options |

## Scripts

Run each script as `<python> "<skill folder>/scripts/<script>.py" <action>` (use `\` in the path on Windows). The Python scripts run the same way on Windows and Linux.

| Script | Run it when |
|---|---|
| `scripts/vlsit_find_python.ps1` (Windows) and `scripts/vlsit_find_python.sh` (Linux, macOS) | Step 2, and again after Python was installed |
| `scripts/vlsit_spec_gaps.py` (`gaps`, `facts`) | Step 4a: find what the specification leaves open, print its tables |
| `scripts/vlsit_rtl_check.py` (`check`, `coverage`) | Steps 5, 7: check the mechanical rules; list what stays manual |
| `scripts/vlsit_lint_rtl.py` (`tools`, `filelist`, `lint`) | Step 6: find lint tools, write `filelist.f`, run lint |

Exit codes: `vlsit_spec_gaps.py` 0 no BLOCK gap, 2 gaps; `vlsit_rtl_check.py` 0 pass, 1 errors, 2 bad input; `vlsit_lint_rtl.py` 0 pass, 1 lint errors, 2 bad input, 3 no lint tool.

## Output

All deliverables are saved in the output folder the user names (R-018): the `.sv` files, `filelist.f`, the lint logs, and the rule-check report if one was asked for. The final message gives the folder, the file list, the top module, the rule-ID report and the commands that reproduce the checks.
