# Style Presets Reference

Curated visual styles for frontend-resume. Each preset uses distinctive font pairings and color palettes. **No generic AI aesthetics.**

---

## Mood-to-Preset Mapping

Use this table to select 3 presets for guided style discovery:

| Mood                       | Dark Options                  | Light Options               | Specialty                 |
| -------------------------- | ----------------------------- | --------------------------- | ------------------------- |
| Professional/Authoritative | Midnight Architect, Dark Luxe | Clean Slate, Soft Blueprint | —                         |
| Creative/Distinctive       | Dark Luxe, Cosmic Depth       | Paper Craft                 | Brutalist Mono, Retro Ink |
| Modern/Technical           | Neon Terminal, Cosmic Depth   | Soft Blueprint              | Brutalist Mono            |
| Warm/Approachable          | Dark Luxe                     | Paper Craft, Sage Garden    | Retro Ink                 |

---

## Dark Themes

### 1. Midnight Architect

**Vibe:** Sophisticated, premium, established
**Best for:** Senior executives, architects, consultants

**Typography:**

- Display: `Clash Display` (600/700) — via Fontshare
- Body: `Satoshi` (400/500) — via Fontshare

**Font import:**

```html
<link
  href="https://api.fontshare.com/v2/css?f[]=clash-display@600,700&f[]=satoshi@400,500,700&display=swap"
  rel="stylesheet"
/>
```

**Colors:**

```css
:root {
  --bg-primary: #0a0a0f;
  --bg-secondary: #12121a;
  --bg-card: #1a1a24;
  --text-primary: #e8e4dd;
  --text-secondary: #9a958e;
  --accent: #c9a96e;
  --accent-hover: #dbb978;
  --accent-subtle: rgba(201, 169, 110, 0.1);
  --border: rgba(201, 169, 110, 0.15);
}
```

**Animation style:** Slow fade-ins with subtle scale (0.95 -> 1), staggered delays 0.1s increments
**Background:** Solid dark with faint radial gradient glow at top-right
**Skill bars:** Thin horizontal lines with gold fill, percentage on right
**Timeline:** Gold accent line, cards with subtle border glow on hover

---

### 2. Neon Terminal

**Vibe:** Hacker-chic, developer-focused, technical
**Best for:** Software engineers, DevOps, security professionals

**Typography:**

- Display & Body: `JetBrains Mono` (400/700)

**Font import:**

```html
<link
  href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&display=swap"
  rel="stylesheet"
/>
```

**Colors:**

```css
:root {
  --bg-primary: #0d1117;
  --bg-secondary: #161b22;
  --bg-card: #1c2128;
  --text-primary: #c9d1d9;
  --text-secondary: #8b949e;
  --accent: #39d353;
  --accent-secondary: #58a6ff;
  --accent-subtle: rgba(57, 211, 83, 0.1);
  --border: rgba(57, 211, 83, 0.2);
}
```

**Animation style:** Typewriter text reveal for name, blinking cursor after title, instant-appear cards
**Background:** Dark with faint scanline overlay (CSS repeating-linear-gradient, 2px lines)
**Skill bars:** Terminal-style progress `[████████░░] 80%` rendered as styled divs
**Timeline:** Dashed green line, monospace dates, command-prompt style markers (`>_`)
**Signature:** Scanline CSS overlay, `$` prefix on section titles

---

### 3. Dark Luxe

**Vibe:** Elegant, editorial, premium
**Best for:** Creative directors, luxury brand professionals, marketing leads

**Typography:**

- Display: `Cormorant Garamond` (400/600) — elegant serif
- Body: `DM Sans` (400/500)

**Font import:**

```html
<link
  href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,600;1,400&family=DM+Sans:wght@400;500;700&display=swap"
  rel="stylesheet"
/>
```

**Colors:**

```css
:root {
  --bg-primary: #1a1a2e;
  --bg-secondary: #1f1f35;
  --bg-card: #25253d;
  --text-primary: #eee8d5;
  --text-secondary: #a09b90;
  --accent: #e07a5f;
  --accent-hover: #e8917a;
  --accent-subtle: rgba(224, 122, 95, 0.1);
  --border: rgba(224, 122, 95, 0.15);
}
```

**Animation style:** Parallax-style slide-ups (40px), blur-in reveals (filter: blur(8px) -> 0)
**Background:** Deep navy with soft abstract gradient circles (CSS radial-gradient, blurred)
**Skill bars:** Elegant thin bars with terracotta fill, italic percentage labels
**Timeline:** Thin warm-toned line, serif date labels, cards with subtle warm glow

---

### 4. Cosmic Depth

**Vibe:** Bold, futuristic, cutting-edge
**Best for:** Tech founders, AI/ML engineers, researchers

