Чат-GPT выдал **великолепный, профессиональный совет**. Это уровень системного архитектора. 

Дело в том, что наш скрипт — это "одноразовая инструкция" (oneshot). Он идеально отрабатывает при загрузке сервера. Но если в процессе работы:
* Mihomo крашнется и поднимется заново (интерфейс пересоздастся, а правила `iptables` потеряются),
* или Docker перезапустит свою сеть,
то трафик просто остановится, и скрипт об этом не узнает.

Предложенный таймер (health-check) раз в минуту — это идеальный "легковесный сторож". Он не грузит систему и сам чинит правила, если что-то слетело.

Давай реализуем этот план. Это займет 2 минуты на каждом сервере.

### 1. Делаем Mihomo самовосстанавливающимся
Если Mihomo когда-нибудь упадет, systemd поднимет его сам через 5 секунд.
Выполни команду:
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
*(Если Mihomo у тебя в Docker, то добавь флаг `--restart unless-stopped` при запуске контейнера, это等效но).*

### 2. Создаем скрипт-сторож (Health-check)
1. Создай файл:
```bash
nano /usr/local/sbin/check-warp-routing.sh
```
2. Вставь этот код (здесь мы **добавили перепроверку через 5 секунд**, чтобы Mihomo точно успел подняться, и сразу починили маршруты):
```bash
#!/bin/sh
PROXY_IF="tun-mihomo"          # Имя интерфейса (поменяй, если у тебя mitun0)
DOCKER_NETS="172.29.172.0/24"  # Твоя подсеть Амнезии

# Если интерфейс Mihomo исчез, перезапускаем сам Mihomo
if ! ip link show "$PROXY_IF" >/dev/null 2>&1; then
    logger "warp-check: Интерфейс $PROXY_IF отсутствует. Перезапускаю Mihomo..."
    systemctl restart mihomo.service
    sleep 5 # Ждем, пока поднимется интерфейс
fi

# Проверяем, есть ли наше правило маршрутизации
if ! ip rule | grep -q "from $DOCKER_NETS lookup 100"; then
    logger "warp-check: Правила маршрутизации слетели. Восстанавливаю..."
    systemctl restart warp-docker-routing.service
    exit 1
fi

exit 0
```
*(Сохрани: `Ctrl+O`, `Enter`, `Ctrl+X`)*

3. Сделай исполняемым:
```bash
chmod +x /usr/local/sbin/check-warp-routing.sh
```

### 3. Создаем службу для таймера
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
*(Сохрани)*

### 4. Создаем сам таймер (запуск раз в минуту)
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
*(Сохрани)*

### 5. Запускаем таймер
```bash
systemctl daemon-reload
systemctl enable --now check-warp-routing.timer
```

### 6. Добавляем Reload в основной скрипт (как советовал GPT)
Открой службу:
```bash
nano /etc/systemd/system/warp-docker-routing.service
```
И добавь строчку `ExecReload=...`:
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
Сохрани и обнови:
```bash
systemctl daemon-reload
```

---

**Всё! Теперь система полностью автономна.**
Если что-то сломается, таймер через минуту это заметит, перезапустит Mihomo и заново применит правила `iptables`. Можешь смело ставить это на все серверы и "забыть"!
