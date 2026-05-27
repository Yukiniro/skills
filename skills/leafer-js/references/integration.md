# Framework & platform integration, JSON, coordinates

## Frameworks

Universal rule: **create Leafer in a mount hook, destroy on unmount, and never store Leafer nodes in
reactive state.** Reactive proxies wrap every node and tank performance. For reactivity use the
element's `proxyData`.

### React
```tsx
import { useEffect } from 'react'
import { Leafer, Rect } from 'leafer-ui'

export default function App() {
  useEffect(() => {
    const leafer = new Leafer({ view: 'leafer-view' })  // id string, no '#'
    leafer.add(new Rect({ x: 100, y: 100, width: 200, height: 200, fill: '#32cd79', draggable: true }))
    return () => leafer.destroy()   // StrictMode mounts twice in dev — destroy is required
  }, [])
  return <div id="leafer-view" style={{ position: 'absolute', inset: 0, width: '100%', height: '100%' }} />
}
```

### Vue 3
```vue
<script setup lang="ts">
import { onMounted, onUnmounted } from 'vue'
import { Leafer, Rect } from 'leafer-ui'
let leafer: Leafer
onMounted(() => {
  leafer = new Leafer({ view: 'leafer-view' })
  leafer.add(new Rect({ x: 100, y: 100, width: 200, height: 200, fill: '#32cd79', draggable: true }))
})
onUnmounted(() => leafer?.destroy())
</script>
<template><div id="leafer-view" style="position:absolute;inset:0;width:100%;height:100%"></div></template>
```
Community wrapper with components: `leafer-vue`.

### Next.js / Nuxt / VitePress (SSR)
Leafer needs the DOM, so it must run **client-side only**:
- **Next.js**: put the canvas component in a `'use client'` component and create Leafer inside
  `useEffect`; or `dynamic(() => import('./Canvas'), { ssr: false })`.
- **Nuxt**: use `<ClientOnly>` or create inside `onMounted` (guard with `import.meta.client`).
- **VitePress**: wrap in `<ClientOnly>`.

## Platforms (non-browser)

`leafer-ui` is browser-first. For other runtimes use the platform build (same API, different import):

| Platform | Approach |
| --- | --- |
| Web Worker | worker build (`@leafer-ui/worker` / the worker entry) — offload rendering |
| Node.js | `@leafer-ui/node` (uses node-canvas) or the NAPI/skia build for native canvas; export plugin bundled |
| WeChat / Taro / uni-app miniapp | miniapp build; pass the miniapp canvas node as `view` |

Server-side image generation pattern (Node): build the tree, then `await leafer.export('out.png')`
(export is bundled in Node builds). Check current package names on https://www.leaferjs.com/ui/guide/install
before installing — platform package names occasionally change between major versions.

## Save / load JSON

JSON import/export is built in (no plugin). The tree round-trips, so it's the storage format.

```ts
const json = leafer.toJSON()        // -> { tag: 'Leafer', children: [{ tag: 'Rect', ... }] }
const str  = leafer.toString()      // JSON string

// restore
const leafer2 = new Leafer({ view: window })
leafer2.set(json)                   // or: leafer2.add(json.children) / pass a child object to add()
```
`event` listeners and `data` functions are **not** serialized. Any element accepts a `tag`-keyed plain
object, so partial JSON works: `group.set({ children: [{ tag: 'Rect', width: 100, height: 100, fill: '#32cd79' }] })`.

## Coordinate systems & bounds

Leafer has multiple coordinate spaces. Convert between them with the `getXxxPoint()` methods.

| Space | Meaning |
| --- | --- |
| **world** | global screen/canvas coordinates (after all transforms) |
| **page** | scene coordinates ignoring the viewport pan/zoom layer |
| **local** | relative to the element's parent |
| **inner** | inside the element, before its own scale/rotation |
| **box** | the element's own untransformed box coordinates |

Conversion helpers (each "from→to", also accept a distance flag): `getWorldPoint`, `getInnerPoint`,
`getLocalPoint`, `getPagePoint`, `getBoxPoint`, `getWorldPointByPage`, `getInnerPointByLocal`, …
Common case — pointer to scene coords:
```ts
leafer.on('tap', (e) => {
  const inner = leafer.getInnerPoint(e)   // e has worldX/worldY; convert to scene coords
})
```

### Bounds (OBB vs AABB)
- `boxBounds` — element's base box in inner coordinates.
- `renderBounds` — render box (AABB) in inner coordinates (includes stroke/shadow spread).
- `worldBoxBounds` / `worldRenderBounds` — same, in world coordinates (AABB).
- `getBounds(type, relative)` — AABB; `type` ∈ `'box' | 'render' | ...`, `relative` ∈ `'inner' | 'local' | 'world' | 'page'`.
- `getLayoutBounds(type, relative)` — OBB (keeps rotation/scale); `getLayoutPoints()` returns its 4 corners.
- `renderSpread` — force-enlarge render bounds to fix clipped text/effects.
