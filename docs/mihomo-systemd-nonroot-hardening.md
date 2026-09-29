# Mihomo под systemd без полного root: least-privilege hardening

**Статус:** Research / частично Confirmed  
**Область применения:** Linux VPS, Mihomo как systemd-service; особенно TUN/TProxy-сценарии  
**Проверено на:** официальная документация Mihomo и systemd-модель; live-миграция конкретного VPS пока не выполнена  
**Последняя проверка:** 2026-09-29  
**Source of truth:** актуальный unit конкретного VPS + документация Mihomo/systemd

## Что решаем

Если systemd-unit Mihomo не задаёт `User=`, процесс обычно стартует с root-привилегиями. Для сетевого прокси это увеличивает последствия возможной уязвимости. Идея hardening — запустить Mihomo от отдельного системного пользователя и оставить только реально необходимые Linux capabilities.

Это **не готовая команда для слепого применения**. Нужный capability-set зависит от режима Mihomo, портов, TUN/TProxy, auto-route/auto-redirect, файлов и каталогов, к которым процесс обращается.

## Что подтверждено

Официальный пример systemd от Mihomo запускает daemon с `CapabilityBoundingSet` и `AmbientCapabilities`. В текущем upstream-примере набор заметно шире двух capabilities и включает, среди прочего, `CAP_NET_ADMIN`, `CAP_NET_RAW` и `CAP_NET_BIND_SERVICE`.

Документация TUN подтверждает, что Mihomo может сам создавать маршруты и, в Linux, при `auto-redirect` работать с iptables/nftables. Следовательно, сетевые capabilities действительно являются частью задачи least privilege.

Ссылки:

- https://wiki.metacubex.one/en/startup/service/
- https://wiki.metacubex.one/en/config/inbound/tun/

## Что предложил Gemini

В исходном research была предложена миграция:

- отдельный `mihomo` system user без login shell;
- `User=mihomo` / `Group=mihomo`;
- только `CAP_NET_ADMIN CAP_NET_BIND_SERVICE`;
- `ProtectSystem=full`;
- `ProtectHome=true`;
- передача `/etc/mihomo` пользователю Mihomo.

Направление разумное, но **точный рецепт пока Research**.

Raw provenance: [../archive/raw/gemini-mihomo-systemd-hardening-2026-09-29.md](../archive/raw/gemini-mihomo-systemd-hardening-2026-09-29.md).

## Важные поправки к исходной рекомендации

### Не считать два capability универсально достаточными

`CAP_NET_ADMIN` логично требуется для сетевых административных операций. `CAP_NET_BIND_SERVICE` нужен только если процесс действительно bind'ится к портам ниже 1024.

Однако upstream systemd-пример Mihomo дополнительно выдаёт `CAP_NET_RAW` и другие права. Пока конкретный workload не протестирован, нельзя утверждать, что:

```ini
AmbientCapabilities=CAP_NET_ADMIN CAP_NET_BIND_SERVICE
CapabilityBoundingSet=CAP_NET_ADMIN CAP_NET_BIND_SERVICE
```

работает для всех TUN/TProxy-конфигураций.

Правильный подход: начать с обоснованного набора, выполнить функциональные тесты и уменьшать privileges только при доказанном сохранении функций.

### Не делать `chown -R /etc/mihomo` автоматически

Конфигурация может содержать секреты. Полная передача каталога daemon-пользователю означает, что скомпрометированный Mihomo сможет изменять собственную конфигурацию.

Предпочтительнее разделять:

- root-owned конфигурацию, которую Mihomo только читает;
- writable runtime/state/cache, если они действительно нужны;
- права на отдельные файлы и каталоги по фактической необходимости.

Точная раскладка зависит от того, что лежит в `-d /etc/mihomo` и какие файлы текущая конфигурация создаёт или обновляет.

### `ProtectSystem=full` требует проверки writable paths

Hardening systemd полезен только если он совместим с реальными файловыми операциями процесса. Перед включением `ProtectSystem=full` нужно установить, куда Mihomo пишет:

- cache/state;
- GeoIP/GeoSite/MMDB;
- runtime-файлы;
- обновляемые rule providers;
- логи, если они файловые.

Не следует одновременно сделать путь read-only через systemd и ожидать, что daemon продолжит обновлять данные в нём.

## Безопасный план эксперимента

### 1. Снять baseline

До изменения unit сохранить:

```sh
systemctl cat mihomo
systemctl show mihomo -p User -p Group -p AmbientCapabilities -p CapabilityBoundingSet
ps -eo user,group,pid,comm,args | grep -E 'mihomo|clash' | grep -v grep
ss -lntup
ip -details link show
ip rule show
ip route show table all
```

Также сохранить копию текущего unit и зафиксировать рабочую проверку через прокси/TUN.

### 2. Инвентаризировать файловые зависимости

Проверить владельцев и права без массового `chown`:

```sh
namei -l /usr/local/bin/mihomo
namei -l /etc/mihomo
find /etc/mihomo -maxdepth 2 -printf '%M %u:%g %p\n'
```

Отдельно определить, какие файлы Mihomo реально должен менять.

### 3. Создать service account

