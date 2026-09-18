# MagiTrickle

Избирательная маршрутизация доменов в туннель/политику через перехват DNS
на Keenetic. Один из трёх китов базовой схемы канала
(Mihomo + MagiTrickle + watchdog).

## Документация и установка

- **Официальная документация** — <https://magitrickle.dev/docs/welcome/> —
  Source: #28; гайд по Keenetic —
  <https://magitrickle.dev/docs/getting-started/keenetic/> — Source: #29.
- **Репозиторий пакетов**: `wget -qO- http://bin.magitrickle.dev/packages/add_repo.sh | sh`
  → `opkg update && opkg install magitrickle` → `S99magitrickle start` —
  Source: #31, #32, #36, #48 (bin.magitrickle.dev).
- **Установка конкретного релиза** (через GitHub API и
  `opkg print-architecture`) — Source: #46.
- **Ручная установка .ipk** (`opkg install --force-reinstall /opt/tmp/…`) —
  Source: #895 (вложение `magitrickle_0.7.1git.ipk`).
- GitLab-зеркало — <https://gitlab.com/magitrickle/magitrickle> —
  Source: #1117.

## Конфигурация

- **Интерфейс t2s0** для списков MagiTrickle (веб на :8080) — Source: #1091
  (перепост Internet Helper; полная связка MagiTrickle + Mihomo от KeeneticOS
  3.9+).
- Ограничение: если на клиенте вручную задан частный DNS — связка не
  работает; при своём WireGuard-сервере на роутере — указать IP роутера как
  DNS клиента — Source: #1091.
- Ранняя «бюллетень»-версия настройки (domainlist, policy=bypass_wa, ipset,
  опрос DNS-кэша) — Source: #30. **Historical**: конфигурационный формат
  modern MagiTrickle другой; запись ценна как история концепции.

## Редакторы конфигураций

| Редактор | Source |
|---|---|
| [kiarant/editorMT](https://kiarant.github.io/editorMT) | #42 |
| [qp-io magitricle-editor](https://qp-io.github.io/magitrickle/magitricle-editor) | #42 (пакетная вставка доменов) |

## Модификации и связки

- [LarinIvan/MagiTrickle_Mod](https://github.com/LarinIvan/MagiTrickle_Mod) —
  модифицированная версия — Source: #1091.
- [avgustvishne/CDN-Cloud-MagiTrickle](https://github.com/avgustvishne/CDN-Cloud-MagiTrickle) —
  Source: #1230.
- Списки доменов для правил — см. [whitelist-mode.md](whitelist-mode.md)
  (подсети/доменные списки применимы и здесь) и [dns.md](dns.md).
