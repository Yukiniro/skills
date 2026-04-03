# AI Agent Skills 合集

一组精选的 AI Agent Skills，为 AI 编程助手（Cursor、Claude Code 等）提升生产力和代码质量。

## 包含的 Skills

### Project Setup（项目初始化）

快速配置开发工具链、代码规范和 AI Agent Skills。自动检测项目环境，适配宿主项目的包管理器、框架和现有工具链。

- 智能环境检测（包管理器、项目类型、TypeScript）
- 自动生成 AGENTS.md 项目约定文档
- 配置 Prettier 代码格式化和 Vitest 测试框架
- 安装常用 AI Agent Skills（Vercel React、Frontend Design、shadcn/ui、Vitest）
- 为 Next.js 项目配置 next-intl 国际化

[查看文档 →](skills/project-setup/SKILL.md)

```bash
npx skills add https://github.com/Yukiniro/skills --skill project-setup
```

### Prompt Optimizer（提示词优化）

将模糊或简单的用户提示词转化为高质量、结构化的 AI 指令。运用 XML 标签、Few-shot 示例、思维链（Chain-of-Thought）等系统化优化技术。

- 基于「AI 即新员工」理念的系统化提示词优化
- 结构化提示词构建（角色、上下文、任务、要求、输出格式）
- 提升 AI 输出的可靠性、准确性和格式一致性

[查看文档 →](skills/prompt-optimizer/SKILL.md)

```bash
npx skills add https://github.com/Yukiniro/skills --skill prompt-optimizer
```

### Frontend Resume（前端简历）

将 PDF 简历转换为零依赖、动画丰富的交互式单页 HTML 简历网站。帮助用户通过视觉探索发现自己喜欢的美学风格。

- 零依赖单文件输出（内联 CSS/JS，无需构建工具）
- 10 种独特风格预设（Midnight Architect、Neon Terminal、Clean Slate 等）
- 滚动触发动画、浮动导航、交互式技能条
- 响应式布局、打印友好、WCAG AA 无障碍支持

[查看文档 →](skills/frontend-resume/SKILL.md)

```bash
npx skills add https://github.com/Yukiniro/skills --skill frontend-resume
```

### Resume Screener（简历筛选）

基于 10 级评分体系（C → SSS）和 9 维度多角度评分，系统化评估简历与岗位需求的匹配度，输出证据驱动的评估报告和招聘建议。

- 9 维度评估（学历、工作经验、技术能力、项目经验等）
- 支持中英文简历，理解 985/211、BAT/FAANG 体系
- 硬性要求检测与评级封顶机制
- 结构化输出：综合评级、维度详情、优劣势分析、面试建议

[查看文档 →](skills/resume-screener/SKILL.md)

```bash
npx skills add https://github.com/Yukiniro/skills --skill resume-screener
```

### Work Weekly Report（工作周报）

从每日工作日志生成结构化的周工作总结。按项目/主题分组而非按天排列，提取客观事实并分类归维。

- 按项目/主题分组，非时间顺序
- 仅陈述客观事实，不加主观评价
- 按维度分类（业务/功能、技术/基建、数据/调研）
- 支持中英文双语输出

[查看文档 →](skills/work-weekly-report/SKILL.md)

```bash
npx skills add https://github.com/Yukiniro/skills --skill work-weekly-report
```

### Smart Commit（智能提交）

自动分析 Git 变更并创建符合 Conventional Commits 规范的提交信息。全自动流程——分析 diff、判断类型、生成信息、执行提交，无需确认。

- Conventional Commits 格式：`type(scope): 描述`
- 自动类型检测（feat、fix、docs、refactor、perf、test、build、ci、style、chore、revert）
- 智能暂存：使用已暂存的变更，或在暂存区为空时暂存全部
- 描述语言自动跟随项目 commit 历史
- 敏感文件检测（`.env`、credentials）——警告并阻止提交
- 尊重 pre-commit hooks（不使用 `--no-verify`）

[查看文档 →](skills/smart-commit/SKILL.md)

```bash
npx skills add https://github.com/Yukiniro/skills --skill smart-commit
```

### Squash Commits（提交压缩）

将当前功能分支上的所有提交（相对于 main/master）压缩为一个干净的提交，同时保留分支名称。包含安全检查、用户确认和智能提交信息生成。

- 自动检测主分支（main/master）
- 安全检查：工作目录干净、不在主分支、至少 2 个提交
- 智能提交信息，原始信息作为列表保留
- 压缩后引导（force-push 提醒）
- 中英文双语触发

[查看文档 →](skills/squash-commits/SKILL.md)

```bash
npx skills add https://github.com/Yukiniro/skills --skill squash-commits
```

### Deep Code Analysis（深度代码分析）

系统性地分析和理解代码逻辑与业务需求。以"先测量，再理解，最后才动手"为核心原则，通过六步工作流建立对代码的深度认知。

