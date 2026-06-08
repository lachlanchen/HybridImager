# digiOBSCURA System Overview

## What this project is
- A DIY 32×32 image sensor made from 1,024 ALS-PT19 phototransistors on a dedicated sensor PCB.
- Two ADG732 (32:1) analog multiplexers select one column and one row; their common pins are `OUTCOL` (driven high) and `OUTROW` (analog read).
- A SAMD21G18A MCU board provides power, timing, SD logging, OLED UI, and shutter/buttons. Power: 18650 + MCP73831 charger + 3.3 V LDO.
- Firmware options: camera mode (`Firmware/digiOBSCURA_camera`) saves 32×32 BMPs to SD; webcam mode (`Firmware/digiOBSCURA_Webcam_Arduino` + Processing sketch) streams pixels over serial.

## Key electrical nets and connectors
- Sensor board headers (`PCB/image_sensor/digiobscura.sch`): `J1` (ROW) and `J2` (COL) carry `A0..A4`, `CS`, `WR`, `EN`, `OUTROW`, `OUTCOL`, 3V3, GND.
- Multiplexer control: `A0..A4` set address, `CS` chip select, `WR` write enable, `EN` output enable. Separate nets for ROW and COL muxes.
- Sensing path: GPIO drives `OUTCOL` high; selected phototransistor sinks current; voltage develops at `OUTROW`, read by MCU ADC.
- MCU board breakouts (`J2`/`J3` in `digiobscura_mcu.sch`) map MCU pins to the sensor nets; jumpers/potentiometer near `OUTROW` allow bias tweaking.

## Current firmware behavior (camera mode)
- Select pixel with `pixelSelect(col, row)` → set ADG732 address → strobe `WR`.
- Read `OUTROW` `avgCount` times (default 10) → store in `imgBuff`, track min/max → map to grayscale → write BMP to SD → show thumbnail on OLED.
- Timing: ~10k ADC reads per frame; frame rate is low; no per-session dark/flat calibration.

## Known limitations
- Noise and crosstalk from ADG732 on-resistance and long traces; `OUTCOL` is a stiff GPIO high (not a current source).
- No analog buffering on `OUTROW`; ADC sees mux + sensor impedance directly.
- Dynamic range and speed constrained by averaging and 3.3 V bias; no event/differential readout yet.
