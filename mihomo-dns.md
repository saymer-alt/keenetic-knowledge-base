Да. Я покопался именно в связке **Keenetic → Proxy-клиент → Mihomo**, а не в общих советах для OpenWrt. И похоже, мы наконец нашли тот штатный механизм Keenetic, который раньше у нас оставался недокопанным.

## Главный вывод

Для нашей архитектуры я бы **не отправлял DNS самого Keenetic напрямую в `mitun0`**. У Keenetic уже есть более правильный штатный путь:

```text
Клиент
  ↓ DNS
Keenetic DNS-proxy
  ↓
DoT / DoH, привязанный к ProxyN
  ↓
ProxyN
  ↓ SOCKS5
127.0.0.1:7890
  ↓
Mihomo
  ↓ правила Mihomo
нужный proxy / proxy-group
  ↓
VLESS / HY2 / AWG / ...
  ↓
удалённый DNS
```

И это не просто моя теория. В CLI Keenetic для **DoT и DoH прямо существует параметр `on <interface>`**. Для DoT синтаксис такой:

```text
dns-proxy tls upstream <address> [port] ... [on <interface>] [domain <domain>]
```

То есть DNS-соединение можно явно привязать к определённому интерфейсу. То же самое предусмотрено для DoH. ([Google Cloud Storage][1])

А на форуме Keenetic есть тема буквально **«DNS через прокси-клиент»**. Пользователь жалуется, что DNS идёт мимо Proxy, и Le ecureuil отвечает: почему бы, согласно официальной инструкции, не настроить **DoH/DoT на прокси-интерфейсе**. То есть это практически наш случай. ([Keenetic Community][2])

Более того, официальная документация Keenetic по Proxy Client отдельно предупреждает, что для нормальной работы доступа через Proxy рекомендуется использовать DNS-over-TLS или DNS-over-HTTPS. ([Кинетик][3])

### Почему это особенно хорошо подходит нашему проекту

Наш `ProxyN` уже ведёт в:

```text
127.0.0.1:7890
```

то есть прямо в Mihomo. И текущий `install.sh` настраивает Proxy-интерфейс как SOCKS5 и включает `socks5-udp`.

С UDP у Keenetic была интересная история: в старых версиях пользователи жаловались, что `proxy socks5-udp` не работает. Но в ноябре 2025 это повторно исследовали уже после перехода Keenetic на `hev-socks5-tunnel`: оказалось, что надо сначала задать `proxy protocol socks5`, затем `proxy socks5-udp`. После этого пользователь проверил DNS через OpenDNS и подтвердил: **«Работает!»**. Именно такой порядок у нас сейчас и используется. ([Keenetic Community][4])

То есть у нас потенциально работают **оба** варианта: обычный UDP/53 через ProxyN и DoT/DoH через ProxyN.

---

## Что я предлагаю тестировать завтра первым

Я бы начал именно с **DoT через ProxyN**, а не с обычного UDP DNS.

Причины простые: DoT — TCP/853, значит мы вообще не зависим от особенностей SOCKS5 UDP; в Keenetic команда официально умеет `on ProxyN`; сервер задаётся IP-адресом + SNI, поэтому нет проблемы «сначала надо разрешить имя самого DoH-сервера»; а если из-за ошибки Mihomo вдруг выпустит соединение через `DIRECT`, провайдер хотя бы увидит TLS-соединение, а не открытый DNS.

Для первого опыта я бы использовал Cloudflare просто потому, что **сам Keenetic в официальном CLI приводит ровно этот пример**:

```text
1.1.1.1:853
SNI cloudflare-dns.com
```

([Google Cloud Storage][5])

Очень важно: **не сохраняем конфигурацию через `system configuration save`**, пока не убедимся, что схема работает.

### Завтрашний тест

1. Сначала ничего не меняем и снимаем состояние. Нам надо определить именно наш проектный `ProxyN`:

```bash
ndmc -c 'show version'
ndmc -c 'show ip name-server'
ndmc -c 'show dns-proxy'
ndmc -c 'show ip route'
ndmc -c 'show running-config' | grep -E 'interface Proxy|description.*mihomo|proxy protocol|proxy socks5-udp|proxy upstream|ip global'
```

Ожидаем увидеть что-то вроде:

```text
interface Proxy0
    description "mihomo t2s0"
    proxy protocol socks5
    proxy socks5-udp
    proxy upstream 127.0.0.1 7890
```

Не обязательно это будет именно `Proxy0` — наш installer специально умеет использовать `Proxy1`, `Proxy2` и т.д.

2. Затем выберем DNS, которого **сейчас нет среди твоих DNS-серверов**. Это важно для безопасного удаления тестовой записи. Если `1.1.1.1` свободен, допустим наш интерфейс оказался `Proxy0`:

