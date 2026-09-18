# VPS / серверная практика

Hardening, бенчмарки, выбор хостинга, Docker, мониторинг. Пересекается с
VPS-кластером этого репозитория (`amnezia.md`, `awg.md`, `check.md`,
`install.sh`) и [owner-projects.md](owner-projects.md).

## Hardening и первичная настройка

- **UFW для VPN-сервера**: allow ssh + 51820/udp — Source: #151.
- **Полный сетап «от и до»** (самоподписанные сертификаты, SSH на порт 2222,
  ppk-ключи, ufw, fail2ban) — Source: #764–#765, #771–#779, #791–#792
  (серия с setup.sh/final.sh, вложения). **Research**:AI-ассистированные
  гайды автора, не аудированы.
- **Debian 12 hardening для VPN/Proxy** (apt, ufw, fail2ban, swapfile,
  sysctl-оптимизации `vm.swappiness`, dirty_ratio) — Source: #857, #772.
- **fail2ban jail.conf** (полный конфиг с комментариями) — Source: #226.
- **SSH**: доступность порта снаружи (telnet/nc), не закрывать активную
  сессию при правках — Source: #774, #775; массовый SSH-скан соседей по
  Wi-Fi (Bash Days) — #818; [rand1l/ssh-bot](https://github.com/rand1l/ssh-bot)
  — Telegram-бот исполнения команд — #939.
- **Оптимизация ядра под нагрузку** (sysctl) — Source: #772, #778.
- ICMPv6/ICMP tuning (`net.ipv6.icmp.echo_ignore_all` и т.п.) — #163, #164.
- [wrx861/server-shield](https://github.com/wrx861/server-shield),
  [xtclovver/RKNHardering](https://github.com/xtclovver/RKNHardering),
  [Dreaght/rknhardering-ios-module](https://github.com/Dreaght/rknhardering-ios-module) —
  Source: #463, #724, #731.

## Бенчмарки и тесты серверов

- Набор: `bench.tlab.pw`, `ip.check.place`, `sysbench`, storage.umager.ru
  (`ipregion.sh`, `check_inst_ru.sh`, `checker_all_ru`) — Source: #234,
  #516, #744, #1133; [Davoyan/ipregion](https://github.com/Davoyan/ipregion)
  + [vernette/censorcheck](https://github.com/vernette/censorcheck) — #663;
  скрипты Code Lab — #1133.
- **iperf3-серторы РФ** — [itdoginfo/russian-iperf3-servers](https://github.com/itdoginfo/russian-iperf3-servers)
  — Source: #228.
- Яндекс-спидтест CLI — [begugla0/yandexspeedtestcli](https://github.com/begugla0/yandexspeedtestcli)
  — Source: #1115.

## Выбор хостинга (Research — субъективные сводки)

- «Стабильней всех за год: Aeza, Nexus, Vanda, ServHost» — Source: #656
  (форвард Stas).
- Обзоры/рейтинги: sostav.ru топ-10 (#931), Habr сравнение 2026 (#955),
  poiskvps.ru (#675), innon.org 179₽ Германия (#519), ExpessHost
  переписка про ограничения РФ (#919).
- **Индустриальные события**: падение nLighten/Mirhosting и отклики
  хостеров (#899, #900, #901); запрет NL-датацентра на VPN (#943);
  OVH-блокировки и списки подсетей (#457, #472–#474).
- Как выбрать хостера для Amnezia self-hosted (официальный блог) — #954.

## Docker и сервисы

- Чистка старых контейнеров (3 ГБ мусора) — Source: #204.
- docker-compose обслуживание MTProxy-стека (`telemt-stat.sh`, glances,
  watch) — Source: #450, #455, #456.
- [amneziavpn/amnezia-xray-core](https://hub.docker.com/r/amneziavpn/amnezia-xray-core)
  (21 МБ, без ядерных модулей) — Source: #575.
- wg-easy (#242, #479), docker-гайды WARP-роутинга (#1079).
- Мониторинг: [louislam/uptime-kuma](https://github.com/louislam/uptime-kuma)
  (#935), htop/ss/docker stats (#770), proxy-metrics.py (#770).
- «Колхозный» drop-подсетей через iptables raw — Source: #462.

## GeoIP / IP-репутация

- **GeoIP-poisoning сервисами Google** (угон локации VPS из-за 8.8.8.8) —
  Source: #1220; связь с [dns.md](dns.md).
- Хостинги под 16-кБ блокировкой (список ASN с ntc.party) — #457.
- [lord-alfred/ipranges](https://github.com/lord-alfred/ipranges) — #1105;
  geoexport.org — #1005; ASN-подписи
  [asn.web2core.workers.dev](https://asn.web2core.workers.dev) / sw.ext.io —
  #967, #1129, #1001.
