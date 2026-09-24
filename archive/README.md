# Archive — provenance и история

Этот каталог — **прованс и история**, а не актуальная документация. Полезное знание
из этих файлов уже извлечено в поддерживаемые статьи [`../docs/`](../docs/); сырые
утверждения, старые команды и списки не следует использовать без перепроверки.

Правило из [`../AGENTS.md`](../AGENTS.md): **`archive/` — provenance/history; не
продвигать утверждения из него без повторной верификации.**

## `raw/`

Исследовательские/чат-снимки, оставленные после извлечения полезного знания. Могут
содержать старые AI-рассуждения, непроверенные утверждения, устаревшие команды,
исторические URL/IP, эксперименты. Это provenance, **не инструкции**.

## `historical/`

Заменённые скрипты/артефакты проектов, исторические снимки, творческий/несвязанный
материал, сохранённый ради истории. Тоже **не актуальная документация**. Исторические
`.sh`-файлы сохранены байт-в-байт для provenance: их не запускать и не считать
рабочими рецептами.

## Карта: архив → поддерживаемая замена

| Файл в архиве | Поддерживаемая замена / причина хранения |
| --- | --- |
| [`raw/proxy.md`](raw/proxy.md) | [`docs/vpn-proxy-terminology.md`](../docs/vpn-proxy-terminology.md), [`docs/network-layer-tunnel-map.md`](../docs/network-layer-tunnel-map.md), [`docs/proxy-tunnel-protocol-stack.md`](../docs/proxy-tunnel-protocol-stack.md) |
| [`raw/mihomo-dns.md`](raw/mihomo-dns.md) | [`docs/keenetic-dns-via-mihomo.md`](../docs/keenetic-dns-via-mihomo.md) |
| [`raw/moshub.md`](raw/moshub.md) | [`docs/moshub-entware-mirror.md`](../docs/moshub-entware-mirror.md) |
| [`raw/NVR-WL.md`](raw/NVR-WL.md) | [`docs/iot-cloud-routing-methodology.md`](../docs/iot-cloud-routing-methodology.md), [`docs/whitelist-mode-architecture.md`](../docs/whitelist-mode-architecture.md), [`docs/mihomo-keenetic-routing.md`](../docs/mihomo-keenetic-routing.md), [`docs/keenetic-policy-segment-ssid-naming.md`](../docs/keenetic-policy-segment-ssid-naming.md) |
| [`raw/VirtIO-FS.md`](raw/VirtIO-FS.md), [`raw/virtiofsd.md`](raw/virtiofsd.md), [`raw/MosTech_cifrovoj.md`](raw/MosTech_cifrovoj.md) | [`docs/kvm-windows-virtiofs.md`](../docs/kvm-windows-virtiofs.md) |
| [`historical/amnezia.md`](historical/amnezia.md), [`historical/awg.md`](historical/awg.md), [`historical/check.md`](historical/check.md), [`historical/install.sh`](historical/install.sh), [`historical/uninstall.sh`](historical/uninstall.sh) | [`docs/amnezia-mihomo-gateway-evolution.md`](../docs/amnezia-mihomo-gateway-evolution.md); актуальный source of truth — [saymer-alt/amnezia-mihomo-gateway](https://github.com/saymer-alt/amnezia-mihomo-gateway) |
| [`historical/moshubrd.md`](historical/moshubrd.md) | [`docs/moshub-entware-mirror.md`](../docs/moshub-entware-mirror.md) (README реального проекта владельца на Mos.Hub; namespace для возможного пилота) |
| [`historical/setup-kvm-motech.sh`](historical/setup-kvm-motech.sh) | аудит — в [`docs/kvm-windows-virtiofs.md`](../docs/kvm-windows-virtiofs.md) §«Аудит»; **исторический артефакт; не утверждён к выполнению** |
| [`historical/MosTech.md`](historical/MosTech.md), [`historical/cloudmos.md`](historical/cloudmos.md), [`historical/class.md`](historical/class.md) | творческий/несвязанный исторический материал; поддерживаемой технической замены нет |

Физическое перемещение выполнено 2026-09-24 (TASK-KB-12) после завершения кампании
содержательного аудита (TASK-KB-08..11); исходные пути в корне репозитория больше не
используются.
