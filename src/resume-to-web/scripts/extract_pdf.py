#!/usr/bin/env python3
"""
PDF Resume Text Extractor for resume-to-web skill.

Usage:
    python extract_pdf.py <resume.pdf> [--format json|text]

Extracts text from a PDF resume with structural hints.
Uses pdfplumber (primary) with PyPDF2 fallback.
"""

import sys
import json
import os


def extract_with_pdfplumber(file_path):
    """Extract text using pdfplumber with layout and font size hints."""
    import pdfplumber

    pages_data = []
    with pdfplumber.open(file_path) as pdf:
        for page_num, page in enumerate(pdf.pages):
            lines = []
            # Extract words with font size info
            chars = page.chars
            if chars:
                current_line = []
                current_top = None
                for char in chars:
                    top = round(char["top"], 1)
                    if current_top is None:
                        current_top = top
                    # New line if vertical position changes significantly
                    if abs(top - current_top) > 3:
                        if current_line:
                            text = "".join(c["text"] for c in current_line).strip()
                            if text:
                                avg_size = sum(c.get("size", 12) for c in current_line) / len(current_line)
                                is_bold = any("Bold" in str(c.get("fontname", "")) or "bold" in str(c.get("fontname", "")) for c in current_line)
                                lines.append({
                                    "text": text,
                                    "font_size": round(avg_size, 1),
                                    "is_bold": is_bold,
                                })
                        current_line = [char]
                        current_top = top
                    else:
                        current_line.append(char)
                # Last line
                if current_line:
                    text = "".join(c["text"] for c in current_line).strip()
                    if text:
                        avg_size = sum(c.get("size", 12) for c in current_line) / len(current_line)
                        is_bold = any("Bold" in str(c.get("fontname", "")) or "bold" in str(c.get("fontname", "")) for c in current_line)
                        lines.append({
                            "text": text,
                            "font_size": round(avg_size, 1),
                            "is_bold": is_bold,
                        })
            else:
                # Fallback: extract raw text
                raw_text = page.extract_text()
                if raw_text:
                    for line in raw_text.split("\n"):
                        stripped = line.strip()
                        if stripped:
                            lines.append({
                                "text": stripped,
                                "font_size": 12.0,
                                "is_bold": False,
                            })

            pages_data.append({
                "page": page_num + 1,
                "lines": lines,
            })

    return pages_data


def extract_with_pypdf2(file_path):
    """Extract text using PyPDF2 as fallback (no font info)."""
    from PyPDF2 import PdfReader

    reader = PdfReader(file_path)
    pages_data = []

    if reader.is_encrypted:
        try:
            reader.decrypt("")
        except Exception:
            print("ERROR: PDF is password-protected. Please provide an unencrypted PDF.", file=sys.stderr)
            sys.exit(1)

    for page_num, page in enumerate(reader.pages):
        text = page.extract_text() or ""
        lines = []
        for line in text.split("\n"):
            stripped = line.strip()
            if stripped:
                lines.append({
                    "text": stripped,
                    "font_size": 12.0,
                    "is_bold": False,
                })
        pages_data.append({
            "page": page_num + 1,
            "lines": lines,
        })

    return pages_data


def format_as_text(pages_data):
    """Format extracted data as plain text."""
    output = []
    for page in pages_data:
        output.append(f"--- Page {page['page']} ---")
        for line in page["lines"]:
            prefix = ""
            if line["font_size"] > 14:
                prefix = "[H] "  # Likely heading
            elif line["is_bold"]:
                prefix = "[B] "  # Bold text
            output.append(f"{prefix}{line['text']}")
        output.append("")
    return "\n".join(output)


def main():
    if len(sys.argv) < 2:
        print("Usage: python extract_pdf.py <resume.pdf> [--format json|text]", file=sys.stderr)
        sys.exit(1)

    file_path = sys.argv[1]
    output_format = "text"

    if "--format" in sys.argv:
        idx = sys.argv.index("--format")
        if idx + 1 < len(sys.argv):
            output_format = sys.argv[idx + 1]

    if not os.path.exists(file_path):
        print(f"ERROR: File not found: {file_path}", file=sys.stderr)
        sys.exit(1)

    if not file_path.lower().endswith(".pdf"):
        print("WARNING: File does not have .pdf extension.", file=sys.stderr)

    # Try pdfplumber first, then PyPDF2
    pages_data = None
    extractor_used = None

    try:
        pages_data = extract_with_pdfplumber(file_path)
        extractor_used = "pdfplumber"
    except ImportError:
        try:
            pages_data = extract_with_pypdf2(file_path)
            extractor_used = "PyPDF2"
        except ImportError:
            print("ERROR: No PDF library available.", file=sys.stderr)
            print("Install one of:", file=sys.stderr)
            print("  pip install pdfplumber", file=sys.stderr)
            print("  pip install PyPDF2", file=sys.stderr)
            sys.exit(1)
    except Exception as e:
        print(f"ERROR: pdfplumber failed: {e}", file=sys.stderr)
        try:
            pages_data = extract_with_pypdf2(file_path)
            extractor_used = "PyPDF2 (fallback)"
        except ImportError:
            print("ERROR: PyPDF2 not available as fallback.", file=sys.stderr)
            print("  pip install PyPDF2", file=sys.stderr)
            sys.exit(1)

    # Check for image-only PDFs
    total_text = sum(len(line["text"]) for page in pages_data for line in page["lines"])
    if total_text < 50:
        print("WARNING: Very little text extracted. The PDF may be image-based (scanned).", file=sys.stderr)
        print("Consider using an OCR tool first, or provide resume content as text.", file=sys.stderr)

    print(f"# Extracted with: {extractor_used}", file=sys.stderr)
    print(f"# Pages: {len(pages_data)}", file=sys.stderr)

    if output_format == "json":
        print(json.dumps(pages_data, ensure_ascii=False, indent=2))
    else:
        print(format_as_text(pages_data))


if __name__ == "__main__":
    main()
