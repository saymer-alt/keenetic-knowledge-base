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
| `amnezia.md` | source/raw + project candidate | Пошаговая схема маршрутизации Docker/AmneziaWG через Mihomo TUN на VPS, sysctl/ip rule/iptables/systemd | Сравнить с текущим VPS gateway/bootstrap; не применять как production-инструкцию без проверки |
| `awg.md` | source/raw + project candidate | Ещё одна, более отредактированная версия AmneziaWG → Mihomo routing с обсуждением code review | Сопоставить с `amnezia.md`, `check.md`, `install.sh`; извлечь только подтверждённую архитектуру |
| `check.md` | source/raw + project candidate | Health-check/self-healing для Mihomo и policy routing через systemd timer | Проверить необходимость и failure modes; вероятно относится к VPS-проекту |
| `install.sh` | project artifact | Bash-инсталлятор AmneziaWG → Mihomo routing: Docker discovery, sysctl, ip rule/iptables, systemd | Провести отдельный security/network review; сравнить с текущим VPS gateway/bootstrap перед любым переносом |
| `uninstall.sh` | project artifact | Удаление компонентов, созданных `install.sh`, включая routing cleanup и systemd | Проверять парой с installer; убедиться, что rollback действительно полный |
| `moshub.md` | source/raw → candidate | Очень крупное исследование Mos.Hub/GitLab как площадки для артефактов, IPK/OPKG feed и зеркалирования | Высокий приоритет на тематическое извлечение; текущие возможности/квоты/URL перепроверить; возможные выводы сравнить с `entware-go` |
| `moshubrd.md` | source/raw / historical | Сохранённый/сгенерированный Mos.Hub README и связанные заметки | Не считать документацией проекта; сохранить как provenance до разбора `moshub.md` |
| `Каталог_ссылок_TechnoBypass.md` | candidate / scaffold | Каркас каталога Keenetic/VPN/DPI/сервисов без полноценного наполнения | Либо превратить в реальный curated index, либо архивировать после появления нормальной навигации |
| `VirtIO-FS.md` | source/raw / historical | Ответ/заметка про VirtIO-FS в Windows, в частности mount point/букву диска | Вынести из Keenetic-тематики; технические утверждения перепроверить перед повторным использованием |
| `virtiofsd.md` | source/raw → candidate | Материал по virtiofsd/VirtIO-FS и обмену файлами в виртуализации | Возможная отдельная Linux/KVM reference-статья, но не Keenetic core |
| `setup-kvm-motech.sh` | project artifact / unrelated to Keenetic | Bash-автоматизация настройки KVM/virt-manager в среде MosTech | Хранить отдельно от Keenetic; перед reuse провести code review и определить реальный проект-владелец |
| `MosTech.md` | historical / unrelated | Творческий сатирический текст про MosTech с техническими отсылками | Не смешивать с KB; сохранить в archive/historical либо вынести в более подходящий проект |
| `MosTech_cifrovoj.md` | historical / source/raw / unrelated | Творческий/описательный материал про опыт MosTech, KVM, VirtIO и рабочие эксперименты | Перед архивированием извлечь уникальные реальные наблюдения, если они там есть |
| `cloudmos.md` | unrelated / historical | Сатирический текст/анкета про корпоративную MosTech-среду | Архивировать отдельно от технической KB |
| `class.md` | unrelated | Астрологическая классификация в IT-метафорах | Не относится к Keenetic/networking; безопасный кандидат на отдельный архив |

## NVR/

| Path | First-pass status | Что там сейчас | Возможное действие |
|---|---|---|---|
| `NVR/README.md` | candidate, near-canonical | Оформленная инструкция Keenetic + Entware + ffmpeg: NVR, сегментация, streaming | Провести технический аудит против фактических скриптов и актуального ffmpeg/Entware; после этого может стать canonical |
| `NVR/record_cctv.sh` | project artifact | RTSP recording loop, segment files, PID files | Проверить shell compatibility, credentials handling, failure/restart behavior |
| `NVR/cleanup_cctv.sh` | project artifact | Малый cleanup-скрипт для архива | Проверить retention semantics и безопасное удаление |
| `NVR/S99cctv` | project artifact | Entware init script для записи CCTV | Проверить graceful stop, PID lifecycle и совместимость с Entware init conventions |
| `NVR/S99stream` | project artifact | Entware init/streaming logic для HTTP MPEG-TS | Проверить порт, lifecycle, ffmpeg restart и ресурсы |
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

**Следующий шаг:** сравнить весь кластер с текущим VPS gateway/bootstrap проектом. Старые
Markdown-ответы не должны управлять production-кодом.

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
2. Глубоко разобрать VPS-кластер и сравнить его с текущим VPS-проектом.
3. Аудировать NVR как самостоятельный мини-проект.
4. Разделить `proxy.md` на карту будущих статей.
5. Разобрать `moshub.md` по темам и проверить, есть ли там актуальные идеи для `entware-go`.
6. Вытащить технические факты из MosTech/VirtIO материалов и затем отделить их от творческого архива.
7. Только после этого выбрать окончательную структуру каталогов.
