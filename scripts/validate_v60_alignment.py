#!/usr/bin/env python3
"""Validate Version 6.0 alignment across labs, PPT, LG, LP and Markdown."""

from __future__ import annotations

import hashlib
import json
import re
import urllib.parse
import zipfile
from pathlib import Path

from docx import Document
from pptx import Presentation


ROOT = Path(__file__).resolve().parents[1]
COURSEWARE = ROOT / "courseware"
VERSION = "6.0"
TITLE = "Business Process Automation with Power Automate and Copilot Studio Agents"


def fail(message: str) -> None:
    print(f"FAIL: {message}")
    raise SystemExit(1)


def office_text(path: Path) -> str:
    document = Document(path)
    parts = [paragraph.text for paragraph in document.paragraphs]
    for table in document.tables:
        for row in table.rows:
            parts.extend(cell.text for cell in row.cells)
    return "\n".join(parts)


def ppt_slide_text(slide) -> str:
    return "\n".join(
        shape.text
        for shape in slide.shapes
        if getattr(shape, "has_text_frame", False) and shape.text.strip()
    )


def archive_media_hashes(path: Path, prefix: str) -> set[str]:
    with zipfile.ZipFile(path) as archive:
        return {
            hashlib.sha256(archive.read(name)).hexdigest()
            for name in archive.namelist()
            if name.startswith(prefix) and not name.endswith("/")
        }


