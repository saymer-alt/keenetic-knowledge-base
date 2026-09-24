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
| `proxy.md` | source/raw → candidate | Большое исследование/обсуждение классификации VPN, proxy, L2/L3, transport и смежных технологий | Разделить на несколько тематических статей; факты и классификацию перепроверить по актуальным источникам |
| `amnezia.md` | historical / superseded source | Ранняя ручная версия маршрутизации Docker/AmneziaWG через Mihomo TUN | Сохранить как provenance; актуальная реализация — `amnezia-mihomo-gateway`; сравнение: `docs/amnezia-mihomo-gateway-evolution.md` |
| `awg.md` | historical / superseded source | Ещё одна стадия того же ручного решения AmneziaWG → Mihomo routing | Сохранить как provenance; технические идеи уже promoted в активный проект |
| `check.md` | historical / concept promoted | Ранняя версия watchdog/self-healing через systemd timer | Концепция уже встроена в `amnezia-mihomo-gateway`; оставить как историю эволюции |
| `install.sh` | historical project artifact / superseded | Ранний installer AmneziaWG → Mihomo routing | Не запускать из KB; текущий source of truth — `amnezia-mihomo-gateway/install.sh` |
| `uninstall.sh` | historical duplicate snapshot | Cleanup companion; на 2026-09-19 blob совпадает с активным `amnezia-mihomo-gateway/uninstall.sh` | Не считать canonical copy; rollback неполный, детали в `docs/amnezia-mihomo-gateway-evolution.md` |
| `moshub.md` | source/raw → candidate | Очень крупное исследование Mos.Hub/GitLab как площадки для артефактов, IPK/OPKG feed и зеркалирования | Высокий приоритет на тематическое извлечение; текущие возможности/квоты/URL перепроверить; возможные выводы сравнить с `entware-go` |
| `moshubrd.md` | source/raw / historical | Сохранённый/сгенерированный Mos.Hub README и связанные заметки | Не считать документацией проекта; сохранить как provenance до разбора `moshub.md` |
| `mihomo-dns.md` | source/raw → extracted | Research-диалог (2026-09-22) о DNS Keenetic через ProxyN→Mihomo; с header-указателем на извлечённую статью | Provenance для `docs/keenetic-dns-via-mihomo.md`; как production-процедуру не использовать |
| `Каталог_ссылок_TechnoBypass.md` | candidate / scaffold | Каркас каталога Keenetic/VPN/DPI/сервисов без полноценного наполнения | Либо превратить в реальный curated index, либо архивировать после появления нормальной навигации |
| `VirtIO-FS.md` | source/raw / historical | Ответ/заметка про VirtIO-FS в Windows, в частности mount point/букву диска | Вынести из Keenetic-тематики; технические утверждения перепроверить перед повторным использованием |
| `virtiofsd.md` | source/raw → candidate | Материал по virtiofsd/VirtIO-FS и обмену файлами в виртуализации | Возможная отдельная Linux/KVM reference-статья, но не Keenetic core |
| `setup-kvm-motech.sh` | project artifact / unrelated to Keenetic | Bash-автоматизация настройки KVM/virt-manager в среде MosTech | Хранить отдельно от Keenetic; перед reuse провести code review и определить реальный проект-владелец |
| `MosTech.md` | historical / unrelated | Творческий сатирический текст про MosTech с техническими отсылками | Не смешивать с KB; сохранить в archive/historical либо вынести в более подходящий проект |
| `MosTech_cifrovoj.md` | historical / source/raw / unrelated | Творческий/описательный материал про опыт MosTech, KVM, VirtIO и рабочие эксперименты | Перед архивированием извлечь уникальные реальные наблюдения, если они там есть |
| `cloudmos.md` | unrelated / historical | Сатирический текст/анкета про корпоративную MosTech-среду | Архивировать отдельно от технической KB |
| `class.md` | unrelated | Астрологическая классификация в IT-метафорах | Не относится к Keenetic/networking; безопасный кандидат на отдельный архив |
| `catalog/` | canonical | Каталог TechnoBypass: темы, индекс проектов, unclassified, STATS + аудиты (REVIEW, SECURITY_REVIEW, OWNER_LINK_AUDIT, VERIFIED_RESOURCES) | Поддерживать при новых экспортах (парсер — ниже); статусы не понижать без причины |
| `tools/` | project artifact | `parse_telegram_export.py` — детерминированный парсер Telegram-экспортов (stdlib-only) | Использовать для будущих экспортов; выход — только в рабочий каталог вне git |
| `docs/` | candidate | Извлечённые статьи по ARTICLE_TEMPLATE со разведёнными статусами: 7 тем TB-05 + эволюция amnezia-mihomo-gateway + именование слоёв Keenetic (2026-09-23) + DNS через ProxyN (2026-09-24) | Повышать до canonical по мере проверки; расширять из catalog-тем и новых research-материалов |
| `PROMOTION_BACKLOG.md` | canonical | Реестр кандидатов на перенос в активные проекты (TB-06) | Закрывать пункты по мере выполнения/отклонения |

## NVR/

