# Interactive Elements

每种互动元素的 HTML + 配套 CSS/JS。CSS 追加到 SLIDE_ENGINE 的 `<style>` 末尾；JS 追加到 `<script>` 末尾（注意要放在 SLIDE_ENGINE 主 IIFE 之后）。

---

## 1. Tooltip（术语提示）

适合场景：原文里出现的"非常识"术语，第一次出现时加 tooltip。常识词（HTML/API/database）不加。

### HTML

```html
<p>
  机器学习模型的<span class="tip" data-tip="给模型新数据后，预测它没见过的输入。">泛化能力</span>，
  本质上是在<span class="tip" data-tip="一种用噪声扰动训练数据的正则化技巧。">数据增强</span>之后才显现。
</p>
```

### CSS（追加到 `<style>`）

```css
.tip {
  position: relative;
  border-bottom: 2px dotted var(--accent);
  cursor: help;
  font-weight: 500;
}
.tip::after {
  content: attr(data-tip);
  position: absolute;
  bottom: calc(100% + 8px);
  left: 50%;
  transform: translateX(-50%) translateY(4px);
  background: var(--bg-elevated);
  color: var(--fg);
  font-size: var(--text-caption);
  font-weight: 400;
  padding: 10px 14px;
  border-radius: var(--radius-md);
  border: 1px solid var(--border);
  box-shadow: var(--shadow-md);
  width: max-content;
  max-width: 280px;
  white-space: normal;
  line-height: 1.4;
  opacity: 0;
  pointer-events: none;
  transition: opacity var(--dur-mid) var(--ease-out), transform var(--dur-mid) var(--ease-out);
  z-index: 10;
}
.tip:hover::after, .tip:focus::after {
  opacity: 1;
  transform: translateX(-50%) translateY(0);
}
```

（无需 JS，纯 CSS 即可。触屏设备 `:hover` 退化为 tap-focus，需要把 `.tip` 设为可聚焦：`tabindex="0"`。模板里没默认加，必要时手动加。）

---

## 2. Inline Quiz（内嵌小测验）

适合场景：一个概念讲完后立即检验。**这是 slide 内的"轻量测验"**，与第 4 阶段的独立测验 HTML 是两回事。

### HTML — 单选

```html
<section class="slide" data-type="quiz">
  <h3>知识点检验</h3>
  <h2>哪种说法最准确？</h2>
  <form class="iquiz" data-type="single" data-correct="b" data-explain="过拟合是指模型对训练数据记得太死，对新数据反而表现差。">
    <label><input type="radio" name="q" value="a"><span>过拟合让模型在所有数据上都更准</span></label>
    <label><input type="radio" name="q" value="b"><span>过拟合让模型对训练数据极准，但对新数据变差</span></label>
    <label><input type="radio" name="q" value="c"><span>过拟合只出现在小数据集</span></label>
    <button type="submit" class="iquiz-submit">提交</button>
    <p class="iquiz-feedback" hidden></p>
  </form>
</section>
```

### HTML — 多选

```html
<form class="iquiz" data-type="multi" data-correct="a,c" data-explain="a 和 c 是缓解过拟合的常见手段；b 反而会加剧。">
  <label><input type="checkbox" value="a"><span>增大训练集</span></label>
  <label><input type="checkbox" value="b"><span>把模型参数量加 10 倍</span></label>
  <label><input type="checkbox" value="c"><span>引入正则化（L1/L2）</span></label>
  <button type="submit" class="iquiz-submit">提交（多选）</button>
  <p class="iquiz-feedback" hidden></p>
</form>
```

### CSS

```css
.iquiz { display: flex; flex-direction: column; gap: var(--space-2); max-width: 56ch; }
.iquiz label {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  padding: 14px 18px;
  background: var(--bg-elevated);
  border: 1.5px solid var(--border);
  border-radius: var(--radius-md);
  cursor: pointer;
  transition: border-color var(--dur-mid) var(--ease-out), background var(--dur-mid) var(--ease-out);
  font-size: var(--text-body);
}
.iquiz label:hover { border-color: var(--accent-soft); }
.iquiz label.is-correct { border-color: var(--accent); background: var(--accent-soft); }
.iquiz label.is-wrong { border-color: #C84A4A; background: #F8D7D7; }
.iquiz input { margin-top: 6px; accent-color: var(--accent); }
.iquiz-submit {
  align-self: flex-start;
  margin-top: var(--space-2);
  background: var(--accent);
  color: var(--accent-fg);
  border: 0;
  padding: 10px 24px;
  font-size: var(--text-body);
  font-weight: 600;
  border-radius: var(--radius-pill);
  cursor: pointer;
  transition: transform var(--dur-mid) var(--ease-out);
}
.iquiz-submit:hover { transform: translateY(-1px); }
.iquiz-submit:disabled { opacity: 0.5; cursor: not-allowed; transform: none; }
.iquiz-feedback {
  margin: 0;
  padding: 14px 18px;
  border-radius: var(--radius-md);
  font-size: var(--text-caption);
  line-height: 1.5;
}
.iquiz-feedback.is-right { background: var(--accent-soft); color: var(--accent-strong); }
.iquiz-feedback.is-wrong { background: #F8D7D7; color: #8B2C2C; }
```

