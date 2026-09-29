# Raw research — Gemini: запуск Mihomo без root через systemd

**Дата получения:** 2026-09-29  
**Источник:** рекомендация Gemini, переданная владельцем репозитория  
**Статус:** Raw / AI-generated research; не является подтверждённой инструкцией

## Исходная рекомендация

Gemini по результатам осмотра VPS сообщил:

- Mihomo запущен от root; `User=` в systemd unit не задан.
- На сервере из обычных пользователей отмечен `mita` (UID 1000, shell `/bin/sh`).
- В группе sudo никого нет, `/etc/sudoers.d/` пуст.
- Строки `AmbientCapabilities=...` являются директивами systemd, а не командами shell.

Предложенная схема hardening:

1. Создать системного пользователя:
   ```sh
   useradd -r -s /usr/sbin/nologin mihomo
   ```
2. Передать ему рабочий каталог:
   ```sh
   chown -R mihomo:mihomo /etc/mihomo
   ```
3. Запускать unit с:
   ```ini
   User=mihomo
   Group=mihomo
   AmbientCapabilities=CAP_NET_ADMIN CAP_NET_BIND_SERVICE
   CapabilityBoundingSet=CAP_NET_ADMIN CAP_NET_BIND_SERVICE
   ProtectSystem=full
   ProtectHome=true
   ```
4. Выполнить `systemctl daemon-reload`, перезапустить Mihomo и проверить владельца процесса.

Исходная гипотеза: `CAP_NET_ADMIN` достаточно для TUN/TProxy, а `CAP_NET_BIND_SERVICE` — для привязки к привилегированным портам, поэтому полный root не требуется.

## Почему это сохранено как raw

После сверки 2026-09-29 рекомендация оказалась полезным направлением hardening, но **не готовым универсальным рецептом**:

- официальная инструкция Mihomo для systemd действительно использует capabilities, но её пример содержит существенно более широкий набор, включая `CAP_NET_RAW`, `CAP_DAC_READ_SEARCH`, `CAP_DAC_OVERRIDE` и другие;
- поэтому утверждение, что именно двух capabilities всегда достаточно, upstream-документацией не подтверждено;
- `chown -R /etc/mihomo` расширяет права демона на конфигурацию и возможные секреты и не должен применяться автоматически;
- `ProtectSystem=full` делает системные каталоги read-only для сервиса и требует отдельно проверить, куда конкретная конфигурация Mihomo пишет runtime/cache/geodata;
- необходим live-тест на конкретном VPS и конкретном режиме TUN/TProxy.

Проверенная переработка и безопасный тест-план: [../../docs/mihomo-systemd-nonroot-hardening.md](../../docs/mihomo-systemd-nonroot-hardening.md).
