# PROMOTION BACKLOG — кандидаты на перенос в активные проекты (TASK-TB-06)

Дата анализа: 2026-09-19. Источники: каталог TechnoBypass (`catalog/`),
сырые файлы этого репозитория (`INVENTORY.md`), верификационные прогоны
TB-02B/TB-04. Для каждой цели прочитаны её правила (AGENTS.md рабочей копии
или через GitHub API), текущее дерево и сравнено с кандидатским знанием.

Главный вывод анализа: **большинство «кандидатов из канала» уже реализованы
или уже задокументированы** — канал во многом предшествует/дублирует то,
что позже стало кодом проектов владельца. Настоящих пробелов мало; они
перечислены в конце. Никакие другие репозитории в этой задаче не менялись.

Легенда действий: no action / documentation / bug fix / feature /
historical note / further research.

---

## saymer-alt/keenetic-auto-setup

| # | Источник | Идея | Текущее состояние | Почему полезно | Проверка | Риск | Действие |
|---|---|---|---|---|---|---|---|
| K1 | #923 | История «почему сделан проект» для README/ARCHITECTURE | **уже реализовано**: ARCHITECTURE.md §«Почему появился проект» — тот же нарратив | — | чтение файла 2026-09-19 | — | no action |
| K2 | #45 | Установка S00ubifs одной командой | **уже реализовано**: install.sh:120–126 ставит S00ubifs из репозитория и стартует | — | grep install.sh | — | no action |
| K3 | #14 | Мёртвые команды deploy.sh/gist в закреплённом посте | удалены из репо (909a9cc); пост канала не правится агентом | читатели поста получают 404 | TB-02B: git-история + API gist (404) | правка Telegram = оператор | historical note (+ оператор: текст замены готов в OWNER_LINK_AUDIT) |
| K4 | #815 | Ручное обновление Mihomo (PDF-гайд) | **superseded**: update-mihomo.sh; задокументировано | — | TB-02B | — | no action |
| K5 | #1127 | Mihomo Interface Checker | **уже реализовано**: mihomo-interface-check.sh v1.0.3 в репо | — | дерево репо | — | no action |
| K6 | #59 | youtubeUnblock на роутере | иной механизм (SNI-байпас), вне скоупа проекта | — | — | — | no action |
| K7 | #315, #1210 | ping-check профили KeeneticOS для VPN-интерфейсов | в проекте нет; проект = менеджмент Mihomo, не WG | авто-переключение упавших WG | не проверялось на живом | расширяет скоуп | further research (вопрос владельцу о границах скоупа) |
| K8 | #230 | Тюнинг health-check proxy-groups (interval/tolerance/idle_timeout) | домен конфигов пользователя/генератора, не инсталлера; AWL-failover уже настроен в link-generators (NIGHT-06) | — | — | — | no action |
| K9 | #96, #181, #1146 | DNS-связки (AdGuardHome, DoT ndmc) | чувствительная зона DNS; вне скоупа | — | — | сеть | no action |
| K10 | #882 | Бан MTProxy по JA3 | информационно; к проекту отношения не имеет | — | — | — | no action |

## saymer-alt/link-generators

| # | Источник | Идея | Текущее состояние | Проверка | Действие |
|---|---|---|---|---|---|
| L1 | #990, #978–#984 | masque://-генерация | **уже реализовано** (ядро продукта; origin/main) | grep origin/main (2026-09-19): masque-полный цикл | no action |
| L2 | #1156 | Поддержка файлов warpscout | **осознанно удалено** владельцем; пост фиксирует фазу | история продукта (memory + ветки) | historical note (уже отражено в каталоге owner-projects.md) |
| L3 | #263 | Дашборд Zashboard | **уже реализовано** (bf2e4a7, selectable Web UI) | git origin/main | no action |
| L4 | #985, #986 | Сканеры WARP-эндпоинтов | не реализовано — и **конфликтует с контрактом** фиксированного пула эндпоинтов (анти-DPI стратегия) | AGENTS.md продукта | no action (нарушение load-bearing контракта) |
| L5 | #1083, #651, #1180 | Паттерн «конвертер чужих конфигов» (ProtonVPN→AWG) | не реализовано; новая доменная область (Proton-конфиги) | — | further research (спросить владельца о желаемости) |

## saymer-alt/entware-go

