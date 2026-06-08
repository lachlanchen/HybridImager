[English](../README.md) · [العربية](README.ar.md) · [Español](README.es.md) · [Français](README.fr.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [Tiếng Việt](README.vi.md) · [中文 (简体)](README.zh-Hans.md) · [中文（繁體）](README.zh-Hant.md) · [Deutsch](README.de.md) · [Русский](README.ru.md)

[![LazyingArt banner](https://github.com/lachlanchen/lachlanchen/raw/main/figs/banner.png)](https://github.com/lachlanchen/lachlanchen/blob/main/figs/banner.png)

# HybridImager

*단일 픽셀, 이벤트, 프레임, 스펙트럼 감지를 하나의 유지 가능한 연구 스택으로 묶는 오픈 하이브리드 과학 이미징.*

[![Website](https://img.shields.io/badge/Website-lazying.art-111827?style=for-the-badge&logo=googlechrome&logoColor=white)](https://lazying.art)
[![Concept Paper](https://img.shields.io/badge/PDF-Concept%20Paper-334155?style=for-the-badge&logo=latex&logoColor=white)](../publications/hybrid_camera_concept.pdf)
[![Survey](https://img.shields.io/badge/PDF-Open%20Camera%20Survey-0f766e?style=for-the-badge&logo=readthedocs&logoColor=white)](../publications/open_camera_project_survey.pdf)
[![GitHub Sponsors](https://img.shields.io/badge/Sponsor-lachlanchen-ea4aaa?style=for-the-badge&logo=githubsponsors&logoColor=white)](https://github.com/sponsors/lachlanchen)

HybridImager는 혼합 과학 검출기를 위한 연구 및 설계 작업 공간입니다. 고동적 범위 단일 픽셀 버킷 검출기, 이벤트 카메라 타이밍, 프레임 카메라 텍스처, 선택적 스펙트럼 측정을 하나의 동기화된 데이터 모델로 결합합니다.

| Donate | PayPal | Stripe |
| --- | --- | --- |
| [![Donate](https://img.shields.io/badge/Donate-LazyingArt-0EA5E9?style=for-the-badge&logo=kofi&logoColor=white)](https://chat.lazying.art/donate) | [![PayPal](https://img.shields.io/badge/PayPal-RongzhouChen-00457C?style=for-the-badge&logo=paypal&logoColor=white)](https://paypal.me/RongzhouChen) | [![Stripe](https://img.shields.io/badge/Stripe-Donate-635BFF?style=for-the-badge&logo=stripe&logoColor=white)](https://buy.stripe.com/aFadR8gIaflgfQV6T4fw400) |

## 시스템 개념

![Hybrid board layout](../figures/hybrid_board_layout.png)

- **단일 픽셀 브랜치:** 절대 강도, 고동적 범위, 스펙트럼 또는 부호화 측정을 위한 중앙 저잡음 검출기/TIA 경로입니다.
- **이벤트 브랜치:** 먼저 상용 이벤트 카메라로 비동기 시간 대비를 사용하고, 가능해지면 오픈 FPGA 인터페이스로 확장합니다.
- **프레임 브랜치:** 텍스처, 보정, 사람이 확인할 수 있는 검사를 위한 글로벌 셔터 프레임 모듈입니다.
- **퓨전 레이어:** 노출, 게인, 보정 프로파일, 트리거, 패턴 메타데이터를 포함하는 타임스탬프 스트림입니다.

## 현재 내용

| 영역 | 위치 |
| --- | --- |
| 개념 논문 | `publications/hybrid_camera_concept.pdf` |
| 오픈 카메라 조사 | `publications/open_camera_project_survey.pdf` |
| 연구 노트 | `references/` |
| 결정론적 다이어그램 | `figures/hybrid_board_layout.*`, `figures/hybrid_signal_chain.*` |
| 하드웨어 계획 | `hardware/board_architecture.md` |
| 재구성 계획 | `algorithms/reconstruction_plan.md` |
| 이전 맥락 | `copied-context/` |
| 오픈 프로젝트 미러 | `external/` git submodule |

## 빠른 시작

```bash
git clone --recurse-submodules https://github.com/lachlanchen/HybridImager.git
cd HybridImager
make all
```

이미 클론한 경우:

```bash
git submodule update --init --recursive
make survey
```

## 연구 기준선

가장 강한 오픈 단일 픽셀 경로는 **ONE-PIX**와 **ONE-PIX_hardware**입니다. 이벤트 비전의 현실적인 첫 빌드는 상용 이벤트 카메라와 **OpenEB**, **jAER**, **v2e**, **E2VID**를 사용합니다. 프레임 하드웨어에는 **OneInchEye**, **Antmicro OV9281**, **AXIOM Beta**, **Seeed reCamera**가 유용한 오픈 참고 자료입니다.

이 프로젝트는 첫 단계에서 맞춤형 이벤트 센서 ASIC을 전제로 하지 않습니다. 먼저 보드 수준 동기화, 오픈 데이터 형식, 재현 가능한 재구성, 재사용 가능한 기계/PCB 참고 자료에서 시작합니다.

## CAD 및 하드웨어 노트

편집 가능한 기계 작업을 위한 Shapr3D 권장 내보내기 패키지:

```text
STEP + native .shapr + Parasolid + DXF from sketch + 3MF/STL preview
```

STEP은 기본 교환 형식, Parasolid는 고충실도 솔리드 백업, DXF는 2D 외곽선과 판재, STL/3MF는 출력 또는 메시 미리보기 전용으로 사용합니다.

## 빌드 명령

```bash
make figures
make paper
make survey
make all
make clean
```

## 인용

연구에서 HybridImager를 사용한다면 이 저장소를 인용하세요. GitHub는 [CITATION.cff](../CITATION.cff)를 읽어 저장소 페이지에 **Cite this repository** 패널을 표시합니다.

```bibtex
@software{chen_hybridimager_2026,
  author = {Chen, Lachlan},
  title = {HybridImager: Open Hybrid Scientific Imaging Research Workspace},
  year = {2026},
  url = {https://github.com/lachlanchen/HybridImager}
}
```

## 상태

이 저장소는 초기 연구 작업 공간이며 인증된 이미징 제품이 아닙니다. 즉각적인 목표는 광학 및 현미경 실험을 위한 유지 가능한 파이프라인입니다. 사용 가능한 모듈로 만들고, 깨끗하게 동기화하고, 재현 가능하게 재구성하며, 데이터 계약이 안정된 뒤에만 맞춤형 하드웨어를 통합합니다.

덜 만들고, 더 많이 이미징합니다.
