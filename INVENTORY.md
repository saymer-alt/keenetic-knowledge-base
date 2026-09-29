# INVENTORY — current repository contents

Первичная содержательная карта репозитория.

Это **не окончательный вердикт** и не разрешение на удаление файлов. Статусы нужны для
последующей разборки. `candidate` и `source/raw` означают: материал может быть ценным,
но его нельзя публиковать как актуальную инструкцию без проверки.

## Status legend

- **canonical** — поддерживаемый документ или служебный файл репозитория.
- **candidate** — хороший кандидат на отдельную проверенную статью.
- **source/raw** — сырьё: диалог, исследование, AI-ответ, заметки.
- **project artifact** — исполняемый скрипт/конфигурация; требует code review как код.
- **historical** — полезный контекст, но не текущий источник истины.
- **unrelated** — не относится к основной Keenetic/networking KB.
- **review needed** — нужен более глубокий разбор перед дальнейшим решением.

## Root

| Path | First-pass status | Что там сейчас | Возможное действие |
|---|---|---|---|
| `AGENTS.md` | canonical | Проектные правила для AI-агентов, provenance, safety и promotion workflow | Оставить в корне |
| `README.md` | canonical | Честная точка входа в текущий переходный репозиторий | Поддерживать синхронно с реальным деревом |
| `ROADMAP.md` | canonical | План переработки архива в KB | Обновлять по мере этапов |
| `INVENTORY.md` | canonical | Эта карта содержимого | Уточнять после глубокого аудита |
| `SOURCES.md` | canonical | Журнал provenance, сторонних материалов и текущего статуса лицензирования | Поддерживать при переносе/добавлении внешних материалов |
| `ARTICLE_TEMPLATE.md` | canonical | Шаблон для будущих проверенных статей | Использовать как ориентир, не как обязательную бюрократию |
| `archive/` | canonical (provenance/history) | Прованс и история: `archive/raw/` (исследовательские снимки после извлечения знания) и `archive/historical/` (заменённые артефакты, исторические файлы); карта замен — `archive/README.md` | Не источник актуальных инструкций; утверждения не продвигать без перепроверки |
| `catalog/` | canonical | Каталог TechnoBypass: темы, индекс проектов, unclassified, STATS + аудиты (REVIEW, SECURITY_REVIEW, OWNER_LINK_AUDIT, VERIFIED_RESOURCES) | Поддерживать при новых экспортах (парсер — ниже); статусы не понижать без причины |
| `tools/` | project artifact | `parse_telegram_export.py` — детерминированный парсер Telegram-экспортов (stdlib-only) | Использовать для будущих экспортов; выход — только в рабочий каталог вне git |
| `docs/` | candidate | Извлечённые статьи по ARTICLE_TEMPLATE со разведёнными статусами: 7 тем TB-05 + эволюция amnezia-mihomo-gateway + именование слоёв Keenetic (2026-09-23) + DNS через ProxyN + карта уровней/встраивания и стек протоколов из `proxy.md` + аудит Mos.Hub-зеркала + методология облачных зависимостей IoT (статья KVM/Windows/VirtIO-FS из MosTech-кластера с 2026-09-29 живёт в `MosTech/`) | Повышать до canonical по мере проверки; расширять из catalog-тем и новых research-материалов |
| `MosTech/` | canonical (авторский цикл) | Единый раздел цикла MosTech: сатирические статьи, raw-заметки, скрипт провижининга и поддерживаемая статья `kvm-windows-virtiofs.md`; собран 2026-09-29 из `archive/` + `docs/` по решению владельца | Поддерживать как самостоятельную серию (см. `MosTech/README.md`); скрипт не утверждён к выполнению |
| `PROMOTION_BACKLOG.md` | canonical | Реестр кандидатов на перенос в активные проекты (TB-06) | Закрывать пункты по мере выполнения/отклонения |


## archive/ (физически перемещено из корня 2026-09-24, TASK-KB-12)

Статусы аудита сохранены; физическое перемещение выполнено `git mv` без изменения содержимого.

