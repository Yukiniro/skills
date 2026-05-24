# Slide Engine Template

整个课件页的 HTML 骨架 + 内联 CSS + 内联 JS。**直接 copy，只修改占位符（`__XXX__`）**，不要重写 JS 逻辑。

## 占位符清单

| 占位符 | 替换为 |
|---|---|
| `__LANG__` | `zh-CN` 或 `en` |
| `__TITLE__` | 课件标题（也用于浏览器标签和封面） |
| `__ACCENT__` | 主色 hex（如 `#E26D5A`） |
| `__ACCENT_SOFT__` | 浅色 hex |
| `__ACCENT_STRONG__` | 深色 hex |
| `__ACCENT_FG__` | 主色上的文字色，一般 `#FFFFFF` |
| `__SOURCE_LABEL__` | 来源（文件名 / 域名 / "本地文件"） |
| `__QUIZ_HREF__` | 测验 HTML 的相对路径（如 `README.quiz.html`） |
| `__SLIDES__` | 所有 `<section class="slide">` 拼接的内容 |
| `__NAV_DOTS__` | 与 slide 数量对应的导航点，每个 slide 一个 `<button class="nav-dot" data-go="N"></button>` |
| `__LABEL_QUIZ_CTA__` | "开始测验 →" / "Start the quiz →" |
| `__LABEL_HELP_TITLE__` | "快捷键" / "Shortcuts" |
| `__LABEL_HELP_*__` | 帮助面板各条文案，见模板内 |

## 完整模板

