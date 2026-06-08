# Stage 4 — Full Event-Sensor Redesign

Goal: move toward a DVS-style sensor that emits asynchronous events instead of full frames, with substantially new hardware.

## High-level options
1) **Per-pixel temporal contrast (closest to classic DVS)**
   - Each pixel gets AC coupling + a tiny storage cap and two comparators (ON/OFF). Output is row/col address + polarity when log-intensity crosses thresholds.
   - Requires custom pixel cell and dense routing; beyond the scope of the current PCB and ADG732 muxes.
2) **Row/column shared comparators (practical DIY)**
   - Keep phototransistor matrix, but add per-row and per-column sample/hold plus shared comparators that measure Δ vs a previous frame stored in analog caps.
   - An FPGA/CPLD/microcontroller with analog front-end coordinates sampling, differencing, and emits events.
3) **Segmented sensor with small mux + parallel comparators**
   - Break the array into tiles (e.g., 8×8 blocks). Each tile uses a small mux (8:1) feeding a fast comparator, so scan time per tile is short. Combine events digitally.

## Proposed DIY path (leveraging what exists)
- Respins:
  - Replace ADG732 with smaller 8:1/16:1 muxes per tile to cut address time and reduce charge injection per pixel.
  - Add per-tile op-amp buffer/TIA and a fast comparator with adjustable reference (DAC or resistor ladder).
  - Include a modest FPGA/CPLD (e.g., ICE40UP) or a faster MCU with more timers/DMAs to timestamp events and handle USB.
- Pixel front-end:
  - AC-couple each phototransistor (small series cap) into the comparator input so only changes (dI/dt) pass; provide bias via current source.
  - Set hysteresis/dual thresholds to create ON/OFF events and suppress chatter.
- Data format:
  - Emit `(timestamp, x, y, polarity)` over USB/UART/SD. Use 1–2 byte addresses (32×32 fits in 2 bytes), 1 byte polarity/flags, 4-byte timestamp (µs resolution if possible).

## Risks and mitigations
- Routing density: 1,024 pixels with added analog parts is tight—consider reducing resolution (e.g., 16×16) for the first spin.
- Power/noise: many comparators switching can inject noise; isolate analog and digital grounds, add plenty of decoupling.
- Development load: FPGA toolchain adds complexity; mitigate by using an off-the-shelf dev module for the first prototype and a mezzanine to the sensor PCB.

## Suggested milestones
1) Prototype a single 4×4 or 8×8 tile with AC coupling + comparator + FPGA/MCU capture; validate event generation.
2) Scale to a 16×16 board; measure event rate, false positives, and latency.
3) Integrate SD/USB event logging and a viewer to visualize event clouds in real time.
