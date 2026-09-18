# DNS

AdGuard Home, шифрованный DNS (DoT/DoH/DoQ), перехват DNS ТСПУ,
самостоятельный хостинг резолверов.

## AdGuard Home

- **Вики Internet-Helper по настройке AdGuard Home (RU)** —
  <https://github.com/Internet-Helper/AdGuard-Home/wiki> — Source: #35.
- **Оптимизация AdGuard Home на роутере** (перенос статистики/журнала с
  флешки) — Source: #94 (форвард Bird4Static): отключение записи журналов
  на накопитель. **Research**.
- **Связка с Keenetic**: `opkg dns-override` + upstream AdGuardHome
  `127.0.0.1:3553` + добавление политики в «Приоритетах подключений» —
  Source: #96. **Observed** (автор канала: «сам проверил»).

## Шифрованный DNS на Keenetic

- **Импорт DoT Google + Cloudflare в Keenetic** (ndmc `dns-proxy tls
  upstream … sni …`) — Source: #181 (форвард Ponywka), #1146 (компактная
  версия команды).
- **Проверка DoT/DoH/DoQ/DNSCrypt утилитой `q`** (`q A @tls://9.9.9.9 ya.ru`)
  — Source: #1158.
- **Конфиг dns-proxy с rebind-protect/intercept + Quad9** — Source: #1159.
- Самостоятельный DoH на VPS: гайд man smart-home — Source: #1174;
  [TheGreatAzizi/Secure-DNS-over-HTTPS-Cloudflare-Worker] — Source: #1198.

## Публичные резолверы, упомянутые каналом

| Ресурс | Контекст | Source |
|---|---|---|
| `dns.privatenode.ru` (DoH/DoT/DoQ) | «AdGuard и NextDNS попали под блокировку» — альтернатива | #466 |
| [paulmillr/encrypted-dns](https://github.com/paulmillr/encrypted-dns) | Список/конфиги публичных шифрованных DNS | #602 |
| [pymumu/smartdns](https://github.com/pymumu/smartdns) | Мульти-апстрим DNS-прокси | #1187 |
| [Internet-Helper/GeoHideDNS](https://github.com/Internet-Helper/GeoHideDNS) | hosts-набор против GeoIP-подмены | #1228 |
| [ward-sentry/DoT_n_DoH-Checker](https://github.com/ward-sentry/DoT_n_DoH-Checker) | Проверка доступности DoT/DoH | #959 |

## Новости: давление на DNS (Historical + Research)

- 2026-08-28 — «На ТСПУ начали перехватывать открытые DNS-запросы к
  1.1.1.1, 8.8.8.8»; неделей раньше «начали давить DoH» — Source: #1184.
- 2026-08-27 — предупреждение о DNS Cloudflare: при коннекте на RU PoP
  выход всё равно даёт msk-ix — Source: #1177. **Research** (наблюдение
  автора форварда).
- GeoIP-poisoning сервисами Google для VPS (угон локации, 8.8.8.8 как
  фактор) — Source: #1220. Связано с [vps-server.md](vps-server.md).
- Смена Firefox 155 домена проверки captive-портала — Source: #1211.

Диагностика DNS (dnsleaktest, dnscheck.tools и т.п.) —
[diagnostics.md](diagnostics.md).
