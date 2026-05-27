# Plugin catalog & packaging

## Golden rule
Core elements (Rect, Group, Text, …) come from `leafer-ui`. **Plugin features must be imported** or they
silently do nothing. Two import styles:

```ts
import '@leafer-in/editor'              // side-effect import: enough to enable `editable`, etc.
import { Editor } from '@leafer-in/editor'  // named import: only when you instantiate the class
```

`@leafer-in/*` packages are installed automatically as deps of `leafer-ui`'s peer set in most setups,
but to be safe install the ones you import: `npm i @leafer-in/editor @leafer-in/animate`.

## Which feature needs which plugin

| You use… | Import |
| --- | --- |
| `editable`, `app.editor`, selection/transform | `@leafer-in/editor` |
| double-click text editing (with editor) | `@leafer-in/text-editor` |
| `type: 'viewport'/'design'/'document'`, zoom/pan | `@leafer-in/viewport` |
| `animation`, `transition`, `el.animate()` | `@leafer-in/animate` |
| `hoverStyle`/`pressStyle`/`states`/`state`/`selected` | `@leafer-in/state` |
| `Flow` auto-layout container | `@leafer-in/flow` |
| `motionPath`/`motion` along a path | `@leafer-in/motion-path` (+ animate) |
| `Arrow` element / line arrowheads | `@leafer-in/arrow` |
| `Robot` sprite/game character | `@leafer-in/robot` (+ animate) |
| `el.export()` / `syncExport()` to image/json | `@leafer-in/export` |
| `find()`/`findOne()`/`findTag()` | `@leafer-in/find` |
| `resizeWidth()`/`scaleResize()`/`lockRatio` | `@leafer-in/resize` |
| infinite-canvas scrollbars | `@leafer-in/scroll` |
| zoom-to-fit / focus element | `@leafer-in/view` |
| render HTML content / `HTMLText` | `@leafer-in/html` |
| `dim`/`bright` highlight | `@leafer-in/bright` |
| color utilities | `@leafer-in/color` |
| filter effects | `@leafer-in/filter` |
| extra corner controls | `@leafer-in/corner` |
| fixed scale (ignore view zoom) | `@leafer-in/scale-fixed` |
| Box layout extras | `@leafer-in/box` |

All-in-one bundles (no per-plugin imports needed): `leafer-editor` (editor+viewport+export+…),
`leafer-game` (animate+state+motion-path+robot), `leafer` (everything).

## Export (most common plugin task)

```ts
import { Leafer, Rect } from 'leafer-ui'
import '@leafer-in/export'

const leafer = new Leafer({ view: window })
const rect = Rect.one({ fill: '#32cd79' }, 100, 100)
leafer.add(rect)

rect.export('test.png')                        // browser downloads; Node saves to path
rect.export('HD.png', { pixelRatio: 2 })       // 2x hi-dpi
const r1 = await rect.export('jpg')            // r1.data = base64; jpg quality export('jpg', 0.92)
const r2 = await rect.export('png', { blob: true })           // binary blob
const sync = rect.syncExport('jpg')            // sync (only after images already loaded)
leafer.export('screenshot.png', { screenshot: true })          // whole canvas screenshot

// watermark via onCanvas hook
rect.export('wm.png', {
  pixelRatio: 2,
  onCanvas(canvas) {
    const { context, pixelRatio, width, height } = canvas
    context.scale(pixelRatio, pixelRatio)
    context.fillText('watermark', width - 60, height - 20)
  },
})
```
`export()` is async (returns a Promise); `syncExport()` is sync but requires all referenced images to
be loaded already. JSON export (`toJSON()`) does **not** need a plugin — see
[integration.md](integration.md#save--load-json).

## Arrow
```ts
import { Leafer } from 'leafer-ui'
import { Arrow } from '@leafer-in/arrow'
new Arrow({ x: 100, y: 100, stroke: '#32cd79', strokeWidth: 5, startArrow: 'none', endArrow: 'arrow' })
```
~12 built-in arrowheads via `startArrow` / `endArrow`: `'none'`, `'angle'`, `'angle-side'`, `'arrow'`,
`'triangle'`, `'triangle-flip'`, `'mark'`, `'circle'`, `'circle-line'`, `'square'`, `'square-line'`,
`'diamond'`, `'diamond-line'`, plus custom. Built on `Line`, so it also takes `points`/`toPoint`.

## Robot (game sprite)
```ts
import '@leafer-in/animate'
import { Robot } from '@leafer-in/robot'
// frame-based sprite with walk/attack action presets — see official robot docs for the config shape
```

## Script tag / CDN (no bundler)

```html
<!-- leafer-ui core -->
<script src="https://unpkg.com/leafer-ui@2/dist/web.min.js"></script>
<script>
  const { Leafer, Rect } = LeaferUI                          // everything on the LeaferUI global
  const { MyImage, MyPointerEvent, MyDragEvent } = LeaferUI  // ⚠️ aliases for browser-global conflicts
  const leafer = new Leafer({ view: window })
  leafer.add(new Rect({ x: 100, y: 100, width: 200, height: 200, fill: '#32cd79', draggable: true }))
</script>
```
For the full bundle with plugins, use `https://unpkg.com/leafer@2/dist/web.min.js` (then
`const { Leafer, App, Editor, Arrow, Animate } = LeaferUI`). ESM variant:
`import { Leafer } from 'https://unpkg.com/leafer-ui@2/dist/web.module.min.js'`. Replace `unpkg.com`
with `cdn.jsdelivr.net/npm` if needed. Pin a concrete version (e.g. `@2.1.2`) for production.

> Verify exact current plugin names/versions against https://www.leaferjs.com or npm before pinning —
> the ecosystem adds packages over time.
