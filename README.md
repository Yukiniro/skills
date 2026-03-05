# AI Agent Skills Collection

一组精心设计的 AI Agent Skills，提升 AI 编程助手（Cursor、Claude Code 等）的工作效率和代码质量。

## 包含的 Skills

### Project Setup

为新项目快速配置开发工具链、代码规范和 AI agent skills。自动探测项目环境并适配宿主项目的包管理器、框架和已有工具链。

- 智能环境探测（包管理器、项目类型、TypeScript）
- 自动生成 AGENTS.md 项目规范文档
- 配置 Prettier 代码格式化与 Vitest 测试框架
- 安装常用 AI Agent Skills（Vercel React、Frontend Design、shadcn/ui、Vitest）
- 为 Next.js 项目配置 next-intl 国际化

[详细文档 →](src/project-setup/SKILL.md)

### Prompt Optimizer

将模糊或简单的用户提示词转换为高质量、结构化的 AI 指令。使用 XML 标签、Few-shot 示例和 Chain-of-Thought 等系统化优化技术。

- 基于"AI 作为新员工"理念的系统化提示词优化
- 结构化提示词构建（role、context、task、requirements、output_format）
- 提升 AI 输出的可靠性、准确性和格式一致性

[详细文档 →](src/prompt-optimizer/SKILL.md)

### Resume to Web

将 PDF 简历转换为零依赖、动画丰富的交互式单页 HTML 简历网站。通过视觉探索帮助用户发现自己偏好的美学风格。

- 零依赖单文件输出（内联 CSS/JS，无需构建工具）
- 10 种独特风格预设（Midnight Architect、Neon Terminal、Clean Slate 等）
- 滚动触发动画、浮动导航、交互式技能条
- 响应式布局、打印友好、WCAG AA 无障碍支持

[详细文档 →](src/resume-to-web/SKILL.md)

### Resume Screener

基于岗位要求对简历进行系统化评估，采用 10 级评分体系（C → SSS）和 9 维度多角度打分，输出证据驱动的评估报告与录用建议。

- 9 维度评估（教育背景、工作经验、技术技能、项目经验等）
- 支持中英文简历，理解 985/211、BAT/FAANG 等体系
- 硬性要求自动检测与评级封顶机制
- 结构化输出：总评、维度明细、优劣势分析、面试建议

[详细文档 →](src/resume-screener/SKILL.md)

## 快速开始

### 安装

```bash
# 通过 npx skills 安装到项目（推荐）
npx skills add <your-github-username>/skills \
  --skill project-setup prompt-optimizer resume-to-web resume-screener \
  --agent cursor claude-code agents -y

# 或克隆到本地
git clone https://github.com/<your-github-username>/skills.git ~/.cursor/skills-custom
```

### 使用

在 Cursor、Claude Code 或其他支持 Agent Skills 的 AI 编程助手中：

| Skill            | 示例指令                                               |
| ---------------- | ------------------------------------------------------ |
| Project Setup    | "使用 project-setup skill 初始化项目"                  |
| Prompt Optimizer | "使用 prompt-optimizer skill 优化这个提示词：[提示词]" |
| Resume to Web    | "把这份 PDF 简历转成交互式网页"                        |
| Resume Screener  | "用这个 JD 评估这份简历"                               |

## 项目结构

```
skills/
├── README.md
├── src/
│   ├── project-setup/           # 项目设置
│   │   ├── SKILL.md
│   │   └── templates/
│   │       ├── AGENTS.md
│   │       ├── prettier.config.md
│   │       ├── vitest.config.md
│   │       └── next-intl.config.md
│   ├── prompt-optimizer/        # 提示词优化
│   │   ├── SKILL.md
│   │   └── references/
│   │       └── GUIDE.md
│   ├── resume-to-web/           # 简历转网页
│   │   ├── SKILL.md
│   │   ├── scripts/
│   │   │   └── extract_pdf.py
│   │   └── references/
│   │       ├── HTML_ARCHITECTURE.md
│   │       ├── STYLE_PRESETS.md
│   │       └── RESUME_COMPONENTS.md
│   └── resume-screener/         # 简历筛选评估
│       ├── SKILL.md
│       └── references/
│           ├── EVALUATION_DIMENSIONS.md
│           ├── GRADING_RUBRIC.md
│           └── OUTPUT_FORMAT.md
└── .gitignore
```

## 贡献

欢迎提交 Issue 和 Pull Request。

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/amazing-skill`)
3. 提交更改 (`git commit -m 'Add some amazing skill'`)
4. 推送到分支 (`git push origin feature/amazing-skill`)
5. 开启 Pull Request

## 许可证

MIT License

## 相关资源

- [Cursor AI](https://cursor.sh/) - AI-first 代码编辑器
- [Claude Code](https://www.anthropic.com/) - Anthropic 的 AI 编程助手
- [npx skills CLI](https://www.npmjs.com/package/skills) - Skills 安装工具
