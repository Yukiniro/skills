# Styling & appearance

Style properties are set at construction, by direct assignment, or via `set()`. Reassign whole objects
when changing nested values (e.g. `el.fill = {...}`) — see the first-level-setter gotcha in SKILL.md.

## Table of contents
- [Fill](#fill) (solid, linear/radial/angular gradient, image/pattern)
- [Stroke](#stroke)
- [Shadow & innerShadow](#shadow--innershadow)
- [Corner radius](#corner-radius)
- [Opacity & visibility](#opacity--visibility)
- [Mask & eraser](#mask--eraser)
- [Blend mode](#blend-mode)
- [Origin & around (transform anchor)](#origin--around)

## Fill

`fill` is like CSS `background-color` (or text `color`). It accepts a color string, a paint object, or
an **array of paints** stacked bottom→top.

```ts
fill: '#32cd79'                                              // solid
fill: 'rgba(50,205,121,0.7)'

fill: { type: 'linear', stops: ['#FF4B4B', '#FEB027'] }      // linear gradient (top→bottom by default)
fill: { type: 'linear', from: 'left', to: 'right', stops: [{ offset: 0, color: '#FF4B4B' }, { offset: 1, color: '#FEB027' }] }
fill: { type: 'radial', stops: ['#FF4B4B', '#FEB027'] }      // radial gradient
fill: { type: 'angular', stops: ['#FF4B4B', '#FEB027'] }     // conic/angular gradient

fill: { type: 'image', url: '/image/leafer.jpg', mode: 'cover' }   // image fill
```
Image-fill `mode`: `'cover' | 'fit' | 'fill' | 'stretch' | 'clip' | 'repeat' | 'normal'`. Pattern
controls: `scale`, `rotation`, `offset`, and (Leafer extras) fixed-size tiling + gap/stagger spacing.
Stack multiple fills: `fill: [{ type: 'solid', color: '#000' }, { type: 'image', url, mode: 'cover', opacity: 0.5 }]`.

## Stroke

`stroke` takes the same paint types as `fill` (solid/gradient/image), single or array.

```ts
new Rect({
  stroke: '#32cd79',
  strokeWidth: 5,
  strokeAlign: 'center',     // 'inside' | 'center' | 'outside'
  strokeCap: 'round',        // 'none' | 'round' | 'square'
  strokeJoin: 'round',       // 'miter' | 'bevel' | 'round'
  strokeScaleFixed: true,    // keep line width constant when the view zooms ('zoom-in' | number | boolean)
  dashPattern: [6, 6],       // dashed
  dashOffset: 3,
})
```

## Shadow & innerShadow

Both accept a single object or an array of objects.

```ts
shadow: { x: 10, y: -10, blur: 20, color: '#FF0000AA' }          // outer (drop) shadow
shadow: { x: 0, y: 8, blur: 20, spread: 4, color: '#0006', box: true }  // box-shadow style (spread, box)
innerShadow: { x: 10, y: 5, blur: 20, color: '#FF0000AA' }       // inner shadow
```
Leafer extras vs other engines: inner shadow, box shadow, multiple stacked shadows, fixed shadow.

## Corner radius
`cornerRadius: 20` or `[topLeft, topRight, bottomRight, bottomLeft]`. Works on Rect, Box, Frame, Polygon, Star, Image.

## Opacity & visibility
```ts
el.opacity = 0.5        // 0–1; group opacity composites without per-child overlap artifacts
el.visible = false      // hide (kept in tree); worldOpacity is the resolved value incl. parents
```

## Mask & eraser

Put a sibling inside a `Group` and flag it. Affects the other children in that group.

```ts
import { Group, Ellipse, Image } from 'leafer-ui'
const group = new Group({ x: 100, y: 100 })
const mask = new Ellipse({ width: 100, height: 100, fill: 'black', mask: true })   // 'clip' | 'alpha' | 'grayscale' | 'path' | true
const image = new Image({ width: 100, height: 100, url: '/image/leafer.jpg' })
group.add([mask, image])     // image is clipped to the ellipse
```
```ts
const eraser = new Ellipse({ width: 70, height: 70, fill: 'black', eraser: true }) // erases overlapping siblings
group.add([image, eraser])
```

## Blend mode
`blendMode: 'multiply'` (and the usual CSS modes: `normal`, `screen`, `overlay`, `darken`, `lighten`,
`color-dodge`, `difference`, `hue`, `saturation`, …). Leafer also supports child blend modes.

## Origin & around

Both set the transform anchor for `rotation`/`scale`. Value: `'center'`, `'top'`, `'bottom'`,
`'left-top'`, …, or a `{ x, y }` point.

- **`origin`** — like CSS `transform-origin`: rotate/scale around that point, position unchanged.
- **`around`** — also moves the element's anchor point to its `(x, y)` (game-engine "anchor"). Useful to
  position by center: `{ x: 50, y: 50, around: 'center' }`.

```ts
new Rect({ x: 25, y: 25, width: 50, height: 50, origin: 'center', rotation: 45, fill: '#4DCB71' })
```

## Pixel-level hit testing (image transparency)
Combine with interaction: `hitFill: 'pixel'` filters transparent pixels of PNG/SVG fills so only the
visible shape is clickable — see [events.md](events.md).

## Interaction-state styles (hover/press/…)
`hoverStyle`, `pressStyle`, `selectedStyle`, `states` etc. require `@leafer-in/state` — see
[animation.md](animation.md#interaction-states) and [plugins.md](plugins.md).
