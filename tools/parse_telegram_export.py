#!/usr/bin/env python3
"""Parse a Telegram Desktop HTML chat/channel export into structured JSON.

Usage:

    python3 parse_telegram_export.py --out <workdir> FILE [FILE ...]

- Accepts one or more export HTML files (e.g. messages.html, messages2.html)
  and treats them as ONE chronological export: messages are merged,
  deduplicated by Telegram message id and sorted by id.
- Writes into <workdir>:
    messages.json  full per-message dataset (plain text, links, hashtags,
                   media file names, forwarded provenance, sensitivity flags)
    links.json     URL inventory with conservative normalization + dedup
    stats.json     corpus statistics (counts, hashtags, domains, forwarded
                   authors, date range, sensitivity findings - counts only)
    digest.txt     one line per message for quick browsing
- Deterministic: identical inputs produce byte-identical outputs
  (json.dump with sort_keys=True, ordering by message id).
- Read-only regarding the repository: the script NEVER writes Markdown and
  never modifies catalog files. Curating catalog/<source>/*.md (descriptions,
  statuses, grouping) stays a human/agent decision - re-running the parser
  on a newer export produces a fresh dataset to diff against, not an
  overwrite of reviewed text.
- SECURITY NOTE: outputs contain the raw channel text and raw links. They are
  work artifacts and must NOT be committed to a public repository. Only the
  curated Markdown layer under catalog/ belongs in git.

Telegram export format notes (machine-generated HTML, quite regular):
- <div class="message service" id="message-229">   -> date separator, skipped
- <div class="message default clearfix[ joined]" id="message1040"> -> message
- post date:      <div class="pull_right date details" title="...">
- channel author: <div class="from_name"> (only when not "joined")
- forwarded:      <div class="forwarded body"> with its own
                  <div class="from_name">Author<span class="date details"
                  title="...">...</span></div> (span = original date)
- text:           <div class="text"> with <a href>, hashtag anchors
                  (href="" + onclick ShowHashtag) and <pre> blocks
- attachments:    <div class="media_wrap"> -> div.title.bold = file name
"""

from __future__ import annotations

import argparse
import ipaddress
import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit, parse_qsl, urlencode

MSG_ID_RE = re.compile(r"^message(-?\d+)$")

# ---------------------------------------------------------------- sensitive
SENSITIVE_PATTERNS = [
    # (category, regex) - applied to plain text and hrefs; counts only, never
    # echoed into reports with the matched content.
    ("telegram-private-link", r"t\.me/(?:c/|\+|joinchat)"),
    ("mtproto-proxy-secret", r"(?:tg://|t\.me/)proxy\?[^\s]*secret="),
    ("subscription-token-url", r"/api/v1/client/subscribe\?|sub\?token=|\?token=[A-Za-z0-9]{16,}"),
    ("proxy-credential-scheme", r"\b(?:vmess|vless|trojan|ss|ssr|hysteria2?|tuic|masque|webtunnel)://\S{8,}"),
    ("private-key-block", r"BEGIN [A-Z ]*PRIVATE KEY"),
    ("password-assignment", r"(?i)\b(passwd|password|passphrase|secret|api[_-]?key|auth[_-]?token)\s*[:=]\s*\S{6,}"),
    # Russian-language credential lines found by the TASK-TB-03 manual audit
    ("password-ru", r"Пароль\s*[:=]\s*\S{4,}"),
    ("login-ru", r"Логин\s*[:=]\s*\S{3,}"),
    ("psk-assignment", r"(?i)(?:общий\s+ключ\s+)?psk\s*[:=]\s*\S{4,}"),
    ("url-embedded-credentials", r"[?&](?:user|username|pass|password)=\S{3,}|://[^/\s:]+:[^@\s]{3,}@"),
    ("vpn-server-credentials", r"Сервер:\s*\d{1,3}(?:\.\d{1,3}){3}"),
]

TRACKING_PARAMS = re.compile(r"^(utm_|yclid|fbclid|gclid|ref$|igshid)", re.IGNORECASE)

TG_DATE_RE = re.compile(r"^(\d{2})\.(\d{2})\.(\d{4})[ T](\d{2}):(\d{2})")


