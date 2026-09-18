# Mihomo (Clash.Meta)

Установка Mihomo на Keenetic, панели, схемы отказоустойчивости и MASQUE.
Часть установочных цепочек канала пересекается с
[magitrickle.md](magitrickle.md) и [owner-projects.md](owner-projects.md).

## Установка на Keenetic

- **qp-io — установка Mihomo/Xray/sing-box на Keenetic**
  <https://qp-io.github.io/xray/keenetic-xray-sb-mihomo> — Source: #1091
  (перепост Internet Helper, шаги: компонент «Клиент прокси» → установка →
  конфиг `/opt/etc/mihomo/config.yaml` → `S99mihomo start/status`).
- Пример конфига с `clash_api`/`external_controller`/`cache_file`
  (experimental) — Source: #90.
- **Удаление Mihomo** (opkg remove + зачистка процесса и файлов) —
  Source: #570.
- Пакет в репозиториях sw.ext.io (см. [keenetic-entware.md](keenetic-entware.md),
  #1117).

## Панели и дашборды

| Ресурс | Контекст | Source |
|---|---|---|
| [spatiumstas/web4static](https://github.com/spatiumstas/web4static) | Панель редактирования конфига Mihomo (порт 99) | #1091 |
| [Zephyruso/zashboard](https://github.com/Zephyruso/zashboard) | Дашборд | #263 |
| MetaCubeXD (metacubex) | Дашборд (в тестах канала) | #90 |
| [MetaCubeX/meta-rules-dat](https://github.com/MetaCubeX/meta-rules-dat) | geosite-списки (пример: google-gemini.json) | #54 |
| [123jjck/mihomo-configurator](https://123jjck.github.io/mihomo-configurator/) | Онлайн-генератор конфигов Mihomo (скорее под OpenWrt) | #655 |

## Отказоустойчивость и маршрутизация

- **Схема «Клиент (РФ) → VPS Москва → VPS заграница»** на Mihomo: relay через
  московский VPS, балансировка, поведение при падении — Source: #798, #799
  (2026-05-04). **Research**: схема не проверялась на живой системе.
- `interval/tolerance/idle_timeout/interrupt_exist_connections` — подбор
  параметров health-check — Source: #230.
- **Mihomo Interface Checker** (Keenetic + Entware) — мини-утилита диагностики
  нескольких провайдеров/интерфейсов — Source: #1127 (2026-08-06).
- Тонкая маршрутизация по VLESS/Trojan-подписке со своей балансировкой
  (Habr, OpenWrt/Keenetic) — см. [articles.md](articles.md) (#1185).

## MASQUE в Mihomo (эксперименты владельца)

Серия сообщений о заведении MASQUE (HTTP/3 CONNECT-UDP туннель) в Mihomo:

- Финальный **универсальный шаблон `masque://`-ссылки** (SNI, URL-encoded
  base64 ключи, ip, udp, remote-dns-resolve) — Source: #978–#981
  (2026-06-23). Шаблон содержит плейсхолдеры, не реальные ключи.
- Обсуждение реакции генераторов и клиентов на MASQUE — #978, #984.
- Итог этой работы — онлайн-генератор
  [`saymer-alt/link-generators`](owner-projects.md) (#990); позже —
  эксперимент с поддержкой файлов
  [vernette/warpscout](https://github.com/vernette/warpscout) (#1156).

## Ручное обновление (Historical/Superseded)

- Вложение «Mihomo Manual Update Arm Keenetic Entware» — Source: #815
  (2026-05-11): ручное обновление бинарника на ARM/ARM64 с учётом отсутствия
  `file`, разных путей установки, backup.
- **Superseded**: автоматизированный путь обновления теперь —
  `update-mihomo.sh` из [`saymer-alt/keenetic-auto-setup`](owner-projects.md)
  (config test, авто-rollback, защита от даунгрейда). Ручная инструкция
  сохраняет ценность как описание краевых случаев.

## Клиенты

- Hiddify / Happ / Karing / Nekoray / sing-box GUI — обзор-сравнение —
  Source: #120, #293. Подробнее по клиентам — [vpn-protocols.md](vpn-protocols.md).
- [KaringX/karing](https://github.com/KaringX/karing) — кросс-платформенный
  клиент — Source: #105.