Пример для системы с `useradd`:

```sh
useradd --system --no-create-home --shell /usr/sbin/nologin mihomo
```

Перед выполнением убедиться, что пользователь ещё не существует и что выбранный shell присутствует в системе.

### 4. Менять unit поэтапно

Не копировать capability-set из этой статьи как универсальный.

Сначала определить фактические требования конкретной конфигурации. После каждой ступени:

```sh
systemd-analyze verify /etc/systemd/system/mihomo.service
systemctl daemon-reload
systemctl restart mihomo
systemctl --no-pager --full status mihomo
journalctl -u mihomo -b --no-pager -n 200
```

### 5. Проверить не только процесс, но и dataplane

После рестарта проверить:

- процесс действительно работает не от root;
- TUN существует;
- policy routing/routes сохранились;
- TProxy/redirect работает, если используется;
- DNS-путь работает;
- proxy inbounds доступны только там, где должны;
- внешний IP и leak-проверки соответствуют baseline;
- rule providers/geodata продолжают обновляться, если это требуется.

Проверка владельца процесса:

```sh
ps -eo user,group,pid,comm,args | grep -E 'mihomo|clash' | grep -v grep
```

## Rollback / recovery

Перед экспериментом сохранить исходный unit.

Если после hardening Mihomo не стартует или dataplane изменился:

```sh
cp /root/mihomo.service.backup /etc/systemd/system/mihomo.service
systemctl daemon-reload
systemctl restart mihomo
systemctl --no-pager --full status mihomo
```

Путь backup здесь только пример: использовать реально выбранный заранее путь и не перезаписывать единственную копию.

После rollback повторить baseline-проверки TUN, routing, DNS и proxy.

## Что подтверждено, а что нет

**Confirmed:**

- официальный systemd-пример Mihomo использует Linux capabilities;
- upstream-пример содержит более широкий набор, чем `CAP_NET_ADMIN + CAP_NET_BIND_SERVICE`;
- TUN/auto-route/auto-redirect выполняют сетевые операции, которые нельзя оценивать только по факту запуска процесса;
- `AmbientCapabilities=...` и `CapabilityBoundingSet=...` — директивы systemd unit, а не команды shell.

**Observed (из переданного владельцем Gemini-аудита):**

- на исследованном VPS Mihomo был запущен как root;
- был отмечен обычный пользователь `mita` UID 1000;
- sudo-группа/дополнительные sudoers в том снимке не использовались.

Эти наблюдения относятся только к тому VPS и не являются общим свойством установок Mihomo.

**Still research / unknown:**

- минимальный capability-set для конкретной конфигурации владельца;
- нужен ли ей `CAP_NET_RAW`;
- совместимость non-root с используемыми TUN/TProxy/Mihomo-функциями;
- точный writable-path layout;
- совместимость с `ProtectSystem=full` и дополнительными systemd sandboxing options;
- отсутствие регрессий после перезагрузки.

## Практика владельца: почему это не срочная миграция

**Observed (owner practice, 2026-09-29):** владелец ранее уже экспериментировал на своих VPS с переводом сервисов/сетапа от полного root к менее привилегированной схеме, но в итоге сознательно отказался от этой практики для текущих серверов. Существующие root-based установки Mihomo эксплуатируются примерно полгода или дольше и за это время наблюдаемых проблем, связанных именно с запуском Mihomo от root, не зафиксировано.

Это наблюдение важно как противовес абстрактной hardening-рекомендации: работающая длительное время конфигурация не должна переделываться только ради формального соответствия совету AI. Одновременно отсутствие наблюдавшихся инцидентов **не доказывает**, что root-вариант безопаснее или что риск отсутствует.

Практический вывод для этой базы знаний:

- текущие рабочие VPS не мигрировать на non-root только из-за рекомендации Gemini;
- считать non-root/capability-модель потенциальным hardening, а не исправлением обнаруженной неисправности;
- проверять её сначала на disposable/test VPS;
- сравнивать не только статус процесса, но и TUN/TProxy, routing, DNS, providers, restart и reboot;
- повышать рекомендацию до Observed/Confirmed только после собственного успешного длительного теста.

Таким образом, здесь сознательно сохранены **оба слоя знания**: рекомендация Gemini как research-гипотеза и реальная эксплуатационная практика владельца как Observed.

## Следующий практический шаг

На disposable/test VPS выполнить **наблюдаемый поэтапный эксперимент**, а не сразу заменить production unit. По результату зафиксировать:

1. точный Mihomo version;
2. unit до/после;
3. фактический capability-set;
4. используемые TUN/TProxy функции;
5. writable paths;
6. проверки dataplane;
7. reboot test.

Только после этого повышать статью из Research в Observed/Confirmed.

## Источники и provenance

- Mihomo official docs — systemd service: https://wiki.metacubex.one/en/startup/service/
- Mihomo official docs — TUN: https://wiki.metacubex.one/en/config/inbound/tun/
- raw AI research: [../archive/raw/gemini-mihomo-systemd-hardening-2026-09-29.md](../archive/raw/gemini-mihomo-systemd-hardening-2026-09-29.md)
- owner-provided environment observations: 2026-09-29
