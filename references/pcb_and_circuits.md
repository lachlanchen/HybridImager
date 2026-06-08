# PCB and Circuit Design

## Board Partition

Design the first PCB as four electrical islands with explicit interfaces:

- **Bucket detector island:** central large-area photodiode, avalanche photodiode, PMT/SiPM adapter, or scintillator-coupled detector.
- **Event tile island:** commercial event module connector or DIY photodiode/comparator tiles.
- **Frame tile island:** global-shutter image sensor module or MIPI/parallel camera board.
- **Timing/control island:** FPGA or fast MCU, ADC, DAC references, USB/Ethernet, trigger I/O, and scan-sync inputs.

Keep the analog detector island physically quiet. Route digital clocks and MIPI/LVDS away from the TIA summing node and comparator thresholds.

## Central TIA Channel

The bucket detector should use a low-noise transimpedance amplifier. TI notes that TIAs convert low-level photodiode current into usable voltage and require compensation for stable operation ([SBOA055](https://www.ti.com/lit/pdf/sboa055)). TI AN-1803 highlights that photodiode capacitance plus amplifier input capacitance affects noise gain and stability, and that a feedback capacitor across the feedback resistor is used to maintain phase margin ([SNOA515](https://www.ti.com/lit/pdf/snoa515)).

Practical design rules:

- Place the detector and op-amp input within millimeters.
- Use selectable feedback networks, for example `100 k`, `1 M`, `10 M`, and `100 M` ohm with matching `Cf` options.
- Add a low-leakage analog switch only after testing the fixed-gain baseline.
- Guard the summing node with a driven guard at the same potential.
- Use a fully differential ADC driver after the TIA when long traces or high-resolution ADCs are used.
- Add a calibration LED/current source and dark shutter input for offset/dark-current measurement.

## Differential Event Circuit

A practical DIY event tile can start without per-pixel ASICs:

1. Sample each photodiode or phototransistor through a mux.
2. Store a previous value in a small capacitor or digital baseline table.
3. Subtract current minus baseline using an instrumentation/difference amplifier or ADC pair.
4. Compare against positive and negative DAC thresholds.
5. Latch `(tile,row,col,polarity,timestamp)` when either threshold crosses.

Use hysteresis and a refractory interval to suppress chatter. Put DAC references and comparator inputs on quiet analog rails. If the tile is muxed, include settle time after switching because mux resistance, detector capacitance, and PCB capacitance smear fast changes.

## Layout Rules

- Split analog and digital power filtering; join returns at a controlled low-impedance point.
- Keep high-impedance nodes short, guarded, and free of solder flux residue.
- Add shield-can footprints around the bucket detector and TIA.
- Route MIPI/LVDS/USB as controlled impedance differential pairs.
- Provide test points for detector bias, TIA output, ADC input, comparator thresholds, event IRQ, frame trigger, and scan-sync.
- Add board-edge SMA/MCX or coax headers for microscope scan clock, beam blanking, detector output, and trigger.

## KiCad Implementation Notes

Start from the copied `CustomSensor` KiCad files only as a topology reference. The new board should be drawn as separate hierarchical sheets:

- `detector_bucket.kicad_sch`
- `event_tile.kicad_sch`
- `frame_sensor_connector.kicad_sch`
- `timing_fpga.kicad_sch`
- `power_and_bias.kicad_sch`

Export manufacturing outputs early: schematic PDF, interactive BOM, Gerbers, drill files, STEP, and a 3D board render. Run ERC/DRC before every fabrication package.
