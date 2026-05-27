# Events & interaction

Leafer has a DOM-like event system with **capture + bubble** phases, simulated events, and rich
pointer/gesture/viewport events. Listen on any element (or the Leafer/App root).

## Listening

```ts
import { Leafer, Rect, PointerEvent } from 'leafer-ui'

const rect = new Rect({ width: 200, height: 200, fill: '#32cd79', draggable: true })

function onEnter(e: PointerEvent) { (e.current as Rect).fill = '#42dd89' }
function onLeave(e: PointerEvent) { (e.current as Rect).fill = '#32cd79' }

rect.on(PointerEvent.ENTER, onEnter)
rect.on(PointerEvent.LEAVE, onLeave)
rect.off(PointerEvent.ENTER, onEnter)        // remove
rect.once('tap', e => {})                    // fire once
rect.emit('pointer.enter', { current: rect })// dispatch manually
```

- `e.current` = element the listener is bound to; `e.target` = the actual hit element.
- Use string types (`'pointer.enter'`, `'tap'`, `'drag'`) or the static constants (`PointerEvent.ENTER`).
- Capture phase: `rect.on(type, fn, { capture: true })`. Stop propagation: `e.stop()` / `e.stopDefault()`.
- `on_()` returns an id and accepts a `bind` `this`; pair with `off_()` for easy cleanup.

### Init-time `event` object (not serialized to JSON)
```ts
Rect.one({
  fill: '#32cd79', draggable: true,
  event: {
    [PointerEvent.ENTER]: e => { (e.current as Rect).fill = '#42dd89' },
    [PointerEvent.LEAVE]: e => { (e.current as Rect).fill = '#32cd79' },
  },
}, 100, 100, 200, 200)
```

## Dragging

`draggable: true` enables built-in dragging (no plugin needed). Constrain with `dragBounds`
(`{ x, y, width, height }` or `'parent'`) and `dragBoundsType: 'inner' | 'outer'`. Listen to
`DragEvent.START / DRAG / END`, and `DropEvent` for drop targets. `dropTo(parent)` reparents on drop.

## Event types (constants → string namespace)

| Event class | Common members | When |
| --- | --- | --- |
| `PointerEvent` | `DOWN UP MOVE TAP DOUBLE_TAP CLICK LONG_PRESS ENTER LEAVE OVER OUT MENU` | unified mouse/touch/pen pointer |
| `DragEvent` | `START DRAG END` | dragging an element |
| `DropEvent` | `DROP` | dropping onto a target |
| `SwipeEvent` | `SWIPE LEFT RIGHT UP DOWN` | swipe gestures |
| `MoveEvent` | `BEFORE_MOVE MOVE END` | viewport pan (wheel/touch) |
| `ZoomEvent` | `BEFORE_ZOOM ZOOM END` | viewport zoom (ctrl+wheel/pinch) |
| `RotateEvent` | `BEFORE_ROTATE ROTATE END` | rotate gesture |
| `KeyEvent` | `DOWN UP` | keyboard |
| `ImageEvent` | `LOAD LOADED ERROR` | image element loading |
| `ChildEvent` | `ADD REMOVE` | tree mutations |
| `PropertyEvent` | `CHANGE` | a watched property changed (e.g. viewport x/y/scale) |
| `BoundsEvent` | — | element bounds changed |
| `ResizeEvent` | `RESIZE` | engine/canvas resized |
| `LayoutEvent` / `RenderEvent` | `START END` | layout/render lifecycle hooks |
| `LeaferEvent` | `START READY VIEW_READY END` | engine lifecycle |

> CDN/script-tag note: `PointerEvent` and `DragEvent` collide with browser globals — use
> `MyPointerEvent` / `MyDragEvent` from the `LeaferUI` global.

### String naming
String type = `category.action`, e.g. `'pointer.enter'`, `'pointer.tap'`, `'drag.start'`, `'zoom.zoom'`,
`'child.add'`, `'image.loaded'`.

## Hit testing (control what is interactive)

| Prop | Meaning |
| --- | --- |
| `hittable` | element responds to pointer events (like CSS `pointer-events`) |
| `hitChildren` | whether children are interactive |
| `hitSelf` | whether the element itself (excluding children) is interactive |
| `hitFill` | `'all'` \| `'pixel'` \| `'none'` — `'pixel'` does per-pixel hit on PNG/SVG fill (skips transparent) |
| `hitStroke` | `'all'` \| `'path'` \| `'none'` — hit area for stroke |
| `hitRadius` | enlarge the hit area (easier touch targets) |
| `cursor` | hover cursor; any CSS cursor name, or custom |

```ts
new Image({ url: '/sprite.png', hitFill: 'pixel' })   // only opaque pixels are clickable
```

`pick(worldPoint, options?)` returns the element(s) at a point (supports through-path). Use for custom
selection/hover logic outside the normal event flow.

## Viewport gesture events
`MoveEvent` / `ZoomEvent` / `RotateEvent` drive infinite-canvas pan/zoom. The viewport plugin handles
them automatically; for custom logic listen to `BEFORE_MOVE` / `BEFORE_ZOOM` — see
[app-editor-viewport.md](app-editor-viewport.md).
