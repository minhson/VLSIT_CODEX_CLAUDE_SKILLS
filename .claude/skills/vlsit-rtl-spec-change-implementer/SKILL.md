---
name: vlsit-rtl-spec-change-implementer
description: Analyze existing RTL against an optional prior specification and a requested new feature, present a minimal-change plan in scientific English for explicit user sign-off, then implement only the approved changes and report the RTL code-change percentage.
---

# RTL Specification Change Analysis and Implementation

## Operating contract

1. Read [rule.md](rule.md) completely before doing anything. Its numbered rules (RSC-xxx) are mandatory and rank above everything else.
2. Follow the workflow below. It orders the work; it never relaxes a rule.
3. Consult `references/` for the review-document template. References rank below `rule.md`.
4. Run helpers from `scripts/` (index: [scripts/README.md](scripts/README.md)) instead of repeating manual steps.
5. Apply the self-improvement rules RSC-090..095 at the end of every run.

## Workflow

1. **Inputs (RSC-010..015).** RTL directory (required), old spec (optional), new spec or description. Ask once for gaps.
2. **Baseline (RSC-020..024).** Read-only analysis. Before any edit run `python scripts/rtl_change_metrics.py snapshot <RTL_DIR> <SNAPSHOT_DIR>`, with the snapshot outside the RTL tree.
3. **Plan (RSC-030..033).** Write `rtl_change_review.md` using [references/review_template.md](references/review_template.md).
4. **Gate (RSC-034..037).** Ask APPROVE / REVISE / STOP for the named plan version; wait.
5. **Implement (RSC-040..044).** Minimal approved edits only.
6. **Validate and report (RSC-050..051, 060..063).** Run only approved checks, then `python scripts/rtl_change_metrics.py compare <SNAPSHOT_DIR> <RTL_DIR>` for the percentage; update the review document.
7. **Improve (RSC-090..095).** Add or fix scripts and references, log in `references/improvement_log.md`, and propose rule changes to the user.

## Folder map

| Path | Role | Priority |
|---|---|---|
| `rule.md` | Numbered mandatory rules | 1 (highest) |
| `SKILL.md` | Workflow and routing | 2 |
| `references/` | Review template, improvement log | 3 |
| `scripts/` | `rtl_change_metrics.py` and model-added helpers | tool |