### JS（追加到模板 `<script>` 主 IIFE 之后）

```javascript
document.querySelectorAll('.iquiz').forEach(form => {
  form.addEventListener('submit', e => {
    e.preventDefault();
    const type = form.dataset.type;
    const correct = form.dataset.correct.split(',').map(s => s.trim());
    const inputs = Array.from(form.querySelectorAll('input'));
    const picked = inputs.filter(i => i.checked).map(i => i.value);
    if (!picked.length) return;
    const isRight = type === 'single'
      ? picked.length === 1 && picked[0] === correct[0]
      : picked.length === correct.length && picked.every(v => correct.includes(v));
    inputs.forEach(i => {
      const label = i.closest('label');
      if (correct.includes(i.value)) label.classList.add('is-correct');
      else if (i.checked) label.classList.add('is-wrong');
      i.disabled = true;
    });
    const fb = form.querySelector('.iquiz-feedback');
    fb.hidden = false;
    fb.classList.add(isRight ? 'is-right' : 'is-wrong');
    fb.textContent = (isRight ? (form.dataset.lang === 'en' ? '✓ Correct. ' : '✓ 答对了。') : (form.dataset.lang === 'en' ? '✗ Not quite. ' : '✗ 还差一点。')) + form.dataset.explain;
    form.querySelector('.iquiz-submit').disabled = true;
  });
});
```

---

## 3. Diagram（SVG 示意图）

提供 4 种结构，按内容选最合适的一种。**不要堆砌**——一页一图，图必须清晰说明一个观点。

### 3.1 流程箭头（左→右）

```html
<section class="slide" data-type="diagram">
  <h2>请求是如何流转的</h2>
  <svg class="dia-flow" viewBox="0 0 1000 200" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="请求流程图">
    <g font-family="var(--font-body)" font-size="18" text-anchor="middle">
      <rect x="40" y="60" width="180" height="80" rx="12" fill="var(--bg-elevated)" stroke="var(--border)"/>
      <text x="130" y="105" fill="var(--fg)">用户</text>
      <path d="M 230 100 H 310" stroke="var(--accent)" stroke-width="2" marker-end="url(#arr)"/>
      <rect x="320" y="60" width="180" height="80" rx="12" fill="var(--bg-elevated)" stroke="var(--border)"/>
      <text x="410" y="105" fill="var(--fg)">前端</text>
      <path d="M 510 100 H 590" stroke="var(--accent)" stroke-width="2" marker-end="url(#arr)"/>
      <rect x="600" y="60" width="180" height="80" rx="12" fill="var(--bg-elevated)" stroke="var(--border)"/>
      <text x="690" y="105" fill="var(--fg)">API</text>
      <path d="M 790 100 H 870" stroke="var(--accent)" stroke-width="2" marker-end="url(#arr)"/>
      <rect x="880" y="60" width="100" height="80" rx="12" fill="var(--accent)" stroke="none"/>
      <text x="930" y="105" fill="var(--accent-fg)">DB</text>
    </g>
    <defs>
      <marker id="arr" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto">
        <path d="M0,0 L10,5 L0,10 z" fill="var(--accent)"/>
      </marker>
    </defs>
  </svg>
</section>
```

### 3.2 对比双栏（左 vs 右）

```html
<svg class="dia-compare" viewBox="0 0 1000 360" xmlns="http://www.w3.org/2000/svg">
  <g font-family="var(--font-body)">
    <rect x="40" y="40" width="440" height="280" rx="16" fill="var(--bg-elevated)" stroke="var(--border)"/>
    <text x="260" y="80" text-anchor="middle" font-size="22" font-weight="700" fill="var(--fg)">传统方式</text>
    <text x="260" y="160" text-anchor="middle" font-size="16" fill="var(--fg-muted)">• 全量加载</text>
    <text x="260" y="200" text-anchor="middle" font-size="16" fill="var(--fg-muted)">• 单点故障</text>
    <text x="260" y="240" text-anchor="middle" font-size="16" fill="var(--fg-muted)">• 难以扩展</text>
    <rect x="520" y="40" width="440" height="280" rx="16" fill="var(--accent-soft)" stroke="var(--accent)" stroke-width="2"/>
    <text x="740" y="80" text-anchor="middle" font-size="22" font-weight="700" fill="var(--accent-strong)">新方式</text>
    <text x="740" y="160" text-anchor="middle" font-size="16" fill="var(--fg)">• 按需加载</text>
    <text x="740" y="200" text-anchor="middle" font-size="16" fill="var(--fg)">• 自动容灾</text>
    <text x="740" y="240" text-anchor="middle" font-size="16" fill="var(--fg)">• 水平扩展</text>
  </g>
</svg>
```

