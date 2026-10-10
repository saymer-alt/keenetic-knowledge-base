#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Stage only curated docs/ Markdown for MkDocs; do not publish repository root.

Run from any cwd: python tools/prepare_site_docs.py
The source Markdown files remain unchanged. Relative links to archive/catalog and
other files outside docs/ become absolute links to the corresponding GitHub source.
"""
from __future__ import annotations

import posixpath
import re
import shutil
from pathlib import Path
from urllib.parse import quote, unquote

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "docs"
OUTPUT = ROOT / ".site-content"
GITHUB_BLOB = "https://github.com/saymer-alt/keenetic-knowledge-base/blob/main/"

# Explicit allowlist. Never include archive/, catalog/, NVR/, MosTech/, or
# any other repository directory merely because a Markdown file exists there.
PAGES = (
    "index.md",
    "README.md",
    "amnezia-mihomo-gateway-evolution.md",
    "dns-geoip-ecs-leak-diagnostics.md",
    "dpi-diagnostics-map.md",
    "iot-cloud-routing-methodology.md",
    "keenetic-dns-via-mihomo.md",
    "keenetic-entware-base.md",
    "keenetic-policy-segment-ssid-naming.md",
    "mihomo-keenetic-routing.md",
    "mihomo-systemd-nonroot-hardening.md",
    "mobile-apn-methodology.md",
    "mipsel-binary-supply-chain.md",
    "moshub-entware-mirror.md",
    "network-layer-tunnel-map.md",
    "proxy-tunnel-protocol-stack.md",
    "vpn-proxy-terminology.md",
    "whitelist-mode-architecture.md",
    "zapret-ecosystem.md",
    "github-traffic-window-semantics.md",
)

# Only Markdown links; do not rewrite examples or arbitrary prose containing ../ .
MARKDOWN_URL = re.compile(
    r"(?P<before>!?\[[^\]\n]*\]\()"
    r"(?P<url>[^)\s]+)"
    r"(?P<after>(?:\s+\"[^\"]*\")?\))"
)


def rewrite_source_links(content: str) -> str:
    """Preserve site-internal links; link repository-only sources to GitHub."""

    def replace(match: re.Match[str]) -> str:
        url = match.group("url")
        # MkDocs gives README.md the same route as index.md; publish the
        # existing docs/README.md source as catalog.md in the staged site.
        path, sep, fragment = url.partition("#")
        if path == "README.md":
            return match.group("before") + "catalog.md" + ("#" + fragment if sep else "") + match.group("after")
        if not url.startswith("../"):
            return match.group(0)
        normalized = posixpath.normpath(posixpath.join("docs", unquote(path)))
        if normalized in {".", ".."} or normalized.startswith("../") or normalized.startswith("/"):
            raise ValueError(f"Link escapes repository: {url}")

        # Outside docs/ remains visible as a source reference on GitHub, NOT
        # as an exported site page. Inside docs/ is a normal relative page.
        if normalized.startswith("docs/"):
            destination = normalized.removeprefix("docs/")
        else:
            destination = GITHUB_BLOB + quote(normalized, safe="/-_.~")
        if sep:
            destination += "#" + fragment
        return match.group("before") + destination + match.group("after")

    return MARKDOWN_URL.sub(replace, content)


def validate_local_links(page: str, body: str) -> None:
    """Prevent broken links between the explicitly published articles."""
    curated = {"catalog.md" if name == "README.md" else name for name in PAGES}
    for match in MARKDOWN_URL.finditer(body):
        url = match.group("url")
        if url.startswith(("https://", "http://", "mailto:", "#", "tel:")):
            continue
        path = unquote(url.partition("#")[0])
        if not path:
            continue
        if path.startswith(("/", "../")):
            raise ValueError(f"{page}: unexpected unresolved link: {url}")
        normalized = posixpath.normpath(posixpath.join(posixpath.dirname(page), path))
        if normalized.endswith(".md") and normalized not in curated:
            raise ValueError(f"{page}: link to a non-published article: {url}")
        if not normalized.endswith(".md"):
            raise ValueError(f"{page}: local non-Markdown asset requires explicit review: {url}")


def build() -> None:
    if OUTPUT.is_symlink():
        raise ValueError("Refusing to replace symlinked site output")
    missing = [name for name in PAGES if not (SOURCE / name).is_file()]
    if missing:
        raise FileNotFoundError(f"Missing curated sources: {missing}")
    if OUTPUT.exists():
        shutil.rmtree(OUTPUT)
    OUTPUT.mkdir()

    for filename in PAGES:
        source = (SOURCE / filename).read_text(encoding="utf-8")
        transformed = rewrite_source_links(source)
        validate_local_links(filename, transformed)
        published_name = "catalog.md" if filename == "README.md" else filename
        (OUTPUT / published_name).write_text(transformed, encoding="utf-8")

    unpublished = sorted({p.name for p in SOURCE.glob("*.md")} - set(PAGES))
    print(f"Staged {len(PAGES)} curated Markdown pages in {OUTPUT.name}/.")
    if unpublished:
        print(f"NOT published (new docs require review): {', '.join(unpublished)}")
    print("Excluded by design: archive/, catalog/, MosTech/, NVR/ and repository root.")


if __name__ == "__main__":
    build()
