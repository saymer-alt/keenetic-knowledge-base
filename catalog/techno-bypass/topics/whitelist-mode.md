# Режим белых списков («шатдауны»)

Работа интернета, когда провайдер пропускает только разрешённые ресурсы:
гайды, чекеры, подписки, подсети, MTProxy. Крупнейшая практическая тема
канала наряду с APN.

## Гайды

- **byewhitelists.ru — бесплатный гайд по обходу шатдаунов** —
  Source: #251 (форвард «Обход белых списков», 2025-11-23).
  **Dead (проверено 2026-09-19, TB-04)**: соединение отвергается
  (ECONNREFUSED) — гайд временно/полностью недоступен; смотреть web.archive.
  См. [VERIFIED_RESOURCES.md](../VERIFIED_RESOURCES.md).
- **Обход белых списков на мобильном интернете** (telegra.ph) и
  продолжение (teletype.in/@derryt) — Source: #201.
- Гайд на вылавливание IP TimeWeb (все операторы, PDF) — Source: #1219
  (форвард WhiteList-канала; приватные ссылки опущены).

## Чекеры режима

- **cheburcheck.ru** — «чекер чебурнета» + список доменов белых списков
  (`/kb/whitelist`) — Source: #321, #492, #1024.
- **hyperion-cs: ipv4-whitelisted-subnets** — какие подсети доступны —
  Source: #491.

## Подписки и списки конфигов

Подписки — изменчивый и непроверяемый материал: статус **Research**,
актуальность на дату публикации. Публичные подписочные списки-агрегаторы
канала: #669, #795, #837, #844 (EtoNeYa + gitverse-наборы, 30–45 ссылок).

