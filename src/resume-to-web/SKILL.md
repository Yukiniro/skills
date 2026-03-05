---
name: resume-to-web
description: Convert PDF resumes into interactive, animated single-page HTML resume websites with distinctive visual styles. Use when the user wants to create a web resume, convert a PDF resume to HTML, build an interactive CV page, or generate a personal resume website. Helps non-designers discover their aesthetic through visual exploration ("show, don't tell"). Supports PDF input, text input, and enhancement of existing HTML resumes.
---

# Resume to Web

Create zero-dependency, animation-rich HTML resume pages that run entirely in the browser. Help users discover their preferred aesthetic through visual exploration, then generate production-quality interactive resumes.

## Core Philosophy

1. **Zero Dependencies** — Single HTML files with inline CSS/JS. No npm, no build tools.
2. **Show, Don't Tell** — Generate visual previews, let users pick what they like.
3. **Distinctive Design** — Avoid generic "AI slop" aesthetics. Each resume should feel custom-crafted.
4. **Print-Friendly** — Every resume MUST include `@media print` styles for clean PDF output.
5. **Accessible** — Semantic HTML, keyboard nav, reduced motion support, WCAG AA contrast.

---

## Phase 0: Detect Mode

Determine what the user wants:

**Mode A: From PDF** — User provides a .pdf resume file → Phase 1
**Mode B: From Text** — User provides resume content as text → Phase 1
**Mode C: Enhancement** — User has an existing HTML resume to improve → Read file, then Phase 2

---

## Phase 1: Content Extraction & Structuring

### Step 1.1: PDF Extraction (Mode A only)

Run `scripts/extract_pdf.py` on the user's PDF:

```bash
python [skill-dir]/scripts/extract_pdf.py <resume.pdf>
```

Requires `pdfplumber` (preferred) or `PyPDF2`. If neither is installed, prompt user to install:
```bash
pip install pdfplumber
```

Present extracted content to user for confirmation.

### Step 1.2: Structure Content

Parse raw text into structured sections:
- **header**: name, title/tagline, location, contact (email, phone, LinkedIn, GitHub, portfolio)
- **about**: professional summary
- **experience[]**: company, role, dates, location, bullets
- **education[]**: school, degree, dates, honors/GPA
- **skills{}**: grouped by category with optional proficiency levels (0-100)
- **projects[]**: name, description, tech stack, link
- **certifications[]**: name, issuer, date (optional)
- **languages[]**: language, proficiency (optional)

Present structured content to user for review. Ask: "Does this look correct? Any sections to add, remove, or modify?"

### Step 1.3: Section Priority

Ask via AskUserQuestion:
- Header: "Layout"
- Question: "Which sections should be most prominent?"
- Options:
  - "Experience-heavy" — Work history is the star (senior professionals)
  - "Skills-focused" — Technical skills front and center (developers/engineers)
  - "Projects-driven" — Portfolio/projects spotlight (designers/freelancers)
  - "Balanced" — Equal weight to all sections

---

## Phase 2: Style Discovery

### Step 2.0: Style Path

Ask: "How would you like to choose your resume style?"
- "Show me options" — Generate 3 visual previews (recommended) → Step 2.1
- "I know what I want" — Pick from preset list directly → Show preset picker below

**Available Presets:**

| Preset | Vibe | Best For |
|--------|------|----------|
| Midnight Architect | Sophisticated, premium | Executives, consultants |
| Neon Terminal | Hacker-chic, developer | Software engineers, DevOps |
| Dark Luxe | Elegant, editorial | Creative directors, marketing |
| Cosmic Depth | Bold, futuristic | Tech founders, AI/ML engineers |
| Clean Slate | Minimal, Swiss-inspired | Designers, product managers |
| Paper Craft | Warm, tactile | Writers, educators, academics |
| Soft Blueprint | Technical, approachable | Engineers, data scientists |
| Brutalist Mono | Raw, anti-design | Brand strategists, standout seekers |
| Sage Garden | Nature-inspired, calming | HR, wellness, educators |
| Retro Ink | Vintage editorial | Journalists, personal brands |

If user picks one directly, skip to Phase 3.

### Step 2.1: Guided Discovery

**Question 1 — Mood** (multiSelect up to 2):
- "Professional/Authoritative" — Established, trustworthy
- "Creative/Distinctive" — Unique, design-forward
- "Modern/Technical" — Clean, developer-oriented
- "Warm/Approachable" — Friendly, personable

