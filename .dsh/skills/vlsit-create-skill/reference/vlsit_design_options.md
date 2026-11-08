# Design options

Guidance only; the mandatory requirements are in [rule.md](../rule.md) (R-036, R-037,
R-039 for presenting options; R-020 to R-028 limit what the scripts may do). Write
every message to the user in the language they use.

## When to offer options

Offer options for a decision when the alternatives really differ in what the skill
does, costs or risks, and the right answer depends on the user's business. Do not
offer options for settled matters (name format, file layout, the house rules) or
for something the user already said. Raise only the decisions that fit this skill,
usually two to five, in one message.

| Decision | Raise it when |
|---|---|
| D1 Scope | the job has parts that could be used on their own |
| D2 Where the work is done | always, unless the user already described it |
| D3 User confirmation | the skill writes, overwrites, deletes, sends or downloads |
| D4 Trigger breadth | other skills or similar requests exist |
| D5 Reference material | the skill depends on documents, templates or outside data |
| D6 Output location | the skill produces files |
| D7 Script structure | the skill has more than one scripted job |
| D8 Outside packages | the standard library cannot do a needed job |
| D9 Rule strictness | the user listed many requirements |
| D10 Testing depth | the skill will be used by others |

## How to present a decision

For each decision, show the options as below. Keep each option to a few lines, in
plain words, and say what it means in practice (time, tokens, risk, effort), not
only what it is called.

```
Decision D3 - How much should the skill ask before acting?
Why it matters: it writes files, and a wrong guess would overwrite your work.

A. Ask before each risky step (recommended)
   Meaning: stops and asks before writing, downloading or overwriting.
   Advantages: nothing happens that you did not see; mistakes are caught early.
   Disadvantages: more interruptions on a long job.
   Choose it when: the files matter and runs are not very frequent.
B. Run on its own
   Meaning: does everything after your first request.
   Advantages: fastest; no interruptions.
   Disadvantages: a wrong guess is acted on before you see it.
   Choose it when: the skill only reads and reports.
C. Other - write your own idea: ______________________

Recommendation: A, because the skill overwrites files.
```

Rules for the message:

- Every option set ends with the open choice "Other - write your own idea" (R-039). If
  the host offers a multiple-choice question feature, use it for the choosing, but
  keep this analysis in the message first, because option labels are too short to
  carry it, and make sure the feature lets the user type a free answer; if it does
  not, add the open choice as an ordinary option. In plain text, keep the blank
  line to be filled in.
- At least two real options besides the open one (R-036). Do not pad with a
  strawman that nobody would pick.
- Mark at most one option as recommended and give the reason (R-037). The
  recommendation follows from the facts the user gave; if you have no reason, mark
  none.
- Be even-handed: every option has a real advantage and a real disadvantage.
- Number the decisions and the options so that the user can answer "D1 B, D2 other:
  ...".
- "You decide" means the recommended option; record it as such. A silent answer
  is not a choice: ask again.

## Handling the user's own idea

Restate it in one sentence to show it was understood and record it in the user's
words. Then check it against the rules. If it fits, adopt it. If it collides with a
rule (for example a package that is not in the standard library, a script that
overwrites silently, an extra frontmatter key), name the rule, explain the reason in
one sentence and propose the nearest variant that complies; do not silently break a
rule and do not silently drop the idea. Some conflicts are the user's call to
make: a package needs their approval (R-022), and they can ask to change a rule of
this skill, which is then done in rule.md as a separate, explicit edit.

## The catalog

### D1 Scope: one skill or several

| Option | Advantages | Disadvantages | Choose it when |
|---|---|---|---|
| One skill for the whole job | one trigger; simple to use; one place to maintain | long workflow; broad description may fire at the wrong time; parts cannot be reused | the steps always run together, by the same person |
| Several small skills that chain | each is focused and reusable; precise triggers; easier to test | the user must know the chain; more files and README entries; shared prerequisites repeat | the parts are useful on their own, as with downloading a document and converting a scan |

### D2 Where the work is done