| Path | Статус | Что там | Действие/замена |
|---|---|---|---|
| `archive/raw/proxy.md` | source/raw → extracted | Исследовательский диалог: классификация VPN/proxy/L2-L3/transport, цепочки туннелей, модель слоёв абстракции; с header-указателем на извлечённые статьи | Полезное знание извлечено в `docs/vpn-proxy-terminology.md`, `docs/network-layer-tunnel-map.md`, `docs/proxy-tunnel-protocol-stack.md`; хранить как provenance |
| `archive/historical/amnezia.md` | historical / superseded source | Ранняя ручная версия маршрутизации Docker/AmneziaWG через Mihomo TUN | Сохранить как provenance; актуальная реализация — `amnezia-mihomo-gateway`; сравнение: `docs/amnezia-mihomo-gateway-evolution.md` |
| `archive/historical/awg.md` | historical / superseded source | Ещё одна стадия того же ручного решения AmneziaWG → Mihomo routing | Сохранить как provenance; технические идеи уже promoted в активный проект |
| `archive/historical/check.md` | historical / concept promoted | Ранняя версия watchdog/self-healing через systemd timer | Концепция уже встроена в `amnezia-mihomo-gateway`; оставить как историю эволюции |
| `archive/historical/install.sh` | historical project artifact / superseded | Ранний installer AmneziaWG → Mihomo routing | Не запускать из KB; текущий source of truth — `amnezia-mihomo-gateway/install.sh` |
| `archive/historical/uninstall.sh` | historical duplicate snapshot | Cleanup companion; на 2026-09-19 blob совпадает с активным `amnezia-mihomo-gateway/uninstall.sh` | Не считать canonical copy; rollback неполный, детали в `docs/amnezia-mihomo-gateway-evolution.md` |
| `archive/raw/moshub.md` | source/raw → extracted | Компиляция AI-разведок о Mos.Hub/GitLab/GitHub для IPK-дистрибуции; выводы противоречивы; с header-указателем | Проверенные выводы — в `docs/moshub-entware-mirror.md` (аудит 2026-09-24, решение по пилоту B); хранить как provenance |
| `archive/historical/moshubrd.md` | historical / provenance artifact | Нетронутый шаблонный README реального проекта владельца на Mos.Hub (`sayone/saymer`, 2026-05-09); с header-указателем | Уникального знания нет; доказывает существование namespace для пилота; не удалять до решения по зеркалу |
| `archive/raw/mihomo-dns.md` | source/raw → extracted | Research-диалог (2026-09-22) о DNS Keenetic через ProxyN→Mihomo; с header-указателем на извлечённую статью | Provenance для `docs/keenetic-dns-via-mihomo.md`; как production-процедуру не использовать |
| `Каталог_ссылок_TechnoBypass.md` | candidate / scaffold | Каркас каталога Keenetic/VPN/DPI/сервисов без полноценного наполнения | Либо превратить в реальный curated index, либо архивировать после появления нормальной навигации |
| `archive/raw/NVR-WL.md` (бывший `NVR/WL.md`) | source/raw → extracted | Исторический диалог: уровни Mihomo/правила/политики + облачные зависимости камер | Знание извлечено в статьи именования/маршрутизации/whitelist и `docs/iot-cloud-routing-methodology.md`; перемещён из NVR/ 2026-09-24 |

## MosTech/ (авторский цикл, собран 2026-09-29)

Весь исторический цикл MosTech (корень 2026-07/09 → `archive/` 2026-09-24 →
`MosTech/` 2026-09-29) объединён в одном разделе по решению владельца: цикл
сохраняется единым произведением, без деления на «техническую» и «творческую»
части. Содержимое файлов при сборке не переписывалось; статусы аудита 2026-09-24
сохранены. Назначение раздела — `MosTech/README.md`.

