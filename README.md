# 📚 Keenetic Knowledge Base

Личная инженерная база знаний и исследовательская мастерская по Keenetic, Entware,
сетям, VPN/proxy, Mihomo/Xray, DPI и смежным темам.

> **EN:** Personal engineering knowledge base: research notes and verified articles on Keenetic routers, Entware, Mihomo, VPN routing and DPI bypass (content in Russian).

Одним из основных входящих источников является Telegram-канал **TechnoBypass**: туда
попадают найденные проекты, ссылки, пересылки, эксперименты и рабочие заметки, а этот
репозиторий должен превращать такой поток в удобный каталог и проверенные знания.

> **Статус:** основная структурная реорганизация завершена (2026-09-24): поддерживаемые
> статьи — в `docs/`, архив provenance — в `archive/`, активные проекты — в своих
> каталогах. Отдельные статьи всё ещё несут статусы Confirmed / Observed / Research,
> и часть live-валидаций остаётся незакрытой — см. «Что уже сделано и что дальше».

## Зачем этот репозиторий нужен

Изначально он задумывался как структурированная база знаний по Keenetic. Со временем сюда
стали складываться исследования и рабочие заметки из разных задач.

Теперь цель репозитория шире:

- сохранить полезный технический опыт, который иначе теряется в чатах;
- превратить поток ссылок и материалов из TechnoBypass в индексируемую исследовательскую память;
- отделить реальные наблюдения от непроверенных предположений и старых ответов ИИ;
- превращать сырой материал в небольшие проверенные статьи;
- использовать найденные знания в активных проектах владельца;
- хранить контекст и причины инженерных решений, не создавая конкурирующих источников истины.

Рабочий принцип:

```text
TechnoBypass / старые заметки / upstream / реальные тесты
                         ↓
                 source catalog
                         ↓
             инвентаризация и темы
                         ↓
        проверка по коду и документации
                         ↓
          нормальная статья / артефакт
                         ↓
       при необходимости — promotion
           в профильный проект
```

## С чего начать

**Читателю:**

