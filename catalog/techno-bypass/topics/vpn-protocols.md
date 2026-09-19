# WireGuard / AmneziaWG / WARP и альтернативные туннели

Протоколы и их обфускация; всё, что не Xray/Mihomo (см.
[xray-vless.md](xray-vless.md), [mihomo.md](mihomo.md)).

## AmneziaWG

- **Обфускация WireGuard-конфига параметрами Jc/Jmin/Jmax (+H1–H4, I1)** —
  Source: #66; рекомендация «Jc 3–5, Jmin 40, Jmax 70» от Amnezia (RU) —
  Source: #198.
- **AmneziaWG 2.0** — анонсы для self-hosted (#657) и в режиме opkgtun
  на Keenetic (#375); конфиг-генератор
  [HereIamGosu/amnezia-config-gen](https://github.com/HereIamGosu/amnezia-config-gen)
  (версия 2.6.0, режим маршрутов) — Source: #1155; билдер
  valokda-amnezia.vercel.app — Source: #1154.
- **AmneziaWG 3.0 на Keenetic** (гайд SecurityLab) — Source: #1191.
- **Ядерный модуль AWG для Keenetic** (hoaxisr; MT7621: −50% CPU против
  awg-go; scp .ko на роутер) — Source: #402–#405. Связано с
  [awg-manager](owner-projects.md).
- **amneziawg-tools** — [amnezia-vpn/amneziawg-tools](https://github.com/amnezia-vpn/amneziawg-tools)
  (✓ TB-04: активен) — Source: #1038. Upstream-реализация протокола:
  [MetaCubeX/amneziawg-go](https://github.com/MetaCubeX/amneziawg-go) (найден
  при верификации TB-04).
- **AWG-Easy** (панель): [gennadykataev/awg-easy](https://github.com/gennadykataev/awg-easy)
  (#149), AWG-Easy 3 (Habr, #1169),
  [w0rng/amnezia-wg-easy](https://github.com/w0rng/amnezia-wg-easy) в
  docker-compose (#1092; **Low activity, TB-04**: без push с 2024-09),
  [PRVTPRO/Amnezia-Web-Panel](https://github.com/PRVTPRO/Amnezia-Web-Panel)
  (#1168),
  [Vadim-Khristenko/AmneziaWG-Architect](https://github.com/Vadim-Khristenko/AmneziaWG-Architect)
  (#684, #685).
- **Разбор «джанка» AmneziaWG против DPI** (мимикрия новых протоколов
  амнезии) — Source: #1188 (форвард Night Specter).
- **ProtonVPN → AmneziaWG**: конвертер
  <https://protonvpn-converter.github.io/> (WireGuard .conf → AWG,
  генерация i1 для AWG 1.5, «Без мусора») — Source: #1083, #651, #1180;
  генератор с нуля <https://proton-generator.github.io/> — #1180.
  **Observed** (форвард: «долгое время отлично работает»).

## WireGuard и WARP

- [ViRb3/wgcf](https://github.com/ViRb3/wgcf) — генерация WARP-конфига —
  Source: #441.
- **WARP-генераторы**: cybportal.vercel.app, warp-generator.github.io,
  warp-gen.vercel.app, ptechgithub (#634),
  [nellimonix/warp-config-generator-vercel](https://github.com/nellimonix/warp-config-generator-vercel)
  (#1136); сканер endpoints
  [bia-pain-bache/BPB-Warp-Scanner](https://github.com/bia-pain-bache/BPB-Warp-Scanner)
  (#986), список endpoints
  [TheyCallMeSecond/WARP-Endpoint-IP](https://github.com/TheyCallMeSecond/WARP-Endpoint-IP)
  (#985); обзор альтернативных зеркал/эндпоинтов WARP (февраль 2026) —
  #401.
- **warp-relay** — [openwarpkit/warp-relay](https://github.com/openwarpkit/warp-relay)
  (#726, #734, #891), [bekirovtimur/warp-relay](https://github.com/bekirovtimur/warp-relay)
  (#487).
- [distillium/warp-native](https://github.com/distillium/warp-native) —
  нативный WARP + скрипт маршрутизации Docker-трафика через WARP
  (`warp-docker-routing.sh` + systemd unit + wg-easy) — Source: #1079
  (форвард D.). **Research**: скрипт родственен материалам
  [vps-server.md](vps-server.md) и VPS-кластеру этого репозитория.
- WireGuard: ping-check профили на Keenetic — #315, #1210;
  извлечение приватного ключа из памяти роутера (вопрос без ответа) — #864.
- [wiresock.net — WireSock Secure Connect](https://www.wiresock.net/wiresock-secure-connect/download) —
  split tunnel + AWG2 для Windows (✓ TB-04: v3.6.1.1 stable) — Source: #504,
  #438; habr-гайд — #1077;
  [wiresock/amneziawg-install](https://github.com/wiresock/amneziawg-install) —
  #1167; [wiresock/proxifyre](https://github.com/wiresock/proxifyre) — #239.
- Android: [WireGuard Auto-Tunnel](https://play.google.com/store/apps/details?id=com.zaneschepke.wireguardautotunnel)
  — Source: #468.

## Альтернативные туннели и стелс-протоколы

| Ресурс | Контекст | Source |
|---|---|---|
| Hysteria2 (`get.hy2.sh`) | Установка hy2-сервера + гайд по VPS | #764, #765 |
| mieru (mita) | «Максимально скрытный сервер», инструкция с диапазоном портов | #776–#778, #1128 |
| DNSTT (туннель поверх DNS) | [TrackLine/dnstt-install](https://github.com/TrackLine/dnstt-install), приложение dnstt_xyz, запуск через HTTP Injector | #296, #297, #343, #515 |
| [Snawoot/opera-proxy](https://github.com/Snawoot/opera-proxy) | «Халявный VPN от Opera» через Proxy0 на Keenetic | #183, #1231 |
| MASQUE | Хабр-реализация + эксперименты владельца | #285, см. [mihomo.md](mihomo.md) |
| [Verity-Freedom/Tor-Portable](https://github.com/Verity-Freedom/Tor-Portable) | Портативный Tor | #210 |
| [anonvector/SlipNet](https://github.com/anonvector/SlipNet) | — | #571 |
| [ZeroTworu/anet](https://github.com/ZeroTworu/anet) | Альтернативный стек туннелей на Rust (ANet, MIT) | #410, #418 |
| TrustTunnel (AdGuard VPN) | Открытый протокол; скрипт для Keenetic (форум #27375) | #334, #412 |
| OpenVPN 2.7 производительность | Новость | #433 |
| [heiher/hev-socks5-tunnel](https://github.com/heiher/hev-socks5-tunnel) | SOCKS5→TUN | #289 |
| [KillTheCensorship/Turnel](https://github.com/KillTheCensorship/Turnel), [MaxTunnel](https://github.com/KillTheCensorship/MaxTunnel) | Туннели поверх TURN/прочее | #340, #341 |
| [nebesniy/easy-vk-tunnel](https://github.com/nebesniy/easy-vk-tunnel) | Туннель через звонилки ВК (dial-up 2.0); watchdog, авто-замена домена | #145, #158, #165 |
| vk-turn-proxy семейство | [cacggghp](https://github.com/cacggghp/vk-turn-proxy) (#393, #573, #687, #706), [kiper292](https://github.com/kiper292/vk-turn-proxy) (#671), [SpaceNeuroX/android](https://github.com/SpaceNeuroX/proxy-turn-vk-android) (#957), [kulikov0/whitelist-bypass](https://github.com/kulikov0/whitelist-bypass) (#645) | см. id |
| Reticulum / Meshtastic | [reticulum.network](https://reticulum.network), [liamcottle/reticulum-meshchat](https://github.com/liamcottle/reticulum-meshchat) (#370); Meshtastic + Hidden Lake (#927); резервное управление дачей (#829) | #370, #927, #829 |
| GNUnet 0.25 | Новость | #138 |
| [chatmail/relay](https://github.com/chatmail/relay) | chatmail-ретлей для Delta Chat | #827 |

## Клиенты

- Обзор клиентов (Nekoray → Clash Meta → sing-box GUI/Hiddify) — Source: #120.
- Hiddify / Happ / Karing (#293, #105); ускорение теста пинга в Happ — #624.
- [v2rayA/v2rayA](https://github.com/v2rayA/v2rayA) — #513.
- FoxyProxy: RegExp-наборы для YouTube/Gemini/Claude (#413, #896, #992),
  конфиг-вложение (#1072). Браузерные прокси-расширения — также
  [diagnostics.md](diagnostics.md).