| Path | Статус | Что там | Действие/замена |
|---|---|---|---|
| `MosTech/MosTech.md` | historical / creative (часть цикла) | Сатирический выпуск-основание про MosTech (2026-07-21) | Хранить как часть цикла; проверяемых техфактов нет |
| `MosTech/MosTech_cifrovoj.md` | historical narrative / extracted | Нарратив с реальными наблюдениями: связка воспроизведена на 3 машинах; с header-указателем | Наблюдения учтены как Observed в `MosTech/kvm-windows-virtiofs.md`; QXL/secboot/порядок — не универсализированы |
| `MosTech/virtiofsd.md` | source/raw → extracted | Исторический диалог: буква диска/реестр VirtIO-FS в Windows; с header-указателем | Заявки проверены по исходникам virtio-win/WinFSP в `MosTech/kvm-windows-virtiofs.md`; часть опровергнута (дефолт `*`, перебор Z→D); хранить как provenance |
| `MosTech/VirtIO-FS.md` | source/raw → extracted | Историческое сравнение VirtIO-FS / QEMU-SMB / Samba с рабочим путём VirtIO-FS; с header-указателем | Рабочий путь извлечён в `MosTech/kvm-windows-virtiofs.md`; Samba-советы (`chmod 777`, guest ok) в статью сознательно не перенесены |
| `MosTech/cloudmos.md` | historical / creative (часть цикла) | Сатирическая анкета про корпоративную среду (2026-07-30) | Хранить как часть цикла; технического содержания нет |
| `MosTech/class.md` | unrelated creative → часть цикла (2026-09-29) | Астрологические знаки как IT-метафоры (2026-09-06); с header-примечанием о релокации | Хранить как часть цикла; к сетевой тематике отношения не имеет |
| `MosTech/setup-kvm-motech.sh` | historical project artifact / **не утверждён к выполнению** | Скрипт провижининга KVM+virt-manager (root; dnf; группа libvirt; polkit-правило) | Static-аудит 2026-09-24 (`MosTech/kvm-windows-virtiofs.md` §«Аудит»): 1 High, 2 Medium, 1 Low-кластер; не правился, не выполнялся |
| `MosTech/kvm-windows-virtiofs.md` | canonical (техническая статья цикла) | Поддерживаемая статья (TASK-KB-11): рецепт VirtIO-FS, поведение буквы диска, аудит скрипта | Поддерживать; provenance-ссылки — на соседние raw-файлы цикла |

## NVR/

| Path | First-pass status | Что там сейчас | Возможное действие |
|---|---|---|---|
| `NVR/README.md` | candidate, reviewed | Оформленная инструкция Keenetic + Entware + ffmpeg: NVR, сегментация, streaming | Технический аудит выполнен 2026-09-19 (`NVR/AUDIT.md`); исправлена совместимость с текущим FFmpeg, до canonical нужен повторный live-test |
| `NVR/record_cctv.sh` | project artifact, reviewed | RTSP recording loop, segment files, PID files | `-timeout` обновлён для FFmpeg 6.x; live-test и graceful-stop/PID hardening остаются открыты |
| `NVR/cleanup_cctv.sh` | project artifact, reviewed | Малый cleanup-скрипт для архива | Сохранить текущую `find -mtime +3` semantics; проверить фактический retention на устройстве при live-test |
| `NVR/S99cctv` | project artifact, reviewed | Entware init script для записи CCTV | Аудит выявил stale-PID/PID-reuse и SIGKILL caveats; менять lifecycle только после live-test |
| `NVR/S99stream` | project artifact, reviewed | Entware init/streaming logic для HTTP MPEG-TS | Проверены структура и stop lifecycle; credentials должны оставаться с ограниченными правами; нужен live reconnect/load test |

## scripts/

Активных скриптов в репозитории больше нет: сторонний `scripts/service` удалён из
текущего HEAD 2026-09-24 (TASK-KB-14) по решению аудита TASK-KB-13
([`archive/historical/entware-service-helper-audit.md`](archive/historical/entware-service-helper-audit.md);
происхождение/лицензия не установлены — класс C; история Git не переписывалась,
оригинальный blob остаётся в исторических коммитах). Каталог `scripts/` исчез за
пустотой.

## Candidate knowledge clusters

### 1. VPS: AmneziaWG → Mihomo

Связанные файлы:

- `archive/historical/amnezia.md`
- `archive/historical/awg.md`
- `archive/historical/check.md`
- `archive/historical/install.sh`
- `archive/historical/uninstall.sh`

Это выглядит не как пять независимых материалов, а как эволюция одного решения:
Docker/AmneziaWG traffic → policy routing → Mihomo TUN → recovery/health-check → installer.

**Аудит выполнен 2026-09-19:** кластер сопоставлен с текущим
`amnezia-mihomo-gateway`. Результат —
[`docs/amnezia-mihomo-gateway-evolution.md`](docs/amnezia-mihomo-gateway-evolution.md).
Файлы кластера с 2026-09-24 лежат в `archive/historical/` (TASK-KB-12) и не должны управлять production-кодом.

### 2. Network concepts / proxy taxonomy

Основной источник:

- `archive/raw/proxy.md`

Статьи из этого материала созданы 2026-09-24 (TASK-KB-08):
`docs/vpn-proxy-terminology.md`, `docs/network-layer-tunnel-map.md`,
`docs/proxy-tunnel-protocol-stack.md`; raw-файл остаётся provenance.

### 3. Keenetic NVR / streaming

Основные источники:

