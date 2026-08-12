#!/bin/sh

# === НАСТРОЙКИ (ЗАМЕНИТЕ НА СВОИ) ===
BASE_DIR="/tmp/mnt/YOUR_USB_DRIVE/cctv"
RTSP_USER="YOUR_USERNAME"
RTSP_PASS="YOUR_PASSWORD"
RTSP_IP="192.168.1.XXX"

# Проверка: примонтирован ли диск?
# Если команда "mountpoint" не найдена — эти 3 строки просто проигнорируются
if ! mountpoint -q "$BASE_DIR" 2>/dev/null; then
    if [ ! -d "$BASE_DIR" ]; then
        echo "ERROR: Disk not mounted!" >&2
        exit 1
    fi
fi

# Флаг работы
touch /tmp/cctv_is_running

start_recording() {
    CAM_ID=$1
    DIR="$BASE_DIR/cam$CAM_ID"
    mkdir -p "$DIR"
    URL="rtsp://$RTSP_USER:$RTSP_PASS@$RTSP_IP:554/Streaming/Channels/$CAM_ID"
    
    (
        while [ -f /tmp/cctv_is_running ]; do
            echo "Starting record for Camera $CAM_ID..."
            
            /opt/bin/ffmpeg -hide_banner -loglevel error \
                -rtsp_transport tcp -i "$URL" \
                -c copy -f segment -segment_time 900 \
                -strftime 1 -reset_timestamps 1 \
                "$DIR/cam${CAM_ID}_%Y-%m-%d_%H-%M-%S.mkv" > /dev/null 2>&1 &
            
            PID=$!
            echo $PID > /tmp/cctv_cam${CAM_ID}.pid
            
            LASTFILE=""
            # Следим за процессом: если файл не растёт 2+ минуты — убиваем
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
    ) &
}

start_recording "101"
start_recording "201"
start_recording "301"

echo "CCTV recording started in watchdog mode."
