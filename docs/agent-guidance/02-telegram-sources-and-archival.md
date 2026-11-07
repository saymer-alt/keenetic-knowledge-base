# TechnoBypass primary-source workflow and archival classification

> **Сохранённые исходные инструкции — 07.11.2026.** Следующие разделы перенесены из корневого `AGENTS.md` ветки `main` на коммите `e262ddf2b5f9e52d622a3abd1480e691b543ea9b` без сокращения текста; для ссылок Markdown исправлена только глубина относительных путей. Упоминания «this file» и пути в обратных кавычках относятся к прежнему корневому файлу и корню репозитория.
>
> Это **тематический справочник**, а не безусловно загружаемые инструкции. Для каждой задачи сначала действует [краткий AGENTS.md](../../AGENTS.md); загружайте только относящиеся к задаче разделы. Исторические свидетельства не становятся Confirmed без новой проверки. Эти справочники не входят в белый список опубликованных MkDocs-статей и не получают автоматически лицензию CC BY.

---

## 3. TechnoBypass is a primary source corpus

The owner's Telegram channel **TechnoBypass** is one of the main research inputs for this
repository.

Treat the channel as an **inbox and discovery stream**, not as an authoritative technical
source. It may contain:

- links worth preserving;
- original owner notes;
- real-world observations;
- forwarded posts from other people or channels;
- project announcements;
- AI-generated text;
- speculative workarounds;
- outdated instructions;
- duplicate references to the same project.

The desired flow is:

```
TechnoBypass export
    ↓
parse messages and links
    ↓
preserve provenance
    ↓
deduplicate / classify / index
    ↓
review and verify
    ↓
canonical knowledge or promotion to the owning project
```

### Telegram import rules

When processing a Telegram export:

1. Preserve useful provenance whenever available:
   - Telegram message ID;
   - date/time;
   - whether the post is original or forwarded;
   - forwarded author/channel when relevant;
   - source URL;
   - enough surrounding text to understand why the resource was saved.
2. Normalize and deduplicate repeated links conservatively.
3. Do not collapse distinct GitHub issues, releases, files, branches, documentation pages or
   distinct Telegram posts merely because they share a domain or repository.
4. Imported material starts as **Source** or **Research** unless there is independent evidence
   for a stronger status.
5. A confident Telegram statement is not sufficient for **Confirmed**.
6. A forwarded statement proves that the statement appeared in the source corpus; it does not
   prove that the statement is technically correct.
7. Preserve useful negative results, operator observations and historical context.
8. Keep unclassified material instead of forcing a false category.

### Raw export policy

Raw Telegram HTML exports should **normally not be committed** to this public repository.

They may contain:

- private or internal Telegram links;
- names and attribution from forwarded messages;
- repeated/generated HTML;
- credentials or sensitive strings copied into a post;
- unrelated conversation noise.

Prefer committing normalized Markdown/catalog data derived from the export.

Never publish private keys, tokens, credentials, subscription URLs containing secrets,
private infrastructure details or sensitive private-channel references discovered during
import. Record only that sensitive source material was omitted when provenance needs to be
preserved.

### Catalog versus canonical knowledge

A catalog entry answers:

- what resource was found;
- what topic it belongs to;
- where it appeared;
- why it may be interesting.

A canonical article additionally requires verification.

Do not turn the catalog into thousands of copied Telegram posts. Summarize context, preserve
links and provenance, and promote only the material that is worth maintaining.

Where the current artifacts live:

- curated catalog: `catalog/techno-bypass/` (status model and provenance rules are
  documented in its README; audits live next to it as REVIEW.md, SECURITY_REVIEW.md,
  OWNER_LINK_AUDIT.md, VERIFIED_RESOURCES.md);
- parser: `tools/parse_telegram_export.py`;
- maintained extracted articles: `docs/`.

## 4. Do not destroy the useful junk

A large file can be ugly and still contain unique information.

Do not delete, heavily rewrite, or split old material merely because it looks like a chat dump.
Before changing an existing raw file, determine whether it contains:

- unique commands or configuration examples;
- results of real tests;
- historical reasoning behind a later project decision;
- links or source references;
- failure cases that are not documented elsewhere;
- operator observations that cannot be reconstructed from public documentation.

Prefer **extract + preserve** over **rewrite in place**.

When reorganizing the repository, raw/historical material should normally move to an archive
or source area while cleaned knowledge is written separately. Git history is useful, but it is
not a substitute for keeping important provenance understandable in the current tree.

Since 2026-09-24 that archive is `archive/` (`archive/raw/` for extracted research
snapshots, `archive/historical/` for superseded artifacts and historical/creative
material; the mapping to maintained articles is in `archive/README.md`).
`archive/` is provenance/history: do not promote claims from it without re-verification
against current sources.

## 5. Classification before cleanup

Before a broad cleanup, classify files rather than moving them by filename alone.

Useful classes are:

- **canonical** — already suitable as maintained documentation;
- **candidate** — useful material that should become a proper article;
- **source/raw** — conversation, research dump, experiment notes, copied output;
- **project artifact** — script/config that should be tested and documented as code;
- **historical** — useful for understanding how a solution evolved, but not current guidance;
- **unrelated** — not part of the Keenetic/networking knowledge base;
- **duplicate/obsolete** — only after the newer authoritative replacement is identified.

Do not call something obsolete simply because it is old. A dated workaround may still explain
why a current guard, fallback, or architecture exists.