| Источник | Контекст | Source |
|---|---|---|
| EtoNeYa (github pages) | Подписки «ЭтоНеЯ» | #669, #844 |
| [AvenCores/goida-vpn-configs](https://github.com/AvenCores/goida-vpn-configs) | Зеркала конфигов | #240 |
| [ksenkovsolo/HardVPN-bypass-WhiteLists-](https://github.com/ksenkovsolo/HardVPN-bypass-WhiteLists-) | WHITELIST-ALL.txt | #631 |
| [RKPchannel/RKP_bypass_configs](https://github.com/RKPchannel/RKP_bypass_configs) | sources.txt | #577 |
| [hxehex/russia-mobile-internet-whitelist](https://github.com/hxehex/russia-mobile-internet-whitelist) | whitelist.txt | #273 |
| [zieng2/wl](https://github.com/zieng2/wl) | vless_lite.txt | #283 |
| [mermeroo/V2RAY-CLASH-BASE64-Subscription.Links](https://github.com/mermeroo/V2RAY-CLASH-BASE64-Subscription.Links) | База ссылок подписок | #796 |
| [gbwltg/ConfuseRKN](https://github.com/gbwltg/ConfuseRKN) | Скрипт своей подписки (GoodbyeWL-экосистема) | #535 |
| GoodbyeWL | Подписки/активация через Happ/Karing | #293 |
| [openlibrecommunity/twl](https://github.com/openlibrecommunity/twl) | Верифицированный список (verified.txt) | #961 |
|      | **Archived (TB-04, 2026-09-19)** — репозиторий заархивирован; данные остаются доступными | — |
| remnacracker (Ponywka) | Конвертер подписок с HWID для клиентов без HWID + self-host на CF Workers | #1204, #1205 |
| Утёкшая подписка DUREV | **Не воспроизводим**: доступ к платной подписке получен утечкой | #1214 |

Конкретные `vless://`-конфиги и webtunnel-мостики из сообщений канала
(#212–#216, #632 и др.) в каталог **не переносятся** — одноразовые
учётные данные; provenance — по id сообщений.

## Подсети и доменные списки (для маршрутизации)

Канал систематически собирал подсети для ipset/правил:

| Что | Source |
|---|---|
| Подсети Telegram (91.108.x, 149.154.x, 5.28.195.0/24, 95.161.64.0/20) | #109, #110, #112, #192, #422, #937, #938 |
| Cloudflare | #140, #229 |
| Google/GCP | #191 |
| Meta/Facebook (WhatsApp) | #396, #447 |
| YouTube (домены) | #342, #367 |
| Instagram | #224 |
| Gemini/AI Google | #344, #345, #1144 |
| ChatGPT/OpenAI | #71, #139 |
| MAX/VK/OK/Mail + oneme | #221, #540, #541, #630, #728 |
| Rutube/Яндекс (реклама и слежка) | #338 |
| Реклама/телеметрия (общий список) | #1149, #1164 |
| Маршрутизация VK/Mail через Bridge2 на Keenetic (`ip route … 127.0.0.1 Bridge2`) | #543, #544 |
| [v2fly/domain-list-community](https://github.com/v2fly/domain-list-community) (data/telegram) | #55, #416 |
| [tread-lightly/CyberOK_Skipa_ips](https://github.com/tread-lightly/CyberOK_Skipa_ips), [C24Be/AS_Network_List](https://github.com/C24Be/AS_Network_List), [shadow-netlab/traffic-guard-lists](https://github.com/shadow-netlab/traffic-guard-lists), [dotX12/traffic-guard](https://github.com/dotX12/traffic-guard) | #666, #741, #830, #560, #561, #461 |
| iplist.opencck.org | #56, #290 |

## MTProxy-экосистема для Telegram

- [alexbers/mtprotoproxy](https://github.com/alexbers/mtprotoproxy) —
  Source: #693; [Liafanx/MTproxy-reanimation](https://github.com/Liafanx/MTproxy-reanimation) —
  #991; [MaksimTMB/mtg-adminpanel](https://github.com/MaksimTMB/mtg-adminpanel) —
  #607; [yzewe/mtproto-checker](https://github.com/yzewe/mtproto-checker) —
  #1195.
- **telemt** (сервер MTProxy + обфускация tdlib):
  [telemt/telemt](https://github.com/telemt/telemt), [tdlib-obf](https://github.com/telemt/tdlib-obf),
  [An0nX/telemt-docker](https://github.com/An0nX/telemt-docker),
  [Dimasssss/free_telemt_servers](https://github.com/Dimasssss/free_telemt_servers),
  [vsibilev007/telemt-bot](https://github.com/vsibilev007/telemt-bot),
  фронтинг-сплиттинг-докуемнты (#637, #643), API (#547) —
  Source: #432, #525, #547, #637, #643, #812, #882.
- **MTProxy банится по JA3-хешу TLS ClientHello** — Source: #882
  (форвард Telemt; задокументированное наблюдение автора telemt).
- Официальный [telegramdesktop/tproxy-server](https://github.com/telegramdesktop/tproxy-server) —
  Source: #1162; [w2ppx/Telegram-XRay](https://github.com/w2ppx/Telegram-XRay) —
  #686; [kort0881/telegram-proxy-collector](https://github.com/kort0881/telegram-proxy-collector) —
  #964; [RTHeLL/tg-web-proxy](https://github.com/RTHeLL/tg-web-proxy) — #1163.
- Семейство **tg-ws-proxy** (Zapret для Telegram Desktop, SOCKS5+WS):
  [Flowseal/tg-ws-proxy](https://github.com/Flowseal/tg-ws-proxy) (#546,
  #615), Android-порты [LemoLev](https://github.com/LemoLev/tg-ws-proxy-ANDROID)
  (#613), [amurcanov](https://github.com/amurcanov/tg-ws-proxy-android) (#972),
  [noteaya](https://github.com/noteaya/tg-ws-proxy) (#611),
  [therufe/linux](https://github.com/therufe/tg-ws-proxy-linux) (#612),
  [valnesfjord/rs](https://github.com/valnesfjord/tg-ws-proxy-rs) (#1216),
  [romanvht/MTGAndroid](https://github.com/romanvht/MTGAndroid) (#623).
  Сводный пост — #617.

Готовые tg://proxy-ссылки с секретами из канала (#219, #232, #233, #419,
#444, #453, #459, #595–#599 и др.) в каталог не переносятся — содержат
секреты прокси; provenance — по id сообщений.

## Связь вне интернета

- **Delta Chat** — работает при белых списках через почту mail.ru/Яндекс —
  Source: #347, #587 (гайд LowiK).
- Reticulum/MeshChat, Meshtastic — см. [vpn-protocols.md](vpn-protocols.md).
- [gitlab.com/shadow_contributor/ntptun](https://gitlab.com/shadow_contributor/ntptun) —
  туннель поверх NTP — Source: #1110, #1141.
