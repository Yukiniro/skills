---
name: any-to-course
description: Turn a local text file (MD/TXT) or a web URL into a single-page HTML slide-style course that's ready to present and teach from, plus a companion multiple-choice quiz HTML for post-class self-test. Both outputs are self-contained single HTML files with inline CSS/JS (only Google Fonts CDN). The course includes a slide engine (arrow-key navigation, fullscreen, overview, print-to-PDF), embedded quizzes, micro-animations, term tooltips, and SVG diagrams. Use whenever the user wants to convert an article, doc, blog post, README, lecture notes, or any reading material into a presentable courseware / slide deck for teaching, sharing, or self-study. Triggers on phrases like "把这篇文章做成课件", "做成 PPT", "做成幻灯片", "生成课件", "turn this into a course", "make a slide deck from this URL", "presentable course from this markdown", "build a slide course".
---

# Any-to-Course

把一份 **本地文本文件（MD/TXT）** 或一个 **网页 URL** 的内容，转换成两个独立的单页 HTML 文件：

1. **课件**（`<name>.course.html`）— 幻灯片模式，一屏一页，左右键翻页，包含动画、tooltip、SVG 示意图、内嵌小测验
2. **配套测验**（`<name>.quiz.html`）— 全部为选择题（单选 + 多选），答完可一键交卷查看总分和错题解析

两份产物都是 **零运行时依赖** 的单 HTML（仅允许 Google Fonts CDN），双击即可在浏览器打开，方便分享、演示、自学。

## Core Principles

1. **Self-contained** — 所有 CSS/JS 内联，唯一外链是 Google Fonts。把 HTML 拷给任何人都能直接打开。
2. **Language follows source** — 中文输入 → 中文课件；英文输入 → 英文课件。绝不混杂。
3. **Show, don't tell** — 一页一观点、宁少勿多。把长段落提炼成 3 条以内要点，不要把原文塞进幻灯片。
4. **Presentable** — 不只是好看，是真的能拿去线下/线上演讲。键盘可控、可全屏、可打印导出 PDF。
5. **Self-test ready** — 测验页独立存在、可单独分发。题目要"考概念理解"而不是"考字面记忆"。

---

## Phase 0 — 识别输入

判断用户给的是哪种来源：

| 输入形态 | 处理方式 |
|---|---|
| `.md` / `.markdown` / `.txt` 本地文件 | 直接 `Read` |
| URL（`http://` / `https://`） | 优先调用 `defuddle` skill 抓取为干净 markdown；失败则降级 `WebFetch` |
| PDF / DOCX / PPTX / HTML 等其他格式 | **明确拒绝**，告诉用户 `any-to-course` 仅支持 MD/TXT/URL，建议先用 `defuddle` 或 `read` 转成 MD 再来 |

读到内容后，**先扫一遍前 200 字判断主语言**（中文字符占比 ≥ 30% → 中文，否则英文）。把这个判断作为后续所有文案、提示、按钮文字的语言。

如果用户没指定输出路径：
- 本地文件输入 → 与输入同目录，`<input-basename>.course.html` + `<input-basename>.quiz.html`
- URL 输入 → 当前工作目录，`<slugified-title>.course.html` + `<slugified-title>.quiz.html`

---

## Phase 1 — 内容分析

不要急着写 HTML，先把原文消化成结构化数据（在脑子里 / 草稿区都行）：

- **元信息**：标题、副标题、作者/来源、原文链接
- **章节树**：H1/H2/H3 层级
- **关键概念**：值得 tooltip 解释的术语（≥ 3 个，不要把常识词如 "HTML"、"API" 都加上，那是噪音）
- **代码块 / 引用 / 列表 / 表格 / 数据**：哪些适合做 `code` 类型 slide，哪些适合做 `diagram`
- **知识检验点**：哪些段落讲完后适合插一道小测验（概念定义后、流程梳理后、对比讲完后）
- **可视化候选**：原文里描述的"流程 / 对比 / 关系 / 层级"，都可以做成 SVG 示意图或微动画

---

## Phase 2 — 课件大纲设计

**总片数 6–15 张**：

| 原文长度 | 建议片数 |
|---|---|
| < 1500 字 | 6–8 张 |
| 1500–5000 字 | 8–12 张 |
| > 5000 字 | 12–15 张（必要时做二级合并，绝不超过 20 张） |

**幻灯片类型菜单**（不是每张都要用，按需选）：

- `title` — 封面（标题/副标题/来源）
- `agenda` — 目录页
- `concept` — 概念定义（含 tooltip 高亮）
- `content` — 普通内容页（要点 + 视觉强调）
- `diagram` — SVG 示意图（流程/对比/关系/层级）
- `animation` — 微动画页（步骤展开、数据流动）
- `code` — 代码 + 解释（双栏）
- `quiz` — 内嵌小测验（单选或多选）
- `summary` — 章节小结
- `outro` — 结语 + 「开始测验 →」按钮

