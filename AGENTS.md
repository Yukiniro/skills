# Repository Guidelines

## Project Structure & Module Organization

This Claude Code plugin marketplace distributes Markdown-based AI agent skills and helper scripts.

- `skills/<skill-name>/SKILL.md`: each skill's entry point.
- Skill-local `references/`, `scripts/`, and `templates/`: supporting documentation, executable helpers, and reusable assets.
- `template/SKILL.md`: starting point for new skills.
- `.claude-plugin/marketplace.json`: marketplace registration.
- `README.md` and `README.zh-CN.md`: English and Chinese catalogs.

## Build, Test, and Development Commands

There is no repository-wide build, development server, test runner, or lint configuration. Vitest and Prettier files under `skills/project-setup/templates/` are templates for downstream projects.

Create skills from `template/SKILL.md`, replacing its placeholders. Run checks from the repository root:

```bash
# When marketplace registration changes:
python3 -m json.tool .claude-plugin/marketplace.json > /dev/null
# When smart-commit evaluation cases change:
python3 -m json.tool skills/smart-commit/evals/evals.json > /dev/null
git diff --check
```

JSON checks validate syntax; `git diff --check` detects whitespace errors in tracked changes. Inspect newly created files separately.

## Coding Style & Naming Conventions

Use lowercase, hyphen-separated skill directory names. Each `SKILL.md` starts with YAML frontmatter containing only `name` and `description`; the name must match its directory. Describe the capability and activation conditions with concrete English and Chinese triggers where appropriate. Avoid colon-space in unquoted descriptions.

Link detailed references instead of duplicating them. Use relative Markdown links, language-labelled code fences, two-space JSON indentation, and four-space Python indentation. Preserve each skill's reference filename conventions.

## Testing Guidelines

There is no automated coverage threshold or bundled evaluation runner. For prose-only edits, check changed instructions, links, and examples. For behavior changes, exercise representative prompts or helper inputs and record observed results; use `skills/smart-commit/evals/evals.json` as the format for new evaluation cases. Exercise Git-mutating skills in a disposable repository.

Finish after relevant checks pass and problems introduced by the change are fixed. Report unavailable checks or unrelated failures without expanding scope. Editing instructions does not authorize executing the commits, pushes, or external actions they describe.

## Commit & Pull Request Guidelines

History predominantly uses Conventional Commits: `feat: add leafer-js skill` or `docs(skill-name): clarify usage`. English and Chinese descriptions both appear; match the changed content.

Work on a feature branch and target `main`. Describe affected skills and validation; link relevant issues and include screenshots for visual output changes. When adding, removing, or renaming a skill, synchronize its directory, marketplace registration, and both README catalogs, including install examples and usage-table entries. Keep credentials and machine-local configuration out of commits; preserve Git hooks.
