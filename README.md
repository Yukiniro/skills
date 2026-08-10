# AI Agent Skills Collection

A curated set of AI Agent Skills to boost productivity and code quality for AI coding assistants (Cursor, Claude Code, etc.).

## Included Skills

### Project Setup

Quickly configure development toolchains, code standards, and AI agent skills for new projects. Automatically detects the project environment and adapts to the host project's package manager, framework, and existing toolchain.

- Smart environment detection (package manager, project type, TypeScript)
- Auto-generate AGENTS.md project conventions document
- Configure Prettier code formatting and Vitest test framework
- Install popular AI Agent Skills (Vercel React, Frontend Design, shadcn/ui, Vitest)
- Configure next-intl internationalization for Next.js projects

[Documentation →](skills/project-setup/SKILL.md)

```bash
npx skills add https://github.com/Yukiniro/skills --skill project-setup
```

### Setup AGENTS.md

Create or update a reusable engineering-principles section in `AGENTS.md` without replacing its existing content.

- Preserves the original document and changes only its engineering-principles section
- Prefers simple complete solutions, modular design, existing dependencies, and mature libraries
- Uses `SKILL.md` as the single source of truth, avoiding a duplicate template

[Documentation →](skills/setup-agents-md/SKILL.md)

```bash
npx skills add https://github.com/Yukiniro/skills --skill setup-agents-md
```

### Prompt Optimizer

Transform vague or simple user prompts into high-quality, structured AI instructions. Uses systematic optimization techniques like XML tagging, few-shot examples, and Chain-of-Thought.

- Systematic prompt optimization based on the "AI as a New Employee" philosophy
- Structured prompt construction (role, context, task, requirements, output_format)
- Improve reliability, accuracy, and format consistency of AI outputs

[Documentation →](skills/prompt-optimizer/SKILL.md)

```bash
npx skills add https://github.com/Yukiniro/skills --skill prompt-optimizer
```

### Frontend Resume

Convert PDF resumes into zero-dependency, animation-rich interactive single-page HTML resume websites. Help users discover their preferred aesthetic through visual exploration.

- Zero-dependency single-file output (inline CSS/JS, no build tools)
- 10 distinctive style presets (Midnight Architect, Neon Terminal, Clean Slate, etc.)
- Scroll-triggered animations, floating navigation, interactive skill bars
- Responsive layout, print-friendly, WCAG AA accessibility support

[Documentation →](skills/frontend-resume/SKILL.md)

```bash
npx skills add https://github.com/Yukiniro/skills --skill frontend-resume
```

### Resume Screener

Systematically evaluate resumes against job requirements using a 10-level grading system (C → SSS) with 9-dimension multi-angle scoring, producing evidence-driven evaluation reports and hiring recommendations.

- 9-dimension evaluation (education, work experience, technical skills, project experience, etc.)
- Supports Chinese and English resumes, understands 985/211, BAT/FAANG systems
- Hard requirement detection with grade capping mechanism
- Structured output: overall rating, dimension details, strengths/weaknesses analysis, interview suggestions

[Documentation →](skills/resume-screener/SKILL.md)

```bash
npx skills add https://github.com/Yukiniro/skills --skill resume-screener
```

### Work Weekly Report

Generate structured weekly work summaries from daily work logs. Groups work by project/topic instead of by day, extracting objective facts with categorized dimensions.

- Group by project/topic, not chronological order
- Objective facts only — no subjective evaluations
- Categorize by dimension (Business/Feature, Technical/Infrastructure, Data/Research)
- Supports bilingual output (Chinese/English)

[Documentation →](skills/work-weekly-report/SKILL.md)

```bash
npx skills add https://github.com/Yukiniro/skills --skill work-weekly-report
```

### Smart Commit

Automatically analyze git changes and create Conventional Commits with Chinese descriptions. Fully automatic — analyzes diff, determines type, generates message, and commits without confirmation.

- Conventional Commits format: `type(scope): 中文描述`
- Auto type detection (feat, fix, docs, refactor, perf, test, build, ci, style, chore, revert)
- Smart staging: uses existing staged changes or stages all if empty
- Concise Chinese commit descriptions (under 50 characters)
- Sensitive file detection (`.env`, credentials) — warns and blocks commit
- Respects pre-commit hooks (no `--no-verify`)

[Documentation →](skills/smart-commit/SKILL.md)

