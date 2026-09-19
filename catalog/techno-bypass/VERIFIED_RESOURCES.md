# VERIFIED RESOURCES — первый верификационный проход (TASK-TB-04)

Дата проверки: **2026-09-19**. Метод: GitHub/GitLab API (read-only, `gh`),
HTTP-проверка страниц. Скрипты третьих сторон не выполнялись, ничего не
устанавливалось, сетевые настройки не менялись. Выборка: ~65 самых ценных
ресурсов по сигналам частоты в канале, связи с Keenetic и проектами
владельца, фундаментального upstream-статуса и перекрёстных ссылок тем.

Статусы: Active / Maintained / Low activity / Archived / Dead / Moved /
Superseded / Unknown. «Активность» — дата последнего push (для репозиториев)
на момент проверки; это факт, не оценка качества.

## Главные находки прохода

1. **byewhitelists.ru — Dead (ECONNREFUSED)**: бесплатный гайд по обходу
   белых списков из #251 недоступен (connect refused на 443). Ссылка в
   [whitelist-mode.md](topics/whitelist-mode.md) помечена.
2. **LL33ch/dpi-rip → LL33ch/dpi-checker (Moved)**: репозиторий переименован;
   сайт dpi.rip резолвится (JS-only контент), код активен (2026-05-28).