def date_to_iso(s: str) -> str | None:
    """'16.09.2025 21:09:44 UTC+03:00' -> '2025-09-16 21:09' (or None)."""
    if not s:
        return None
    m = TG_DATE_RE.match(s.strip())
    if not m:
        return None
    d, mo, y, h, mi = m.groups()
    return "%s-%s-%s %s:%s" % (y, mo, d, h, mi)


def normalize_url(url: str) -> str:
    """Conservative normalization: lowercase scheme+host, drop tracking
    params, strip trailing slash. Fragments are kept (they are meaningful
    for article anchors). NO collapsing of repo-vs-issue, path variants,
    www vs bare host etc. - that is deliberately left to curation."""
    try:
        parts = urlsplit(url.strip())
    except ValueError:
        return url.strip()
    if not parts.scheme and not parts.netloc:
        return url.strip()
    scheme = parts.scheme.lower()
    netloc = parts.netloc.lower()
    path = parts.path or "/"
    if path != "/" and path.endswith("/"):
        path = path.rstrip("/")
    # git hosts: repo root vs repo.git point at the same project; distinct
    # paths (issues/releases/blob) are unaffected by this rule.
    if netloc.endswith(("github.com", "gitlab.com")) and path.endswith(".git"):
        path = path[:-4] or "/"
    query = ""
    if parts.query:
        kept = [(k, v) for k, v in parse_qsl(parts.query, keep_blank_values=True)
                if not TRACKING_PARAMS.match(k)]
        if kept:
            query = urlencode(kept)
    return urlunsplit((scheme, netloc, path, query, parts.fragment))


def looks_like_autolinked_hostname(href: str, text: str) -> bool:
    """Telegram autolinks bare hostnames/IPs as https://<hostname>, producing
    fake URLs (e.g. APN names like b2b.mts.ru or IPs). Detect the case where
    the anchor text IS the host of the href."""
    t = (text or "").strip().rstrip(".,;:)")
    if not t or "/" in t or " " in t:
        return False
    try:
        parts = urlsplit(href)
        if parts.scheme not in ("http", "https") or parts.path not in ("", "/"):
            return False
        host = parts.netloc.lower().split("@")[-1].split(":")[0]
        if host == t.lower():
            return True
        # IP-literal autolinks: href https://1.2.3.4, text 1.2.3.4
        try:
            ipaddress.ip_address(t)
            return host == t
        except ValueError:
            return False
    except ValueError:
        return False


def classify_url(href: str, anchor: str) -> str:
    """Best-effort link type; 'other' is a valid answer."""
    if looks_like_autolinked_hostname(href, anchor):
        return "hostname-mention"
    u = urlsplit(href)
    host = (u.netloc.lower().split("@")[-1].split(":")[0]) or ""
    path = u.path or "/"
    if host.endswith("github.com") or host.endswith("githubusercontent.com") or host == "gist.github.com":
        if host == "gist.github.com" or host.endswith("githubusercontent.com"):
            if "gist" in host:
                return "gist"
            return "github-raw"
        seg = [s for s in path.split("/") if s]
        if seg and seg[0] in ("sitemap.xml",):
            return "other"
        if len(seg) >= 3 and seg[2] in ("releases", "issues", "pull", "blob", "tree", "wiki", "discussions", "actions", "commit", "tags", "archive", "settings"):
            return "github-subpage"
        if len(seg) >= 2:
            return "github-repo"
        return "github-profile"
    if host.endswith("gitlab.com"):
        return "gitlab"
    if host == "t.me" or host.endswith("telegram.me") or host.endswith(".telegram.org"):
        return "telegram"
    if host in ("telegra.ph", "teletype.in", "habr.com", "medium.com", "vc.ru", "dtf.ru",
                "4pda.to", "forum.keenetic.com", "www.reddit.com", "reddit.com",
                "linux.org.ru", "forum.zalinux.ru", "svsool.com") or host.startswith("habr."):
        return "article-or-forum"
    if host in ("pastebin.com", "ghostbin.com", "paste.ee", "controlc.com", "dpaste.com",
                "rentry.co", "textbin.net"):
        return "pastebin"
    if host.endswith("keenetic.com") or host.endswith("magitrickle.dev") or host.endswith("entware.net") \
            or host.endswith("xray.com") or host.endswith("go.dev") or host.endswith("readthedocs.io") \
            or host.endswith("mihomo.party") or host.endswith("wireguard.com") \
            or host.endswith("amnezia.org") or host.endswith("proxifly.com") or "/docs" in path:
        return "documentation"
    diagnostics = ("browserleaks.com", "dnsleaktest.com", "ipleak.net", "speedtest.net",
                   "check-host.net", "ifconfig.me", "ipinfo.io", "ip.sb", "whatismyipaddress.com",
                   "whoer.net", "2ip.ru", "ipleak.com", "wifi4games.com", "tagaev.xyz")
    if host in diagnostics or host.endswith(".speedtest.net") or host.endswith(".ooklaserver.net"):
        return "diagnostic-service"
    if re.fullmatch(r"\d{1,3}(?:\.\d{1,3}){3}", host):
        return "ip-literal"
    return "other"


class ExportParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.messages = {}
        self.service_count = 0
        # state
        self.stack = []             # list of class-lists for open <div>/<span>
        self.cur = None             # current message dict or None
        self.cur_service = False
        self.capture = None         # 'text' | 'from_name' | 'fwd_name' | 'media_title' | None
        self.text_buf = []
        self.name_buf = []
        self.link = None            # active link dict
        self.link_buf = []
        self.pseudo_link = False    # anchor looks like autolinked hostname

    # -- helpers ---------------------------------------------------------
    def _cls(self, attrs):
        for k, v in attrs:
            if k == "class":
                return (v or "").split()
        return []

    def _attr(self, attrs, name):
        for k, v in attrs:
            if k == name:
                return v
        return None

    def _in(self, *names):
        want = set(names)
        return any(c & want for c in self.stack)

    # -- tags ------------------------------------------------------------
    def handle_starttag(self, tag, attrs):
        cls = set(self._cls(attrs))
        if tag == "div":
            self.stack.append(cls)
            if "message" in cls:
                mid = self._attr(attrs, "id")
                m = MSG_ID_RE.match(mid or "")
                if m and "service" in cls:
                    self.service_count += 1
                    self.cur_service = True
                    self.cur = None
                elif m:
                    self.cur_service = False
                    self.cur = {
                        "id": int(m.group(1)),
                        "joined": "joined" in cls,
                        "date": None,
                        "author": None,
                        "forwarded_from": None,
                        "forwarded_date": None,
                        "text": "",
                        "hashtags": [],
                        "links": [],
                        "media_files": [],
                        "media_photos": 0,
                    }
                else:
                    self.cur_service = True
                    self.cur = None
                return
            if self.cur is None and not self.cur_service:
                return
            if self.cur is not None:
                if cls >= {"date", "details"} and "pull_right" in cls:
                    self.cur["date"] = self._attr(attrs, "title")
                elif cls == {"text"}:
                    # capture text both in the outer body and the forwarded body
                    self.capture = "text"
                    self.text_buf = []
                elif cls == {"from_name"}:
                    if self._in_fwd_body():
                        self.capture = "fwd_name"
                    else:
                        self.capture = "from_name"
                    self.name_buf = []
                elif "media_wrap" in cls:
                    self._media_kind = None
                elif cls >= {"title", "bold"} and self._in("media_wrap"):
                    self.capture = "media_title"
                    self.name_buf = []
            return
        if tag == "span":
            self.stack.append(cls)
            if cls >= {"date", "details"} and self.cur is not None:
                # span inside forwarded from_name = original message date
                self.cur["forwarded_date"] = self._attr(attrs, "title")
            return
        if tag == "br":
            if self.capture == "text":
                self.text_buf.append("\n")
            if self.link is not None:
                self.link_buf.append(" ")
            return
        if tag == "a" and self.cur is not None:
            href = self._attr(attrs, "href") or ""
            onclick = self._attr(attrs, "onclick") or ""
            if "ShowHashtag" in onclick or (not href and "ShowBotCommand" in onclick):
                self.link = {"kind": "hashtag", "text": ""}
                self.link_buf = []
            elif href:
                self.link = {"kind": "link", "href": href, "text": ""}
                self.link_buf = []
            return

    def handle_endtag(self, tag):
        if tag == "div":
            if not self.stack:
                return
            cls = self.stack.pop()
            if self.cur is not None:
                if cls == {"text"} and self.capture == "text":
                    self._finish_text()
                elif cls == {"from_name"} and self.capture in ("from_name", "fwd_name"):
                    self._finish_name()
                elif cls >= {"title", "bold"} and self.capture == "media_title":
                    self._finish_media_title()
                elif "message" in cls:
                    self._finish_message()
            return
        if tag == "span":
            if self.stack:
                self.stack.pop()
            return
        if tag == "a" and self.link is not None:
            text = "".join(self.link_buf).strip()
            if self.link["kind"] == "hashtag":
                if text:
                    self.cur["hashtags"].append(text.lstrip("#").strip())
            else:
                self.cur["links"].append({"href": self.link["href"], "text": text})
            self.link = None
            self.link_buf = []
            return

    def handle_data(self, data):
        if self.link is not None:
            self.link_buf.append(data)
            if self.link["kind"] == "link":
                # anchor text is part of the plain text too
                if self.capture == "text":
                    self.text_buf.append(data)
            return
        if self.capture == "text":
            self.text_buf.append(data)
        elif self.capture in ("from_name", "fwd_name", "media_title"):
            self.name_buf.append(data)

    # -- finishers -------------------------------------------------------
    def _in_fwd_body(self):
        # a from_name directly inside div.forwarded.body
        for c in self.stack[:-1]:
            if "forwarded" in c:
                return True
        return False

    def _finish_text(self):
        self.capture = None
        text = "".join(self.text_buf)
        text = re.sub(r"[ \t]+\n", "\n", text)
        text = re.sub(r"\n{3,}", "\n\n", text)
        self.cur["text"] = self.cur["text"] + text if self.cur["text"] else text

    def _finish_name(self):
        name = "".join(self.name_buf).strip()
        # forwarded author names embed the original date span text; strip it
        name = re.sub(r"\d{2}\.\d{2}\.\d{4}.*$", "", name).strip()
        if self.capture == "fwd_name":
            self.cur["forwarded_from"] = name or None
        else:
            self.cur["author"] = name or None
        self.capture = None

    def _finish_media_title(self):
        title = "".join(self.name_buf).strip()
        self.capture = None
        if not title:
            return
        if title.lower() == "photo":
            self.cur["media_photos"] += 1
        else:
            self.cur["media_files"].append(title)

    def _finish_message(self):
        m, self.cur = self.cur, None
        if m is None:
            return
        m["date_iso"] = date_to_iso(m.get("date"))
        m["sensitive_flags"] = []  # category names only, filled by scan_sensitive
        self.messages[m["id"]] = m