```html
<!doctype html>
<html lang="__LANG__">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>__TITLE__</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:wght@600;700;800&family=DM+Sans:wght@400;500;700&family=JetBrains+Mono:wght@400;600&family=Noto+Sans+SC:wght@400;500;700&display=swap" rel="stylesheet">
<style>
:root {
  --accent: __ACCENT__;
  --accent-soft: __ACCENT_SOFT__;
  --accent-strong: __ACCENT_STRONG__;
  --accent-fg: __ACCENT_FG__;
  --bg: #FAF7F2;
  --bg-elevated: #FFFFFF;
  --bg-subtle: #F0EBE3;
  --fg: #1F1B16;
  --fg-muted: #6B635A;
  --border: #E5DED1;
  --code-bg: #1E1E2E;
  --code-fg: #CDD6F4;
  --font-display: 'Bricolage Grotesque', 'Noto Sans SC', system-ui, sans-serif;
  --font-body: 'DM Sans', 'Noto Sans SC', system-ui, sans-serif;
  --font-mono: 'JetBrains Mono', 'SF Mono', Consolas, monospace;
  --text-hero: clamp(48px, 7vw, 96px);
  --text-title: clamp(36px, 5vw, 64px);
  --text-subtitle: clamp(20px, 2.5vw, 32px);
  --text-body: clamp(18px, 1.6vw, 24px);
  --text-caption: clamp(14px, 1.2vw, 18px);
  --text-code: clamp(14px, 1.3vw, 20px);
  --space-1: 0.5rem;
  --space-2: 1rem;
  --space-3: 1.5rem;
  --space-4: 2rem;
  --space-6: 3rem;
  --space-8: 4rem;
  --space-12: 6rem;
  --radius-sm: 6px;
  --radius-md: 12px;
  --radius-lg: 20px;
  --radius-pill: 999px;
  --shadow-sm: 0 1px 2px rgba(31, 27, 22, 0.08);
  --shadow-md: 0 4px 16px rgba(31, 27, 22, 0.10);
  --shadow-lg: 0 16px 48px rgba(31, 27, 22, 0.14);
  --ease-out: cubic-bezier(0.16, 1, 0.3, 1);
  --dur-mid: 280ms;
}
@media (prefers-color-scheme: dark) {
  :root {
    --bg: #1A1714;
    --bg-elevated: #25201B;
    --bg-subtle: #2E2823;
    --fg: #F5EFE6;
    --fg-muted: #A8A096;
    --border: #3A332C;
  }
}
* { box-sizing: border-box; }
html, body { margin: 0; padding: 0; height: 100%; overflow: hidden; }
body {
  font-family: var(--font-body);
  color: var(--fg);
  background: var(--bg);
  font-size: var(--text-body);
  line-height: 1.55;
  -webkit-font-smoothing: antialiased;
}

/* ===== Slide Deck Layout ===== */
.deck { position: relative; width: 100vw; height: 100vh; overflow: hidden; }
.slides { display: flex; height: 100%; transition: transform var(--dur-mid) var(--ease-out); will-change: transform; }
.slide {
  flex: 0 0 100vw;
  height: 100vh;
  padding: var(--space-12) var(--space-12);
  display: flex;
  flex-direction: column;
  justify-content: center;
  gap: var(--space-4);
  overflow-y: auto;
  background: var(--bg);
}
.slide:nth-child(even) { background: var(--bg-subtle); }
.slide h1 { font-family: var(--font-display); font-size: var(--text-hero); line-height: 1.05; margin: 0; font-weight: 800; letter-spacing: -0.02em; }
.slide h2 { font-family: var(--font-display); font-size: var(--text-title); line-height: 1.1; margin: 0; font-weight: 700; letter-spacing: -0.01em; }
.slide h3 { font-size: var(--text-subtitle); margin: 0; font-weight: 600; color: var(--fg-muted); }
.slide p { font-size: var(--text-body); margin: 0; max-width: 56ch; }
.slide ul, .slide ol { font-size: var(--text-body); margin: 0; padding-left: 1.5em; max-width: 56ch; }
.slide ul li, .slide ol li { margin-bottom: var(--space-2); }
.slide .lede { font-size: var(--text-subtitle); color: var(--fg-muted); max-width: 50ch; }
.slide .accent { color: var(--accent); }
.slide .source-label { font-size: var(--text-caption); color: var(--fg-muted); text-transform: uppercase; letter-spacing: 0.08em; }

/* ===== Chrome ===== */
.chrome {
  position: fixed;
  bottom: var(--space-3);
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  align-items: center;
  gap: var(--space-3);
  padding: var(--space-1) var(--space-3);
  background: var(--bg-elevated);
  border: 1px solid var(--border);
  border-radius: var(--radius-pill);
  box-shadow: var(--shadow-md);
  z-index: 50;
  font-size: var(--text-caption);
  color: var(--fg-muted);
}
.chrome button {
  background: transparent;
  border: 0;
  color: var(--fg-muted);
  cursor: pointer;
  font-size: 16px;
  padding: 6px 10px;
  border-radius: var(--radius-sm);
  transition: background var(--dur-mid) var(--ease-out), color var(--dur-mid) var(--ease-out);
}
.chrome button:hover { background: var(--bg-subtle); color: var(--fg); }
.chrome .counter { font-variant-numeric: tabular-nums; min-width: 56px; text-align: center; }
.progress {
  position: fixed;
  top: 0; left: 0; right: 0;
  height: 3px;
  background: transparent;
  z-index: 60;
}
.progress > span {
  display: block;
  height: 100%;
  background: var(--accent);
  transform-origin: left;
  transition: transform var(--dur-mid) var(--ease-out);
}

/* ===== Nav Dots ===== */
.nav-dots {
  position: fixed;
  right: var(--space-3);
  top: 50%;
  transform: translateY(-50%);
  display: flex;
  flex-direction: column;
  gap: 10px;
  z-index: 50;
}
.nav-dot {
  width: 8px; height: 8px;
  border-radius: 50%;
  background: var(--border);
  border: 0;
  padding: 0;
  cursor: pointer;
  transition: all var(--dur-mid) var(--ease-out);
}
.nav-dot:hover { background: var(--fg-muted); transform: scale(1.3); }
.nav-dot.is-current { background: var(--accent); transform: scale(1.5); }

/* ===== Overview (Esc) ===== */
.overview {
  position: fixed;
  inset: 0;
  background: var(--bg);
  z-index: 100;
  padding: var(--space-6);
  display: none;
  overflow-y: auto;
}
.overview.is-open { display: block; }
.overview-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: var(--space-3);
}
.overview-card {
  aspect-ratio: 16 / 9;
  background: var(--bg-elevated);
  border: 1px solid var(--border);
  border-radius: var(--radius-md);
  padding: var(--space-3);
  cursor: pointer;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  gap: var(--space-1);
  transition: transform var(--dur-mid) var(--ease-out), box-shadow var(--dur-mid) var(--ease-out);
  position: relative;
}
.overview-card:hover { transform: translateY(-4px); box-shadow: var(--shadow-lg); }
.overview-card .idx { position: absolute; top: 8px; right: 12px; font-size: var(--text-caption); color: var(--fg-muted); font-variant-numeric: tabular-nums; }
.overview-card h2, .overview-card h1 { font-size: 22px; line-height: 1.2; margin: 0; }
.overview-card p { font-size: 13px; color: var(--fg-muted); margin: 0; }

/* ===== Help (?) ===== */
.help {
  position: fixed;
  inset: 0;
  background: rgba(31, 27, 22, 0.4);
  display: none;
  align-items: center;
  justify-content: center;
  z-index: 200;
}
.help.is-open { display: flex; }
.help-card {
  background: var(--bg-elevated);
  padding: var(--space-6);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-lg);
  max-width: 480px;
  width: 90%;
}
.help-card h3 { font-family: var(--font-display); font-size: 24px; margin: 0 0 var(--space-3); }
.help-card dl { margin: 0; display: grid; grid-template-columns: auto 1fr; gap: 12px 24px; align-items: center; }
.help-card dt { font-family: var(--font-mono); background: var(--bg-subtle); padding: 4px 10px; border-radius: var(--radius-sm); font-size: 13px; }
.help-card dd { margin: 0; color: var(--fg-muted); font-size: 14px; }

/* ===== Print (export PDF) ===== */
@media print {
  html, body { overflow: visible; height: auto; }
  .deck, .slides { display: block; height: auto; transform: none !important; }
  .slide { page-break-after: always; height: 100vh; flex: 1 1 100%; padding: 4cm 3cm; }
  .chrome, .nav-dots, .progress, .overview, .help { display: none !important; }
}

/* ===== Reduced motion ===== */
@media (prefers-reduced-motion: reduce) {
  * { transition: none !important; animation: none !important; }
}

/* ===== Quiz CTA in outro ===== */
.quiz-cta {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  background: var(--accent);
  color: var(--accent-fg);
  padding: var(--space-2) var(--space-4);
  font-size: var(--text-subtitle);
  font-weight: 700;
  border-radius: var(--radius-pill);
  text-decoration: none;
  box-shadow: var(--shadow-md);
  transition: transform var(--dur-mid) var(--ease-out), box-shadow var(--dur-mid) var(--ease-out);
  margin-top: var(--space-4);
  width: fit-content;
}
.quiz-cta:hover { transform: translateY(-2px); box-shadow: var(--shadow-lg); }

/* Interactive elements styling lives in INTERACTIVE_ELEMENTS.md — paste those styles after this comment when assembling. */
</style>
</head>
<body>

<div class="progress"><span id="progressBar" style="transform: scaleX(0)"></span></div>

<div class="deck">
  <div class="slides" id="slides">
    __SLIDES__
  </div>
</div>

<div class="nav-dots" id="navDots">
  __NAV_DOTS__
</div>

<div class="chrome">
  <button id="btnPrev" aria-label="Previous">◀</button>
  <span class="counter"><span id="curIdx">1</span> / <span id="totalIdx">1</span></span>
  <button id="btnNext" aria-label="Next">▶</button>
  <button id="btnOverview" aria-label="Overview">▦</button>
  <button id="btnFullscreen" aria-label="Fullscreen">⛶</button>
  <button id="btnHelp" aria-label="Help">?</button>
</div>

<div class="overview" id="overview">
  <div class="overview-grid" id="overviewGrid"></div>
</div>

<div class="help" id="help">
  <div class="help-card">
    <h3>__LABEL_HELP_TITLE__</h3>
    <dl>
      <dt>← →</dt><dd>__LABEL_HELP_PREV_NEXT__</dd>
      <dt>Home / End</dt><dd>__LABEL_HELP_JUMP__</dd>
      <dt>Esc</dt><dd>__LABEL_HELP_OVERVIEW__</dd>
      <dt>F</dt><dd>__LABEL_HELP_FULLSCREEN__</dd>
      <dt>P</dt><dd>__LABEL_HELP_PRINT__</dd>
      <dt>?</dt><dd>__LABEL_HELP_THIS__</dd>
    </dl>
  </div>
</div>

<script>
(function () {
  const slidesEl = document.getElementById('slides');
  const slides = Array.from(slidesEl.querySelectorAll('.slide'));
  const total = slides.length;
  const counterCur = document.getElementById('curIdx');
  const counterTotal = document.getElementById('totalIdx');
  const progressBar = document.getElementById('progressBar');
  const navDotsEl = document.getElementById('navDots');
  const overviewEl = document.getElementById('overview');
  const overviewGrid = document.getElementById('overviewGrid');
  const helpEl = document.getElementById('help');
  let cur = 0;

  counterTotal.textContent = total;

  function clamp(i) { return Math.max(0, Math.min(total - 1, i)); }

  function render() {
    slidesEl.style.transform = `translateX(-${cur * 100}vw)`;
    counterCur.textContent = cur + 1;
    progressBar.style.transform = `scaleX(${(cur + 1) / total})`;
    navDotsEl.querySelectorAll('.nav-dot').forEach((d, i) => {
      d.classList.toggle('is-current', i === cur);
    });
    if (location.hash !== '#' + (cur + 1)) {
      history.replaceState(null, '', '#' + (cur + 1));
    }
  }

  function go(i) { cur = clamp(i); render(); }
  function next() { if (cur < total - 1) go(cur + 1); }
  function prev() { if (cur > 0) go(cur - 1); }

  // Build overview grid lazily on first open
  let overviewBuilt = false;
  function buildOverview() {
    if (overviewBuilt) return;
    slides.forEach((s, i) => {
      const card = document.createElement('div');
      card.className = 'overview-card';
      const head = s.querySelector('h1, h2');
      const sub = s.querySelector('p, .lede');
      card.innerHTML = `
        <span class="idx">${i + 1}</span>
        ${head ? `<h2>${head.textContent.slice(0, 60)}</h2>` : ''}
        ${sub ? `<p>${sub.textContent.slice(0, 80)}</p>` : ''}
      `;
      card.addEventListener('click', () => { go(i); toggleOverview(false); });
      overviewGrid.appendChild(card);
    });
    overviewBuilt = true;
  }
  function toggleOverview(force) {
    const open = force == null ? !overviewEl.classList.contains('is-open') : force;
    if (open) buildOverview();
    overviewEl.classList.toggle('is-open', open);
  }
  function toggleHelp(force) {
    const open = force == null ? !helpEl.classList.contains('is-open') : force;
    helpEl.classList.toggle('is-open', open);
  }

  // Wire up chrome
  document.getElementById('btnPrev').addEventListener('click', prev);
  document.getElementById('btnNext').addEventListener('click', next);
  document.getElementById('btnOverview').addEventListener('click', () => toggleOverview());
  document.getElementById('btnHelp').addEventListener('click', () => toggleHelp());
  document.getElementById('btnFullscreen').addEventListener('click', () => {
    if (!document.fullscreenElement) document.documentElement.requestFullscreen?.();
    else document.exitFullscreen?.();
  });

  // Nav dots delegated
  navDotsEl.addEventListener('click', e => {
    const dot = e.target.closest('.nav-dot');
    if (!dot) return;
    go(parseInt(dot.dataset.go, 10) - 1);
  });

  // Overview backdrop click closes
  overviewEl.addEventListener('click', e => { if (e.target === overviewEl) toggleOverview(false); });
  helpEl.addEventListener('click', e => { if (e.target === helpEl) toggleHelp(false); });

  // Keyboard
  document.addEventListener('keydown', e => {
    if (e.target.matches('input, textarea, select')) return;
    if (overviewEl.classList.contains('is-open')) {
      if (e.key === 'Escape') { toggleOverview(false); e.preventDefault(); }
      return;
    }
    if (helpEl.classList.contains('is-open')) {
      if (e.key === 'Escape' || e.key === '?') { toggleHelp(false); e.preventDefault(); }
      return;
    }
    switch (e.key) {
      case 'ArrowRight': case 'PageDown': case ' ': next(); e.preventDefault(); break;
      case 'ArrowLeft': case 'PageUp': prev(); e.preventDefault(); break;
      case 'Home': go(0); e.preventDefault(); break;
      case 'End': go(total - 1); e.preventDefault(); break;
      case 'Escape': toggleOverview(true); e.preventDefault(); break;
      case 'f': case 'F': document.getElementById('btnFullscreen').click(); break;
      case 'p': case 'P': window.print(); e.preventDefault(); break;
      case '?': toggleHelp(true); e.preventDefault(); break;
    }
  });

  // Touch swipe
  let touchStartX = null;
  document.addEventListener('touchstart', e => { touchStartX = e.changedTouches[0].clientX; }, { passive: true });
  document.addEventListener('touchend', e => {
    if (touchStartX == null) return;
    const dx = e.changedTouches[0].clientX - touchStartX;
    if (Math.abs(dx) > 50) (dx < 0 ? next : prev)();
    touchStartX = null;
  });

  // Init from hash
  const initial = parseInt(location.hash.replace('#', ''), 10);
  if (!isNaN(initial) && initial >= 1 && initial <= total) cur = initial - 1;
  render();
})();
</script>

<!-- Interactive element JS (tooltip, quiz, animation) lives in INTERACTIVE_ELEMENTS.md — paste it after this comment when assembling. -->

</body>
</html>
```

