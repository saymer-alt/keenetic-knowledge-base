# Диагностика: DPI-чекеры и онлайн-тесты

Инструменты проверки блокировок, утечек и проходимости. Часть ссылок
дублирует [dpi-zapret.md](dpi-zapret.md) (инструменты обхода).

## DPI/ТСПУ-чекеры

| Инструмент | Что делает | Source |
|---|---|---|
| [hyperion-cs/dpi-checkers](https://hyperion-cs.github.io/dpi-checkers/ru/tcp-16-20/) | Тест ТСПУ на блокировку популярных хостингов; ipv4-whitelisted-subnets; dwc-ветка на Python | #87, #241, #488, #491, #1024 |
| [Runnin4ik/dpi-detector](https://github.com/Runnin4ik/dpi-detector) | Анализ TLS, проверка сайтов/CDN/хостингов у РФ-провайдеров; Docker-образ, win10-сборка | #465, #601, #606, #1192 |
| [cheburcheck.ru](https://cheburcheck.ru/) | Чекер «чебурнета» + база белых списков | #321, #492, #1024 |
| [vernette/censorcheck](https://github.com/vernette/censorcheck) | Скрипт проверки цензуры | #663, #1022 |
| [MayersScott/rkn-block-checker](https://github.com/MayersScott/rkn-block-checker) | «Проблема сети или РКН» | #809, #1022 |
| [Viktor45/as-tspu](https://github.com/Viktor45/as-tspu) | Проверка по ASN/ТСПУ | #1002, #1024 |
| [LL33ch/dpi-rip](https://github.com/LL33ch/dpi-rip) | dpi.rip — проверка DPI | #881, #1028 |
| [Nintoryan/all-dpi-bypass-travel](https://github.com/Nintoryan/all-dpi-bypass-travel) | — | #1008, #1022 |
| [cherepavel/VPN-Detector](https://github.com/cherepavel/VPN-Detector) | Детект VPN | #722, #733 |
| [dimon27254/antiscan](https://github.com/dimon27254/antiscan) + тема форума #21009 | Выявление сканирования роутера | #449, #484, #1026 |
| [pwnnex/ByeByeVPN](https://github.com/pwnnex/ByeByeVPN) | «Взгляд на сервер глазами ТСПУ»: DNS, GeoIP из 9 источников, TCP/UDP-скан | #802 |
| TSPU Checker (Habr) | Статья-инструмент | #904 |
| [ward-sentry/DoT_n_DoH-Checker](https://github.com/ward-sentry/DoT_n_DoH-Checker) | Доступность DoT/DoH | #959 |
| [kauri-off/mcp_tunnel](https://github.com/kauri-off/mcp_tunnel) | — | #250, #1026 |
| [Viktor45/sub-filter](https://github.com/Viktor45/sub-filter) | Фильтрация подписок | #268, #1026 |
| ooni (explorer.ooni.org) | Измерения цензуры; «замедления не обнаруживает» (критика) | #469, #635 |

Важно: **#1022–#1028** — сам владелец уже прогонял архив через
AI-извлечение ссылок по теме «DPI, блокировки, проверки, диагностика» —
эти сообщения themselves являются мини-каталогами и хорошей точкой входа.

## Онлайн-диагностика сети

| Сервис | Назначение | Source |
|---|---|---|
| [check-host.net](https://check-host.net) | Много-точечная проверка | #1024+ |
| [dnscheck.tools](https://dnscheck.tools) | Проверка DNS/резолверов | #1024 |
| [dnsleaktest.com](https://dnsleaktest.com), [ipleak.net](https://ipleak.net), browserleaks.com | Утечки DNS/IP/браузера | #120, #1024 |
| [badssl.com/dashboard](https://badssl.com/dashboard/) | «Дырявость» браузера по сертификатам | #60, #489 |
| [http3check.net](https://http3check.net/) | Поддержка HTTP/3 | #197 |
| speedtest-альтернативы: fiber.google.com/speedtest, rtk.speedtestcustom.com | «Работающие спидтесты» | #490 |
| ipinfo.io / ifconfig.co | Внешний IP | #4, #450 |
| 2ip.io (обзор anycast, рост реестра РКН в 4,3 раза) | Просветительские статьи | #1212, #1213 |

## Расширения браузера

- **IPvFoo** — показывает, куда реально идёт запрос (v4/v6) — Source: #57;
  форк ipvfoobarbaz — #952.
- **Domain Inspector** — что не добавлено в правила — Source: #255.

## Гео-данные и списки

- iplist.opencck.org (Format: Text / Data type для списков) — Source: #56, #290.
- ASN-подписи asn.web2core.workers.dev / sw.ext.io (быстрый способ получить
  подсети AS) — Source: #967, #1001, #1129.
- [P3TERX/GeoLite.mmdb](https://github.com/P3TERX/GeoLite.mmdb) — #614.
