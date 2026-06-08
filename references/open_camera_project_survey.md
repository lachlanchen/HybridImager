# Open Camera Project Survey

This note records current single-pixel, event-camera, and open image-sensor
projects that are useful for the HybridCamera direction.

## Short Conclusion

The best open single-pixel starting point is **ONE-PIX**: it has acquisition
software, Raspberry Pi control, hyperspectral reconstruction, a hardware
repository, and a premounted commercial kit option. For algorithms, **SPyRiT**
is the best companion because it focuses on single-pixel reconstruction.

For event vision, no mature fully open event-sensor silicon project was found.
The practical path is to buy a commercial event camera or sensor module and use
open software/gateware around it: **OpenEB/Metavision**, **jAER**, **v2e**,
**E2VID**, and **openEye-CamSI**. openEye-CamSI is notable because its roadmap
explicitly targets a Prophesee/Sony event-sensor interface.

For open frame-camera hardware, use projects that expose PCB, enclosure, and
interface design practice around commercial sensors: **AXIOM Beta**, **OneInchEye**,
**Antmicro OV9281 Dual Camera Board**, and **Seeed reCamera**.

## Cloned Repositories

| Path | Role | Notes |
| --- | --- | --- |
| `external/one-pix` | Single-pixel hyperspectral camera software | Open acquisition/control stack with GUI, CLI, plugins, and examples. |
| `external/one-pix-hardware` | Single-pixel kit hardware | Laser-cut case plans, STL fixtures, and editable CAD for the ONE-PIX kit. |
| `external/spyrit` | Single-pixel reconstruction | Deep reconstruction toolbox for simulated and experimental single-pixel data. |
| `external/single-pixel-camera-demo` | Minimal educational demo | Small DIY reference for coded illumination and reconstruction. |
| `external/openeb` | Event-camera SDK core | Open modules for event device HAL, streaming, visualization, ML, and plugins. |
| `external/event-based-get-started` | Event-camera examples | Python/C++ examples for Prophesee Metavision SDK workflows. |
| `external/jaer` | AER/event tooling | Long-lived Java tool stack for DVS/DAVIS-style sensors and AER processing. |
| `external/v2e` | Frame-to-event simulator | Converts normal videos into realistic synthetic DVS event streams. |
| `external/rpg-e2vid` | Event-to-frame reconstruction | Baseline for reconstructing intensity video from event streams. |
| `external/openeye-camsi` | Open camera interface/gateware | Open FPGA camera serial interface; roadmap includes event-camera hardware integration. |
| `external/one-inch-eye` | Open frame camera board | Raspberry Pi IMX283 one-inch CMOS sensor board with KiCad and STEP assets. |
| `external/ov9281-camera-board` | Open global-shutter stereo board | KiCad dual OV9281 MIPI CSI-2 board with open hardware files. |
| `external/axiom-beta-hardware` | Modular open cinema camera | Large open hardware camera stack with sensor boards, PCBs, enclosure, and manufacturing assets. |
| `external/oshw-recamera-series` | Modular AI camera hardware | Open hardware frame-camera system; not verified as an event-camera design in this clone. |

## Buying and Sourcing

**Single-pixel camera:** Start with ONE-PIX if the goal is a real working
research instrument. The hardware repo links to a premounted ONE-PIX kit from
Photonics Bretagne. UPOLabs also lists a single-pixel imaging experiment system
using a DMD spatial light modulator, single-pixel detector, and reconstruction
algorithms. For Taobao sourcing, I found component-style routes more credible
than a turnkey high-quality camera. Search terms to use:

- `单像素成像 实验系统`
- `DMD 空间光调制器`
- `DLP LightCrafter 4500`
- `DLP9500UV DMD`
- `光电探测器 TIA`
- `雪崩光电二极管 模块`
- `光电倍增管 模块`
- `数据采集卡 DAQ`

Minimum component set: DMD/DLP pattern source, photodiode/APD/PMT detector,
low-noise TIA or lock-in amplifier, synchronized ADC/DAQ, lenses, calibration
target, and a rigid optical rail or enclosure.

**Event camera:** Buy a commercial event camera or module first. The IMX636
Prophesee/Sony sensor has 1280 x 720 events, high dynamic range, and EVK options.
Use OpenEB for software, and consider openEye-CamSI if the goal is eventually
to build an open FPGA interface around an event sensor.

**Open image-sensor manufacturing:** I did not find a credible open CMOS image
sensor tapeout project ready for camera use. Open PDKs and open EDA exist, but
image sensors need analog pixels, pinned photodiodes, color/microlens process
steps, dark-current control, packaging, and calibration. For this project, treat
commercial sensors as the physical front end and make the board, synchronization,
data format, calibration, and reconstruction open.

## HybridCamera Design Implications

Use ONE-PIX as the center-bucket/spectral branch reference. Use an OpenEB-capable
event camera for first experiments, then study openEye-CamSI for a future FPGA
event interface. Use OneInchEye, OV9281, AXIOM, and reCamera as mechanical/PCB
examples for frame-camera modules. Keep the HybridCamera data model independent
from any vendor by storing timestamped streams with source ID, exposure/gain,
calibration profile, and hardware trigger metadata.

## Shapr3D Export Preference

Preferred export package for designs you want me to update:

1. `STEP` as the main editable interchange format.
2. Native `.shapr` as the design archive.
3. `Parasolid` (`.x_t` or `.x_b`) as the highest-fidelity solid backup.
4. `DXF from sketch` for flat plates, optical mounts, laser cutting, and PCB
   outline constraints.
5. `3MF` or `STL` for printing/mesh preview only.
6. `GLB` or `OBJ` for web preview, Blender rendering, or documentation only.

Avoid using STL, OBJ, image, PDF, or SVG as the only source for a part that needs
engineering edits. They lose solid CAD history or dimensional intent. IGES is a
fallback if STEP fails. DWG/JT/USDZ are useful only when a manufacturer or viewer
specifically requests them.

For HybridCamera, export **STEP + `.shapr` + Parasolid + DXF sketches + one 3MF
or STL preview** for every mechanical part. That gives enough information for
KiCad 3D placement, FreeCAD/CAD repair, Blender rendering, OpenSCAD reference
geometry, and fabrication checks.

## Source Links

- ONE-PIX: https://github.com/PhotonicsOpenProjects/ONE-PIX
- ONE-PIX hardware: https://github.com/PhotonicsOpenProjects/ONE-PIX_hardware
- SPyRiT: https://github.com/openspyrit/spyrit
- UPOLabs single-pixel imaging system: https://www.upolabs.com/ProductsStd_769.html
- TI DLPC900 DLP controller EVM: https://www.ti.com/product/DLPLCRC900EVM/part-details/DLPLCRC900EVM
- Prophesee OpenEB: https://github.com/prophesee-ai/openeb
- Prophesee/Sony IMX636: https://www.prophesee.ai/event-based-sensor-imx636-sony-prophesee/
- jAER: https://github.com/SensorsINI/jaer
- openEye-CamSI: https://github.com/chili-chips-ba/openeye-CamSI
- Antmicro OV9281 Dual Camera Board: https://github.com/antmicro/ov9281-camera-board
- OneInchEye: https://github.com/will127534/OneInchEye
- AXIOM Beta hardware: https://github.com/apertus-open-source-cinema/beta-hardware
- Seeed OSHW reCamera Series: https://github.com/Seeed-Studio/OSHW-reCamera-Series