```bash
ndmc -c 'dns-proxy tls upstream 1.1.1.1 853 sni cloudflare-dns.com on Proxy0 domain example.com'
```

`domain example.com` здесь очень удобен: эксперимент не переводит весь роутер на новый DNS, а ограничивает новую запись тестовой зоной. Поддержка и `on <interface>`, и `domain <domain>` есть в официальном синтаксисе Keenetic. ([Google Cloud Storage][5])

После этого:

```bash
ndmc -c 'show dns-proxy'
```

3. Теперь с компьютера обращаемся **именно к Keenetic как DNS**, чтобы не путать эксперимент с DNS самого Windows:

```cmd
nslookup example.com 192.168.1.1
```

Разумеется, вместо `192.168.1.1` — LAN-адрес тестового Keenetic.

Это важно ещё по одной причине: официальный Keenetic поясняет, что если DHCP выдаёт клиенту внешний DNS напрямую, клиент вообще минует DNS-proxy роутера. Нам сейчас нужно исследовать именно цепочку `client → Keenetic DNS-proxy`. ([Кинетик][6])

4. Теперь самое главное — доказать **не просто успешный DNS**, а путь трафика.

На Keenetic полезно посмотреть:

```bash
tcpdump -ni lo 'port 7890'
```

Во время `nslookup` должна появиться активность между Proxy-интерфейсом и Mihomo.

Отдельно:

```bash
tcpdump -ni any 'host 1.1.1.1 and tcp port 853'
```

Здесь нас интересует, **не появляется ли прямое соединение с 1.1.1.1 через WAN**.

А ещё лучше посмотреть в MetaCubeX/Mihomo connections, куда Mihomo отправил:

```text
1.1.1.1:853
```

И самый железобетонный вариант, поскольку у тебя есть свои VPS: на том сервере, через который сейчас реально выходит выбранный proxy, посмотреть:

```bash
tcpdump -ni any 'host 1.1.1.1 and tcp port 853'
```

Если мы увидим `1.1.1.1:853` уже **на выходе VPS**, задача доказана полностью:

```text
Keenetic DNS
→ ProxyN
→ Mihomo
→ VPS
→ 1.1.1.1:853
```

5. Здесь есть один очень важный подводный камень. **Попадание DNS в Mihomo ещё не означает, что Mihomo отправил его через туннель.**

Например:

```text
Keenetic
 → Proxy0
 → Mihomo
 → DIRECT
 → 1.1.1.1
```

технически означает, что ProxyN прекрасно сработал — но DNS всё равно вышел через провайдера.

Mihomo обрабатывает такие соединения обычными `rules`, причём правила идут сверху вниз. Поэтому если твой конфиг для `1.1.1.1` выбирает `DIRECT`, получим именно этот эффект. ([Метакубекс Вики][7])

Если это обнаружится, для эксперимента можно временно заставить этот адрес идти через **реальное имя твоей proxy-группы**:

```yaml
rules:
  - IP-CIDR,1.1.1.1/32,ИМЯ_ТВОЕЙ_PROXY_ГРУППЫ,no-resolve
```

Именно имя группы я сейчас намеренно не придумываю — завтра посмотрим твой реальный конфиг.

6. После теста запись удаляется штатной командой:

```bash
ndmc -c 'no dns-proxy tls upstream 1.1.1.1 853'
```

Keenetic официально документирует именно такой `no`-синтаксис удаления конкретного DoT upstream. ([Google Cloud Storage][5])

Поэтому я и предлагаю брать DNS-IP, которого до эксперимента в конфигурации нет.

7. Если выяснится, что твоя KeeneticOS почему-то принимает `on Proxy0`, но фактически не направляет DoT в Proxy, тогда идём вторым путём — **жёсткий `/32` маршрут DNS-сервера через ProxyN**:

```bash
ndmc -c 'ip route 1.1.1.1 Proxy0 auto reject'
```

Статический маршрут через Proxy-интерфейс — нормальный поддерживаемый сценарий Keenetic; на форуме показан работающий пример, где `/32` имеет `interface: Proxy0`, а Linux-маршрут уходит через соответствующий `t2s` интерфейс. ([Keenetic Community][8])

`reject` здесь особенно интересен: если выбранный интерфейс перестанет быть доступен, маршрут не должен тихо свалиться на другой WAN. Это позволяет строить **fail-closed DNS без утечки**. Такая возможность есть в современном синтаксисе статических маршрутов Keenetic. ([Google Cloud Storage][1])

Но этот вариант требует осторожности: если Mihomo для `1.1.1.1` после получения соединения выберет `DIRECT`, может получиться петля:

```text
1.1.1.1
 → маршрут Proxy0
 → Mihomo
 → DIRECT на 1.1.1.1
 → маршрут Proxy0
 → Mihomo
 ...
```

