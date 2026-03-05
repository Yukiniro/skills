# HTML Architecture Reference

Base template, mandatory CSS, responsive system, JS architecture, and accessibility patterns for resume-to-web.

---

## Table of Contents

1. [HTML Template](#1-html-template)
2. [Mandatory Base CSS](#2-mandatory-base-css)
3. [CSS Variables Pattern](#3-css-variables-pattern)
4. [JS Architecture](#4-js-architecture)
5. [Print Stylesheet](#5-print-stylesheet)
6. [Accessibility Checklist](#6-accessibility-checklist)

---

## 1. HTML Template

Every generated resume MUST follow this structure:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>[Name] - [Title] | Resume</title>
    <meta name="description" content="Interactive resume of [Name] - [Title]">

    <!-- Font imports (Google Fonts / Fontshare) -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="[FONT_URL]" rel="stylesheet">

    <style>
        /* === CSS RESET === */
        /* === CSS VARIABLES (:root) === */
        /* === BASE TYPOGRAPHY === */
        /* === LAYOUT === */
        /* === COMPONENTS (from RESUME_COMPONENTS.md) === */
        /* === RESPONSIVE BREAKPOINTS === */
        /* === REDUCED MOTION === */
        /* === PRINT STYLES === */
    </style>
</head>
<body>
    <!-- Scroll Progress Bar -->
    <div class="scroll-progress" role="progressbar" aria-label="Page scroll progress"></div>

    <!-- Floating Navigation -->
    <nav class="floating-nav" role="navigation" aria-label="Resume sections">
        <!-- See RESUME_COMPONENTS.md #2 -->
    </nav>

    <main>
        <!-- Hero Section -->
        <header id="hero" class="section hero-section">
            <!-- See RESUME_COMPONENTS.md #3 -->
        </header>

        <!-- About Section (optional) -->
        <section id="about" class="section">
            <div class="section-inner">
                <h2 class="section-title reveal">About</h2>
                <p class="about-text reveal delay-1">[Professional summary]</p>
            </div>
        </section>

        <!-- Experience Section -->
        <section id="experience" class="section">
            <div class="section-inner">
                <!-- See RESUME_COMPONENTS.md #4 -->
            </div>
        </section>

        <!-- Skills Section -->
        <section id="skills" class="section">
            <div class="section-inner">
                <!-- See RESUME_COMPONENTS.md #5 -->
            </div>
        </section>

        <!-- Projects Section (optional) -->
        <section id="projects" class="section">
            <div class="section-inner">
                <!-- See RESUME_COMPONENTS.md #6 -->
            </div>
        </section>

        <!-- Education Section -->
        <section id="education" class="section">
            <div class="section-inner">
                <!-- See RESUME_COMPONENTS.md #7 -->
            </div>
        </section>

        <!-- Contact Section -->
        <section id="contact" class="section contact-section">
            <!-- See RESUME_COMPONENTS.md #8 -->
        </section>
    </main>

    <!-- Back to Top -->
    <button class="back-to-top" aria-label="Back to top">&uarr;</button>

    <script>
        /* === ResumeApp Class === */
        /* === Initialization === */
    </script>
</body>
</html>
```

**Section order is flexible.** Adjust based on section priority from Phase 1:
- Experience-heavy: hero -> about -> experience -> skills -> education -> projects -> contact
- Skills-focused: hero -> about -> skills -> experience -> projects -> education -> contact
- Projects-driven: hero -> about -> projects -> skills -> experience -> education -> contact
- Balanced: hero -> about -> experience -> skills -> projects -> education -> contact

Omit sections with no content. At minimum, include: hero, experience OR skills, contact.

---

## 2. Mandatory Base CSS

Include in ALL resumes. Provides reset, smooth scroll, section layout.

```css
/* === RESET === */
*, *::before, *::after {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
}

html {
    scroll-behavior: smooth;
    -webkit-text-size-adjust: 100%;
}

body {
    font-family: var(--font-body);
    font-size: var(--body-size);
    color: var(--text-primary);
    background: var(--bg-primary);
    line-height: 1.6;
    overflow-x: hidden;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
}

img { max-width: 100%; height: auto; display: block; }
a { color: inherit; }
ul, ol { list-style: none; }

/* === SECTION LAYOUT === */
.section {
    padding: var(--section-padding);
    position: relative;
}

.section-inner {
    max-width: var(--content-max-width);
    margin: 0 auto;
}

.section-title {
    font-family: var(--font-heading);
    font-size: var(--h2-size);
    font-weight: 700;
    color: var(--text-primary);
    margin-bottom: clamp(1.5rem, 4vw, 3rem);
}

/* === EASING === */
:root {
    --ease-out-expo: cubic-bezier(0.16, 1, 0.3, 1);
}

/* === SELECTION === */
::selection {
    background: var(--accent);
    color: var(--bg-primary);
}
```

---

## 3. CSS Variables Pattern

Every preset MUST define these variables in `:root`. Values come from STYLE_PRESETS.md.

```css
:root {
    /* === COLORS (from preset) === */
    --bg-primary: ;
    --bg-secondary: ;
    --bg-card: ;
    --text-primary: ;
    --text-secondary: ;
    --accent: ;
    --accent-hover: ;
    --accent-subtle: ;
    --border: ;

    /* === TYPOGRAPHY (from preset) === */
    --font-heading: ;
    --font-body: ;

    /* === RESPONSIVE TYPE SCALE (mandatory) === */
    --h1-size: clamp(2rem, 6vw, 4.5rem);
    --h2-size: clamp(1.5rem, 4vw, 2.5rem);
    --h3-size: clamp(1.1rem, 2.5vw, 1.5rem);
    --body-size: clamp(0.875rem, 1.5vw, 1.125rem);
    --small-size: clamp(0.75rem, 1.2vw, 0.875rem);

    /* === SPACING (mandatory) === */
    --section-padding: clamp(3rem, 8vh, 8rem) clamp(1rem, 5vw, 6rem);
    --content-max-width: min(90vw, 1100px);
    --gap: clamp(1rem, 3vw, 2rem);

    /* === ANIMATION (mandatory) === */
    --ease-out-expo: cubic-bezier(0.16, 1, 0.3, 1);
    --reveal-duration: 0.7s;
    --reveal-distance: 30px;

    /* === COMPONENTS === */
    --border-radius: 12px;
    --card-shadow: 0 4px 24px rgba(0, 0, 0, 0.1);
}
```

### Responsive Overrides

```css
/* Small screens */
@media (max-width: 640px) {
    :root {
        --h1-size: clamp(1.75rem, 8vw, 3rem);
        --section-padding: clamp(2rem, 6vh, 4rem) clamp(1rem, 4vw, 2rem);
    }
}

/* Short viewports */
@media (max-height: 600px) {
    :root {
        --section-padding: clamp(1.5rem, 4vh, 3rem) clamp(1rem, 4vw, 2rem);
    }
}
```

---

## 4. JS Architecture

Single `ResumeApp` class that initializes all interactive features.

```javascript
class ResumeApp {
    constructor() {
        this.initRevealObserver();
        this.initNavTracking();
        this.initSkillBars();
        this.initScrollProgress();
        this.initBackToTop();
        this.initSmoothScroll();
    }

    /* Scroll reveal via IntersectionObserver */
    initRevealObserver() {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('visible');
                }
            });
        }, { threshold: 0.1, rootMargin: '0px 0px -50px 0px' });

        document.querySelectorAll('.reveal, .reveal-left, .reveal-scale, .reveal-blur')
            .forEach(el => observer.observe(el));
    }

    /* Active nav section tracking */
    initNavTracking() {
        const sections = document.querySelectorAll('section[id], header[id]');
        const navLinks = document.querySelectorAll('.nav-links a');
        if (!navLinks.length) return;

        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const id = entry.target.getAttribute('id');
                    navLinks.forEach(link => {
                        link.classList.toggle('active',
                            link.getAttribute('href') === `#${id}`);
                    });
                }
            });
        }, { threshold: 0.3, rootMargin: '-10% 0px -60% 0px' });

        sections.forEach(s => observer.observe(s));
    }

    /* Animated skill bars */
    initSkillBars() {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const items = entry.target.querySelectorAll('.skill-item');
                    items.forEach((item, i) => {
                        const level = item.getAttribute('data-level');
                        const fill = item.querySelector('.skill-fill');
                        if (fill) {
                            fill.style.setProperty('--level', level + '%');
                            setTimeout(() => item.classList.add('animated'), i * 100);
                        }
                    });
                    observer.unobserve(entry.target);
                }
            });
        }, { threshold: 0.2 });

        document.querySelectorAll('.skill-category, .skills-grid')
            .forEach(el => observer.observe(el));
    }

    /* Scroll progress bar */
    initScrollProgress() {
        const bar = document.querySelector('.scroll-progress');
        if (!bar) return;
        window.addEventListener('scroll', () => {
            const scrollTop = window.scrollY;
            const docHeight = document.documentElement.scrollHeight - window.innerHeight;
            bar.style.width = (docHeight > 0 ? (scrollTop / docHeight) * 100 : 0) + '%';
        }, { passive: true });
    }

    /* Back to top button */
    initBackToTop() {
        const btn = document.querySelector('.back-to-top');
        if (!btn) return;
        window.addEventListener('scroll', () => {
            btn.classList.toggle('visible', window.scrollY > window.innerHeight * 0.5);
        }, { passive: true });
        btn.addEventListener('click', () => {
            window.scrollTo({ top: 0, behavior: 'smooth' });
        });
    }

    /* Smooth scroll for nav links */
    initSmoothScroll() {
        document.querySelectorAll('.nav-links a, a[href^="#"]').forEach(link => {
            link.addEventListener('click', (e) => {
                const href = link.getAttribute('href');
                if (href && href.startsWith('#')) {
                    e.preventDefault();
                    const target = document.querySelector(href);
                    if (target) target.scrollIntoView({ behavior: 'smooth' });
                }
            });
        });
    }
}

