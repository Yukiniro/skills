# Elements (display nodes)

All elements import from the core package (`leafer-ui`, or `leafer` for the full bundle). Every element
shares the common props/methods in [api](#common-props--methods). Below: each element's distinct purpose
+ a minimal example.

## Table of contents

- [Shapes](#shapes): Rect, Ellipse, Line, Polygon, Star, Path, Pen, Image, SVG, Canvas, Text
- [Containers](#containers): Group, Box, Frame
- [Custom elements](#custom-elements)
- [Common props & methods](#common-props--methods)

## Shapes

### Rect — rectangle / rounded rectangle
```ts
new Rect({ x: 100, y: 100, width: 100, height: 100, fill: '#32cd79', cornerRadius: [0, 40, 20, 40] })
```
`cornerRadius`: number or `[tl, tr, br, bl]`.

### Ellipse — circle, ring, sector, arc
```ts
new Ellipse({ width: 100, height: 100, startAngle: -60, endAngle: 180, innerRadius: 0.5, fill: '#32cd79' })
```
`innerRadius` (0–1) makes a ring; `startAngle`/`endAngle` make sectors/arcs. Draw from center with `around: 'center'`.

### Line — line, polyline, smooth curve
```ts
new Line({ width: 100, strokeWidth: 5, stroke: '#32cd79' })           // horizontal line by width
new Line({ points: [0, 0, 100, 50, 200, 0], curve: true, stroke: '#32cd79', strokeWidth: 4 }) // polyline / curve
```
A Line has no fill; style it with `stroke`. `rotation` angles it; `toPoint` sets the end.

### Polygon — triangle, regular/free polygon
```ts
new Polygon({ width: 100, height: 100, sides: 6, cornerRadius: 10, fill: '#32cd79' })  // regular hexagon
new Polygon({ points: [0, 90, 100, 60, 200, 80, 300, 40], curve: true, fill: '#32cd79' }) // free polygon
```

### Star
```ts
new Star({ width: 100, height: 100, corners: 8, innerRadius: 0.5, cornerRadius: 5, fill: '#32cd79' })
```

### Path — arbitrary shape via path data
```ts
new Path({ path: 'M10 10 L100 10 L100 100 Z', fill: '#32cd79', scale: 0.5 })
```
`path` accepts an SVG path string, a numeric command array, or a command-object array. Set
`pathString`/`path` to enter "path-first" mode.

### Pen — imperative drawing (Canvas 2D-like API)
```ts
const pen = new Pen()
pen.setStyle({ fill: '#FF4B4B', windingRule: 'evenodd' })
pen.roundRect(0, 0, 100, 100, 30).arc(50, 50, 25)
leafer.add(pen)
```
Methods: `moveTo`, `lineTo`, `arc`, `rect`, `roundRect`, `drawEllipse`, `setStyle`, … Chainable. `Path` also exposes a `path.pen` PathCreator.

### Image — raster or SVG image
```ts
new Image({ url: '/image/leafer.jpg', draggable: true })             // url can be png/jpg/svg/webp
import { Platform } from 'leafer-ui'
new Image({ url: Platform.toURL(svgString, 'svg') })                 // inline SVG string -> crisp scaling
```
Listen for load/error with `ImageEvent`. Any element can also show an image via image fill (see styling.md).

### SVG — see Image; `Image` and image-fill both load SVG with crisp scaling.

### Canvas — a drawable offscreen canvas element
```ts
const canvas = new Canvas({ width: 800, height: 600 })
const { context } = canvas          // native CanvasRenderingContext2D
context.fillStyle = '#FF4B4B'; context.fillRect(0, 0, 100, 100)
canvas.paint()                       // commit pixels, then re-render
leafer.add(canvas)
```

### Text — multi-line text, HTML5-equivalent rendering
```ts
new Text({ text: 'Welcome to LeaferJS', fill: '#32cd79', fontSize: 24, fontWeight: 'bold' })
```
Key props: `fontSize`, `fontFamily`, `fontWeight`, `fontStyle`, `textAlign`, `verticalAlign`,
`lineHeight`, `letterSpacing`, `textDecoration`, `padding`, `textOverflow`. Auto-sizes when `width`
is omitted. Supports count/typewriter animation (see animation.md). Double-click editing needs
`@leafer-in/text-editor` (+ editor).

## Containers

| Container | Like | Notes |
| --- | --- | --- |
| `Group` | transform group | No fill/stroke. Has x/y/scale/rotation; children positioned relative to it. Nest freely. |
| `Box` | HTML `<div>` | `Group` + `Rect` styling (fill, stroke, cornerRadius, shadow). Nest freely. |
| `Frame` | artboard / page | A `Box` that clips overflow and defaults to white background. Use for design "pages". |

```ts
import { Group, Rect, Ellipse } from 'leafer-ui'
const group = new Group({ x: 100, y: 100 })
group.add([new Rect({ width: 100, height: 100, fill: '#32cd79' }),
           new Ellipse({ x: 50, y: 50, width: 100, height: 100, fill: '#FEB027' })])
leafer.add(group)
```
`Box`/`Frame` also support `overflow`, and with `@leafer-in/flow` become auto-layout containers (see app-editor-viewport.md).

## Custom elements

Register a custom element class to extend rendering. Pattern:
```ts
import { UI, registerUI, dataProcessor, RectData } from 'leafer-ui'

@registerUI()
class MyShape extends UI {
  get __tag() { return 'MyShape' }
  // override __draw / __drawShape to render custom geometry
}
```
For full custom-element details (attr decorators, custom data, draw lifecycle) consult the official
docs (`reference/display/custom`). Most use cases are covered by `Path`/`Pen` instead.

## Common props & methods

Set on any element; settable at construction, via direct assignment, or `set()`.

**Identity:** `id`, `tag`, `name`, `className`, `innerId` (runtime-only), `data` (your `{}` namespace).
**Layout:** `x`, `y`, `width`, `height`, `scaleX`/`scaleY`/`scale`, `rotation`, `skewX`/`skewY`,
`offsetX`/`offsetY`, `origin`, `around`, `zIndex`, `visible`, `opacity`, `lockRatio` (needs resize plugin).
**Appearance:** `fill`, `stroke`, `strokeWidth`, `strokeAlign`, `dashPattern`, `shadow`, `innerShadow`,
`cornerRadius`, `blendMode`, `mask`, `eraser` — see [styling.md](styling.md).
**Interaction:** `draggable`, `editable` (needs editor), `hittable`, `hitFill`, `hitStroke`, `cursor`,
`dragBounds` — see [events.md](events.md).
**Relations:** `parent`, `leafer`, `app`.

**Common methods:**
- Tree: `add()`, `remove()`, `destroy()`, `clone()`.
- Data: `set(data, transition?)`, `get()`, `reset(data?)`, `setAttr()`, `getAttr()`, `toJSON()`, `toString()`.
- Transform (incremental, optional `transition`): `move()`, `moveInner()`, `rotateOf()`, `scaleOf()`,
  `skewOf()`, `flip()`, `setTransform()`, `getTransform()`.
- Bounds: `getBounds(type, relative)` (AABB), `getLayoutBounds()` (OBB w/ rotation/scale).
- Find (needs `@leafer-in/find`): `find()`, `findOne()`, `findTag()`. Pick: `pick(point)`.
- Events: `on()`, `once()`, `off()`, `emit()` — see [events.md](events.md).
- Update: `forceUpdate()`, `forceRender()`, `nextRender(fn)`, `updateLayout()`.
- Export (needs `@leafer-in/export`): `export()`, `syncExport()` — see [plugins.md](plugins.md).
- Path: `getPath()`, `getPathString()`.

Coordinate systems (world/page/inner/local/box) and the full bounds model are in
[integration.md](integration.md#coordinate-systems--bounds).