## Slide Section 通用结构

每张 slide 都是这样的：

```html
<section class="slide" data-type="content">
  <!-- 内容 -->
</section>
```

`data-type` 是元数据（`title` / `agenda` / `concept` / `content` / `diagram` / `animation` / `code` / `quiz` / `summary` / `outro`），便于以后扩展样式钩子，目前 CSS 没强依赖。

## 各类型 slide 的内容范例

### `title` — 封面

```html
<section class="slide" data-type="title">
  <span class="source-label">__SOURCE_LABEL__</span>
  <h1>__TITLE__</h1>
  <p class="lede">一句话副标题/导读。</p>
</section>
```

### `agenda` — 目录

```html
<section class="slide" data-type="agenda">
  <h2>本节内容</h2>
  <ol>
    <li>章节一</li>
    <li>章节二</li>
    <li>章节三</li>
  </ol>
</section>
```

### `content` — 普通内容

```html
<section class="slide" data-type="content">
  <h3>章节名</h3>
  <h2>本页的核心观点</h2>
  <ul>
    <li>要点一</li>
    <li>要点二（≤ 3 条，宁少勿多）</li>
    <li>要点三</li>
  </ul>
</section>
```

### `outro` — 结语 + 测验入口

```html
<section class="slide" data-type="outro">
  <h2>课程到此结束 🎉</h2>
  <p class="lede">想看看自己掌握了多少？</p>
  <a class="quiz-cta" href="__QUIZ_HREF__">__LABEL_QUIZ_CTA__</a>
</section>
```

