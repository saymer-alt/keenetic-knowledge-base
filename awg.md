Скажу честно: **ChatGPT выдал абсолютно грамотный и профессиональный code review.** Он увидел те же самые узкие места, о которых мы знаем, и его советы — это классика хорошего тона в системном администрировании. 

Давай разберем его правки и соберем **идеальную финальную инструкцию** для твоих трех серверов:

1. **`ip_forward=1`** — отличное замечание. Docker обычно включает это сам, но прописать это явно в системе — правильный тон, чтобы маршрутизация между интерфейсами точно работала.
2. **Убрать `fwmark 0`** — он прав. Правило `priority 40` (маршрутизация по метке `0x88`) сработает первым, поэтому писать `fwmark 0` для Докера избыточно. Убрали за ненадобностью, так чище.
3. **Привязка к `mihomo.service` в systemd** — **золотой совет**. Если при перезагрузке сервера наш скрипт запустится раньше, чем Mihomo поднимет интерфейс `tun-mihomo`, скрипт упадет с ошибкой. Привязка решает эту проблему.
4. **Проверочные команды** — согласен, добавил их в конец.

Вот **финальный, отполированный рецепт**, который можно смело копировать на оставшиеся серверы (и Debian, и Ubuntu).

---

### Шаг 0. Сбор данных (ОБЯЗАТЕЛЬНО на каждом сервере!)
```bash
docker network inspect amnezia-dns-net --format='{{range .IPAM.Config}}{{.Subnet}}{{end}}'
ip -o -4 route show to default | awk '{print $5}'
```
*Запиши эти значения. Допустим, это `172.29.172.0/24` и `ens3`.*

### Шаг 1. Настройка Mihomo
Убедись, что в конфиге Mihomo включен TUN:
```yaml
tun:
  enable: true
  stack: gvisor
  device: tun-mihomo
  auto-route: false
  auto-detect-interface: true
  inet4-address: 198.18.0.1/30
```
Перезапусти Mihomo (`systemctl restart mihomo` или `docker restart mihomo`).

### Шаг 2. Настройка ядра (sysctl)
Создаем файл с настройками ядра:
```bash
cat << 'EOF' > /etc/sysctl.d/99-amnezia.conf
net.ipv4.ip_forward = 1
net.ipv4.conf.all.rp_filter = 0
net.ipv4.conf.default.rp_filter = 0
EOF
```
Применяем настройки:
```bash
sysctl -p /etc/sysctl.d/99-amnezia.conf
```

### Шаг 3. Скрипт маршрутизации
1. Создаем файл:
```bash
nano /usr/local/sbin/warp-docker-routing.sh
```
2. Вставляем код (не забудь вписать свои данные из Шага 0 в переменные `DOCKER_NETS` и `HOST_IF`):
```bash
#!/bin/sh
set -eu

PROXY_IF="tun-mihomo"
DOCKER_NETS="172.29.172.0/24"  # Впиши подсеть из Шага 0
WG_PORT="51820"                # Порт AWG
TABLE_ID="100"
HOST_IF="ens3"                 # Впиши интерфейс из Шага 0

if ! ip link show "$PROXY_IF" >/dev/null 2>&1; then
    echo "Error: Interface '$PROXY_IF' does not exist. Is Mihomo TUN running?"
    exit 1
fi

# 1. Очистка старых правил
ip rule del fwmark 0x88 lookup main priority 40 2>/dev/null || true
ip rule del from "$DOCKER_NETS" lookup "$TABLE_ID" priority 100 2>/dev/null || true

iptables -t mangle -D PREROUTING -s "$DOCKER_NETS" -p udp --sport "$WG_PORT" -j MARK --set-mark 0x88 2>/dev/null || true
iptables -t nat -D POSTROUTING -o "$PROXY_IF" -j MASQUERADE 2>/dev/null || true
iptables -D FORWARD -s "$DOCKER_NETS" -j ACCEPT 2>/dev/null || true
iptables -D FORWARD -d "$DOCKER_NETS" -j ACCEPT 2>/dev/null || true

# 2. Настройка маршрутов
ip route replace default dev "$PROXY_IF" table "$TABLE_ID"
ip rule add from "$DOCKER_NETS" lookup "$TABLE_ID" priority 100
ip rule add fwmark 0x88 lookup main priority 40

# 3. Маркируем ОТВЕТЫ контейнера (порт 51820) мимо прокси
iptables -t mangle -I PREROUTING 1 -s "$DOCKER_NETS" -p udp --sport "$WG_PORT" -j MARK --set-mark 0x88

# 4. Маскарадинг в прокси
iptables -t nat -A POSTROUTING -o "$PROXY_IF" -j MASQUERADE

# 5. АБСОЛЮТНЫЙ ПРИОРИТЕТ ДЛЯ ТРАФИКА КОНТЕЙНЕРА (Обход UFW DROP)
iptables -I FORWARD 1 -s "$DOCKER_NETS" -j ACCEPT
iptables -I FORWARD 2 -d "$DOCKER_NETS" -j ACCEPT
```
*(Сохрани: `Ctrl+O`, `Enter`, `Ctrl+X`)*

3. Делаем исполняемым:
```bash
chmod +x /usr/local/sbin/warp-docker-routing.sh
```

### Шаг 4. Служба Systemd (с привязкой к Mihomo)
1. Создаем файл:
```bash
nano /etc/systemd/system/warp-docker-routing.service
```
2. Вставляем код:
```ini
[Unit]
Description=Route Amnezia Docker traffic through Mihomo TUN
After=network-online.target docker.service mihomo.service
Requires=mihomo.service
Wants=network-online.target docker.service

[Service]
Type=oneshot
ExecStart=/usr/local/sbin/warp-docker-routing.sh
RemainAfterExit=yes

[Install]
WantedBy=multi-user.target
```
*(Сохрани: `Ctrl+O`, `Enter`, `Ctrl+X`)*

3. Запускаем:
```bash
systemctl daemon-reload
systemctl enable --now warp-docker-routing.service
```

### Шаг 5. Проверочные команды (как советовал ChatGPT)
Выполни эти команды. Если вывод совпадает с описанием — всё настроено идеально:
```bash
ip rule
```
*(Должны быть строчки: `40: from all fwmark 0x88 lookup main` и `100: from 172.29.172.0/24 lookup 100`)*

```bash
ip route show table 100
```
*(Должна быть строчка: `default dev tun-mihomo scope link`)*

```bash
iptables -t mangle -L PREROUTING -n -v
```
*(Должно быть правило `udp spt:51820 MARK set 0x88`)*

---
Всё! Инструкция доведена до ума. Можешь смело идти на остальные серверы. С такой конфигурацией оно будет работать как швейцарские часы.
