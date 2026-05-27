# App architecture, graphic editor, infinite canvas & auto-layout

This is the "design tool / infinite canvas / editor" workflow — Leafer's headline use case.

## App: multi-layer engine

`App` hosts several `Leafer` engine layers that render independently. Conventional layers:

| Layer | Role |
| --- | --- |
| `ground` | bottom (background, grid) — optional |
| `tree` | middle, main content (like `<body>`) |
| `sky` | top (changing content, e.g. editor selection handles) |

```ts
import { App, Leafer, Frame, Rect } from 'leafer-ui'

const app = new App({
  view: window,
  fill: '#333',
  tree: { type: 'design' },   // create the tree layer (with a design viewport)
  sky: {},                    // create the sky layer
})
app.tree.add(Rect.one({ fill: '#FEB027' }, 100, 100, 200, 200))
```
Or add layers manually: `app.add(app.tree = new Leafer({ type: 'design' }))`. Use `App` **only** when
you need an editor or layered performance; otherwise a single `Leafer` is simpler. `grow` is not
supported on App.

## Graphic editor

`@leafer-in/editor` (+ `@leafer-in/viewport` recommended). Or install `leafer-editor` which bundles
both. Editing needs the App structure (handles render on `sky`).

```ts
import { App, Frame, Rect } from 'leafer-ui'
import '@leafer-in/editor'
import '@leafer-in/viewport'

const app = new App({
  view: window,
  fill: '#333',
  editor: {},   // shorthand: auto-creates app.editor + tree + sky layers
})

app.tree.add(Frame.one({
  children: [
    Rect.one({ editable: true, fill: '#FEB027', cornerRadius: [20, 0, 0, 20] }, 100, 100),
    Rect.one({ editable: true, fill: '#FFE04B', cornerRadius: [0, 20, 20, 0] }, 300, 100),
  ],
}, 100, 100, 500, 600))
```

- Set `editable: true` per element to make it selectable/transformable.
- The editor provides move/scale/rotate/skew, multi-select, marquee, group/ungroup, double-click into
  group, lock, z-order. Read the current selection via `app.editor.list` / `app.editor.target`.
- Configure handles/snapping/style via the editor config; custom tools via `EditTool`, custom inline
  editors via `InnerEditor`. Text editing inside the editor needs `@leafer-in/text-editor`.
- Explicit form (what `editor: {}` expands to): `app.sky.add(app.editor = new Editor())` with
  `import { Editor } from '@leafer-in/editor'`.

## Infinite canvas — viewport types

Zoom/pan needs `@leafer-in/viewport`. Set `type` on the `Leafer` (or `App`'s `tree`). The engine wires
up the right wheel/touch/keyboard handling automatically.

| `type` | Behavior |
| --- | --- |
| `block` | default; content fixed (no pan/zoom) |
| `viewport` | wheel/drag pan, ctrl+wheel / pinch zoom |
| `design` | viewport + space/middle-drag pan, zoom clamped 0.01–256 (Figma-like) |
| `document` | viewport + scroll limited to content, zoom ≥ 1 (document-like) |
| `custom` | viewport hooks, but you implement pan/zoom yourself |

```ts
import { Leafer, Rect } from 'leafer-ui'
import '@leafer-in/viewport'
const leafer = new Leafer({ view: window, type: 'design' })   // App form: tree: { type: 'design' }
leafer.add(Rect.one({ fill: '#32cd79' }, 100, 100, 200, 200))
```

### Manual / custom pan & zoom
The viewport is a zoom/pan layer; move/scale it directly via `leafer.zoomLayer`:
```ts
leafer.on(MoveEvent.BEFORE_MOVE, (e: MoveEvent) => {
  leafer.zoomLayer.move(leafer.getValidMove(e.moveX, e.moveY))
})
leafer.on(ZoomEvent.BEFORE_ZOOM, (e: ZoomEvent) => {
  leafer.zoomLayer.scaleOfWorld(e, leafer.getValidScale(e.scale))   // zoom around pointer
})
```
You can also set viewport `x` / `y` / `scale` directly to programmatically pan/zoom. Watch changes via
`PropertyEvent`. Related plugins: `@leafer-in/view` (fit / fit-width / focus element) and
`@leafer-in/scroll` (infinite-canvas scrollbars).

## Auto-layout (Flow) — Flex-like layout

`@leafer-in/flow`. A `Flow` container (a Box with auto-layout) arranges children automatically.

```ts
import { Leafer, Box } from 'leafer-ui'
import { Flow } from '@leafer-in/flow'

const flow = new Flow({
  fill: '#676', width: 100, height: 100,
  flow: 'x',                 // 'x' | 'y' | true; direction of layout
  gap: 10,                   // spacing; or [rowGap, colGap]
  padding: [10, 20],
  flowAlign: 'center',       // main-axis alignment
  flowWrap: true,            // wrap to new lines
  children: [
    new Box({ fill: '#FF4B4B', children: [{ tag: 'Text', text: '1', fill: '#fff', textAlign: 'center', width: 25, height: 20 }] }),
    new Box({ fill: '#FEB027', children: [{ tag: 'Text', text: '2', fill: '#fff', textAlign: 'center', width: 25, height: 40 }] }),
  ],
})
leafer.add(flow)
```
Children can use `autoWidth`/`autoHeight` (omit width/height) to size to content. Combine with `Box`
`overflow` for scroll regions. For exact prop names/values consult the official flow plugin docs.
