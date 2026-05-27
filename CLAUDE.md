# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repository is

A curated **collection of AI Agent Skills** distributed as a Claude Code plugin marketplace. Each skill is a self-contained directory of Markdown instructions (plus optional reference docs, scripts, and templates) that an AI coding assistant loads on demand. There is **no build, test, lint, or compile step** — the "source" is the prose itself. Quality work here means writing clear, well-scoped skill instructions, not shipping code.

Skills are consumed by end users via:

```bash
npx skills add https://github.com/Yukiniro/skills --skill <skill-name>
```

## Anatomy of a skill

Every skill lives in `skills/<name>/` and must contain a `SKILL.md`. Optional subdirectories:

- `references/` — deep-dive Markdown loaded **on demand**, not upfront (see progressive disclosure below)
- `scripts/` — helper scripts a skill shells out to (e.g. `frontend-resume/scripts/extract_resume.py`)
- `templates/` — file templates a skill copies/fills in (e.g. `project-setup/templates/`)
- `LICENSE.txt`

`SKILL.md` frontmatter has exactly two fields:

```yaml
---
name: my-skill-name        # lowercase, hyphen-separated; matches the directory name
description: What it does AND when to use it, with trigger keywords.
---
```

`template/SKILL.md` is the canonical starting point for a new skill.

## The two conventions that matter most

**1. The `description` is the activation trigger.** A skill only fires when the assistant matches the user's intent against this one line, so it must pack in concrete trigger phrases — and most skills here list them **bilingually (English + 中文)**. Study existing descriptions (`smart-commit`, `deep-code-analysis`, `leafer-js`) before writing one: they enumerate verbs and phrases users actually say ("commit", "提交代码", "analyze this module", "帮我理解这个业务逻辑"). A vague description means the skill never activates.

**2. Progressive disclosure keeps `SKILL.md` lean.** `SKILL.md` is loaded into context whenever the skill is considered, so it stays short and points to `references/*.md` for heavy detail that's only read when needed. `leafer-js` is the clearest example: a lean SKILL.md routing to 7 reference files. Don't inline a reference file's content into SKILL.md — link to it.

## Adding or renaming a skill — keep three things in sync

When you add, remove, or rename a skill, update **all** of these or the change is incomplete:

1. The `skills/<name>/` directory itself
2. `.claude-plugin/marketplace.json` — register the skill under `plugins[0].skills` as `./skills/<name>`
3. **Both** `README.md` and `README.zh-CN.md` — add the description section, the install command, and the usage-table row

> Note: `marketplace.json` currently lists only 7 of the 10 skills (it omits `work-weekly-report`, `squash-commits`, and `deep-code-analysis`). The READMEs are the more complete catalog. When touching the marketplace file, reconcile it against the actual `skills/` directory rather than trusting it as the source of truth.

## Windows / environment notes

- Any Python helper script (and tools like skill-creator) should be run with `PYTHONIOENCODING=utf-8` to avoid encoding errors on Windows.
- Avoid `: ` (colon-space) inside `description` YAML values — it can break the frontmatter parse. Rephrase instead.

## Git workflow & commit convention

PRs target `main`. Commits follow [Conventional Commits](https://www.conventionalcommits.org/): `type(scope): description`. The repo's own `smart-commit` skill (`skills/smart-commit/SKILL.md`) is the authority — follow it.

The format is `type(scope): description`, where:

- `scope` is optional — the affected skill or area (e.g. `smart-commit`, `project-setup`). Omit it when a change spans multiple unrelated skills.
- `description` starts with a verb, stays under ~50 chars, and is specific. Don't restate the type (`fix: fix the bug`).
- `type` is the highest-priority one that fits, from: `feat`, `fix`, `docs`, `refactor`, `perf`, `test`, `build`, `ci`, `style`, `chore`, `revert`. Since this repo is documentation-driven, most commits are `feat` (a new skill or capability) or `docs` (README / reference updates).

**Language:** match the surrounding history; commits here exist in both English and Chinese. When in doubt, match the language of the files being changed (e.g. an edit to a Chinese skill → Chinese description). Default to English if unclear.

**Rules:** never bypass hooks (`--no-verify`); never commit secrets (`.env`, credentials, keys). Branch off `main` before committing.

Examples:

```text
feat: add any-to-course skill (slides + quiz)
feat(smart-commit): 添加 smart-commit 技能及 README 说明
docs: update README with installation instructions for new skills
fix: correct typos and improve wording in SKILL.md
```
