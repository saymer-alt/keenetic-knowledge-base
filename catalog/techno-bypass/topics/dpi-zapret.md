# DPI / ТСПУ: zapret, nfqws и стратегии обхода

Семейство инструментов активного противодействия DPI и новости об эволюции
блокировок. Новости-разборы — в [articles.md](articles.md);
чекеры/диагностика — в [diagnostics.md](diagnostics.md).

## zapret (bol-van)

- [bol-van/zapret](https://github.com/bol-van/zapret) — Source: #354, #1022
  и др.; [zapret2](https://github.com/bol-van/zapret2) — #257.
- **Полный лог установки zapret на VPS** (Debian, install_easy.sh, выбор
  nftables/flow-offloading/autohostlist; грабли с libnetfilter-queue-dev,
  установка через git вместо curl-redirect) — Source: #354–#366.
  **Observed** (реальная установка автором канала на Saymer2).
- **Гайд «починка ТГ медиа и звонков с ПК»** (zapret discussion #1668 +
  правки для vless) — Source: #274 (форвард YEP).

## Стратегии (ALT11 и производные)

- **Стратегия ALT11 из zapret-discord-youtube 1.9.2** (файлы nfqws.conf,
  ipset.list, user.list; провайдер Airnet СПб — доступ к игровым серверам) —
  Source: #333 (форвард, вложение `nfqws(ZapALT11).zip`), #323, #332
  (адаптация под Билайн ЮФО).
- [Flowseal/zapret-discord-youtube](https://github.com/Flowseal/zapret-discord-youtube) —
  Source: #331, #350 (план подбора стратегий: отключить nfqws на роутере →
  подобрать на десктопе → перенести).

## zapret-экосистема

| Проект | Контекст | Source |
|---|---|---|
| [Virenbar/ZapretControl](https://github.com/Virenbar/ZapretControl) | GUI для zapret | #736 |
| [CherretGit/zaprett-app](https://github.com/CherretGit/zaprett-app) | Приложение | #759 |
| [StressOzz/Zapret-Manager](https://github.com/StressOzz/Zapret-Manager) | Менеджер | #1035 |
| [youtubediscord/zapret](https://github.com/youtubediscord/zapret) | Ветка/форк | #750 |
| Каналы «Запрет ГУИ» (стабильный/dev) | Новости zapret-сборок | #605 |
| [nfqws/nfqws2-keenetic](https://github.com/nfqws/nfqws2-keenetic) + [nfqws-keenetic-web](https://github.com/nfqws/nfqws-keenetic-web) | nfqws2 для Keenetic + веб-морда (в оффлайн-инсталляторах sw.ext.io) | #1117 |
| [spatiumstas/tg-ws-proxy-go](https://github.com/spatiumstas/tg-ws-proxy-go) | Go-прокси для Telegram (в инсталляторах sw.ext.io) | #1117 |

## Прочие DPI-инструменты

| Проект | Контекст | Source |
|---|---|---|
| [Waujito/youtubeUnblock](https://github.com/Waujito/youtubeUnblock) | «Стоит у меня на роутере» (Observed автором) | #59 |
| [xtrime-ru/antizapret-vpn-docker](https://github.com/xtrime-ru/antizapret-vpn-docker) | AntiZapret VPN в Docker | #654 |
| [GubernievS/AntiZapret-VPN](https://github.com/GubernievS/AntiZapret-VPN) | AntiZapret | #476 |
| [Ground-Zerro/Phobos](https://github.com/Ground-Zerro/Phobos) | Клиент обхода | #337, #477 |
| [stopcenz/fakesni](https://github.com/stopcenz/fakesni) | Подмена SNI | #275 |
| [EndPositive/slipstream](https://github.com/EndPositive/slipstream) | — | #188 |

## Аналитика блокировок (Research/Historical)

- **Наблюдения hyperion-cs / dpi-ch** о технической природе блокировок
  (Сибирь, июнь 2026) — Source: #932; продолжение — #947 (блокируется не
  Chrome вообще, а конкретные версии), #953, #974 («от серых списков по ASN
  приходят к белым спискам на проводе»). **Research**: первоисточник —
  publish.obsidian.md-заметки dpi-ch.
- Тайминговый анализ ТСПУ сессий (Typical Sysadmin) — Source: #1007.
- `packageNameRegex` в sing-box — «борьба с детектом VPN» (ntc.party) —
  Source: #743.
- 3X-UI и новые блокировки — Source: #933.
- TSPU Checker (Habr) — #904; разборы DPI-фильтрации — #819, #821.