| Option | Advantages | Disadvantages | Choose it when |
|---|---|---|---|
| Scripts do the mechanical work, instructions do the judgment (usual) | repeatable; few tokens per run; testable | needs Python; effort to write the scripts; unusual input needs a script change | there is a mix of exact steps and judgment |
| Mostly scripts | the same result every time; cheapest to run | rigid; every new case needs a developer | the job is fully rule-based, such as converting or checking files |
| Mostly instructions | fastest to build; flexible; no scripts to maintain | results vary run to run; costs more tokens; harder to verify | the job is mostly drafting or judgment (R-020 still moves any exact step into a script) |

### D3 User confirmation

| Option | Advantages | Disadvantages | Choose it when |
|---|---|---|---|
| Ask before each risky step | nothing happens unseen; early correction | more interruptions | files matter and the job is not very frequent |
| Show a dry run, then run on approval | one decision shows everything that will change | the script needs a `--dry-run` mode; extra effort | many files or many changes in one run |
| Run on its own | fastest | wrong guesses are acted on first | the skill only reads and reports |

### D4 Trigger breadth (the description)

| Option | Advantages | Disadvantages | Choose it when |
|---|---|---|---|
| Broad: many situations and phrasings | the user need not know the skill name; catches paraphrases | may fire when not wanted; competes with other skills | the skill is the obvious tool for a common request |
| Narrow: specific documents and keywords | precise; rarely fires by mistake | misses requests phrased differently; may need to be called by name | similar skills exist, or a wrong run is costly |

A skill that must never run unless called by name cannot be expressed in the portable
format: the switch for it is tool-specific (R-005). Narrow wording is the nearest
substitute; say so if the user asks.

### D5 Reference material

| Option | Advantages | Disadvantages | Choose it when |
|---|---|---|---|
| Keep copies in `reference/` | works offline; versioned; the same every run | may go stale; adds size; check the licence of what is copied | the material is stable and small |
| A script fetches it at run time | always current | needs network; the source may change or block scripts; one more failure mode | the data changes often |
| The user supplies it each time | nothing to maintain; no licence question | effort at every run; quality varies | the material differs per case, or is confidential |

### D6 Output location

| Option | Advantages | Disadvantages | Choose it when |
|---|---|---|---|
| Next to the input | easy to find | clutters the folder; risk of overwriting | single files, and the user wants the result beside the source |
| A dedicated output folder | tidy; inputs untouched | the user has to look in another place | many files, or batch runs |
| Ask each time | fits every case | one more question per run | locations differ by case |

An existing output file is never overwritten unless the user passes `--force` (R-027).

### D7 Script structure

| Option | Advantages | Disadvantages | Choose it when |
|---|---|---|---|
| One script with sub-commands | one entry point; shared code; simple to document | grows large; one bug touches everything | the jobs share data or helpers |
| One small script per job | simple; independent | duplicated helpers; more files to link and explain | the jobs are unrelated |

### D8 Outside packages

| Option | Advantages | Disadvantages | Choose it when |
|---|---|---|---|
| Standard library only (default) | nothing to install; fewest failure modes; works offline | more code for hard formats (PDF, spreadsheets) | the standard library can do the job, even if longer; Word and Excel files can be built as zip archives of XML |
| One approved package | far less code for hard formats | the user must install and keep it working; version drift; trouble on locked-down or offline machines | the format is too hard to handle without it; needs the user's approval (R-022) |

### D9 Rule strictness

| Option | Advantages | Disadvantages | Choose it when |
|---|---|---|---|
| Few strict rules (safety, honesty, formats, limits) | short to read; cheap per run; the assistant keeps freedom | more variation in style and wording | most skills |
| Detailed rules (also wording, order, style) | consistent results | long rule.md costs tokens every run; more chance of conflicts; more upkeep | the output is a controlled document or a legal text |

### D10 Testing depth

| Option | Advantages | Disadvantages | Choose it when |
|---|---|---|---|
| Smoke test: validate, and run scripts on a sample | quick; always possible | does not show whether an assistant picks and follows the skill | a personal or low-risk skill |
| Sample inputs and expected outputs kept in `reference/`, with a self-test script | catches regressions after edits | more files to keep current | the skill will be edited and shared |
| Also try it in a fresh session with a realistic request | tests the triggering and the workflow | needs the user's time | before sharing the skill with the team |