> 其他类型（`concept` / `diagram` / `animation` / `code` / `quiz` / `summary`）的 HTML 片段见 `INTERACTIVE_ELEMENTS.md`。

## 拼接 `__NAV_DOTS__`

为每张 slide 生成一个 dot：

```html
<button class="nav-dot" data-go="1" aria-label="Slide 1"></button>
<button class="nav-dot" data-go="2" aria-label="Slide 2"></button>
<!-- ... -->
```

## 语言标签（zh / en 对照）

| 占位符 | 中文 | 英文 |
|---|---|---|
| `__LABEL_QUIZ_CTA__` | 开始测验 → | Start the quiz → |
| `__LABEL_HELP_TITLE__` | 快捷键 | Shortcuts |
| `__LABEL_HELP_PREV_NEXT__` | 上一页 / 下一页 | Previous / Next |
| `__LABEL_HELP_JUMP__` | 跳到首页 / 末页 | Jump to first / last |
| `__LABEL_HELP_OVERVIEW__` | 总览模式 | Overview grid |
| `__LABEL_HELP_FULLSCREEN__` | 全屏 | Toggle fullscreen |
| `__LABEL_HELP_PRINT__` | 打印 / 导出 PDF | Print / export PDF |
| `__LABEL_HELP_THIS__` | 显示/关闭本面板 | Toggle this panel |
