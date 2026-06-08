# Stage 2 — Comparator-Assisted Event Mode (Minimal Hardware Change)

Goal: use a comparator to flag intensity changes so firmware can react immediately, while still addressing pixels via the existing ADG732 muxes.

## Concept
- Bias the pixel (via `OUTCOL`) and compare `OUTROW` against a reference (set by the MCU DAC or a potentiometer). When the selected pixel crosses the threshold, an interrupt fires instead of (or in addition to) an ADC read.
- This reduces per-pixel ADC time and enables “stop scanning when event found” behavior.

## Practical path on current hardware
- MCU resources: SAMD21 has an analog comparator (AC) and a DAC output that can feed the reference.
- Wiring (logical): keep `OUTROW` on A4; route A4 to AC positive input; route DAC to AC negative input. In firmware, configure:
  - DAC to desired threshold (e.g., midscale + offset from calibration).
  - AC in window/edge mode; generate interrupt on rising and/or falling edges.
- Scan loop update:
  - Set mux address (`pixelSelect`), strobe `WR`, enable AC, wait short settle (a few µs), then check comparator flag. Only fall back to ADC if flag set or for periodic sanity checks.
  - If an edge is detected, log event `(row,col,polarity,timestamp)`; optionally halt scanning and rescan neighborhood for refinement.

## Calibration
- On boot, take a dark frame with ADC to estimate baseline; set DAC reference to `baseline + k*noise` (start k=3). Optionally allow user pot (if you add one in-line with DAC) to bias the reference manually.
- Periodically recompute baseline to track temperature drift.

## Limitations
- You still scan pixels sequentially with ADG732, so worst-case latency is one frame; best-case latency improves when events are rare (you can early-stop once events are detected).
- AC input bandwidth is fine for this speed, but mux on-resistance plus sensor impedance can cause edge slewing—keep a small settle delay after `WR`.

## Suggested firmware changes (new “Comparator mode”)
- Add a compile-time flag or menu item.
- Reuse the differencing buffers from Stage 1; if AC interrupt fires, mark `eventMask`; optionally also take one ADC sample for magnitude.
- Add a lightweight timing guard so AC results are ignored during mux switching (e.g., mask interrupts for 5–10 µs after `WR` toggle).
