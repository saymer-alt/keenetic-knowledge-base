# Keenetic + Entware/OPKG

Базовый слой канала: установка Entware, продление жизни флеш-памяти,
системные скрипты, ndmc/RCI, полезные темы форума.
Статусы ниже — Source (появилось в канале), если не указано иное;
техническая проверка не проводилась.

## Установка Entware / OPKG

- **Официальная статья Keenetic — установка OPKG на встроенную память**
  — <https://help.keenetic.com/hc/ru/articles/360021888880>
  — Source: #3 (2025-09-16). Первый материал канала.
- **Установщики по архитектуре** (`opkg disk storage:/…installer.tar.gz`,
  варианты aarch64/mipsel) — Source: #174, #243, #244, #790.
  Канонический источник — <https://bin.entware.net>.
- **Оффлайн-инсталляторы для Keenetic/Netcraze со sw.ext.io**
  (варианты с nfqws2+web, openssh/dropbear) — Source: #1117 (2026-08-03).
  См. также [dpi-zapret.md](dpi-zapret.md).

## S00ubifs — tmpfs для /opt/tmp, /opt/var/log, /opt/var/run

Скрипт перевода сервисных каталогов в RAM для снижения износа флеш-памяти.
Канал сопровождает его всей жизни: публикация pastebin-версии, доработки,
вариант для устройств с 128 МБ RAM, чат-версии с проверкой свободной памяти.

- Pastebin-оригинал: <https://pastebin.com/xALmaqsD> — Source: #12, #95.
- Файловые вложения канала: `S00ubifs` (4.4 KB, #13), доработанные версии
  (#106, #127, #129 — вложения не экспортированы).
- Вариант для 128 МБ RAM (меньшие квоты tmpfs) — Source: #106 (2025-09-17).
- Правильное размещение: `/opt/etc/init.d/S00ubifs`, права 0755,
  управление `start|stop|status|enable|disable` — Source: #13.
- **Status: Research** (скрипт не аудировался; логи в tmpfs пропадают при
  перезагрузке — предупреждение самого канала, #8).

## bypass_wa и 020-bypass_wa.sh (ручной вариант)

Серия «бюллетеней» о ручном построении туннельного пула: приоритет
подключений `bypass_wa`, перенос туда VPN-интерфейсов, обслуживание через
него трафика OPKG, маркировка UDP WhatsApp/Telegram (порты 1400,3478,3482)
скриптом `/opt/etc/ndm/netfilter.d/020-bypass_wa.sh` (цепочка
`_CUST_BYPASS_WA_`, mangle, метка из API localhost:79 через curl+jq).

- Source: #17, #18, #19, #20, #23, #24 (вложение скрипта), #33, #34, #97.
- **Status: Historical/Superseded (частично)** — ручные бюллетени описывают
  ту же архитектуру, которую позже автоматизировал
  [`saymer-alt/keenetic-auto-setup`](owner-projects.md); паттерн
  `020-bypass_wa.sh` в mangle/own-chain жив и в автоматизированной версии.
  Ручные шаги `ndmc` без проверок UNKNOWN не соответствуют текущему
  fail-closed-подходу проекта.

## ndmc: SOCKS-прокси-интерфейсы Proxy0/Proxy1/Proxy2

Создание системных прокси-интерфейсов, привязанных к локальным портам
Xray (1080/1081/1082), с `socks5-udp` и сохранением конфигурации.

- Source: #15, #16, #101, #183, #279. Связано с [xray-vless.md](xray-vless.md).
- Полезное дополнение: `interface Proxy0 ping-check profile <имя>` —
  Source: #315, #1210 (профили ping-check для WireGuard/прокси-интерфейсов).

## RCI / REST API роутера

- REST-вкладка веб-интерфейса: `GET interface/...` — Source: #62.
- Прямые URL вида `http://192.168.1.1/rci/interface/Wireguard0/...` —
  Source: #135. См. также [topics/owner-projects.md](owner-projects.md)
  про отказ от слепого RCI в собственных проектах.

## Системное обслуживание

- **Dropbear**: смена порта через `/opt/etc/config/dropbear.conf`,
  PID-файл `/opt/var/run/dropbear.pid` — Source: #69; фикс «умершего»
  dropbear (сбитый pid) — Source: #371; оригинальный конфиг Entware —
  Source: #826; фикс-скрипт `dropbear_fix` — Source: #169.
- **Бэкап Entware**: `tar`-архив установки на флешку/внутреннюю память —
  Source: #738.
- **Смена загрузочного слота** (dual image, webcli без Entware):
  `copy proc:/dual_image/boot_backup proc:/dual_image/boot_active` и т.п. —
  Source: #530, #532. **Research**: операция затрагивает загрузку; канал
  сам помечает «на свой страх и риск».
- **Перезагрузка по расписанию** (Netcraze support) — Source: #785.
- **Asterisk IP-PBX как OPKG-пакет** (Netcraze support) — Source: #874.
- **Доступ по SSH из интернета** (help.keenetic, KN-1012) — Source: #67.

## Прочие Keenetic-инструменты (GitHub)

| Проект | Что (по контексту канала) | Source |
|---|---|---|
| [R17a/Susanin.Keenetic](https://github.com/R17a/Susanin.Keenetic) | Keenetic-утилита (без расшифровки в канале) | #1221 |
| [ivn-git/PolicyTraySwitch](https://github.com/ivn-git/PolicyTraySwitch) | Переключалка политик Keenetic в трее Windows + монитор внешнего IP (тема форума #28834) | #902, #942 |
| [Stak646/keenetic-TG-Bot](https://github.com/Stak646/keenetic-TG-Bot) | Telegram-бот управления Keenetic | #506 |
| [Eralde/mndw-opkg-feed](https://github.com/Eralde/mndw-opkg-feed) | OPKG-фид (MDNS?) | #1047 |
| [keenetic/lpac](https://github.com/keenetic/lpac) | eSIM-утилита от Keenetic | #1111 |
| [keenetic/multifast](https://github.com/keenetic/multifast) | Официальный репозиторий Keenetic | #889 |
| [nikrays/keen_bypass_public](https://github.com/nikrays/keen_bypass_public) | Скрипт установки/настройки фильтрации трафика (загрузка пакетов, автозапуск) | #306 |
| [invisible25/keenetic-vpn-xor](https://github.com/invisible25/keenetic-vpn-xor) | XOR-обфускация для VPN на Keenetic | #1003 |
| [hoaxisr/amneziawg-linux-kernel-module-keenetic](https://github.com/hoaxisr/amneziawg-linux-kernel-module-keenetic) | Ядерный модуль AmneziaWG для Keenetic (MT7621: −50% CPU) | #402–#405, #1117 |
| [ShidlaSGC/keenetic-entware-awg-go](https://gitlab.com/ShidlaSGC/keenetic-entware-awg-go) | AWG-go для Keenetic/Entware (GitLab) | #300 |

## Темы форума Keenetic

| Тема | Source |
|---|---|
| OPKG TUN в режимах mixed и system (#26950) | #305 |
| Ядерный модуль AWG / awg-manager (#26510) | #402 |
| TrustTunnel на Keenetic (#27375) | #412 |
| Antiscan — выявление и блокировка сканирования (#21009) | #484 |
| Управление роутером по telnet/RCI (#112) | #551 |
| Приложение-переключатель политик (#28834) | #902 |

Форум: <https://forum.keenetic.ru> (в ссылках канала также
forum.keenetic.com/#…, 9 вхождений).
