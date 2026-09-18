# Проекты владельца, отражённые в канале

Канал TechnoBypass — «публичная витрина» работы владельца: в нём
анонсировались и обсуждались его собственные проекты и материалы этого
репозитория. Файл — карта соответствий «сообщение канала ↔ проект».

> Правило репозитория: код проекта — источник истины. Канал фиксирует
> историю и моменты публикации, но не переопределяет текущее состояние
> репозиториев.

## saymer-alt/keenetic-auto-setup

- #14 (2025-09-16) — «редактируемый пост» со ссылкой на репозиторий и
  curl-установкой **deploy.sh** (+ gist-зеркало). **Broken (проверено
  2026-09-19)**: `deploy.sh` удалён из репозитория 2026-09-17 (коммит
  909a9cc), gist-зеркало `ecd0706b…` также удалено (404 через API).
  Единственный поддерживаемый путь — `install.sh`. Готовый текст замены
  поста — в [OWNER_LINK_AUDIT.md](../OWNER_LINK_AUDIT.md).
- #923 (2026-06-05) — история «Почему я вообще сделал Keenetic Auto Setup»:
  мотивация, цели, чего не хотелось. Ценный provenance для README проекта.
- #1125 (2026-08-06) — рекомендация [ARCHITECTURE.md](https://github.com/saymer-alt/keenetic-auto-setup/blob/main/ARCHITECTURE.md)
  (файл существует — current).
- #922 — прямая ссылка на репозиторий.
- **Дипломированные артефакты канала** (проверено 2026-09-19): скрипт
  `S00ubifs` из #13 теперь поставляется файлом в корне репозитория;
  «Mihomo Interface Checker» из #1127 — как `mihomo-interface-check.sh`;
  мануал ручного обновления из #815 удалён вместе с deploy.sh — заменён
  `update-mihomo.sh`.

## saymer-alt/link-generators

- #990 (2026-06-24) — анонс онлайн-генератора
  <https://saymer-alt.github.io/link-generators/> (+ страница mihomo.html,
  позже удалённая из проекта).
- #1156 (2026-08-19) — «переделал генератор… теперь работает с файлами от
  vernette/warpscout». **Historical**: поддержка warpscout позже осознанно
  убрана из продукта; сообщение фиксирует эту фазу (не «восстанавливать»).
- Предыстория MASQUE-шаблона — #978–#984 (см. [mihomo.md](mihomo.md)).

## saymer-alt/amnezia-mihomo-gateway

- #1088, #1090 (2026-07-25) — публикация репозитория и README: скрипт
  маршрутизации AmneziaWG-контейнера через Mihomo TUN на VPS
  (auto-detect подсети/порта AWG, sysctl, systemd, watchdog на
  `tun-mihomo`, `Restart=always`).
- #1089 — «работает на четырёх моих серверах» (Observed).
- #1088 также ссылается на `uninstall.sh` этого репозитория (KB).
- Родня: VPS-кластер KB (`amnezia.md`/`awg.md`/`check.md`/`install.sh`) и
  [#1079 warp-docker-routing](../topics/vps-server.md).

## saymer-alt/keenetic-knowledge-base (этот репозиторий)

Канал анонсировал материалы, которые сейчас лежат здесь:

| Сообщение | Материал |
|---|---|
| #1075 | `MosTech.md` |
| #1080 | `virtiofsd.md` |
| #1082 | `VirtIO-FS.md` |
| #1140 | `NVR/README.md` (Keenetic NVR) |
| #1147 | `proxy.md` (таксономия VPN/proxy/транспорт/маскировка) |
| #1088 | `uninstall.sh` |

## saymer-alt/entware-go

- #801 (2026-05-06, форвард Stas) — сборка beszel-agent:
  [PR #12](https://github.com/Entware/entware-go/pull/12) (aarch64/mipsel/mips).
  **Проверено 2026-09-19**: PR смержен 2026-08-29; автор — **spatiumstas**
  (upstream, не владелец); пакет пришёл в `saymer-alt/entware-go` синком
  2026-09-07. Каталожное упоминание — про линию форка, не про авторство PR.
- #817 — «тру автосборщик»: workflow
  [build-mihomo.yml](https://github.com/spatiumstas/entware-go/blob/gh-action-build/.github/workflows/build-mihomo.yml)
  (fork = источник saymer-alt линии; upstream-репозиторий третьего лица).
- #46 — установка MagiTrickle из GitHub Releases с фильтром по архитектуре
  (паттерн того же семейства).

## awg-manager (hoaxisr) и ядерный модуль AWG

- [hoaxisr/awg-manager](https://github.com/hoaxisr/awg-manager) — Source:
  #1117 (в наборе оффлайн-инсталляторов sw.ext.io); репозиторий активен
  (проверено 2026-09-19).
- ~~hoaxisr/amneziawg-linux-kernel-module-keenetic~~ — Source: #404;
  эффект на MT7621 (−50% CPU) — #402, #403 (форварды Nightman; Observed
  авторами форвардов). **Broken (проверено 2026-09-19)**: репозиторий
  больше не резолвится (удалён/переименован владельцем — третьим лицом).
  См. [OWNER_LINK_AUDIT.md](../OWNER_LINK_AUDIT.md).

## Прочие следы работы владельца в канале

- Генератор «по способу @Ponywka» (вложения generated.html) — #80, #82
  (2025-09-16): ранняя форма генератора конфигов. **Historical**.
- FoxyProxy-наборы RegExp (#413, #896, #992, #1072) — вспомогательные
  артефакты работы с прокси.
- `webtunnel`-мостики с documentary-адресами 2001:db8:: (#212–#216, #1070) —
  тестовый материал; ключи/URL в каталог не переносятся.
