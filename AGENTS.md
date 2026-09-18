# AGENTS.md — keenetic-knowledge-base

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

## 8. Scripts and dangerous examples

Some files contain executable shell code, firewall rules, routing changes, service units,
VPN configuration, Docker/networking setup, or router commands.

Treat those as operational code, not harmless prose.

Without an explicit owner task, do not:

- run commands against a live router or VPS;
- change routes, DNS, firewall rules, policy routing, VPN interfaces or persistent Keenetic
  configuration;
- publish secrets, private keys, tokens, credentials, subscription URLs, private IP inventory
  or other sensitive values found in old material;
- replace a working script with a "cleaner" rewrite just because it looks old;
- use `chmod 777`, `eval`, disabled TLS verification, blind `curl | sh`, global firewall
  flushes, or other unsafe shortcuts as recommended practice;
- remove rollback/recovery steps from networking instructions.

For a script promoted from raw material into maintained code, inspect it as code: shell
dialect, dependencies, idempotency, failure behavior, quoting, temporary files, permissions,
network side effects and rollback.

A command copied from a chat is not considered tested code.

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

## 10. Repository restructuring

A future structure may include areas such as `docs/`, `reference/`, `scripts/` and
`archive/raw/`, but the exact layout is not sacred.

Do not perform a mass move/rename/delete in one opaque change.

For a large reorganization:

1. inventory the current tree;
2. propose or document the mapping;
3. preserve raw material first;
4. create cleaned documents separately;
5. repair internal links;
6. update README only after the new paths actually exist;
7. review the final diff for accidental loss.

A smaller, understandable series of commits is preferable to one giant "cleanup" commit.

## 11. README policy

README.md should eventually become the real entry point to the knowledge base, not a promise
about directories that do not exist.

Until the reorganization is actually implemented:

- do not add more fictional paths;
- do not describe planned sections as completed;
- do not rewrite README around a new taxonomy unless the files are created in the same work;
- when the structure changes, keep README navigation synchronized with the tree.

## 12. Git working rules

Before editing:

- inspect the current tree and the relevant files;
- check recent history when a file looks like the result of an earlier project decision;
- understand whether the task is archival, editorial, research, or code work;
- keep unrelated cleanup out of the diff.

Before committing:

- review the complete diff;
- make sure no secrets were introduced;
- make sure moved/extracted material was not accidentally truncated;
- verify links and commands that were changed;
- clearly distinguish verified facts from notes that still need verification.

Do not force-push or rewrite history.

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