- `NVR/README.md`
- `NVR/record_cctv.sh`
- `NVR/cleanup_cctv.sh`
- `NVR/S99cctv`
- `NVR/S99stream`

Это самый близкий к самостоятельному законченному мини-проекту блок в текущем дереве.

### 4. Whitelist / Mihomo routing model

Источник (с 2026-09-24 в `archive/raw/NVR-WL.md`):

Несмотря на расположение, это материал про различие между:

- маршрутизацией устройства через отдельную policy;
- отправкой только выбранного трафика в Mihomo;
- DIRECT и proxy decisions;
- поведением в сетях с разрешённым белым списком.

Потенциально полезен для общей документации и для проверки текущего whitelist mode в
активных проектах.

**Контент извлечён 2026-09-24 (TASK-KB-10):** терминологические части — в
`docs/keenetic-policy-segment-ssid-naming.md`, `docs/mihomo-keenetic-routing.md`,
`docs/whitelist-mode-architecture.md`; методология облачных зависимостей камер/IoT —
в [`docs/iot-cloud-routing-methodology.md`](docs/iot-cloud-routing-methodology.md).
Файл перемещён в `archive/raw/NVR-WL.md` 2026-09-24 (TASK-KB-12); физическое перемещение завершено.

### 5. Mos.Hub / package distribution research

Источники:

- `archive/raw/moshub.md`
- `archive/historical/moshubrd.md`
- частично `Каталог_ссылок_TechnoBypass.md`

Проверено 2026-09-24 (TASK-KB-09): результат — `docs/moshub-entware-mirror.md`
(решение по пилоту B); свежая проверка hub.mos.ru выполнена, дальнейшие действия — за
пилотом оператора.

### 6. MosTech / KVM / VirtIO-FS

Весь цикл (статьи, raw-заметки, скрипт, техническая статья) с 2026-09-29 собран в
корневом разделе `MosTech/` — см. таблицу в разделе `MosTech/` выше. Это отдельная
авторская тема, не ядро Keenetic Knowledge Base. Техническое извлечение выполнено
2026-09-24 (TASK-KB-11): `MosTech/kvm-windows-virtiofs.md`; прежнее разделение
«творческое в archive/ + техническая статья в docs/» отменено решением владельца —
цикл сохраняется единым произведением.

## Immediate priorities

1. **Не перемещать файлы массово.**
2. ~~Глубоко разобрать VPS-кластер и сравнить его с текущим VPS-проектом.~~ Выполнено 2026-09-19.
3. ~~Аудировать NVR как самостоятельный мини-проект.~~ Выполнено 2026-09-19; результат — `NVR/AUDIT.md`, до canonical нужен live-test.
4. ~~Разобрать `proxy.md` на карту оставшегося уникального знания.~~ Выполнено 2026-09-24 (TASK-KB-08): извлечены `docs/network-layer-tunnel-map.md` и `docs/proxy-tunnel-protocol-stack.md`; файл помечен как provenance.
5. ~~Разобрать `moshub.md` по темам и проверить, есть ли там актуальные идеи для `entware-go`.~~ Выполнено 2026-09-24 (TASK-KB-09): результат — `docs/moshub-entware-mirror.md`, решение по пилоту B; реальный пилот — за оператором.
6. ~~Сопоставить `NVR/WL.md` с уже созданными статьями про Mihomo/whitelist.~~ Выполнено 2026-09-24 (TASK-KB-10): методология облачных зависимостей камер/IoT извлечена в `docs/iot-cloud-routing-methodology.md`; файл помечен extracted/misplaced, физическое перемещение — позже.
7. ~~Вытащить технические факты из MosTech/VirtIO материалов и затем отделить их от творческого архива.~~ Выполнено 2026-09-24 (TASK-KB-11): `kvm-windows-virtiofs.md` + аудит `setup-kvm-motech.sh`; творческие файлы классифицированы; физическое перемещение в архив — следующий этап. 2026-09-29: весь цикл дополнительно объединён в `MosTech/` (решение владельца).
8. ~~Планирование реорганизации архива.~~ Выполнено 2026-09-24 (TASK-KB-12): `archive/raw/` + `archive/historical/` созданы, 17 файлов перемещены `git mv`, ссылки отремонтированы.
9. **Следующий приоритет:** сопровождение (live-валидации DNS/NVR, пилот Mos.Hub, promotion-решения владельца, сопровождение архива (например, судьба `archive/historical/entware-service-helper-audit.md`)) — не структурные задачи.
