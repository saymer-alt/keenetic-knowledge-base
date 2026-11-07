# Evidence levels, article writing and truthful progress

> **Сохранённые исходные инструкции — 07.11.2026.** Следующие разделы перенесены из корневого `AGENTS.md` ветки `main` на коммите `e262ddf2b5f9e52d622a3abd1480e691b543ea9b` без сокращения текста; для ссылок Markdown исправлена только глубина относительных путей. Упоминания «this file» и пути в обратных кавычках относятся к прежнему корневому файлу и корню репозитория.
>
> Это **тематический справочник**, а не безусловно загружаемые инструкции. Для каждой задачи сначала действует [краткий AGENTS.md](../../AGENTS.md); загружайте только относящиеся к задаче разделы. Исторические свидетельства не становятся Confirmed без новой проверки. Эти справочники не входят в белый список опубликованных MkDocs-статей и не получают автоматически лицензию CC BY.

---

## 6. Knowledge quality rules

This repository must distinguish between four kinds of statements:

1. **Observed** — tested by the owner or captured from a real system.
2. **Confirmed** — verified against current code or authoritative documentation.
3. **Historical** — true for an older version/configuration but not necessarily current.
4. **Hypothesis / research note** — plausible, but not yet confirmed.

Do not silently convert category 4 into category 2.

Old AI answers are **sources to investigate, not evidence by themselves**. Text such as
"ChatGPT said...", "Claude checked...", or a confident answer copied from a conversation
must be independently checked before it becomes canonical documentation.

When current facts matter (protocol support, version behavior, package availability, CLI,
KeeneticOS behavior, Mihomo/Xray fields, etc.), verify them against current upstream sources
or the actual current project code.

Do not invent citations, test results, device compatibility, version support, or production
experience.

## 7. Article style

Maintained user-facing knowledge should normally be in Russian. This AGENTS.md is in English
because it is instructions for coding/research agents.

Prefer small topic-focused documents over giant transcripts.

A good article should answer:

- what problem this solves;
- where it applies;
- prerequisites and assumptions;
- the actual configuration/procedure;
- how to verify it;
- common failure modes;
- rollback/recovery when changes can break networking;
- where the claim came from and what is still uncertain.

Do not pad articles with generic explanations when the repository has concrete operational
knowledge.

Preserve exact commands, paths, interface names, ports and config keys when they are part of
the technical contract, but separate examples from universal requirements.

## 11. README policy

README.md should eventually become the real entry point to the knowledge base, not a promise
about directories that do not exist.

Until the reorganization is actually implemented:

- do not add more fictional paths;
- do not describe planned sections as completed;
- do not rewrite README around a new taxonomy unless the files are created in the same work;
- when the structure changes, keep README navigation synchronized with the tree.

## 13. What "good progress" looks like here

Good progress is not measured by how many files were reformatted.

Good progress means one or more of the following:

- a useful fact hidden in a chat dump became a verified article;
- an old experiment was clearly marked historical instead of being mistaken for current advice;
- a working script gained enough context and safety notes to be reusable;
- duplicate information was replaced by a link to the actual source of truth;
- useful research was promoted into one of the owner's active projects after verification;
- unrelated material was safely archived without losing potentially useful history;
- README became more truthful about what the repository actually contains.

When unsure whether something is trash, **preserve it and classify it first**. The whole point
of this repository is to turn accumulated material into useful engineering knowledge without
losing the reasons and experiments that produced it.

