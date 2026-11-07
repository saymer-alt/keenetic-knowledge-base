# Unsafe scripts, cautious restructuring and Git rules

> **Сохранённые исходные инструкции — 07.11.2026.** Следующие разделы перенесены из корневого `AGENTS.md` ветки `main` на коммите `e262ddf2b5f9e52d622a3abd1480e691b543ea9b` без сокращения текста; для ссылок Markdown исправлена только глубина относительных путей. Упоминания «this file» и пути в обратных кавычках относятся к прежнему корневому файлу и корню репозитория.
>
> Это **тематический справочник**, а не безусловно загружаемые инструкции. Для каждой задачи сначала действует [краткий AGENTS.md](../../AGENTS.md); загружайте только относящиеся к задаче разделы. Исторические свидетельства не становятся Confirmed без новой проверки. Эти справочники не входят в белый список опубликованных MkDocs-статей и не получают автоматически лицензию CC BY.

---

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