### 3.3 层级树（树状结构）

```html
<svg class="dia-tree" viewBox="0 0 1000 360" xmlns="http://www.w3.org/2000/svg">
  <g font-family="var(--font-body)" font-size="16" text-anchor="middle">
    <rect x="430" y="20" width="140" height="60" rx="10" fill="var(--accent)" stroke="none"/>
    <text x="500" y="55" fill="var(--accent-fg)" font-weight="700">根</text>
    <path d="M 500 80 L 200 160" stroke="var(--border)" stroke-width="2"/>
    <path d="M 500 80 L 500 160" stroke="var(--border)" stroke-width="2"/>
    <path d="M 500 80 L 800 160" stroke="var(--border)" stroke-width="2"/>
    <rect x="120" y="160" width="160" height="50" rx="8" fill="var(--bg-elevated)" stroke="var(--border)"/>
    <text x="200" y="190" fill="var(--fg)">子节点 A</text>
    <rect x="420" y="160" width="160" height="50" rx="8" fill="var(--bg-elevated)" stroke="var(--border)"/>
    <text x="500" y="190" fill="var(--fg)">子节点 B</text>
    <rect x="720" y="160" width="160" height="50" rx="8" fill="var(--bg-elevated)" stroke="var(--border)"/>
    <text x="800" y="190" fill="var(--fg)">子节点 C</text>
  </g>
</svg>
```

### 3.4 关系网（圆 + 连线，适合"概念之间的联系"）

```html
<svg class="dia-net" viewBox="0 0 1000 400" xmlns="http://www.w3.org/2000/svg">
  <g font-family="var(--font-body)" font-size="15" text-anchor="middle">
    <path d="M 500 80 L 200 320 M 500 80 L 800 320 M 200 320 L 800 320" stroke="var(--border)" stroke-width="2"/>
    <circle cx="500" cy="80" r="56" fill="var(--accent)"/>
    <text x="500" y="86" fill="var(--accent-fg)" font-weight="700">概念 1</text>
    <circle cx="200" cy="320" r="56" fill="var(--bg-elevated)" stroke="var(--accent)" stroke-width="2"/>
    <text x="200" y="326" fill="var(--fg)">概念 2</text>
    <circle cx="800" cy="320" r="56" fill="var(--bg-elevated)" stroke="var(--accent)" stroke-width="2"/>
    <text x="800" y="326" fill="var(--fg)">概念 3</text>
  </g>
</svg>
```

### CSS

```css
.dia-flow, .dia-compare, .dia-tree, .dia-net {
  width: 100%;
  height: auto;
  max-height: 60vh;
  display: block;
}
```

> SVG 里的 `var(--accent)` 等 CSS 变量会直接生效，无需额外脚本。

---

## 4. Animation（微动画）

最常用的就两种：**入场动画**（slide 进入视口时元素逐条出现）和 **数据流动**（沿路径运动）。每张片最多一个，避免眩晕。

### 4.1 逐条入场（list reveal）

```html
<section class="slide" data-type="animation">
  <h2>三步搞定</h2>
  <ul class="reveal-list">
    <li>第一步：明确目标</li>
    <li>第二步：制定计划</li>
    <li>第三步：复盘迭代</li>
  </ul>
</section>
```

CSS：

```css
.reveal-list li {
  opacity: 0;
  transform: translateY(12px);
  transition: opacity 480ms var(--ease-out), transform 480ms var(--ease-out);
}
.slide.is-active .reveal-list li {
  opacity: 1;
  transform: translateY(0);
}
.slide.is-active .reveal-list li:nth-child(1) { transition-delay: 100ms; }
.slide.is-active .reveal-list li:nth-child(2) { transition-delay: 300ms; }
.slide.is-active .reveal-list li:nth-child(3) { transition-delay: 500ms; }
.slide.is-active .reveal-list li:nth-child(4) { transition-delay: 700ms; }
```

JS（追加，给当前 slide 标记 `.is-active`）：

