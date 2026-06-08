# Reconstruction Plan

## Data Products

- `events.parquet` or binary event log: timestamp, x, y, polarity, source.
- `frames/`: raw frames with exposure metadata.
- `bucket.csv`: timestamped ADC samples, gain, bias, dark state.
- `spectral.csv`: wavelength/bin metadata and scalar samples.
- `calibration.json`: geometry, gain, thresholds, timing offsets, and dark/flat corrections.

## Simulation First

Before hardware is finished, generate synthetic data from a known image/video:

1. Downsample a frame sequence to the proposed tile geometry.
2. Generate DVS-like events from log-intensity threshold crossings.
3. Generate Hadamard or random single-pixel measurements.
4. Add realistic read noise, dark current, threshold mismatch, and timing jitter.
5. Evaluate reconstruction against the known source.

## Reconstruction Stack

- Use NumPy/SciPy for the first physics-based solver.
- Add PyTorch for learned E2VID/SPyRiT-style branches.
- Store experiments as scripts plus JSON configs so a hardware run can be replayed.

## Minimal Solver

Start with frame and bucket fusion:

```python
# x is a vectorized image estimate
loss = frame_weight * norm(M @ x - frame) ** 2
loss += bucket_weight * norm(Phi @ x - bucket) ** 2
loss += tv_weight * total_variation(x)
```

Then add event constraints once timestamps and thresholds are calibrated.