def parse_file(path: Path) -> ExportParser:
    p = ExportParser()
    p.feed(path.read_text(encoding="utf-8", errors="replace"))
    p.close()
    return p


def build_inventory(messages: list[dict]) -> dict:
    inv = {}
    for m in messages:
        ctx = m["text"][:180].replace("\n", " ").strip()
        for lnk in m["links"]:
            href = lnk["href"]
            if not href.startswith(("http://", "https://")):
                continue
            norm = normalize_url(href)
            typ = classify_url(href, lnk["text"])
            e = inv.setdefault(norm, {
                "first_seen": None, "last_seen": None,
                "occurrences": 0, "messages": [],
                "example_hrefs": [], "type": typ,
                "anchor_examples": [], "contexts": [],
            })
            e["occurrences"] += 1
            e["messages"].append(m["id"])
            d = (m.get("date_iso") or "")[:10]
            if d:
                if e["first_seen"] is None or d < e["first_seen"]:
                    e["first_seen"] = d
                if e["last_seen"] is None or d > e["last_seen"]:
                    e["last_seen"] = d
            if href not in e["example_hrefs"] and len(e["example_hrefs"]) < 3:
                e["example_hrefs"].append(href)
            if lnk["text"] and lnk["text"] not in e["anchor_examples"] and len(e["anchor_examples"]) < 3:
                e["anchor_examples"].append(lnk["text"][:80])
            if ctx and ctx not in e["contexts"] and len(e["contexts"]) < 3:
                e["contexts"].append(ctx)
    for e in inv.values():
        e["messages"] = sorted(set(e["messages"]))
    return inv


