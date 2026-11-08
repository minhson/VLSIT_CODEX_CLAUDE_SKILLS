# Interview guide

Guidance only; the mandatory requirements are in [rule.md](../rule.md) (R-029, R-035,
R-038, R-039). Write every message to the user in the language they use.

## Why interview first

The user knows the business; the assistant knows the format. A skill built from a
one-line request gets the purpose roughly right and the details wrong: the triggers
too broad, the output in the wrong place, a mandatory requirement missing. The
interview collects those details while they are cheap to change.

## The opening message

Send one message. Ask the user to describe the skill in their own words, say that
rough or partial answers are fine, and list the topics. Keep it short enough to read
in half a minute. Example (translate it, and adapt the example to the request):

> To build this skill well I need a description in your own words. Answer what you
> can, in any order; I will ask about the gaps.
> 1. **Purpose** - what should the skill do, and what should it deliberately not do?
> 2. **Who and when** - who will use it, and what would they type when they want it?
> 3. **Input** - what do they hand over (a file, a folder, a number, a sentence)?
> 4. **Output** - what comes out, in which format, saved where?
> 5. **Steps today** - how is the job done by hand now, step by step?
> 6. **Must and never** - what must always happen, and what must never happen?
> 7. **Material** - are there sample files, templates or documents it should use? A
>    sample input with the result you expect is the most useful thing you can give me.
> 8. **Environment** - Windows only? Internet allowed? Anything confidential?
>
> Example for a meeting-minutes skill: "Turns my raw notes (.txt) into a Word
> document in our template, listing decisions and action items with owners. It must
> never invent an owner. People say 'write up today's meeting'."

## What each topic should yield

| Topic | You need to leave with | Becomes |
|---|---|---|
| Purpose | one sentence of what it does, one of what it does not | intro of SKILL.md, the description |
| Who and when | the phrases and situations that should trigger it | the "Use when ..." part of the description |
| Input | kind, location, size, typical quality, what to do when it is missing | the first workflow step, input checks in a script |
| Output | format, location, naming, who reads it | the Output section, a script that writes it |
| Steps today | the order a person follows, and where judgment is needed | the workflow; judgment stays in SKILL.md |
| Must and never | each requirement as one sentence, and what goes wrong if it is broken | one rule each, the Why line |
| Material | files, templates, sources, samples | `reference/` files, test inputs |
| Environment | OS, network, installs, secrecy, size and time limits | `compatibility`, script choices |

Mechanical steps (anything with one right answer: parse, convert, count, compare,
download, copy) are found by asking "which of these steps would a computer do
identically every time?". They become Python scripts.

## Follow-up questions

- Ask only about gaps and vague answers. Do not ask what the conversation or the
  repository already tells you; read the files first.
- At most four questions per round and two rounds. Prefer concrete questions with an
  example ("Should the minutes name the owner of each action, or only the team?") over
  abstract ones ("What are the requirements?").
- When a follow-up offers choices, it is an option set: end it with an open choice
  ("Other - write your own idea"), as the design step does.
- Treat "you decide" as an invitation to propose. State the proposal as an
  assumption and put it in the design summary, where the user confirms or changes it.
  Never silently fill a gap.
- A vague answer ("it should be good") is a gap. Ask for an observable test: what
  would a good result look like next to a bad one?

## When the user wants to change an existing skill

Read the skill first (SKILL.md, rule.md, the file list). Ask what is wrong or missing
instead of re-interviewing from the start, and ask for approval before changing the
folder (R-030).

## The design summary

After the options are settled, send one summary and ask for approval or changes. The
skill folder is created only after the user approves.

```
Skill: <name>
Description (draft): <one line, 500 characters at most>
Rules: R-001 <one line> ... (the rules that will be written)
Workflow: <numbered steps, one line each>
Scripts: <file> - <what it does>
Reference: <file> - <what it holds>
Environment: <runtime, network, installs>
Decisions: <decision> - <option chosen> (<user's own idea, if any, in their words>)
Assumptions: <anything you proposed because the user said "you decide">
```

Mark each of the user's own ideas as such and keep their wording, so that they can see
it was heard.
