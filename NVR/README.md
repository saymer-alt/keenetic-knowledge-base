# Keenetic NVR + Streaming: Легковесный видеорегистратор и вещатель

Набор скриптов для превращения роутера Keenetic (с установленной средой Entware) в полноценный сетевой видеорегистратор (NVR) и/или HTTP-вещатель для IP-камер. Тестировалось на Keenetic 1012 (MediaTek Filogic) — нагрузка на CPU при записи трех потоков H.265 (2K) практически нулевая благодаря прямому копированию потока (`-c copy`).

## Возможности

### Режим NVR (Запись архива)
* **Захват RTSP-потока** без транскодирования (Stream Copy).
* **Сегментация** видео на отрезки по 15 минут.
* **Умный Watchdog:** автоматический переподключение при обрывах связи, перезагрузке камеры, зависании процесса или отвале USB-диска.
* **PID-менеджмент:** корректный `stop` через PID-файлы — не убивает чужие процессы `ffmpeg`.
* **Кольцевой буфер:** автоматическое удаление старых записей (старше 72 часов) через Cron.
* **Автозапуск:** старт записи при включении/перезагрузке роутера.

### Режим Streaming (Вещание на ТВ/приставку)
* **HTTP MPEG-TS** потоки для IPTV-приставок (например, Selenga) или VLC.
* **Видео без нагрузки на CPU** (`-c:v copy`), звук транскодируется в AAC (`-c:a aac`).
* **Встроенный HTTP-сервер** `ffmpeg -listen 1` — минимум ресурсов, максимум надёжности.
* **Авто-перезапуск** при отключении клиента (телевизора).

## Требования
1. Роутер Keenetic с USB-накопителем (для NVR рекомендуется EXT4).
2. Установленная среда Entware на USB-накопителе.
3. Пакеты: `ffmpeg`, `cron` (для NVR).
   ```sh
   opkg update
   opkg install ffmpeg cron
   ```

---

## Часть 1. NVR — Запись архива на диск

### 1. Подготовка папок

Замените `/tmp/mnt/YOUR_USB_DRIVE` на ваш путь к диску.

```sh
mkdir -p /tmp/mnt/YOUR_USB_DRIVE/cctv/cam101
mkdir -p /tmp/mnt/YOUR_USB_DRIVE/cctv/cam201
mkdir -p /tmp/mnt/YOUR_USB_DRIVE/cctv/cam301
```

### 2. Скрипт записи (`record_cctv.sh`)

Сохраните в `/tmp/mnt/YOUR_USB_DRIVE/cctv/record_cctv.sh` и отредактируйте переменные.

```bash
#!/bin/sh

# === НАСТРОЙКИ ===
BASE_DIR="/tmp/mnt/YOUR_USB_DRIVE/cctv"
RTSP_USER="YOUR_USERNAME"
RTSP_PASS="YOUR_PASSWORD"
RTSP_IP="192.168.1.XXX"

# Защита: если диск отвалился — не пишем во внутреннюю память
if [ ! -d "$BASE_DIR" ]; then
    echo "ERROR: Disk not mounted!" >&2
    exit 1
fi

# Защита от двойного запуска
if [ -f /tmp/cctv_is_running ]; then
    echo "CCTV already running."
    exit 0
fi

touch /tmp/cctv_is_running

start_recording() {
    CAM_ID=$1
    DIR="$BASE_DIR/cam$CAM_ID"
    mkdir -p "$DIR"
    URL="rtsp://$RTSP_USER:$RTSP_PASS@$RTSP_IP:554/Streaming/Channels/$CAM_ID"
    
    (
        while [ -f /tmp/cctv_is_running ]; do
            /opt/bin/ffmpeg -hide_banner -loglevel error \
                -rtsp_transport tcp -i "$URL" \
                -c copy -f segment -segment_time 900 \
                -strftime 1 -reset_timestamps 1 \
                "$DIR/cam${CAM_ID}_%Y-%m-%d_%H-%M-%S.mkv" > /dev/null 2>&1 &
            
            PID=$!
            echo $PID > /tmp/cctv_cam${CAM_ID}.pid
            
            LASTFILE=""
            # Если файл не растёт 2+ минуты — убиваем зависший ffmpeg
            while kill -0 $PID 2>/dev/null; do
                CURRENT=$(ls -t "$DIR"/cam${CAM_ID}_*.mkv 2>/dev/null | head -n 1)
                if [ -n "$CURRENT" ] && [ "$CURRENT" != "$LASTFILE" ]; then
                    LASTFILE="$CURRENT"
                elif [ -n "$LASTFILE" ]; then
                    NOW=$(date +%s)
                    MTIME=$(stat -c %Y "$LASTFILE" 2>/dev/null)
                    if [ -n "$MTIME" ] && [ $((NOW - MTIME)) -gt 120 ]; then
                        kill $PID 2>/dev/null
                        break
                    fi
                fi
                sleep 30
            done
            
            wait $PID 2>/dev/null
            rm -f /tmp/cctv_cam${CAM_ID}.pid
            sleep 5
        done
    ) > /dev/null 2>&1 &
}

start_recording "101"
start_recording "201"
start_recording "301"

echo "CCTV recording started in watchdog mode."
```