def validate_markdown_links(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    missing: list[str] = []
    for target in re.findall(r"!?\[[^\]]*\]\(([^)]+)\)", text):
        target = target.strip().strip("<>")
        if not target or target.startswith(("http://", "https://", "#", "mailto:")):
            continue
        target = urllib.parse.unquote(target.split("#", 1)[0].split("?", 1)[0])
        resolved = (path.parent / target).resolve()
        if not resolved.exists():
            missing.append(f"{path.relative_to(ROOT)} -> {target}")
    return missing


manifest = json.loads((COURSEWARE / "alignment_manifest.json").read_text(encoding="utf-8"))
slide_map = json.loads((COURSEWARE / "slide_map.json").read_text(encoding="utf-8"))
if manifest["version"] != VERSION or slide_map["version"] != VERSION:
    fail("manifest or slide map version is not 6.0")
if manifest["deck"] != slide_map["deck"]:
    fail("manifest and slide map deck filenames differ")
if [lab["number"] for lab in manifest["labs"]] != list(range(1, 11)):
    fail("manifest does not contain the canonical Lab 1-10 sequence")

deck_path = COURSEWARE / manifest["deck"]
deck_pdf = deck_path.with_suffix(".pdf")
lg_md = ROOT / "LEARNER-GUIDE.md"
lg_docx = COURSEWARE / f"LG-{TITLE}.docx"
lg_pdf = COURSEWARE / f"LG-{TITLE}.pdf"
lp_docx = COURSEWARE / f"LP-{TITLE}.docx"
lp_pdf = COURSEWARE / f"LP-{TITLE}.pdf"
readme = ROOT / "README.md"
for path in (deck_path, deck_pdf, lg_md, lg_docx, lg_pdf, lp_docx, lp_pdf, readme):
    if not path.exists():
        fail(f"missing artifact: {path.relative_to(ROOT)}")

lg_text = lg_md.read_text(encoding="utf-8")
readme_text = readme.read_text(encoding="utf-8")
lg_doc_text = office_text(lg_docx)
lp_doc_text = office_text(lp_docx)
presentation = Presentation(deck_path)
if len(presentation.slides) != slide_map["slides"] or len(presentation.slides) != 113:
    fail("deck slide count differs from the Version 6.0 slide map")

deck_text = "\n".join(ppt_slide_text(slide) for slide in presentation.slides)
cover_text = ppt_slide_text(presentation.slides[0])
if f"Version {VERSION}" not in cover_text:
    fail("deck cover does not show Version 6.0")
for label, text in (
    ("PPT", deck_text),
    ("Learner Guide Markdown", lg_text),
    ("LG DOCX", lg_doc_text),
    ("LP DOCX", lp_doc_text),
):
    if VERSION not in text:
        fail(f"{label} does not contain Version 6.0")
if manifest["deck"] not in lp_doc_text:
    fail("LP does not name the Version 6.0 deck")
if "Courseware-6.0" not in readme_text or manifest["deck"] not in readme_text:
    fail("README version or deck reference is not Version 6.0")

concept_groups = {
    "cloud flow types": ("Instant cloud flow", "Scheduled cloud flow", "Automated cloud flow"),
    "workflow anatomy": ("Trigger", "Actions", "Output"),
    "agent building blocks": ("Knowledge", "Skills", "Tools", "Memory", "Model", "Instructions"),
    "web foundations": ("HTTP request", "Webhook", "JSON"),
}
for group, terms in concept_groups.items():
    for term in terms:
        if term.lower() not in deck_text.lower():
            fail(f"PPT missing {group} concept: {term}")
        if term.lower() not in lg_text.lower():
            fail(f"Learner Guide missing {group} concept: {term}")

ppt_media_hashes = archive_media_hashes(deck_path, "ppt/media/")
lg_media_hashes = archive_media_hashes(lg_docx, "word/media/")
for lab in manifest["labs"]:
    lab_path = ROOT / lab["path"]
    lab_text = lab_path.read_text(encoding="utf-8")
    if not lab_text.startswith(f"# {lab['title']}\n"):
        fail(f"{lab['id']} heading differs from canonical title")
    if f"Approximately {lab['duration_minutes']} minutes." not in lab_text:
        fail(f"{lab['id']} duration differs from manifest")
    for required in ("## Workflow visual", "## Detailed step-by-step", "## Troubleshooting"):
        if required not in lab_text:
            fail(f"{lab['id']} missing section: {required}")
    flowchart = lab_path.parent / "assets" / "flowchart.png"
    if not flowchart.exists() or "assets/flowchart.png" not in lab_text:
        fail(f"{lab['id']} flowchart missing or not referenced")
    flow_hash = hashlib.sha256(flowchart.read_bytes()).hexdigest()
    if flow_hash not in ppt_media_hashes:
        fail(f"{lab['id']} flowchart is not embedded in PPT")
    if flow_hash not in lg_media_hashes:
        fail(f"{lab['id']} flowchart is not embedded in LG")
    for label, text in (
        ("Learner Guide Markdown", lg_text),
        ("LG DOCX", lg_doc_text),
        ("LP DOCX", lp_doc_text),
        ("README", readme_text),
    ):
        if lab["title"] not in text:
            fail(f"{lab['id']} canonical title missing from {label}")
    if slide_map["labs"][lab["id"]] != lab["slides"]:
        fail(f"{lab['id']} slide range differs between manifest and slide map")
    slide_text = ppt_slide_text(presentation.slides[lab["overview_slide"] - 1])
    if lab["title"] not in slide_text:
        fail(f"{lab['id']} canonical title missing from PPT overview slide")
    if lab["slides"].replace("-", "–") not in lp_doc_text:
        fail(f"{lab['id']} slide range missing from LP")

missing_links: list[str] = []
for path in [readme, lg_md] + [ROOT / lab["path"] for lab in manifest["labs"]]:
    missing_links.extend(validate_markdown_links(path))
if missing_links:
    fail("broken Markdown links:\n  " + "\n  ".join(missing_links))

print("PASS: Version 6.0 courseware alignment validated")
print("  113-slide concept-first deck and canonical Lab 1-10 sequence")
print("  Core flow, trigger, agent and HTTP/webhook concepts present in PPT and LG")
print("  PPT/LG use the same 10 workflow visuals")
print("  LG, LP, README, manifest and slide map use the same titles, durations and ranges")
print("  Markdown links checked with 0 missing targets")