- 🌐 **[Открыть онлайн-справочник](https://saymer-alt.github.io/keenetic-knowledge-base/)** — тематическая навигация, поиск и 16 отобранных статей. Сырой архив не опубликован на сайте.
- [docs/](docs/) — извлечённые проверяемые статьи из материалов канала и новых
  research-заметок (Keenetic/Entware, маршрутизация Mihomo, белые списки, DPI,
  терминология, APN). Лучшая стартовая точка.
- [catalog/techno-bypass/README.md](catalog/techno-bypass/README.md) — каталог экспорта
  TechnoBypass (темы, проекты, статьи, provenance, аудиты и верификация).

**Навигация и метаданные репозитория:**

- [INVENTORY.md](INVENTORY.md) — первичная карта текущих файлов и их предполагаемая ценность.
- [ROADMAP.md](ROADMAP.md) — план превращения накопленных материалов в настоящую базу знаний.
- [SOURCES.md](SOURCES.md) — происхождение сторонних и raw-материалов, а также текущий статус лицензирования.
- [COPYRIGHT_AND_LICENSING.md](COPYRIGHT_AND_LICENSING.md) — утверждённые области **CC BY 4.0** для авторских статей и **MIT** для собственного кода; сторонние материалы и архивы исключены, общей лицензии на репозиторий нет.
- [ARTICLE_TEMPLATE.md](ARTICLE_TEMPLATE.md) — шаблон для будущих проверенных статей.
- [AGENTS.md](AGENTS.md) — правила работы для AI-агентов и границы безопасности (не документация пользователя).
- [docs/keenetic-policy-segment-ssid-naming.md](docs/keenetic-policy-segment-ssid-naming.md) —
  почему политика доступа, локальный сегмент, SSID, MagiTrickle/Mihomo и операторский WL — разные слои, и как именовать их без путаницы.
- [docs/keenetic-dns-via-mihomo.md](docs/keenetic-dns-via-mihomo.md) —
  upstream DNS самого Keenetic через ProxyN → Mihomo (DoT/DoH `on ProxyN`):
  подтверждённые примитивы, безопасный тест-план и что ещё требует live-проверки.
- [docs/dns-geoip-ecs-leak-diagnostics.md](docs/dns-geoip-ecs-leak-diagnostics.md) —
  диагностика DNS leak, ECS, IPv4/IPv6 и границы туннеля при VPN/proxy/VPS; отдельно отмечено, что точный алгоритм service-specific GeoIP остаётся research без публичного подтверждения.
- [docs/mihomo-systemd-nonroot-hardening.md](docs/mihomo-systemd-nonroot-hardening.md) —
  research по запуску Mihomo под отдельным systemd-пользователем и least-privilege capabilities: что подтверждает upstream, где исходная рекомендация Gemini слишком оптимистична, безопасный тест-план и rollback.
- [docs/network-layer-tunnel-map.md](docs/network-layer-tunnel-map.md) и
  [docs/proxy-tunnel-protocol-stack.md](docs/proxy-tunnel-protocol-stack.md) —
  слоёные модели туннелей/прокси: уровни L2/L3, TUN/TAP и встраивание в ОС;
  стек протокол/транспорт/маскировка и чтение цепочек (извлечено из `proxy.md`).
- [docs/moshub-entware-mirror.md](docs/moshub-entware-mirror.md) —
  пригодность Mos.Hub как вторичного зеркала .ipk для `entware-go`: что подтверждено
  живой проверкой, что осталось GitLab-предположением, и план пилота.
- [docs/iot-cloud-routing-methodology.md](docs/iot-cloud-routing-methodology.md) —
  как выяснить облачные зависимости камеры/IoT и направить в Mihomo только нужный
  трафик (извлечено из `NVR/WL.md`).
- [MosTech/README.md](MosTech/README.md) — авторский цикл MosTech: сатирические
  статьи, raw-заметки и скрипт о жизни с корпоративным ALT Linux, а также
  поддерживаемая техническая статья
  [MosTech/kvm-windows-virtiofs.md](MosTech/kvm-windows-virtiofs.md)
  (KVM/Windows/VirtIO-FS: проверенный рецепт, поведение буквы диска и аудит
  `setup-kvm-motech.sh`).
- [Keenetic NVR](https://github.com/saymer-alt/keenetic-nvr) — **самостоятельный основной репозиторий** NVR v2.4, Telegram-бота, установщиков и тестов. Старый каталог `NVR/`: **ARCHIVED / MOVED**.
  [NVR/README.md](NVR/README.md) здесь оставлен как исторический раздел v1 и HTTP-вещания.


## TechnoBypass как основной research source

TechnoBypass используется как **входящий поток исследований**, а не как автоматически
проверенная документация. В канал могут попадать собственные заметки, ссылки на GitHub,
документация, пересланные сообщения, подборки, гипотезы и материалы, которые позже
оказываются устаревшими или ошибочными.

Цель этого репозитория — сделать такой поток пригодным для поиска и повторного использования:

- извлекать ссылки и контекст из экспортов канала;
- сохранять дату и Telegram message ID для provenance;
- отличать собственные посты от пересланных материалов;
- объединять повторные ссылки на один проект без потери контекста;
- раскладывать ресурсы по темам;
- сохранять непроверенное как `Source` / `Research`;
- повышать материал до `Observed` / `Confirmed` только после реальной проверки;
- находить материалы, которые стоит перенести в активные проекты владельца.

Сырые HTML-экспорты Telegram **не предназначены для обычного коммита в публичный
репозиторий**: в них много служебной разметки, повторов, пересланных данных и потенциально
приватных ссылок. В репозитории должен храниться нормализованный результат импорта, а не
необработанный экспорт.

TechnoBypass — важный источник того, **что стоит исследовать**. Источником истины для
конкретного поведения остаётся актуальный код соответствующего проекта, официальная
документация или явно зафиксированный реальный тест.

## Структура репозитория

```text
docs/       поддерживаемые статьи знаний
MosTech/    авторский цикл MosTech (статьи, raw-материалы, скрипт)
catalog/    исследовательский каталог TechnoBypass
NVR/        исторические NVR v1/streaming и сохранённая копия NVR v2 (upstream: keenetic-nvr)
tools/      детерминированные инструменты импорта
archive/    provenance: raw-исследования и исторические файлы
```

Корень содержит только навигацию/метаданные (этот README, AGENTS, INVENTORY, ROADMAP,
SOURCES, ARTICLE_TEMPLATE, PROMOTION_BACKLOG, Каталог_ссылок_TechnoBypass).

История с несовпадением имени и тематики — из предыдущего состояния: например,
бывший `NVR/WL.md` (сейчас `archive/raw/NVR-WL.md`) содержал материал про Mihomo и
белые списки, а не про видеорегистратор. Именно поэтому перемещение файлов шло только
после содержательного аудита, по правилам [AGENTS.md](AGENTS.md).

## Связь с активными проектами

Этот репозиторий не должен дублировать документацию, принадлежащую коду.

Если материал относится к существующему проекту, актуальное поведение сначала сверяется
с его кодом и собственным `AGENTS.md`:

- [saymer-alt/keenetic-auto-setup](https://github.com/saymer-alt/keenetic-auto-setup) —
  установка и эксплуатация Mihomo на Keenetic, watchdog, интеграция с KeeneticOS;
- [saymer-alt/link-generators](https://github.com/saymer-alt/link-generators) —
  генерация конфигураций, поддержка протоколов, валидация и UI;
- [saymer-alt/entware-go](https://github.com/saymer-alt/entware-go) —
  Entware-пакеты и их сборка;
- [saymer-alt/vps-gateway-bootstrap](https://github.com/saymer-alt/vps-gateway-bootstrap) —
  framework для аудируемого VPS-провижининга (ранняя стадия);
- [saymer-alt/amnezia-mihomo-gateway](https://github.com/saymer-alt/amnezia-mihomo-gateway) —
  маршрутизация AmneziaAWG через Mihomo TUN/WARP на VPS (серверная systemd/iptables схема).

**Код проекта, который реализует поведение, является источником истины.**
Здесь остаются объяснения, исследования, исторический контекст и материалы для дальнейшей
переработки.

## Правила качества

Проверенная документация должна явно отличать:

- **наблюдалось на реальной системе**;
- **подтверждено текущим кодом или документацией**;
- **историческая информация**;
- **гипотеза / непроверенная заметка**.

Старый ответ ChatGPT/Claude/другого ИИ сам по себе не является подтверждением факта.

Команды, которые меняют маршруты, firewall, DNS, systemd, VPN или конфигурацию Keenetic,
нельзя считать безопасными только потому, что они сохранены в Markdown-файле.

## Что уже сделано и что дальше

Первый большой входящий массив — TechnoBypass — уже обработан:

- создан нормализованный каталог с provenance и тематической навигацией;
- выполнены независимый review, security-аудит и проверка части high-value ресурсов;
- создан reusable Telegram-export parser;
- извлечены первые тематические статьи в `docs/`;
- сформирован promotion backlog для активных проектов.

Кампания содержательного аудита старого архива завершена (TASK-KB-08..11): знание из
`proxy.md`, `moshub.md`, `NVR/WL.md`, MosTech/VirtIO-кластера и VPS-кластера извлечено
в поддерживаемые статьи; 2026-09-24 (TASK-KB-12) все отработанные raw/исторические
файлы физически перемещены в `archive/raw/` и `archive/historical/` (карта замен —
[archive/README.md](archive/README.md)); 2026-09-29 весь авторский цикл MosTech
(сатирические статьи, raw-заметки, скрипт и техническую статью) дополнительно
объединён в самостоятельный раздел [MosTech/](MosTech/) — решение владельца
сохранить цикл единым произведением.

**Оставшаяся конкретная работа** (не структурная):

- live-валидации: DNS-путь `DoT on ProxyN` (тест-план в
  [docs/keenetic-dns-via-mihomo.md](docs/keenetic-dns-via-mihomo.md)) и NVR на живом
  Keenetic (см. `NVR/AUDIT.md`);
- пилот Mos.Hub-зеркала (решение B, план в
  [docs/moshub-entware-mirror.md](docs/moshub-entware-mirror.md)) — задача оператора;
- promotion-решения владельца из [PROMOTION_BACKLOG.md](PROMOTION_BACKLOG.md)
  (sing-box в entware-go, Proton-конвертер и др.);
- будущие импорты TechnoBypass через `tools/parse_telegram_export.py`;
- (решено 2026-09-24) сторонний `scripts/service` удалён из HEAD после аудита
  TASK-KB-13/14 — см. `archive/historical/entware-service-helper-audit.md`;
- сопровождение статусов статей (Research → Confirmed по мере проверок).

Подробности и текущие статусы — в [ROADMAP.md](ROADMAP.md) и [INVENTORY.md](INVENTORY.md).
