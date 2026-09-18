# OWNER LINK AUDIT — ссылки на проекты владельца (TASK-TB-02B)

Проверка owner-controlled ссылок каталога перед проверкой сотен внешних
ресурсов. Дата проверки: 2026-09-19. Методы: локальные клоны
`keenetic-auto-setup` / `keenetic-knowledge-base` (git-история и дерево),
GitHub API (`gh` как saymer-alt, read-only), HTTP-проверка Pages.
Сами Telegram-посты не редактируются (нет полномочий) — ниже даётся
готовый текст замены для ручной правки оператором.

## Сводка находок

| # | Сообщение | Старая ссылка/команда | Текущий источник истины | Статус | Действие оператора |
|---|---|---|---|---|---|
| 1 | #14 | `raw…/keenetic-auto-setup/main/deploy.sh` (3 варианта команды, включая `--resolve` и `/etc/hosts`) | `README.md` §1: `install.sh` (см. текст замены ниже) | **broken** (файл удалён коммитом 909a9cc, 2026-09-17) | отредактировать закреплённый пост |
| 2 | #14 | gist-зеркало `gist…/saymer-alt/ecd0706b286bd6f9b63e07fce5ee60dc/raw/keenetic_deploy.sh` (+wget-вариант) | — | **broken** (gist 404 через API от имени saymer-alt — удалён/скрыт) | убрать из поста вместе с deploy.sh |
| 3 | #14 | `github.com/saymer-alt/keenetic-auto-setup` (корень) | репозиторий активен (f0a8f33+) | **current** | — |
| 4 | #14 | `/opt/etc/init.d/S99mihomo restart` | сервис S99mihomo — текущий контракт установщика | **current** | — |
| 5 | #922, #923 | корень репозитория; история «почему сделал» | репозиторий активен | **current** | — |
| 6 | #1125 | `blob/main/ARCHITECTURE.md` | файл существует в корне репозитория | **current** | — |
| 7 | #815 | вложение-PDF «Mihomo Manual Update Arm…» | `update-mihomo.sh` (единственный поддерживаемый путь обновления; мануал `mihomo_manual_update_arm.md` удалён тем же 909a9cc) | **superseded** | пост можно дополнить ссылкой на update-mihomo.sh |
| 8 | #990 | `saymer-alt.github.io/link-generators/` | генератор активен (main = prod) | **current** | — |
| 9 | #990 | `saymer-alt.github.io/link-generators/mihomo.html` | страница удалена намеренно (404 проверен 2026-09-19) | **historical** (by design) | правка не обязательна; анонс своей эпохи |
| 10 | #1156 | генератор + поддержка файлов vernette/warpscout | warpscout-парсер осознанно убран из продукта; пост фиксирует ту фазу | **historical** (не «чинить» возвратом функции) | — |
| 11 | #1088, #1090 | `github.com/saymer-alt/amnezia-mihomo-gateway` | репозиторий существует, public, активен (обновлён 2026-09-18) | **current** | — |
| 12 | #1088 | `keenetic-knowledge-base/blob/main/uninstall.sh` | файл существует | **current** | — |
| 13 | #1075, #1080, #1082, #1140, #1147 | `MosTech.md`, `virtiofsd.md`, `VirtIO-FS.md`, `NVR/README.md`, `proxy.md` | все файлы в текущем дереве KB | **current** | — |
| 14 | #801 | `Entware/entware-go` PR #12 (beszel-agent) | PR **MERGED** 2026-08-29; автор — **spatiumstas** (не владелец); пакет пришёл в `saymer-alt/entware-go` синком от 2026-09-07 | **current** (уточнение авторства в каталоге) | — |
| 15 | #817 | `spatiumstas/entware-go` workflow build-mihomo.yml | upstream-репозиторий третьего лица (источник линии форка) | не проверялся live (третье лицо) | — |
| 16 | #402–#405, #1117 | `hoaxisr/amneziawg-linux-kernel-module-keenetic` | репозиторий **не резолвится** (нет в текущем списке репозиториев hoaxisr) | **broken** (третье лицо; канал править не можем) | при необходимости уточнить у hoaxisr новое имя |
| 17 | #1117 | `hoaxisr/awg-manager` | активен (push 2026-09-18) | **current** | — |
| 18 | #13, #12, #95 | S00ubifs (pastebin `xALmaqsD` и вложения) | скрипт **вырос в файл `S00ubifs`** в корне `keenetic-auto-setup` (MIT; в шапке — первоисточник Entware pastebin `6SyQqPHJ`) | **superseded** (каноник — репозиторий) | — |
| 19 | #1127 | «Mihomo Interface Checker» (пост-утилита) | поставляется как `mihomo-interface-check.sh` (v1.0.3) в `keenetic-auto-setup` | **current** (дипломирован в репозиторий) | — |

Примечание к keenetic-auto-setup: в локальном клоне есть незакоммиченная
правка `install.sh` (атомарный same-fs стейджинг watchdog-бинарника) —
рабочий материал оператора, к ссылкам отношения не имеет.

## Предлагаемая замена для закреплённого поста #14 (ручная правка)

```text
Актуально на сентябрь 2026

Установка (единственный поддерживаемый путь):
opkg update && opkg install curl && \
curl -fSsL https://raw.githubusercontent.com/saymer-alt/keenetic-auto-setup/main/install.sh | sh

Вариант для внешнего носителя (USB HDD/NVMe):
opkg update && opkg install curl && \
curl -fSsL https://raw.githubusercontent.com/saymer-alt/keenetic-auto-setup/main/install.sh | sh -s -- disk

Обновление Mihomo:
curl -fSsL https://raw.githubusercontent.com/saymer-alt/keenetic-auto-setup/main/update-mihomo.sh | sh

Диагностика:
curl -fSsL https://raw.githubusercontent.com/saymer-alt/keenetic-auto-setup/main/mihomo-doctor.sh | sh

Репозиторий: https://github.com/saymer-alt/keenetic-auto-setup

P.S. deploy.sh и gist-зеркало из старой версии поста удалены и не
поддерживаются; используйте install.sh.
```

Для поста #815 (опционально) добавить строку:
`Актуальный путь обновления: curl -fSsL https://raw.githubusercontent.com/saymer-alt/keenetic-auto-setup/main/update-mihomo.sh | sh`

## Что проверено и чем

- `keenetic-auto-setup`: git-история (`deploy.sh` удалён в 909a9cc вместе с
  `mihomo_manual_update_arm.md`), текущее дерево (`install.sh`,
  `update-mihomo.sh`, `mihomo-doctor.sh`, `ARCHITECTURE.md`, `S00ubifs`,
  `mihomo-interface-check.sh`), README §1 (канонические команды).
- GitHub API: gist `ecd0706b…` (404), `saymer-alt/amnezia-mihomo-gateway`
  (активен), `Entware/entware-go` PR #12 (MERGED, автор spatiumstas),
  репозитории saymer-alt (существуют), список репозиториев hoaxisr
  (kernel-module отсутствует, awg-manager активен).
- HTTP: `saymer-alt.github.io/link-generators/mihomo.html` → 404 (by design).
- `keenetic-knowledge-base`: все шесть файлов, анонсированных каналом, в дереве.

Внешние (не owner) ссылки каталога здесь намеренно не проверялись —
они очередь TASK-TB-02C/liveness-прохода.