- 六步工作流：明确范围 → 测量 → 结构认知 → 追踪逻辑 → 设计意图 → 呈现结果
- 三档规模策略：直接分析（<50KB）、按模块深入（50-500KB）、子 agent 并行（>500KB）
- 多种追踪模式：业务逻辑、数据流、调用链
- 专注于理解——不做 review、不做开发、不做重构
- 中英文双语触发

[查看文档 →](skills/deep-code-analysis/SKILL.md)

```bash
npx skills add https://github.com/Yukiniro/skills --skill deep-code-analysis
```

## 安装

一次性安装所有 Skills：

```bash
npx skills add https://github.com/Yukiniro/skills \
  --skill project-setup prompt-optimizer frontend-resume resume-screener work-weekly-report smart-commit squash-commits deep-code-analysis
```

或单独安装某个 Skill：

```bash
npx skills add https://github.com/Yukiniro/skills --skill frontend-resume
```

## 使用方法

在 Cursor、Claude Code 或任何支持 Agent Skills 的 AI 编程助手中：

| Skill              | 示例提示词                                              |
| ------------------ | ------------------------------------------------------- |
| Project Setup      | "使用 project-setup skill 初始化我的项目"               |
| Prompt Optimizer   | "使用 prompt-optimizer skill 优化这段提示词：……"        |
| Frontend Resume    | "将这份 PDF 简历转换成交互式网页"                       |
| Resume Screener    | "根据这份职位描述评估这份简历"                          |
| Work Weekly Report | "根据这些每日工作日志生成周报"                          |
| Smart Commit       | "提交代码" 或 "Commit my changes"                       |
| Squash Commits     | "压缩提交" 或 "Squash all commits on this branch"      |
| Deep Code Analysis | "分析这个模块" 或 "帮我理解这个业务逻辑"               |

## 创建自定义 Skill

以 [template/SKILL.md](template/SKILL.md) 作为起步模板：

```markdown
---
name: my-skill-name
description: A clear description of what this skill does and when to use it.
---

# My Skill Name

[在此添加你的指令]
```

frontmatter 只需要两个字段：

- `name` — Skill 的唯一标识符（小写，连字符分隔）
- `description` — 清晰描述该 Skill 的功能和使用场景

更多信息请参阅 [How to create custom skills](https://support.claude.com/en/articles/12512198-creating-custom-skills)。

## 项目结构

```
skills/
├── .claude-plugin/
│   └── marketplace.json        # Claude Code Plugin 市场配置
├── skills/
│   ├── project-setup/          # 项目初始化
│   │   ├── SKILL.md
│   │   ├── LICENSE.txt
│   │   └── templates/
│   │       ├── AGENTS.md
│   │       ├── prettier.config.md
│   │       ├── vitest.config.md
│   │       └── next-intl.config.md
│   ├── prompt-optimizer/       # 提示词优化
│   │   ├── SKILL.md
│   │   ├── LICENSE.txt
│   │   └── references/
│   │       └── GUIDE.md
│   ├── frontend-resume/         # 前端简历
│   │   ├── SKILL.md
│   │   ├── LICENSE.txt
│   │   ├── scripts/
│   │   │   └── extract_pdf.py
│   │   └── references/
│   │       ├── HTML_ARCHITECTURE.md
│   │       ├── STYLE_PRESETS.md
│   │       └── RESUME_COMPONENTS.md
│   ├── resume-screener/        # 简历筛选评估
│   │   ├── SKILL.md
│   │   ├── LICENSE.txt
│   │   └── references/
│   │       ├── EVALUATION_DIMENSIONS.md
│   │       ├── GRADING_RUBRIC.md
│   │       └── OUTPUT_FORMAT.md
│   ├── work-weekly-report/     # 周报生成
│   │   └── SKILL.md
│   ├── smart-commit/           # 智能 Git 提交
│   │   └── SKILL.md
│   ├── squash-commits/         # 提交压缩
│   │   └── SKILL.md
│   └── deep-code-analysis/    # 深度代码分析
│       └── SKILL.md
├── template/
│   └── SKILL.md                # 新 Skill 创建模板
├── .gitignore
├── LICENSE
└── README.md
```

## 贡献

欢迎提交 Issue 和 Pull Request。

1. Fork 本仓库
2. 创建功能分支（`git checkout -b feature/amazing-skill`）
3. 提交更改（`git commit -m 'Add some amazing skill'`）
4. 推送到分支（`git push origin feature/amazing-skill`）
5. 发起 Pull Request

## 许可证

MIT License

## 资源

- [Agent Skills Spec](https://agentskills.io/) - Agent Skills 标准规范
- [Cursor AI](https://cursor.sh/) - AI 优先的代码编辑器
- [Claude Code](https://www.anthropic.com/) - Anthropic 的 AI 编程助手
- [npx skills CLI](https://www.npmjs.com/package/skills) - Skills 安装工具
