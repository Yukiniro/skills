# AI Agent Skills Collection

这是一个精心设计的 AI Agent Skills 集合,旨在提升 AI 编程助手(如 Cursor、Claude Code 等)的工作效率和代码质量。

## 📦 包含的 Skills

### 1. Project Setup

为新项目快速配置开发工具链、代码规范和 AI agent skills。自动探测项目环境并适配宿主项目的包管理器、框架和已有工具链。

**功能特性:**

- 🔍 智能环境探测(包管理器、项目类型、TypeScript)
- 📝 自动生成 AGENTS.md 项目规范文档
- 🎨 配置 Prettier 代码格式化
- 🧪 配置 Vitest 测试框架
- 🤖 安装常用 AI Agent Skills(Vercel React、Frontend Design、shadcn/ui、Vitest)
- 🌍 为 Next.js 项目配置 next-intl 国际化

**使用场景:**

- 初始化新项目的开发环境
- 为现有项目添加标准化工具链
- 配置代码格式化、测试框架和 AI skills
- 为 Next.js 项目配置国际化支持

**详细文档:** [src/project-setup/SKILL.md](src/project-setup/SKILL.md)

### 2. Prompt Optimizer

将模糊或简单的用户提示词转换为高质量、结构化、高性能的 AI 指令。使用系统化优化技术,如 XML 标签、Few-shot 示例和 Chain-of-Thought。

**功能特性:**

- 🧠 基于"AI 作为新员工"理念的系统化提示词优化
- 🏗️ 结构化提示词构建(role、context、task、requirements、output_format)
- 📋 支持 XML 标签、Few-shot 示例、Chain-of-Thought 等高级技术
- ✨ 提升 AI 输出的可靠性、准确性和格式一致性

**使用场景:**

- 优化复杂的 AI 任务指令
- 提升 AI 输出的质量和一致性
- 构建可复用的高质量提示词模板

**详细文档:** [src/prompt-optimizer/SKILL.md](src/prompt-optimizer/SKILL.md)

## 🚀 快速开始

### 安装 Skills

这些 skills 可以通过 `npx skills add` 命令安装到你的项目或全局环境中:

```bash
# 安装到项目级别(推荐)
npx skills add <your-github-username>/skills --skill project-setup prompt-optimizer --agent cursor claude-code agents -y

# 或者克隆仓库到本地
git clone https://github.com/<your-github-username>/skills.git ~/.cursor/skills-custom
```

### 使用 Skills

在 Cursor、Claude Code 或其他支持 Agent Skills 的 AI 编程助手中:

1. **Project Setup**: 在项目根目录说 "使用 project-setup skill 初始化项目"
2. **Prompt Optimizer**: 说 "使用 prompt-optimizer skill 优化这个提示词:[你的提示词]"

## 📁 项目结构

```
skills/
├── README.md                           # 本文件
├── src/
│   ├── project-setup/                  # 项目设置 skill
│   │   ├── SKILL.md                    # Skill 定义和使用说明
│   │   └── templates/                  # 配置模板
│   │       ├── AGENTS.md               # 项目规范模板
│   │       ├── prettier.config.md      # Prettier 配置
│   │       ├── vitest.config.md        # Vitest 配置
│   │       └── next-intl.config.md     # next-intl 配置
│   └── prompt-optimizer/               # 提示词优化 skill
│       ├── SKILL.md                    # Skill 定义和使用说明
│       └── references/
│           └── GUIDE.md                # 优化方法论指南
└── .gitignore
```

## 🤝 贡献

欢迎提交 Issue 和 Pull Request!

如果你有好的 skill 想法或改进建议:

1. Fork 本仓库
2. 创建你的特性分支 (`git checkout -b feature/amazing-skill`)
3. 提交你的更改 (`git commit -m 'Add some amazing skill'`)
4. 推送到分支 (`git push origin feature/amazing-skill`)
5. 开启一个 Pull Request

## 📄 许可证

MIT License

## 🔗 相关资源

- [Cursor AI](https://cursor.sh/) - AI-first 代码编辑器
- [Claude Code](https://www.anthropic.com/) - Anthropic 的 AI 编程助手
- [Agent Skills 规范](https://github.com/cursor-ai/agent-skills) - Agent Skills 官方规范
- [npx skills CLI](https://www.npmjs.com/package/skills) - Skills 安装工具

---

**Made with ❤️ for better AI-assisted development**
