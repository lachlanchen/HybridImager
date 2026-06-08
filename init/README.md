# Init Notes

This repository was initialized as a local Git workspace for the HybridCamera experiment.

```bash
mkdir -p HybridCamera/{init,references,publications,figures,hardware,firmware,algorithms,copied-context,scripts}
cd HybridCamera
git init
```

## Copied Local Context

The following related material was copied into `copied-context/` so the hybrid-camera design can be developed without mutating the original repositories:

- `CustomSensor/README.md`
- `CustomSensor/docs/01-firmware-differencing.md`
- `CustomSensor/docs/02-comparator-event-mode.md`
- `CustomSensor/docs/03-bias-and-buffer-upgrade.md`
- `CustomSensor/docs/04-full-event-sensor-redesign.md`
- `CustomSensor/PCB/image_sensor/` schematic and KiCad board files
- `CustomSensor/PCB/mcu/` schematic and KiCad board files
- `CustomSensor/Firmware/` Arduino and Processing sketches
- `NanoMi/README.md`, `NanoMi/AGENTS.md`, and `NanoMi/references/README.md`
- `HYBRID_EM_SENSOR_ROADMAP.AppAutoAction.md`

## Relationship to CustomSensor

`../CustomSensor` already contains a useful first-pass research track for event-like sensing. It proposes:

- Firmware-only temporal differencing.
- Comparator-assisted event detection with the SAMD21 analog comparator.
- TIA/buffer upgrades for the weak muxed phototransistor output.
- Longer-term tiled event-sensor redesign with per-tile comparators and FPGA/MCU capture.

HybridCamera keeps those ideas, but reframes them as one branch of a larger multimodal board. The new work adds a central single-pixel detector, spectral measurements, frame/event fusion, electron-microscopy detector motivation, and a reconstruction pipeline.
