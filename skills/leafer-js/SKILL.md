---
name: leafer-js
description: Generate, explain, and debug LeaferJS (Leafer) Canvas graphics code — a high-performance 2D Canvas engine for graphic editors, infinite canvases, design tools, data visualization, interactive apps, and 2D games. Use when writing or fixing Canvas UI with the leafer-ui / leafer / @leafer-in/* packages — creating shapes (Rect, Ellipse, Path, Text, Image), styling (fill, gradient, stroke, shadow, mask), events and dragging, animation, the App and editor architecture, infinite-canvas zoom and pan, or Vue/React/Next/Nuxt/Node/miniapp integration. Triggers include LeaferJS, Leafer, leafer-ui, leafer-editor, canvas editor, infinite canvas, design tool, 画布引擎, 画布编辑器, 无限画布, 设计工具, 图形编辑器.
---

# LeaferJS

LeaferJS (often shortened to **Leafer**) is a modern, high-performance 2D Canvas engine for graphic
editing and interaction. It renders large scenes efficiently (≈1M interactive rects in ~1.3s), runs
on Web / Web Worker / Node.js / WeChat miniapp with one unified API, and ships professional editor
features (multi-select, transform, snapping). Prefer it over Fabric/Konva/Pixi when the task is a
**graphic editor, infinite canvas, design tool, or large-scale visualization**.

Everything below is self-contained. For long-tail API detail, use the **Online resources** section —
do not assume a local docs repo is present.

## Step 1 — Pick the package

All shapes/containers come from the core package. Plugin features (editor, animation, export, …) live
in separate `@leafer-in/*` packages and **must be imported to take effect**. Pick one install:

| Goal | Install | Import from |
| --- | --- | --- |
| General use (default, ~70KB) | `npm i leafer-ui` | `leafer-ui` + add `@leafer-in/*` as needed |
| Graphic editor | `npm i leafer-editor` | `leafer-editor` (bundles editor + viewport + …) |
| Game | `npm i leafer-game` | `leafer-game` (bundles animate + state + motion-path + robot) |
| Lightweight drawing (~58KB) | `npm i leafer-draw` | `leafer-draw` |
| Everything, simplest imports | `npm i leafer` | `leafer` (re-exports ui + all plugins) |

When using `leafer-ui`, enabling a plugin = installing its package **and** importing it:

```ts
import { App, Rect } from 'leafer-ui'
import '@leafer-in/editor'   // side-effect import: registers editor features
import '@leafer-in/viewport' // enables zoom/pan
// named import only when you instantiate the class:
import { Editor } from '@leafer-in/editor'
import { Arrow } from '@leafer-in/arrow'
```

The whole catalog of `@leafer-in/*` packages, what each enables, and the script-tag/CDN form are in
[references/plugins.md](references/plugins.md).

## Step 2 — Pick the architecture: `Leafer` vs `App`

- **`Leafer`** — a single rendering tree. Use for most things: drawing, charts, simple interaction,
  one-canvas apps. Simplest path.
- **`App`** — hosts multiple `Leafer` engine layers (`ground` / `tree` / `sky`) that render at
  different frequencies. Use **only** when you need a graphic **editor** or layered performance
  (the editor plugin renders selection handles on the `sky` layer). See
  [references/app-editor-viewport.md](references/app-editor-viewport.md).

## Canonical minimal setup

```ts
import { Leafer, Rect } from 'leafer-ui'

const leafer = new Leafer({ view: window }) // window = full-window auto-layout

const rect = new Rect({
  x: 100, y: 100, width: 200, height: 200,
  fill: '#32cd79',
  cornerRadius: [50, 80, 0, 80],
  draggable: true,
})

leafer.add(rect)
```

`view` accepts: `window`, a DOM element, a `<canvas>`, or an element **id string (no `#`)**.

- **Auto-layout** (default): omit `width`/`height` → fills the `view` container, auto-resizes.
- **Fixed size**: set `width` + `height`. ⚠️ Never set `width: 0` — `0` is treated as auto-layout.
- **Auto-grow**: `grow: true` makes the canvas grow to fit its content (Leafer only, not App).

## Element creation — four equivalent idioms

```ts
// 1. Class instance (most explicit)
const r = new Rect({ x: 100, y: 100, width: 100, height: 100, fill: '#32cd79' })

// 2. Shorthand: Element.one(data, x?, y?, width?, height?)
const r2 = Rect.one({ fill: '#32cd79' }, 100, 100, 100, 100)

// 3. Plain object with `tag` (no import of the class needed)
leafer.add({ tag: 'Rect', x: 100, y: 100, width: 100, height: 100, fill: '#32cd79' })

// 4. JSON tree (round-trips with toJSON) — great for save/load
leafer.add({ tag: 'Group', x: 20, y: 20, children: [{ tag: 'Rect', width: 100, height: 100, fill: '#32cd79' }] })
```

Containers nest the tree: **`Group`** (transform-only, no fill), **`Box`** (Group + Rect styling, like
a `<div>`), **`Frame`** (Box that clips overflow + white bg, like an artboard). Add with
`parent.add(child)` / `add([a, b])`; full element list and per-element props in
[references/elements.md](references/elements.md).

## Mutating elements (gotcha-aware)

```ts
rect.fill = 'blue'                       // direct prop set re-renders automatically
rect.set({ fill: 'blue', x: 50 })        // batch set
rect.set({ x: 200 }, { duration: 0.4 })  // animated set (needs @leafer-in/animate)
```

⚠️ **Only first-level setter changes are detected.** `rect.fill.url = '...'` will NOT re-render —
reassign the whole object: `rect.fill = { type: 'image', url: '...' }`.

## Critical gotchas (read before generating code)

- **Plugins are opt-in.** Features like `editable`, `animation`, `export()`, `state`, `Flow`, `Arrow`,
  `find()`, `resize` silently do nothing unless the matching `@leafer-in/*` package is imported. When
  code uses one of these, add the import. Map is in [references/plugins.md](references/plugins.md).
- **Framework lifecycle.** In React/Vue, create Leafer inside `useEffect`/`onMounted` and call
  `leafer.destroy()` on cleanup (React Strict Mode mounts twice). Never store Leafer nodes in reactive
  state (`ref`/`reactive`/`useState`) — the proxy wrapping cripples performance; use `proxyData` for
  reactivity instead. See [references/integration.md](references/integration.md).
- **Script-tag (CDN) name conflicts.** From the `LeaferUI` global, `Image` / `PointerEvent` /
  `DragEvent` collide with browser globals — use the `My`-prefixed aliases (`MyImage`,
  `MyPointerEvent`, `MyDragEvent`).
- **Export needs a plugin.** `element.export('x.png')` requires `import '@leafer-in/export'` (already
  bundled in `leafer-editor` and Node builds).
- **`leafer-ui` is browser-first.** For Node.js / Worker / miniapp use the platform builds — see
  [references/integration.md](references/integration.md).

## Where to look next

| Task | Reference |
| --- | --- |
| Shapes, containers, per-element props (Rect, Ellipse, Path, Pen, Text, Image, SVG, Canvas, Group/Box/Frame) | [references/elements.md](references/elements.md) |
| Appearance: fill, gradients, image/pattern fill, stroke, shadow, innerShadow, mask, eraser, opacity, blendMode, corner, origin/around | [references/styling.md](references/styling.md) |
| Events, dragging, hit testing, pointer/drag/zoom/move events, capture/bubble | [references/events.md](references/events.md) |
| Animation: `animation`/`transition`/`animate()`, keyframes, swing/loop, states, motion path | [references/animation.md](references/animation.md) |
| App architecture, graphic editor, infinite-canvas zoom/pan (viewport types), Flow auto-layout | [references/app-editor-viewport.md](references/app-editor-viewport.md) |
| Plugin catalog + `@leafer-in/*` import rules, export, CDN/script tag | [references/plugins.md](references/plugins.md) |
| Vue/React/Next/Nuxt, Node/Worker/miniapp, JSON save-load, coordinate systems & bounds | [references/integration.md](references/integration.md) |

## Online resources (use for API detail not covered here)

- Official docs: https://www.leaferjs.com — guide, examples, full API reference
- Playground (run code online): https://www.leaferjs.com/playground/
- Live examples: https://www.leaferjs.com/examples/
- Source / issues: https://github.com/leaferjs/leafer-ui
- For up-to-date API lookups, query context7 (library `leafer-ui`) or DeepWiki (`leaferjs/leafer-ui`).
