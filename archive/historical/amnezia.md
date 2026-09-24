Вот идеальная, финальная инструкция. Она учитывает абсолютно все нюансы, с которыми мы столкнулись: отключение `rp_filter` (чтобы ядро не убивало пакеты), обход жесткого UFW, предотвращение зацикливания порта AWG и даже автопочинку при сбоях.

Распечатай или сохрани этот текст и выполняй по шагам.

---

### Шаг 0. Сбор данных (ОБЯЗАТЕЛЬНО для этого сервера!)
На каждом сервере подсеть докера, порт AWG и имя сетевого интерфейса могут быть своими. Выполни эти три команды и **запиши ответы**:

1. Узнать подсеть Амнезии:
   ```bash
   docker network inspect amnezia-dns-net --format='{{range .IPAM.Config}}{{.Subnet}}{{end}}'
   ```
   *(Допустим, выдаст `172.29.172.0/24`)*

2. Узнать имя основного сетевого интерфейса:
   ```bash
   ip -o -4 route show to default | awk '{print $5}'
   ```
   *(Допустим, выдаст `ens3`)*

3. Узнать порт AWG:
   ```bash
   docker ps --format "{{.Names}}: {{.Ports}}"
   ```
   *(Найди контейнер `amnezia-awg2` и посмотри порт, например `51820->51820/udp`. Запиши `51820`)*

---

### Шаг 1. Настройка Mihomo
Убедись, что в конфиге Mihomo включен TUN-интерфейс строго с такими параметрами (адрес `198.18.0.1/30` обязателен!):
```yaml
tun:
  enable: true
  stack: gvisor
  device: tun-mihomo
  auto-route: false
  auto-detect-interface: true
  inet4-address: 198.18.0.1/30
```
После этого **обязательно перезапусти Mihomo**:
```bash
systemctl restart mihomo
```
*(Или `docker restart mihomo`, если он в докере).*

---

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

---

### Шаг 3. Скрипт маршрутизации
1. Создаем файл:
```bash
nano /usr/local/sbin/warp-docker-routing.sh
```
2. Вставляем код. **ВНИМАНИЕ: Впиши в переменные сверху те данные, которые получил в Шаге 0!**
```bash
#!/bin/sh
set -eu

# === НАСТРОЙКИ (ОБЯЗАТЕЛЬНО ПРОВЕРЬ ПОД СЕБЯ) ===
PROXY_IF="tun-mihomo"          # Имя TUN-интерфейса в Mihomo
DOCKER_NETS="172.29.172.0/24"  # Впиши подсеть из Шага 0
WG_PORT="51820"                # Впиши порт AWG из Шага 0
TABLE_ID="100"
HOST_IF="ens3"                 # Впиши интерфейс из Шага 0

# 1. ПРИНУДИТЕЛЬНО ОТКЛЮЧАЕМ RP_FILTER (чтобы ядро не убивало асимметричные пакеты)
for i in /proc/sys/net/ipv4/conf/*/rp_filter; do echo 0 > $i; done

if ! ip link show "$PROXY_IF" >/dev/null 2>&1; then
    echo "Error: Interface '$PROXY_IF' does not exist. Is Mihomo TUN running?"
    exit 1
fi

# 2. ОЧИСТКА СТАРЫХ ПРАВИЛ
ip rule del fwmark 0x88 lookup main priority 40 2>/dev/null || true
ip rule del from "$DOCKER_NETS" lookup "$TABLE_ID" priority 100 2>/dev/null || true

iptables -t mangle -D PREROUTING -s "$DOCKER_NETS" -p udp --sport "$WG_PORT" -j MARK --set-mark 0x88 2>/dev/null || true
iptables -t nat -D POSTROUTING -o "$PROXY_IF" -j MASQUERADE 2>/dev/null || true
iptables -D FORWARD -s "$DOCKER_NETS" -j ACCEPT 2>/dev/null || true
iptables -D FORWARD -d "$DOCKER_NETS" -j ACCEPT 2>/dev/null || true

# 3. НАСТРОЙКА МАРШРУТОВ
ip route replace default dev "$PROXY_IF" table "$TABLE_ID"
ip rule add from "$DOCKER_NETS" lookup "$TABLE_ID" priority 100
ip rule add fwmark 0x88 lookup main priority 40

# 4. МАРКИРУЕМ ОТВЕТЫ КОНТЕЙНЕРА (порт AWG) МИМО ПРОКСИ
iptables -t mangle -I PREROUTING 1 -s "$DOCKER_NETS" -p udp --sport "$WG_PORT" -j MARK --set-mark 0x88

# 5. МАСКАРАДИНГ В ПРОКСИ (NAT)
iptables -t nat -A POSTROUTING -o "$PROXY_IF" -j MASQUERADE

# 6. АБСОЛЮТНЫЙ ПРИОРИТЕТ ДЛЯ ТРАФИКА КОНТЕЙНЕРА (Обход UFW DROP)
iptables -I FORWARD 1 -s "$DOCKER_NETS" -j ACCEPT
iptables -I FORWARD 2 -d "$DOCKER_NETS" -j ACCEPT
```
*(Сохрани: `Ctrl+O`, `Enter`, `Ctrl+X`)*

