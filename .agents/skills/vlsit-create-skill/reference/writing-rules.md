# Writing rules

Guidance only; the mandatory requirements are in [rule.md](../rule.md). The template
is [templates/rule.md.tpl](templates/rule.md.tpl).

## Anatomy of a rule

```
### R-012 Short title
MUST <one checkable requirement>.
- Why: <the reason, so edge cases can be judged>
- Check: <a script command, or "manual - how to verify">
```

- **ID**: `R-` plus three digits, as a level-3 heading. Group rules under level-2
  headings. Give a new rule the next free number. Never reuse the number of a deleted
  rule and never renumber, because SKILL.md, reports and users cite rules by ID.
- **Statement**: starts with `MUST` or `MUST NOT` (capitals). One requirement per
  rule: if you need "and MUST", write two rules. Use the active voice and name the
  object ("MUST ask the user before overwriting a file", not "overwriting should be
  avoided").
- **Why**: one sentence on what goes wrong without the rule.
- **Check**: how anyone can tell the rule was followed. Prefer a script command;
  otherwise "manual -" plus the concrete inspection.

## Good and bad statements

| Bad | Why it is bad | Better |
|---|---|---|
| `Be careful with existing files.` | not checkable, no MUST | `MUST ask the user before overwriting a file that this skill did not create.` |
| `MUST validate and report and mirror.` | three requirements | three rules |
| `MUST NOT overwrite files, except when it is convenient.` | the exception swallows the rule | state the exact exception: `... unless the caller passes -Force` |

## No duplicates, no conflicts

Two rules repeat each other when they demand the same thing in different words. They
conflict when satisfying one breaks the other (typically `MUST X` and `MUST NOT X`,
or two different values for the same setting).

`skillkit.py validate` compares the wording of every pair of statements:

| Output | Meaning | What to do |
|---|---|---|
| `ERROR ... duplicate` | almost the same words | merge into one rule; the other ID is retired |
| `ERROR ... conflict` | almost the same words, opposite polarity | decide which is right; rewrite one rule |
| `REVIEW ... possible-conflict` | similar words, opposite polarity | read both; reword if they really clash |
| `REVIEW ... possible-overlap` | heavy word overlap | read both; narrow the wording so each covers one thing |

The script cannot understand meaning, so a clean result does not prove that no two
rules conflict. It finds the candidates; you judge them. Resolve by merging or
rewording. Do not add a third rule that says "except when ...": that hides the clash
instead of removing it.

## Precedence

When files disagree: `rule.md` first, then `SKILL.md`, then `reference/`. Reference
files hold background and may be looser or older than the rules. If you find a
requirement written only in a reference file, make it a rule or delete it.

## How many rules

Only what must never be left to judgment: safety, honesty, formats, ordering,
limits. Style preferences and tips belong in SKILL.md or reference/. A long rule list
costs tokens on every run, and the longer it grows the more likely two rules clash.
