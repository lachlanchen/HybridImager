# Wiring and Control

## Timing Model

All modalities need one shared timebase. Use an FPGA or high-speed MCU timer as the timestamp authority, then synchronize:

- Event packets from event sensor or comparator tiles.
- Frame exposure start/end.
- ADC samples from the bucket detector.
- Spectral/filter position or wavelength index.
- Microscope scan coordinates, beam blanking, and dwell clock.

Target data records should include `timestamp_ns`, `source`, `x`, `y`, `polarity`, `value`, `gain`, `exposure`, and `calibration_id` where applicable.

## Physical Wiring

- **Bucket detector:** guarded coax or short PCB trace into the TIA; optional reverse-bias supply; differential ADC output to controller.
- **Event module:** MIPI, USB3, or parallel event bus if commercial; GPIO event IRQ and SPI/I2C configuration if DIY.
- **Frame module:** MIPI CSI-2 or parallel DVP into FPGA/SBC; global shutter trigger line preferred.
- **Spectral branch:** filter-wheel UART/I2C, grating motor driver, or spectrometer trigger/USB.
- **Microscope branch:** isolated trigger input, scan X/Y sample, beam blank, and detector gate lines.

## Firmware State Machine

1. Load calibration profile and detector gain table.
2. Arm the global clock and clear event/frame/ADC FIFOs.
3. Trigger frame exposure and bucket integration.
4. Stream events continuously.
5. On each scan dwell or pattern step, tag bucket samples with scan/pattern ID.
6. Flush records into a chunked file format such as HDF5/Zarr or a simple binary log plus JSON sidecar.

## Control Interfaces

The prototype can expose a Python control layer:

```python
camera.set_bucket_gain("10M")
camera.set_event_threshold(on=0.12, off=-0.12)
camera.trigger_frame(exposure_us=500)
camera.start_scan_sync(source="external_ttl")
camera.record("runs/sample_001")
```

For live work, publish reduced streams first: event count map, latest frame, bucket trace, and reconstructed preview. Store raw streams for offline reconstruction and calibration.