Поэтому `/32 → ProxyN` будем пробовать **только после проверки правила Mihomo**.

---

## Какие варианты вообще получаются

| Схема                                    | Что происходит                                      | Для нас                                              |
| ---------------------------------------- | --------------------------------------------------- | ---------------------------------------------------- |
| `DoT on ProxyN`                          | Keenetic сам отправляет TCP/853 через SOCKS5/Mihomo | **Первый кандидат**                                  |
| `DoH on ProxyN`                          | То же через HTTPS                                   | Рабочая идея, но сложнее из-за имени DoH endpoint/H3 |
| `ip name-server ... on ProxyN`           | обычный DNS UDP/TCP через ProxyN                    | Очень интересно после проверки DoT                   |
| `/32 route → ProxyN`                     | принудительный маршрут IP DNS через proxy interface | Хороший fallback                                     |
| Keenetic → `127.0.0.1:1053` → Mihomo DNS | DNS полностью отдаётся внутреннему DNS Mihomo       | Продвинутый вариант                                  |
| напрямую `mitun0`                        | системный DNS роутера направляется в TUN Mihomo     | Я бы пока не трогал                                  |

И особенно интересен третий вариант. Современный CLI Keenetic умеет:

```text
ip name-server <IP> [:port] [domain [on interface]]
```

то есть теоретически мы можем вообще сделать:

```bash
ip name-server 1.1.1.1 "" on Proxy0
```

и обычный UDP DNS Keenetic должен идти через Proxy0. Официальный CLI разрешает привязку `ip name-server` к интерфейсу. ([Google Cloud Storage][1])

А поскольку наш ProxyN уже имеет исправно настроенный SOCKS5 UDP, это **вполне реальный второй эксперимент**.

Для его доказательства есть даже красивый тест, который использовали на форуме Keenetic:

```text
myip.opendns.com @resolver1.opendns.com
```

Пользователь именно так проверил UDP через SOCKS5 и получил внешний IP прокси вместо WAN-IP Keenetic. После исправления порядка `protocol socks5 → socks5-udp` он подтвердил работу. ([Keenetic Community][4])

Это можно будет сделать отдельным тестом через `208.67.222.222`.

---

## Почему я пока против прямого `mitun0`

`mitun0` у нас — Linux TUN, созданный **самим Mihomo**. `ProxyN`, наоборот, — полноценный интерфейс KeeneticOS, который штатный NDM знает как интернет-соединение.

Если насильно направлять системный DNS в `mitun0`, появляется неприятный вопрос: как гарантировать, что собственные outbound-соединения Mihomo не попадут обратно в его же TUN. Особенно при локально созданном трафике роутера.

С `ProxyN` такого архитектурного конфликта нет:

```text
Keenetic application
→ ProxyN
→ SOCKS request
→ Mihomo
→ outbound
```

То есть граница компонентов совершенно ясная.

---

## Есть ещё вариант с собственным DNS Mihomo

Если штатная схема Keenetic окажется недостаточно управляемой, Mihomo сам умеет поднимать DNS listener, например условно:

```yaml
dns:
  enable: true
  listen: 127.0.0.1:1053
  enhanced-mode: redir-host
```

А его upstream DNS можно **явно привязать к proxy**, например синтаксисом вида:

```yaml
nameserver:
  - 'https://8.8.8.8/dns-query#proxy'
```

Mihomo официально поддерживает указание proxy/interface для DNS upstream. Если DNS должен идти по proxy, документация отдельно предупреждает настроить `proxy-server-nameserver`, чтобы не получить chicken-and-egg при разрешении доменного имени самого proxy-сервера. ([Метакубекс Вики][9])

Тогда архитектура будет:

```text
Client
→ Keenetic DNS-proxy
→ 127.0.0.1:1053
→ Mihomo DNS
→ proxy-group
→ remote DNS
```

Причём `dns.listen` Mihomo поддерживает UDP и TCP, а `redir-host` является штатным режимом; для нашего первого опыта я бы **не использовал fake-ip**, чтобы не смешивать исследование DNS transport с Fake-IP/MagiTrickle. ([Метакубекс Вики][9])

Это мне тоже нравится, но уже как **план B/C**, потому что требует менять `config.yaml`. `DoT on ProxyN` гораздо изящнее: Mihomo вообще не обязан становиться DNS-сервером.

---

## И ещё важное про наши старые разговоры о `dns-proxy intercept`

Здесь наконец можно разделить две совершенно разные вещи.

`dns-proxy intercept enable` — это **перехват транзитных DNS-запросов клиентов**. То есть клиент захотел отправить классический DNS/53 куда-то ещё, а Keenetic перехватил его в свой DNS-proxy.

Это **не настройка того, через какой WAN/VPN/Proxy идёт upstream DNS самого Keenetic**. В актуальном CLI она именно так и описана — transit DNS interception. Поэтому для завтрашнего исследования её вообще не надо трогать. ([Google Cloud Storage][1])