def scan_sensitive(messages: list[dict]) -> dict:
    counts = {cat: 0 for cat, _ in SENSITIVE_PATTERNS}
    flagged_msgs = {cat: [] for cat, _ in SENSITIVE_PATTERNS}
    for m in messages:
        blob = m["text"] + "\n" + "\n".join(l["href"] for l in m["links"])
        for cat, rx in SENSITIVE_PATTERNS:
            if re.search(rx, blob):
                counts[cat] += 1
                flagged_msgs[cat].append(m["id"])
                m.setdefault("sensitive_flags", []).append(cat)
    return {"counts": counts,
            "message_ids": {k: v for k, v in flagged_msgs.items() if v}}


def selftest():
    """Synthetic detection/redaction check. Uses ONLY fake placeholder values
    (never real secrets); prints PASS/FAIL, categories and counts, never values."""
    fake = [
        {"id": 1, "text": "see https://github.com/example/project releases",
         "links": [{"href": "https://github.com/example/project", "text": ""}], "hashtags": []},
        {"id": 2, "text": "tg proxy Пароль: fakepass123",
         "links": [{"href": "tg://proxy?server=example&port=1&secret=" + "f" * 32, "text": ""}], "hashtags": []},
        {"id": 3, "text": "IKEv2 Сервер: 192.0.2.1 Общий ключ PSK: fakepsk Логин: fakeuser",
         "links": [], "hashtags": []},
        {"id": 4, "text": "private invite",
         "links": [{"href": "https://t.me/c/123456/7", "text": ""}], "hashtags": []},
    ]
    res = scan_sensitive(fake)
    flagged_ids = {i for ids in res["message_ids"].values() for i in ids}
    expect = {"mtproto-proxy-secret", "password-ru", "psk-assignment", "login-ru",
              "vpn-server-credentials", "telegram-private-link"}
    got = set(res["counts"])
    ok = expect <= got and 1 not in flagged_ids and {2, 3, 4} <= flagged_ids
    print("selftest:", "PASS" if ok else "FAIL",
          "| detected:", sorted(got),
          "| public-url msg flagged:", 1 in flagged_ids)
    return 0 if ok else 1


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--out", help="work directory for JSON/digest outputs")
    ap.add_argument("--selftest", action="store_true",
                    help="run synthetic sensitive-detection checks and exit")
    ap.add_argument("files", nargs="*", help="Telegram export HTML file(s)")
    args = ap.parse_args(argv)
    if args.selftest:
        return selftest()
    if not args.out or not args.files:
        ap.error("--out and at least one input file are required (or use --selftest)")

    outdir = Path(args.out)
    outdir.mkdir(parents=True, exist_ok=True)

    merged = {}
    service_total = 0
    for f in args.files:
        p = parse_file(Path(f))
        merged.update(p.messages)
        service_total += p.service_count

    messages = [merged[k] for k in sorted(merged)]
    # fill author for "joined" messages (same author as previous)
    prev_author = None
    for m in messages:
        if m["author"]:
            prev_author = m["author"]
        elif m["joined"] and prev_author:
            m["author_inferred"] = prev_author

    inv = build_inventory(messages)
    sens = scan_sensitive(messages)

    dates = sorted(m["date_iso"][:10] for m in messages if m.get("date_iso"))
    hashtags = {}
    fwd_authors = {}
    type_counts = {}
    domain_counts = {}
    for m in messages:
        for h in m["hashtags"]:
            hashtags.setdefault(h.lower(), {"count": 0, "messages": []})
            hashtags[h.lower()]["count"] += 1
            hashtags[h.lower()]["messages"].append(m["id"])
        if m.get("forwarded_from"):
            fwd_authors[m["forwarded_from"]] = fwd_authors.get(m["forwarded_from"], 0) + 1
    for norm, e in inv.items():
        type_counts[e["type"]] = type_counts.get(e["type"], 0) + 1
        d = urlsplit(norm).netloc.lower()
        domain_counts[d] = domain_counts.get(d, 0) + e["occurrences"]

    total_link_occ = sum(e["occurrences"] for e in inv.values())
    real_urls = {k: v for k, v in inv.items() if v["type"] != "hostname-mention"}

    stats = {
        "files": [str(Path(f).name) for f in args.files],
        "messages_total": len(messages),
        "service_messages": service_total,
        "date_first": dates[0] if dates else None,
        "date_last": dates[-1] if dates else None,
        "forwarded_messages": sum(1 for m in messages if m.get("forwarded_from")),
        "forwarded_authors": dict(sorted(fwd_authors.items(), key=lambda kv: -kv[1])),
        "link_occurrences_total": total_link_occ,
        "unique_normalized_urls": len(inv),
        "unique_real_urls_excl_hostname_mentions": len(real_urls),
        "url_type_counts_unique": dict(sorted(type_counts.items(), key=lambda kv: -kv[1])),
        "top_domains_by_occurrences": dict(sorted(domain_counts.items(), key=lambda kv: -kv[1])[:60]),
        "hashtags": dict(sorted(hashtags.items(), key=lambda kv: -kv[1]["count"])),
        "messages_with_text": sum(1 for m in messages if m["text"].strip()),
        "messages_with_links": sum(1 for m in messages if m["links"]),
        "messages_with_media_files": sum(1 for m in messages if m["media_files"]),
        "sensitive": {"counts": sens["counts"],
                      "flagged_message_count_by_category": {k: len(v) for k, v in sens["message_ids"].items()}},
    }

    def dump(name, obj):
        (outdir / name).write_text(
            json.dumps(obj, ensure_ascii=False, indent=1, sort_keys=True),
            encoding="utf-8", newline="\n")

    dump("messages.json", {"messages": messages})
    links_out = {k: inv[k] for k in sorted(inv)}
    dump("links.json", links_out)
    dump("stats.json", stats)
    (outdir / "sensitive-message-ids.json").write_text(
        json.dumps(sens["message_ids"], ensure_ascii=False, indent=1, sort_keys=True),
        encoding="utf-8", newline="\n")

    # digest: message ids of sensitive categories are still shown (ids only,
    # never the content); the text preview of a flagged message is replaced
    # with a category-only redaction notice
    flag_map = {}
    for cat, ids in sens["message_ids"].items():
        for i in ids:
            flag_map.setdefault(i, []).append(cat)
    lines = []
    for m in messages:
        flags = []
        if m.get("forwarded_from"):
            flags.append("FWD=%s(%s)" % (m["forwarded_from"], (m.get("forwarded_date") or "")[:10]))
        if m["hashtags"]:
            flags.append("#" + ",#".join(m["hashtags"]))
        nlinks = len(m["links"])
        if nlinks:
            doms = []
            for l in m["links"][:6]:
                h = urlsplit(l["href"]).netloc.lower()
                doms.append(h + ("/" + urlsplit(l["href"]).path.split("/")[1] if len(urlsplit(l["href"]).path.split("/")) > 1 and urlsplit(l["href"]).path.split("/")[1] else ""))
            flags.append("links:%d[%s]" % (nlinks, ",".join(doms[:4])))
        if m["media_files"]:
            flags.append("files:" + ",".join(m["media_files"][:2]))
        if m["id"] in flag_map:
            head = "[sensitive: %s - text preview omitted]" % ",".join(sorted(flag_map[m["id"]]))
        else:
            head = re.sub(r"\s+", " ", m["text"])[:200].strip()
        lines.append("#%d %s %s | %s" % (m["id"], (m.get("date_iso") or "")[:16], " ".join(flags), head))
    (outdir / "digest.txt").write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")

    print("messages: %d (service skipped: %d)" % (len(messages), service_total))
    print("range: %s .. %s" % (stats["date_first"], stats["date_last"]))
    print("links: %d occurrences, %d unique normalized (%d real excl. hostname-mentions)"
          % (total_link_occ, len(inv), len(real_urls)))
    print("sensitive counts:", {k: v for k, v in stats["sensitive"]["counts"].items()})
    return 0


if __name__ == "__main__":
    sys.exit(main())
