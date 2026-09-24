# DNS Keenetic через Mihomo: штатный путь через ProxyN (DoT/DoH `on ProxyN`)

**Статус:** Confirmed (архитектурные примитивы: синтаксис CLI Keenetic, контракт ProxyN в
`keenetic-auto-setup`, возможности Mihomo) + Research (сквозная цепочка целиком не
проверялась на живом роутере; live-тест — обязательный следующий шаг)  
**Область применения:** KeeneticOS 3.9+ (компонент «Proxy client»); связка
`keenetic-auto-setup` (ProxyN → Mihomo `127.0.0.1:7890`); задача «DNS самого Keenetic не
должен уходить через провайдера напрямую»  
**Проверено на:** официальный CLI-справочник Keenetic (команды `dns-proxy tls/https
upstream`, `ip name-server`, `ip route`, `dns-proxy intercept enable`), код
`saymer-alt/keenetic-auto-setup` (install.sh, ARCHITECTURE.md), документация Mihomo
(wiki.metacubex.one) — всё на 2026-09-24  
**Последняя проверка:** 2026-09-24  
**Source of truth:** CLI-справочник Keenetic; `keenetic-auto-setup/install.sh` (контракт
ProxyN); [wiki.metacubex.one/config/dns](https://wiki.metacubex.one/en/config/dns/)  
**Provenance:** research-диалог [`mihomo-dns.md`](../archive/raw/mihomo-dns.md) (снимок 2026-09-22);
форум Keenetic — как поддерживающее свидетельство, не как истина

## Что решаем

Задача: **upstream DNS самого Keenetic** (куда роутер ходит за резолвингом) должен
проходить через Mihomo и его proxy/outbound, а не напрямую через провайдера. При этом
решение должно оставаться штатным для KeeneticOS — без iptables-хаков и без
принудительного заворачивания системного DNS в TUN Mihomo.

Кандидатная архитектура:

```text
Keenetic DNS-proxy
  ↓ DoT (TCP/853) или DoH, привязанный к ProxyN
ProxyN (прокси-интерфейс KeeneticOS)
  ↓ SOCKS5
127.0.0.1:7890 (mixed-port Mihomo)
  ↓ правила Mihomo
выбранный proxy / proxy-group
  ↓
удалённый DNS-резолвер (DoT/DoH)
```

Статья фиксирует, какие примитивы этой схемы подтверждены синтаксисом и кодом, а какие
части остаются непроверенными до live-теста. **Полная цепочка целиком нигде ещё не
запускалась** — это Research-интеграция на подтверждённых примитивах.

## Контекст: три независимых DNS-решения

Прежде чем менять DNS, важно развести три разных вопроса (модель — из
[`ARCHITECTURE.md`](https://github.com/saymer-alt/keenetic-auto-setup/blob/main/ARCHITECTURE.md)
проекта `keenetic-auto-setup`):

1. **DNS клиента** — куда клиенты отправляют запросы. Установщик проекта включает
   перехват транзитного DNS (`dns-proxy intercept enable`), чтобы классический DNS/53
   приходил в DNS-прокси роутера (нужно MagiTrickle для классификации).
2. **DNS upstream** — куда за резолвингом ходит сам Keenetic. Этим управляют `ip
   name-server` (классические DNS) и `dns-proxy tls/https upstream` (DoT/DoH). **Только
   этот уровень — предмет настоящей статьи.**
3. **DoH/DoT клиентов** — шифрованный DNS браузеров и приложений идёт мимо порта 53 в
   любом случае и перехватом не контролируется.

### Ключевое различение: `dns-proxy intercept` ≠ выбор upstream-пути

`dns-proxy intercept enable` — это **перехват транзитных DNS-запросов клиентов**:
клиент хотел отправить классический DNS/53 внешнему резолверу, а Keenetic перенаправил
запрос в собственный DNS-proxy. Официальный справочник описывает команду именно так:
«Enable transit DNS requests interception for system profile» (появилась в 3.06, в 3.08
убиралась как устаревшая, с 3.09 снова присутствует).

```text
client DNS interception                          Keenetic DNS-proxy → upstream
(перехват запросов клиентов)                     (транспорт/путь собственного резолва)
        dns-proxy intercept enable                 ip name-server / dns-proxy tls|https upstream
```

Это **не** настройка того, через какой интерфейс/WAN/Proxy идёт upstream DNS самого
Keenetic. Для управления upstream-путем служит привязка `on <interface>` в командах
upstream — см. ниже. Смешение этих двух механизмов — типичная ошибка при обсуждении
«завести DNS в прокси».

## Как это работает (подтверждённые примитивы)

### CLI Keenetic: upstream с привязкой к интерфейсу

Официальный CLI-справочник подтверждает синтаксис (версии — по history справочника;
проверено 2026-09-24):

**DoT upstream** (с 3.01; аргумент `domain` — с 3.08):

```text
dns-proxy tls upstream <address> [<port>] [sni <fqdn>] [spki <hash>] [on <interface>] [domain <domain>]
no dns-proxy tls upstream [<address>] [<port>]
```

Родной пример справочника — ровно тот случай, который нужен для эксперимента:

```text
(config-dnspx)> tls upstream 1.1.1.1 853 sni cloudflare-dns.com on ISP
Dns::Secure::ManagerDot: DNS-over-TLS name server 1.1.1.1:853 added.
```

**DoH upstream** (с 3.01; `domain` — с 3.08):

```text
dns-proxy https upstream <url> [<format>] [sni <hash>] [on <interface>] [domain <domain>]
no dns-proxy https upstream [<url>]
```

Пример справочника: `https upstream https://dns.adguard.com/dns-query dnsm on ISP`.
Отличие от DoT: endpoint задаётся URL (доменное имя), что добавляет задачу начального
резолва имени самого DoH-сервера; в справочнике для DoH параметр закрепления сертификата
идёт как hash (spki) — тонкость синтаксиса, которую при live-тесте нужно сверить с
подсказкой CLI на месте (`dns-proxy https upstream ?`).

**Классический DNS с привязкой** (`ip name-server`, с 2.00; порт — с 2.14):

```text
ip name-server <address> [:<port>] [<domain> [on <interface>]]
no ip name-server [<address>[:<port>]] [<domain> [on <interface>]]
```

Пример справочника: `ip name-server 8.8.8.8 "" on ISP` (пустая строка `""` — домен по
умолчанию, сервер используется для всех запросов; до 16 доменов на одну запись).

**Скоупинг эксперимента доменом.** И DoT/DoH upstream, и `ip name-server` принимают
аргумент `domain <домен>` — запись обслуживает только указанную зону. Это позволяет
проводить проверку, не переводя весь роутер на новый DNS.

**Статический /32-маршрут с fail-closed семантикой** (`ip route`; `reject` — с 3.08,
работает только вместе с `auto`, неприменим к default route):

```text
ip route <host> <interface> auto reject
```

Официальное описание `reject`: «If the specified interface is not active, the traffic is
not sent via other possible routes» — то есть при недоступности выбранного интерфейса
трафик **не** уходит через другие маршруты. Родной пример справочника:
`ip route 123.123.123.123 Wireguard1 auto reject`.

### Контракт ProxyN из кода keenetic-auto-setup

Подтверждено по `install.sh` текущего `main` (проверено 2026-09-24):

- проектный ProxyN — Proxy-интерфейс KeeneticOS с upstream **SOCKS5 на
  `127.0.0.1:7890`** (фиксированный контрактный порт Mihomo);
- порядок настройки в установщике: сначала `interface ProxyN proxy protocol socks5`,
  затем `interface ProxyN proxy socks5-udp`, затем `interface ProxyN proxy upstream
  127.0.0.1 7890`, затем `description "mihomo t2sN"`;
- проектный интерфейс опознаётся по **двум** маркерам сразу (`description "mihomo t2sN"`
  и `proxy upstream 127.0.0.1 7890` в одном блоке running-config); чужой Proxy не
  трогается; на чистом роутере создаётся `Proxy0`, при занятом — первый свободный
  `ProxyN`;
- bootstrap-конфиг Mihomo от установщика содержит только `mixed-port: 7890` — секции
  `dns:` в проекте **нет**: DNS-listener Mihomo не является частью текущей установки.

Компонент «Proxy client» существует с KeeneticOS 3.9 (официальная статья «Proxy client»),
поддерживает HTTP/HTTPS/SOCKS5. Сами подкоманды `proxy protocol` / `proxy socks5-udp` /
`proxy upstream` в индекс CLI-справочника не входят — они живут в контексте интерфейса
(документированы в PDF-справочниках CLI и видны в `show running-config`); для нас их
авторитетный источник — код установщика, который применяет их на реальных роутерах.

### Возможности Mihomo (текущая документация)

Подтверждено по [wiki.metacubex.one/config/dns](https://wiki.metacubex.one/en/config/dns/)
(проверено 2026-09-24):

- `dns.enable` + `dns.listen` — встроенный DNS-сервер Mihomo; listener поддерживает UDP
  и TCP (пример: `listen: 127.0.0.1:1053`);
- `enhanced-mode: redir-host | fake-ip` — оба режима документированы (default —
  redir-host); redir-host не помечен deprecated;
- upstream-DNS можно привязать к прокси или интерфейсу суффиксом `#`:
  `'https://8.8.8.8/dns-query#PROXY'` (имя существующего прокси; иначе — имя интерфейса),
  `#RULES` — следовать routing-правилам;
- `proxy-server-nameserver` — отдельный резолвер для доменных имён proxy-нод; без него
  при proxy-bound DNS возможен chicken-and-egg (документированное предупреждение);
- `default-nameserver` — резолвер имён самих DNS-серверов (нужен, когда upstream задан
  доменным именем, например DoH URL);
- routing-правила Mihomo матчатся сверху вниз, приоритет у верхних; у IP-правил есть
  параметр `no-resolve` (нюанс: если DNS-резолв уже был вызван более ранним правилом,
  target-IP правило сматчится и с `no-resolve`).

## Кандидатные варианты

| Схема | Что происходит | Статус |
| --- | --- | --- |
| `dns-proxy tls upstream … on ProxyN` | Keenetic отправляет DoT (TCP/853) через SOCKS5/Mihomo | **Первый кандидат**; примитивы Confirmed, цепочка — Research |
| `dns-proxy https upstream … on ProxyN` | То же через DoH | Research (сложнее: bootstrap имени endpoint) |
| `ip name-server <IP> "" on ProxyN` | Классический UDP/TCP DNS через ProxyN (SOCKS5 UDP) | Research; зависит от фактической работы `proxy socks5-udp` |
| `/32 ip route → ProxyN [auto reject]` | Принудительный маршрут IP резолвера через Proxy-интерфейс | Research-fallback; риск петли при DIRECT в Mihomo (см. ниже) |
| Keenetic → `127.0.0.1:1053` → DNS Mihomo с `#PROXY` upstream | DNS полностью отдаётся Mihomo | Research (план B/C: требует правки `config.yaml`, не входит в проект) |
| Keenetic → `mitun0` напрямую | Системный DNS заворачивается в TUN Mihomo | **Не рекомендуется** — см. ниже |

### Почему не `mitun0` напрямую

`mitun0` — Linux TUN, созданный **самим Mihomo**; `ProxyN` — полноценный интерфейс
KeeneticOS, который NDM знает как соединение. При заворачивании системного DNS в
`mitun0` нет простой гарантии, что собственные outbound-соединения Mihomo не попадут
обратно в его же TUN (особенно для локально созданного трафика роутера). У `ProxyN`
граница компонентов ясная: `Keenetic application → ProxyN → SOCKS → Mihomo → outbound`.
Прямой `mitun0`-вариант не является каноническим, пока не доказан отдельно (обратное
тоже не доказано — это осознанный выбор более простой для рассуждения границы).

## Требования

- KeeneticOS 3.9+ с установленным компонентом «Proxy client»;
- развёрнутый `keenetic-auto-setup` (существующий проектный ProxyN, Mihomo слушает
  `127.0.0.1:7890`);
- доступ к CLI роутера (`ndmc`) и понимание, что команды ниже меняют running-config
  (не persistent до `system configuration save`);
- для доказательства egress — доступ к VPS, через который реально выходит выбранный
  proxy (tcpdump на выходе).

## Безопасный тест-план (НЕ выполнен; выполнять только как задачу на живом роутере)

Цель: доказать цепочку `Keenetic DoT → ProxyN → Mihomo → proxy (не DIRECT) → 1.1.1.1:853`,
не переводя роутер на новый DNS и не сохраняя конфигурацию до успешной проверки.

1. **Снять состояние, ничего не меняя.** Определить фактический проектный `ProxyN`
   (не предполагать `Proxy0`):

   ```bash
   ndmc -c 'show version'
   ndmc -c 'show ip name-server'
   ndmc -c 'show dns-proxy'
   ndmc -c 'show running-config' | grep -E 'interface Proxy|description.*mihomo|proxy protocol|proxy socks5-udp|proxy upstream|ip global'
   ```

   Проектный интерфейс опознаётся по паре маркеров в одном блоке:
   `description "mihomo t2sN"` + `proxy upstream 127.0.0.1 7890`. Ниже в примерах —
   `Proxy0`; подставить фактический.

2. **Выбрать DNS-IP, которого сейчас нет** среди name-server/upstream — это упростит
   чистое удаление тестовой записи. Если `1.1.1.1` уже используется, взять другой
   публичный DoT-резолвер (например, из Quad9/Google) и соответствующий ему SNI.

3. **Добавить domain-scoped DoT upstream** (меняет только running-config; не трогает
   DNS остальных зон):

   ```bash
   ndmc -c 'dns-proxy tls upstream 1.1.1.1 853 sni cloudflare-dns.com on Proxy0 domain example.com'
   ndmc -c 'show dns-proxy'
   ```

   `domain example.com` ограничивает запись тестовой зоной: весь остальной резолв
   роутера не меняется.

4. **Проверить резолв через Keenetic** с LAN-клиента, явно указав роутер как DNS
   (чтобы не смешивать с DNS самой ОС клиента; если DHCP выдаёт клиентам внешний DNS
   напрямую, клиент вообще минует DNS-proxy роутера):

   ```cmd
   nslookup example.com <LAN-IP-роутера>
   ```

5. **Доказать путь трафика, а не только успешный резолв:**

   ```bash
   # на Keenetic (Entware): активность между Proxy-интерфейсом и Mihomo
   tcpdump -ni lo 'port 7890'
   # не появляется ли ПРЯМОЕ соединение с 1.1.1.1 через WAN (утечка мимо ProxyN)
   tcpdump -ni any 'host 1.1.1.1 and tcp port 853'
   ```

   Плюс Mihomo-дашборд (Connections): куда Mihomo отправил `1.1.1.1:853`. Самое сильное
   доказательство — tcpdump на VPS, через который выходит выбранный proxy:
   `host 1.1.1.1 and tcp port 853` на выходе VPS закрывает цепочку полностью.

6. **Различить «попал в Mihomo» и «вышел через proxy».** Попадание DNS в Mihomo ещё не
   означает выход через туннель: если правила Mihomo выбирают `DIRECT` для `1.1.1.1`,
   DNS уйдёт через провайдера, хотя ProxyN сработал. Правила матчатся сверху вниз; для
   эксперимента можно временно закрепить адрес за реальной proxy-группой:

   ```yaml
   rules:
     - IP-CIDR,1.1.1.1/32,ИМЯ_PROXY_ГРУППЫ,no-resolve
   ```

   (имя группы — из фактического `config.yaml`; правка — временная, с откатом).

7. **Удалить тестовую запись штатной командой:**

   ```bash
   ndmc -c 'no dns-proxy tls upstream 1.1.1.1 853'
   ndmc -c 'show dns-proxy'
   ```

8. **Не выполнять `system configuration save`** до успешного завершения проверки; после
   удаления тестовой записи running-config возвращается к исходному состоянию
   перезагрузкой или сохранением без тестовых записей — по выбору оператора.

Если `on Proxy0` принимается, но DoT фактически не идёт через Proxy — резервный путь:
`/32`-маршрут `ip route 1.1.1.1 Proxy0 auto reject` (fail-closed). **Только после**
проверки правила Mihomo из шага 6: при `DIRECT` для этого адреса маршрут зациклится
(`1.1.1.1 → Proxy0 → Mihomo → DIRECT → маршрут Proxy0 → …`).

## Типичные проблемы

### «DNS работает», но уходит через провайдера

Резолв успешен, tcpdump на WAN видит `1.1.1.1:853` напрямую. Причина: правила Mihomo
выбрали `DIRECT` (шаг 6). Лечение — закрепить адрес за proxy-группой.

### Петля при /32-маршруте

`ip route … auto reject` + `DIRECT` для того же адреса в Mihomo = цикл. Всегда сначала
правило Mihomo, потом маршрут.

### Chicken-and-egg у proxy-bound DNS Mihomo

Upstream вида `https://8.8.8.8/dns-query#PROXY` требует, чтобы домен proxy-ноды
резолвился без прокси — для этого существуют `proxy-server-nameserver` и
`default-nameserver` (документированное предупреждение Mihomo).

### ISP DNS всё ещё опрашивается параллельно

Keenetic обращается к нескольким настроенным DNS (до 8 upstream, приоритет по времени
отклика; статические/динамические name-server описаны в справочнике `ip name-server`).
«Ни одного DNS через провайдера» — отдельная задача: удаление/игнорирование ISP DNS и
fail-closed политика поверх доказанной схемы, не часть первого эксперимента.

## Rollback / recovery

Все команды теста обратимы штатными `no`-формами без сохранения конфигурации:

```bash
ndmc -c 'no dns-proxy tls upstream 1.1.1.1 853'   # удалить DoT upstream
ndmc -c 'no ip name-server <IP> [domain]'         # удалить классический NS (если использовался)
ndmc -c 'no ip route 1.1.1.1 Proxy0'              # удалить тестовый /32-маршрут
ndmc -c 'show dns-proxy'                          # убедиться, что тестовых записей нет
```

Эксперимент domain-scoped, не меняет default route и не трогает `dns-proxy intercept`;
после `no`-форм и проверки `show`-командами сохранение конфигурации не требуется.

## Что подтверждено, а что нет

**Confirmed** (по официальному справочнику/коде/документации, 2026-09-24):

- синтаксис `dns-proxy tls upstream … [on <interface>] [domain <domain>]` (с 3.01,
  `domain` с 3.08), включая родной пример `1.1.1.1 853 sni cloudflare-dns.com on ISP`;
- синтаксис `dns-proxy https upstream … [on <interface>] [domain <domain>]`;
- синтаксис `ip name-server <address>[:port] [<domain> [on <interface>]]` (с 2.00);
- `no`-формы удаления всех трёх;
- `dns-proxy intercept enable` = перехват транзитного DNS (не выбор upstream-пути);
- `ip route <host> <iface> auto reject` — fail-closed маршрут (с 3.08, только с `auto`);
- проектный ProxyN: SOCKS5, upstream `127.0.0.1:7890`, порядок
  `protocol socks5 → socks5-udp → upstream`, маркеры `mihomo t2sN` + upstream,
  первый свободный ProxyN (код `keenetic-auto-setup`);
- в проекте нет DNS-listener Mihomo (bootstrap-конфиг = только `mixed-port: 7890`);
- Mihomo: `dns.listen` UDP/TCP, redir-host валиден, привязка upstream `#PROXY/#RULES`,
  `proxy-server-nameserver`, `default-nameserver`, правила сверху вниз, `no-resolve`;
- официальная рекомендация использовать DoT/DoH при работе через Proxy (статья «Proxy
  client»; тема форума «DNS через прокси-клиент» — поддерживающее свидетельство).

**Observed:**

- ProxyN как рабочий egress подтверждён практическим кейсом владельца (камеры в
  политике с выходом через `t2s0/ProxyN → Mihomo` — см. статью о слоях именования);
- на форуме Keenetic зафиксирован чужой рабочий тест UDP-DNS через `proxy socks5-udp`
  после порядка `protocol socks5 → socks5-udp` (тема «туннелирование UDP через socks5
  proxy», проверка через `myip.opendns.com @resolver1.opendns.com`) — стороннее
  наблюдение, не наш тест.

**Research / needs live test (не считать доказанным):**

- что DoT/DoH upstream с `on ProxyN` **фактически** маршрутизируется через SOCKS5 на
  живом роутере (справочник допускает интерфейс, форумы поддерживают, но на нашей
  KeeneticOS это не проверялось);
- фактическая работа `proxy socks5-udp` для классического DNS через ProxyN (UDP/53 в
  SOCKS5 UDP ASSOCIATE);
- вся цепочка целиком, включая «вышел через proxy, а не DIRECT» и подтверждение на
  выходе VPS;
- варианты DoH (bootstrap имени endpoint), `/32 reject`-маршрута и DNS-listener Mihomo;
- поведение при недоступности ProxyN (что делает DoT-upstream: ждёт, fallback на
  другие upstream, молчит) — определить в live-тесте;
- интернет-детали реализации Proxy client (hev-socks5-tunnel и история фикса UDP) —
  форумные свидетельства, не официальная документация.

## Источники и provenance

- Официальный CLI-справочник Keenetic (команды `dns-proxy tls/https upstream`, `ip
  name-server`, `ip route`, `dns-proxy intercept enable`; проверено через встроенный
  справочник 2026-09-24) — источник истины по синтаксису.
- Статья «Proxy client» (support.keenetic.com, компонент с OS 3.9, HTTP/HTTPS/SOCKS5,
  рекомендация DoT/DoH).
- Код: `saymer-alt/keenetic-auto-setup` — `install.sh` (контракт ProxyN, порядок
  подкоманд, маркеры, bootstrap-конфиг Mihomo), `ARCHITECTURE.md` (три уровня DNS,
  8 upstream, DoT/DoH с OS 3.0).
- Mihomo: [DNS configuration](https://wiki.metacubex.one/en/config/dns/),
  [Route Rules](https://wiki.metacubex.one/en/config/rules/) (проверено 2026-09-24).
- Форум Keenetic (поддерживающие свидетельства): «DNS через прокси-клиент» (тема
  19957), «туннелирование UDP через socks5 proxy» (тема 19036), «Настройка Proxy
  только для определённых сайтов» (тема 17351, /32 через Proxy-интерфейс).
- Raw/provenance: [`mihomo-dns.md`](../archive/raw/mihomo-dns.md) — research-диалог 2026-09-22, из
  которого извлечена эта статья; его команды не проверялись как production-процедура.

## Связанные материалы

- [Mihomo на Keenetic: где он в архитектуре маршрутизации](mihomo-keenetic-routing.md) —
  слои и три пути трафика, ProxyN/mitun0.
- [Политика, сегмент, SSID и маршрут: не называйте всё WL](keenetic-policy-segment-ssid-naming.md) —
  где ProxyN/t2sN и политика доступа лежат в общей карте слоёв.
- [Режим белых списков: как это устроено и что работает](whitelist-mode-architecture.md) —
  внешний контекст, в котором вопрос «DNS через Mihomo» возникает.
