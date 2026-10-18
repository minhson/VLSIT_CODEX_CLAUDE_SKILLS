# Rules

These rules are mandatory every time this skill runs. When this file, SKILL.md and a file in `reference/` differ, this file wins.

Each rule is one checkable requirement. It has a permanent ID (R-NNN) that is never reused or renumbered, a statement that starts with MUST or MUST NOT, a Why line and a Check line. No two rules may repeat or contradict each other.

"The rule file" below means `VLSIT_RTL_Design_Rule.md` (version v2). "The specification template" means `VLSIT_ASIC_IP_Design_Specification_Template.md`. "The output folder" is the folder the user names for the deliverables.

## General

### R-001 Report only verified results
MUST report a result as checked, tested or installed only when a command or an inspection in the current run confirmed it, and list everything that was not confirmed.
- Why: the designer acts on the report, and an unverified claim costs more than an honest "not checked".
- Check: manual - every claim in the final report points to a command output or to a file that was read.

### R-002 Protect existing files
MUST ask the user before overwriting or deleting a file that this skill did not create in the current run.
- Why: the user may have edited the file by hand, and a silent overwrite destroys that work.
- Check: manual - no existing file changed without a recorded yes from the user.

## Inputs and questions

### R-003 Rule file first
MUST read the rule file in full before writing or changing any RTL line, taking it from the path the user names or from `spec_template/VLSIT_RTL_Design_Rule.md` of the working tree, and ask for the path when neither exists.
- Why: naming, structure and the list of prohibited constructs come from that document, and a guess about them forces rework of every file.
- Check: manual - the report names the rule file path and its version.

### R-004 Scan the specification
MUST run `vlsit_spec_gaps.py gaps` on the specification before writing RTL from it, and show the designer the BLOCK gaps it reports.
- Why: the scan finds unresolved placeholders, open decisions and inconsistent sections in seconds, which a read-through misses.
- Check: manual - the gap list is in the run before the first RTL file.

### R-005 Ask, do not invent
MUST stop and ask the designer about every BLOCK gap and every ambiguity that changes RTL behavior, instead of choosing a value for it.
- Why: an invented port, reset value or latency becomes a silent defect in a design that is reused and taped out.
- Check: manual - every behavior in the RTL traces to the specification or to a recorded answer of the designer.

### R-006 Question format
MUST write each question to the designer with at least two options, each explained with a concrete example, at most one marked as recommended with its reason, and a last open choice for the designer's own idea.
- Why: the designer knows the product context, and a bare question or a single proposal hides the trade-offs that decide the answer.
- Check: manual - each question in the chat shows the options, their examples and the open choice.

### R-007 Header data from the designer
MUST take the project name and the user name for the file header from the designer instead of inventing them.
- Why: the header names the human author and the project, and a made-up value would be false documentation in every file.
- Check: manual - the Project and Author lines of the headers match the designer's answer.

## Writing and changing RTL

### R-008 Approved change plan
MUST present a change plan for existing RTL, with files, exact edits, reasons and expected effect on behavior, and edit only after the designer approves it.
- Why: a small edit in working RTL can change behavior elsewhere, and the designer must see the scope before it happens.
- Check: manual - an approval message follows the plan and precedes the first edit; the edits match the plan.

### R-009 Originals untouched
MUST write modified and generated RTL as new files in the output folder and leave the original RTL files unchanged.
- Why: the original is the baseline for comparison and for undoing the change.
- Check: manual - the original files have the same content as before the run.

### R-010 Design RTL only
MUST NOT generate testbenches, SVA or any other verification code, nor apply the design rules to such code.
- Why: the rule file covers synthesizable RTL only, and verification belongs to a separate source set.
- Check: vlsit_rtl_check.py reports no P14 or P19 finding; manual - the output folder holds design files only.

### R-011 Deviations recorded
MUST write a reason in the module header for every deviation from a SHOULD rule of the rule file.
- Why: the rule file allows a deviation only when its reason is written down for the reviewer.
- Check: manual - each deviation named in the report has its reason in the header of the file.

## Verification

### R-012 Rule check
MUST deliver only `.sv` files for which `vlsit_rtl_check.py check` prints RESULT: PASS.
- Why: the script decides the mechanical rules the same way every time, so the designer reviews meaning instead of spelling.
- Check: the last run of the script on the delivered files prints RESULT: PASS.

### R-013 Findings explained
MUST give each remaining WARN or INFO finding of the rule check and of lint either a fix or a written reason in the report.
- Why: a warning left without a decision cannot be told apart from a warning nobody read.
- Check: manual - every WARN and INFO line of the last runs appears in the report with its decision.

### R-014 Lint
MUST lint the complete delivered file set with `vlsit_lint_rtl.py lint`, correcting each lint error before delivery.
- Why: lint finds width, latch, undriven and connection problems that the rule check does not see.
- Check: the last lint run prints RESULT: PASS with 0 errors.

### R-015 No lint tool
MUST continue with the rule check, report lint as not run, and offer the designer the install options when no lint tool is found, installing nothing unasked.
- Why: the designer may not have a tool installed or may not want one installed, and delivery must not stop or hide the gap.
- Check: manual - the report says "lint not run" and lists the options; nothing was installed before a yes from the user.

### R-016 Rule-ID report
MUST end with a report by rule ID that names the rules failed, justified, clean by script, covered by lint and inspected by hand, and says what was not run.
- Why: the designer can then see exactly which rules stand behind the delivery and which do not.
- Check: manual - the report lists the manual rules from `vlsit_rtl_check.py coverage` with the result of each inspection.

## Delivery

### R-017 Filelist
MUST deliver a `filelist.f` made by `vlsit_lint_rtl.py filelist` that lists every delivered `.sv` file in compile order.
- Why: tools and the designer need the same compile order, and a hand-written list drifts from the files.
- Check: the filelist command output names every delivered file and the top module.

### R-018 Output folder
MUST save every deliverable, log and report inside the output folder, and ask the user for it when none is named.
- Why: results scattered over the working tree are hard to find, review and remove.
- Check: manual - no file of this run exists outside the output folder except edits the designer approved.
