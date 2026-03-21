---
name: smart-commit
description: >
  Automatically analyze git changes and create Conventional Commits with Chinese descriptions.
  Use when: user wants to commit, asks to commit code, says commit/smart commit or any
  Chinese equivalents like 提交/提交代码/保存更改/自动提交. Fully automatic — analyzes diff,
  determines type, generates Chinese message, and commits without confirmation.
---

# Smart Commit

Analyze staged or unstaged git changes, determine the Conventional Commits type, and create a commit with a Chinese description. Fully automatic — no user confirmation needed.

## Commit Message Format

```
type(scope): 中文描述
```

- **type**: Required. One of: `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `build`, `ci`, `chore`, `revert`
- **scope**: Optional. The primary module, directory, or component affected. Omit if changes span many areas.
- **Description**: Required. Concise Chinese summary of what changed, under 50 characters.

## Workflow

### Step 1: Pre-flight Checks

Run `git status` to assess the working tree.

- **No changes at all** (clean working tree) → Tell the user there is nothing to commit and stop.
- **Merge conflict markers present** → Tell the user to resolve conflicts first and stop.

### Step 2: Stage Changes

- **If the staging area already has content** (files under "Changes to be committed") → Use staged changes as-is. Do NOT modify the staging area.
- **If the staging area is empty** → Run `git add -A` to stage all changes including untracked files.

### Step 3: Analyze Diff

Run `git diff --cached --stat` and `git diff --cached` to read the staged diff.

For large diffs (>500 lines), rely on `--stat` plus the first 200 lines of the full diff. The stat summary is usually sufficient for type/scope determination.

### Step 4: Determine Commit Type

Select the type based on these rules (first match wins):

| Type       | When to use |
|------------|-------------|
| `revert`   | A previous commit is being reverted |
| `feat`     | New functionality — new files with exports, API endpoints, components, routes |
| `fix`      | Bug fixes — correcting wrong behavior, fixing errors, patching edge cases |
| `docs`     | Only `.md` files, comments, or documentation changes |
| `test`     | Only test files changed (`*.test.*`, `*.spec.*`, `__tests__/`) |
| `build`    | Build config changes (`package.json` deps, bundler config, `tsconfig`, `Dockerfile`) |
| `ci`       | CI/CD files (`.github/workflows/`, `.gitlab-ci.yml`, `Jenkinsfile`) |
| `style`    | Whitespace, formatting, semicolons, CSS-only with no logic change |
| `perf`     | Optimizations — caching, lazy loading, memoization, algorithm improvements |
| `refactor` | Code restructuring with no behavior change — renames, extractions, reorganization |
| `chore`    | Everything else — tooling, config, maintenance, dependency bumps |

When multiple types apply, choose the one that best describes the **primary intent**.

### Step 5: Determine Scope

- All changes in one module/directory → use it as scope (e.g., `auth`, `api`, `utils`)
- Changes touch a single component → use component name (e.g., `Button`, `login`)
- Changes span multiple unrelated areas → omit scope

### Step 6: Generate Chinese Description

Follow these rules:

1. **Start with a verb**: 添加、修复、更新、重构、优化、移除、调整、配置
2. **Describe what changed**, not implementation details: "添加用户登录功能" not "在 auth 目录下新建了三个文件"
3. **Under 50 characters**
4. **No trailing punctuation**
5. **Avoid redundancy with type**: If type is `fix`, don't start with "修复" — describe what was fixed instead: `fix(auth): 用户登出后 token 未清除的问题`

### Step 7: Commit

Run `git commit -m "type(scope): description"`. Pass the message via heredoc for safe formatting:

```bash
git commit -m "$(cat <<'EOF'
type(scope): 中文描述
EOF
)"
```

Do NOT use `--no-verify` — let pre-commit hooks run. If a hook fails, report the error and stop.

## Examples

| Scenario | Message |
|----------|---------|
| New login page and API | `feat(auth): 添加用户登录页面和认证接口` |
| Fix null pointer in cart | `fix(cart): 修正商品数量为空时的崩溃问题` |
| Update README | `docs: 更新项目安装说明` |
| Refactor utils into modules | `refactor(utils): 将工具函数拆分为独立模块` |
| Add unit tests for parser | `test(parser): 补充解析器的单元测试` |
| Upgrade dependencies | `build: 升级 React 至 19.x 并更新相关依赖` |
| GitHub Actions config | `ci: 添加自动化部署工作流` |
| Format code | `style: 统一代码缩进和引号风格` |
| Memoize expensive render | `perf(list): 对列表渲染添加 useMemo 优化` |
| Misc config changes | `chore: 更新 .gitignore 和编辑器配置` |
| Revert broken release | `revert: 回退 v2.1.0 引入的支付模块变更` |

## Edge Cases

- **Sensitive files staged** (`.env`, `.env.local`, credentials, private keys): Warn the user and do NOT commit. Suggest adding them to `.gitignore`.
- **Only lockfile changes** (`package-lock.json`, `pnpm-lock.yaml`, `yarn.lock`): Use `chore(deps): 更新依赖锁文件`.
- **Lockfile + package.json together**: Use `build: 添加/更新项目依赖`.
- **Single deleted file**: Reflect the deletion — e.g., `chore: 移除废弃的配置文件`.
- **Binary files only**: Use `chore: 更新静态资源文件`.