| # | Источник | Идея | Текущее состояние | Проверка | Действие |
|---|---|---|---|---|---|
| E1 | #801 | Пакет beszel-agent | **уже реализовано**: пакет в дереве; PR #12 upstream MERGED 2026-08-29 | дерево + gh API | no action |
| E2 | #817 | Автосборка mihomo (workflow) | **уже реализовано**: build-mihomo.yml | дерево | no action |
| E3 | #16, #49, #63, #72, #173, #244 | Пакет sing-box в фиде entware-go | **genuinely missing**: канал многократно ставит sing-box на Keenetic c чужих фидов (qp-io/sw.ext.io) | проверено: sing-box в дереве entware-go отсутствует | **feature (будущая задача)**: решение владельца + проверка go.mod против SDK-тулчейна (правило Go-совместимости) + правила CI |

## saymer-alt/vps-gateway-bootstrap

Репозиторий в полёте (локально ahead 2 + незакоммиченная правка
pipeline.go; контрактом запрещены ad-hoc изменения). Кандидаты — только
как будущие задачи.

| # | Источник | Идея | Текущее состояние | Действие |
|---|---|---|---|---|
| V1 | #1079 | warp-docker-routing (WARP→Docker→routing) | концепция **уже живёт в amnezia-mihomo-gateway**; для этого репо чужие скрипты — только референс (оркестрационный lifecycle обязателен) | historical note / reference |
| V2 | #1220 | GeoIP-подмена локации VPS при DNS 8.8.8.8 | не отражено в docs/lessons-learned.md | **documentation (будущая задача)**: добавить урок после стабилизации ветки |
| V3 | #765, #791–#792 | Hardening setup.sh для VPS | вытеснено собственной security-моделью репо | no action |

## saymer-alt/amnezia-mihomo-gateway

Существует, активен (push 2026-09-18), собственный AGENTS.md,
install.sh/uninstall.sh/install.md/scripts/systemd.

| # | Источник | Идея | Текущее состояние | Проверка | Действие |
|---|---|---|---|---|---|
| A1 | #1079, #1088–#1090 | AWG(Docker)→Mihomo TUN→WARP с watchdog и автоопределением | **уже реализовано** — репозиторий этим и является (README: policy routing, скрытие IP, WARP-выход, watchdog, cleanup) | gh API README/дерево | no action |
| A2 | Кластер этого KB: `amnezia.md`, `awg.md`, `check.md`, `install.sh`, `uninstall.sh` (+ #1088) | Сверка сырых наблюдений с текущей реализацией: что уже покрыто, какие failure-cases стоит перенести | сверки не было (Phase-1 кластер в ROADMAP) | — | **further research (приоритетная будущая задача)**: разбор кластера KB против репо; переносить только подтверждённое, минимально, в стиле целевого проекта |
| A3 | #1133 | Скрипты проверки серверов | в репо свои health-checks (watchdog) | README | no action |

## keenetic-knowledge-base (сам репозиторий)

| # | Источник | Идея | Действие |
|---|---|---|---|
| S1 | TASK-TB-02A review | INVENTORY.md не знает `catalog/`, `tools/`, `docs/` | **documentation — выполняется в этой же задаче** (строки добавлены) |
| S2 | TB-01P | ROADMAP Phase-2 чекбоксы оператора vs выполненная работа; ссылки README/AGENTS на каталог | future task ПОСЛЕ reconciliation расхождения с origin (конфликтная зона) |

---

## Сводка

- Кандидатов рассмотрено: **24**.
- Уже реализовано/задокументировано в целях: **12** (K1, K2, K4, K5, L1, L2,
  L3, E1, E2, A1, частично K3/L4 — контрактом закрыто).
- Genuinely missing: **3** — E3 (sing-box в entware-go, feature, будущая
  задача), L5 (Proton-конвертер, нужен владелец), S1 (INVENTORY-строки,
  сделано здесь).
- Historical-only: K3, L2, V1 (+ фиксация в каталоге уже выполнена).
- Further research: K7, A2 (приоритет), V2, L5.

## Высокоценные следующие задачи (порядок)

1. **Оператор**: reconciliation расхождения origin/main этого KB
   (блокирует публикацию всего каталога и статей) — см. отчёт TASK-TB-01P.
2. **Оператор**: правка закреплённого поста #14 (текст замены готов в
   `catalog/techno-bypass/OWNER_LINK_AUDIT.md`).
3. **Будущая задача**: разбор VPS-кластера KB против amnezia-mihomo-gateway
   (A2) — старейший нетронутый кластер репозитория.
4. **Будущая задача (после reconciliation)**: doc-sync ROADMAP/README/AGENTS
   этого KB (S2) + INVENTORY уже закрыт здесь (S1).
5. **Вопрос владельцу**: sing-box в entware-go (E3) и границы скоупа
   keenetic-auto-setup по ping-check профилям (K7).
