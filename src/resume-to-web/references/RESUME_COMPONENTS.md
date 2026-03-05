# Resume Interactive Components

CSS/JS patterns for resume-specific interactive elements. Each component is self-contained and can be mixed into any style preset.

---

## Table of Contents

1. [Scroll Reveal System](#1-scroll-reveal-system)
2. [Floating Navigation](#2-floating-navigation)
3. [Hero / Header Section](#3-hero--header-section)
4. [Experience Timeline](#4-experience-timeline)
5. [Animated Skill Bars](#5-animated-skill-bars)
6. [Project Cards Grid](#6-project-cards-grid)
7. [Education Section](#7-education-section)
8. [Contact Section](#8-contact-section)
9. [Scroll Progress Bar](#9-scroll-progress-bar)
10. [Back-to-Top Button](#10-back-to-top-button)
11. [3D Tilt Effect](#11-3d-tilt-effect)

---

## 1. Scroll Reveal System

Core animation system. All `.reveal` elements animate when entering viewport.

```css
/* Base reveal - hidden state */
.reveal {
    opacity: 0;
    transform: translateY(var(--reveal-distance, 30px));
    transition: opacity var(--reveal-duration, 0.7s) var(--ease-out-expo),
                transform var(--reveal-duration, 0.7s) var(--ease-out-expo);
}

/* Visible state - triggered by IntersectionObserver */
.reveal.visible {
    opacity: 1;
    transform: translateY(0);
}

/* Stagger delays for child elements */
.reveal.delay-1 { transition-delay: 0.1s; }
.reveal.delay-2 { transition-delay: 0.2s; }
.reveal.delay-3 { transition-delay: 0.3s; }
.reveal.delay-4 { transition-delay: 0.4s; }
.reveal.delay-5 { transition-delay: 0.5s; }

/* Variant: slide from left */
.reveal-left {
    opacity: 0;
    transform: translateX(-30px);
    transition: opacity 0.6s var(--ease-out-expo), transform 0.6s var(--ease-out-expo);
}
.reveal-left.visible { opacity: 1; transform: translateX(0); }

/* Variant: scale in */
.reveal-scale {
    opacity: 0;
    transform: scale(0.95);
    transition: opacity 0.6s var(--ease-out-expo), transform 0.6s var(--ease-out-expo);
}
.reveal-scale.visible { opacity: 1; transform: scale(1); }

/* Variant: blur in */
.reveal-blur {
    opacity: 0;
    filter: blur(8px);
    transition: opacity 0.8s var(--ease-out-expo), filter 0.8s var(--ease-out-expo);
}
.reveal-blur.visible { opacity: 1; filter: blur(0); }

/* Reduced motion */
@media (prefers-reduced-motion: reduce) {
    .reveal, .reveal-left, .reveal-scale, .reveal-blur {
        opacity: 1;
        transform: none;
        filter: none;
        transition: none;
    }
}
```

```javascript
/* IntersectionObserver for reveals */
const revealObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('visible');
        }
    });
}, { threshold: 0.1, rootMargin: '0px 0px -50px 0px' });

document.querySelectorAll('.reveal, .reveal-left, .reveal-scale, .reveal-blur')
    .forEach(el => revealObserver.observe(el));
```

---

## 2. Floating Navigation

Fixed sidebar or top navigation with active section tracking.

```html
<nav class="floating-nav" role="navigation" aria-label="Resume sections">
    <button class="nav-toggle" aria-label="Toggle navigation" aria-expanded="false">
        <span></span><span></span><span></span>
    </button>
    <ul class="nav-links">
        <li><a href="#hero" class="active">Home</a></li>
        <li><a href="#about">About</a></li>
        <li><a href="#experience">Experience</a></li>
        <li><a href="#skills">Skills</a></li>
        <li><a href="#projects">Projects</a></li>
        <li><a href="#education">Education</a></li>
        <li><a href="#contact">Contact</a></li>
    </ul>
</nav>
```

```css
.floating-nav {
    position: fixed;
    right: clamp(1rem, 3vw, 2rem);
    top: 50%;
    transform: translateY(-50%);
    z-index: 100;
    display: flex;
    flex-direction: column;
    gap: 0;
}

.nav-toggle { display: none; }

.nav-links {
    list-style: none;
    padding: 0.75rem;
    margin: 0;
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 999px;
    display: flex;
    flex-direction: column;
    gap: 0.25rem;
}

.nav-links a {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 10px;
    height: 10px;
    border-radius: 50%;
    background: var(--text-secondary);
    opacity: 0.3;
    transition: opacity 0.3s, transform 0.3s, background 0.3s;
    text-indent: -9999px; /* Hide text, show dot */
    overflow: hidden;
}

.nav-links a:hover,
.nav-links a.active {
    opacity: 1;
    background: var(--accent);
    transform: scale(1.4);
}

/* Mobile: bottom bar */
@media (max-width: 768px) {
    .floating-nav {
        right: auto;
        top: auto;
        bottom: 0;
        left: 0;
        width: 100%;
        transform: none;
        flex-direction: row;
    }
    .nav-links {
        flex-direction: row;
        justify-content: center;
        width: 100%;
        border-radius: 0;
        padding: 0.5rem;
        gap: 0.75rem;
    }
}

/* Print: hide */
@media print { .floating-nav { display: none; } }
```

```javascript
/* Active section tracking */
const sections = document.querySelectorAll('section[id], header[id]');
const navLinks = document.querySelectorAll('.nav-links a');

const navObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            const id = entry.target.getAttribute('id');
            navLinks.forEach(link => {
                link.classList.toggle('active', link.getAttribute('href') === `#${id}`);
            });
        }
    });
}, { threshold: 0.3, rootMargin: '-10% 0px -60% 0px' });

sections.forEach(section => navObserver.observe(section));

/* Smooth scroll on click */
navLinks.forEach(link => {
    link.addEventListener('click', (e) => {
        e.preventDefault();
        const target = document.querySelector(link.getAttribute('href'));
        if (target) target.scrollIntoView({ behavior: 'smooth' });
    });
});
```

---

## 3. Hero / Header Section

```html
<header id="hero" class="section hero-section">
    <div class="hero-content">
        <h1 class="hero-name reveal">[Name]</h1>
        <p class="hero-title reveal delay-1">[Title / Tagline]</p>
        <div class="hero-contact reveal delay-2">
            <a href="mailto:email" aria-label="Email">email@example.com</a>
            <a href="https://github.com/user" target="_blank" rel="noopener" aria-label="GitHub">GitHub</a>
            <a href="https://linkedin.com/in/user" target="_blank" rel="noopener" aria-label="LinkedIn">LinkedIn</a>
        </div>
    </div>
</header>
```

```css
.hero-section {
    min-height: 100vh;
    min-height: 100dvh;
    display: flex;
    align-items: center;
    justify-content: center;
    text-align: center;
    padding: var(--section-padding);
    position: relative;
}

.hero-name {
    font-family: var(--font-heading);
    font-size: var(--h1-size);
    font-weight: 700;
    color: var(--text-primary);
    line-height: 1.1;
    margin: 0 0 clamp(0.5rem, 2vw, 1rem);
}

.hero-title {
    font-family: var(--font-body);
    font-size: var(--h3-size);
    color: var(--text-secondary);
    margin: 0 0 clamp(1rem, 3vw, 2rem);
}

.hero-contact {
    display: flex;
    flex-wrap: wrap;
    gap: clamp(0.75rem, 2vw, 1.5rem);
    justify-content: center;
}

.hero-contact a {
    color: var(--accent);
    text-decoration: none;
    font-size: var(--small-size);
    transition: color 0.3s;
    border-bottom: 1px solid transparent;
}

.hero-contact a:hover {
    color: var(--accent-hover);
    border-bottom-color: var(--accent-hover);
}

/* Print: ensure links show URLs */
@media print {
    .hero-contact a[href^="http"]::after {
        content: " (" attr(href) ")";
        font-size: 0.7em;
        color: #666;
    }
}
```

---

## 4. Experience Timeline

```html
<section id="experience" class="section">
    <h2 class="section-title reveal">Experience</h2>
    <div class="timeline">
        <article class="timeline-item reveal">
            <div class="timeline-marker"></div>
            <div class="timeline-content">
                <div class="timeline-header">
                    <h3 class="timeline-role">[Role]</h3>
                    <span class="timeline-date">[Start] - [End]</span>
                </div>
                <p class="timeline-company">[Company] &middot; [Location]</p>
                <ul class="timeline-details">
                    <li>[Achievement/responsibility]</li>
                </ul>
            </div>
        </article>
    </div>
</section>
```

```css
.timeline {
    position: relative;
    max-width: var(--content-max-width);
    margin: 0 auto;
    padding-left: clamp(2rem, 5vw, 4rem);
}

/* Vertical line */
.timeline::before {
    content: '';
    position: absolute;
    left: 0;
    top: 0;
    bottom: 0;
    width: 2px;
    background: var(--accent);
    opacity: 0.3;
}

.timeline-item {
    position: relative;
    margin-bottom: clamp(1.5rem, 4vw, 3rem);
    padding-left: clamp(1rem, 3vw, 2rem);
}

.timeline-marker {
    position: absolute;
    left: calc(-1 * clamp(2rem, 5vw, 4rem) + clamp(1rem, 3vw, 2rem));
    top: 0.4rem;
    width: 12px;
    height: 12px;
    border-radius: 50%;
    background: var(--accent);
    border: 2px solid var(--bg-primary);
    z-index: 1;
}

.timeline-header {
    display: flex;
    justify-content: space-between;
    align-items: baseline;
    flex-wrap: wrap;
    gap: 0.5rem;
    margin-bottom: 0.25rem;
}

.timeline-role {
    font-family: var(--font-heading);
    font-size: var(--h3-size);
    font-weight: 600;
    color: var(--text-primary);
    margin: 0;
}

.timeline-date {
    font-size: var(--small-size);
    color: var(--text-secondary);
    white-space: nowrap;
}

.timeline-company {
    font-size: var(--body-size);
    color: var(--accent);
    margin: 0 0 0.75rem;
}

.timeline-details {
    list-style: none;
    padding: 0;
    margin: 0;
}

.timeline-details li {
    font-size: var(--body-size);
    color: var(--text-secondary);
    line-height: 1.6;
    padding-left: 1em;
    position: relative;
    margin-bottom: 0.4rem;
}

.timeline-details li::before {
    content: '\2022';
    color: var(--accent);
    position: absolute;
    left: 0;
}

/* Print: simplify */
@media print {
    .timeline::before { background: #ccc; }
    .timeline-marker { background: #333; border-color: #fff; }
}
```

---

## 5. Animated Skill Bars

```html
<section id="skills" class="section">
    <h2 class="section-title reveal">Skills</h2>
    <div class="skills-grid">
        <div class="skill-category reveal">
            <h3>[Category Name]</h3>
            <div class="skill-item" data-level="90">
                <div class="skill-info">
                    <span class="skill-name">[Skill]</span>
                    <span class="skill-percent">90%</span>
                </div>
                <div class="skill-bar">
                    <div class="skill-fill"></div>
                </div>
            </div>
        </div>
    </div>
</section>
```

```css
.skills-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(min(100%, 300px), 1fr));
    gap: var(--gap);
    max-width: var(--content-max-width);
    margin: 0 auto;
}

.skill-category h3 {
    font-family: var(--font-heading);
    font-size: var(--h3-size);
    color: var(--accent);
    margin: 0 0 clamp(0.75rem, 2vw, 1.5rem);
}

.skill-item {
    margin-bottom: clamp(0.5rem, 1.5vw, 1rem);
}

.skill-info {
    display: flex;
    justify-content: space-between;
    margin-bottom: 0.3rem;
}

.skill-name {
    font-size: var(--body-size);
    color: var(--text-primary);
}

.skill-percent {
    font-size: var(--small-size);
    color: var(--text-secondary);
}

.skill-bar {
    height: 6px;
    background: var(--accent-subtle);
    border-radius: 3px;
    overflow: hidden;
}

.skill-fill {
    height: 100%;
    width: 0;
    background: var(--accent);
    border-radius: 3px;
    transition: width 1s var(--ease-out-expo);
}

/* Animated state */
.skill-item.animated .skill-fill {
    width: var(--level); /* Set via JS */
}

/* Print: show full bars */
@media print {
    .skill-fill {
        width: var(--level) !important;
        transition: none;
    }
}
```

```javascript
/* Animate skill bars when visible */
const skillObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            const items = entry.target.querySelectorAll('.skill-item');
            items.forEach((item, i) => {
                const level = item.getAttribute('data-level');
                item.querySelector('.skill-fill').style.setProperty('--level', level + '%');
                setTimeout(() => item.classList.add('animated'), i * 100);
            });
            skillObserver.unobserve(entry.target);
        }
    });
}, { threshold: 0.2 });

