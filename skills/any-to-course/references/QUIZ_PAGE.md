# Quiz Page Template

测验页是一个完全独立的 HTML 文件。所有题目都是 **选择题**（单选 + 多选）。直接 copy 下面的模板，只改占位符和题目 JSON，不要重写 JS 逻辑。

## 占位符清单

| 占位符 | 替换为 |
|---|---|
| `__LANG__` | `zh-CN` 或 `en` |
| `__TITLE__` | 测验标题，建议 `<课件标题> · 测验` / `<Course Title> · Quiz` |
| `__ACCENT__` / `__ACCENT_SOFT__` / `__ACCENT_STRONG__` / `__ACCENT_FG__` | 与课件保持一致的主题色 |
| `__SOURCE_LABEL__` | 来源（文件名 / 域名） |
| `__COURSE_HREF__` | 课件 HTML 的相对路径（如 `README.course.html`） |
| `__QUIZ_JSON__` | 题目 JSON，见下方 schema |
| `__LABEL_BACK_TO_COURSE__` | "← 返回课件" / "← Back to course" |
| `__LABEL_SUBMIT__` | "交卷" / "Submit" |
| `__LABEL_RETRY_WRONG__` | "重做错题" / "Retry wrong only" |
| `__LABEL_RETRY_ALL__` | "全部重做" / "Retry all" |
| `__LABEL_SCORE__` | "得分" / "Score" |
| `__LABEL_CORRECT_RATE__` | "正确率" / "Accuracy" |
| `__LABEL_RESULT_TITLE__` | "结果" / "Results" |
| `__LABEL_PROGRESS__` | "已答 {done} / 共 {total}" / "Answered {done} of {total}" |
| `__LABEL_MULTI_HINT__` | "（多选）" / "(multiple)" |
| `__LABEL_FROM_SLIDE__` | "→ 见课件第 {n} 页" / "→ See slide {n}" |

## 题目 JSON Schema

```json
{
  "title": "课件标题 · 测验",
  "lang": "zh-CN",
  "questions": [
    {
      "id": "q1",
      "type": "single",
      "stem": "下面哪个最准确地描述了 X？",
      "options": [
        { "key": "a", "text": "选项 A" },
        { "key": "b", "text": "选项 B" },
        { "key": "c", "text": "选项 C" },
        { "key": "d", "text": "选项 D" }
      ],
      "answer": ["b"],
      "explain": "B 正确的原因是……A 看起来对，但忽略了……",
      "from_slide": 4
    },
    {
      "id": "q2",
      "type": "multi",
      "stem": "下面哪些做法可以缓解 Y？",
      "options": [
        { "key": "a", "text": "做法 A" },
        { "key": "b", "text": "做法 B" },
        { "key": "c", "text": "做法 C" },
        { "key": "d", "text": "做法 D" }
      ],
      "answer": ["a", "c"],
      "explain": "A 和 C 都正确。B 是反作用，D 与问题无关。"
    }
  ]
}
```

- `type`：只允许 `single` 或 `multi`
- `answer`：永远是数组；single 长度 1，multi 长度 ≥ 2
- `from_slide`：可选，如果填了就在解析里追加链接
- `explain`：必填，答完后展示

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
<link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:wght@600;700;800&family=DM+Sans:wght@400;500;700&family=Noto+Sans+SC:wght@400;500;700&display=swap" rel="stylesheet">
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
  --danger: #C84A4A;
  --danger-soft: #F8D7D7;
  --font-display: 'Bricolage Grotesque', 'Noto Sans SC', system-ui, sans-serif;
  --font-body: 'DM Sans', 'Noto Sans SC', system-ui, sans-serif;
  --quiz-text-title: clamp(28px, 3vw, 42px);
  --quiz-text-question: clamp(18px, 1.6vw, 22px);
  --quiz-text-option: clamp(16px, 1.4vw, 18px);
  --radius-md: 12px;
  --radius-lg: 20px;
  --radius-pill: 999px;
  --shadow-sm: 0 1px 2px rgba(31, 27, 22, 0.08);
  --shadow-md: 0 4px 16px rgba(31, 27, 22, 0.10);
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
    --danger-soft: #3A1C1C;
  }
}
* { box-sizing: border-box; }
html, body { margin: 0; padding: 0; }
body {
  font-family: var(--font-body);
  background: var(--bg);
  color: var(--fg);
  line-height: 1.55;
  -webkit-font-smoothing: antialiased;
}

