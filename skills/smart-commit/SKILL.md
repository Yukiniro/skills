---
name: smart-commit
description: Automated Git commit with Conventional Commits format. Analyzes staged changes, determines commit type and scope, detects description language from commit history (defaults to English), and generates a complete commit message. Use when the user says "commit", "smart commit", "提交代码", "帮我提交", or any variation of requesting a git commit with an auto-generated message.
---

# Smart Commit

Analyze code changes and generate a Conventional Commits message automatically. The description language follows the project's existing commit history — if prior commits are in Chinese, the description will be in Chinese; if in English, it will be in English. The user can also specify a language explicitly.

## Workflow

### Step 1: Pre-flight Check

Run `git status` to assess the working tree.

- If there are **no changes** (clean working tree, nothing staged), inform the user and stop.
- If there are **merge conflicts**, inform the user and stop — do not attempt to commit during a conflict.

### Step 2: Stage Changes

Check whether the staging area already has content:

- If `git diff --cached --stat` shows staged files, use them as-is — the user intentionally staged specific files.
- If the staging area is empty but there are unstaged changes, run `git add -A` to stage everything.

Before proceeding, check for sensitive files in the staging area (`.env`, `.env.*`, `credentials.*`, `*secret*`, `*.pem`, `*.key`). If any are found, **warn the user and stop** — do not commit secrets.

### Step 3: Analyze Changes

Run these commands to understand what changed:

- `git diff --cached --stat` — file-level summary (which files, insertions/deletions)
- `git diff --cached` — actual content changes

If the diff output exceeds 200 lines, truncate and work with the summary + first 200 lines. This is enough to determine type, scope, and description.

### Step 4: Determine Commit Type

Based on the changes, select the most appropriate type using this priority order:

| Priority | Type | When to use |
|----------|------|-------------|
| 1 | `revert` | Reverting a previous commit |
| 2 | `feat` | New feature or capability |
| 3 | `fix` | Bug fix |
| 4 | `docs` | Documentation only |
| 5 | `test` | Adding or updating tests |
| 6 | `build` | Build system or dependencies |
| 7 | `ci` | CI/CD configuration |
| 8 | `style` | Code formatting, whitespace, semicolons |
| 9 | `perf` | Performance improvement |
| 10 | `refactor` | Code restructuring without behavior change |
| 11 | `chore` | Maintenance, tooling, other tasks |

If changes span multiple types, use the highest-priority type that covers the primary intent.

### Step 5: Determine Scope

Scope is the module, component, or area affected:

- Single module/component changed → use it as scope (e.g., `auth`, `api`, `button`)
- Changes span multiple unrelated areas → omit scope entirely
- Keep scope short — one word when possible

### Step 6: Detect Description Language

Run `git log --oneline -10` to examine recent commit messages.

- Identify the language used in the majority of recent commit descriptions (after the type/scope prefix).
- Use that same language for the new commit description. This is not limited to Chinese or English — it can be any language the project uses.
- If the user explicitly requests a language (e.g., "用中文提交", "commit in English"), use the requested language instead.
- If history is empty or the language cannot be determined, default to **English**.

### Step 7: Generate Description

Write the description in the detected language:

- Start with a verb (e.g., "add", "fix", "update" / "添加", "修复", "更新")
- Keep it under 50 characters
- Do not repeat information already conveyed by the type (e.g., don't write `fix: fix the bug`)
- Be specific about what changed, not vague

### Step 8: Commit

Run the commit command:

```
git commit -m "type(scope): description"
```

Or without scope:

```
git commit -m "type: description"
```

**Never skip hooks** — do not use `--no-verify`. If a pre-commit hook fails, report the error to the user and stop. Do not retry automatically.

## Edge Cases

| Situation | Action |
|-----------|--------|
| Clean working tree | Inform user "nothing to commit" and stop |
| Merge conflicts present | Inform user and stop |
| `.env` or credential files staged | Warn and refuse to commit |
| Only lockfile changes (`package-lock.json`, `yarn.lock`, `pnpm-lock.yaml`) | `chore(deps): update lockfile` |
| Only binary/asset files | `chore: update static assets` |
| Pre-commit hook fails | Report error, do not retry |

## Examples

**English examples:**

```
feat(auth): add JWT token refresh mechanism
fix(api): resolve null pointer in user endpoint
docs: update installation instructions in README
test(utils): add unit tests for date formatting
refactor(db): extract connection pool into shared module
chore(deps): update lockfile
style: apply prettier formatting to components
perf(query): add database index for user lookups
build: upgrade webpack to v5
ci: add GitHub Actions workflow for staging deploy
```

**Chinese examples:**

```
feat(auth): 添加 JWT 令牌刷新机制
fix(api): 修复用户接口空指针异常
docs: 更新 README 安装说明
test(utils): 为日期格式化添加单元测试
refactor(db): 将连接池提取为共享模块
chore(deps): 更新锁文件
style: 对组件应用 prettier 格式化
perf(query): 为用户查询添加数据库索引
build: 升级 webpack 至 v5
ci: 添加 GitHub Actions 预发布部署流程
```
