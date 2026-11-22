# License: not assigned yet. This file is not in the explicit MIT list of
# COPYRIGHT_AND_LICENSING.md section 2; adding it needs an owner decision.
"""Host-boundary contract of the Telegram export URL classifier (F-21).

Only an exact domain or a real subdomain (dot boundary) may be treated as a
known host. A lookalike suffix such as ``notgithub.com`` must stay ``other``
and must not receive GitHub/GitLab-specific normalization.
"""
import unittest

from tools.parse_telegram_export import classify_url, normalize_url

GITHUB_LIKE = {"github-repo", "github-profile", "github-subpage",
               "github-raw", "gist"}


class ClassifyHostBoundaryTests(unittest.TestCase):
    def assertNotTrusted(self, href, category):
        actual = classify_url(href, "link")
        self.assertNotEqual(category, actual, href)
        self.assertEqual("other", actual, href)

    def test_exact_github_domain(self):
        self.assertEqual("github-repo", classify_url(
            "https://github.com/user/repo", "link"))

    def test_github_subdomains_keep_their_meaning(self):
        self.assertEqual("gist", classify_url(
            "https://gist.github.com/user/123", "link"))
        self.assertEqual("github-raw", classify_url(
            "https://raw.githubusercontent.com/user/repo/main/file", "link"))
        self.assertEqual("github-repo", classify_url(
            "https://www.github.com/user/repo", "link"))

    def test_lookalike_github_suffix_is_not_github(self):
        self.assertNotTrusted("https://notgithub.com/user/repo", "github-repo")

    def test_github_domain_used_as_a_suffix_is_not_github(self):
        self.assertNotTrusted("https://github.com.evil.test/user/repo", "github-repo")

    def test_lookalike_raw_suffix_is_not_github_raw(self):
        self.assertNotTrusted(
            "https://notgithubusercontent.com/user/repo/main/file", "github-raw")

    def test_com_cd_lookalike_is_not_github(self):
        self.assertNotTrusted("https://notgithub.com.ru/user/repo", "github-repo")

    def test_gitlab_exact_and_lookalike(self):
        self.assertEqual("gitlab", classify_url(
            "https://gitlab.com/user/repo", "link"))
        self.assertNotTrusted("https://notgitlab.com/user/repo", "gitlab")

    def test_documentation_domains(self):
        for href in ("https://docs.keenetic.com/",
                     "https://keenetic.com/",
                     "https://entware.net/",
                     "https://docs.magitrickle.dev/x",
                     "https://pkg.go.dev/x"):
            self.assertEqual("documentation", classify_url(href, "link"), href)

    def test_lookalike_documentation_domains(self):
        self.assertNotTrusted("https://fakekeenetic.com/", "documentation")
        self.assertNotTrusted("https://fakeentware.net/", "documentation")
        self.assertNotTrusted("https://notgo.dev/x", "documentation")
        self.assertNotTrusted("https://fakemagitrickle.dev/x", "documentation")

    def test_lookalike_telegram_domain(self):
        self.assertNotTrusted("https://nottelegram.me/channel", "telegram")

    def test_userinfo_and_port_do_not_bypass_the_check(self):
        self.assertNotIn(classify_url(
            "https://user:pass@notgithub.com:8443/user/repo", "link"),
            GITHUB_LIKE)
        self.assertNotEqual("documentation", classify_url(
            "https://user@fakekeenetic.com:8080/", "link"))
        self.assertEqual("github-repo", classify_url(
            "https://github.com:8443/user/repo", "link"))

    def test_existing_categories_are_preserved(self):
        cases = {
            "https://t.me/s/channel": "telegram",
            "https://telegra.ph/post-1": "article-or-forum",
            "https://habr.com/ru/post/1/": "article-or-forum",
            "https://forum.keenetic.com/topic/1": "article-or-forum",
            "https://pastebin.com/abc123": "pastebin",
            "https://browserleaks.com/ip": "diagnostic-service",
            "https://sub.speedtest.net/x": "diagnostic-service",
            "https://198.51.100.7/": "ip-literal",
            "https://example.com/article": "other",
        }
        for href, expected in cases.items():
            self.assertEqual(expected, classify_url(href, "link"), href)

    def test_habr_prefix_lookalike_is_not_a_forum(self):
        # The old prefix check host.startswith("habr.") accepted habr.evil.com;
        # habr.com/habr.ru and their real subdomains must stay classified.
        self.assertNotTrusted("https://habr.evil.com/x", "article-or-forum")
        self.assertEqual("article-or-forum", classify_url(
            "https://special.habr.com/x", "link"))

    def test_docs_path_rule_is_unchanged(self):
        self.assertEqual("documentation", classify_url(
            "https://example.com/docs/install", "link"))


class NormalizeGitSuffixTests(unittest.TestCase):
    def test_github_dot_git_is_stripped(self):
        self.assertEqual("https://github.com/user/repo",
                         normalize_url("https://github.com/user/repo.git"))

    def test_gitlab_dot_git_is_stripped(self):
        self.assertEqual("https://gitlab.com/user/repo",
                         normalize_url("https://gitlab.com/user/repo.git"))

    def test_lookalike_dot_git_is_kept(self):
        for url in ("https://notgithub.com/user/repo.git",
                    "https://notgitlab.com/user/repo.git"):
            self.assertEqual(url, normalize_url(url))

    def test_domain_without_dot_boundary_keeps_dot_git(self):
        for url in ("https://mygithub.com/user/repo.git",
                    "https://github.com.evil.test/user/repo.git"):
            self.assertEqual(url, normalize_url(url))

    def test_host_case_is_folded_and_path_case_kept(self):
        self.assertEqual("https://github.com/User/Repo",
                         normalize_url("https://GitHub.COM/User/Repo.git"))

    def test_port_and_userinfo_do_not_change_the_rule(self):
        self.assertEqual("https://github.com:443/user/repo",
                         normalize_url("https://github.com:443/user/repo.git"))
        self.assertEqual("https://user:pw@github.com/u/r",
                         normalize_url("https://user:pw@github.com/u/r.git"))
        self.assertEqual("https://notgithub.com:443/u/r.git",
                         normalize_url("https://notgithub.com:443/u/r.git"))
        self.assertEqual("https://user@notgithub.com/u/r.git",
                         normalize_url("https://user@notgithub.com/u/r.git"))

    def test_query_and_fragment_are_preserved(self):
        self.assertEqual(
            "https://github.com/u/r?tab=readme#L10",
            normalize_url("https://github.com/u/r.git?utm_source=x&tab=readme#L10"))

    def test_empty_and_malformed_urls_do_not_raise(self):
        self.assertEqual("", normalize_url(""))
        self.assertEqual("", normalize_url("   "))
        self.assertEqual("not a url", normalize_url("not a url"))
        # No exact string is promised for scheme-only input: the contract is
        # "returns a string, never raises".
        self.assertIsInstance(normalize_url("http://"), str)


if __name__ == "__main__":
    unittest.main()
