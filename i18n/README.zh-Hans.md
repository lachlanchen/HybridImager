[English](../README.md) · [العربية](README.ar.md) · [Español](README.es.md) · [Français](README.fr.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [Tiếng Việt](README.vi.md) · [中文 (简体)](README.zh-Hans.md) · [中文（繁體）](README.zh-Hant.md) · [Deutsch](README.de.md) · [Русский](README.ru.md)

[![LazyingArt banner](https://github.com/lachlanchen/lachlanchen/raw/main/figs/banner.png)](https://github.com/lachlanchen/lachlanchen/blob/main/figs/banner.png)

# HybridImager

*开放式混合科学成像：把单像素、事件、帧图像和光谱感知放进一个可维护的研究栈。*

[![Website](https://img.shields.io/badge/Website-lazying.art-111827?style=for-the-badge&logo=googlechrome&logoColor=white)](https://lazying.art)
[![Concept Paper](https://img.shields.io/badge/PDF-Concept%20Paper-334155?style=for-the-badge&logo=latex&logoColor=white)](../publications/hybrid_camera_concept.pdf)
[![Survey](https://img.shields.io/badge/PDF-Open%20Camera%20Survey-0f766e?style=for-the-badge&logo=readthedocs&logoColor=white)](../publications/open_camera_project_survey.pdf)
[![GitHub Sponsors](https://img.shields.io/badge/Sponsor-lachlanchen-ea4aaa?style=for-the-badge&logo=githubsponsors&logoColor=white)](https://github.com/sponsors/lachlanchen)

HybridImager 是一个面向混合科学探测器的研究与设计工作区。它把高动态范围单像素桶探测器、事件相机时序、帧相机纹理以及可选光谱测量统一到一个同步数据模型中。

| Donate | PayPal | Stripe |
| --- | --- | --- |
| [![Donate](https://img.shields.io/badge/Donate-LazyingArt-0EA5E9?style=for-the-badge&logo=kofi&logoColor=white)](https://chat.lazying.art/donate) | [![PayPal](https://img.shields.io/badge/PayPal-RongzhouChen-00457C?style=for-the-badge&logo=paypal&logoColor=white)](https://paypal.me/RongzhouChen) | [![Stripe](https://img.shields.io/badge/Stripe-Donate-635BFF?style=for-the-badge&logo=stripe&logoColor=white)](https://buy.stripe.com/aFadR8gIaflgfQV6T4fw400) |

## 系统概念

![Hybrid board layout](../figures/hybrid_board_layout.png)

- **单像素分支：** 中央低噪声探测器/TIA 通路，用于绝对强度、高动态范围、光谱或编码测量。
- **事件分支：** 先使用商用事件相机获取异步时间对比，再在可行时走向开放 FPGA 接口。
- **帧图像分支：** 全局快门模块提供纹理、标定和可读检查图像。
- **融合层：** 带时间戳的数据流，包含曝光、增益、标定配置、触发和图案元数据。

## 当前内容

| 区域 | 位置 |
| --- | --- |
| 概念论文 | `publications/hybrid_camera_concept.pdf` |
| 开放相机项目调研 | `publications/open_camera_project_survey.pdf` |
| 研究笔记 | `references/` |
| 确定性生成图 | `figures/hybrid_board_layout.*`, `figures/hybrid_signal_chain.*` |
| 硬件计划 | `hardware/board_architecture.md` |
| 重建计划 | `algorithms/reconstruction_plan.md` |
| 既有上下文 | `copied-context/` |
| 开放项目镜像 | `external/` git submodule |

## 快速开始

```bash
git clone --recurse-submodules https://github.com/lachlanchen/HybridImager.git
cd HybridImager
make all
```

如果已经克隆：

```bash
git submodule update --init --recursive
make survey
```

## 研究基线

最可靠的开放单像素路径是 **ONE-PIX** 加 **ONE-PIX_hardware**。事件视觉的现实第一步是使用商用事件相机，并结合 **OpenEB**、**jAER**、**v2e** 和 **E2VID**。帧相机硬件可参考 **OneInchEye**、**Antmicro OV9281**、**AXIOM Beta** 和 **Seeed reCamera**。

项目第一阶段不假设自研事件传感器 ASIC。它从开放的板级同步、开放数据格式、可复现实验重建、可复用机械与 PCB 参考开始。

## CAD 与硬件说明

用于可编辑机械设计的 Shapr3D 推荐导出包：

```text
STEP + native .shapr + Parasolid + DXF from sketch + 3MF/STL preview
```

STEP 作为主要交换格式，Parasolid 作为高保真实体备份，DXF 用于二维轮廓和板件，STL/3MF 仅用于打印或网格预览。

## 构建命令

```bash
make figures
make paper
make survey
make all
make clean
```

## 状态

这是早期研究工作区，不是经过认证的成像产品。当前目标是为光学和显微实验建立可维护的流程：用现成模块搭建、干净同步、可重复重建，并在数据契约稳定之后再集成定制硬件。

少造一点，多成像一点。
