# Keenetic Knowledge Base

Инженерный справочник о Keenetic, Entware, Mihomo, VPN, сетевой маршрутизации и диагностике DPI.

Здесь собраны **отобранные технические статьи** из публичного репозитория. Это не копия всего исследовательского архива и не замена документации проектов, в которых реализован описанный код.

!!! warning "Проверяйте статус материала"
    В статьях явно различаются **Confirmed** (проверено в указанном объёме), **Observed** (практическое наблюдение), **Research** (ещё не подтверждено полностью) и **Historical** (история). Сетевые настройки зависят от версии ПО, оборудования и условий подключения.

## Быстрый старт

| Интересует | С чего начать |
| --- | --- |
| VPN, прокси и транспортные протоколы | [Словарь терминов](vpn-proxy-terminology.md) |
| Keenetic + Entware | [Базовая модель](keenetic-entware-base.md) |
| Mihomo на роутере | [Архитектура маршрутизации](mihomo-keenetic-routing.md) |
| DNS через ProxyN | [Keenetic DNS через Mihomo](keenetic-dns-via-mihomo.md) |
| IoT и маршрутизация камер | [Методология обнаружения облачных зависимостей](iot-cloud-routing-methodology.md) |
| DPI и неполадки доступа | [Карта диагностических инструментов](dpi-diagnostics-map.md) |

[Открыть полный каталог из 16 статей](README.md)

## Как пользоваться

Используйте **поиск** по статьям и меню разделов. Перед выполнением команд смотрите даты проверки, ограничения и ссылки на первоисточники. Если в статье описана работа другого проекта, актуальное поведение следует сверять с его собственным репозиторием.

Для исходных материалов, архивов и provenance см. [исходный GitHub-репозиторий](https://github.com/saymer-alt/keenetic-knowledge-base) и [журнал происхождения материалов](https://github.com/saymer-alt/keenetic-knowledge-base/blob/main/SOURCES.md).

## Связанные разработки

- [keenetic-auto-setup](https://github.com/saymer-alt/keenetic-auto-setup) — установка, обновление и диагностика Mihomo на Keenetic.
- [link-generators](https://github.com/saymer-alt/link-generators) — генератор конфигураций и ссылок.
- [entware-go](https://github.com/saymer-alt/entware-go) — Entware-пакеты Mihomo и WARPSCOUT.
- [amnezia-mihomo-gateway](https://github.com/saymer-alt/amnezia-mihomo-gateway) — маршрутизация AmneziaWG через Mihomo и WARP.

!!! info "Прозрачность публикации"
    MkDocs собирает сайт только из явно перечисленных страниц `docs/`. Сырой архив, Telegram-экспорты, исходные исследования, скрипты и внутренние материалы **не включаются**. Ссылки на первоисточники вне сайта ведут на GitHub.

!!! note "Лицензирование"
    Для всего содержимого репозитория пока не выбрана единая лицензия: происхождение и условия переиспользования материалов описаны в [SOURCES.md](https://github.com/saymer-alt/keenetic-knowledge-base/blob/main/SOURCES.md). Публичная доступность не означает разрешение на свободное копирование.