### 3. Скрипт очистки (`cleanup_cctv.sh`)

```bash
#!/bin/sh
find /tmp/mnt/YOUR_USB_DRIVE/cctv/ -name "*.mkv" -type f -mtime +3 -delete
```

Если `find` не поддерживает `-delete`, замените последнее слово на:
```bash
-exec rm -f {} +
```

### 4. Скрипт автозагрузки (`S99cctv`)

Сохраните в `/opt/etc/init.d/S99cctv`.

```bash
#!/bin/sh

SCRIPT_PATH="/tmp/mnt/YOUR_USB_DRIVE/cctv/record_cctv.sh"

case "$1" in
    start)
        if [ -f /tmp/cctv_is_running ]; then
            echo "CCTV already running."
            exit 0
        fi
        echo "Starting CCTV recording..."
        sh "$SCRIPT_PATH"
        ;;
    stop)
        echo "Stopping CCTV recording..."
        rm -f /tmp/cctv_is_running
        
        # Мягко завершаем только наши процессы
        for pidfile in /tmp/cctv_cam*.pid; do
            [ -f "$pidfile" ] || continue
            PID=$(cat "$pidfile")
            kill -TERM "$PID" 2>/dev/null
        done
        
        sleep 5
        
        # Добиваем, если кто-то завис
        for pidfile in /tmp/cctv_cam*.pid; do
            [ -f "$pidfile" ] || continue
            PID=$(cat "$pidfile")
            kill -0 "$PID" 2>/dev/null && kill -9 "$PID" 2>/dev/null
            rm -f "$pidfile"
        done
        ;;
    restart)
        $0 stop
        sleep 2
        $0 start
        ;;
    *)
        echo "Usage: $0 {start|stop|restart}"
        exit 1
        ;;
esac
```

### 5. Настройка Cron

```sh
nano /opt/etc/crontab
```

Добавьте:
```text
0 * * * * root sh /tmp/mnt/YOUR_USB_DRIVE/cctv/cleanup_cctv.sh
```

Перезапустите:
```sh
/opt/etc/init.d/S10cron restart
```

### 6. Права и запуск

```sh
chmod +x /tmp/mnt/YOUR_USB_DRIVE/cctv/record_cctv.sh
chmod +x /tmp/mnt/YOUR_USB_DRIVE/cctv/cleanup_cctv.sh
chmod +x /opt/etc/init.d/S99cctv

/opt/etc/init.d/S99cctv start
```

---

## Часть 2. Streaming — Вещание на ТВ/приставку

Для второго (или третьего) роутера, который отдаёт живой эфир по HTTP.

### Скрипт вещания (`S99stream`)

Сохраните в `/opt/etc/init.d/S99stream`.

