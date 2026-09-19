# Эволюция AmneziaAWG → Mihomo gateway: что осталось от старого VPS-кластера

**Статус:** Historical + Confirmed comparison  
**Область применения:** история и provenance решения AmneziaAWG (Docker) → Mihomo TUN → WARP  
**Проверено:** 2026-09-19  
**Текущий source of truth:** [saymer-alt/amnezia-mihomo-gateway](https://github.com/saymer-alt/amnezia-mihomo-gateway)

## Зачем этот документ

В корне knowledge base остался старый кластер:

- `amnezia.md`
- `awg.md`
- `check.md`
- `install.sh`
- `uninstall.sh`

Это не пять независимых решений. Они фиксируют эволюцию одного проекта, который позже
стал отдельным репозиторием `saymer-alt/amnezia-mihomo-gateway`.

**Использовать корневые файлы этого KB как актуальную инструкцию не следует.**
Текущее поведение определяется кодом активного проекта, прежде всего его `install.sh`.

## Что из старого решения сохранилось

Базовая архитектура пережила перенос почти без изменений:

```text
AWG client
    ↓
AmneziaAWG in Docker
    ↓
source-based policy rule
    ↓
routing table 100
    ↓
tun-mihomo
    ↓
Mihomo / WARP
    ↓
Internet
```

Сохранились ключевые инженерные решения:

- `rp_filter=0` для асимметричного Docker → TUN пути;
- отдельная routing table `100`, без переноса server traffic в TUN;
- правило `from <docker-subnet> lookup 100`;
- `fwmark 0x88` для ответного WireGuard-трафика через `main`;
- NAT/MASQUERADE на TUN;
- FORWARD rules для Docker-сети;
- watchdog через systemd timer;
- отсутствие direct fallback при исчезновении TUN как fail-secure модель.

Эти идеи больше не нужно восстанавливать из старых chat/AI-файлов: они уже явно
зафиксированы в активном проекте и его `AGENTS.md`.

## Сопоставление файлов

| Старый файл KB | Что это было | Текущее состояние |
|---|---|---|
| `amnezia.md` | ручная инструкция с параметрами конкретного сервера | **Historical / superseded** — архитектура сохранена, ручной рецепт заменён installer'ом |
| `awg.md` | более ранняя «финальная» версия того же ручного рецепта | **Historical / superseded** |
| `check.md` | отдельная идея watchdog/self-healing | **Promoted** — watchdog уже встроен в активный installer |
| `install.sh` | ранний автоматизированный installer | **Superseded** — текущий installer существенно расширен |
| `uninstall.sh` | cleanup companion | **Duplicate snapshot** — на 2026-09-19 blob совпадает с активным проектом, но rollback неполный |

## Что изменилось в текущем installer

По сравнению с корневым `install.sh` knowledge base текущий
`amnezia-mihomo-gateway/install.sh` дополнительно:

- использует именованную таблицу `100 mihomo`;
- добавляет маршрут fake-IP range через TUN;
- ждёт появления `tun-mihomo` до 30 секунд;
- увеличивает `txqueuelen` TUN до 5000;
- настраивает `TCPMSS --clamp-mss-to-pmtu`;
- применяет `mtu: 1420` и `gso: true`;
- при необходимости включает BBR/fq;
- умеет перезапускать Mihomo как systemd service **или** Docker container;
- патчит текущий `config.yaml` Mihomo;
- управляет DNS/systemd-resolved и, при определённых условиях, Docker DNS;
- создаёт backup Mihomo config перед patch;
- использует текущие диапазоны:
  - `fake-ip-range: 198.18.0.0/16`;
  - `inet4-address: 10.255.255.1/30`.

Поэтому значения из старых заметок:

- `inet4-address: 198.18.0.1/30`;
- `fake-ip-range: 240.0.0.1/4`;

следует считать историческими для этого проекта.

## Почему старый systemd-рецепт тоже нельзя копировать буквально

В старом `amnezia.md` service жёстко использовал:

```ini
Requires=mihomo.service
After=... mihomo.service
```

Текущий проект специально не делает Mihomo обязательной systemd-зависимостью,
потому что поддерживает и Docker-вариант Mihomo. Installer/watchdog сам определяет,
как его перезапустить.

Аналогично старый `check.md` предлагал отдельно создавать override
`Restart=always` для `mihomo.service`; текущий installer этого не делает и не должен
считаться источником политики restart для чужого сервиса.

## Важный rollback caveat

`uninstall.sh` удаляет routing rules, systemd units, generated scripts и sysctl-файл,
но **не является полным возвратом сервера к исходному состоянию**.

По текущему коду installer/uninstaller после удаления могут остаться:

- изменённый live sysctl state до следующей явной перенастройки/reboot;
- отключённый `systemd-resolved`;
- переписанный `/etc/resolv.conf`, включая immutable attribute;
- запись `100 mihomo` в `/etc/iproute2/rt_tables`;
- созданный installer'ом `/etc/docker/daemon.json`, если его не было ранее;
- изменения в найденном `config.yaml` Mihomo (backup создаётся, но uninstall его автоматически не восстанавливает).

Это не повод автоматически менять cleanup-код: поведение активного проекта должно
меняться отдельно и с тестом на VPS. Но документация не должна называть такой uninstall
«полным восстановлением».

## Что уникального осталось в старом сырье

Практически все важные технические причины уже мигрировали в активный проект:

- зачем нужен `rp_filter=0`;
- зачем маркировать WG replies;
- почему нельзя включать Mihomo `auto-route`;
- почему используется отдельная table 100;
- почему watchdog должен восстанавливать правила;
- почему отсутствие TUN должно давать fail-secure, а не direct fallback.

Ценность старых файлов теперь в основном **историческая**: они показывают, как решение
эволюционировало от ручных команд к installer'у.

## Что делать с файлами в корне KB

Пока их не удаляем: они остаются provenance.

Но их статус после этого аудита:

- `amnezia.md` → Historical / superseded source;
- `awg.md` → Historical / superseded source;
- `check.md` → Historical, concept promoted;
- `install.sh` → Historical project artifact, **не запускать из KB**;
- `uninstall.sh` → Historical duplicate snapshot, **не использовать как canonical copy**.

При будущей реорганизации весь кластер можно переместить в `archive/historical/`
с одной ссылкой на этот документ и на активный репозиторий.

## Связанные материалы

- [PROMOTION_BACKLOG.md](../PROMOTION_BACKLOG.md)
- [INVENTORY.md](../INVENTORY.md)
- [amnezia-mihomo-gateway](https://github.com/saymer-alt/amnezia-mihomo-gateway)