```bash
npx skills add https://github.com/Yukiniro/skills --skill smart-commit
```

### Squash Commits

Squash all commits on the current feature branch (relative to main/master) into a single clean commit while preserving the branch name. Includes safety checks, user confirmation, and smart commit message generation.

- Auto-detect main branch (main/master)
- Safety checks: clean working directory, not on main, >=2 commits required
- Smart commit message with all original messages as bullet points
- Post-squash guidance (force-push reminder)
- Bilingual triggers (English + Chinese)

[Documentation →](skills/squash-commits/SKILL.md)

```bash
npx skills add https://github.com/Yukiniro/skills --skill squash-commits
```

### Deep Code Analysis

Systematically analyze and understand code logic and business requirements. Follows a "measure first, understand second, act last" principle with a 6-step workflow.

- 6-step workflow: scope → measure → structure → trace logic → design intent → present
- Size-based strategy: direct analysis (<50KB), module-by-module (50-500KB), parallel sub-agents (>500KB)
- Multiple trace modes: business logic, data flow, call chain
- Focused on understanding only — no review, no development, no refactoring
- Bilingual triggers (English + Chinese)

[Documentation →](skills/deep-code-analysis/SKILL.md)

```bash
npx skills add https://github.com/Yukiniro/skills --skill deep-code-analysis
```

### Any to Course

Turn a local text file (MD/TXT) or a web URL into two standalone single-page HTML files: a **slide-based courseware** (arrow-key navigation, fullscreen presenting) + a companion **multiple-choice quiz** (submit, see explanations for wrong answers, retry).

- Two artifacts: `<name>.course.html` + `<name>.quiz.html`
- Slide engine: keyboard nav, overview grid, URL hash memory, print-to-PDF
- Full interactivity: inline quizzes, SVG diagrams, term tooltips, entrance animations, callouts
- Quiz is all single/multiple-choice with "retry wrong / retry all", state persisted to localStorage
- Zero runtime deps single HTML (Google Fonts CDN only), open with a double-click
- Output language follows input (Chinese in → Chinese out, English in → English out)

[Documentation →](skills/any-to-course/SKILL.md)

```bash
npx skills add https://github.com/Yukiniro/skills --skill any-to-course
```

### LeaferJS

Generate, explain, and debug LeaferJS (Leafer) Canvas graphics code — a high-performance 2D Canvas engine for graphic editors, infinite canvases, design tools, and data visualization. Distilled from the official LeaferJS docs into a lean, self-contained skill (no source repo required).

- Package selection (leafer-ui / leafer-editor / leafer-game / leafer) and the `@leafer-in/*` plugin import rules
- Core patterns: shapes & containers, fill/gradient/stroke/shadow/mask styling, events & dragging, animation & states
- App architecture, graphic editor, infinite-canvas zoom/pan, Flow auto-layout
- Vue/React/Next/Nuxt/Node/miniapp integration, JSON save-load, coordinate systems
- 7 on-demand reference files keep SKILL.md lean; long-tail API points to leaferjs.com

[Documentation →](skills/leafer-js/SKILL.md)

```bash
npx skills add https://github.com/Yukiniro/skills --skill leafer-js
```

## Installation

Install all skills at once:

```bash
npx skills add https://github.com/Yukiniro/skills \
  --skill project-setup setup-agents-md prompt-optimizer frontend-resume resume-screener work-weekly-report smart-commit squash-commits deep-code-analysis any-to-course leafer-js
```

Or install a specific skill:

```bash
npx skills add https://github.com/Yukiniro/skills --skill frontend-resume
```

## Usage

In Cursor, Claude Code, or any AI coding assistant that supports Agent Skills:

| Skill              | Example Prompt                                              |
| ------------------ | ----------------------------------------------------------- |
| Project Setup      | "Use the project-setup skill to initialize my project"      |
| Setup AGENTS.md    | "Create or update AGENTS.md with engineering principles"   |
| Prompt Optimizer   | "Use the prompt-optimizer skill to optimize this prompt: …" |
| Frontend Resume    | "Convert this PDF resume into an interactive web page"      |
| Resume Screener    | "Evaluate this resume against this job description"         |
| Work Weekly Report | "Generate a weekly report from these daily logs"            |
| Smart Commit       | "提交代码" or "Commit my changes"                           |
| Squash Commits     | "Squash all commits on this branch into one" / "压缩提交"  |
| Deep Code Analysis | "Analyze this module" / "帮我理解这个业务逻辑"              |
| Any to Course      | "把这篇文章做成课件" / "Turn this URL into slides"          |
| LeaferJS           | "Build a canvas editor with LeaferJS" / "用 Leafer 做无限画布" |