3. **openlibrecommunity/twl — Archived**: большой research-репозиторий по
   белым спискам (#961) заархивирован (последний push 2026-08-28).
4. **MetaCubeX/mihomo — identity quirk**: канонический репозиторий прокси-ядра
   (34k звёзд, активен ежедневно, wiki.metacubex.one), но поле description
   сейчас показывает текст стороннего проекта (Honkai: Star Rail parser) —
   исторический артефакт нейминга, проект не переезжал.
5. **Новое upstream-открытие для тем владельца**: у MetaCubeX есть
   `mipstack` («mihomo IP stack (MIPS), pure-Go userspace» — источник
   `stack: mips` в Mihomo) и `amneziawg-go` (upstream AWG-реализации) —
   полезные якоря для mihomo.md/vpn-protocols.md.

## Репозитории GitHub (проверено 50)

| Репозиторий | Статус | Последний push | Примечание |
|---|---|---|---|
| bol-van/zapret | Active | 2026-09-18 | — |
| bol-van/zapret2 | Active | 2026-09-18 | — |
| Flowseal/zapret-discord-youtube | Active | 2026-08-30 | — |
| Waujito/youtubeUnblock | Active | 2026-08-30 | — |
| nfqws/nfqws2-keenetic | Active | 2026-09-17 | — |
| nfqws/nfqws-keenetic-web | Active | 2026-09-17 | — |
| Virenbar/ZapretControl | Active | 2026-08-26 | — |
| xtrime-ru/antizapret-vpn-docker | Active | 2026-09-08 | — |
| Ground-Zerro/Phobos | Active | 2026-08-11 | — |
| hyperion-cs/dpi-checkers | Active | 2026-09-15 | — |
| Runnin4ik/dpi-detector | Active | 2026-09-18 | — |
| vernette/censorcheck | Active | 2026-09-03 | — |
| MayersScott/rkn-block-checker | Active | 2026-09-12 | — |
| LL33ch/dpi-checker | Moved+Active | 2026-05-28 | бывш. dpi-rip; сайт dpi.rip жив (JS-only) |
| Viktor45/as-tspu | Active | 2026-09-19 | краудсорс-список AS под ТСПУ |
| pwnnex/ByeByeVPN | Active | 2026-09-11 | — |
| dimon27254/antiscan | Active | 2026-08-14 | — |
| MagiTrickle/MagiTrickle | Active | 2026-09-08 | канонический — GitLab; GitHub зеркало |
| LarinIvan/MagiTrickle_Mod | Low activity | 2026-01-21 | fork; исходный parent недоступен |
| hoaxisr/awg-manager | Active | 2026-09-18 | — |
| nikrays/keen_bypass_public | Low activity | 2026-04-05 | — |
| spatiumstas/web4static | Low activity | 2026-04-12 | — |
| MetaCubeX/mihomo | Active | 2026-09-19 | description показывает чужой текст (находка №4) |
| MetaCubeX/meta-rules-dat | Active | 2026-09-19 | fork; parent-строка API недоступна |
| Zephyruso/zashboard | Active | 2026-09-18 | — |
| XTLS/Xray-core | Active | 2026-09-19 | — |
| XTLS/Xray-install | Low activity | 2026-01-18 | — |
| XTLS/RealiTLScanner | Low activity | 2026-05-30 | — |
| alireza0/x-ui | Maintained | 2026-08-21 | fork; исходный vaxilu недоступен |
| alireza0/s-ui | Active | 2026-09-16 | — |
| remnawave/panel | Active | 2026-09-12 | — |
| chika0801/Xray-examples | Low activity | 2025-12-01 | — |
| telemt/telemt | Active | 2026-09-13 | — |
| telemt/tdlib-obf | Low activity | 2026-06-29 | fork; parent недоступен |
| alexbers/mtprotoproxy | Maintained | 2026-05-30 | — |
| telegramdesktop/tproxy-server | Active | 2026-09-10 | proof-of-concept от tdesktop |
| openlibrecommunity/twl | **Archived** | 2026-08-28 | research по белым спискам |
| hxehex/russia-mobile-internet-whitelist | Active | 2026-07-24 | — |
| gbwltg/ConfuseRKN | Low activity | 2026-03-03 | — |
| nebesniy/easy-vk-tunnel | Low activity | 2025-10-03 | — |
| kulikov0/whitelist-bypass | Active | 2026-09-18 | WebRTC-туннель |
| ViRb3/wgcf | Active | 2026-09-18 | — |
| distillium/warp-native | Low activity | 2026-05-31 | — |
| openwarpkit/warp-relay | Active | 2026-08-03 | — |
| wg-easy/wg-easy | Active | 2026-09-18 | — |
| w0rng/amnezia-wg-easy | Low activity | 2024-09-22 | fork wg-easy; parent недоступен; 2 года без push |
| amnezia-vpn/amneziawg-tools | Active | 2026-08-12 | fork; parent недоступен |
| amnezia-vpn/amnezia-client | Active | 2026-09-18 | — |
| MetaCubeX/mipstack | Active | 2026-09-19 | новый якорь: userspace IP-стек mihomo (MIPS) |
| MetaCubeX/amneziawg-go | Active | 2026-09-08 | upstream AWG-реализации |

## Сайты и GitLab (проверено 15)

| Ресурс | Статус | Примечание |
|---|---|---|
| magitrickle.dev/docs/welcome | Active | документация загружается |
| magitrickle.dev/docs/getting-started/keenetic/ | Unknown | резолвится, но контент не отдаётся фетчером (клиентский рендер/redirect) — проверить в браузере |
| bin.magitrickle.dev/packages/add_repo.sh | Active | endpoint отдаёт bootstrap-скрипт (тип содержимого подтверждён; не выполнялся) |
| cheburcheck.ru | Active | — |
| cheburcheck.ru/kb/whitelist | Active | методология белых списков + CSV; дата «01.01.1970» — плейсхолдер сайта |
| hyperion-cs.github.io/dpi-checkers/ru/tcp-16-20 | Active | — |
| qp-io.github.io/xray/keenetic-xray-sb-mihomo | Active | гайд xray/sb/mihomo на Keenetic |
| sw.ext.io/ent/installers | Active | 19 оффлайн-инсталляторов (aarch64/mips/mipsel; dropbear/openssh; nfqws2/vanilla) + README |
| iplist.opencck.org | Active | — |
| byewhitelists.ru | **Dead** | ECONNREFUSED — гайд из #251 недоступен |
| kiarant.github.io/editorMT | Active | редактор групп доменов MagiTrickle |
| wiresock.net (Secure Connect) | Active | v3.6.1.1 stable / 3.7.1.1 beta |
| dpi.rip | Active (JS-only) | контент рендерится клиентом; см. переименование репо |
| gitlab.com/magitrickle/magitrickle | Active | канонический репозиторий (GPLv3+, 18 релизов) |
| gitlab.com/ShidlaSGC/keenetic-entware-awg-go | Active | мануал AWG-Go для Keenetic |

Ранее установленное (TB-02B, 2026-09-19): gist-зеркало deploy.sh — Dead;
hoaxisr/amneziaawg-linux-kernel-module-keenetic — Dead (не резолвится);
amnezia-mihomo-gateway, link-generators — Active.

## Ограничения

- «Последний push» ≠ активная поддержка (могут быть только issue);
  «Low activity» — не приговор проекту.
- Ни один сторонний код не запускался; проверка — API/страницы.
- Следующий проход (TB-02C-уровень): следующие ~50 по частоте + живость
  habr/telegra.ph-статей из articles.md.