Мы просто делаем:

```text
nslookup test-domain <IP Keenetic>
```

и тем самым гарантированно обращаемся непосредственно к DNS-proxy.

Это заодно позволит нам не смешивать два наших старых вопроса.

---

### Что я считаю наиболее вероятным результатом

С высокой вероятностью рабочая штатная конструкция окажется такой:

```text
dns-proxy
    tls upstream 1.1.1.1 853 sni cloudflare-dns.com on ProxyN
```

а в Mihomo нужно будет только гарантировать, что `1.1.1.1:853` выбирает нужную proxy-группу, а не `DIRECT`.

И тогда это уже может стать **новой нормальной функцией нашего `keenetic-auto-setup`**, а не каким-то iptables-хаком: installer/Doctor смогут видеть `ProxyN`, DNS upstream сможет быть привязан к этому же проектному интерфейсу, и вся цепочка останется штатной для Keenetic.

Есть ещё одна архитектурная вещь на будущее: Keenetic умеет одновременно обращаться к нескольким доступным DNS и использовать быстрые ответы; официальная документация прямо предупреждает, что запросы могут отправляться имеющимся DNS-серверам, включая полученные от ISP. Поэтому если целью станет **«ни одного DNS через провайдера»**, после доказательства схемы придётся отдельно продумать удаление/игнорирование ISP DNS и политику fail-closed/fail-open. ([Кинетик][10])

Но **завтра я бы ISP DNS пока вообще не трогал**. Сначала сделаем маленький domain-scoped тест `example.com → DoT on ProxyN`, посмотрим tcpdump + Mihomo + выход VPS. Если это подтвердится — дальше уже аккуратно спроектируем полноценный режим **DNS via Mihomo** для проекта. Это выглядит значительно перспективнее, чем тот путь, который мы раньше пытались искать через `mitun0`.

[1]: https://storage.googleapis.com/docs.help.keenetic.com/cli/5.0/en/cli_manual_kn-1010_tr.pdf "https://storage.googleapis.com/docs.help.keenetic.com/cli/5.0/en/cli_manual_kn-1010_tr.pdf"
[2]: https://forum.keenetic.ru/topic/19957-dns-%D1%87%D0%B5%D1%80%D0%B5%D0%B7-%D0%BF%D1%80%D0%BE%D0%BA%D1%81%D0%B8-%D0%BA%D0%BB%D0%B8%D0%B5%D0%BD%D1%82/?utm_source=chatgpt.com "DNS через прокси-клиент. - Обмен опытом - Keenetic Community"
[3]: https://support.keenetic.com/peak/kn-2710/en/49443-proxy-client.html?utm_source=chatgpt.com "Proxy client"
[4]: https://forum.keenetic.ru/topic/19036-%D1%82%D1%83%D0%BD%D0%BD%D0%B5%D0%BB%D0%B8%D1%80%D0%BE%D0%B2%D0%B0%D0%BD%D0%B8%D0%B5-udp-%D1%87%D0%B5%D1%80%D0%B5%D0%B7-socks5-proxy/?utm_source=chatgpt.com "туннелирование UDP через socks5 proxy - Развитие - Keenetic Community"
[5]: https://storage.googleapis.com/docs.help.keenetic.com/cli/4.0/en/cli_manual_kn-1011.pdf?utm_source=chatgpt.com "Command Reference Guide"
[6]: https://support.keenetic.com/explorer/kn-1613/en/34928-using-public-dns-servers.html?utm_source=chatgpt.com "Using public DNS servers"
[7]: https://wiki.metacubex.one/en/config/rules/?utm_source=chatgpt.com "Route Rules - mihomo docs"
[8]: https://forum.keenetic.ru/topic/17351-%D0%BD%D0%B0%D1%81%D1%82%D1%80%D0%BE%D0%B9%D0%BA%D0%B0-proxy-%D1%82%D0%BE%D0%BB%D1%8C%D0%BA%D0%BE-%D0%B4%D0%BB%D1%8F-%D0%BE%D0%BF%D1%80%D0%B5%D0%B4%D0%B5%D0%BB%D1%91%D0%BD%D0%BD%D1%8B%D1%85-%D1%81%D0%B0%D0%B9%D1%82%D0%BE%D0%B2/?utm_source=chatgpt.com "Настройка Proxy только для определённых сайтов - Вопросы по сборке и настройке Opkg - Keenetic Community"
[9]: https://wiki.metacubex.one/en/config/dns/?utm_source=chatgpt.com "DNS configuration - mihomo docs"
[10]: https://support.keenetic.com/challenger/kn-3910/en/22961-additional-dns-servers.html?utm_source=chatgpt.com "Additional DNS servers"