.topbar {
  position: sticky;
  top: 0;
  z-index: 50;
  background: rgba(250, 247, 242, 0.92);
  backdrop-filter: saturate(180%) blur(12px);
  border-bottom: 1px solid var(--border);
}
@media (prefers-color-scheme: dark) {
  .topbar { background: rgba(26, 23, 20, 0.92); }
}
.topbar-inner {
  max-width: 880px;
  margin: 0 auto;
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 14px 24px;
  font-size: 14px;
}
.topbar a {
  color: var(--fg-muted);
  text-decoration: none;
  transition: color var(--dur-mid) var(--ease-out);
}
.topbar a:hover { color: var(--accent); }
.topbar .source {
  color: var(--fg-muted);
  text-transform: uppercase;
  letter-spacing: 0.06em;
  font-size: 12px;
  flex: 1;
  text-align: center;
}
.topbar .progress-text {
  color: var(--fg-muted);
  font-variant-numeric: tabular-nums;
}
.progress-track {
  height: 3px;
  background: var(--border);
  position: relative;
}
.progress-track > span {
  position: absolute;
  inset: 0 auto 0 0;
  background: var(--accent);
  transform: scaleX(0);
  transform-origin: left;
  transition: transform var(--dur-mid) var(--ease-out);
  display: block;
}

main {
  max-width: 760px;
  margin: 0 auto;
  padding: 48px 24px 120px;
}
h1.quiz-title {
  font-family: var(--font-display);
  font-size: var(--quiz-text-title);
  margin: 0 0 8px;
  line-height: 1.15;
  letter-spacing: -0.01em;
}
.quiz-meta {
  color: var(--fg-muted);
  margin: 0 0 40px;
  font-size: 14px;
}

.q-card {
  background: var(--bg-elevated);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  padding: 28px 32px;
  margin-bottom: 24px;
  box-shadow: var(--shadow-sm);
}
.q-card .stem {
  font-size: var(--quiz-text-question);
  font-weight: 600;
  margin: 0 0 4px;
  line-height: 1.4;
}
.q-card .stem .multi-hint { color: var(--accent); font-weight: 500; font-size: 0.85em; margin-left: 6px; }
.q-card .q-index {
  color: var(--fg-muted);
  font-size: 13px;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  margin: 0 0 14px;
}

.q-options { display: flex; flex-direction: column; gap: 10px; margin-top: 18px; list-style: none; padding: 0; }
.q-option label {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  padding: 14px 18px;
  background: var(--bg);
  border: 1.5px solid var(--border);
  border-radius: var(--radius-md);
  cursor: pointer;
  font-size: var(--quiz-text-option);
  line-height: 1.45;
  transition: border-color var(--dur-mid) var(--ease-out), background var(--dur-mid) var(--ease-out);
}
.q-option label:hover { border-color: var(--accent-soft); }
.q-option input { margin-top: 5px; accent-color: var(--accent); flex-shrink: 0; }
.q-option .key { font-family: var(--font-display); font-weight: 700; color: var(--fg-muted); width: 18px; flex-shrink: 0; text-transform: uppercase; }

