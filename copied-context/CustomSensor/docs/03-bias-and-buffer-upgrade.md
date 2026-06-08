# Stage 3 — Bias and Buffer Improvements

Goal: improve SNR, consistency, and speed of reads by upgrading biasing and adding analog buffering on `OUTROW`.

## Issues today
- `OUTCOL` is a GPIO high; source impedance and voltage vary with load and temperature.
- ADG732 on-resistance plus sensor impedance means `OUTROW` sees a weak, variable source; ADC input loading and PCB capacitance smear fast changes.

## Upgrades
1) **Stable bias / current source on `OUTCOL`**
   - Replace GPIO drive with a small current source (e.g., op-amp + sense resistor or a JFET current diode set for tens of µA). Keep within ALS-PT19 limits.
   - Alternatively, buffer GPIO through an op-amp follower referenced to 3.3 V to stiffen the bias.
2) **Transimpedance or buffer on `OUTROW`**
   - Minimum: op-amp voltage follower (rail-to-rail, low bias current) between `OUTROW` and ADC/AC input.
   - Better: transimpedance amplifier (TIA) that converts sensor current to voltage and sets bandwidth via feedback resistor+cap; pick Rf to use most of ADC range without saturating in bright scenes.
   - Add RC at the op-amp input or TIA feedback cap to tame mux charge injection and set the noise bandwidth.
3) **Guard and layout tweaks (if respinning)**
   - Short, symmetric traces for `OUTROW` and `OUTCOL`; ground guard ring around `OUTROW`.
   - Local decoupling near the muxes (already partly present); add a small cap (10–47 pF) from mux output to ground if charge injection is visible as spikes.

## Testing and tuning
- Characterize dark voltage, full-scale voltage, and noise before/after buffer; set ADC reference and gain accordingly.
- Sweep bias current and TIA resistor to find sweet spot between saturation and noise.
- Verify comparator mode (Stage 2) still triggers reliably with the new analog front-end.
