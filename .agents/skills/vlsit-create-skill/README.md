# vlsit-create-skill

Creates a new skill in the house format: `SKILL.md` (workflow), `rule.md` (numbered rules), `reference/`, `scripts/`. Interviews the user, offers design options with advantages and disadvantages, then validates and mirrors the skill from the Claude Code canonical tree to `.agents/skills/` for Codex and `.dsh/skills/` for this repository's DeepSeek Harness setup with `scripts/vlsit_skillkit.py` (Python standard library only).

Tạo skill mới theo chuẩn: `SKILL.md` (quy trình), `rule.md` (rule có ID), `reference/`, `scripts/`. Skill phỏng vấn người dùng, đưa phương án thiết kế kèm ưu nhược điểm, rồi kiểm tra và đồng bộ từ cây chuẩn Claude Code sang `.agents/skills/` cho Codex và `.dsh/skills/` cho cấu hình DeepSeek Harness của repository này bằng `scripts/vlsit_skillkit.py` (chỉ dùng thư viện chuẩn Python).

Claude Code: `/vlsit-create-skill`; Codex: `$vlsit-create-skill`; DeepSeek Harness: `/vlsit-create-skill`; or describe the task naturally. / Claude Code: `/vlsit-create-skill`; Codex: `$vlsit-create-skill`; DeepSeek Harness: `/vlsit-create-skill`; hoặc mô tả trực tiếp yêu cầu.