document.querySelectorAll('.skill-category').forEach(cat => skillObserver.observe(cat));
```

---

## 6. Project Cards Grid

```html
<section id="projects" class="section">
    <h2 class="section-title reveal">Projects</h2>
    <div class="projects-grid">
        <article class="project-card reveal">
            <h3 class="project-name">[Project Name]</h3>
            <p class="project-desc">[Description]</p>
            <div class="project-tech">
                <span class="tech-pill">[Tech]</span>
            </div>
            <a href="[url]" class="project-link" target="_blank" rel="noopener">View Project &rarr;</a>
        </article>
    </div>
</section>
```

```css
.projects-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(min(100%, 280px), 1fr));
    gap: var(--gap);
    max-width: var(--content-max-width);
    margin: 0 auto;
}

.project-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: var(--border-radius, 12px);
    padding: clamp(1rem, 3vw, 2rem);
    transition: transform 0.3s, box-shadow 0.3s, border-color 0.3s;
}

.project-card:hover {
    transform: translateY(-4px);
    box-shadow: var(--card-shadow);
    border-color: var(--accent);
}

.project-name {
    font-family: var(--font-heading);
    font-size: var(--h3-size);
    color: var(--text-primary);
    margin: 0 0 0.5rem;
}

.project-desc {
    font-size: var(--body-size);
    color: var(--text-secondary);
    line-height: 1.5;
    margin: 0 0 1rem;
}

