# Экосистема zapret/nfqws: карта проектов и концепций

**Статус:** Research (карта) + Observed (установка на VPS — авторский
опыт канала) 
**Область применения:** противодействие DPI на Linux-хостах и Keenetic
**Source of truth:** репозитории проектов (статусы проверены 2026-09-19,
TASK-TB-04)
**Provenance:** канал TechnoBypass —
[каталог: dpi-zapret](../catalog/techno-bypass/topics/dpi-zapret.md)
(#274, #331–#333, #350, #354–#366, #605, #1117)

## Что решаем

Вокруг zapret сложился лес форков, сборок и GUI. Карта фиксирует, что
чем является, чтобы не путать ядро, сборку стратегий и платформенный
порт.

## Карта проектов

| Проект | Чем является | Статус (TB-04) |
|---|---|---|
| [bol-van/zapret](https://github.com/bol-van/zapret) | ядро anti-DPI (nfqws/tpws, стратегии, hostlist) | Active |
| [bol-van/zapret2](https://github.com/bol-van/zapret2) | следующая версия ядра | Active |
| [Flowseal/zapret-discord-youtube](https://github.com/Flowseal/zapret-discord-youtube) | сборка готовых стратегий (Discord/YT) поверх ядра | Active |
| [nfqws/nfqws2-keenetic](https://github.com/nfqws/nfqws2-keenetic) + web | порт на Keenetic + веб-морда (в оффлайн-инсталляторах sw.ext.io) | Active |
| [Virenbar/ZapretControl](https://github.com/Virenbar/ZapretControl) | GUI | Active |
| [Waujito/youtubeUnblock](https://github.com/Waujito/youtubeUnblock) | отдельный подход (SNI-байпас, не zapret) | Active |

**Концепция стратегии**: набор параметров фейков/фрагментации для
конкретного провайдера. **ALT11** — стратегия из десктопной сборки
Flowseal 1.9.2 (файлы nfqws.conf/ipset.list/user.list), адаптировалась
энтузиастами под конкретных операторов (#332, #333).

## Установка на VPS (Observed)

Авторская серия канала (#354–#366, январь 2026) — реальная установка на
Debian:

- рабочий путь — `install_easy.sh` (или `install_bin.sh`); выбор
  nftables/iptables, flow-offloading, режима фильтрации (autohostlist);
- грабли: curl-редирект GitHub на HTML (ставить через git), отсутствие
  `libnetfilter-queue-dev` при сборке;
- перенос стратегии с десктопа: подобрать на zapret-discord-youtube →
  перенести файлы в nfqws на роутере (#350).

**Не инструкция**: рецепт воспроизводится по ссылкам выше; здесь
фиксируются только подтверждённые автором этапы.

## Что подтверждено, а что нет

**Confirmed (TB-04):** все шесть проектов существуют и активны
(zapret/zapret2 обновлялись в день проверки).

**Observed:** установка на VPS (#354–#366 — поэтапный лог автора);
эффективность ALT11 на провайдере Airnet СПб (#333, со слов автора
форварда).

**Research:** эффективность конкретных стратегий в конкретных
регионах/сетях меняется; подбор — эмпирический (#350), универсальной
стратегии нет.

## Источники и provenance

- Канал: каталог-тема dpi-zapret; каналы «Запрет ГУИ» (#605).
- Статусы: VERIFIED_RESOURCES.md (2026-09-19).

## Связанные материалы

- [docs/dpi-diagnostics-map.md](dpi-diagnostics-map.md)
- [docs/keenetic-entware-base.md](keenetic-entware-base.md)
