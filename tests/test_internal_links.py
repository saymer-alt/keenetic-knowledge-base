#!/usr/bin/env python3
"""Check that local Markdown links point at paths that exist in the repository.

Supported syntax (deliberately small, not a CommonMark implementation):

* inline links ``[text](target "title")`` and images ``![alt](target)``;
* destinations in angle brackets: ``[x](<docs/file with spaces.md>)``;
* destinations with balanced parentheses: ``[x](docs/note(1).md)``;
* bare destinations with spaces (GitHub tolerates them): ``[x](docs/my file.md)``;
* a quoted title after the destination is ignored;
* fragments (``#section``) and query strings (``?x=1``) are stripped before
  the file check; anchors themselves are not validated;
* URL-encoded paths are decoded (``%20`` -> space);
* any local target is checked for existence: files of any type, directories
  and repository-root-absolute paths (``/docs/``);
* ``..`` inside the repository is allowed; a target that resolves outside the
  repository root is reported as an error.

Ignored on purpose (documented limitations):

* reference-style links (``[text][id]``, ``[id]``) are skipped, not guessed;
* 4-space indented code blocks are not detected as code;
* fenced code blocks (``` / ~~~) and inline code spans are skipped;
* HTML comments are skipped; a comment ``<!--`` without ``-->`` hides the rest
  of the file, as an unterminated HTML block does in CommonMark;
* comments and code are masked in one pass, so a fence inside a comment is
  comment text and a comment marker inside code is code;
* external URIs are never turned into local paths.

Exit codes: 0 - no broken local links, 1 - broken links found, 2 - usage error.
"""

from __future__ import annotations

import argparse
import os
import re
import sys
import tempfile
import urllib.parse
from pathlib import Path

SCHEME_RE = re.compile(r"^[A-Za-z][A-Za-z0-9+.\-]*:")
FENCE_RE = re.compile(r"^ {0,3}(`{3,}|~{3,})")
SKIP_DIRS = {".git", ".site-build", "node_modules", ".venv", "venv", "__pycache__"}


def _blank(chars, start: int, end: int) -> None:
    for pos in range(start, end):
        chars[pos] = " "


def mask(text: str) -> str:
    """Blank out fenced code blocks, inline code spans and HTML comments.

    One pass tracks both states, because two independent passes cannot tell
    which construct started first: a fence line inside a comment is comment
    text, and ``<!--`` inside code is code. A fenced block is only recognised
    at the start of a line that is not inside a comment, and a comment is only
    recognised outside code. Offsets and line breaks are preserved.
    """
    out = []
    fence = None
    in_comment = False
    for line in text.split("\n"):
        chars = list(line)
        if fence is not None:
            match = FENCE_RE.match(line)
            if (match and match.group(1)[0] == fence[0]
                    and len(match.group(1)) >= len(fence)
                    and re.fullmatch(r"[ \t]*", line[match.end():])):
                fence = None
            _blank(chars, 0, len(chars))
            out.append("".join(chars))
            continue
        if not in_comment:
            match = FENCE_RE.match(line)
            if match:
                fence = match.group(1)
                _blank(chars, 0, len(chars))
                out.append("".join(chars))
                continue
        i = 0
        n = len(line)
        while i < n:
            if in_comment:
                close = line.find("-->", i)
                if close == -1:
                    _blank(chars, i, n)
                    i = n
                    break
                _blank(chars, i, close + 3)
                i = close + 3
                in_comment = False
                continue
            if line.startswith("<!--", i):
                _blank(chars, i, i + 4)
                i += 4
                in_comment = True
                continue
            if line[i] == "`":
                start = i
                while i < n and line[i] == "`":
                    i += 1
                run = i - start
                j = i
                closed = False
                while j < n:
                    if line[j] == "`":
                        k = j
                        while k < n and line[k] == "`":
                            k += 1
                        if k - j == run:
                            _blank(chars, start, k)
                            i = k
                            closed = True
                            break
                        j = k
                    else:
                        j += 1
                if not closed:
                    break
                continue
            i += 1
        out.append("".join(chars))
    return "\n".join(out)


