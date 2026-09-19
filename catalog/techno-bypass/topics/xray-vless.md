# Xray / VLESS / REALITY и панели

Установка Xray на Keenetic, конфигурации VLESS+Reality, сопутствующие
панели и хроника блокировок Xray/VLESS в РФ.

## Установка и конфигурация на Keenetic

- **qp-io — гайд «sing-box / Xray install on Keenetic»**
  <https://qp-io.github.io/xray/sing-box-xray-install-server-keenetik> —
  Source: #16, #375 (там же добавление AWG 2.0 в режиме opkgtun).
- **Эталонная заготовка config.json** (VLESS + Reality, flow
  `xtls-rprx-vision-udp443`, fingerprint chrome, таймауты под роутер:
  handshake 2 / connIdle 30) — Source: #25; файлы-вложения `var_1.json`,
  `var_2.json` (#26, #27); оптимизированный конфиг под KN-1910 (MT7621,
  128 МБ) — #184–#187. **Research**: шаблоны не сверены с текущим Xray-core.
- **Оптимизационные советы** (sniffing off, резервный outbound) —
  Source: #186, #187.
- **Смена «общего пароля» на выданный провайдером** (правка config.json) —
  Source: #83, #101.
- **Удаление Xray с роутера** (opkg remove, чистка /opt/etc/xray) —
  Source: #399.
- **Гайды по sing-box в Entware** (инструкция от третьего лица, переработка
  под sb) — Source: #63, #72 (ipk по архитектурам), #173, #244, #291.

## Апстрим Xray-core

TB-04 (2026-09-19): Xray-core активен (ежедневно); Xray-install, RealiTLScanner
и chika0801/Xray-examples показывают низкую активность (последние push
2026-01, 2026-05, 2025-12 соответственно) — факт активности, не оценка.

- [XTLS/Xray-core, issue #5332](https://github.com/XTLS/Xray-core/issues/5332)
  — подобранные и проверенные настройки при проблемах VLESS — Source: #256.
- [XTLS/Xray-install](https://github.com/XTLS/Xray-install) — официальный
  установщик — Source: #148.
- [XTLS/RealiTLScanner](https://github.com/XTLS/RealiTLScanner) — сканер
  кандидатов для REALITY (SNI/сертификаты) — Source: #114.
- **xDNS и xICMP (FinalMask)** — новость о новых инструментах в ядре Xray —
  Source: #517, #518 (2026-03-01). **Research**: пересказ, не проверено по
  релизам.
- Примеры **VLESS-XHTTP-REALITY, steal_oneself** —
  [chika0801/Xray-examples](https://github.com/chika0801/Xray-examples) —
  Source: #336.

## Панели управления

| Панель | Контекст | Source |
|---|---|---|
| [alireza0/x-ui](https://github.com/alireza0/x-ui) | Панель Xray | #500 |
| [alireza0/s-ui](https://github.com/alireza0/s-ui) | Панель sing-box | #481 |
| 3X-UI | «Что-то навайбкодили — ТСПУ проще блокировать новые версии» (Research) | #933 |
| [remnawave/panel](https://github.com/remnawave/panel) + [migrate](https://github.com/remnawave/migrate) | Панель и миграция | #200, #467 |
| [AlexeyLCP/lucx-ui](https://github.com/AlexeyLCP/lucx-ui) | Панель | #1171 |
| [NiREvil/vless](https://github.com/NiREvil/vless) | Скрипты/конфиги vless | #828 |
| Форк xray-core от Jolymmerys (для Remnawave + mihomo-клиентов) | Source | #1137 |

## Хроника блокировок (Historical)

Сводка сообщений-новостей, датированных временем публикации:

- 2025-11-22 — «В России начались блокировки Xray» (Tech Talk) — #248;
  «РКН подбирается к VLESS» (Amnezia Новости) — #249.
- 2025-11-23 — «Блокировка VLESS(TLS 1.3): ограничивают трафик на TLS 1.3,
  а не сам протокол» (OverSecure) — #252.
- 2026-05-27 — перебои EU-серверов / изменения работы Xray Reality — #866.
- 2026-06-09 — «Блокировки VPN перешли на следующий уровень» (SecurityLab) —
  #1197 (2026-09-02, архивная ссылка).

Эти записи — **Historical**: они фиксируют картину на дату и не являются
текущей аналитикой. Технические разборы — см. [articles.md](articles.md)
и [dpi-zapret.md](dpi-zapret.md).
