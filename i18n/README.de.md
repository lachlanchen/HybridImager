[English](../README.md) · [العربية](README.ar.md) · [Español](README.es.md) · [Français](README.fr.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [Tiếng Việt](README.vi.md) · [中文 (简体)](README.zh-Hans.md) · [中文（繁體）](README.zh-Hant.md) · [Deutsch](README.de.md) · [Русский](README.ru.md)

[![LazyingArt banner](https://github.com/lachlanchen/lachlanchen/raw/main/figs/banner.png)](https://github.com/lachlanchen/lachlanchen/blob/main/figs/banner.png)

# HybridImager

*Offene hybride wissenschaftliche Bildgebung: Einzelpixel, Events, Frames und Spektren in einem wartbaren Forschungs-Stack.*

[![Website](https://img.shields.io/badge/Website-lazying.art-111827?style=for-the-badge&logo=googlechrome&logoColor=white)](https://lazying.art)
[![Concept Paper](https://img.shields.io/badge/PDF-Concept%20Paper-334155?style=for-the-badge&logo=latex&logoColor=white)](../publications/hybrid_camera_concept.pdf)
[![Survey](https://img.shields.io/badge/PDF-Open%20Camera%20Survey-0f766e?style=for-the-badge&logo=readthedocs&logoColor=white)](../publications/open_camera_project_survey.pdf)
[![GitHub Sponsors](https://img.shields.io/badge/Sponsor-lachlanchen-ea4aaa?style=for-the-badge&logo=githubsponsors&logoColor=white)](https://github.com/sponsors/lachlanchen)

HybridImager ist ein Forschungs- und Design-Arbeitsbereich für einen gemischten wissenschaftlichen Detektor. Das Konzept kombiniert einen Einzelpixel-Bucket-Detektor mit hohem Dynamikumfang, Event-Kamera-Timing, Frame-Kamera-Textur und optionale Spektralmessungen in einem synchronisierten Datenmodell.

| Donate | PayPal | Stripe |
| --- | --- | --- |
| [![Donate](https://img.shields.io/badge/Donate-LazyingArt-0EA5E9?style=for-the-badge&logo=kofi&logoColor=white)](https://chat.lazying.art/donate) | [![PayPal](https://img.shields.io/badge/PayPal-RongzhouChen-00457C?style=for-the-badge&logo=paypal&logoColor=white)](https://paypal.me/RongzhouChen) | [![Stripe](https://img.shields.io/badge/Stripe-Donate-635BFF?style=for-the-badge&logo=stripe&logoColor=white)](https://buy.stripe.com/aFadR8gIaflgfQV6T4fw400) |

## Systemkonzept

![Hybrid board layout](../figures/hybrid_board_layout.png)

- **Einzelpixel-Zweig:** zentraler rauscharmer Detektor/TIA-Pfad für absolute Intensität, hohen Dynamikumfang und spektrale oder codierte Messungen.
- **Event-Zweig:** asynchroner zeitlicher Kontrast zuerst mit kommerziellen Event-Kameras, später mit offenen FPGA-Schnittstellen.
- **Frame-Zweig:** Global-Shutter-Module für Textur, Kalibrierung und menschlich lesbare Kontrolle.
- **Fusionsschicht:** Zeitgestempelte Streams mit Belichtung, Gain, Kalibrierprofil, Trigger und Pattern-Metadaten.

## Aktueller Inhalt

| Bereich | Ort |
| --- | --- |
| Konzeptpapier | `publications/hybrid_camera_concept.pdf` |
| Open-Camera-Studie | `publications/open_camera_project_survey.pdf` |
| Forschungsnotizen | `references/` |
| Deterministische Diagramme | `figures/hybrid_board_layout.*`, `figures/hybrid_signal_chain.*` |
| Hardwareplan | `hardware/board_architecture.md` |
| Rekonstruktionsplan | `algorithms/reconstruction_plan.md` |
| Vorheriger Kontext | `copied-context/` |
| Spiegel offener Projekte | `external/` als git submodules |

## Schnellstart

```bash
git clone --recurse-submodules https://github.com/lachlanchen/HybridImager.git
cd HybridImager
make all
```

Wenn das Repository bereits geklont ist:

```bash
git submodule update --init --recursive
make survey
```

## Forschungsbasis

Der stärkste offene Einzelpixel-Pfad ist **ONE-PIX** plus **ONE-PIX_hardware**. Für Event Vision nutzt der realistische erste Aufbau kommerzielle Event-Kameras mit **OpenEB**, **jAER**, **v2e** und **E2VID**. Für Frame-Hardware sind **OneInchEye**, **Antmicro OV9281**, **AXIOM Beta** und **Seeed reCamera** nützliche offene Referenzen.

Das Projekt setzt in der ersten Phase keinen eigenen Event-Sensor-ASIC voraus. Es beginnt mit offener Board-Synchronisation, offenen Datenformaten, reproduzierbarer Rekonstruktion und wiederverwendbaren Mechanik- und PCB-Referenzen.

## CAD- und Hardware-Hinweise

Bevorzugtes Shapr3D-Exportpaket für editierbare Mechanik:

```text
STEP + native .shapr + Parasolid + DXF from sketch + 3MF/STL preview
```

STEP ist das Hauptaustauschformat, Parasolid die hochgenaue Solid-Sicherung, DXF dient 2D-Konturen und Platten, STL/3MF nur Druck oder Mesh-Vorschau.

## Build-Befehle

```bash
make figures
make paper
make survey
make all
make clean
```

## Status

Dies ist ein früher Forschungsarbeitsbereich, kein zertifiziertes Bildgebungsprodukt. Das unmittelbare Ziel ist eine wartbare Experiment-Pipeline für Optik und Mikroskopie: mit verfügbaren Modulen bauen, sauber synchronisieren, reproduzierbar rekonstruieren und kundenspezifische Hardware erst integrieren, wenn der Datenvertrag stabil ist.

Weniger bauen. Mehr abbilden.
