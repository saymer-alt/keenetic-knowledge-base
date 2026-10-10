# SPDX-License-Identifier: MIT
"""Safety and link-conversion contract of the curated MkDocs staging."""
import re
import unittest
from pathlib import Path
from tools.prepare_site_docs import PAGES, rewrite_source_links, validate_local_links


class SiteStagingTests(unittest.TestCase):
    def test_rewrites_archived_sources_to_github(self):
        result = rewrite_source_links(
            "[источник](../archive/raw/mihomo-dns.md) "
            "[каталог](../catalog/techno-bypass/topics/dpi-zapret.md#x)"
        )
        self.assertIn(
            "https://github.com/saymer-alt/keenetic-knowledge-base/blob/main/archive/raw/mihomo-dns.md",
            result,
        )
        self.assertIn("topics/dpi-zapret.md#x", result)

    def test_keeps_cross_article_links(self):
        source = "[статья](network-layer-tunnel-map.md) [домой](README.md)"
        self.assertEqual(
            rewrite_source_links(source),
            "[статья](network-layer-tunnel-map.md) [домой](catalog.md)",
        )
        validate_local_links("index.md", rewrite_source_links(source))

    def test_rejects_unpublished_markdown(self):
        with self.assertRaisesRegex(ValueError, "non-published"):
            validate_local_links("index.md", "[private](sensitive-source.md)")

    def test_explicit_allowlist_excludes_raw_dirs(self):
        self.assertEqual(len(PAGES), 18)
        for name in PAGES:
            self.assertFalse("/" in name)
            self.assertTrue(name.endswith(".md"))
        self.assertNotIn("AGENTS.md", PAGES)

    def test_site_publications_have_explicit_cc_by_scope(self):
        # No page may silently become CC BY without a documented owner decision.
        policy = (Path(__file__).resolve().parents[1] /
                  "COPYRIGHT_AND_LICENSING.md").read_text(encoding="utf-8")
        scope = policy.split("## 1. CC BY 4.0:", 1)[1].split("## 2. MIT:", 1)[0]
        licensed = re.findall(r"\|\s*`docs/([^\`]+\.md)`\s*\|", scope)
        self.assertEqual(set(PAGES), set(licensed))
        self.assertEqual(len(PAGES), len(licensed))

    def test_rejects_unsafe_escape(self):
        with self.assertRaises(ValueError):
            rewrite_source_links("[outside](../../../private.md)")


if __name__ == "__main__":
    unittest.main()
