# Карта инструментов диагностики DPI и блокировок

**Статус:** Research (карта инструментов; статусы — Confirmed на дату
проверки 2026-09-19 через TASK-TB-04)
**Область применения:** диагностика «у меня что-то не открывается» в
условиях ТСПУ/DPI; выбор правильного инструмента под вопрос
**Source of truth:** состояние проектов — GitHub API/страницы на
2026-09-19 ([VERIFIED_RESOURCES.md](../catalog/techno-bypass/VERIFIED_RESOURCES.md))
**Provenance:** канал TechnoBypass —
[каталог: diagnostics](../catalog/techno-bypass/topics/diagnostics.md);
сводные посты владельца #1022–#1028

## Что решаем

Вопрос «это у меня сломалось или у всех?» имеет разные ответы в
зависимости от слоя. Карта сопоставляет вопрос → инструмент.

## Вопрос → инструмент

| Вопрос | Инструмент | Слой | Статус (TB-04) |
|---|---|---|---|
| Домен вообще жив, или это блокировка? | [cheburcheck.ru](https://cheburcheck.ru) | домен/блок-листы | Active |
| Мой провайдер режет конкретный хостинг? | [hyperion-cs/dpi-checkers](https://hyperion-cs.github.io/dpi-checkers/ru/tcp-16-20/) (TCP 16–20) | DPI-обрывы по объёму | Active |
| Какие подсети доступны при белых списках? | hyperion-cs ipv4-whitelisted-subnets | whitelist-подсети | Active |
| Как ТСПУ видит мой сервер снаружи? | [pwnnex/ByeByeVPN](https://github.com/pwnnex/ByeByeVPN) (DNS, GeoIP×9, TCP/UDP-скан) | поверхность сервера | Active |
| Проблема сети или РКН? | [MayersScott/rkn-block-checker](https://github.com/MayersScott/rkn-block-checker) (DNS/TCP/TLS/HTTP по слоям) | послойный диагноз | Active |
| Какие AS уже под ТСПУ? | [Viktor45/as-tspu](https://github.com/Viktor45/as-tspu) (краудсорс) | ASN-уровень | Active |
| Детект VPN-протокола на сервере? | [Runnin4ik/dpi-detector](https://github.com/Runnin4ik/dpi-detector), [cherepavel/VPN-Detector] | TLS/протокол-фингерпринты | Active |
| Проверка доступности сайта из РФ-точек | [check-host.net](https://check-host.net) | распределённые пинги | Active (сервис) |
| Утечки DNS/IP/браузера при VPN | dnsleaktest, ipleak.net, browserleaks | клиентские утечки | Active (сервисы) |
| Корректность TLS-стека браузера | [badssl.com/dashboard](https://badssl.com/dashboard/) | сертификаты | Active (сервис) |
| Поддержка HTTP/3 у сайта | http3check.net | QUIC | Active (сервис) |
| Куда реально идёт запрос (v4/v6)? | IPvFoo (расширение) | браузер | Active |

## Методика (как пользоваться картой)

1. Сначала послойный чекер (rkn-block-checker / cheburcheck) — отделить
   «сломалось у меня» от «блокируется у всех».
2. Если блокировка — определить слой (DNS? TCP-обрыв? TLS?) и механику
   (объём 16–20 КБ → whitelist-режим, а не обычный DPI).
3. Для серверных сценариев — взглянуть на себя глазами цензора
   (ByeByeVPN/dpi-detector) ДО жалоб пользователей.

## Что подтверждено, а что нет

**Confirmed (2026-09-19):** все инструменты первой колонки существуют,
доступны, развиваются (детали — VERIFIED_RESOURCES.md; переименование
dpi-rip → dpi-checker учтено).

**Observed (канал):** практические сценарии применения — #87, #321, #663,
#809; ooni критикуется за неверную детекцию замедлений (#469).

**Research/ограничения:** результаты чекеров зависят от точки измерения
(регион/оператор); «зелёный» результат одного инструмента не доказывает
отсутствие блокировок в других сетях.

## Источники и provenance

- Канал: каталог-тема diagnostics; сборники владельца #1022–#1028
  (AI-извлечение «все ссылки про DPI/тесты» — исторический якорь).
- Проверка живости: TB-04 (2026-09-19).

## Связанные материалы

- [docs/whitelist-mode-architecture.md](whitelist-mode-architecture.md)
- [docs/zapret-ecosystem.md](zapret-ecosystem.md)