.project-tech {
    display: flex;
    flex-wrap: wrap;
    gap: 0.4rem;
    margin-bottom: 1rem;
}

.tech-pill {
    font-size: var(--small-size);
    padding: 0.2em 0.6em;
    border-radius: 999px;
    background: var(--accent-subtle);
    color: var(--accent);
    border: 1px solid var(--border);
}

.project-link {
    font-size: var(--small-size);
    color: var(--accent);
    text-decoration: none;
    font-weight: 500;
    transition: color 0.3s;
}

.project-link:hover { color: var(--accent-hover); }

/* Print: show URLs */
@media print {
    .project-card { border: 1px solid #ddd; break-inside: avoid; }
    .project-link::after { content: " (" attr(href) ")"; font-size: 0.7em; }
}
```

---

## 7. Education Section

```html
<section id="education" class="section">
    <h2 class="section-title reveal">Education</h2>
    <div class="education-list">
        <article class="education-item reveal">
            <div class="edu-header">
                <h3 class="edu-degree">[Degree]</h3>
                <span class="edu-date">[Years]</span>
            </div>
            <p class="edu-school">[School Name]</p>
            <p class="edu-detail">[Honors, GPA, relevant coursework]</p>
        </article>
    </div>
</section>
```

```css
.education-list {
    max-width: var(--content-max-width);
    margin: 0 auto;
    display: flex;
    flex-direction: column;
    gap: clamp(1rem, 3vw, 2rem);
}

.education-item {
    padding: clamp(1rem, 3vw, 2rem);
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: var(--border-radius, 12px);
}

.edu-header {
    display: flex;
    justify-content: space-between;
    align-items: baseline;
    flex-wrap: wrap;
    gap: 0.5rem;
}

.edu-degree {
    font-family: var(--font-heading);
    font-size: var(--h3-size);
    color: var(--text-primary);
    margin: 0;
}

.edu-date {
    font-size: var(--small-size);
    color: var(--text-secondary);
}

.edu-school {
    font-size: var(--body-size);
    color: var(--accent);
    margin: 0.25rem 0 0.5rem;
}

.edu-detail {
    font-size: var(--body-size);
    color: var(--text-secondary);
    margin: 0;
    line-height: 1.5;
}

@media print {
    .education-item { border: 1px solid #ddd; break-inside: avoid; }
}
```

---

## 8. Contact Section

```html
<section id="contact" class="section contact-section">
    <div class="contact-content reveal">
        <h2 class="section-title">Get in Touch</h2>
        <p class="contact-desc">[Brief message about availability]</p>
        <div class="contact-links">
            <a href="mailto:email" class="contact-item">
                <span class="contact-label">Email</span>
                <span class="contact-value">[email]</span>
            </a>
            <a href="[url]" class="contact-item" target="_blank" rel="noopener">
                <span class="contact-label">LinkedIn</span>
                <span class="contact-value">[profile]</span>
            </a>
        </div>
    </div>
</section>
```

```css
.contact-section {
    min-height: 60vh;
    display: flex;
    align-items: center;
    justify-content: center;
    text-align: center;
    padding: var(--section-padding);
}

.contact-desc {
    font-size: var(--body-size);
    color: var(--text-secondary);
    max-width: 500px;
    margin: 0 auto clamp(1.5rem, 4vw, 3rem);
    line-height: 1.6;
}

.contact-links {
    display: flex;
    flex-wrap: wrap;
    gap: clamp(0.75rem, 2vw, 1.5rem);
    justify-content: center;
}

.contact-item {
    display: flex;
    flex-direction: column;
    padding: clamp(0.75rem, 2vw, 1.5rem) clamp(1rem, 3vw, 2rem);
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: var(--border-radius, 12px);
    text-decoration: none;
    transition: transform 0.3s, border-color 0.3s;
}

.contact-item:hover {
    transform: translateY(-2px);
    border-color: var(--accent);
}

.contact-label {
    font-size: var(--small-size);
    color: var(--text-secondary);
    margin-bottom: 0.25rem;
}

.contact-value {
    font-size: var(--body-size);
    color: var(--accent);
}

@media print {
    .contact-item { border: 1px solid #ddd; }
    .contact-item[href^="http"]::after { content: " (" attr(href) ")"; font-size: 0.6em; display: block; color: #666; }
}
```

---

## 9. Scroll Progress Bar

```html
<div class="scroll-progress" role="progressbar" aria-label="Page scroll progress"></div>
```

```css
.scroll-progress {
    position: fixed;
    top: 0;
    left: 0;
    height: 3px;
    width: 0%;
    background: var(--accent);
    z-index: 1000;
    transition: width 0.1s linear;
}

@media print { .scroll-progress { display: none; } }
```

```javascript
window.addEventListener('scroll', () => {
    const scrollTop = window.scrollY;
    const docHeight = document.documentElement.scrollHeight - window.innerHeight;
    const progress = docHeight > 0 ? (scrollTop / docHeight) * 100 : 0;
    document.querySelector('.scroll-progress').style.width = progress + '%';
}, { passive: true });
```

---

## 10. Back-to-Top Button

```html
<button class="back-to-top" aria-label="Back to top">&uarr;</button>
```

```css
.back-to-top {
    position: fixed;
    bottom: clamp(1rem, 3vw, 2rem);
    right: clamp(1rem, 3vw, 2rem);
    width: 40px;
    height: 40px;
    border-radius: 50%;
    background: var(--accent);
    color: var(--bg-primary);
    border: none;
    cursor: pointer;
    font-size: 1.2rem;
    opacity: 0;
    transform: translateY(10px);
    transition: opacity 0.3s, transform 0.3s;
    z-index: 99;
}

.back-to-top.visible {
    opacity: 1;
    transform: translateY(0);
}

.back-to-top:hover {
    background: var(--accent-hover);
}

@media print { .back-to-top { display: none; } }
```

```javascript
const backToTop = document.querySelector('.back-to-top');
window.addEventListener('scroll', () => {
    backToTop.classList.toggle('visible', window.scrollY > window.innerHeight * 0.5);
}, { passive: true });
backToTop.addEventListener('click', () => {
    window.scrollTo({ top: 0, behavior: 'smooth' });
});
```

---

## 11. 3D Tilt Effect

Optional hover effect for project cards. Apply sparingly.

```javascript
class TiltEffect {
    constructor(element, intensity = 8) {
        this.el = element;
        this.intensity = intensity;
        this.el.style.transformStyle = 'preserve-3d';
        this.el.style.willChange = 'transform';

        this.el.addEventListener('mousemove', (e) => {
            const rect = this.el.getBoundingClientRect();
            const x = (e.clientX - rect.left) / rect.width - 0.5;
            const y = (e.clientY - rect.top) / rect.height - 0.5;
            this.el.style.transform = `perspective(800px) rotateY(${x * this.intensity}deg) rotateX(${-y * this.intensity}deg) translateY(-4px)`;
        });

        this.el.addEventListener('mouseleave', () => {
            this.el.style.transform = 'perspective(800px) rotateY(0) rotateX(0) translateY(0)';
        });
    }
}

/* Apply to project cards (desktop only) */
if (window.matchMedia('(min-width: 768px) and (hover: hover)').matches) {
    document.querySelectorAll('.project-card').forEach(card => new TiltEffect(card));
}
```
