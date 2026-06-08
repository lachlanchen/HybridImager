# Stage 1 — Firmware-Only Frame Differencing

Goal: add temporal contrast (basic “event-like” behavior) without hardware changes. Use successive frames to flag pixels whose delta exceeds a threshold.

## Implementation sketch
- Store previous frame in RAM (another 32×32 int array).
- After `pixelSelect()`, take 1–2 ADC reads instead of `avgCount=10` to speed up; optionally make averaging configurable over serial/OLED menu.
- Compute `delta = current - prev`; if `abs(delta) > threshold`, mark event. Separate thresholds for positive/negative deltas if desired.
- Maintain running min/max only on “quiet” pixels to keep auto-gain sensible; clamp thresholds when gain saturates.
- Emit data:
  - Camera mode: keep writing BMPs but also write a compact CSV/CBOR of event coordinates/timestamps, or overlay events on the OLED preview.
  - Webcam mode: stream only event coords over serial: `row,col,polarity,tick`.
- Add a simple calibration pass on boot: take 2–3 dark frames to seed `prev` and estimate noise floor → set default `threshold = noise_mean + k*noise_std` (start with k≈3).

## Suggested code changes (files: `Firmware/digiOBSCURA_camera/digiOBSCURA_camera.ino`)
- Add `prevBuff[32][32]`, `eventMask[32][32]`.
- Replace the inner loop in `snapShot()`:
  - Reduce `avgCount`.
  - Compute `delta` vs `prevBuff`.
  - Update `prevBuff` with a leaky integrator: `prev = prev + alpha*(current - prev)` to avoid drift; try `alpha=0.2`.
- Add a new mode toggle (button long-press or compile-time flag) to switch between “full frame BMP” and “event CSV + optional BMP”.
- When `eventMask` is sparse, skip BMP write or downsample to save time.

## Tuning and tests
- Indoor dark scene: verify false event rate is low; adjust threshold and `avgCount`.
- Moving flashlight: ensure events fire along motion path; compare to full-frame greyscale for alignment.
- Log timing: measure frame time before/after to confirm speedup.
- SD wear: if logging events every frame, preallocate or rotate files to avoid fragmentation.