```bash
#!/bin/sh

RTSP_USER="YOUR_USERNAME"
RTSP_PASS="YOUR_PASSWORD"
RTSP_IP="192.168.1.XXX"
SCRIPT_NAME="stream"

start_stream() {
    CAM_ID=$1
    PORT=$2
    URL="rtsp://$RTSP_USER:$RTSP_PASS@$RTSP_IP:554/Streaming/Channels/$CAM_ID"
    
    (
        while [ -f /tmp/${SCRIPT_NAME}_is_running ]; do
            # Чистим мёртвые PID
            if [ -f /tmp/${SCRIPT_NAME}_cam${CAM_ID}.pid ]; then
                OLD_PID=$(cat /tmp/${SCRIPT_NAME}_cam${CAM_ID}.pid)
                kill -0 $OLD_PID 2>/dev/null || rm -f /tmp/${SCRIPT_NAME}_cam${CAM_ID}.pid
            fi
            
            /opt/bin/ffmpeg -hide_banner -loglevel error \
                -rtsp_transport tcp -i "$URL" \
                -map 0:v:0 -map 0:a? \
                -c:v copy -c:a aac -b:a 64k \
                -f mpegts -listen 1 \
                "http://0.0.0.0:$PORT/stream$CAM_ID.ts" > /dev/null 2>&1 &
            
            PID=$!
            echo $PID > /tmp/${SCRIPT_NAME}_cam${CAM_ID}.pid
            
            wait $PID 2>/dev/null
            rm -f /tmp/${SCRIPT_NAME}_cam${CAM_ID}.pid
            
            sleep 3
        done
    ) > /dev/null 2>&1 &
}

case "$1" in
    start)
        if [ -f /tmp/${SCRIPT_NAME}_is_running ]; then
            echo "Stream already running."
            exit 0
        fi
        echo "Starting CCTV HTTP streams..."
        touch /tmp/${SCRIPT_NAME}_is_running
        start_stream "101" "8999"
        start_stream "201" "9000"
        start_stream "301" "9001"
        echo "Done."
        ;;
    stop)
        echo "Stopping CCTV HTTP streams..."
        rm -f /tmp/${SCRIPT_NAME}_is_running
        
        for pidfile in /tmp/${SCRIPT_NAME}_cam*.pid; do
            [ -f "$pidfile" ] || continue
            PID=$(cat "$pidfile")
            kill -TERM "$PID" 2>/dev/null
        done
        
        sleep 3
        
        for pidfile in /tmp/${SCRIPT_NAME}_cam*.pid; do
            [ -f "$pidfile" ] || continue
            PID=$(cat "$pidfile")
            kill -0 "$PID" 2>/dev/null && kill -9 "$PID" 2>/dev/null
            rm -f "$pidfile"
        done
        ;;
    restart)
        $0 stop
        sleep 2
        $0 start
        ;;
    *)
        echo "Usage: $0 {start|stop|restart}"
        exit 1
        ;;
esac
```

### Запуск

```sh
chmod +x /opt/etc/init.d/S99stream
/opt/etc/init.d/S99stream start
```

### URL для плеера/приставки

```
http://IP_РОУТЕРА:8999/stream101.ts
http://IP_РОУТЕРА:9000/stream201.ts
http://IP_РОУТЕРА:9001/stream301.ts
```

---

## Архитектура: разделение труда

| Роутер | Роль | Инструмент |
|---|---|---|
| **Первый** | VPN, доступ извне | — |
| **Второй** | Архив, кольцевой буфер | `ffmpeg` + `segment` |
| **Третий** | Живой эфир на ТВ | `ffmpeg` + `-listen 1` |

Каждый выполняет одну задачу. Никаких `go2rtc`, никаких лишних прослоек. Чистый Linux, чистый `ffmpeg`.

---

## Проверка работы

```sh
# Сколько ffmpeg работает (должно быть 3)
ps | grep ffmpeg | grep -v grep | wc -l

# Сколько записано на диск (для NVR)
du -sh /tmp/mnt/YOUR_USB_DRIVE/cctv/

# Какой последний файл у камеры 101
ls -lt /tmp/mnt/YOUR_USB_DRIVE/cctv/cam101/ | head -n 2

# Открыты ли порты стриминга (для Streaming)
netstat -tlnp | grep -E '8999|9000|9001'
```

---

## Лицензия

MIT. Делайте что хотите, главное — не пишите архив во внутреннюю память роутера. 😄
```

