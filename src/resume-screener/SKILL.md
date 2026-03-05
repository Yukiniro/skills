---
name: resume-screener
description: Evaluate and grade resumes against job requirements using a 10-level grading system (C, B-, B, B+, A-, A, A+, S, SS, SSS). Provides multi-dimensional scoring with evidence-based reasoning and hiring recommendations. Use when screening candidates, comparing applicants, assessing resume-job fit, or filtering resumes. Supports Chinese and English resumes in any format (PDF, DOCX, text, image).
---

# Resume Screener

Systematically evaluate resumes against job requirements. Produce evidence-based, multi-dimensional grades with clear reasoning and actionable hiring recommendations.

**Core principles**: Fair, consistent, evidence-backed. Every claim must cite specific resume content. Distinguish "not mentioned" from "not possessed."

---

## Phase 0: Input Collection

Detect what the user has provided:

- **Resume + JD both provided** → Proceed to Phase 1
- **Resume only** → Ask user for job requirements / JD
- **JD only** → Ask user for resume
- **Neither** → Ask user for both

Accepted resume formats:
- PDF → Use Read tool
- DOCX → Use Read tool
- Plain text → Use directly
- Image (screenshot/scan) → Use Read tool for visual reading
- If content cannot be extracted → Ask user to paste the text

Accepted JD formats: text, structured requirements list, or file.

---

## Phase 1: Content Extraction & Structuring

### 1.1 Extract Resume Content

Parse resume into structured sections:
- **Personal info**: Name, contact, location
- **Education**: Degrees, schools, dates, GPA/honors
- **Work experience**: Companies, roles, dates, responsibilities, quantified achievements
- **Skills**: Technical skills, tools, languages, frameworks
- **Projects**: Name, description, tech stack, impact metrics
- **Certifications & awards**
- **Publications / patents** (if any)
- **Languages spoken**

### 1.2 Extract JD Requirements

Parse JD into:
- **Hard requirements** (must-haves): Required degree, years of experience, certifications, specific skills
- **Preferred qualifications** (nice-to-haves)
- **Role responsibilities**
- **Seniority level** (inferred if not explicit)
- **Industry/domain context**

Present a brief summary of extracted content for user confirmation.

---

## Phase 2: Requirement Analysis

In a `<thinking>` block, analyze:
1. Which requirements are hard (must-have) vs. soft (preferred)?
2. What seniority level does the JD imply?
3. What industry context matters?
4. What are the dealbreakers?
5. Assign weight (High/Medium/Low) to each of the 9 dimensions based on JD emphasis.

Weight assignment guidance:
- Dimensions explicitly required in JD → **High**
- Dimensions implied or preferred → **Medium**
- Dimensions not mentioned or irrelevant to role → **Low**
- For management roles: Leadership weight = High
- For junior roles: Education weight = High, Leadership weight = Low
- For technical IC roles: Skills + Projects weight = High

---

## Phase 3: Multi-Dimensional Evaluation

Read `references/EVALUATION_DIMENSIONS.md` for detailed criteria per dimension.

Evaluate each of the 9 dimensions:

1. **Education Background Match**
2. **Work Experience Relevance & Depth**
3. **Technical/Professional Skills Match**
4. **Project Experience Relevance**
5. **Leadership & Management Capability**
6. **Industry Domain Knowledge**
7. **Career Progression Trajectory**
8. **Certifications & Achievements**
9. **Communication & Soft Skills Indicators**

For each dimension:
1. State the relevant JD requirement
2. Find specific evidence in the resume (quote or reference)
3. Assess the match quality
4. Assign a grade (C / B- / B / B+ / A- / A / A+ / S / SS / SSS)
5. Write 1-3 sentences of reasoning citing evidence

---

## Phase 4: Overall Grading & Recommendation

Read `references/GRADING_RUBRIC.md` for grade definitions and rules.

1. Review all 9 dimensional grades with their weights.
2. Check hard-requirement grade cap rules:
   - All hard reqs met → No cap
   - 1 major hard req unmet → Overall capped at B+
   - 2+ hard reqs unmet → Overall capped at B
3. Calculate weighted overall assessment.
4. Determine overall grade (C through SSS).
5. Write 3-5 sentence overall assessment.
6. Generate hiring recommendation:
   - **Strong Pass**: Proceed to interview immediately (A+ and above)
   - **Pass**: Recommend for interview (A- to A)
   - **Borderline**: Consider if candidate pool is thin (B to B+)
   - **Fail**: Does not meet requirements (C to B-)
7. List top 3 strengths and top 3 concerns with evidence.
8. Suggest 2-3 interview focus areas.

---

## Phase 5: Report Delivery

Read `references/OUTPUT_FORMAT.md` for report templates.

1. Generate the evaluation report using the appropriate language template (match user's language).
2. Present summary first (overall grade + recommendation), then detailed breakdown.
3. After delivering the report, ask if the user wants to:
   - Evaluate another resume against the same JD
   - Compare this candidate with a previously evaluated one
   - Adjust dimension weighting
   - Deep-dive into a specific dimension

---

## Evaluation Principles

- **Evidence-based**: Every assessment must cite specific resume content. No unsupported claims.
- **Fair and consistent**: Same criteria applied regardless of name, gender, age, or background.
- **Nuanced**: Acknowledge gray areas. Do not force binary judgments on ambiguous situations.
- **Context-aware**: Consider industry norms for career patterns, tenure expectations, and role titles.
- **Bilingual sensitivity**:
  - Chinese resumes: Understand 985/211/C9 university tiers, BAT/TMD company tiers, Chinese career conventions
  - English resumes: Understand Ivy League/Russell Group, FAANG/Fortune 500, Western career conventions
- **Conservative on missing info**: Absence of information is not a negative signal. Grade as "insufficient data" for affected dimensions rather than penalizing.
- **No format bias**: Focus on substance, not resume aesthetics.

---

## Troubleshooting

- **Image-based PDF with no extractable text**: Ask user to paste content or provide a text version.
- **Very short resume**: Note limited information, grade conservatively, flag affected dimensions as "insufficient data."
- **JD too vague**: Ask user to clarify key requirements before proceeding.
- **Multiple positions in JD**: Ask which role to evaluate against.
- **Batch evaluation**: When evaluating multiple resumes, use the batch comparison format from `references/OUTPUT_FORMAT.md` and maintain consistent grading standards across all candidates.
