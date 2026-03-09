---
name: work-weekly-report
description: >
  Generate structured weekly work summaries from daily work logs.
  Use when: user provides daily work logs/notes and asks to create a weekly report/summary (周报/周工作总结),
  or when user pastes fragmented daily entries and wants them consolidated into a categorized summary.
  Triggers on keywords: 周报, 周工作总结, weekly summary, weekly report, 工作日志整理, 每日日志汇总.
---

# Work Weekly Report

Extract key information from fragmented daily work logs and produce a structured, objective weekly work summary grouped by project/topic.

## Processing Rules

1. **Group by project/topic** — Never list by day (Mon/Tue/Wed). Break chronological order and aggregate by project or work item.
2. **Objective facts only** — State actions and results ("released version X", "developed tool Y"). Never include subjective evaluations, emotional descriptions, or modifiers ("efficiently", "in-depth", "successfully").
3. **Merge related items** — If the same feature/task spans multiple days (e.g., initial release on Monday, optimization on Thursday), merge into one entry describing the full scope.
4. **Categorize** — Group items into dimensions (adjust categories based on actual content):
   - 业务/功能迭代 (Business/Feature Iteration)
   - 技术/基建优化 (Technical/Infrastructure)
   - 数据/调研/其他 (Data/Research/Other)

## Output Format

```
**1. [Category Name]**
*   [Core Item]: [detail 1], [detail 2].
*   [Core Item]: [detail].

**2. [Category Name]**
*   [Core Item]: [detail 1], [detail 2].
```

## Example

Input (daily logs):

```
周一：上午修复了商品详情页图片加载异常的 bug，下午参加需求评审会，讨论了 v2.5 版本新功能。
周二：开发用户积分兑换功能前端页面，完成了 80%。
周三：继续开发积分兑换页面并联调接口，修复了 2 个样式问题。升级了前端构建工具从 Webpack 4 到 Webpack 5。
周四：发布积分兑换功能到测试环境，配合测试验证。调研了 React Server Components 方案。
周五：修复测试反馈的 3 个积分兑换相关 bug，编写了积分模块的单元测试。
```

Output:

```
**1. 业务/功能迭代**
*   用户积分兑换功能：完成前端页面开发、接口联调，发布至测试环境，修复测试反馈的 3 个 bug，编写单元测试。
*   商品详情页：修复图片加载异常的 bug。
*   v2.5 版本：参加需求评审会，讨论新功能方案。

**2. 技术/基建优化**
*   前端构建工具：从 Webpack 4 升级至 Webpack 5。

**3. 数据/调研/其他**
*   技术调研：调研 React Server Components 方案。
```
