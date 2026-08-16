Да. И тут лучше **не смешивать в одну кучу «VPN», «прокси», «транспорт» и «маскировку»**, потому что именно из-за этого обычно и возникает спор «полноценный / неполноценный».

Если сделать нормальную карту технологий, получается примерно так.

### 1. L2 — VPN, которые работают на канальном уровне

Это уже не просто IP-маршрутизация, а туннелирование **кадров L2 Ethernet**:

* **PPTP** — L2TP-подобная старая схема, исторически использовалась для VPN; сейчас криптографически устарела.
* **L2TP** — Layer 2 Tunneling Protocol.
* **L2TP/IPsec** — очень распространённая связка L2TP + IPsec.
* **PPTP** — отдельный старый вариант.
* **Ethernet over GRE / EoIP** — перенос Ethernet через туннель.
* **VXLAN** — L2-over-L3, используется прежде всего в сетевой инфраструктуре.
* **GRETAP** — Ethernet через GRE.
* **OpenVPN TAP** — может создавать L2 Ethernet-туннель.
* **SoftEther VPN** — может работать в режимах, позволяющих передавать L2-трафик.
* **EVPN/VXLAN** — уже скорее датацентровая инфраструктура, а не пользовательский VPN.

То есть **да, L2 VPN существуют**, и L2TP исторически именно отсюда.

---

### 2. L3 — IP VPN

А вот здесь уже туннелируется **IP-трафик**, то есть Layer 3.

Классические:

* **IPsec**

  * IKEv1/IKEv2
  * ESP
  * AH
* **WireGuard**
* **OpenVPN TUN**
* **SSTP**
* **GRE**
* **IP-in-IP**
* **6in4 / 6to4**
* **DMVPN**
* **VXLAN** — технически это L2 over L3, поэтому его нельзя просто поставить рядом с WireGuard как обычный L3 VPN.
* **AmneziaWG** — модифицированный WireGuard, то есть по сути тот же класс L3 VPN.
* **Cisco AnyConnect / SSL VPN**
* **Cisco IPsec VPN**
* **FortiGate IPsec/SSL VPN**
* **MPLS L3VPN** — уже операторская технология.
* **OpenConnect** — клиент для ряда SSL-VPN, в зависимости от сервера.

И вот сюда уже нормально попадают **WireGuard, OpenVPN TUN, IPsec** и т. д.

---

## 3. А вот прокси — это совершенно другая категория

И тут список уже очень большой.

### Классические прокси

Самые «настоящие» в привычном понимании:

* **HTTP proxy**
* **HTTPS proxy**
* **SOCKS4**
* **SOCKS4a**
* **SOCKS5**
* **SOCKS5h**
* **HTTP CONNECT**
* **FTP proxy**
* **DNS proxy**
* **SMTP proxy** и специализированные application proxy

Это буквально классический смысл слова **proxy**: клиент говорит с прокси, а прокси говорит с конечным сервером.

---

# 4. Современные прокси/туннельные протоколы

А вот сюда попадает то, с чем ты сейчас работаешь в Mihomo/Xray/sing-box.

### V2Ray/Xray-семейство

* **VMess**
* **VLESS**
* **Trojan**
* **Shadowsocks**
* **Shadowsocks 2022**
* **Xray VLESS + REALITY**
* **VLESS + TLS**
* **VLESS + XTLS/Vision**

Причём важный момент: **REALITY, TLS, Vision, WebSocket, gRPC, XHTTP — это не отдельные прокси-протоколы в том же смысле, что VLESS.**

Например:

**VLESS + REALITY + XHTTP**

это комбинация:

> протокол → VLESS
> транспорт → XHTTP
> криптография/маскировка → REALITY

Xray официально разделяет протокол и транспорт именно таким образом. ([XTLS][1])

---

### QUIC/UDP-направление

* **Hysteria**
* **Hysteria 2 / HY2**
* **TUIC**
* **QUIC-based различные реализации**
* **Juicity**

Hysteria2 и TUIC — это уже совершенно другой подход относительно VLESS/TCP. Они ориентированы на QUIC/UDP. ([2clash.com.cn][2])

---

### Другие современные прокси

И вот здесь начинается тот самый зоопарк, который ты вспомнил:

* **NaiveProxy**
* **Mieru**
* **AnyTLS**
* **ShadowTLS**
* **ShadowSocks**
* **Snell**
* **SSH**
* **MTProto**
* **MASQUE**
* **TrustTunnel**
* **ShadowQUIC**
* **Sudoku**
* **GOST**
* **Tailscale** — это уже скорее mesh/VPN-система, а не просто прокси
* **Tor**
* **obfs4** — транспорт/обфускация, а не самостоятельный VPN
* **Meek** — транспорт/обфускация
* **Snowflake** — транспортная система Tor