3. Сделай исполняемым:
```bash
chmod +x /usr/local/sbin/warp-docker-routing.sh
```

---

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
ExecReload=/usr/local/sbin/warp-docker-routing.sh

[Install]
WantedBy=multi-user.target
```
*(Сохрани)*

3. Запускаем:
```bash
systemctl daemon-reload
systemctl enable --now warp-docker-routing.service
```

---

### Шаг 5. Автопочинка (Watchdog Timer)
Если Mihomo крашнется или перезапустится, этот таймер через минуту восстановит правила.

1. Делаем Mihomo самовосстанавливающимся:
```bash
mkdir -p /etc/systemd/system/mihomo.service.d
cat << 'EOF' > /etc/systemd/system/mihomo.service.d/override.conf
[Service]
Restart=always
RestartSec=5
EOF
systemctl daemon-reload
systemctl restart mihomo
```

2. Создаем скрипт-сторож:
```bash
nano /usr/local/sbin/check-warp-routing.sh
```
Вставь код (если менял подсеть или имя интерфейса, впиши их сюда тоже):
```bash
#!/bin/sh
PROXY_IF="tun-mihomo"
DOCKER_NETS="172.29.172.0/24"

if ! ip link show "$PROXY_IF" >/dev/null 2>&1; then
    logger "warp-check: Интерфейс $PROXY_IF отсутствует. Перезапускаю Mihomo..."
    systemctl restart mihomo.service
    sleep 5
fi

if ! ip rule | grep -q "from $DOCKER_NETS lookup 100"; then
    logger "warp-check: Правила маршрутизации слетели. Восстанавливаю..."
    systemctl restart warp-docker-routing.service
    exit 1
fi
exit 0
```
Сохрани и сделай исполняемым:
```bash
chmod +x /usr/local/sbin/check-warp-routing.sh
```

3. Создаем службу для таймера:
```bash
nano /etc/systemd/system/check-warp-routing.service
```
Вставь:
```ini
[Unit]
Description=Check WARP Docker routing

[Service]
Type=oneshot
ExecStart=/usr/local/sbin/check-warp-routing.sh
```
Сохрани.

4. Создаем сам таймер:
```bash
nano /etc/systemd/system/check-warp-routing.timer
```
Вставь:
```ini
[Unit]
Description=Periodic WARP routing check

[Timer]
OnBootSec=2min
OnUnitActiveSec=1min

[Install]
WantedBy=timers.target
```
Сохрани.

5. Запускаем таймер:
```bash
systemctl daemon-reload
systemctl enable --now check-warp-routing.timer
```

---

### Шаг 6. ФИНАЛЬНАЯ ПРОВЕРКА
1. Подключайся клиентом Amnezia.
2. Открывай **2ip.ru**. IP должен смениться на IP твоего прокси.
3. Для спокойствия выполни `iptables -t mangle -L PREROUTING -n -v` — счетчик пакетов на правиле `udp spt:<ТВОЙ_ПОРТ> MARK set 0x88` должен расти.

Всё! Сервер настроен железобетонно. Удачи!