/* Initialize on DOM ready */
document.addEventListener('DOMContentLoaded', () => new ResumeApp());
```

### Optional Enhancements (per preset)

Add these ONLY when the chosen preset calls for them:

- **TiltEffect** — for project cards (Midnight Architect, Cosmic Depth)
- **Typewriter** — for hero name (Neon Terminal)
- **Particle canvas** — for background (Cosmic Depth)
- **Scanline overlay** — CSS-only (Neon Terminal)

---

## 5. Print Stylesheet

MANDATORY in all resumes.

```css
@media print {
    /* Remove interactive/decorative elements */
    .scroll-progress,
    .floating-nav,
    .back-to-top {
        display: none !important;
    }

    /* Reset colors for print */
    body {
        background: white !important;
        color: #1a1a1a !important;
        font-size: 11pt;
        line-height: 1.4;
    }

    /* Remove animations */
    .reveal, .reveal-left, .reveal-scale, .reveal-blur {
        opacity: 1 !important;
        transform: none !important;
        filter: none !important;
        transition: none !important;
    }

    /* Section spacing for print */
    .section {
        padding: 1rem 0 !important;
        page-break-inside: avoid;
    }

    .hero-section {
        min-height: auto !important;
        padding: 1.5rem 0 !important;
    }

    /* Show link URLs */
    a[href^="http"]::after,
    a[href^="mailto"]::after {
        content: " (" attr(href) ")";
        font-size: 0.75em;
        color: #666;
        word-break: break-all;
    }

    /* Card borders for print */
    .project-card,
    .education-item,
    .contact-item {
        border: 1px solid #ddd !important;
        box-shadow: none !important;
        background: white !important;
        break-inside: avoid;
    }

    /* Timeline for print */
    .timeline::before { background: #ccc !important; }
    .timeline-marker { background: #333 !important; }

    /* Skill bars always full */
    .skill-fill {
        transition: none !important;
    }
    .skill-item.animated .skill-fill,
    .skill-fill {
        width: var(--level) !important;
        background: #333 !important;
    }

    /* Page setup */
    @page {
        margin: 1.5cm;
        size: A4;
    }
}
```

---

## 6. Accessibility Checklist

Verify these BEFORE delivering:

- [ ] Semantic HTML: `<header>`, `<main>`, `<section>`, `<article>`, `<nav>`, `<footer>` used correctly
- [ ] All sections have `id` attributes for navigation
- [ ] `<nav>` has `role="navigation"` and `aria-label`
- [ ] All links have meaningful text or `aria-label`
- [ ] External links have `target="_blank"` with `rel="noopener"`
- [ ] `<html lang="en">` (or appropriate language) set
- [ ] Color contrast meets WCAG AA (4.5:1 for body text, 3:1 for large text)
- [ ] `@media (prefers-reduced-motion: reduce)` disables animations:
  ```css
  @media (prefers-reduced-motion: reduce) {
      *, *::before, *::after {
          animation-duration: 0.01ms !important;
          transition-duration: 0.2s !important;
      }
      html { scroll-behavior: auto; }
  }
  ```
- [ ] Interactive elements (buttons, links) have visible focus styles
- [ ] Back-to-top button has `aria-label`
- [ ] Scroll progress bar has `role="progressbar"` and `aria-label`
- [ ] Tab order is logical (follows visual order)
