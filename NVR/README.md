# Keenetic NVR: Легковесный видеорегистратор на базе роутера

Набор скриптов для превращения роутера Keenetic (с установленной средой Entware) в полноценный сетевой видеорегистратор (NVR) для IP-камер. Тестировалось на Keenetic 1012 (MediaTek Filogic) — нагрузка на CPU при записи трех потоков H.265 (2K) практически нулевая благодаря прямому копированию потока (`-c copy`).

## Возможности
* **Захват RTSP-потока** без транскодирования (Stream Copy).
* **Сегментация** видео на отрезки по 15 минут.
* **Watchdog (Сторожевой пес):** автоматический переподключение к камере при обрывах связи, перезагрузке камеры или падении процесса.
* **Кольцевой буфер:** автоматическое удаление старых записей (например, старше 72 часов) через Cron.
* **Автозапуск:** старт записи при включении/перезагрузке роутера.

## Требования
1. Роутер Keenetic с USB-накопителем (рекомендуется файловая система EXT4).
2. Установленная среда Entware на USB-накопителе.
3. Пакеты: `ffmpeg`, `cron`.
   ```sh
   opkg update
   opkg install ffmpeg cron



## Настройка

### 1. Подготовка папок

Создайте структуру директорий на вашем жестком диске. Замените `/tmp/mnt/YOUR_USB_DRIVE` на ваш путь к диску.

```sh
mkdir -p /tmp/mnt/YOUR_USB_DRIVE/cctv/cam101
mkdir -p /tmp/mnt/YOUR_USB_DRIVE/cctv/cam201
mkdir -p /tmp/mnt/YOUR_USB_DRIVE/cctv/cam301

```

### 2. Скрипт записи (Watchdog + FFmpeg)

Сохраните скрипт `record_cctv.sh` в папку `/tmp/mnt/YOUR_USB_DRIVE/cctv/` и сделайте его исполняемым.
**Не забудьте отредактировать переменные логина, пароля, IP-адреса и пути к вашему диску внутри скрипта.**

### 3. Скрипт очистки (Кольцевой буфер)

Сохраните скрипт `cleanup_cctv.sh` в ту же папку и сделайте исполняемым. Он удаляет файлы старше 3 дней.

```sh
chmod +x /tmp/mnt/YOUR_USB_DRIVE/cctv/cleanup_cctv.sh

```

### 4. Настройка Cron

Добавьте задачу в планировщик, чтобы очистка запускалась каждый час:

```sh
nano /opt/etc/crontab

```

Добавьте строку:

```text
0 * * * * root sh /tmp/mnt/YOUR_USB_DRIVE/cctv/cleanup_cctv.sh

```

Перезапустите Cron: `/opt/etc/init.d/S10cron restart`

### 5. Автозагрузка и управление

Скопируйте скрипт `S99cctv` в директорию `/opt/etc/init.d/` и выдайте права:

```sh
chmod +x /opt/etc/init.d/S99cctv

```

Теперь запись будет стартовать вместе с роутером.
Ручное управление:

* `/opt/etc/init.d/S99cctv start` — запустить
* `/opt/etc/init.d/S99cctv stop` — остановить
* `/opt/etc/init.d/S99cctv restart` — перезапустить

```

---

### Файл 2: `record_cctv.sh` (Очищенный от паролей)

```bash
#!/bin/sh

# НАСТРОЙКИ (Укажите ваши данные)
BASE_DIR="/tmp/mnt/YOUR_USB_DRIVE/cctv"
RTSP_USER="YOUR_USERNAME"
RTSP_PASS="YOUR_PASSWORD"
RTSP_IP="192.168.1.XXX"

# Создаем "флаг", разрешающий работу цикла
touch /tmp/cctv_is_running

start_recording() {
    CAM_ID=$1
    DIR="$BASE_DIR/cam$CAM_ID"
    URL="rtsp://$RTSP_USER:$RTSP_PASS@$RTSP_IP:554/Streaming/Channels/$CAM_ID"
    
    (
        while [ -f /tmp/cctv_is_running ]; do
            echo "Starting record for Camera $CAM_ID..."
            
            # Захват потока, сегментация по 900 сек (15 мин)
            /opt/bin/ffmpeg -hide_banner -loglevel error \
                -rtsp_transport tcp -i "$URL" \
                -c copy -f segment -segment_time 900 \
                -strftime 1 -reset_timestamps 1 \
                "$DIR/cam${CAM_ID}_%Y-%m-%d_%H-%M-%S.mkv" > /dev/null 2>&1
            
            # Защита от спама процессора при падении потока
            sleep 10
        done
    ) &
}

# Добавьте или удалите вызовы функций в зависимости от количества камер
start_recording "101"
start_recording "201"
start_recording "301"

echo "CCTV recording started in watchdog mode (auto-restart)."

```

---

### Файл 3: `cleanup_cctv.sh` (Скрипт очистки)

```bash
#!/bin/sh

# Укажите ваш путь к диску. 
# Параметр +3 означает удаление файлов старше 3 суток (72 часа).
find /tmp/mnt/YOUR_USB_DRIVE/cctv/ -name "*.mkv" -type f -mtime +3 -exec rm {} \;

```

---

### Файл 4: `S99cctv` (Скрипт автозагрузки в /opt/etc/init.d/)

```bash
#!/bin/sh

# Укажите путь к вашему скрипту записи
SCRIPT_PATH="/tmp/mnt/YOUR_USB_DRIVE/cctv/record_cctv.sh"

case "$1" in
    start)
        echo "Starting CCTV recording..."
        sh $SCRIPT_PATH
        ;;
    stop)
        echo "Stopping CCTV recording..."
        rm -f /tmp/cctv_is_running
        sleep 2
        killall ffmpeg
        ;;
    restart)
        $0 stop
        sleep 5
        $0 start
        ;;
    *)
        echo "Usage: $0 {start|stop|restart}"
        exit 1
        ;;
esac

```
