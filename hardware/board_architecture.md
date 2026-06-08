# Board Architecture

## Prototype 0: Benchtop Hybrid

Use off-the-shelf modules to validate timing and reconstruction:

- Prophesee/Sony event camera or another OpenEB-compatible event source.
- Global-shutter frame camera.
- Central photodiode plus low-noise TIA and ADC.
- FPGA/MCU timing board for triggers and timestamps.
- Optional filter wheel or spectrometer.

This stage proves the measurement model without designing a dense custom sensor.

## Prototype 1A: V1 Weiqi Sparse Sensor Board

The first generated PCB draft is in [`v1-weiqi-sensor/`](v1-weiqi-sensor/). It is a sensor carrier for sparse single-pixel experiments, not a final integrated imager:

- 21 populated detector sites on a 7x7 conceptual Weiqi grid.
- Per-site signal pads for external TIA/comparator probing.
- Back-copper ground spine tying detector guards, headers, SMA shields, and timing-chip exposed pad.
- Three SOIC-8 AFE placeholders and one QFN-48 MCU/FPGA timing placeholder.
- SMA sync in/out, 1x10 power/sync header, and 2x20 expansion header.

Generated outputs include a clean KiCad DRC report, STEP model, Gerbers, drill files, BOM, source dataset, and full-view 3D renders. This board should be reviewed mechanically and electrically before fabrication, but it is now a concrete V1 artifact for sparse detector geometry and bench wiring.

## Prototype 1B: V2 ALS-PT19 32x32 Matrix

The dense follow-up board is in [`v2-als-pt19-32x32/`](v2-als-pt19-32x32/). It uses the same sensor family documented in `CustomSensor`: `1024 x ALS-PT19` phototransistors with a row/column addressing model inspired by digiOBSCURA.

- 32 rows by 32 columns, all populated.
- Unrotated ALS-PT19 footprints on `2.54 mm` pitch so pads are aligned and do not overlap.
- Row header pins align directly with row buses on `F.Cu`.
- Column header pins align directly with column buses on `B.Cu` through per-pixel vias.
- ADG732 row/column mux footprints are placed as addressing placeholders.

This is the preferred first dense sensor-layout candidate. It still needs final schematic capture for the muxes, analog buffering, optical masking, crosstalk review, and firmware pin mapping before fabrication.

## Prototype 1: DIY Event Tile

Adapt the `CustomSensor` concept into one small tile:

- 4x4 or 8x8 detector matrix.
- Mux or row/column select.
- Per-tile TIA/buffer.
- Comparator with DAC thresholds for ON/OFF events.
- FPGA/MCU timestamp capture.

Success criteria: false-event rate, threshold repeatability, latency, and alignment with frame/bucket channels.

## Prototype 2: Integrated Weiqi Board

Build a square PCB with:

- Central bucket detector aperture.
- Alternating frame/event connectors or tiles.
- Spectral/filter input near the central detector.
- Differential ADC and comparator capture.
- Board-edge trigger/scan connectors for microscope integration.

Use the first board for optics/electronics validation, not final miniaturization.
