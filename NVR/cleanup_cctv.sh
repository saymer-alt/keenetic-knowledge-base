#!/bin/sh

# Укажите ваш путь к диску. 
# Параметр +3 означает удаление файлов старше 3 суток (72 часа).
find /tmp/mnt/YOUR_USB_DRIVE/cctv/ -name "*.mkv" -type f -mtime +3 -exec rm {} \;