Современный sing-box, например, поддерживает VLESS, VMess, Shadowsocks, Trojan, Hysteria/Hysteria2, TUIC, AnyTLS, SSH и SOCKS/HTTP, а в расширенных сборках встречаются ещё Mieru, MASQUE, TrustTunnel и другие. ([DeepWiki][3])

---

# 5. И ещё отдельная категория — overlay / mesh VPN

Тут уже:

* **Tailscale**
* **Headscale**
* **ZeroTier**
* **Nebula**
* **NetBird**
* **Netmaker**
* **Innernet**
* **Yggdrasil**

Они создают виртуальную сеть между узлами. Причём внутри могут использовать WireGuard или другие механизмы.

---

# А теперь самое интересное — почему спор про VLESS возник

Ты совершенно правильно сказал:

> **VLESS — прокси L7**

Но я бы немного поправил формулировку: **не стоит говорить, что VLESS буквально «L7-прокси» в строгом OSI-смысле**.

Потому что VLESS — это **протокол проксирования/туннелирования**, а не HTTP-прокси уровня приложения в классическом понимании.

И вот поэтому получается такая картина:

| Технология   | Что это по сути              |
| ------------ | ---------------------------- |
| SOCKS5       | классический прокси          |
| HTTP CONNECT | классический прокси          |
| Shadowsocks  | прокси/туннель               |
| VMess        | прокси/туннель               |
| VLESS        | прокси/туннель               |
| Trojan       | прокси/туннель               |
| Hysteria 2   | прокси/туннель поверх QUIC   |
| TUIC         | прокси/туннель поверх QUIC   |
| NaiveProxy   | прокси                       |
| Mieru        | прокси                       |
| AnyTLS       | прокси/туннельный протокол   |
| MTProto      | прокси-протокол Telegram     |
| SSH          | универсальный туннель/прокси |
| WireGuard    | **L3 VPN**                   |
| OpenVPN TUN  | **L3 VPN**                   |
| IPsec        | **L3 VPN**                   |
| L2TP         | **L2 tunneling**             |
| PPTP         | **L2 tunneling**             |
| OpenVPN TAP  | **L2 VPN**                   |
| GRE          | туннель L3                   |
| VXLAN        | **L2 over L3**               |

И вот **VLESS не становится VPN от того, что его запустили через TUN**.

Происходит другое:

**VLESS → прокси-протокол → TUN-интерфейс → система видит виртуальный IP-интерфейс → весь трафик приложений можно отправлять через VLESS.**

Поэтому снаружи пользователь получает **поведение, очень похожее на VPN**, но внутри это всё равно прокси-цепочка.

И наоборот:

**WireGuard → настоящий L3 VPN → IP-пакеты идут через зашифрованный туннель.**

---

### А твой список из Mihomo

Вот это:

> VLESS, VMess, Trojan, SS, HY2, TUIC, MASQUE, Mieru, TT, WG (.conf/.awg), HTTP(S) subscriptions

вообще особенно показательный.

Там у тебя **не все пункты одного уровня**:

* VLESS — прокси-протокол
* VMess — прокси-протокол
* Trojan — прокси-протокол
* SS — прокси-протокол
* HY2 — прокси/туннельный протокол
* TUIC — прокси/туннельный протокол
* Mieru — прокси-протокол
* MASQUE — **протокол туннелирования поверх HTTP/3**
* TT (TrustTunnel) — туннельный протокол
* WG — **настоящий L3 VPN**
* `.conf/.awg` — вообще **формат конфигурации**, а не протокол
* HTTP(S) subscription — **формат доставки конфигурации**, вообще не протокол передачи трафика.

То есть если человеку хочется сказать **«VLESS — неполноценный прокси»**, я бы попросил его сначала определить, что он понимает под «полноценным». Потому что в технической классификации у него тогда придётся объяснить, чем VLESS «неполноценнее» VMess, Trojan, Hysteria2, Mieru или того же Shadowsocks.

А **SOCKS5 и VLESS — просто прокси разных поколений и совершенно разной архитектуры**. Нельзя сказать, что один «настоящий», а второй «ненастоящий». ([github.com][4])

[1]: https://xtls.github.io/en/config/transport.html?utm_source=chatgpt.com "Transport Configuration | Project X"
[2]: https://2clash.com.cn/clash-proxy-protocols-comparison/?utm_source=chatgpt.com "Clash 代理协议全面对比：SS/VLESS/Trojan/VMess/Hysteria2/TUIC – 我的Clash"
[3]: https://deepwiki.com/SagerNet/sing-box/4.2-proxy-protocol-implementations?utm_source=chatgpt.com "Proxy Protocol Implementations | SagerNet/sing-box | DeepWiki"
[4]: https://github.com/cfal/shoes?utm_source=chatgpt.com "GitHub - cfal/shoes: A multi-protocol proxy server written in Rust (HTTP, SOCKS5, Vmess, Vless, Shadowsocks, Trojan, Snell, Hysteria2, TUIC v5, AnyTLS, Naiveproxy, XTLS) · GitHub"
