# KVM/libvirt → Windows-гость → общая папка хоста через VirtIO-FS

**Статус:** Confirmed (механика хоста и гостя — по документации libvirt и исходникам
virtio-win/WinFSP, проверено 2026-09-24) + Observed (связка воспроизводилась владельцем
на трёх машинах, среда MosTech/ALT — историческое наблюдение) + Historical (утверждения
raw-файлов, не совпавшие с текущими источниками)  
**Область применения:** Linux-хост KVM/libvirt/virt-manager, Windows 10-гость; задача
«дать гостю доступ к каталогу хоста с локальной ФС-семантикой»  
**Проверено на:** [libvirt formatdomain](https://libvirt.org/formatdomain.html) и
[kbase/virtiofs](https://libvirt.org/kbase/virtiofs.html); исходники
`virtio-win/kvm-guest-drivers-windows` (`viofs/svc/virtiofs.cpp`) и `winfsp/winfsp`
(`src/dll/mount.c`, `src/dll/fs.c`); пакетные индексы ALT/Debian/Fedora — всё
2026-09-24  
**Последняя проверка:** 2026-09-24  
**Source of truth:** документация libvirt; код virtio-win и WinFSP; для среды
MosTech — только наблюдения владельца  
**Provenance:** raw-файлы этого репозитория
[`VirtIO-FS.md`](../archive/raw/VirtIO-FS.md), [`virtiofsd.md`](../archive/raw/virtiofsd.md),
[`MosTech_cifrovoj.md`](../archive/raw/MosTech_cifrovoj.md); аудит
[`setup-kvm-motech.sh`](../archive/historical/setup-kvm-motech.sh) — раздел ниже

## Что решаем

Windows-приложение не бежит на Linux-хосте; его кладут в KVM-гость, и ему нужен доступ
к каталогу хоста. Классические варианты (Samba, эмулируемая сетевая папка) дают
сетевую семантику; **VirtIO-FS** — sharing с локальной ФС-семантикой и
производительностью. Эта статья фиксирует рабочий путь и его требования, а также то,
что в старых raw-заметках оказалось историческим.

Среда MosTech (ALT Linux в корпоративном костюме) здесь — только provenance:
наблюдения владельца из этой среды не универсальны для всех дистрибутивов.

## Требования (хост)

- KVM + libvirt + virt-manager/virt-install;
- **virtiofsd** — vhost-user-демон, который libvirt запускает как бэкенд устройства
  virtiofs (элемент `<binary path=.../>` в XML; по умолчанию libvirt ищет его сам);
- общий каталог на хосте, читаемый процессом qemu (учёт прав/SELinux — стандартные
  для libvirt-передачи каталогов).

**Упаковка virtiofsd — дистро-специфична.** В текущих индексах это отдельный пакет:
ALT Sisyphus/p11 — `virtiofsd` («Virtio-fs vhost-user device daemon (Rust version)»),
Debian — `virtiofsd`, Fedora — `virtiofsd`. Старая наблюдение владельца «в MosTech
virtiofsd не находился ни как `virtiofsd`, ни как `virtio-fs`, был спрятан внутри
`qemu-kvm`» — **Historical**: с текущим ALT-индексом не согласуется (возможно,
отражает старый образ/патченный репозиторий). Имя пакета не универсально — сверять
со своим дистрибутивом.

## Требование разделяемой памяти (ключевой пункт)

VirtIO-FS — vhost-user-устройство: оно реализуется процессом virtiofsd вне QEMU, и
QEMU **должен выделять память гостя как разделяемую**. libvirt формулирует это прямо:
«Using virtiofs requires setting up shared memory» и «Don't forget the
`<memoryBacking>` elements. They are necessary for the vhost-user connection with the
virtiofsd daemon».

Рекомендуемая конфигурация (из kbase libvirt):

```xml
<memoryBacking>
  <source type='memfd'/>
  <access mode='shared'/>
</memoryBacking>
```

Альтернативы — file-backed memory (`memory_backing_dir` в `qemu.conf`) и
hugepages; memfd не требует подготовки хоста и рекомендуется по умолчанию. В
`virt-manager` этому соответствует галочка **«Enable shared memory»** в свойствах
памяти ВМ. Забытая разделяемая память — самая частая причина «устройство добавил, а
гость не стартует/не видит ФС».

## Устройство filesystem: source и mount tag

```xml
<filesystem type='mount' accessmode='passthrough'>
  <driver type='virtiofs' queue='1024'/>
  <source dir='/path/on/host'/>
  <target dir='mount_tag'/>
  <!-- опционально: <readonly/>; <binary path='/usr/libexec/virtiofsd' xattr='on'/> -->
</filesystem>
```

Документация libvirt фиксирует семантику: `source dir` — каталог хоста;
`target dir` — **не путь в госте**, а произвольная строка-тег:

> «Note that despite its name, the target dir is an arbitrary string called a mount
> tag that is used inside the guest to identify the shared file system to be mounted.
> It does not have to correspond to the desired mount point in the guest.»

(Cf. примечание libvirt: virtiofs-драйвер поддерживается с libvirt 6.2.0; версии
virtiofsd до 1.11 не поддерживают миграцию — migration/save/snapshots-with-memory
ограничены, это фиксировать при эксплуатации.)

## Сторона Windows-гостя

1. **WinFSP** — жёсткая зависимость: сервис virtio-win собирается против
   `winfsp/winfsp.h` и вызывает `FSP_*`-API; при невозможности загрузить WinFSP сервис
   сообщает об ошибке (обработка присутствует в исходнике). Устанавливать до/вместе с
   гостевыми компонентами.
2. **virtio-win guest tools** — включают драйвер `viofs` и **сервис
   «VirtIO-FS»**; сервис берёт тег из устройства, подключается к virtio-fs-устройству
   и монтирует ФС как диск.
3. Логин/просмотр: после запуска сервиса общая папка появляется как диск в
   «Этот компьютер».

## Поведение точки монтирования и буквы диска (проверено по исходникам)

Сервис читает параметры реестра при старте из **`HKLM\SOFTWARE\Virtio-FS`** (имя
ключа в исходнике: `Software\` + `VirtIO-FS`): `MountPoint`, `DebugFlags`,
`DebugLogFile`, `CaseInsensitive`, `FileSystemName`, `Owner`, `OverflowUid/Gid` и др.

- Дефолт `MountPoint` = `*`; при `*` сервис вызывает
  `FspFileSystemSetMountPoint(FileSystem, NULL)`, а WinFSP подставляет wildcard
  `*:` и ищет свободную букву **перебором от `Z` вниз к `D`**, беря первую незанятую
  (исходник WinFSP, `mount.c`: `for (Drive = 'Z'; 'D' <= Drive; Drive--)`).
- Отсюда практические следствия: на типичной системе первая свободная буква при
  таком переборе действительно `Z:` (что объясняет наблюдаемый «дефолт Z:»), но
  **это не жёсткий дефолт**: если `Z:` занят, WinFSP возьмёт `Y:`, `X:` и т. д., а
  не упадёт.
- Переназначить букву можно значением `MountPoint` (строковое, например `Y:`) в
  `HKLM\SOFTWARE\Virtio-FS` с последующим перезапуском сервиса «VirtIO-FS» в
  `services.msc`.

**Historical (не переносить в актуальные инструкции):** raw-файл утверждал, что
буква «жёстко прописана» на `Z:` и при её занятости сервис «молча отвалится», а ключ
реестра находится в `HKLM\SOFTWARE\Virtio-FS\Service`. Текущим исходникам это не
соответствует: дефолт — автоперебор Z→D, а ключ — без подветки `Service`
(возможно, старая версия сборки или неточность воспоминания). Механика «строковый
параметр `MountPoint` + перезапуск сервиса» подтверждается текущим кодом — меняется
только точный путь.

## Проверка

```text
гость:   services.msc → VirtIO-FS Service запущен; диск с общей папкой в «Этот компьютер»
хост:    ps aux | grep virtiofsd   # процесс, запущенный libvirt для этой ВМ
смысловое: создать файл в госте → он появляется в каталоге хоста (и наоборот)
```

Проверка целостности шага — файл в обе стороны; «диск появился» без записи не
доказывает работоспособность прав.

## Типичные проблемы

### ВМ не стартует / устройство не появляется

Пропущена разделяемая память (`memoryBacking`/галочка shared memory). Проверить XML:
`virsh dumpxml <vm> | grep -A2 memoryBacking`.

### Сервис в госте не поднимает диск

Нет WinFSP (жёсткая зависимость), не запущен сервис, другой тег (`target dir` в
libvirt и ожидания сервиса), `virtiofsd` отсутствует на хосте. Диагностика: журнал
сервиса Windows, `DebugLogFile` в ключе реестра сервиса.

### Видео/драйверы гостя

Historical/Observed из среды владельца: QXL-драйвер не вставал на Windows 10 c
Secure Boot; рабочий обход — ВМ с UEFI без secboot и порядок «сначала драйверы
virtio-win и SPICE Guest Tools, потом Windows Update». Это наблюдение конкретной
среды/эпохи, не универсальное правило (сверять со своим гипервизором/версиями).

### Медленная альтернатива: Samba

Samba на хосте — работоспособная альтернативная архитектура (сетевая семантика, не
локальная ФС). Старые raw-заметки предлагали `chmod 777`, `guest ok = yes` и
`force user` как путь «чтобы работало» — **так и не оставлять**: world-writable
каталоги и гостевой доступ — не рекомендуемый дефолт; при необходимости Samba
настраивается с обычными правами владельца и аутентификацией. Здесь подробно не
разбирается — статья про VirtIO-FS.

## Аудит `setup-kvm-motech.sh` (static review, не выполнялся)

Скрипт готовит хост (root): ставит KVM-пакеты, включает `libvirtd`, настраивает
сокет (`unix_sock_group "libvirt"`, `unix_sock_rw_perms "0770"`,
`auth_unix_rw "polkit"`), добавляет выбранного пользователя в группу `libvirt` и
кладёт polkit-правило. Он **не** ставит virtiofsd/WinFSP/гостевые компоненты — это
только провижининг доступа к virt-manager.

| Серьёзность | Находка |
| --- | --- |
| **High** | Polkit-правило `49-libvirt-mostech.rules` возвращает `polkit.Result.YES` для `org.libvirt.unix.manage` **любому члену группы `libvirt` безусловно**. Это полный доступ к API libvirtd: создание/уничтожение/правка произвольных ВМ, управление сетями libvirt, проброс хостовых устройств, filesystem-passthrough (virtiofs/9p — доступ к каталогам хоста в рамках прав qemu). В сочетании с `unix_sock_rw_perms 0770` группа и так на RW-сокете — правило убирает последний интерактивный контроль. Эффективно это делегирование power, сопоставимого с root в управляемой libvirt области хоста; в многопользовательской/доменной среде — путь повышения привилегий. Приемлемо только как осознанное решение для доверенных рабочих мест; скрипт этот security-scope нигде не документирует |
| **Medium** | Дистро-привязка: `dnf install` + пакеты с именами `lib64*` (gir/gstreamer/spice) — стиль семейства OpenMandriva; на других дистрибутивах скрипт падает или ставит лишнее, `set -e` останавливает его в произвольной точке без отката |
| **Medium** | Нет бэкапа/отката: `set_conf` правит `libvirtd.conf` `sed -i` на месте и **молча перезаписывает** существующие пользовательские значения трёх ключей; polkit-файл перезаписывается целиком; undo-путь не описан |
| **Low** | Поиск целевого пользователя (`who`/`last -s -30days`//etc/passwd) может поднимать устаревшие/служебные учётки (смягчено интерактивным подтверждением; организации-специфичные исключения `lroot`/`leaderpc` захардкожены) |
| **Low** | Монолитный `libvirtd.service` (на новых libvirt — модульные демоны); `systemctl restart polkit` не нужен (rules.d перечитывается) и может дёрнуть чужие policy-решения; `egrep` устарел; проверка только `vmx|svm` в cpuinfo без проверки загруженного модуля kvm; идемпотентность в целом есть, но `gpasswd -a` при повторном запуске шумит; автозапуск сети `default` не проверяется |

Автоматически скрипт не правился и правиться не должен до явной задачи владельца;
до разбора находок считать его **не утверждённым к выполнению**.

## Что подтверждено, а что нет

**Confirmed:**

- разделяемая память обязательна (`memoryBacking` memfd+shared; virt-manager —
  «Enable shared memory»), формулировка и XML — документация libvirt;
- `source dir` = каталог хоста, `target dir` = mount-tag-строка, а не путь гостя
  (дословно из kbase);
- virtiofsd — vhost-user-демон-бэкенд; virtiofs-драйвер libvirt с 6.2.0; ограничения
  миграции до virtiofsd 1.11;
- WinFSP — жёсткая зависимость сервиса; сервис «VirtIO-FS» читает `MountPoint` и
  др. из `HKLM\SOFTWARE\Virtio-FS`; дефолт `*`; WinFSP выбирает букву перебором
  Z→D (исходники virtio-win/WinFSP);
- virtiofsd как отдельный пакет существует в текущих ALT/Debian/Fedora.

**Observed:**

- владелец воспроизводил связку KVM+Windows 10+VirtIO-FS (shared memory + guest
  сервис) на трёх машинах в среде MosTech/ALT; диск появлялся с `Z:`; потребовались
  повторные попытки (сервис/перезагрузка).

**Historical:**

- «буква жёстко Z:, при конфликте сервис падает» — противоречит текущему WinFSP
  (автоперебор Z→D);
- путь реестра `...\Virtio-FS\Service` — в текущем исходнике ключ без `Service`;
- «virtiofsd спрятан внутри `qemu-kvm`» — с текущим ALT-индексом не согласуется.

**Research / не проверялось:**

- поведение на других дистрибутивах/версиях; точные версии сборок virtio-win, с
  которыми работал владелец; производительность против Samba в конкретных сценариях.

## Источники и provenance

- [libvirt: formatdomain — Filesystems](https://libvirt.org/formatdomain.html)
  (virtiofs с 6.2.0, shared memory, mount tag, `<binary path=...virtiofsd>`).
- [libvirt kbase: Sharing files with Virtiofs](https://libvirt.org/kbase/virtiofs.html)
  (memoryBacking XML, «Don't forget the memoryBacking elements», tag-семантика,
  миграция до 1.11, guest kernel 5.4+).
- [virtio-win/kvm-guest-drivers-windows → viofs/svc/virtiofs.cpp](https://github.com/virtio-win/kvm-guest-drivers-windows/blob/main/viofs/svc/virtiofs.cpp)
  (`FS_SERVICE_NAME`, `FS_SERVICE_REGKEY`, `ParseRegistry`, `MountPoint{L"*"}`,
  WinFSP-зависимость).
- [winfsp/winfsp → src/dll/fs.c, src/dll/mount.c](https://github.com/winfsp/winfsp)
  (`FspFileSystemSetMountPoint`, wildcard `*:` → перебор `Z`→`D`).
- Пакетные индексы: [packages.altlinux.org → virtiofsd](https://packages.altlinux.org/en/sisyphus/srpms/virtiofsd/),
  [packages.debian.org → virtiofsd](https://packages.debian.org/sid/virtiofsd),
  [src.fedoraproject.org/rpms/virtiofsd](https://src.fedoraproject.org/rpms/virtiofsd).
- Raw: [`VirtIO-FS.md`](../archive/raw/VirtIO-FS.md), [`virtiofsd.md`](../archive/raw/virtiofsd.md),
  [`MosTech_cifrovoj.md`](../archive/raw/MosTech_cifrovoj.md),
  [`setup-kvm-motech.sh`](../archive/historical/setup-kvm-motech.sh) — исторические/raw-материалы.

## Связанные материалы

- [INVENTORY.md](../INVENTORY.md) — статусы всех файлов MosTech-кластера.
- [docs/dpi-diagnostics-map.md](dpi-diagnostics-map.md) — пример другого
  методологического разбора в этом репозитории.
