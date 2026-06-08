[English](README.md) · [العربية](i18n/README.ar.md) · [Español](i18n/README.es.md) · [Français](i18n/README.fr.md) · [日本語](i18n/README.ja.md) · [한국어](i18n/README.ko.md) · [Tiếng Việt](i18n/README.vi.md) · [中文 (简体)](i18n/README.zh-Hans.md) · [中文（繁體）](i18n/README.zh-Hant.md) · [Deutsch](i18n/README.de.md) · [Русский](i18n/README.ru.md)


[![LazyingArt banner](https://github.com/lachlanchen/lachlanchen/raw/main/figs/banner.png)](https://github.com/lachlanchen/lachlanchen/blob/main/figs/banner.png)

# digiOBSCURA - A DIY Image Sensor and Digital Camera 📷

[![License: CC BY-NC-SA 3.0 (firmware header)](https://img.shields.io/badge/Firmware%20Header-CC%20BY--NC--SA%203.0-lightgrey?style=for-the-badge)](https://creativecommons.org/licenses/by-nc-sa/3.0/)
[![Repo License](https://img.shields.io/badge/Repository%20License-GPL--3.0-2563eb?style=for-the-badge)](./LICENSE)
[![Project Type](https://img.shields.io/badge/Type-DIY%20Hardware%20%2B%20Firmware-f97316?style=for-the-badge)](#overview)
[![Sensor](https://img.shields.io/badge/Sensor-32x32%20(1024px)-16a34a?style=for-the-badge)](#features)
[![MCU](https://img.shields.io/badge/MCU-SAMD21G18A-1d4ed8?style=for-the-badge)](#hardware-firmware-architecture-current)
[![Contributions](https://img.shields.io/badge/Contributions-Welcome-0f766e?style=for-the-badge&logo=github)](#contributing)
[![GitHub Stars](https://img.shields.io/github/stars/lachlanchen/CustomSensor?style=for-the-badge)](https://github.com/lachlanchen/CustomSensor/stargazers)
[![GitHub Issues](https://img.shields.io/github/issues/lachlanchen/CustomSensor?style=for-the-badge)](https://github.com/lachlanchen/CustomSensor/issues)

> A fully open DIY imaging stack: custom sensor PCB, MCU board, firmware, webcam viewer, and printable enclosure parts.

## 📚 Table of Contents

- [Overview](#overview)
- [Demo](#demo)
- [Features](#features)
- [Project Structure](#project-structure)
- [Hardware/Firmware Architecture (Current)](#hardwarefirmware-architecture-current)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration Notes](#configuration-notes)
- [Examples](#examples)
- [Development Notes](#development-notes)
- [Troubleshooting](#troubleshooting)
- [Roadmap and Technical Notes](#roadmap-and-technical-notes)
- [Contributing](#contributing)
- [Support](#%E2%9D%A4%EF%B8%8F-support)
- [License](#license)

## Overview 🛰️

`digiOBSCURA` is a DIY 32x32 imaging system built around a custom phototransistor array and a SAMD21-based controller.

This repository contains:
- Firmware for standalone camera capture to SD card.
- Firmware + Processing sketch for serial webcam-style live viewing.
- Full KiCad source files for both boards (`image_sensor` and `mcu`) plus production gerbers.
- Mechanical assets (`.f3d`, `.stl`) for enclosure/lens/tripod components.
- Design notes and staged upgrade roadmap documents in [`docs/`](./docs/).

## Quick Snapshot 📌

| Item | Details |
| --- | --- |
| Project size | Camera + firmware + viewer + mechanical design |
| Sensor array | `32x32` (`1024`) custom phototransistor matrix |
| Core controller | `SAMD21G18A` |
| Image output | SD card BMP / serial live frame stream |
| Target workflows | Standalone capture • Webcam-style preview |

## Demo 🎬

Check out the video:

[![digiOBSCURA Video](https://img.youtube.com/vi/PaXweP73NT4/0.jpg)](https://youtu.be/PaXweP73NT4)

Find the BOM for both boards here: https://www.findchips.com/org/10-open-hardware/list/162969-digiobscura-diy-image-sensor-and-digital-camera

## Features ✨

- 32x32 (1024-pixel) custom phototransistor imaging array.
- Dual ADG732 mux addressing for row/column pixel selection.
- Standalone camera workflow:
  - OLED status UI.
  - Shutter input.
  - SD card output (`DGO_####.bmp`, auto-incremented).
- Webcam workflow:
  - Arduino firmware responds to serial pixel requests at `115200`.
  - Processing app renders a live grayscale 32x32 view.
- Open hardware source:
  - KiCad schematics/PCBs.
  - Production outputs and BOM artifacts.
  - Printable mechanical files.

## Project Structure 🧱

```text
CustomSensor/
|- README.md
|- LICENSE
|- Firmware/
|  |- digiOBSCURA_camera/
|  |  |- digiOBSCURA_camera.ino
|  |- digiOBSCURA_Webcam_Arduino/
|  |  |- digiOBSCURA_Webcam_Arduino.ino
|  `- digiOBSCURA_Webcam_Processing/
|     `- digiOBSCURA_Webcam_Processing.pde
|- docs/
|  |- overview.md
|  |- 01-firmware-differencing.md
|  |- 02-comparator-event-mode.md
|  |- 03-bias-and-buffer-upgrade.md
|  `- 04-full-event-sensor-redesign.md
|- PCB/
|  |- image_sensor/
|  |  |- digiobscura.kicad_pcb
|  |  |- digiobscura.sch
|  |  |- sym-lib-table
|  |  `- fp-lib-table
|  `- mcu/
|     |- digiobscura_mcu.kicad_pcb
|     |- digiobscura_mcu.sch
|     |- sym-lib-table
|     `- fp-lib-table
|- PCB-Production/
|- F3D/
|- STL/
|- logo/
|- i18n/
|- .auto-readme-work/
|  |- pipeline-context.md
|  `- repo-structure-analysis.md
`- .git
```

## Hardware/Firmware Architecture (Current) 🧰

Based on [`docs/overview.md`](./docs/overview.md):

| Subsystem | Details |
|---|---|
| Sensor matrix | `1024 x ALS-PT19` phototransistors |
| Addressing | `2 x ADG732` analog muxes (row + column) |
| Core board | `SAMD21G18A` |
| Power path | `18650` battery, `MCP73831` charger, `3.3 V` regulation |
| Signal path | `OUTCOL` is driven high by MCU GPIO; selected sensor path is read on `OUTROW` via ADC |
| Capture behavior | Camera firmware performs full-frame scans and writes 24-bit BMP files |

## Prerequisites 🧰

### Hardware

- Assembled `image_sensor` and `mcu` boards (or equivalent wiring).
- SAMD21-compatible target board matching pin assignments used in firmware.
- MicroSD card (camera mode).
- `64x48` SSD1306 OLED (camera mode, 4-wire software SPI in current sketch).
- Shutter button/switch input.

### Software

- Arduino IDE (or Arduino CLI) with a SAMD21 board package.
- Required Arduino libraries for camera firmware:
  - `U8g2`
  - `SPI`
  - `SD`
- Processing IDE/runtime for [`Firmware/digiOBSCURA_Webcam_Processing`](./Firmware/digiOBSCURA_Webcam_Processing/).

## Installation 🧩

1. Clone this repository:

```bash

git clone https://github.com/lachlanchen/CustomSensor.git
cd CustomSensor
```

2. Open one firmware sketch in Arduino IDE:
- Camera mode: [`Firmware/digiOBSCURA_camera/digiOBSCURA_camera.ino`](./Firmware/digiOBSCURA_camera/digiOBSCURA_camera.ino)
- Webcam mode: [`Firmware/digiOBSCURA_Webcam_Arduino/digiOBSCURA_Webcam_Arduino.ino`](./Firmware/digiOBSCURA_Webcam_Arduino/digiOBSCURA_Webcam_Arduino.ino)

3. Select the correct SAMD21 board and port, then upload.

4. For webcam mode, open the Processing sketch:
- [`Firmware/digiOBSCURA_Webcam_Processing/digiOBSCURA_Webcam_Processing.pde`](./Firmware/digiOBSCURA_Webcam_Processing/digiOBSCURA_Webcam_Processing.pde)

## Usage 🚀

### Camera Mode (SD snapshot workflow) 📸

1. Flash `digiOBSCURA_camera.ino`.
2. Insert an SD card formatted FAT/FAT32.
3. Power/reset the board; firmware scans for the next free `DGO_####.bmp` filename.
4. Trigger capture with the shutter input.
5. The device captures and writes BMP to SD and shows a thumbnail preview on OLED.

### Webcam Mode (host-rendered live view) 🖥️

1. Flash `digiOBSCURA_Webcam_Arduino.ino`.
2. Connect over USB serial at `115200`.
3. In the Processing sketch, set `String portName` to your actual serial port (the template uses `COM32`).
4. Run Processing sketch; it polls 32x32 pixels and renders a grayscale live frame.

## Configuration Notes 🛠️

Current firmware-level defaults from source:

| Setting | Current value / behavior |
|---|---|
| Resolution | Fixed `32x32` |
| ADC resolution | `analogReadResolution(12)` |
| Camera-mode averaging | `avgCount = 10` (higher quality, lower frame speed) |
| SD CS pin (camera sketch) | `cardPin = 21` |
| Serial baud (webcam path) | `115200` |
| I/O mapping | Hardcoded arrays/variables (`SCOL`, `SROW`, `WR`, `CS`, `EN`, `OUTCOL`, `OUTROW`, etc.) |

If your wiring differs, update pin definitions near the top of each `.ino` file before flashing.

## Examples 🧪

### Open and edit camera firmware

```bash
cd Firmware/digiOBSCURA_camera
# open digiOBSCURA_camera.ino in Arduino IDE
```

### Open and edit the Processing webcam viewer

```bash
cd Firmware/digiOBSCURA_Webcam_Processing
# open digiOBSCURA_Webcam_Processing.pde in Processing IDE
```

### Open PCB sources in KiCad

- `PCB/image_sensor/digiobscura.sch`
- `PCB/image_sensor/digiobscura.kicad_pcb`
- `PCB/mcu/digiobscura_mcu.sch`
- `PCB/mcu/digiobscura_mcu.kicad_pcb`

## Development Notes 📘

- There is no unified build system (`Makefile`, `platformio.ini`, `package.json`, etc.) in this repository.
- Development currently spans Arduino + Processing + KiCad + mechanical CAD files.
- `PCB/image_sensor/README.md` and `PCB/mcu/README.md` currently contain placeholder/template-like content and are not authoritative.
- `i18n/` contains translated README variants; they appear incomplete in places and may lag the English content.

## Troubleshooting 🧯

| Symptom | Checks |
|---|---|
| SD card not detected in camera mode | Confirm wiring and `cardPin` (`21` in current sketch). Reformat SD card (FAT/FAT32) and retry. |
| Blank/noisy image data | Verify `OUTCOL`/`OUTROW` wiring and mux control pins. Check power integrity and sensor board connections. |
| Processing viewer shows no data | Confirm serial baud `115200` in both Arduino and Processing. Update `portName` from `COM32` to your actual port. |
| Very slow capture | Expected with full 32x32 scan and averaging (`avgCount=10` by default). |

## Roadmap and Technical Notes 🗺️

The `docs/` directory tracks planned and exploratory technical directions:

| Document | Focus |
|---|---|
| [`docs/01-firmware-differencing.md`](./docs/01-firmware-differencing.md) | Firmware-only temporal differencing / events |
| [`docs/02-comparator-event-mode.md`](./docs/02-comparator-event-mode.md) | Comparator-assisted event detection |
| [`docs/03-bias-and-buffer-upgrade.md`](./docs/03-bias-and-buffer-upgrade.md) | Analog front-end and bias improvements |
| [`docs/04-full-event-sensor-redesign.md`](./docs/04-full-event-sensor-redesign.md) | Longer-term event-sensor redesign options |

## Contributing 🤝

Contributions are welcome. Suggested contribution areas:

- Hardware bring-up notes and verified pin maps.
- Toolchain/version validation (Arduino core, libraries, Processing version).
- Documentation updates, especially wiring diagrams and calibration workflow.

- `i18n/` README translations once language targets are finalized.

For changes touching hardware or firmware behavior, include:
- Test setup details.
- Board revision context.
- Before/after behavior notes.

## ❤️ Support

| Donate | PayPal | Stripe |
| --- | --- | --- |
| [![Donate](https://camo.githubusercontent.com/24a4914f0b42c6f435f9e101621f1e52535b02c225764b2f6cc99416926004b7/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f446f6e6174652d4c617a79696e674172742d3045413545393f7374796c653d666f722d7468652d6261646765266c6f676f3d6b6f2d6669266c6f676f436f6c6f723d7768697465)](https://chat.lazying.art/donate) | [![PayPal](https://camo.githubusercontent.com/d0f57e8b016517a4b06961b24d0ca87d62fdba16e18bbdb6aba28e978dc0ea21/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f50617950616c2d526f6e677a686f754368656e2d3030343537433f7374796c653d666f722d7468652d6261646765266c6f676f3d70617970616c266c6f676f436f6c6f723d7768697465)](https://paypal.me/RongzhouChen) | [![Stripe](https://camo.githubusercontent.com/1152dfe04b6943afe3a8d2953676749603fb9f95e24088c92c97a01a897b4942/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f5374726970652d446f6e6174652d3633354246463f7374796c653d666f722d7468652d6261646765266c6f676f3d737472697065266c6f676f436f6c6f723d7768697465)](https://buy.stripe.com/aFadR8gIaflgfQV6T4fw400) |

## License

- `LICENSE` in this repository currently indicates the project is distributed as GPL-3.0 at the repository level.
- Firmware header comments also reference `CC BY-NC-SA 3.0` for some source-header content.

When redistributing binaries, hardware artifacts, or derivatives, verify the exact license conditions in the files you touch and ensure compatibility with your intended use.
