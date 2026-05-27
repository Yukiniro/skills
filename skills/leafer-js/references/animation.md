# Animation, transitions & states

All animation features require the **animate plugin**:
```ts
import '@leafer-in/animate'          // side-effect import (or use leafer-game / leafer which bundle it)
```
Interaction states need `@leafer-in/state`; motion-path needs `@leafer-in/motion-path` (+ animate).

## Four ways to animate

| Way | Use for |
| --- | --- |
| `animation` prop | declarative looping/keyframe/enter animation defined on the element |
| `transition` prop | smooth interpolation when a property/state changes |
| `el.animate(...)` method | imperative one-off animation, returns an Animate instance |
| `el.set(data, transition)` / `move(...)` etc. | animate a single change inline |

## `animation` property

### Single style keyframe (with swing/loop)
```ts
new Rect({
  y: 100, fill: '#32cd79', cornerRadius: 50,
  animation: {
    style: { x: 500, cornerRadius: 0, fill: '#ffcd00' }, // target
    duration: 1,
    swing: true,        // ping-pong back and forth
    // loop: true,      // repeat; loop: 3 for a count
    // easing: 'ease-in-out' | 'linear' | 'bounce-out' | ...
    // delay: 0.2,
  },
})
```

### Multi keyframes
```ts
animation: {
  keyframes: [
    { style: { x: 150, scaleX: 2, fill: '#ffcd00' }, duration: 0.5 },
    { style: { x: 50, scaleX: 1 }, duration: 0.2 },
    { style: { x: 550, cornerRadius: 0 }, delay: 0.1, easing: 'bounce-out' },
    { x: 50, rotation: -720, cornerRadius: 50 },   // bare style keyframe
  ],
  duration: 3,    // total; unassigned keyframes split the remainder
  loop: true,
  join: true,     // use the element's pre-animation state as the first ("from") keyframe
}
```

### Enter / exit animation
```ts
new Frame({
  fill: '#FEB027',
  animation:    { keyframes: [{ opacity: 0, offsetX: -150 }, { opacity: 1, offsetX: 0 }], duration: 0.8 }, // enter
  animationOut: { style: { opacity: 0, offsetX: 150 }, duration: 0.8 },                                   // exit (on remove)
})
```
Adding the element plays `animation`; removing it plays `animationOut`.

## `el.animate()` method
```ts
const anim = rect.animate({ x: 300, rotation: 90 }, { duration: 1, loop: true })
anim.pause(); anim.play(); anim.seek(0.5); anim.kill()
```

## Interaction states

`@leafer-in/state`. CSS-like state styles auto-revert; transitions need the animate plugin too.

```ts
import '@leafer-in/state'
import '@leafer-in/animate'

new Box({
  x: 100, y: 100, fill: '#32cd79', cornerRadius: 5, origin: 'center',
  button: true,                       // children sync state automatically
  hoverStyle: { fill: '#FF4B4B', scale: 1.5, cornerRadius: 20 },
  pressStyle: { fill: '#FEB027', scale: 1.1, transitionOut: 'bounce-out' },
  children: [{ tag: 'Text', text: 'Button', padding: [10, 20], hoverStyle: { fill: 'black' } }],
})
```
Built-in state styles: `hoverStyle`, `pressStyle`, `focusStyle`, `selectedStyle`, `disabledStyle`
(+ booleans `selected`, `disabled`, and `focus()`).

### Custom named states
```ts
new Rect({
  width: 100, height: 100, fill: '#32cd79', origin: 'center',
  states: {
    color: { fill: '#FEB027' },
    rotate: { animation: { keyframes: [{ rotation: 45 }, { rotation: 135, scale: 1.2 }], duration: 1, swing: true } },
  },
  state: 'color',     // active state
  transition: 1,      // transition seconds between states
  event: { tap(e) { const r = e.current; r.state = r.state === 'color' ? 'rotate' : 'color' } },
})
```

## Motion path (move/grow along a path)

`@leafer-in/motion-path` (+ animate). Flag a path element `motionPath: true`; siblings in the same
`Group` with a `motion` value travel along it.

```ts
import '@leafer-in/animate'
import '@leafer-in/motion-path'

const group = new Group()
const track = new Polygon({ x: 100, y: 100, motionPath: true, points: [0, 90, 200, 80, 450, 10, 550, 90], curve: true, fill: '#32cd79' })
const car = new Path({
  scale: 0.05, fill: '#FEB027', around: 'bottom', path: 'M...car path...',
  motion: 0,
  animation: { style: { motion: { type: 'percent', value: 1 } }, duration: 9, loop: true }, // 0% -> 100% along track
})
group.add([track, car])
leafer.add(group)
```
`motionRotation` offsets the auto-orientation angle. A path can self-animate its **own** stroke
(drawing/growth) the same way (set `motionPath: true` + `motion` animation on the stroked Path itself).
Helpers: `getMotionTotal()`, `getMotionPoint(at)`.

## Text-specific animation
`Text` supports count animation (animate a numeric `text`) and typewriter animation. See the official
Text docs for exact options.

## Dashed-line / virtual animation
Animate `dashOffset` with `easing: 'linear'`, `loop: true` for marching-ants / flowing arrows (pairs
well with `@leafer-in/arrow`).