.q-card.graded .q-option label { cursor: default; }
.q-card.graded .q-option.is-correct label { border-color: var(--accent); background: var(--accent-soft); color: var(--accent-strong); }
.q-card.graded .q-option.is-wrong label { border-color: var(--danger); background: var(--danger-soft); color: #8B2C2C; }
.q-card.graded input { pointer-events: none; }

.q-explain {
  margin-top: 18px;
  padding: 16px 20px;
  background: var(--bg-subtle);
  border-radius: var(--radius-md);
  font-size: 15px;
  line-height: 1.6;
  display: none;
}
.q-explain a { color: var(--accent); text-decoration: none; }
.q-explain a:hover { text-decoration: underline; }
.q-card.graded .q-explain { display: block; }
.q-explain .verdict { font-weight: 700; margin-right: 6px; }
.q-explain .verdict.is-right { color: var(--accent-strong); }
.q-explain .verdict.is-wrong { color: var(--danger); }

.actions {
  position: sticky;
  bottom: 0;
  margin: 0 -24px;
  padding: 16px 24px;
  background: linear-gradient(to top, var(--bg) 70%, transparent);
  display: flex;
  justify-content: center;
  gap: 12px;
}
.btn {
  font: 600 16px/1 var(--font-body);
  padding: 14px 28px;
  border-radius: var(--radius-pill);
  border: 1.5px solid transparent;
  cursor: pointer;
  transition: transform var(--dur-mid) var(--ease-out), box-shadow var(--dur-mid) var(--ease-out);
}
.btn-primary { background: var(--accent); color: var(--accent-fg); box-shadow: var(--shadow-md); }
.btn-primary:hover { transform: translateY(-2px); }
.btn-primary:disabled { opacity: 0.4; cursor: not-allowed; transform: none; }
.btn-ghost { background: transparent; color: var(--fg); border-color: var(--border); }
.btn-ghost:hover { background: var(--bg-elevated); }

.result {
  background: var(--bg-elevated);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  padding: 32px;
  margin-bottom: 32px;
  text-align: center;
  display: none;
  box-shadow: var(--shadow-md);
}
.result.is-shown { display: block; }
.result h2 { font-family: var(--font-display); margin: 0 0 16px; font-size: 32px; }
.result .score-row { display: flex; justify-content: center; gap: 48px; margin-top: 18px; }
.result .score-cell { text-align: center; }
.result .score-num { font-family: var(--font-display); font-size: 56px; line-height: 1; color: var(--accent); font-weight: 800; }
.result .score-label { font-size: 13px; color: var(--fg-muted); text-transform: uppercase; letter-spacing: 0.08em; margin-top: 8px; }

@media (prefers-reduced-motion: reduce) {
  * { transition: none !important; animation: none !important; }
}
</style>
</head>
<body>

<header class="topbar">
  <div class="topbar-inner">
    <a href="__COURSE_HREF__">__LABEL_BACK_TO_COURSE__</a>
    <span class="source">__SOURCE_LABEL__</span>
    <span class="progress-text" id="progressText">0 / 0</span>
  </div>
  <div class="progress-track"><span id="progressBar"></span></div>
</header>

<main>
  <h1 class="quiz-title" id="quizTitle">__TITLE__</h1>
  <p class="quiz-meta" id="quizMeta"></p>

  <div class="result" id="result"></div>
  <div id="questions"></div>

  <div class="actions">
    <button class="btn btn-primary" id="btnSubmit" disabled>__LABEL_SUBMIT__</button>
    <button class="btn btn-ghost" id="btnRetryWrong" hidden>__LABEL_RETRY_WRONG__</button>
    <button class="btn btn-ghost" id="btnRetryAll" hidden>__LABEL_RETRY_ALL__</button>
  </div>
</main>

<script id="quiz-data" type="application/json">
__QUIZ_JSON__
</script>

<script>
(function () {
  const LABELS = {
    submit: '__LABEL_SUBMIT__',
    retryWrong: '__LABEL_RETRY_WRONG__',
    retryAll: '__LABEL_RETRY_ALL__',
    score: '__LABEL_SCORE__',
    rate: '__LABEL_CORRECT_RATE__',
    resultTitle: '__LABEL_RESULT_TITLE__',
    progressTpl: '__LABEL_PROGRESS__',
    multiHint: '__LABEL_MULTI_HINT__',
    fromSlide: '__LABEL_FROM_SLIDE__',
  };
  const data = JSON.parse(document.getElementById('quiz-data').textContent);
  const STORAGE_KEY = 'any-to-course:quiz:' + location.pathname;
  const isEN = (data.lang || '__LANG__').startsWith('en');
  const verdictRight = isEN ? '✓ Correct.' : '✓ 答对了。';
  const verdictWrong = isEN ? '✗ Not quite.' : '✗ 还差一点。';
  const courseHref = '__COURSE_HREF__';

  const root = document.getElementById('questions');
  const btnSubmit = document.getElementById('btnSubmit');
  const btnRetryWrong = document.getElementById('btnRetryWrong');
  const btnRetryAll = document.getElementById('btnRetryAll');
  const resultEl = document.getElementById('result');
  const progressBar = document.getElementById('progressBar');
  const progressText = document.getElementById('progressText');

  let state = loadState();
  let visibleIds = data.questions.map(q => q.id); // for "retry wrong" filtering

  function loadState() {
    try { return JSON.parse(localStorage.getItem(STORAGE_KEY)) || { answers: {}, submitted: false }; }
    catch { return { answers: {}, submitted: false }; }
  }
  function saveState() {
    try { localStorage.setItem(STORAGE_KEY, JSON.stringify(state)); } catch {}
  }

  function setEqual(a, b) {
    if (a.length !== b.length) return false;
    const sa = [...a].sort().join('|'), sb = [...b].sort().join('|');
    return sa === sb;
  }

  function questionsToRender() {
    return data.questions.filter(q => visibleIds.includes(q.id));
  }

  function render() {
    root.innerHTML = '';
    const qs = questionsToRender();
    qs.forEach((q, i) => {
      const card = document.createElement('section');
      card.className = 'q-card';
      card.dataset.qid = q.id;
      const isMulti = q.type === 'multi';
      const inputType = isMulti ? 'checkbox' : 'radio';
      const stemHTML = `${escapeHTML(q.stem)}${isMulti ? `<span class="multi-hint">${LABELS.multiHint}</span>` : ''}`;
      card.innerHTML = `
        <p class="q-index">${i + 1} / ${qs.length}</p>
        <p class="stem">${stemHTML}</p>
        <ul class="q-options"></ul>
        <div class="q-explain"></div>
      `;
      const ul = card.querySelector('.q-options');
      q.options.forEach(opt => {
        const li = document.createElement('li');
        li.className = 'q-option';
        li.dataset.key = opt.key;
        li.innerHTML = `
          <label>
            <input type="${inputType}" name="${q.id}" value="${opt.key}">
            <span class="key">${opt.key.toUpperCase()}</span>
            <span>${escapeHTML(opt.text)}</span>
          </label>
        `;
        ul.appendChild(li);
      });
      // Restore answers
      const picked = state.answers[q.id] || [];
      ul.querySelectorAll('input').forEach(inp => {
        if (picked.includes(inp.value)) inp.checked = true;
        inp.addEventListener('change', () => onAnswerChange(q));
      });
      root.appendChild(card);
    });
    if (state.submitted) gradeAll(false);
    updateProgress();
  }

  function onAnswerChange(q) {
    const card = root.querySelector(`.q-card[data-qid="${q.id}"]`);
    const picked = Array.from(card.querySelectorAll('input:checked')).map(i => i.value);
    state.answers[q.id] = picked;
    saveState();
    updateProgress();
  }

  function updateProgress() {
    const qs = questionsToRender();
    const done = qs.filter(q => (state.answers[q.id] || []).length > 0).length;
    progressBar.style.transform = `scaleX(${qs.length ? done / qs.length : 0})`;
    progressText.textContent = LABELS.progressTpl
      .replace('{done}', done).replace('{total}', qs.length);
    btnSubmit.disabled = done < qs.length || state.submitted;
  }

  function gradeAll(persist = true) {
    let right = 0;
    const wrongIds = [];
    const qs = questionsToRender();
    qs.forEach(q => {
      const card = root.querySelector(`.q-card[data-qid="${q.id}"]`);
      const picked = state.answers[q.id] || [];
      const isRight = setEqual(picked, q.answer);
      if (isRight) right += 1; else wrongIds.push(q.id);
      card.classList.add('graded');
      card.querySelectorAll('.q-option').forEach(li => {
        const key = li.dataset.key;
        if (q.answer.includes(key)) li.classList.add('is-correct');
        else if (picked.includes(key)) li.classList.add('is-wrong');
      });
      const ex = card.querySelector('.q-explain');
      const verdictHTML = isRight
        ? `<span class="verdict is-right">${verdictRight}</span>`
        : `<span class="verdict is-wrong">${verdictWrong}</span>`;
      const slideRef = q.from_slide
        ? ` <a href="${courseHref}#${q.from_slide}">${LABELS.fromSlide.replace('{n}', q.from_slide)}</a>`
        : '';
      ex.innerHTML = `${verdictHTML}${escapeHTML(q.explain)}${slideRef}`;
    });
    if (persist) {
      state.submitted = true;
      state.lastWrongIds = wrongIds;
      saveState();
    }
    showResult(right, qs.length, wrongIds);
    btnSubmit.disabled = true;
    btnRetryAll.hidden = false;
    btnRetryWrong.hidden = wrongIds.length === 0;
  }

  function showResult(right, total, wrongIds) {
    const pct = Math.round((right / total) * 100);
    resultEl.innerHTML = `
      <h2>${LABELS.resultTitle}</h2>
      <div class="score-row">
        <div class="score-cell">
          <div class="score-num">${right}<span style="font-size:24px;color:var(--fg-muted)">/${total}</span></div>
          <div class="score-label">${LABELS.score}</div>
        </div>
        <div class="score-cell">
          <div class="score-num">${pct}%</div>
          <div class="score-label">${LABELS.rate}</div>
        </div>
      </div>
    `;
    resultEl.classList.add('is-shown');
    resultEl.scrollIntoView({ behavior: 'smooth', block: 'start' });
  }

  function retryAll() {
    state = { answers: {}, submitted: false };
    saveState();
    visibleIds = data.questions.map(q => q.id);
    resultEl.classList.remove('is-shown');
    btnRetryAll.hidden = true;
    btnRetryWrong.hidden = true;
    render();
  }
  function retryWrong() {
    const wrongIds = state.lastWrongIds || [];
    if (!wrongIds.length) return;
    visibleIds = wrongIds;
    wrongIds.forEach(id => { delete state.answers[id]; });
    state.submitted = false;
    saveState();
    resultEl.classList.remove('is-shown');
    btnRetryAll.hidden = true;
    btnRetryWrong.hidden = true;
    render();
  }

  function escapeHTML(s) {
    return String(s).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  }

  btnSubmit.addEventListener('click', () => gradeAll(true));
  btnRetryAll.addEventListener('click', retryAll);
  btnRetryWrong.addEventListener('click', retryWrong);

  document.getElementById('quizMeta').textContent = isEN
    ? `${data.questions.length} questions`
    : `共 ${data.questions.length} 题`;

  render();
})();
</script>

</body>
</html>
```

## 出题 QA 自检（生成后必须过一遍）

- [ ] 每题都有 `type`、`stem`、`options`（≥3 个）、`answer`（数组）、`explain`
- [ ] `single` 题 `answer` 长度恰好 1；`multi` 题 `answer` 长度 ≥ 2
- [ ] `multi` 题干末尾不要手动加"（多选）"——模板会自动渲染
- [ ] 干扰项"像但不对"，避免出现"显然是凑数"的选项
- [ ] 没有出现"以上都对/都不对"这种偷懒选项
- [ ] 解析至少回答了"为什么对 / 为什么其他不对"中的一个
- [ ] 如果有 `from_slide`，slide 编号必须真实存在
- [ ] 全部题目语言一致（与课件 `__LANG__` 一致）

## 语言标签对照

| 占位符 | 中文 | 英文 |
|---|---|---|
| `__LABEL_BACK_TO_COURSE__` | ← 返回课件 | ← Back to course |
| `__LABEL_SUBMIT__` | 交卷 | Submit |
| `__LABEL_RETRY_WRONG__` | 重做错题 | Retry wrong only |
| `__LABEL_RETRY_ALL__` | 全部重做 | Retry all |
| `__LABEL_SCORE__` | 得分 | Score |
| `__LABEL_CORRECT_RATE__` | 正确率 | Accuracy |
| `__LABEL_RESULT_TITLE__` | 结果 | Results |
| `__LABEL_PROGRESS__` | 已答 {done} / 共 {total} | Answered {done} of {total} |
| `__LABEL_MULTI_HINT__` | （多选） | (multiple) |
| `__LABEL_FROM_SLIDE__` | → 见课件第 {n} 页 | → See slide {n} |