```javascript
// 监听 slides 容器 transform 完成，给当前 slide 加 is-active
(function () {
  const slidesEl = document.getElementById('slides');
  const slides = Array.from(slidesEl.querySelectorAll('.slide'));
  function markActive() {
    const idx = Math.round(Math.abs(parseFloat(getComputedStyle(slidesEl).transform.split(',')[4] || 0)) / window.innerWidth);
    slides.forEach((s, i) => s.classList.toggle('is-active', i === idx));
  }
  // 首次
  markActive();
  // 翻页时
  new MutationObserver(markActive).observe(slidesEl, { attributes: true, attributeFilter: ['style'] });
})();
```

### 4.2 沿路径运动（packet flow）

```html
<svg class="dia-flow" viewBox="0 0 1000 200" xmlns="http://www.w3.org/2000/svg">
  <!-- 复用流程箭头的 rect/path -->
  <circle r="8" fill="var(--accent)">
    <animateMotion dur="3s" repeatCount="indefinite" path="M 130 100 L 410 100 L 690 100 L 930 100"/>
  </circle>
</svg>
```

---

## 5. Callout（提示框）

```html
<aside class="callout callout-tip">
  <strong>💡 小贴士</strong>
  <p>这里放一段补充说明，长度控制在 2 行内。</p>
</aside>

<aside class="callout callout-warn">
  <strong>⚠️ 注意</strong>
  <p>这里强调一个容易踩的坑。</p>
</aside>

<aside class="callout callout-note">
  <strong>📝 备注</strong>
  <p>背景信息，看与不看都不影响主线。</p>
</aside>
```

CSS：

```css
.callout {
  padding: var(--space-2) var(--space-3);
  border-radius: var(--radius-md);
  border-left: 4px solid var(--accent);
  background: var(--bg-elevated);
  max-width: 56ch;
}
.callout strong { font-size: var(--text-caption); display: block; margin-bottom: 4px; color: var(--fg-muted); text-transform: uppercase; letter-spacing: 0.06em; }
.callout p { margin: 0; font-size: var(--text-body); }
.callout-tip { border-left-color: var(--accent); }
.callout-warn { border-left-color: #D97706; background: #FEF3C7; color: #78350F; }
.callout-note { border-left-color: var(--fg-muted); }
@media (prefers-color-scheme: dark) {
  .callout-warn { background: #2D2317; color: #FCD34D; }
}
```

---

## 6. Code with Explanation（双栏代码）

```html
<section class="slide" data-type="code">
  <h2>关键代码片段</h2>
  <div class="code-pair">
    <pre><code>def fib(n):
    if n &lt;= 1:
        return n
    return fib(n - 1) + fib(n - 2)</code></pre>
    <div class="code-explain">
      <p><strong>这段代码做了什么？</strong></p>
      <p>计算斐波那契数列第 n 项。它<em>自己调用自己</em>，每次问题缩小一点，直到落到最小情况。</p>
    </div>
  </div>
</section>
```

CSS：

```css
.code-pair {
  display: grid;
  grid-template-columns: 1.2fr 1fr;
  gap: var(--space-3);
  align-items: start;
}
.code-pair pre {
  background: var(--code-bg);
  color: var(--code-fg);
  padding: var(--space-3);
  border-radius: var(--radius-md);
  overflow-x: auto;
  font-family: var(--font-mono);
  font-size: var(--text-code);
  line-height: 1.55;
  margin: 0;
}
.code-explain {
  font-size: var(--text-body);
  background: var(--bg-elevated);
  padding: var(--space-3);
  border-radius: var(--radius-md);
  border: 1px solid var(--border);
}
.code-explain p { margin: 0 0 var(--space-2); }
.code-explain p:last-child { margin-bottom: 0; }
@media (max-width: 900px) {
  .code-pair { grid-template-columns: 1fr; }
}
```

---

## 7. Concept Card（概念卡片）

```html
<section class="slide" data-type="concept">
  <h3>核心概念</h3>
  <h2><span class="accent">闭包</span></h2>
  <p class="lede">一个函数<strong>"记住"</strong>了它被定义时所处的环境，即使在那个环境消失之后。</p>
  <ul>
    <li>它捕获的不是值，而是变量本身</li>
    <li>这就是 JS 模块化和私有变量的基础</li>
  </ul>
</section>
```

不需要额外 CSS——用模板里已有的 `h2` / `.lede` / `ul` 样式即可。

---

## 组装小结

写每张 slide 时按这个流程：
1. 选 `data-type` → 从本文件取 HTML 片段
2. 替换文案
3. 如果用到 quiz / animation，确认 JS 段已追加到模板 `<script>` 末尾（避免重复）
4. 如果用到 tooltip / callout，确认对应 CSS 段已追加到模板 `<style>` 末尾
