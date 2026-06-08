[English](../README.md) · [العربية](README.ar.md) · [Español](README.es.md) · [Français](README.fr.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [Tiếng Việt](README.vi.md) · [中文 (简体)](README.zh-Hans.md) · [中文（繁體）](README.zh-Hant.md) · [Deutsch](README.de.md) · [Русский](README.ru.md)

[![LazyingArt banner](https://github.com/lachlanchen/lachlanchen/raw/main/figs/banner.png)](https://github.com/lachlanchen/lachlanchen/blob/main/figs/banner.png)

# HybridImager

*Imagerie scientifique hybride et ouverte : pixel unique, événements, images et spectre dans une pile de recherche maintenable.*

[![Website](https://img.shields.io/badge/Website-lazying.art-111827?style=for-the-badge&logo=googlechrome&logoColor=white)](https://lazying.art)
[![Concept Paper](https://img.shields.io/badge/PDF-Concept%20Paper-334155?style=for-the-badge&logo=latex&logoColor=white)](../publications/hybrid_camera_concept.pdf)
[![Survey](https://img.shields.io/badge/PDF-Open%20Camera%20Survey-0f766e?style=for-the-badge&logo=readthedocs&logoColor=white)](../publications/open_camera_project_survey.pdf)
[![GitHub Sponsors](https://img.shields.io/badge/Sponsor-lachlanchen-ea4aaa?style=for-the-badge&logo=githubsponsors&logoColor=white)](https://github.com/sponsors/lachlanchen)

HybridImager est un espace de recherche et de conception pour un détecteur scientifique mixte. Il associe un détecteur à pixel unique à grande dynamique, le timing d'une caméra événementielle, la texture d'une caméra à images et des mesures spectrales optionnelles dans un même modèle de données synchronisé.

| Donate | PayPal | Stripe |
| --- | --- | --- |
| [![Donate](https://img.shields.io/badge/Donate-LazyingArt-0EA5E9?style=for-the-badge&logo=kofi&logoColor=white)](https://chat.lazying.art/donate) | [![PayPal](https://img.shields.io/badge/PayPal-RongzhouChen-00457C?style=for-the-badge&logo=paypal&logoColor=white)](https://paypal.me/RongzhouChen) | [![Stripe](https://img.shields.io/badge/Stripe-Donate-635BFF?style=for-the-badge&logo=stripe&logoColor=white)](https://buy.stripe.com/aFadR8gIaflgfQV6T4fw400) |

## Concept du système

![Hybrid board layout](../figures/hybrid_board_layout.png)

- **Branche pixel unique :** détecteur central et TIA faible bruit pour l'intensité absolue, la grande dynamique et les mesures spectrales ou codées.
- **Branche événementielle :** contraste temporel asynchrone avec des caméras commerciales d'abord, puis des interfaces FPGA ouvertes lorsque cela devient pratique.
- **Branche image :** modules à obturateur global pour la texture, la calibration et l'inspection lisible.
- **Couche de fusion :** flux horodatés avec exposition, gain, profil de calibration, déclenchement et métadonnées de motif.

## Contenu actuel

| Zone | Emplacement |
| --- | --- |
| Article conceptuel | `publications/hybrid_camera_concept.pdf` |
| Revue des caméras ouvertes | `publications/open_camera_project_survey.pdf` |
| Notes de recherche | `references/` |
| Diagrammes déterministes | `figures/hybrid_board_layout.*`, `figures/hybrid_signal_chain.*` |
| Plan matériel | `hardware/board_architecture.md` |
| Plan de reconstruction | `algorithms/reconstruction_plan.md` |
| Contexte antérieur | `copied-context/` |
| Miroirs de projets ouverts | `external/` comme sous-modules git |

## Démarrage rapide

```bash
git clone --recurse-submodules https://github.com/lachlanchen/HybridImager.git
cd HybridImager
make all
```

Si le dépôt est déjà cloné :

```bash
git submodule update --init --recursive
make survey
```

## Base de recherche

La voie ouverte la plus solide pour le pixel unique est **ONE-PIX** avec **ONE-PIX_hardware**. Pour la vision événementielle, le premier montage réaliste utilise des caméras commerciales avec **OpenEB**, **jAER**, **v2e** et **E2VID**. Pour le matériel image, les références ouvertes utiles sont **OneInchEye**, **Antmicro OV9281**, **AXIOM Beta** et **Seeed reCamera**.

Le projet ne suppose pas un ASIC événementiel personnalisé dès la première étape. Il commence par une synchronisation ouverte au niveau carte, des formats de données ouverts, une reconstruction reproductible et des références mécaniques/PCB réutilisables.

## Notes CAD et matériel

Paquet d'export Shapr3D préféré pour le travail mécanique éditable :

```text
STEP + native .shapr + Parasolid + DXF from sketch + 3MF/STL preview
```

Utilisez STEP comme format principal, Parasolid comme sauvegarde solide haute fidélité, DXF pour les contours 2D et les plaques, et STL/3MF seulement pour l'impression ou la prévisualisation de maillage.

## Commandes de construction

```bash
make figures
make paper
make survey
make all
make clean
```

## Citation

Si vous utilisez HybridImager dans une recherche, citez le dépôt. GitHub lit [CITATION.cff](../CITATION.cff) et affiche le panneau **Cite this repository** sur la page du dépôt.

```bibtex
@software{chen_hybridimager_2026,
  author = {Chen, Lachlan},
  title = {HybridImager: Open Hybrid Scientific Imaging Research Workspace},
  year = {2026},
  url = {https://github.com/lachlanchen/HybridImager}
}
```

## Statut

C'est un espace de recherche précoce, pas un produit d'imagerie certifié. L'objectif immédiat est une chaîne expérimentale maintenable pour l'optique et la microscopie : construire avec des modules disponibles, synchroniser proprement, reconstruire de manière reproductible, puis intégrer du matériel personnalisé seulement lorsque le contrat de données est stable.

Construire moins. Imager plus.
