[English](README.md) · [العربية](i18n/README.ar.md) · [Español](i18n/README.es.md) · [Français](i18n/README.fr.md) · [日本語](i18n/README.ja.md) · [한국어](i18n/README.ko.md) · [Tiếng Việt](i18n/README.vi.md) · [中文 (简体)](i18n/README.zh-Hans.md) · [中文（繁體）](i18n/README.zh-Hant.md) · [Deutsch](i18n/README.de.md) · [Русский](i18n/README.ru.md)

[![LazyingArt banner](https://github.com/lachlanchen/lachlanchen/raw/main/figs/banner.png)](https://github.com/lachlanchen/lachlanchen/blob/main/figs/banner.png)

# HybridImager

*Open hybrid scientific imaging: single-pixel, event, frame, and spectral sensing in one maintainable research stack.*

[![Website](https://img.shields.io/badge/Website-lazying.art-111827?style=for-the-badge&logo=googlechrome&logoColor=white)](https://lazying.art)
[![Concept Paper](https://img.shields.io/badge/PDF-Concept%20Paper-334155?style=for-the-badge&logo=latex&logoColor=white)](publications/hybrid_camera_concept.pdf)
[![Survey](https://img.shields.io/badge/PDF-Open%20Camera%20Survey-0f766e?style=for-the-badge&logo=readthedocs&logoColor=white)](publications/open_camera_project_survey.pdf)
[![GitHub Sponsors](https://img.shields.io/badge/Sponsor-lachlanchen-ea4aaa?style=for-the-badge&logo=githubsponsors&logoColor=white)](https://github.com/sponsors/lachlanchen)

HybridImager is a research and design workspace for a mixed scientific detector. The concept combines a high-dynamic-range single-pixel bucket detector, event-camera timing, frame-camera texture, and optional spectral measurements under one synchronized data model.

| Donate | PayPal | Stripe |
| --- | --- | --- |
| [![Donate](https://img.shields.io/badge/Donate-LazyingArt-0EA5E9?style=for-the-badge&logo=kofi&logoColor=white)](https://chat.lazying.art/donate) | [![PayPal](https://img.shields.io/badge/PayPal-RongzhouChen-00457C?style=for-the-badge&logo=paypal&logoColor=white)](https://paypal.me/RongzhouChen) | [![Stripe](https://img.shields.io/badge/Stripe-Donate-635BFF?style=for-the-badge&logo=stripe&logoColor=white)](https://buy.stripe.com/aFadR8gIaflgfQV6T4fw400) |

## System Concept

![Hybrid board layout](figures/hybrid_board_layout.png)

- **Single-pixel branch:** a central low-noise detector/TIA path for absolute intensity, high dynamic range, and spectral or coded measurements.
- **Event branch:** asynchronous temporal contrast from commercial event cameras first, then open FPGA interfaces when practical.
- **Frame branch:** global-shutter frame modules for texture, calibration, and human-readable inspection.
- **Fusion layer:** timestamped streams with exposure, gain, calibration profile, trigger, and pattern metadata.

## V1 Sensor Board

![HybridImager V1 KiCad render](hardware/v1-weiqi-sensor/artifacts/hybridimager-v1-kicad-render-full.png)

The first board draft is a KiCad-generated **Weiqi sparse sensor carrier** with 21 single-pixel detector sites, not one central bucket only. It includes per-site signal pads, explicit ground routing, three AFE placeholders, a QFN timing placeholder, SMA sync in/out, power/sync header, and a 2x20 expansion header for later event/frame/tile work.

Review package: [`hardware/v1-weiqi-sensor/`](hardware/v1-weiqi-sensor/) contains the KiCad board, dataset, BOM, clean DRC JSON, STEP model, Gerbers, drill files, and full-view renders.

## Current Contents

| Area | Location |
| --- | --- |
| Concept paper | `publications/hybrid_camera_concept.pdf` |
| Open camera survey | `publications/open_camera_project_survey.pdf` |
| V1 sparse sensor board | `hardware/v1-weiqi-sensor/` |
| Research notes | `references/` |
| Deterministic diagrams | `figures/hybrid_board_layout.*`, `figures/hybrid_signal_chain.*` |
| Hardware plan | `hardware/board_architecture.md` |
| Reconstruction plan | `algorithms/reconstruction_plan.md` |
| Prior context | `copied-context/` |
| Open project mirrors | `external/` as git submodules |

## Quick Start

```bash
git clone --recurse-submodules https://github.com/lachlanchen/HybridImager.git
cd HybridImager
make all
```

If the repository is already cloned:

```bash
git submodule update --init --recursive
make survey
```

## Research Baseline

The strongest open single-pixel path is **ONE-PIX** plus **ONE-PIX_hardware**. For event vision, the realistic first build uses commercial event cameras with **OpenEB**, **jAER**, **v2e**, and **E2VID**. For frame hardware, the useful open references are **OneInchEye**, **Antmicro OV9281**, **AXIOM Beta**, and **Seeed reCamera**.

The project does not assume a custom event-sensor ASIC in the first stage. It starts with open board-level synchronization, open data formats, open reconstruction, and reusable mechanical/PCB references.

## CAD And Hardware Notes

Preferred Shapr3D export package for editable mechanical work:

```text
STEP + native .shapr + Parasolid + DXF from sketch + 3MF/STL preview
```

Use STEP as the main interchange format, Parasolid as the high-fidelity solid backup, DXF for 2D outlines and plates, and STL/3MF only for print or mesh preview.

## Build Commands

```bash
make figures   # regenerate deterministic diagrams
make paper     # compile the HybridImager concept paper
make survey    # compile the open camera project survey
make all       # run paper and survey builds
make clean     # remove LaTeX build byproducts
```

## Citation

If you use HybridImager in research, cite the repository. GitHub reads [CITATION.cff](CITATION.cff) and shows a **Cite this repository** panel on the repo page.

```bibtex
@software{chen_hybridimager_2026,
  author = {Chen, Lachlan},
  title = {HybridImager: Open Hybrid Scientific Imaging Research Workspace},
  year = {2026},
  url = {https://github.com/lachlanchen/HybridImager}
}
```

## Status

This is an early research workspace, not a certified imaging product. The immediate goal is a maintainable experiment pipeline for optical and microscopy setups: build with available modules, synchronize cleanly, reconstruct reproducibly, and only integrate custom hardware after the data contract is stable.

Build less. Image more.
