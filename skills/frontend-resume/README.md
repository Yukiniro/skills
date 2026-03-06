# Frontend Resume

Convert resumes into zero-dependency, animation-rich interactive single-page HTML websites. Helps non-designers discover their preferred aesthetic through visual exploration — show, don't tell.

## Features

- **Zero Dependencies** — Single `.html` file with inline CSS/JS. No npm, no build tools, no framework.
- **10 Style Presets** — From Midnight Architect to Brutalist Mono, each with curated font pairings and color palettes.
- **Guided Style Discovery** — Answer mood/tone questions, get 3 visual previews, pick your favorite.
- **Multi-Format Input** — PDF, DOCX, Markdown, plain text, [JSON Resume](https://jsonresume.org), or direct text.
- **Interactive Components** — Scroll-triggered reveals, floating nav, animated skill bars, experience timeline, 3D tilt effects.
- **Print-Friendly** — `@media print` styles for clean PDF export via Ctrl+P.
- **Accessible** — Semantic HTML5, WCAG AA contrast, keyboard navigation, `prefers-reduced-motion` support.
- **Responsive** — `clamp()`-based sizing that works from mobile to desktop.

## Available Presets

| Preset             | Vibe                     | Best For                            |
| ------------------ | ------------------------ | ----------------------------------- |
| Midnight Architect | Sophisticated, premium   | Executives, consultants             |
| Neon Terminal      | Hacker-chic, developer   | Software engineers, DevOps          |
| Dark Luxe          | Elegant, editorial       | Creative directors, marketing       |
| Cosmic Depth       | Bold, futuristic         | Tech founders, AI/ML engineers      |
| Clean Slate        | Minimal, Swiss-inspired  | Designers, product managers         |
| Paper Craft        | Warm, tactile            | Writers, educators, academics       |
| Soft Blueprint     | Technical, approachable  | Engineers, data scientists          |
| Brutalist Mono     | Raw, anti-design         | Brand strategists, standout seekers |
| Sage Garden        | Nature-inspired, calming | HR, wellness, educators             |
| Retro Ink          | Vintage editorial        | Journalists, personal brands        |

## Installation

```bash
npx skills add https://github.com/Yukiniro/skills --skill frontend-resume
```

## Quick Start

Tell your AI coding assistant:

```
Convert this PDF resume into an interactive web page
```

Or provide resume content directly:

```
Create an interactive HTML resume with the following info: [paste your resume text]
```

The skill walks you through:

1. **Content extraction** — Parse your resume file or text into structured sections
2. **Style discovery** — Choose a preset directly or explore 3 visual previews
3. **Generation** — Produce a single self-contained HTML file
4. **Delivery** — Open in browser, ready to deploy or print

## Project Structure

```
frontend-resume/
├── SKILL.md                           # Skill definition & workflow
├── README.md
├── LICENSE.txt
├── scripts/
│   └── extract_resume.py              # Multi-format resume text extractor
└── references/
    ├── STYLE_PRESETS.md                # Full preset definitions (colors, fonts, CSS variables)
    ├── RESUME_COMPONENTS.md            # Interactive component CSS/JS patterns
    └── HTML_ARCHITECTURE.md            # Base HTML template & accessibility checklist
```

## Resume Extraction

The included Python script handles text extraction from multiple formats:

```bash
python scripts/extract_resume.py resume.pdf
python scripts/extract_resume.py resume.docx
python scripts/extract_resume.py resume.md --format json
```

| Format      | Extensions | Dependency                           |
| ----------- | ---------- | ------------------------------------ |
| PDF         | `.pdf`     | `pdfplumber` (preferred) or `PyPDF2` |
| Word        | `.docx`    | `python-docx`                        |
| Markdown    | `.md`      | None                                 |
| Plain Text  | `.txt`     | None                                 |
| JSON Resume | `.json`    | None                                 |

## Output

A single self-contained HTML file with:

- All CSS in `<style>` tags
- All JS in `<script>` tags
- Font imports via `<link>` (with system font fallbacks)
- Semantic HTML5 structure (`<header>`, `<main>`, `<section>`, `<nav>`)

The output file can be:

- Opened directly in any browser
- Deployed to any static hosting (GitHub Pages, Netlify, Vercel, etc.)
- Printed to PDF via Ctrl+P / Cmd+P
- Shared as a single file — no server required

## Inspiration

This skill is inspired by [frontend-slides](https://github.com/zarazhangrui/frontend-slides) — a Claude Code skill that creates stunning HTML presentations from scratch or PowerPoint files. Frontend Resume adapts its core philosophy (zero dependencies, visual style discovery, anti-AI-slop aesthetics) from slide decks to interactive resume websites.

## License

[MIT](LICENSE.txt)
