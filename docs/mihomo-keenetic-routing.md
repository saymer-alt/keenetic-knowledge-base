# Mihomo на Keenetic: где он в архитектуре маршрутизации

**Статус:** Confirmed (архитектурная модель — по документации проекта
keenetic-auto-setup); отдельные наблюдения канала — Observed/Research
**Область применения:** Keenetic + Entware + Mihomo (Clash.Meta)
**Source of truth:** `saymer-alt/keenetic-auto-setup/ARCHITECTURE.md`
(основной текст статьи — конспективное изложение его модели)
**Provenance:** канал TechnoBypass —
[каталог: mihomo](../catalog/techno-bypass/topics/mihomo.md),
[каталог: magitrickle](../catalog/techno-bypass/topics/magitrickle.md)
(#15, #90, #798–#799, #1091 и др.)

## Что решаем

Самая частая ошибка темы — считать Mihomo «VPN на роутере». Эта статья
фиксирует: Mihomo — **отдельный движок маршрутизации**, встроенный в
Keenetic как один из слоёв, и у трафика в эту систему есть три разных
пути, которые нельзя смешивать.

## Модель слоёв

| Уровень | Кто | Отвечает за | Чем НЕ является |
|---|---|---|---|
| Платформа | KeeneticOS | интерфейсы, policy routing, firewall, DNS-прокси | не «коробка с Wi-Fi» |
| Решение | MagiTrickle | классифицирует домены по DNS-запросам | не VPN и не прокси |
| Движок выхода | Mihomo | принимает трафик, разруливает по своим правилам | не «тот самый VPN» |
| Выходы | AWG/WireGuard/VLESS-серверы/DIRECT | физические каналы | взаимозаменяемые детали |

Ключевое разделение ответственности: **кто направил трафик в Mihomo —
не тот, кто решает, куда он уйдёт после попадания**. Направляет
Keenetic/MagiTrickle; решает — правила Mihomo; выходит — выбранный
outbound.

## Три пути трафика

1. **Путь A (основной): DNS-классификация.** Клиент спрашивает DNS →
   MagiTrickle сопоставляет домен с группой → firewall-метка → policy
   routing Keenetic направляет трафик (в `mitun0`, `ProxyN` или напрямую).
2. **Путь B: прямой proxy-inbound.** Клиент сам подключается к mixed-порту
   Mihomo `:7890` (FoxyProxy и любые SOCKS/HTTP-клиенты). MagiTrickle
   здесь не участвует — выбор делает клиент + правила Mihomo.
3. **Путь C: TUN (`mitun0`).** Прозрачный IP-вход; решения внутри — по
   правилам Mihomo, а всё, что уходит несвязанным потоком, следует обычной
   таблице маршрутизации Keenetic (default gateway).

## ProxyN и mitun0 — два входа, два механизма

| | ProxyN (например Proxy0) | mitun0 |
|---|---|---|
| Что | прокси-интерфейс Keenetic (SOCKS5 → 127.0.0.1:7890) | TUN-устройство Mihomo (L3) |
| Создаёт | установщик через `ndmc` (идемпотентно) | сам Mihomo (имя — в его конфиге) |
| Сильная сторона | явная точка назначения для правил по клиенту/сегменту | прозрачный путь без клиентских настроек |

## Развилка «interface в MetaCubeX ≠ выбор WAN»

`interface-name` в Mihomo привязывает **исходящие сокеты самого Mihomo**
(соединения к прокси-серверам). Это НЕ переключение WAN для всего трафика:
поток, вошедший через `mitun0` и ушедший без прокси-outbound, следует
таблицам маршрутизации Keenetic. Per-path выбор WAN — задача policy
routing Keenetic. Подбор правильного `interface-name` упрощает
`mihomo-interface-check.sh` (Confirmed: поставляется в keenetic-auto-setup).

## Что подтверждено, а что нет

**Confirmed** (по ARCHITECTURE.md проекта, 2026-09-19):

- модель слоёв, три пути, таблица ProxyN/mitun0, правило
  «interface-name ≠ WAN», нумерация ProxyN (установщик не трогает чужой
  Proxy0 и берёт первый свободный), поведение MagiTrickle `link: [br0, br1]`
  (новый сегмент нужно добавить в конфигурацию).

**Observed (канал):**

- схема отказоустойчивости «Клиент РФ → VPS Москва (relay) → VPS
  зарубежный» на Mihomo (#798–#799) — авторская конфигурация, не часть
  проекта; параметры health-check (`interval/tolerance/idle_timeout`)
  подбирались эмпирически (#230).

**Research:**

- поведение `auto-detect-interface` на multi-WAN (ARCHITECTURE.md сам
  рекомендует проверять практически);
- производительность TUN-стеков (`stack: gvisor/system/mixed/mips`) на
  конкретном железе; `mips` — оптимизация под MIPS-роутеры (см.
  MetaCubeX/mipstack в [каталоге](../catalog/techno-bypass/VERIFIED_RESOURCES.md)).

## Источники и provenance

- Код (источник истины): `saymer-alt/keenetic-auto-setup` → ARCHITECTURE.md.
- Канал: серия #15–#34 (ручные бюллетени Proxy0/bypass_wa — исторические
  предшественники), #1091 (современная установка MagiTrickle+Mihomo),
  #978–#984 (MASQUE-эксперименты), #990/#1156 (генератор владельца).

## Связанные материалы

- [Методология облачных зависимостей камер/IoT](iot-cloud-routing-methodology.md) —
  как выяснить, какой трафик устройства направлять в Mihomo.
- [DNS Keenetic через Mihomo: штатный путь через ProxyN](keenetic-dns-via-mihomo.md) —
  куда идёт upstream DNS самого Keenetic и почему через ProxyN, а не `mitun0`.
- [Карта встраивания: L2/L3, TUN/TAP, bridge/route](network-layer-tunnel-map.md) —
  почему ProxyN и `mitun0` — разные уровни встраивания в ОС.
- [Стек прокси/туннель-протоколов](proxy-tunnel-protocol-stack.md) — слои
  протокола/транспорта/маскировки для чтения конфигов Mihomo.
- [Политика, сегмент, SSID и маршрут: не называйте всё WL](keenetic-policy-segment-ssid-naming.md)
- [docs/keenetic-entware-base.md](keenetic-entware-base.md)
- [docs/vpn-proxy-terminology.md](vpn-proxy-terminology.md)
- `NVR/WL.md` этого репозитория (raw-предыстория темы DIRECT vs proxy)
