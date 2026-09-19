# Keenetic + Entware: базовая модель

**Статус:** Research (карта понятий) с Confirmed-частями (существование и
назначение файлов/команд — по репозиторию-источнику истины)
**Область применения:** роутеры Keenetic/Netcraze; подготовка OPKG-окружения
**Source of truth:** `saymer-alt/keenetic-auto-setup` (README, ARCHITECTURE.md);
официальная справка help.keenetic.com
**Provenance:** канал TechnoBypass —
[каталог: keenetic-entware](../catalog/techno-bypass/topics/keenetic-entware.md)
(#3, #8, #12–#34, #62, #69, #1091 и др.)

## Что решаем

Понять, что именно даёт Entware на Keenetic, из каких слоёв состоит «тюнинг
роутера» и какие части уже автоматизированы, а какие остаются ручными.
Статья — карта понятий, не пошаговая инструкция.

## Контекст

KeeneticOS — проприетарная ОС роутера (не OpenWrt); Entware — сторонний
репозиторий пакетов, устанавливаемый на USB-носитель или во встроенную
память. После установки появляется `/opt` со своим init-скриптами
(`/opt/etc/init.d/S99*`), cron (`/opt/etc/cron.*`) и хуками firewall
(`/opt/etc/ndm/netfilter.d/`). Всё «продвинутое» (Mihomo, MagiTrickle,
xray, вспомогательные скрипты) живёт в этом слое.

## Слои

| Слой | Что это | Пример |
|---|---|---|
| KeeneticOS | интерфейсы, policy routing, DNS-прокси, firewall | «Приоритеты подключений», `ndmc` |
| Entware | пакетный слой поверх прошивки | `opkg install curl jq` |
| Проектные скрипты | автоматизация установки/обновления | `install.sh`, `update-mihomo.sh` |
| Сервисные скрипты | экономия ресурса, обходы | `S00ubifs`, `020-bypass_wa.sh` |

## Ключевые компоненты (что подтверждено, что нет)

**Confirmed** (файлы существуют в `saymer-alt/keenetic-auto-setup`,
проверено 2026-09-19, см. OWNER_LINK_AUDIT):

- `install.sh` — единственный поддерживаемый установщик
  (`curl -fSsL …/main/install.sh | sh`; вариант `| sh -s -- disk`);
- `S00ubifs` — перенос `/opt/tmp`, `/opt/var/log`, `/opt/var/run` в tmpfs
  для снижения износа флеш-памяти (в шапке файла — ссылка на первоисточник
  Entware-команды; поведение самого скрипта отдельно не аудировалось);
- `mihomo-interface-check.sh` — диагностика WAN-интерфейсов для
  `interface-name` в конфиге Mihomo.

**Research** (описано в канале, не проверялось здесь):

- ручные «бюллетени» создания policy `bypass_wa` и маркировки
  WhatsApp/Telegram-UDP скриптом `020-bypass_wa.sh` (#17–#24, #34). Ручной
  вариант исторически предшествует автоматизации; современный fail-closed
  подход к ProxyN — в проекте, а не в старых постах.

**Historical:**

- `deploy.sh` и gist-зеркало установщика удалены из репозитория
  (2026-09-17, коммит 909a9cc); команды из ранних постов канала (#14)
  ведут на 404. Текущая команда установки — см. Confirmed выше.

## Проверка состояния окружения

```sh
opkg list-installed | grep -E 'curl|jq'   # базовые пакеты
ls /opt/etc/init.d/                        # слой сервисов
```

## Типичные проблемы

- **Логи пропадают после перезагрузки** — следствие tmpfs в `S00ubifs`
  (сам канал предупреждал, #8); для диагностики смотрите до перезагрузки.
- **«OPKG устанавливается, но ничего нет»** — установка шла не на тот
  носитель/раздел; варианты инсталляторов по архитектурам — #174, #243.

## Источники и provenance

- Канал: каталог-тема [keenetic-entware](../catalog/techno-bypass/topics/keenetic-entware.md)
  (сообщения #3–#34 — учебная серия канала; #62 RCI; #1091 — современная
  связка MagiTrickle+Mihomo).
- Код: <https://github.com/saymer-alt/keenetic-auto-setup> (README,
  ARCHITECTURE.md).

## Связанные материалы

- [docs/mihomo-keenetic-routing.md](mihomo-keenetic-routing.md)
- [docs/zapret-ecosystem.md](zapret-ecosystem.md)
