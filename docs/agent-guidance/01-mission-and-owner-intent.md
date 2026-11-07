# Owner mission, project role and cross-project provenance

> **Сохранённые исходные инструкции — 07.11.2026.** Следующие разделы перенесены из корневого `AGENTS.md` ветки `main` на коммите `e262ddf2b5f9e52d622a3abd1480e691b543ea9b` без сокращения текста; для ссылок Markdown исправлена только глубина относительных путей. Упоминания «this file» и пути в обратных кавычках относятся к прежнему корневому файлу и корню репозитория.
>
> Это **тематический справочник**, а не безусловно загружаемые инструкции. Для каждой задачи сначала действует [краткий AGENTS.md](../../AGENTS.md); загружайте только относящиеся к задаче разделы. Исторические свидетельства не становятся Confirmed без новой проверки. Эти справочники не входят в белый список опубликованных MkDocs-статей и не получают автоматически лицензию CC BY.

---

> **Обязательный контракт для всех агентов и авторов ТЗ (30.10.2026):** [подробная постановка задач без «эффекта обезьяньей лапки»](https://github.com/saymer-alt/saymer-alt/blob/main/AGENT-TASK-CONTRACT.md). Перед работой проверить исходные refs/SHA, готовые результаты, точную цель, scope/non-goals, сохранность данных и сервисов, зависимости, границы разрешений/owner GO, негативную приёмку и доказательства. Не сокращать существенные требования ради токенов. Буквальное выполнение в ущерб цели считается **FAIL**. Местные правила безопасности и архитектуры обязательны.

> **Владелец, 26.10.2026 — общее правило для всех проектов:** перед внедрением новой функции / серьёзной переделки требуется короткая «защита идеи» — доказать проблему, сравнить альтернативы (включая ничего не менять / штатную ОС / ждать upstream), оценить пользу, **ТЭО**, стоимость сопровождения, риски, измеримый тест и критерии STOP. Нет доказательства пользы — DEFER/SKIP. Мелкие исправления не требуют отдельной бюрократии. **Источник:** [Proof Before Build](https://github.com/saymer-alt/saymer-alt/blob/main/PROOF-BEFORE-BUILD.md) ([центральный PR #9](https://github.com/saymer-alt/saymer-alt/pull/9)). Существующие safety/CI/permissions сохраняются.

# AGENTS.md — keenetic-knowledge-base

## Owner-wide design gate — SIMPLICITY-FIRST (2026-10-24)

Before a new service, subsystem, manager, web panel, installer/uninstaller, or heavy CI path, apply the [common engineering contract](https://github.com/saymer-alt/saymer-alt/pull/7). First compare: (A) existing/manual route, (B) smallest safe change, (C) ambitious design. Choose A/B unless C has evidence, cost/complexity budget, and explicit owner approval. If a helper grows into another platform or expensive E2E cycles repeat without new evidence, STOP adding layers and seek an architectural decision. Preserve all verified safety boundaries and working user behavior. [KAS uninstall retrospective #225](https://github.com/saymer-alt/keenetic-auto-setup/issues/225) is an **anti-pattern**, not a best-practice pattern. This documentation change does not authorize production or release modifications.

Instructions for AI agents working in this repository.

This repository is intentionally different from the owner's production repositories.
It is a **knowledge workshop**: part archive, part research notebook, part staging area for
material that may later become documentation, scripts, tests, or design decisions in other
projects.

The goal is not to make every old file look neat. The goal is to **recover useful knowledge
without turning old chat fragments, experiments, or AI answers into false documentation**.

## 1. What this repository is

The original idea was a structured Keenetic knowledge base. The current repository is not
there yet.

Today it contains a mixture of:

- useful Keenetic / Entware / networking notes;
- research about VPN, proxies, DNS, DPI, Mihomo, Xray, AmneziaWG and related tools;
- working or experimental shell scripts;
- finished or nearly finished subprojects such as the NVR material;
- copied conversations and AI-generated research;
- Telegram TechnoBypass exports and material derived from the channel;
- notes about VPS/Linux/MosTech/virtualization that are only partly related to Keenetic;
- unrelated historical material that happened to be stored here.

The old README used to describe planned paths such as `docs/`, `dpi/` and `links/`
that did not exist. README.md has now been rewritten as a truthful entry point to the
transition state. Keep it synchronized with the real tree: planned structure belongs in
ROADMAP.md, not in README as if it already existed.

## 2. Main mission

Work in this repository should move information through this pipeline:

```
raw material
    ↓
inventory / classification
    ↓
fact checking against current sources and current project code
    ↓
small, topic-focused knowledge article
    ↓
optional promotion into the repository that actually owns the behavior
    ↓
raw source kept or archived for provenance
```

The important word is **promotion**.

This repository may discover or explain something useful for another project, but it must not
silently become the source of truth for behavior implemented elsewhere.

Examples:

- Mihomo installation/watchdog/router integration → verify against
  `saymer-alt/keenetic-auto-setup`.
- Link/config generation, Mihomo protocol support and validation → verify against
  `saymer-alt/link-generators` and its web4core fork.
- Entware package versions/build workflows → verify against `saymer-alt/entware-go`.
- VPS gateway/bootstrap behavior → verify against the relevant VPS repository before
  publishing a claim here as current behavior.

If another repository owns the code, **that code is authoritative**. This repository can
explain it, index it, compare it, or preserve research behind it.


## 9. Reuse in the owner's other projects

One of the main purposes of this repository is to salvage useful work for the rest of the
owner's ecosystem.

When useful material is found:

1. identify which project actually owns the subject;
2. inspect that project's AGENTS.md before proposing a change there;
3. compare the old note with current implementation and documentation;
4. extract only what is still correct and useful;
5. keep the change in the target project minimal and native to that project's architecture;
6. leave a short reference here when doing so improves provenance.

Do not copy the same maintained documentation into several repositories. Prefer:

- canonical behavior next to the code that implements it;
- conceptual/background material here;
- links between them.

This repository can act as an **index and research memory**, but should not create competing
sources of truth.

## AI agent engineering upstream research (30.10.2026)

Preserve the original research and provenance in [docs/ai-agent-engineering-pstack.md](../../docs/ai-agent-engineering-pstack.md). Cross-project normative rules belong to [saymer-alt/saymer-alt, PR #11](https://github.com/saymer-alt/saymer-alt/pull/11), not to this knowledge-base research article; respect each target repository's AGENTS, constitution and owner GO.