| Path | First-pass status | Что там сейчас | Возможное действие |
|---|---|---|---|
| `NVR/README.md` | candidate, reviewed | Оформленная инструкция Keenetic + Entware + ffmpeg: NVR, сегментация, streaming | Технический аудит выполнен 2026-09-19 (`NVR/AUDIT.md`); исправлена совместимость с текущим FFmpeg, до canonical нужен повторный live-test |
| `NVR/record_cctv.sh` | project artifact, reviewed | RTSP recording loop, segment files, PID files | `-timeout` обновлён для FFmpeg 6.x; live-test и graceful-stop/PID hardening остаются открыты |
| `NVR/cleanup_cctv.sh` | project artifact, reviewed | Малый cleanup-скрипт для архива | Сохранить текущую `find -mtime +3` semantics; проверить фактический retention на устройстве при live-test |
| `NVR/S99cctv` | project artifact, reviewed | Entware init script для записи CCTV | Аудит выявил stale-PID/PID-reuse и SIGKILL caveats; менять lifecycle только после live-test |
| `NVR/S99stream` | project artifact, reviewed | Entware init/streaming logic для HTTP MPEG-TS | Проверены структура и stop lifecycle; credentials должны оставаться с ограниченными правами; нужен live reconnect/load test |
| `NVR/WL.md` | source/raw → candidate, **misplaced** | Обсуждение архитектуры Mihomo, DIRECT vs proxy и обхода ограничений/белых списков | Вынести из NVR при реорганизации; сверить с `keenetic-auto-setup` и текущей архитектурой whitelist mode |

## scripts/

| Path | First-pass status | Что там сейчас | Возможное действие |
|---|---|---|---|
| `scripts/service` | project artifact / reference | Сторонний shell helper для управления Entware services, указан автор Pavel P. / @pnpzx | Проверить происхождение и лицензию перед распространением/изменением; решить, это vendored reference или собственный maintained script |

## Candidate knowledge clusters

### 1. VPS: AmneziaWG → Mihomo

Связанные файлы:

- `amnezia.md`
- `awg.md`
- `check.md`
- `install.sh`
- `uninstall.sh`

Это выглядит не как пять независимых материалов, а как эволюция одного решения:
Docker/AmneziaWG traffic → policy routing → Mihomo TUN → recovery/health-check → installer.

**Аудит выполнен 2026-09-19:** кластер сопоставлен с текущим
`amnezia-mihomo-gateway`. Результат —
[`docs/amnezia-mihomo-gateway-evolution.md`](docs/amnezia-mihomo-gateway-evolution.md).
Старые Markdown-ответы и корневые скрипты остаются provenance и не должны управлять production-кодом.

### 2. Network concepts / proxy taxonomy

Основной источник:

- `proxy.md`

Возможные будущие статьи:

- VPN vs proxy vs transport;
- L2 vs L3 tunnels;
- TUN/TAP;
- WireGuard/AmneziaWG;
- VLESS/REALITY и application-layer proxy protocols;
- где заканчивается транспорт и начинается routing policy.

### 3. Keenetic NVR / streaming

Основные источники:

- `NVR/README.md`
- `NVR/record_cctv.sh`
- `NVR/cleanup_cctv.sh`
- `NVR/S99cctv`
- `NVR/S99stream`

Это самый близкий к самостоятельному законченному мини-проекту блок в текущем дереве.

### 4. Whitelist / Mihomo routing model

Источник:

- `NVR/WL.md`

Несмотря на расположение, это материал про различие между:

- маршрутизацией устройства через отдельную policy;
- отправкой только выбранного трафика в Mihomo;
- DIRECT и proxy decisions;
- поведением в сетях с разрешённым белым списком.

Потенциально полезен для общей документации и для проверки текущего whitelist mode в
активных проектах.

### 5. Mos.Hub / package distribution research

Источники:

- `moshub.md`
- `moshubrd.md`
- частично `Каталог_ссылок_TechnoBypass.md`

Может дать полезные идеи для резервного размещения Entware/IPK артефактов, но любые
утверждения о текущих возможностях Mos.Hub требуют свежей проверки.

### 6. MosTech / KVM / VirtIO-FS

Источники:

- `VirtIO-FS.md`
- `virtiofsd.md`
- `setup-kvm-motech.sh`
- `MosTech.md`
- `MosTech_cifrovoj.md`
- `cloudmos.md`

Это отдельная тема, не ядро Keenetic Knowledge Base. В ней смешаны реальные технические
наблюдения, автоматизация и творческие тексты. Перед перемещением нужно извлечь фактические
наработки, которые могут быть полезны в отдельной Linux/MosTech базе.

## Immediate priorities

1. **Не перемещать файлы массово.**
2. ~~Глубоко разобрать VPS-кластер и сравнить его с текущим VPS-проектом.~~ Выполнено 2026-09-19.
3. ~~Аудировать NVR как самостоятельный мини-проект.~~ Выполнено 2026-09-19; результат — `NVR/AUDIT.md`, до canonical нужен live-test.
4. **Следующий приоритет:** разобрать `proxy.md` на карту оставшегося уникального знания (базовая терминология уже извлечена в `docs/vpn-proxy-terminology.md`).
5. Разобрать `moshub.md` по темам и проверить, есть ли там актуальные идеи для `entware-go`.
6. Вытащить технические факты из MosTech/VirtIO материалов и затем отделить их от творческого архива.
7. Только после этого выбрать окончательную структуру каталогов.
