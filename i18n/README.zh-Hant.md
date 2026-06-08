[English](../README.md) · [العربية](README.ar.md) · [Español](README.es.md) · [Français](README.fr.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [Tiếng Việt](README.vi.md) · [中文 (简体)](README.zh-Hans.md) · [中文（繁體）](README.zh-Hant.md) · [Deutsch](README.de.md) · [Русский](README.ru.md)

[![LazyingArt banner](https://github.com/lachlanchen/lachlanchen/raw/main/figs/banner.png)](https://github.com/lachlanchen/lachlanchen/blob/main/figs/banner.png)

# HybridImager

*開放式混合科學成像：把單像素、事件、影格與光譜感知放進一個可維護的研究堆疊。*

[![Website](https://img.shields.io/badge/Website-lazying.art-111827?style=for-the-badge&logo=googlechrome&logoColor=white)](https://lazying.art)
[![Concept Paper](https://img.shields.io/badge/PDF-Concept%20Paper-334155?style=for-the-badge&logo=latex&logoColor=white)](../publications/hybrid_camera_concept.pdf)
[![Survey](https://img.shields.io/badge/PDF-Open%20Camera%20Survey-0f766e?style=for-the-badge&logo=readthedocs&logoColor=white)](../publications/open_camera_project_survey.pdf)
[![GitHub Sponsors](https://img.shields.io/badge/Sponsor-lachlanchen-ea4aaa?style=for-the-badge&logo=githubsponsors&logoColor=white)](https://github.com/sponsors/lachlanchen)

HybridImager 是面向混合科學探測器的研究與設計工作區。它把高動態範圍單像素桶探測器、事件相機時序、影格相機紋理，以及可選光譜測量整合到同一個同步資料模型中。

| Donate | PayPal | Stripe |
| --- | --- | --- |
| [![Donate](https://img.shields.io/badge/Donate-LazyingArt-0EA5E9?style=for-the-badge&logo=kofi&logoColor=white)](https://chat.lazying.art/donate) | [![PayPal](https://img.shields.io/badge/PayPal-RongzhouChen-00457C?style=for-the-badge&logo=paypal&logoColor=white)](https://paypal.me/RongzhouChen) | [![Stripe](https://img.shields.io/badge/Stripe-Donate-635BFF?style=for-the-badge&logo=stripe&logoColor=white)](https://buy.stripe.com/aFadR8gIaflgfQV6T4fw400) |

## 系統概念

![Hybrid board layout](../figures/hybrid_board_layout.png)

- **單像素分支：** 中央低雜訊探測器/TIA 通路，用於絕對強度、高動態範圍、光譜或編碼測量。
- **事件分支：** 先以商用事件相機取得非同步時間對比，再在可行時走向開放 FPGA 介面。
- **影格分支：** 全域快門模組提供紋理、校準與可讀檢查影像。
- **融合層：** 帶時間戳的資料流，包含曝光、增益、校準設定、觸發與圖案中繼資料。

## V1 感測器板

![HybridImager V1 KiCad 渲染](../hardware/v1-weiqi-sensor/artifacts/hybridimager-v1-kicad-render-full.png)

第一版板卡草案是 KiCad 生成的 **圍棋式稀疏感測器載板**，包含 21 個單像素探測器位置，而不是只有一個中央 bucket。它包含每個探測點的訊號焊盤、明確的接地回流、三個 AFE 佔位、一個 QFN 定時佔位、SMA 同步輸入/輸出、電源/同步排針和 2x20 擴充排針。

審查包：[`hardware/v1-weiqi-sensor/`](../hardware/v1-weiqi-sensor/) 包含 KiCad 板、資料集、BOM、乾淨的 DRC、STEP、Gerber、鑽孔檔和完整視角渲染。

## 目前內容

| 區域 | 位置 |
| --- | --- |
| 概念論文 | `publications/hybrid_camera_concept.pdf` |
| 開放相機專案調研 | `publications/open_camera_project_survey.pdf` |
| V1 稀疏感測器板 | `hardware/v1-weiqi-sensor/` |
| 研究筆記 | `references/` |
| 確定性生成圖 | `figures/hybrid_board_layout.*`, `figures/hybrid_signal_chain.*` |
| 硬體計畫 | `hardware/board_architecture.md` |
| 重建計畫 | `algorithms/reconstruction_plan.md` |
| 既有脈絡 | `copied-context/` |
| 開放專案鏡像 | `external/` git submodule |

## 快速開始

```bash
git clone --recurse-submodules https://github.com/lachlanchen/HybridImager.git
cd HybridImager
make all
```

如果已經 clone：

```bash
git submodule update --init --recursive
make survey
```

## 研究基線

最可靠的開放單像素路徑是 **ONE-PIX** 加 **ONE-PIX_hardware**。事件視覺的現實第一步是使用商用事件相機，並結合 **OpenEB**、**jAER**、**v2e** 和 **E2VID**。影格相機硬體可參考 **OneInchEye**、**Antmicro OV9281**、**AXIOM Beta** 和 **Seeed reCamera**。

專案第一階段不假設自研事件感測器 ASIC。它從開放的板級同步、開放資料格式、可重複實驗重建、可複用機械與 PCB 參考開始。

## CAD 與硬體說明

用於可編輯機械設計的 Shapr3D 推薦匯出包：

```text
STEP + native .shapr + Parasolid + DXF from sketch + 3MF/STL preview
```

STEP 作為主要交換格式，Parasolid 作為高保真實體備份，DXF 用於二維輪廓和板件，STL/3MF 僅用於列印或網格預覽。

## 建置命令

```bash
make figures
make paper
make survey
make all
make clean
```

## 引用

如果在研究中使用 HybridImager，請引用本倉庫。GitHub 會讀取 [CITATION.cff](../CITATION.cff)，並在倉庫頁面顯示 **Cite this repository** 面板。

```bibtex
@software{chen_hybridimager_2026,
  author = {Chen, Lachlan},
  title = {HybridImager: Open Hybrid Scientific Imaging Research Workspace},
  year = {2026},
  url = {https://github.com/lachlanchen/HybridImager}
}
```

## 狀態

這是早期研究工作區，不是經過認證的成像產品。當前目標是為光學與顯微實驗建立可維護的流程：用現成模組搭建、乾淨同步、可重複重建，並在資料契約穩定之後再整合客製硬體。

少造一點，多成像一點。
