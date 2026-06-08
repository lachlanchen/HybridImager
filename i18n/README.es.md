[English](../README.md) · [العربية](README.ar.md) · [Español](README.es.md) · [Français](README.fr.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [Tiếng Việt](README.vi.md) · [中文 (简体)](README.zh-Hans.md) · [中文（繁體）](README.zh-Hant.md) · [Deutsch](README.de.md) · [Русский](README.ru.md)

[![LazyingArt banner](https://github.com/lachlanchen/lachlanchen/raw/main/figs/banner.png)](https://github.com/lachlanchen/lachlanchen/blob/main/figs/banner.png)

# HybridImager

*Imagen científica híbrida y abierta: píxel único, eventos, fotogramas y espectro en una pila de investigación mantenible.*

[![Website](https://img.shields.io/badge/Website-lazying.art-111827?style=for-the-badge&logo=googlechrome&logoColor=white)](https://lazying.art)
[![Concept Paper](https://img.shields.io/badge/PDF-Concept%20Paper-334155?style=for-the-badge&logo=latex&logoColor=white)](../publications/hybrid_camera_concept.pdf)
[![Survey](https://img.shields.io/badge/PDF-Open%20Camera%20Survey-0f766e?style=for-the-badge&logo=readthedocs&logoColor=white)](../publications/open_camera_project_survey.pdf)
[![GitHub Sponsors](https://img.shields.io/badge/Sponsor-lachlanchen-ea4aaa?style=for-the-badge&logo=githubsponsors&logoColor=white)](https://github.com/sponsors/lachlanchen)

HybridImager es un espacio de investigación y diseño para un detector científico mixto. Combina un detector de píxel único de alto rango dinámico, temporización de cámara de eventos, textura de cámara de fotogramas y mediciones espectrales opcionales bajo un modelo de datos sincronizado.

| Donate | PayPal | Stripe |
| --- | --- | --- |
| [![Donate](https://img.shields.io/badge/Donate-LazyingArt-0EA5E9?style=for-the-badge&logo=kofi&logoColor=white)](https://chat.lazying.art/donate) | [![PayPal](https://img.shields.io/badge/PayPal-RongzhouChen-00457C?style=for-the-badge&logo=paypal&logoColor=white)](https://paypal.me/RongzhouChen) | [![Stripe](https://img.shields.io/badge/Stripe-Donate-635BFF?style=for-the-badge&logo=stripe&logoColor=white)](https://buy.stripe.com/aFadR8gIaflgfQV6T4fw400) |

## Concepto del sistema

![Hybrid board layout](../figures/hybrid_board_layout.png)

- **Rama de píxel único:** detector central y TIA de bajo ruido para intensidad absoluta, alto rango dinámico y mediciones codificadas o espectrales.
- **Rama de eventos:** contraste temporal asíncrono con cámaras comerciales al inicio y luego interfaces FPGA abiertas cuando sea práctico.
- **Rama de fotogramas:** módulos de obturador global para textura, calibración e inspección visual.
- **Capa de fusión:** flujos temporizados con exposición, ganancia, perfil de calibración, disparo y metadatos de patrón.

## Contenido actual

| Área | Ubicación |
| --- | --- |
| Artículo conceptual | `publications/hybrid_camera_concept.pdf` |
| Revisión de cámaras abiertas | `publications/open_camera_project_survey.pdf` |
| Notas de investigación | `references/` |
| Diagramas deterministas | `figures/hybrid_board_layout.*`, `figures/hybrid_signal_chain.*` |
| Plan de hardware | `hardware/board_architecture.md` |
| Plan de reconstrucción | `algorithms/reconstruction_plan.md` |
| Contexto previo | `copied-context/` |
| Espejos de proyectos abiertos | `external/` como submódulos git |

## Inicio rápido

```bash
git clone --recurse-submodules https://github.com/lachlanchen/HybridImager.git
cd HybridImager
make all
```

Si ya está clonado:

```bash
git submodule update --init --recursive
make survey
```

## Base de investigación

La ruta abierta más sólida para píxel único es **ONE-PIX** con **ONE-PIX_hardware**. Para visión de eventos, el primer prototipo realista usa cámaras comerciales con **OpenEB**, **jAER**, **v2e** y **E2VID**. Para hardware de fotogramas, las referencias abiertas útiles son **OneInchEye**, **Antmicro OV9281**, **AXIOM Beta** y **Seeed reCamera**.

El proyecto no presupone un ASIC personalizado de eventos en la primera etapa. Empieza con sincronización abierta a nivel de placa, formatos de datos abiertos, reconstrucción reproducible y referencias reutilizables de mecánica y PCB.

## Notas CAD y hardware

Paquete de exportación preferido desde Shapr3D para trabajo mecánico editable:

```text
STEP + native .shapr + Parasolid + DXF from sketch + 3MF/STL preview
```

Use STEP como formato principal, Parasolid como respaldo sólido de alta fidelidad, DXF para contornos 2D y placas, y STL/3MF solo para impresión o vista de malla.

## Comandos de compilación

```bash
make figures
make paper
make survey
make all
make clean
```

## Estado

Este es un espacio de investigación temprano, no un producto de imagen certificado. El objetivo inmediato es una tubería experimental mantenible para óptica y microscopía: construir con módulos disponibles, sincronizar limpiamente, reconstruir de forma reproducible e integrar hardware personalizado solo cuando el contrato de datos sea estable.

Construye menos. Imagen más.
