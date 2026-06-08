# Board Architecture

## Prototype 0: Benchtop Hybrid

Use off-the-shelf modules to validate timing and reconstruction:

- Prophesee/Sony event camera or another OpenEB-compatible event source.
- Global-shutter frame camera.
- Central photodiode plus low-noise TIA and ADC.
- FPGA/MCU timing board for triggers and timestamps.
- Optional filter wheel or spectrometer.

This stage proves the measurement model without designing a dense custom sensor.

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
