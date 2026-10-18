# Skill format: facts for both tools

Checked on 2026-10-16 against the official pages:
[Claude Code skills](https://code.claude.com/docs/en/skills) and
[Codex skills](https://learn.chatgpt.com/docs/build-skills). Tool documentation
changes; if something here looks wrong, check the pages again before relying on it.

This file is background only. Mandatory requirements are in [rule.md](../rule.md).

## What both tools share

A skill is a folder whose entry point is `SKILL.md`: a YAML frontmatter block, then
Markdown instructions. The assistant always sees `name` and `description`. It loads
the body of `SKILL.md` only when the skill is chosen (by the user, or because the
request matches the description), and it reads other files in the folder only when
`SKILL.md` points to them. Scripts are run, not read into context.

## Where each tool looks

| | Claude Code | Codex |
|---|---|---|
| Project skills | `.claude/skills/<name>/SKILL.md` | `.agents/skills/<name>/SKILL.md` |
| Personal skills | `~/.claude/skills/<name>/` | `$HOME/.agents/skills/<name>/` |
| Other | enterprise, plugin, nested `.claude/skills/` in sub-folders | admin `/etc/codex/skills`, bundled system skills |
| Search path | working directory up to the repository root | working directory up to the repository root |

Hence the house setup: author in `.claude/skills/`, generate the `.agents/skills/`
copy with `vlsit_skillkit.py mirror`.

## Frontmatter

| Key | Claude Code | Codex | House rule |
|---|---|---|---|
| `name` | optional (defaults to the folder name) | required | required, equals the folder |
| `description` | recommended | required | required, one line, at most 500 characters |
| `compatibility` | accepted, up to 500 characters | not listed | optional; states runtime and network needs |
| `license`, `metadata` | accepted (Agent Skills spec) | not listed | allowed |
| anything else (`allowed-tools`, `disable-model-invocation`, `context`, ...) | tool-specific controls | goes in `agents/openai.yaml` | not allowed in SKILL.md |

Why keep to the portable keys: Claude Code ignores unknown keys without a message,
but outside Claude Code (web uploads, the Skills API) unknown keys are a hard error,
and Codex keeps its own options in `agents/openai.yaml`. Specification limits:
`name` up to 64 characters of lowercase letters, digits and hyphens; `description`
up to 1024. The house limit for `description` is stricter (500) because Claude Code
truncates the combined description text in its skill listing and many skills share
that listing.

## Invocation

| | Claude Code | Codex |
|---|---|---|
| Explicit | `/skill-name` | `$skill-name`, or `/skills` to pick |
| Implicit | the assistant loads a skill whose description matches the request | same |

Skill files must not contain either syntax (see R-009); the README of the repository
documents invocation for users.

## Folder names inside a skill

Only `SKILL.md` is special. Codex documentation names the optional folders
`scripts/`, `references/` and `assets/`; Claude Code documentation shows
`reference.md` files. Neither tool requires those names, because supporting files are
found through links in `SKILL.md`. The house format uses `reference/` (singular) and
`scripts/`, plus `rule.md`.

## Size and loading

- Keep `SKILL.md` under 500 lines (Claude Code guidance); the body stays in context
  after it loads.
- Claude Code re-attaches up to 5,000 tokens of an invoked skill after context
  compaction, so the most important instructions belong near the top.
- Link supporting files directly from `SKILL.md` and say when to read each one.
  Files reached through a chain of links may be read only in part.