def _balanced_parens(text: str, pos: int):
    """Return the content of a ``(...)`` group starting at pos and the end index."""
    depth = 0
    n = len(text)
    j = pos
    while j < n:
        char = text[j]
        if char == "\\":
            j += 2
            continue
        if char == "(":
            depth += 1
        elif char == ")":
            depth -= 1
            if depth == 0:
                return text[pos + 1:j], j + 1
        j += 1
    return None, pos


def _destination(content: str):
    """Extract the destination from the inside of a link's parentheses."""
    value = content.strip()
    if not value:
        return ""
    if value.startswith("<"):
        close = value.find(">")
        if close == -1:
            return None
        return value[1:close].strip()
    title = re.match(r"^(.*?)\s+(\"[^\"]*\"|'[^']*')\s*$", value, re.S)
    if title:
        return title.group(1).strip()
    return value


def iter_links(text: str):
    """Yield ``(offset, destination, is_image)`` for inline links and images."""
    n = len(text)
    i = 0
    while i < n:
        char = text[i]
        if char == "\\":
            i += 2
            continue
        if char == "!" and i + 1 < n and text[i + 1] == "[":
            is_image = True
            start = i
            i += 1
        elif char == "[":
            is_image = False
            start = i
        else:
            i += 1
            continue
        depth = 0
        j = i
        while j < n:
            symbol = text[j]
            if symbol == "\\":
                j += 2
                continue
            if symbol == "[":
                depth += 1
            elif symbol == "]":
                depth -= 1
                if depth == 0:
                    break
            j += 1
        if j >= n:
            break
        if j + 1 < n and text[j + 1] == "(":
            content, end = _balanced_parens(text, j + 1)
            if content is not None:
                destination = _destination(content)
                if destination is not None:
                    yield start, destination, is_image
                    i = end
                    continue
        i = j + 1


def local_path(target: str):
    """Return a decoded local path, or None for external/absolute-URL targets."""
    value = target.strip()
    if not value:
        return ""
    if value.startswith("//"):
        return None
    if SCHEME_RE.match(value):
        return None
    value = value.split("#", 1)[0].split("?", 1)[0]
    if not value:
        return None
    return urllib.parse.unquote(value)


def _is_inside(path: str, root: str) -> bool:
    try:
        return os.path.commonpath([os.path.abspath(path), os.path.abspath(root)]) == os.path.abspath(root)
    except ValueError:
        return False


def _exists_exact(root: Path, path: Path) -> bool:
    """Case-sensitive existence check, so local runs match Linux CI."""
    try:
        relative = os.path.relpath(str(path), str(root))
    except ValueError:
        return False
    if relative == os.pardir or relative.startswith(os.pardir + os.sep):
        return False
    current = root
    for part in relative.split(os.sep):
        if part in ("", os.curdir):
            continue
        try:
            entries = os.listdir(str(current))
        except OSError:
            return False
        if part not in entries:
            return False
        current = current / part
    return True


def check_target(source: Path, target: str, root: Path):
    """Return a problem description for a broken local target, else None."""
    local = local_path(target)
    if local is None:
        return None
    if not local:
        return "empty link target"
    if local.startswith("/"):
        resolved = os.path.normpath(os.path.join(str(root), local.lstrip("/")))
    else:
        resolved = os.path.normpath(os.path.join(str(source.parent), local))
    if not _is_inside(resolved, str(root)):
        return "target escapes the repository root"
    if not _exists_exact(root, Path(resolved)):
        return "target does not exist"
    return None


def check_file(path: Path, root: Path):
    """Return ``(links_checked, problems)`` for one Markdown file."""
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError as exc:
        return 0, [(1, "<file>", "cannot read: %s" % exc)]
    masked = mask(text)
    problems = []
    links = 0
    last = 0
    line = 1
    for offset, target, is_image in iter_links(masked):
        line += masked.count("\n", last, offset)
        last = offset
        if local_path(target) is None:
            continue
        links += 1
        problem = check_target(path, target, root)
        if problem:
            suffix = " (image)" if is_image else ""
            problems.append((line, target + suffix, problem))
    return links, problems


