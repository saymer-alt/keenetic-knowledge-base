#!/usr/bin/env python3
"""Read-only startup-context, provenance and MkDocs publication guard."""
from pathlib import Path
import ast
import re

ROOT = Path(__file__).resolve().parents[1]
GUIDES = ["docs/agent-guidance/01-mission-and-owner-intent.md","docs/agent-guidance/02-telegram-sources-and-archival.md","docs/agent-guidance/03-knowledge-quality-and-writing.md","docs/agent-guidance/04-scripts-restructuring-and-git.md"]
HEADINGS = ["## Owner-wide design gate — SIMPLICITY-FIRST (2026-10-24)","## 1. What this repository is","## 2. Main mission","## 3. TechnoBypass is a primary source corpus","## 4. Do not destroy the useful junk","## 5. Classification before cleanup","## 6. Knowledge quality rules","## 7. Article style","## 8. Scripts and dangerous examples","## 9. Reuse in the owner's other projects","## 10. Repository restructuring","## 11. README policy","## 12. Git working rules","## 13. What \"good progress\" looks like here","## AI agent engineering upstream research (30.10.2026)"]
SAFETY = ["TechnoBypass","Observed","Confirmed","Historical","Hypothesis","archive/","owner GO","raw Telegram","subscription URLs","COPYRIGHT_AND_LICENSING.md","20 curated","Draft PR","NOT TESTED","main","KAS","source"]

def main():
    agent = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
    size = len(agent.encode("utf-8"))
    assert size <= 12_288, f"AGENTS.md is {size} bytes; 12 KiB max"
    for term in SAFETY:
        assert term.casefold() in agent.casefold(), f"root contract missing: {term}"
    guides_text = ""
    for guide in GUIDES:
        assert f"]({guide})" in agent, f"missing scoped guide link: {guide}"
        content = (ROOT / guide).read_text(encoding="utf-8")
        assert "Сохранённые исходные инструкции" in content, f"missing source marker: {guide}"
        guides_text += content + "\n"
    for heading in HEADINGS:
        assert heading in guides_text, f"original source section lost: {heading}"
    for doc in ["AGENTS.md", *GUIDES]:
        content = (ROOT / doc).read_text(encoding="utf-8")
        for href in re.findall(r"(?<!!)\[[^\]]+\]\(([^)]+)\)", content):
            local = href.split("#", 1)[0]
            if not local or re.match(r"^(?:https?:|mailto:|/)", local, re.I):
                continue
            assert ((ROOT / doc).parent / local).is_file(), f"broken Markdown path: {doc} -> {href}"
    builder = ast.parse((ROOT / "tools/prepare_site_docs.py").read_text(encoding="utf-8"))
    pages = None
    for stmt in builder.body:
        if isinstance(stmt, ast.Assign) and any(isinstance(x, ast.Name) and x.id == "PAGES" for x in stmt.targets):
            pages = ast.literal_eval(stmt.value)
            break
    assert pages is not None, "missing MkDocs explicit PAGES allowlist"
    assert not any("/" in item or item.startswith("agent-guidance") for item in pages), "agent guides must not become site pages"
    assert len(pages) == 20, "unexpected site publishing scope; review copyright before expanding"
    print(f"Agent contract: PASS — {size} startup bytes; {len(GUIDES)} scoped guides; {len(HEADINGS)} source headings; {len(pages)} explicit published pages")

if __name__ == "__main__":
    main()