**Question 2 — Tone:**
- "Light" — Clean, printable
- "Dark" — Bold, screen-optimized
- "Either" — Let the style decide

### Step 2.2: Generate 3 Previews

Based on mood + tone, select 3 presets. Read `references/STYLE_PRESETS.md` for full preset definitions.

**Mood-to-preset mapping:**

| Mood | Dark | Light | Specialty |
|------|------|-------|-----------|
| Professional | Midnight Architect, Dark Luxe | Clean Slate, Soft Blueprint | — |
| Creative | Dark Luxe, Cosmic Depth | Paper Craft | Brutalist Mono, Retro Ink |
| Modern/Technical | Neon Terminal, Cosmic Depth | Soft Blueprint | Brutalist Mono |
| Warm | Dark Luxe | Paper Craft, Sage Garden | Retro Ink |

Generate 3 mini HTML previews in `.claude-design/resume-previews/`:
```
.claude-design/resume-previews/
├── style-a.html
├── style-b.html
└── style-c.html
```

Each preview: self-contained (~80-120 lines), shows hero section + one experience entry + skill bars. Enough to convey the aesthetic.

**NEVER use these generic patterns:**
- Inter, Roboto, Arial as display fonts
- Purple gradients on white, generic indigo `#6366f1`
- Everything centered with no variation
- Gratuitous glassmorphism

### Step 2.3: Choose

Present previews, ask user to pick one or mix elements.

---

## Phase 3: Generate Resume

Read these reference files for the chosen preset:
- **`references/STYLE_PRESETS.md`** — Full CSS variables, font URLs, color palette, animation style
- **`references/RESUME_COMPONENTS.md`** — Interactive component CSS/JS patterns
- **`references/HTML_ARCHITECTURE.md`** — Base HTML template, mandatory CSS, JS architecture, print styles, accessibility checklist

### Output

Generate a single self-contained HTML file:
- All CSS inline in `<style>`
- All JS inline in `<script>`
- Google Fonts / Fontshare via `<link>` (gracefully degradable)
- Semantic HTML5 structure

### Required Features

1. **Scroll-triggered reveals** — Elements animate in via IntersectionObserver
2. **Floating navigation** — Fixed nav with active section tracking
3. **Animated skill bars** — Fill on scroll-into-view
4. **Scroll progress bar** — Thin bar at top
5. **Back-to-top button** — Appears after scrolling
6. **Print stylesheet** — `@media print` with white bg, no animations, visible URLs
7. **Reduced motion** — `@media (prefers-reduced-motion: reduce)` disables animations
8. **Responsive** — All sizes use `clamp()`, works mobile through desktop

### Verification Checklist

Before delivering, verify:
- [ ] All typography uses `clamp(min, preferred, max)`
- [ ] All spacing uses `clamp()` or viewport units
- [ ] Semantic HTML (`<header>`, `<main>`, `<section>`, `<nav>`)
- [ ] Print styles included and functional
- [ ] Reduced motion respected
- [ ] ARIA labels on nav, buttons, progress bar
- [ ] Color contrast meets WCAG AA
- [ ] External links have `target="_blank" rel="noopener"`

---

## Phase 4: Delivery

1. **Clean up** — Delete `.claude-design/resume-previews/` if it exists
2. **Open** — Launch in browser: `open [filename].html`
3. **Summary:**

```
Your interactive resume is ready!

File: [filename].html
Style: [Style Name]
Sections: [list]

Features:
- Scroll-triggered animations
- Animated skill bars
- Interactive timeline
- Floating navigation
- Print-friendly (Ctrl+P)
- Responsive on all screen sizes

To customize:
- Colors: Edit :root CSS variables at the top
- Fonts: Change the font import link
- Animations: Modify .reveal class timings
- Content: Edit text directly in the HTML

Would you like me to make any adjustments?
```

---

## Troubleshooting

**PDF extraction returns little text:** PDF may be image-based (scanned). Ask user to provide text content directly.

**Fonts not loading:** Check font URL. Ensure `font-family` declaration includes system font fallback.

**Animations not triggering:** Verify IntersectionObserver is initialized. Check that `.visible` class is being added.

**Print output looks wrong:** Ensure `@media print` block exists. Check that animations are disabled and backgrounds are white.
