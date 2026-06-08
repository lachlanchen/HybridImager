[English](../README.md) · [العربية](README.ar.md) · [Español](README.es.md) · [Français](README.fr.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [Tiếng Việt](README.vi.md) · [中文 (简体)](README.zh-Hans.md) · [中文（繁體）](README.zh-Hant.md) · [Deutsch](README.de.md) · [Русский](README.ru.md)

[![LazyingArt banner](https://github.com/lachlanchen/lachlanchen/raw/main/figs/banner.png)](https://github.com/lachlanchen/lachlanchen/blob/main/figs/banner.png)

# HybridImager

*Открытая гибридная научная визуализация: один пиксель, события, кадры и спектр в поддерживаемом исследовательском стеке.*

[![Website](https://img.shields.io/badge/Website-lazying.art-111827?style=for-the-badge&logo=googlechrome&logoColor=white)](https://lazying.art)
[![Concept Paper](https://img.shields.io/badge/PDF-Concept%20Paper-334155?style=for-the-badge&logo=latex&logoColor=white)](../publications/hybrid_camera_concept.pdf)
[![Survey](https://img.shields.io/badge/PDF-Open%20Camera%20Survey-0f766e?style=for-the-badge&logo=readthedocs&logoColor=white)](../publications/open_camera_project_survey.pdf)
[![GitHub Sponsors](https://img.shields.io/badge/Sponsor-lachlanchen-ea4aaa?style=for-the-badge&logo=githubsponsors&logoColor=white)](https://github.com/sponsors/lachlanchen)

HybridImager — это исследовательская и проектная среда для смешанного научного детектора. Концепция объединяет однопиксельный bucket-детектор с высоким динамическим диапазоном, тайминг событийной камеры, текстуру кадровой камеры и дополнительные спектральные измерения в одной синхронизированной модели данных.

| Donate | PayPal | Stripe |
| --- | --- | --- |
| [![Donate](https://img.shields.io/badge/Donate-LazyingArt-0EA5E9?style=for-the-badge&logo=kofi&logoColor=white)](https://chat.lazying.art/donate) | [![PayPal](https://img.shields.io/badge/PayPal-RongzhouChen-00457C?style=for-the-badge&logo=paypal&logoColor=white)](https://paypal.me/RongzhouChen) | [![Stripe](https://img.shields.io/badge/Stripe-Donate-635BFF?style=for-the-badge&logo=stripe&logoColor=white)](https://buy.stripe.com/aFadR8gIaflgfQV6T4fw400) |

## Концепция системы

![Hybrid board layout](../figures/hybrid_board_layout.png)

- **Однопиксельная ветка:** центральный малошумящий детектор/TIA для абсолютной интенсивности, высокого динамического диапазона, спектральных или кодированных измерений.
- **Событийная ветка:** асинхронный временной контраст сначала с коммерческими событийными камерами, затем с открытыми FPGA-интерфейсами.
- **Кадровая ветка:** модули с глобальным затвором для текстуры, калибровки и читаемой проверки.
- **Слой слияния:** потоки с временными метками, экспозицией, усилением, профилем калибровки, триггером и метаданными паттерна.

## Текущее содержимое

| Область | Расположение |
| --- | --- |
| Концептуальная статья | `publications/hybrid_camera_concept.pdf` |
| Обзор открытых камер | `publications/open_camera_project_survey.pdf` |
| Исследовательские заметки | `references/` |
| Детерминированные схемы | `figures/hybrid_board_layout.*`, `figures/hybrid_signal_chain.*` |
| План аппаратуры | `hardware/board_architecture.md` |
| План реконструкции | `algorithms/reconstruction_plan.md` |
| Предыдущий контекст | `copied-context/` |
| Зеркала открытых проектов | `external/` как git submodules |

## Быстрый старт

```bash
git clone --recurse-submodules https://github.com/lachlanchen/HybridImager.git
cd HybridImager
make all
```

Если репозиторий уже клонирован:

```bash
git submodule update --init --recursive
make survey
```

## Исследовательская база

Самый сильный открытый путь для однопиксельной системы — **ONE-PIX** плюс **ONE-PIX_hardware**. Для событийного зрения реалистичная первая сборка использует коммерческие событийные камеры с **OpenEB**, **jAER**, **v2e** и **E2VID**. Для кадровой аппаратуры полезны открытые ссылки **OneInchEye**, **Antmicro OV9281**, **AXIOM Beta** и **Seeed reCamera**.

Проект не предполагает собственный ASIC событийного сенсора на первом этапе. Он начинается с открытой синхронизации на уровне платы, открытых форматов данных, воспроизводимой реконструкции и повторно используемых механических/PCB-референсов.

## CAD и аппаратные заметки

Предпочтительный экспорт из Shapr3D для редактируемой механики:

```text
STEP + native .shapr + Parasolid + DXF from sketch + 3MF/STL preview
```

STEP используется как основной формат обмена, Parasolid как высокоточная solid-резервная копия, DXF для 2D-контуров и пластин, а STL/3MF только для печати или просмотра сетки.

## Команды сборки

```bash
make figures
make paper
make survey
make all
make clean
```

## Цитирование

Если вы используете HybridImager в исследовании, процитируйте этот репозиторий. GitHub читает [CITATION.cff](../CITATION.cff) и показывает панель **Cite this repository** на странице репозитория.

```bibtex
@software{chen_hybridimager_2026,
  author = {Chen, Lachlan},
  title = {HybridImager: Open Hybrid Scientific Imaging Research Workspace},
  year = {2026},
  url = {https://github.com/lachlanchen/HybridImager}
}
```

## Статус

Это ранняя исследовательская среда, а не сертифицированный продукт визуализации. Ближайшая цель — поддерживаемый экспериментальный pipeline для оптики и микроскопии: строить из доступных модулей, чисто синхронизировать, воспроизводимо реконструировать и интегрировать кастомную аппаратуру только после стабилизации контракта данных.

Меньше строить. Больше видеть.