**Typography:**

- Display: `Space Grotesk` (500/700)
- Body: `General Sans` (400/500) — via Fontshare

**Font import:**

```html
<link
  href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;700&display=swap"
  rel="stylesheet"
/>
<link
  href="https://api.fontshare.com/v2/css?f[]=general-sans@400,500,600&display=swap"
  rel="stylesheet"
/>
```

**Colors:**

```css
:root {
  --bg-primary: #0b0b1a;
  --bg-secondary: #10102a;
  --bg-card: #16163a;
  --text-primary: #f0f0f0;
  --text-secondary: #8888aa;
  --accent: #7c3aed;
  --accent-secondary: #06b6d4;
  --accent-subtle: rgba(124, 58, 237, 0.1);
  --border: rgba(124, 58, 237, 0.2);
}
```

**Animation style:** Elements emerge with translateY(30px) + scale(0.98), moderate speed (0.6s)
**Background:** Dark with gradient mesh (2-3 radial-gradient layers, purple + cyan blurred spots)
**Skill bars:** Gradient-filled bars (purple -> cyan), rounded ends
**Timeline:** Dual-accent gradient line, cards with glass-like border (rgba border + backdrop-blur if supported)

---

## Light Themes

### 5. Clean Slate

**Vibe:** Minimal, Swiss-inspired, precise
**Best for:** Designers, product managers, anyone wanting clean authority

**Typography:**

- Display: `Instrument Sans` (600/700) — via Google
- Body: `Source Serif 4` (400/500)

**Font import:**

```html
<link
  href="https://fonts.googleapis.com/css2?family=Instrument+Sans:wght@600;700&family=Source+Serif+4:ital,wght@0,400;0,500;1,400&display=swap"
  rel="stylesheet"
/>
```

**Colors:**

```css
:root {
  --bg-primary: #fafaf9;
  --bg-secondary: #f5f5f4;
  --bg-card: #ffffff;
  --text-primary: #1c1917;
  --text-secondary: #78716c;
  --accent: #dc2626;
  --accent-hover: #b91c1c;
  --accent-subtle: rgba(220, 38, 38, 0.06);
  --border: #e7e5e4;
}
```

**Animation style:** Precise slide-from-left (20px), no bounce, 300ms ease-out, minimal
**Background:** Near-white, clean, no decoration
**Skill bars:** Simple thin bars with red fill, no percentage (just bar length implies level)
**Timeline:** Clean vertical black line (1px), dot markers, left-aligned cards

---

### 6. Paper Craft

**Vibe:** Warm, tactile, analog feel
**Best for:** Writers, educators, academics, non-profit professionals

**Typography:**

- Display: `Lora` (500/700) — warm serif
- Body: `Nunito Sans` (400/600)

**Font import:**

```html
<link
  href="https://fonts.googleapis.com/css2?family=Lora:ital,wght@0,500;0,700;1,400&family=Nunito+Sans:wght@400;600;700&display=swap"
  rel="stylesheet"
/>
```

**Colors:**

```css
:root {
  --bg-primary: #fef9ef;
  --bg-secondary: #faf3e3;
  --bg-card: #ffffff;
  --text-primary: #2d2a26;
  --text-secondary: #7a7570;
  --accent: #b45309;
  --accent-hover: #92400e;
  --accent-subtle: rgba(180, 83, 9, 0.08);
  --border: #e8dfd0;
}
```

**Animation style:** Gentle fade-ups (20px), elements "unfold" with slight rotation (-2deg -> 0), 0.5s ease
**Background:** Cream with subtle paper texture (CSS noise SVG or fine dot pattern)
**Skill bars:** Rounded bars with amber fill on cream track, warm feel
**Timeline:** Amber line, cards with paper-like shadow (warm toned, slightly offset)

---

### 7. Soft Blueprint

**Vibe:** Technical but approachable, structured
**Best for:** Engineers, data scientists, technical PMs

**Typography:**

- Display: `IBM Plex Sans` (500/700)
- Mono: `IBM Plex Mono` (400/500)

**Font import:**

```html
<link
  href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500&family=IBM+Plex+Sans:wght@400;500;700&display=swap"
  rel="stylesheet"
/>
```

**Colors:**

```css
:root {
  --bg-primary: #f8fafc;
  --bg-secondary: #f1f5f9;
  --bg-card: #ffffff;
  --text-primary: #1e293b;
  --text-secondary: #64748b;
  --accent: #2563eb;
  --accent-secondary: #0ea5e9;
  --accent-subtle: rgba(37, 99, 235, 0.06);
  --border: #e2e8f0;
}
```

