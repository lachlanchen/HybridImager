# Reconstruction Algorithms

## Measurement Model

Represent the unknown scene, scan plane, or diffraction plane as `x`. HybridCamera records several coupled measurements:

```text
frame:        f_k = M_k x + noise
single-pixel: y_t = phi_t^T x + noise
events:       e_i = (u_i, v_i, t_i, p_i), triggered when Delta log I crosses +/- C
spectral:     s_l = H_l x + noise
```

The frame channel anchors texture and absolute geometry. The event channel supplies high-temporal-resolution changes. The bucket channel supplies high dynamic range scalar constraints. The spectral branch adds wavelength or energy contrast.

## Baseline Pipeline

1. Calibrate dark current, flat field, event thresholds, ADC gains, and geometric alignment.
2. Convert events into time surfaces or event frames for preview.
3. Reconstruct single-pixel images using Hadamard/compressed-sensing matrices.
4. Fuse events with frame anchors using an EDI-style physical model or E2VID-style learned reconstruction.
5. Add bucket measurements as global consistency constraints.
6. Add spectral bins as separate channels or low-rank abundance maps.

## Optimization Form

A practical offline objective is:

```text
min_x  ||M_f x - f||_2^2
     + alpha ||Phi x - y||_2^2
     + beta  E_event(x, e)
     + gamma TV(x)
     + eta   ||H x - s||_2^2
```

`E_event` can enforce that predicted log-intensity changes match event polarities and timestamps. `TV(x)` or wavelet sparsity stabilizes undersampled single-pixel reconstruction.

## Algorithms to Reuse

- **OpenEB / Metavision examples:** event decoding, time surfaces, visualization, filtering, and live camera integration.
- **E2VID:** learned event-to-video reconstruction, useful when a dense preview is needed from sparse event streams.
- **EDI:** high-frame-rate video reconstruction from a blurry/intensity frame plus events.
- **SPyRiT:** single-pixel reconstruction and deep reconstruction baselines.
- **4D STEM sparse processing:** event/electron-counting style storage and reconstruction ideas for microscope detector modes.

## Reconstruction Milestones

1. Simulate synthetic frames, events, and bucket samples from one video or scan image.
2. Recover `x` from bucket-only Hadamard measurements.
3. Recover a high-speed preview from frame plus events.
4. Add bucket constraints to reduce drift and recover saturated/dark regions.
5. Add spectral channels and evaluate on calibration targets.
6. Move to microscope scan data: reconstruct scalar detector images, event maps, and diffraction/spectrum-informed overlays.