def iter_markdown_files(root: Path):
    for dirpath, dirnames, filenames in os.walk(str(root)):
        dirnames[:] = sorted(d for d in dirnames if d not in SKIP_DIRS)
        for name in sorted(filenames):
            if name.lower().endswith(".md"):
                yield Path(dirpath) / name


def check_tree(root: Path):
    files = 0
    links = 0
    problems = []
    for path in iter_markdown_files(root):
        files += 1
        count, found = check_file(path, root)
        links += count
        for line, target, reason in found:
            problems.append((path.relative_to(root).as_posix(), line, target, reason))
    return files, links, problems


def _write_text(path: Path, body: str) -> None:
    with open(str(path), "w", encoding="utf-8", newline="\n") as handle:
        handle.write(body)


def run_self_test() -> int:
    fixtures = {
        "valid": {
            "README.md": (
                "# Root\n\n"
                "[article](docs/a.md)\n"
                "[brackets [inner] in text](docs/a.md)\n"
                "[site](https://example.com/x)\n"
                "[mail](mailto:dev@example.com)\n"
                "[local anchor](#root)\n"
                "![logo](docs/img.png)\n"
            ),
            "docs/a.md": (
                "# A\n\n"
                "[up](../README.md)\n"
                "[sub](sub/b.md)\n"
                "[anchor](sub/b.md#part)\n"
                "[encoded](img%20pic.png)\n"
                "[spaces](img pic.png)\n"
                "[pic](img.png)\n"
                "[dir](../archive/)\n"
                "[license](../LICENSE)\n"
                "[nested](note(1).md)\n"
                "[titled](sub/b.md \"Title\")\n"
                "\n```text\n[broken](nowhere.md)\n```\n"
                "\n`[also-broken](nowhere2.md)`\n"
                "\nPassing `code` keeps [sub](sub/b.md) valid.\n"
            ),
            "docs/sub/b.md": (
                "# B\n\n[up](../a.md)\n[root](../../README.md)\n"
            ),
            "docs/img.png": "png\n",
            "docs/img pic.png": "png\n",
            "docs/note(1).md": "# note\n",
            "archive/README.md": "# archive\n\n[root](../README.md)\n",
            "LICENSE": "MIT\n",
        },
        "missing": {
            "README.md": "[missing](docs/none.md)\n",
        },
        "missing-anchor-file": {
            "README.md": "[x](nope.md#frag)\n",
        },
        "escape": {
            "docs/x.md": "[out](../../outside.md)\n",
        },
        "escape-existing": {
            "docs/x.md": "[out](../../sibling.md)\n",
        },
        "case": {
            "README.md": "[bad](Docs/A.md)\n",
            "docs/a.md": "# a\n",
        },
        # A fence line inside an HTML comment used to open a code block and
        # hide everything after it (false negative).
        "comment-fence-broken": {
            "README.md": (
                "# Doc\n\n"
                "<!-- example\n"
                "```text\n"
                "-->\n\n"
                "[bad](missing.md)\n"
            ),
        },
        "comment-fence-valid": {
            "README.md": (
                "# Doc\n\n"
                "<!-- example\n"
                "```text\n"
                "-->\n\n"
                "[ok](exists.md)\n"
            ),
            "exists.md": "# exists\n",
        },
        # A comment marker inside real code must stay code.
        "code-with-comment": {
            "README.md": (
                "# Doc\n\n"
                "```text\n"
                "<!-- not a comment\n"
                "[hidden](missing-inside.md)\n"
                "```\n\n"
                "[bad](missing-after.md)\n"
            ),
        },
        "comment-multiline": {
            "README.md": (
                "# Doc\n\n"
                "[before](exists.md)\n"
                "<!-- starts\n"
                "```\n"
                "[hidden](missing.md)\n"
                "still commented -->\n"
                "[after](exists.md)\n"
            ),
            "exists.md": "# exists\n",
        },
        "comment-unclosed": {
            "README.md": (
                "# Doc\n\n"
                "[before](exists.md)\n"
                "<!-- unclosed\n"
                "[hidden](missing.md)\n"
            ),
            "exists.md": "# exists\n",
        },
        "fence-closer-info": {
            "README.md": "```text\n```python\n[inside](missing.md)\n```\n",
        },
        "tilde-closer-info": {
            "README.md": "~~~text\n~~~python\n[inside](missing.md)\n~~~\n",
        },
        "fence-close-detects-after": {
            "README.md": "```text\n[inside](missing.md)\n```  \n[after](missing-after.md)\n",
        },
        "fence-short-closer": {
            "README.md": "````text\n```\n[inside](missing.md)\n````\n",
        },
        "fence-links": {
            "README.md": (
                "[before](exists.md)\n"
                "\n"
                "```text\n"
                "[inside](missing.md)\n"
                "```\n"
                "\n"
                "[after](exists.md)\n"
            ),
            "exists.md": "# exists\n",
        },
    }
    expected = {
        "valid": (0, []),
        "missing": (1, ["docs/none.md"]),
        "missing-anchor-file": (1, ["nope.md#frag"]),
        "escape": (1, ["../../outside.md"]),
        "escape-existing": (1, ["../../sibling.md"]),
        "case": (1, ["Docs/A.md"]),
        "comment-fence-broken": (1, ["missing.md"]),
        "comment-fence-valid": (0, []),
        "code-with-comment": (1, ["missing-after.md"]),
        "comment-multiline": (0, []),
        "comment-unclosed": (0, []),
        "fence-closer-info": (0, []),
        "tilde-closer-info": (0, []),
        "fence-close-detects-after": (1, ["missing-after.md"]),
        "fence-short-closer": (0, []),
        "fence-links": (0, []),
    }
    failures = 0
    with tempfile.TemporaryDirectory(prefix="kb-links-") as tmp:
        base = Path(tmp)
        # A target that exists, but only outside the case root, proves the
        # boundary check rejects it rather than a missing file.
        _write_text(base / "sibling.md", "# sibling\n")
        for name, files in fixtures.items():
            case_root = base / name
            for relative, body in files.items():
                target = case_root / relative
                target.parent.mkdir(parents=True, exist_ok=True)
                _write_text(target, body)
        for name in fixtures:
            _, _, problems = check_tree(base / name)
            got_targets = [problem[2] for problem in problems]
            want_count, want_targets = expected[name]
            ok = len(problems) == want_count and got_targets == want_targets
            if not ok:
                failures += 1
            detail = problems[0][3] if problems else "no problems"
            print(
                "%s %-20s expected=%d got=%d (%s)"
                % ("PASS" if ok else "FAIL", name, want_count, len(problems), detail)
            )
        if not (base / "sibling.md").exists():
            print("FAIL sibling.md fixture missing")
            failures += 1
    print("self-test: %s" % ("PASS" if failures == 0 else "FAIL (%d)" % failures))
    return 0 if failures == 0 else 1


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--root", default=None, help="repository root (default: parent of tests/)")
    parser.add_argument("--self-test", action="store_true", help="run the fixture-based self-test")
    args = parser.parse_args(argv)
    if args.self_test:
        return run_self_test()
    root = Path(args.root).resolve() if args.root else Path(__file__).resolve().parent.parent
    if not root.is_dir():
        print("error: repository root not found: %s" % root, file=sys.stderr)
        return 2
    files, links, problems = check_tree(root)
    for relative, line, target, reason in problems:
        print("%s:%d: broken link %r: %s" % (relative, line, target, reason))
    print("checked %d Markdown files, %d local links, %d broken" % (files, links, len(problems)))
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