## Creating Custom Skills

Use [template/SKILL.md](template/SKILL.md) as a starting template:

```markdown
---
name: my-skill-name
description: A clear description of what this skill does and when to use it.
---

# My Skill Name

[Add your instructions here]
```

The frontmatter requires only two fields:

- `name` — A unique identifier for the skill (lowercase, hyphen-separated)
- `description` — A clear description of what the skill does and when to use it

For more information, see [How to create custom skills](https://support.claude.com/en/articles/12512198-creating-custom-skills).

## Project Structure

```
skills/
├── .claude-plugin/
│   └── marketplace.json        # Claude Code Plugin marketplace config
├── skills/
│   ├── project-setup/          # Project setup
│   │   ├── SKILL.md
│   │   ├── LICENSE.txt
│   │   └── templates/
│   │       ├── AGENTS.md
│   │       ├── prettier.config.md
│   │       ├── vitest.config.md
│   │       └── next-intl.config.md
│   ├── setup-agents-md/        # Create or update AGENTS.md
│   │   ├── SKILL.md
│   │   ├── agents/
│   │   │   └── openai.yaml
│   ├── prompt-optimizer/       # Prompt optimization
│   │   ├── SKILL.md
│   │   ├── LICENSE.txt
│   │   └── references/
│   │       └── GUIDE.md
│   ├── frontend-resume/         # Frontend resume
│   │   ├── SKILL.md
│   │   ├── LICENSE.txt
│   │   ├── scripts/
│   │   │   └── extract_pdf.py
│   │   └── references/
│   │       ├── HTML_ARCHITECTURE.md
│   │       ├── STYLE_PRESETS.md
│   │       └── RESUME_COMPONENTS.md
│   ├── resume-screener/        # Resume screening & evaluation
│   │   ├── SKILL.md
│   │   ├── LICENSE.txt
│   │   └── references/
│   │       ├── EVALUATION_DIMENSIONS.md
│   │       ├── GRADING_RUBRIC.md
│   │       └── OUTPUT_FORMAT.md
│   ├── work-weekly-report/     # Weekly report generation
│   │   └── SKILL.md
│   ├── smart-commit/           # Auto git commit with Chinese messages
│   │   └── SKILL.md
│   ├── squash-commits/         # Git commit squashing
│   │   └── SKILL.md
│   ├── deep-code-analysis/    # Deep code & business logic analysis
│   │   └── SKILL.md
│   ├── any-to-course/          # Turn any text/URL into a slide course + quiz
│   │   ├── SKILL.md
│   │   ├── LICENSE.txt
│   │   └── references/
│   │       ├── SLIDE_ENGINE.md
│   │       ├── INTERACTIVE_ELEMENTS.md
│   │       ├── QUIZ_PAGE.md
│   │       ├── DESIGN_SYSTEM.md
│   │       └── CONTENT_PHILOSOPHY.md
│   └── leafer-js/              # LeaferJS canvas engine code generation
│       ├── SKILL.md
│       └── references/
│           ├── elements.md
│           ├── styling.md
│           ├── events.md
│           ├── animation.md
│           ├── app-editor-viewport.md
│           ├── plugins.md
│           └── integration.md
├── template/
│   └── SKILL.md                # New skill creation template
├── .gitignore
├── LICENSE
└── README.md
```

## Contributing

Issues and Pull Requests are welcome.

1. Fork this repository
2. Create a feature branch (`git checkout -b feature/amazing-skill`)
3. Commit your changes (`git commit -m 'Add some amazing skill'`)
4. Push to the branch (`git push origin feature/amazing-skill`)
5. Open a Pull Request

## License

MIT License

## Resources

- [Agent Skills Spec](https://agentskills.io/) - The Agent Skills standard specification
- [Cursor AI](https://cursor.sh/) - AI-first code editor
- [Claude Code](https://www.anthropic.com/) - Anthropic's AI coding assistant
- [npx skills CLI](https://www.npmjs.com/package/skills) - Skills installation tool