**Animation style:** Grid-aligned entrance (slide from left 30px), technical precision, 350ms ease-out
**Background:** Light with thin blueprint grid lines (CSS linear-gradient, #e2e8f0 1px lines, 40px gap)
**Skill bars:** Blue-filled bars with monospace percentage labels
**Timeline:** Blue line, circular node markers with number, clean data-table aesthetic

---

## Specialty Themes

### 8. Brutalist Mono

**Vibe:** Raw, confident, anti-design, memorable
**Best for:** Designers, brand strategists, anyone wanting to stand out

**Typography:**

- Display: `Syne` (700/800)
- Body: `Space Mono` (400/700)

**Font import:**

```html
<link
  href="https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Syne:wght@700;800&display=swap"
  rel="stylesheet"
/>
```

**Colors:**

```css
:root {
  --bg-primary: #ffffff;
  --bg-secondary: #f0f0f0;
  --bg-card: #ffffff;
  --text-primary: #000000;
  --text-secondary: #444444;
  --accent: #ff3333;
  --accent-hover: #cc0000;
  --accent-subtle: rgba(255, 51, 51, 0.05);
  --border: #000000;
}
```

**Animation style:** Hard cuts (no transition, instant appear with opacity snap), bold border animations (border-width 0 -> 3px)
**Background:** Pure white, no decoration
**Skill bars:** Thick-bordered rectangles that fill with black, percentage in bold monospace
**Timeline:** Thick black line (3px), square markers, cards with heavy borders
**Signature:** All-caps section titles, thick borders, stark contrast, no curves (border-radius: 0)

---

### 9. Sage Garden

**Vibe:** Nature-inspired, calming, organic
**Best for:** Environmental professionals, wellness, HR, educators

**Typography:**

- Display: `Fraunces` (500/700) — distinctive serif
- Body: `Outfit` (400/500)

**Font import:**

```html
<link
  href="https://fonts.googleapis.com/css2?family=Fraunces:ital,wght@0,500;0,700;1,400&family=Outfit:wght@400;500;600&display=swap"
  rel="stylesheet"
/>
```

**Colors:**

```css
:root {
  --bg-primary: #f1f5f0;
  --bg-secondary: #e5ece3;
  --bg-card: #fafcf9;
  --text-primary: #1a2e1a;
  --text-secondary: #5a6e5a;
  --accent: #2d5a27;
  --accent-secondary: #8fbc8f;
  --accent-subtle: rgba(45, 90, 39, 0.08);
  --border: #c8d8c4;
}
```

**Animation style:** Organic easing (cubic-bezier(0.34, 1.56, 0.64, 1) — spring physics), elements "grow" into place (scale 0.9 -> 1), 0.6s
**Background:** Sage-tinted white with soft abstract leaf-like gradient shapes (radial-gradient with green tints)
**Skill bars:** Rounded bars with gradient green fill (dark -> light), organic feel
**Timeline:** Dotted green line, leaf-like circular markers, cards with soft green shadow

---

### 10. Retro Ink

**Vibe:** Vintage editorial, personality-driven, literary
**Best for:** Journalists, marketers, personal brand enthusiasts

**Typography:**

- Display: `Playfair Display` (700/900)
- Body: `Karla` (400/500)

**Font import:**

```html
<link
  href="https://fonts.googleapis.com/css2?family=Karla:wght@400;500;700&family=Playfair+Display:ital,wght@0,700;0,900;1,400&display=swap"
  rel="stylesheet"
/>
```

**Colors:**

```css
:root {
  --bg-primary: #fffbf0;
  --bg-secondary: #f5f0e0;
  --bg-card: #ffffff;
  --text-primary: #2c2c2c;
  --text-secondary: #6b6b6b;
  --accent: #c43a31;
  --accent-secondary: #3d5a80;
  --accent-subtle: rgba(196, 58, 49, 0.06);
  --border: #d4cbb8;
}
```

**Animation style:** Typeface-driven reveals (title chars stagger in), decorative rules animate width 0 -> 100%, 0.5s ease
**Background:** Ivory with subtle aged-paper tint
**Skill bars:** Vintage meter style — bordered boxes with red fill, label above
**Timeline:** Decorative red line with diamond markers, serif date labels, pull-quote style descriptions
**Signature:** Decorative horizontal rules `<hr>` between sections, drop-cap on first paragraph, italic accent text

---

## DO NOT USE (Generic AI Patterns)

**Fonts:** Inter, Roboto, Arial, system fonts as display
**Colors:** `#6366f1` (generic indigo), purple gradients on white, generic blue (#3b82f6 as sole accent)
**Layouts:** Everything centered with no variation, identical card grids
**Decorations:** Gratuitous glassmorphism, generic gradient backgrounds, drop shadows without purpose
