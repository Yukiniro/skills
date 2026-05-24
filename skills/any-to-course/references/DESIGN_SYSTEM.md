# Design System

课件和测验页共用一套设计 token，确保视觉统一。模板里已经把这些 token 定义为 CSS 变量，不要手写颜色/字号，统一用 `var(--xxx)` 引用。

## 调色板（Palettes）

提供 4 套主题色，每套都包含 `light` / `dark` 两个模式。生成时挑一套贴合内容主题的：

- **Vermillion**（默认，通用）`#E26D5A` — 暖珊瑚红，适合人文/产品/通用内容
- **Teal** `#2A9D8F` — 青绿，适合技术/工程/科学
- **Mustard** `#E0A93B` — 芥末黄，适合金融/商业/历史
- **Indigo** `#5B5BD6` — 靛蓝，适合 AI/数据/未来话题

替换模板里 `__ACCENT__` 时，对应的 4 个变量都要换：

```css
--accent: #E26D5A;          /* 主色 */
--accent-soft: #F2C7BE;     /* 浅色背景 / hover */
--accent-strong: #B84A38;   /* 深色 / active */
--accent-fg: #FFFFFF;       /* 主色上的文字 */
```

## 中性色（Neutrals）

不要用纯白（#FFF）和纯黑（#000），用带暖意的：

```css
/* Light mode */
--bg: #FAF7F2;              /* off-white，主背景 */
--bg-elevated: #FFFFFF;     /* 卡片背景 */
--bg-subtle: #F0EBE3;       /* 弱化区域 */
--fg: #1F1B16;              /* 主文字 */
--fg-muted: #6B635A;        /* 次要文字 */
--border: #E5DED1;          /* 描边 */
--code-bg: #1E1E2E;         /* 代码块底（Catppuccin） */
--code-fg: #CDD6F4;

/* Dark mode（@media prefers-color-scheme: dark） */
--bg: #1A1714;
--bg-elevated: #25201B;
--bg-subtle: #2E2823;
--fg: #F5EFE6;
--fg-muted: #A8A096;
--border: #3A332C;
```

## 字体（Typography）

通过 Google Fonts 加载，`<link>` 放 `<head>`：

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:wght@600;700;800&family=DM+Sans:wght@400;500;700&family=JetBrains+Mono:wght@400;600&family=Noto+Sans+SC:wght@400;500;700&display=swap" rel="stylesheet">
```

CSS：

```css
--font-display: 'Bricolage Grotesque', 'Noto Sans SC', system-ui, sans-serif;
--font-body: 'DM Sans', 'Noto Sans SC', system-ui, sans-serif;
--font-mono: 'JetBrains Mono', 'SF Mono', Consolas, monospace;
```

中文环境下 display 字体回退到 Noto Sans SC，避免英文 display 字体撑不住中文字形。

## 字号（Type Scale）

**幻灯片专属——比常规网页大得多**：

```css
--text-hero: clamp(48px, 7vw, 96px);     /* title 页大标题 */
--text-title: clamp(36px, 5vw, 64px);    /* 每张片的标题 */
--text-subtitle: clamp(20px, 2.5vw, 32px);
--text-body: clamp(18px, 1.6vw, 24px);   /* 正文要点 */
--text-caption: clamp(14px, 1.2vw, 18px);
--text-code: clamp(14px, 1.3vw, 20px);
```

**测验页字号偏小、更紧凑**：

```css
--quiz-text-title: clamp(28px, 3vw, 42px);
--quiz-text-question: clamp(18px, 1.6vw, 22px);
--quiz-text-option: clamp(16px, 1.4vw, 18px);
```

## 间距（Spacing）

8px 基准网格：

```css
--space-1: 0.5rem;   /* 8px */
--space-2: 1rem;     /* 16px */
--space-3: 1.5rem;   /* 24px */
--space-4: 2rem;     /* 32px */
--space-6: 3rem;     /* 48px */
--space-8: 4rem;     /* 64px */
--space-12: 6rem;    /* 96px */
```

幻灯片内边距至少 `var(--space-8)`，让内容呼吸。

## 圆角与阴影

```css
--radius-sm: 6px;
--radius-md: 12px;
--radius-lg: 20px;
--radius-pill: 999px;

--shadow-sm: 0 1px 2px rgba(31, 27, 22, 0.08);
--shadow-md: 0 4px 16px rgba(31, 27, 22, 0.10);
--shadow-lg: 0 16px 48px rgba(31, 27, 22, 0.14);
```

阴影用暖色调（带 `rgba(31, 27, 22, ...)`），不要用纯黑阴影。

## 动效

```css
--ease-out: cubic-bezier(0.16, 1, 0.3, 1);
--ease-in-out: cubic-bezier(0.65, 0, 0.35, 1);
--dur-fast: 160ms;
--dur-mid: 280ms;
--dur-slow: 520ms;
```

**必须**写 `@media (prefers-reduced-motion: reduce)`，把所有 transition/animation 时间归零或改为可接受的极短值。

## 视觉哲学

- 暖、克制、有文人气；不要赛博朋克、不要紫色渐变、不要"AI slop"
- 大标题 + 大留白 + 一个强调色，永远比花哨配色更有质感
- 卡片用阴影分层，不要靠粗描边
- 代码块永远 dark，即使页面是 light 主题——保持 IDE 熟悉感