**强制至少包含**：1 个 `title` + 1 个 `agenda` + 1 个 `diagram` + 1 个内嵌 `quiz` + ≥3 个 tooltip 术语 + 1 个 `outro`。

**不要把大纲拿出来跟用户对**，直接出结果。用户想改的话他会说。

---

## Phase 3 — 生成课件 HTML（产物 1）

按以下顺序读 reference 并组装：

1. 读 `references/DESIGN_SYSTEM.md` → 拿到色板、字体、间距 token
2. 读 `references/SLIDE_ENGINE.md` → 拿到 HTML 骨架 + slide 引擎的内联 CSS/JS（**完整 copy，不要重写**）
3. 读 `references/INTERACTIVE_ELEMENTS.md` → 按需取每种 slide 类型的 HTML 片段
4. 读 `references/CONTENT_PHILOSOPHY.md` → 在写每张片的文案时遵循

替换模板里的占位符：
- `__LANG__` → `zh-CN` 或 `en`
- `__TITLE__` → 课件标题
- `__ACCENT__` → 从 DESIGN_SYSTEM 提供的 palette 里挑一个，写入 `--accent` CSS 变量
- `__SLIDES__` → 所有 slide `<section>` 拼接
- `__QUIZ_HREF__` → 配套测验 HTML 的相对路径（用于 `outro` 页按钮）
- `__SOURCE_LABEL__` → 来源信息（文件名 / URL）

**单 HTML 输出，CSS/JS 全部内联**。Google Fonts 用 `<link>`，其他一概禁止。

---

## Phase 4 — 生成配套测验 HTML（产物 2）

**所有题目都是选择题**，只有两种题型：单选（radio）、多选（checkbox）。不引入填空、判断、拖拽。

读 `references/QUIZ_PAGE.md` 拿到模板，然后：

1. 出题规模：
   - 短文 → 8–10 题
   - 中等 → 10–15 题
   - 长文 → 15–20 题
2. 题目质量原则（**重要**）：
   - 考"概念理解 / 应用判断"，不考"字面背诵"
   - 干扰项要"像但不对"，不要瞎写明显错的
   - 单选题正确答案只有 1 个；多选题正确答案 ≥ 2 个，要在题干注明「（多选）」
   - 每题必须配一句简短解析（answered 后才展示）
   - 可选字段 `from_slide`（课件第 N 张），如果有就在解析里显示「→ 见课件第 N 页」
3. 题目按课件章节顺序均匀分布
4. 题目数据以 JSON 形式内联在 HTML 顶部：
   ```html
   <script id="quiz-data" type="application/json">
   { "title": "...", "lang": "zh-CN", "questions": [ … ] }
   </script>
   ```
5. 交互（模板已实现，不要重写逻辑）：
   - 顶部进度条
   - 默认"先做完再统一交卷"模式
   - 提交后展示总分、正确率、错题清单 + 解析
   - 「重做错题」「全部重做」按钮
   - 答题状态 `localStorage` 持久化，刷新不丢

替换占位符：
- `__LANG__` / `__TITLE__` / `__ACCENT__` / `__SOURCE_LABEL__`
- `__COURSE_HREF__` → 课件 HTML 的相对路径（返回课件按钮用）
- `__QUIZ_JSON__` → 题目 JSON

---

## Phase 5 — 打开并复盘

```bash
open <name>.course.html
open <name>.quiz.html
```

向用户简短汇报：
- 课件做了几张片，包含哪些 slide 类型
- 测验出了几道单选 / 几道多选
- 两份文件保存在哪里

然后请用户给反馈。**不要主动列改进清单**，让用户先看再说。

---

## Reference 索引

按需读取，不要一次全部加载：

| 文件 | 何时读 | 作用 |
|---|---|---|
| `references/DESIGN_SYSTEM.md` | Phase 3 开头 | 色板、字体、间距、暗色模式 token |
| `references/SLIDE_ENGINE.md` | Phase 3 | 课件 HTML 骨架 + slide 引擎完整代码（不要重写） |
| `references/INTERACTIVE_ELEMENTS.md` | Phase 3 写各类 slide 时 | quiz / tooltip / diagram / animation / callout 的 HTML 片段 |
| `references/QUIZ_PAGE.md` | Phase 4 | 测验页完整 HTML 模板（不要重写） |
| `references/CONTENT_PHILOSOPHY.md` | Phase 2–4 写文案时 | 内容密度、术语选择、测验设题原则 |

---

## 常见失误（避免）

- 把原文整段直接搬上幻灯片 → 每页 ≤ 3 个要点，长段落必须提炼
- 强行加测验 / tooltip 凑数 → 数量是下限不是配额，质量优先
- 出题靠"复述原文" → 改成"理解后判断"
- 课件和测验语言不一致 → 两份产物的语言必须一致，且严格跟随输入
- 重写 SLIDE_ENGINE / QUIZ_PAGE 里的 JS 逻辑 → 直接 copy，只改数据
- 在 outro 忘了放「开始测验」按钮 → 这是课件 → 测验的唯一入口，必须有
