---
name: squash-commits
description: >
  Squash all commits on the current branch (relative to the main branch) into a single commit while preserving the branch name.
  Use when: user wants to squash commits, clean up branch history, compress multiple commits into one, or tidy up before merging.
  Triggers on: squash commits, 压缩提交, 合并提交, clean up commits, compress commits, squash branch, 整理提交记录, 合并为一个提交.
  Make sure to use this skill whenever the user mentions squashing, compressing, or cleaning up commit history on a branch, even if they don't use the exact term "squash".
---

# Squash Commits

Compress all commits on the current feature branch (relative to the main branch) into a single, clean commit. The branch name stays the same — only the commit history changes.

## Workflow

### Step 1: Detect the Main Branch

Determine whether the repository uses `main` or `master` as its primary branch:

```bash
git symbolic-ref refs/remotes/origin/HEAD 2>/dev/null | sed 's@^refs/remotes/origin/@@'
```

If that fails (e.g., `origin/HEAD` is not set), fall back to checking which branch exists locally:

```bash
git branch --list main master
```

Use whichever one exists. If both exist, prefer `main`. Store the result as `$MAIN_BRANCH` for subsequent steps.

### Step 2: Safety Checks

Run all three checks before proceeding. If any fail, stop and explain the issue to the user.

1. **Not on the main branch** — The current branch must not be the main branch itself. Squashing the main branch makes no sense and would rewrite shared history.

   ```bash
   CURRENT_BRANCH=$(git branch --show-current)
   ```

   If `$CURRENT_BRANCH` equals `$MAIN_BRANCH`, stop with a message: "You are currently on the main branch. Switch to a feature branch first."

2. **Clean working directory** — There must be no uncommitted changes (staged or unstaged). A dirty working tree would mix unrelated changes into the squashed commit.

   ```bash
   git status --porcelain
   ```

   If output is non-empty, stop with a message: "You have uncommitted changes. Please commit or stash them first."

3. **Commits exist to squash** — The branch must have at least 2 commits ahead of the main branch. With 0 or 1 commits, there's nothing to squash.

   ```bash
   MERGE_BASE=$(git merge-base $MAIN_BRANCH HEAD)
   COMMIT_COUNT=$(git rev-list --count $MERGE_BASE..HEAD)
   ```

   If `$COMMIT_COUNT` is 0, stop: "This branch has no commits ahead of $MAIN_BRANCH."
   If `$COMMIT_COUNT` is 1, stop: "This branch has only 1 commit — nothing to squash."

### Step 3: Show the User What Will Happen

Before making any changes, show the user a summary so they can confirm:

- Current branch name
- Main branch name
- Number of commits that will be squashed
- List of those commits (hash + message)

```bash
git log --format="%h %s" $MERGE_BASE..HEAD
```

Present this as a clear summary, for example:

```
Branch: feature-login
Squashing 5 commits into 1 (relative to main):
  a1b2c3d feat: add login form
  d4e5f6g fix: handle empty password
  h7i8j9k style: adjust button alignment
  l0m1n2o refactor: extract validation logic
  p3q4r5s test: add login form tests
```

Ask the user to confirm before proceeding. This is a destructive operation — once squashed, the original individual commits are gone from the branch history (they can still be recovered via reflog within the git GC window, but that's not something typical users should rely on).

### Step 4: Build the Commit Message

Compose a commit message for the squashed commit. The message should be useful and informative:

**Title line:** Use the first commit's message as the base, or derive a summary from the branch name. If the branch name follows a pattern like `feature/login` or `fix/auth-bug`, convert it to a readable title (e.g., "feat: add login functionality").

**Body:** List all original commit messages as bullet points so the history isn't completely lost:

```
feat: add login functionality

Squashed commits:
- feat: add login form
- fix: handle empty password
- style: adjust button alignment
- refactor: extract validation logic
- test: add login form tests
```

Show the proposed commit message to the user and let them confirm or provide a custom message. If the user provides their own message, use that instead.

### Step 5: Execute the Squash

```bash
git reset --soft $MERGE_BASE
git commit -m "<the commit message>"
```

`git reset --soft` moves HEAD back to the fork point while keeping all file changes staged. The subsequent `git commit` bundles everything into a single commit. The branch name is unchanged — only the commit graph is rewritten.

### Step 6: Verify and Inform

After the squash, confirm success:

```bash
git log --oneline -5
```

Show the user the new clean history. Also check whether the branch has been pushed to a remote:

```bash
git branch -vv | grep "^\*"
```

If the branch tracks a remote, remind the user: "This branch has been pushed before. You'll need to force-push to update the remote: `git push --force-with-lease`". Recommend `--force-with-lease` over `--force` because it guards against overwriting someone else's work on the same branch.

## Edge Cases

- **Detached HEAD** — If not on any branch, abort with a clear message.
- **Diverged from main** — The squash works on commits since the merge-base, so it handles divergence correctly. The merge-base is the most recent common ancestor, not the tip of main.
- **Merge commits in the branch** — `git reset --soft` handles this fine; all changes (including those from merges) end up staged.
- **Branch has been rebased** — If the branch was previously rebased onto main, the merge-base is already up to date and the squash proceeds normally.
