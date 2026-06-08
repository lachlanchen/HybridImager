[English](README.md) · [العربية](i18n/README.ar.md) · [Español](i18n/README.es.md) · [Français](i18n/README.fr.md) · [日本語](i18n/README.ja.md) · [한국어](i18n/README.ko.md) · [Tiếng Việt](i18n/README.vi.md) · [中文 (简体)](i18n/README.zh-Hans.md) · [中文（繁體）](i18n/README.zh-Hant.md) · [Deutsch](i18n/README.de.md) · [Русский](i18n/README.ru.md)


[![LazyingArt banner](https://github.com/lachlanchen/lachlanchen/raw/main/figs/banner.png)](https://github.com/lachlanchen/lachlanchen/blob/main/figs/banner.png)

# OpenEM / NanoMi Repository

![Status](https://img.shields.io/badge/status-active%20research-blue) ![Platform](https://img.shields.io/badge/platform-Linux-informational) ![License](https://img.shields.io/badge/license-GPL--3.0-success) ![Python](https://img.shields.io/badge/python-3.9%E2%80%933.12-3776AB?logo=python&logoColor=white) ![Domains](https://img.shields.io/badge/scope-CAD%20%7C%20Electronics%20%7C%20Software-0A7EA4) ![Contributions](https://img.shields.io/badge/contributions-welcome-2ea44f)

This repository aggregates the open-source NanoMi transmission electron microscope project: mechanical CAD, electronics designs, reference documentation, and multiple software tools for control, imaging, and optics design. It is intended as a practical starting point for building, studying, or extending a complete open electron microscope.

For background, see the official NanoMi resources linked from `NanoMi/README.md`:
- NRC overview: <https://nrc.canada.ca/en/research-development/nanomi-worlds-first-open-source-transmission-electron-microscope>
- OSF project: <https://osf.io/bpj73/>
- Video overview: <https://www.youtube.com/watch?v=sMi-UkWSFS8&ab_channel=NationalResearchCouncilCanada>
- Hardware blueprint request form: <https://nrc.canada.ca/en/research-development/nanomi-hardware-blueprint-request-form>

> ⚠️ Safety note: this project involves **high voltage (up to 50 kV class)**, **high vacuum**, and potential **X-ray generation**. Use qualified engineers, interlocks, shielding, and follow local electrical/radiation regulations.

---

## 🧭 Quick Access

| I want to... | Go to | Why |
|---|---|---|
| Rebuild from factory perspective | `references/README.md` | Central index for staged build + commissioning docs |
| Launch control software | `NanoMi/Software/NANOmi.py` | Main TEM UI and hardware modules |
| Run optics tooling + tests | `NanoMi/nanomi-optics` | Packaged optics app with automated tests |
| Work on STEM scanner stack | `NanoMi/STEM_Image_Generation_Code` | FPGA, C bridge, and Python UI components |
| Inspect mechanical/electronics assets | `CAD files/`, `Electronics/` | Hardware source-of-truth revisions |

---

## 📚 Table of Contents

- [🎯 Repository Snapshot](#-repository-snapshot)
- [🔭 Overview](#-overview)
- [🧭 Rebuild Roadmap (Start Here)](#-rebuild-roadmap-start-here)
- [✨ Features](#-features)
- [🗂️ Project Structure](#️-project-structure)
- [🧰 Prerequisites](#-prerequisites)
- [🚀 Installation](#-installation)
- [▶️ Usage](#️-usage)
- [⚙️ Configuration](#️-configuration)
- [🧪 Examples](#-examples)
- [🛠️ Development Notes](#️-development-notes)
- [🩺 Troubleshooting](#-troubleshooting)
- [🗺️ Roadmap](#️-roadmap)
- [🤝 Contributing](#-contributing)
- [❤️ Support](#️-support)
- [📄 License](#-license)

---

## 🎯 Repository Snapshot

| Domain | Key location(s) | Purpose |
|---|---|---|
| Hardware | `CAD files/`, `Electronics/` | Mechanical revisions, board designs, and buildable electrical assets |
| Control software | `NanoMi/Software` | Main TEM control app and hardware interaction modules |
| Imaging stack | `NanoMi/STEM_Image_Generation_Code` | STEM FPGA, C bridge, and Python control pathways |
| Optics tools | `NanoMi/nanomi-optics`, `NanoMi/RayOptics` | Lens design, simulation, and optimization workflows |
| Factory workflow | `references/` | Rebuild and commissioning documentation with checklists |

---

## 🔭 Overview

NanoMi is an open hardware/software TEM platform with supporting SEM/STEM workflows. This monorepo combines:
- Full mechanical revision history (`CAD files/`)
- Electronics projects and production outputs (`Electronics/`)
- Control and analysis software (`NanoMi/`)
- Factory-oriented build references and checklists (`references/`)
- A reduced copy of the 2022 publication package (`2022 NanoMi paper/`)

The root README is the top-level index. Detailed subsystem instructions remain in each subproject README.

---

## 🧭 Rebuild Roadmap (Start Here)

| Area | Resource |
|---|---|
| Factory-oriented rebuild index | `references/README.md` |
| Deep step-by-step factory guide (Dongguan-ready) | `references/FACTORY_BUILD_GUIDE.md` |
| Compiled PDF (EN) | `references/FACTORY_BUILD_GUIDE.pdf` |

Checklists:
- `references/checklists/MECH_CHECKLIST.md`
- `references/checklists/ELECTRONICS_CHECKLIST.md`
- `references/checklists/COMMISSIONING_CHECKLIST.md`

Costing helpers:
- `references/costing/README.md`
- `references/costing/electronics_bom_costs.csv`
- `references/repo_manifest.csv`

---

## ✨ Features

- Multi-domain repository covering software, electronics, and mechanical design
- Main NanoMi control application with modular subsystem UI (`AddOnModules`)
- STEM scanner stack with FPGA HDL, C bridge layer, and Python UI
- Optics simulation/optimization tools (`nanomi-optics`, `RayOptics`, and scripts)
- Camera workflow integration (`eye4nanomi`)
- Manufacturing and commissioning references with checklists and costing data
- Standalone browser-based 3D visualizer (`3D_visualizer/index.html`)

---

## 🗂️ Project Structure

- `NanoMi/` - main software tree (TEM control software, STEM scanner code, optics tools, camera integration, and UI assets)
  - `NanoMi/Software/` - control software launcher `NANOmi.py` and UI modules
  - `NanoMi/STEM_Image_Generation_Code/` - FPGA + C + Python scanner stack
  - `NanoMi/nanomi-optics/` - packaged optics GUI/tooling with tests
  - `NanoMi/RayOptics/` - standalone column optics scripts
  - `NanoMi/PythonOpticsCalculations/` - standalone lens and aberration scripts
  - `NanoMi/eye4nanomi/` - camera and external viewer integration
- `CAD files/` - mechanical CAD for multiple NanoMi revisions (Inventor assemblies, STEP exports, design data)
- `Electronics/` - KiCad projects, Gerbers, FPGA projects, and board-level artifacts
- `2022 NanoMi paper/` - publication package and associated artifacts
- `references/` - rebuild roadmap, deep guides, checklists, costing, LaTeX sources
- `3D_visualizer/` - web-based 3D model viewer
- `AGENTS.md` - repository contribution/development conventions

---

## 🧰 Prerequisites

Requirements are subsystem-specific.

Environment matrix:

| Subsystem | Primary runtime | Notes |
|---|---|---|
| `NanoMi/Software` | Linux + Python (PyQt5 stack) | Designed around AccessIO AIOUSB workflow |
| `NanoMi/nanomi-optics` | Python `>=3.9,<3.11` | Poetry-supported package with tests |
| `NanoMi/STEM_Image_Generation_Code` | Python 3.12 + Vivado | Python UI + HDL toolchain split |
| `NanoMi/RayOptics` | Python CLI scripts | Script-driven optics calculations |

General:
- Linux is the primary supported platform for control software workflows
- Git
- Python (version depends on subsystem)

Main control software (`NanoMi/Software`):
- Linux (openSUSE Tumbleweed is repeatedly recommended upstream)
- Python with PyQt5 and module dependencies used by `AddOnModules`
- AccessIO AIOUSB userspace/library stack for supported digital IO boards

`nanomi-optics` package (`NanoMi/nanomi-optics`):
- Python `>=3.9,<3.11`
- `numpy`, `scipy`, `matplotlib`
- Optional: Poetry

STEM scanner UI (`NanoMi/STEM_Image_Generation_Code`):
- Python 3.12 (as documented in that subproject README)
- `pyqt6`, `pyqtgraph`, `numpy`
- Vivado (2022.2 used by authors; nearby versions may work)

---

## 🚀 Installation

Install path summary:

| Goal | Section |
|---|---|
| Full repo checkout | Clone repository |
| Hardware IO stack for TEM control | Install AIOUSB |
| Run NanoMi control GUI | Install and run NanoMi control software |
| Run optics GUI/tooling | Install and run nanomi-optics |
| Run STEM scanner software | Run STEM scanner UI (software side) |

### 1) Clone repository

```bash
git clone https://github.com/NRC-NANOmi/NanoMi.git
cd NanoMi
```

### 2) Install AIOUSB (for NanoMi control software hardware IO)

The following commands are taken from existing NanoMi documentation and remain the canonical baseline.

```bash
sudo zypper install fxload
sudo zypper install gcc-c++
sudo zypper install libusb-1_0-devel
sudo zypper install cmake
sudo zypper install swig
sudo zypper install git

git clone https://github.com/accesio/AIOUSB.git
cd AIOUSB/
git fetch
git checkout USB-AIO16-16F
git clean -df
cd AIOUSB/
mkdir build
cd build/
cmake ..
make
sudo make install
cd ..
sudo cp Firmware/*.hex /usr/share/usb/
sudo cp Firmware/10-acces*.rules /etc/udev/rules.d
```

Notes:
- Copying `.hex` files to `/usr/share/usb/` places firmware where `fxload` can find it.
- Copying udev rules to `/etc/udev/rules.d` enables automatic firmware loading for detected devices.
- Verify `10-acces_usb.rules` points to the correct `fxload` path (often `/usr/sbin/fxload`).

### 3) Install and run NanoMi control software

```bash
cd NanoMi/Software
python NANOmi.py
```

Assumption: `NanoMi/Software/README.md` and `NanoMi/README.md` mention `pip install -r requirements.txt`, but a committed `requirements.txt` was not found in `NanoMi/Software/` in this repository snapshot. Install PyQt5 and any import-missing dependencies manually for now.

### 4) Install and run nanomi-optics

```bash
cd NanoMi/nanomi-optics
poetry install
python main.py
```

Alternative without Poetry:

```bash
cd NanoMi/nanomi-optics
pip install numpy scipy matplotlib
python main.py
```

### 5) Run STEM scanner UI (software side)

```bash
cd NanoMi/STEM_Image_Generation_Code/python
python STEM_Scanner.py
```

---

## ▶️ Usage

### NanoMi control software

```bash
cd NanoMi/Software
python NANOmi.py
```

Runtime behavior and modules:
- On startup, hardware IO boards are scanned and channels are exposed in the Hardware module.
- Settings and assignments are stored under `NanoMi/Software/AddOnModules/SaveFiles/`.
- Deflector and stigmator advanced mappings are persisted as XML.
- Dataset save/load is managed through Data Sets XML.
- The application includes a ZMQ REP endpoint (`tcp://*:8888`) for dataset get/set interactions (per source-level behavior described in repository analysis).

### STEM scanner workflow

- Program/verify FPGA design under `NanoMi/STEM_Image_Generation_Code/HDL/`.
- Ensure host C bridge artifacts under `C_library/` are available.
- Launch Python UI:

```bash
cd NanoMi/STEM_Image_Generation_Code/python
python STEM_Scanner.py
```

### Optics tooling

`nanomi-optics` GUI:

```bash
cd NanoMi/nanomi-optics
python main.py
```

Tests:

```bash
cd NanoMi/nanomi-optics
pytest
```

Ray optics script (argument-driven CLI):

```bash
cd NanoMi/RayOptics
python NanoMi_Optics.py -h
```

Standalone optics scripts:
- `NanoMi/RayOptics/NanoMi_Optics.py`
- `NanoMi/PythonOpticsCalculations/*`

### Camera integration (`eye4nanomi`)

```bash
cd NanoMi/eye4nanomi
python eye4nanomi.py
```

Expected environment (from source and references): `gphoto2`, panta-rhei viewer with scripting/ZMQ enabled.

### 3D visualizer

Open in a browser:

```bash
xdg-open 3D_visualizer/index.html
```

---

## ⚙️ Configuration

Key persistent files:
- `NanoMi/Software/AddOnModules/SaveFiles/IoAssignments.txt`
- `NanoMi/Software/AddOnModules/SaveFiles/DeflectorSettings.xml`
- `NanoMi/Software/AddOnModules/SaveFiles/StigmatorSettings.xml`
- `NanoMi/Software/AddOnModules/SaveFiles/DataSets.xml`

Useful templates/examples:
- `2022 NanoMi paper/XML_shell/DeflectorSettings.xml`
- `2022 NanoMi paper/XML_shell/DataSets.xml`
- `2022 NanoMi paper/XML_shell/StartCanonM50.sh`

Guidance:
- Launch `NANOmi.py` from `NanoMi/Software` so dynamic module loading resolves `AddOnModules/` correctly.
- Keep wiring/channel mappings synchronized with XML settings and physical board assignments.
- Back up `SaveFiles/` before major hardware remaps.

---

## 🧪 Examples

### Example 1: Verify control software launch path

```bash
cd NanoMi/Software
python NANOmi.py
```

If modules do not load, confirm `AddOnModules/` is visible from current working directory.

### Example 2: Run optics test suite

```bash
cd NanoMi/nanomi-optics
pytest
```

Representative test files include:
- `tests/test_optimization.py`
- `tests/test_upper_lenses_math.py`
- `tests/test_lower_lenses_math.py`
- `tests/test_ur_conversion.py`

### Example 3: Open factory rebuild docs

```bash
xdg-open references/README.md
xdg-open references/FACTORY_BUILD_GUIDE.md
```

---

## 🛠️ Development Notes

- Follow `AGENTS.md` for coding style, scope control, and contribution practices.
- Keep diffs focused; avoid broad reformatting unrelated to your change.
- Tests currently exist in `NanoMi/nanomi-optics/tests` and should be updated when modifying that package.
- Root-level repository contents include large binary artifacts; prefer adding concise text documentation alongside any large design file updates.

---

## 🩺 Troubleshooting

- AIOUSB device not detected:
  - Verify udev rules were installed to `/etc/udev/rules.d`.
  - Confirm firmware `.hex` files are present in `/usr/share/usb/`.
  - Confirm `fxload` path inside udev rules is valid.
- `NANOmi.py` fails to load modules:
  - Run from `NanoMi/Software` (not from arbitrary working directory).
  - Check `NanoMi/Software/AddOnModules/` exists and contains expected `UI_*.py` modules.
- Missing Python packages:
  - Install dependencies manually per subproject README when `requirements.txt` is unavailable.
- STEM UI cannot communicate with hardware:
  - Confirm FPGA bitstream/programming state, USB bridge presence, and matching C library artifacts.
- `nanomi-optics` environment errors:
  - Use Python 3.9-3.10 and install dependencies from `pyproject.toml`.

---

## 🗺️ Roadmap

Current practical roadmap for contributors:
1. Consolidate per-subproject dependency manifests (especially `NanoMi/Software`).
2. Add reproducible environment definitions for control software and STEM stacks.
3. Expand automated tests beyond `nanomi-optics`.
4. Improve cross-linking between CAD/electronics revisions and recommended baseline builds.
5. Continue refining factory guides and commissioning checklists in `references/`.

---

## 🤝 Contributing

Contributions are welcome across software, documentation, CAD, and electronics.

Suggested flow:
1. Fork the repository.
2. Create a focused branch (`git checkout -b feature/<name>`).
3. Make targeted changes with clear commit messages.
4. Run relevant checks (for example, `pytest` in `NanoMi/nanomi-optics`).
5. Open a pull request describing scope, files changed, and validation performed.

Documentation note:
- Keep the root multilingual selector as a single top line and avoid duplicate language links.
- When updating README content, keep i18n variants aligned under `i18n/README.<lang>.md`.

For issue reporting and feature requests, use:
- <https://github.com/NRC-NANOmi/NanoMi/issues>

Contact points preserved from upstream docs:
- Software contact: Xuanhao Wang (`wang@xuanhao.site`)
- NanoMi team: `NRC.NanoMi.CNRC@nrc-cnrc.gc.ca`
- Hardware inquiries: Mark Salomons (`Mark.Salomons@nrc-cnrc.gc.ca`)

---

## ❤️ Support

| Donate | PayPal | Stripe |
| --- | --- | --- |
| [![Donate](https://camo.githubusercontent.com/24a4914f0b42c6f435f9e101621f1e52535b02c225764b2f6cc99416926004b7/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f446f6e6174652d4c617a79696e674172742d3045413545393f7374796c653d666f722d7468652d6261646765266c6f676f3d6b6f2d6669266c6f676f436f6c6f723d7768697465)](https://chat.lazying.art/donate) | [![PayPal](https://camo.githubusercontent.com/d0f57e8b016517a4b06961b24d0ca87d62fdba16e18bbdb6aba28e978dc0ea21/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f50617950616c2d526f6e677a686f754368656e2d3030343537433f7374796c653d666f722d7468652d6261646765266c6f676f3d70617970616c266c6f676f436f6c6f723d7768697465)](https://paypal.me/RongzhouChen) | [![Stripe](https://camo.githubusercontent.com/1152dfe04b6943afe3a8d2953676749603fb9f95e24088c92c97a01a897b4942/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f5374726970652d446f6e6174652d3633354246463f7374796c653d666f722d7468652d6261646765266c6f676f3d737472697065266c6f676f436f6c6f723d7768697465)](https://buy.stripe.com/aFadR8gIaflgfQV6T4fw400) |

## 📄 License

- Software in `NanoMi/` is licensed under GPL-3.0 (see `NanoMi/LICENSE` and `NanoMi/Software/LICENSE`).
- CAD, electronics, and paper-associated artifacts should be used according to terms and references in the associated publication and OSF resources.
