# OpenEM / NanoMi Reference & Rebuild Roadmap

This document complements the 2022 NanoMi paper (`2022 NanoMi paper/2022_NanoMi_MicronSI_reduced.pdf`) and the design data in this repository. It is meant as a “master index” and a practical roadmap for rebuilding the OpenEM / NanoMi system from the files in this repo.

It does not replace safety engineering, local regulations, or the paper itself; treat it as a map that connects the publication to concrete files and build steps.

## Factory-Oriented Guides (Start Here for Manufacturing)
- **Deep factory build tutorial**: `references/FACTORY_BUILD_GUIDE.md` (PDF: `references/FACTORY_BUILD_GUIDE.pdf`)
- **Deep factory build tutorial (中文)**: `references/FACTORY_BUILD_GUIDE.zh.md` (PDF: `references/FACTORY_BUILD_GUIDE_zh.pdf`)
- **Checklists (mechanical/electronics/commissioning)**:
  - `references/checklists/MECH_CHECKLIST.md`
  - `references/checklists/ELECTRONICS_CHECKLIST.md`
  - `references/checklists/COMMISSIONING_CHECKLIST.md`
- **Costing + file inventory helpers**:
  - `references/costing/README.md`
  - `references/costing/electronics_bom_costs.csv`
  - `references/repo_manifest.csv` (full repo file manifest for PLM/ERP import)

## Key References from the Paper
- **Main publication**
  - `2022 NanoMi paper/2022_NanoMi_MicronSI_reduced.pdf` – core description of the instrument, design goals, and performance.
- **CAD associated with figures**
  - `2022 NanoMi paper/CAD_drawings/`
    - `NanoMiStandardMountingPlate.stp` – standard mounting plate geometry.
    - `NanoMi5IDMountingPipe.stp` – ID mounting pipe.
    - `v-groove.stp` – v‑groove component.
- **Electronics schematics for Fig. 13 & 14**
  - `2022 NanoMi paper/Fig_13and14_KiCAD_files/`
    - `DeflectorStigmatorPowerV1.0/` – KiCad project (`*.pro`, `*.sch`, `CustomParts.lib`) for the deflector/stigmator power supply.
    - `DeflectorStigmatorV2.1/` – high‑voltage deflector/stigmator board (`HVA.sch`, `HVAV2.1.sch`, custom libraries).
  - These projects match the conceptual schematics shown in the paper.
- **Configuration XML shell**
  - `2022 NanoMi paper/XML_shell/`
    - `DeflectorSettings.xml` – example advanced settings mapping deflector plates to physical DAC channels.
    - `DataSets.xml` – example of saved datasets (full instrument state).
    - `StartCanonM50.sh` – helper script for camera integration.
  - These are minimal “known good” examples for configuring the control software.

---

## Design Targets & Constraints (from the Paper)

- **Operating modes & energy**
  - Intended modes: SEM, TEM, STEM, ED (diffraction).
  - Target incident energy: up to **50 keV**, column performance discussed from **1–50 keV**.
  - Target probe and image resolution: **≈10 nm** in SEM, STEM, and TEM for the initial column.

- **Vacuum & environment**
  - Ultra-high vacuum in the column: **mid‑10⁻⁸ torr** range (turbomolecular pump for column; ion pump recommended for FEG/Schottky guns).
  - Column uses standard CF hardware (8" / DN160 CF) with **152 mm** (6″) tube and internal **127 mm** (5″) half‑pipe breadboard.

- **Electron optics**
  - Electrostatic einzel lenses chosen for the initial column (simpler manufacturing vs magnetic lenses).
  - Representative einzel lens aberration coefficients:
    - Spherical aberration **CS ≈ 50 mm**.
    - Chromatic aberration **CC ≈ 28 mm** at lens potential **UL ≈ 0.8·U₀**.
  - With these values and appropriately chosen convergence angle **2·α** and defocus **Δz**, theoretical **d₅₀ ≤ 4 nm** is achievable over **1–50 keV**; the **10 nm** target is therefore realistic.

- **High-voltage stability**
  - Acceleration supply **U₀** and lens supplies **UL** must be stable at roughly **10 ppm** over the acquisition time for ≈10 nm probes.
  - Both ripple and long‑term drift of the HV supply must stay within this budget during typical STEM/SEM frame times (**tens of seconds**).

- **Electron source options**
  - W‑hairpin filament:
    - Energy spread **ΔE ≈ 2 eV**, brightness **Be ≈ 3×10⁹ A·m⁻²·sr⁻¹** (scaled to NanoMi energies).
    - For a 10 nm probe at 2·α ≈ 10 mrad, ~9 pA beam current is feasible, giving **≈1700 e⁻/pixel** at 30 μs dwell in a 1024² image (~30 s frame).
  - LaB₆:
    - Brighter source (**Be ≈ 3×10¹⁰ A·m⁻²·sr⁻¹**) with **ΔE ≈ 1 eV** or better (≈0.7 eV with careful operation).
    - Allows shorter dwell times and/or higher SNR at similar probe size.
  - Cold field emission / Schottky:
    - Offer still narrower **ΔE**, but require stricter vacuum (ion pump, gun region isolation) and are more sensitive to environmental noise.
  - For a first‑generation rebuild, the paper favours a gun that can accept both W‑hairpin and LaB₆ emitters, operating in mid‑10⁻⁸ torr.

- **Mechanical concept**
  - All electron‑optical elements are mounted on the internal **127 mm half‑pipe** that hangs inside the 152 mm column tube.
  - The vacuum envelope and electron optics are largely independent: the column uses off‑the‑shelf CF parts, while optics mount to the half‑pipe.
  - Full column height ~**1300 mm** for SEM/TEM/STEM/ED; probe‑forming section alone ~**500 mm**.

---

## Mechanical CAD – What to Use and Where

### Global CAD tree
- Root: `CAD files/`
- Revisions (full mechanical designs):
  - `NanoMi rev 2/`
  - `NanoMi rev 3/`
  - `NanoMi rev 4/`
  - `NanoMi rev 5 horizontal column/`
  - `NanoMi rev 6 vertical column/`
- Each revision typically contains:
  - **Assemblies**: `*.iam` – e.g. `complete assembly.iam`, `chamber assembly.iam`, `NanoMi internals.iam`.
  - **Parts**: `*.ipt` – lenses, apertures, vacuum components, brackets, etc.
  - **Exchange formats**: `*.stp` – for neutral CAD/CAM use.
  - **Drawings**: `*.pdf` – e.g. `Rectangular Chamber Assembly v2 (Master).pdf`, `NanoMi internals (Master).pdf`.
  - **Design data**: `Design Data/` and material libraries (`InventorMaterialLibrary.adsklib.zip`).

### Suggested mechanical build target
- For a modern mechanical baseline aligned with the paper:
  - Prefer `NanoMi rev 5 horizontal column/` or `NanoMi rev 6 vertical column/` depending on orientation required by your lab.
  - Within `NanoMi rev 6 vertical column/`, key subassemblies include:
    - `Chamber Assembly/`
    - `NanoMi internals/` – internal column optics: standard mounting plate, thick mounting plate, alignment tool and related parts (`*.ipt`/`*.stp` with paired `*.pdf` drawings).
    - `SED/` – secondary electron detector mounting parts (Teflon part, light pipe, grid, etc.).
    - `Air table/` – vibration isolation support (`tablenanomi.iam`, `tablenanomi.stp`).

### How to use the CAD data
- **Step 1 – Choose a revision set**:
  - Read the paper and compare with the `complete assembly` and `chamber assembly` files under `CAD files/NanoMi rev X/...` to pick a matching revision.
- **Step 2 – Generate or review drawings**:
  - Use the `*.pdf` “(Master)” drawings as primary manufacturing references.
  - If needed, open the Inventor assemblies (`*.iam`) and derive additional drawing views or export updated `*.stp`.
- **Step 3 – Split by fabrication domain**:
  - Vacuum components: flanges, chambers, column tubes, adapters.
  - Precision mechanics: lens mounts, alignment tools, stages.
  - Structural parts: tables, frames, brackets, camera mounts.
- **Step 4 – Manufacturing and QA**:
  - Ensure tolerance, surface finish, and material choice follow the paper and your lab’s vacuum requirements (e.g. stainless steel for vacuum, aluminium for structural).
  - Track any deviations from the CAD (different pumps, viewports, etc.) in your own documentation.
  - For any change that affects alignment (e.g. different flanges or ports), reflect it in your own version of the ray‑trace/optics models (see `NanoMi/RayOptics/NanoMi_Optics.py` and `NanoMi/PythonOpticsCalculations`).

---

## Electronics – Boards, Power, and FPGA Paths

All “current” electronics are in `Electronics/`. These map broadly to:
- Column deflection & stigmation.
- High‑voltage scanning deflectors.
- Piezo motion & drivers.
- STEM image generation and power.

### Column deflectors & stigmators (non‑scanning)
- Path: `Electronics/Column Deflectors (Non-Scanning)/`
- Key projects:
  - `Deflector & Stigmator Boards V2.1/Board Files/`
    - Main KiCad project: `DeflectorStigmatorsV2.1.pro`
    - Schematic: `DeflectorStigmatorsV2.1.sch`, `Schematic.sch`
    - Board: `DeflectorStigmatorsV2.1.kicad_pcb`
    - Libraries: `Deflector_StigmatorsV2.1.lib`, `.dcm`, custom footprints in `*.kicad_mod`.
  - `Deflector & Stigmator Boards V2.3/Board Files/`
    - Main KiCad project: `HVA2.3.kicad_sch`, `HVA2.3.kicad_pcb`
    - Simulation subfolder: `SImulation/MC1458.lib` for op‑amp behaviour.
  - `Power Supply for Deflectors & Stigmators V1.0/Board Files/`
    - Project: `DeflectorStigmatorPowerV1.0.pro`
    - Schematic: `DeflectorStigmatorPowerV1.0.sch`, `Schematic.sch`
    - Board: `DeflectorStigmatorPowerV1.0.kicad_pcb`.

These boards feed the deflector and stigmator plates driven by the control software (see `NanoMi/Software/AddOnModules/UI_I_Deflectors.py`, `UI_H_Stigmators.py`, `UI_H_DeflectorsStigmators.py`).

- **Paper context**
  - These boards realize the electrostatic deflectors and stigmators discussed in the design section: they allow pure shift, pure tilt, and quadrupole fields for stigmation.
  - Plate voltages:
    - ±70 V amplifiers are adequate for alignment and stigmation.
    - ±400 V amplifiers are used for large‑area panning and scanning in SEM/STEM.
  - With the double‑deflector geometry (two plate sets along z, see Fig.7 in the paper), the system can decouple shift and tilt in software.

### High‑voltage scanning deflectors
- Path: `Electronics/High Voltage Column Deflectors (Scanning)/`
- Power board:
  - `FastScanDeflectorsV3.2Power/`
    - Project: `FastScanDeflectorsV3.2Power.pro`
    - Board: `FastScanDeflectorsV3.2Power.kicad_pcb`
    - Schematic: `FastScanDeflectorsV3.2Power.sch`, `Schematic.sch`
    - Libraries: `FastScanDeflectorsV3.2Power.lib`, `.dcm`.
- Control board:
  - `FastScanDeflectorsV3.1Controls/`
    - Project: `FastScanDeflectorsV3.1Controls.pro`
    - Schematics: `FastScanDeflectorsV3.1Controls.sch`, `ControlsAndIO.sch`, `MainSchematic.sch`.
    - Board: (KiCad layout; see `*.kicad_pcb` deeper in this tree).

These boards implement high‑speed scanning deflection; they are coordinated with the STEM image generation boards.

- **Paper context**
  - Deflector plate geometry: plates on a 5.08 mm circle in x–y over 10.16 mm along z, giving fields ≈28 V/mm (±70 V) or ≈158 V/mm (±400 V).
  - At U₀ = 50 kV, this provides ≈17 mrad maximum deflection, enough for ≈(100 μm)² fields of view with ≈1.5 nm step size using a 16‑bit DAC.
  - The paper shows that for very large FOVs (mm‑scale), distortion grows; this is acceptable for coarse navigation, not high‑precision metrology.

### Piezo mover & driver
- Piezo mover:
  - Path: `Electronics/Piezo Mover V3.2/`
  - PCB: `Board Files/` with KiCad project (`Piezo_Driver_V3.2.pro`), schematics (`Inputs.sch`, `Power.sch`, `Output.sch`, `IO_Page.sch`), and board file (`Piezo_Driver_V3.2.kicad_pcb`).
  - FPGA: `FPGA Code - PiezoMoverV3.2.0/PiezoMoverV3.2.0.xpr` (Vivado project).
- Piezo driver:
  - Path: `Electronics/Piezo_Driver_V4.2/Board Files/`
  - Project: `PiezoDriverV4.2.pro`
  - Schematics: `DigitalLogic.sch`, `Power.sch`, `Outputs.sch`, `PiezoDriverV4.2.sch`.
  - Board: `PiezoDriverV4.2.kicad_pcb`.
  - External wiring: `External Wiring/PiezoMoverExternalWiringV4.2.sch` and companions.

These interact with the stage/piezo modules in the control software (`NanoMi/Software/AddOnModules/UI_P_PiezoMover.py`).

### STEM image generation & power
- Path: `Electronics/STEM Image Generation/`
- STEM Scanner V1.0:
  - `STEM Image Generation V1.0/STEMScannerV1.0/`
    - Core project: `STEMScannerV1.0.pro`
    - Schematics split by function:
      - `ADC.kicad_sch`, `ADC.sch`
      - `DAC.kicad_sch`, `DAC.sch`
      - `Power.kicad_sch`, `Power.sch`
      - `SDRAM.kicad_sch`, `SDRAM.sch`
      - `USB.kicad_sch`, `USB.sch`
      - Top‑level: `STEMScannerV1.0.kicad_sch`, `STEMScannerV1.0.sch`
    - Board: `STEMScannerV1.0.kicad_pcb`
    - Resource directories: `3D Models/`, `Gerbers/`, `Simulation/`, `Spin Visualization/`.
- STEM Power V1.0:
  - `STEM Power V1.0/STEM_Power_V1.0/`
    - Project: `STEM_Power_V1.0.pro`
    - Schematic: `STEM_Power_V1.0.sch`, `Power.sch`
    - Board: `STEM_Power_V1.0.kicad_pcb`.

These boards pair with:
- FPGA and C/Python software in `NanoMi/STEM_Image_Generation_Code/`.
- Control software hooks (e.g. `UI_K_Scanner.py`) to integrate scanning and data acquisition.

- **Paper context**
  - The STEM board is designed to:
    - Generate X–Y analog scan signals.
    - Read up to eight analog detector channels simultaneously.
    - Store frames in on‑board RAM and transfer them to the host via USB as quickly as possible.
  - The KiCad projects in `Electronics/STEM Image Generation/` correspond one‑to‑one with the VHDL, C, and Python components described in the paper.

---

## Software Subsystems and Their Role in Rebuild

### Core control software (`NanoMi/Software`)
- Entry point: `NanoMi/Software/NANOmi.py`.
- UI modules in `NanoMi/Software/AddOnModules/`:
  - `UI_A_ElectronGun.py` – electron gun controls.
  - `UI_B_Lenses_Optics_Controller.py` and `UI_D_Lenses.py` – lens and optics control.
  - `UI_I_Deflectors.py`, `UI_H_Stigmators.py`, `UI_H_DeflectorsStigmators.py` – deflector and stigmator control and advanced settings.
  - `UI_N_Stage.py` – stage movement.
  - `UI_P_PiezoMover.py` – piezo mover.
  - `UI_R_Camera.py` – camera integration.
  - `UI_K_Scanner.py` – STEM scanner control.
  - `UI_U_DataSets.py` – saving and loading full microscope state.
- Hardware interface:
  - `Hardware.py` + `HardwareFiles/UsbInterface.py`, `AIOUSB.py` – talk to AIOUSB digital IO boards (as in `NanoMi/Software/README.md`).
  - `LibrariesForPiezoMover/` – USB drivers for piezo hardware (Silicon Labs).
  - `SaveFiles/` – XML (`DataSets.xml`, `StigmatorSettings.xml`, `DeflectorSettings.xml`, `IoAssignments*.txt`) that mirror the configuration shell from the paper.
  - These XML structures correspond directly to the `XML_shell` examples and to the “advanced deflector/stigmator” configuration described in the paper.

### STEM unit software (`NanoMi/STEM_Image_Generation_Code`)
- `HDL/`:
  - Vivado project: `STEM_Scanner.xpr`.
  - Core VHDL: `main.vhd`, `Analog_Inputs.vhd`, `ASYNC_FIFO.vhd`, and various IPs.
- `C_library/`:
  - Windows DLL and C source to move images between FPGA and host (e.g. `StemInterface.c`, `STEM.dll`).
- `python/`:
  - `STEM_Scanner.py` – PyQt6/pyqtgraph UI for scanning and data acquisition.
  - `UsbDLLInterface.py` – binding to the C DLL.

### Optics and modelling
- `NanoMi/nanomi-optics/`:
  - GUI entry point: `main.py` (PyQt).
  - Back‑end: `nanomi_optics/engine/` (lens models, excitation, optimization) and `nanomi_optics/gui/`.
  - Tests: `nanomi-optics/tests/` – a good reference for expected behaviour and numerical methods.
- `NanoMi/PythonOpticsCalculations/`:
  - Standalone scripts for focal length measurement, spherical and chromatic aberration, and thick lens matrices.
  - `NanoMi/RayOptics/`:
  - `NanoMi_Optics.py` – integrates with the ray-optics library to model the column.
  - These tools implement many of the analytical considerations in the paper:
    - Source demagnification and lens placement.
    - Effects of CS, CC, and defocus.
    - SEM/TEM/STEM/ED column layouts with shared sets of einzel lenses.

### Camera and external viewer integration
- `NanoMi/eye4nanomi/`:
  - `eye4nanomi.py` – PyQt5 GUI that:
    - Controls camera parameters via gphoto2.
    - Streams images into the panta‑rhei repository via ZMQ and its scripting API (`PRScriptingInterface`).
    - Provides a UI for live view and acquisition, tied into the microscope workflow.

---

## Detailed Roadmap to Rebuild OpenEM / NanoMi

> **Safety warning**: Rebuilding a TEM involves high voltage, vacuum, and potential X‑ray generation. You must work within your institution’s safety framework, with appropriate shielding, interlocks, and supervision. The steps below are technical guidance only.

### Phase 1 – Understand the System and Choose Targets
1. **Read the 2022 paper**:
   - Focus on sections describing:
     - Column layout and optics (lens positions, apertures, deflectors/stigmators).
     - Electron gun, working voltage, and imaging modes.
     - STEM unit description and performance metrics.
2. **Review official resources**:
   - Links in `NanoMi/README.md` to the NRC webpage, OSF project, and video give a practical overview of the assembled instrument.
3. **Pick a baseline revision**:
   - Mechanical: decide between `CAD files/NanoMi rev 5 horizontal column` and `NanoMi rev 6 vertical column` depending on your space and ergonomics.
   - Electronics: adopt the latest board revisions in `Electronics/` for each subsystem.

### Phase 2 – Infrastructure & Safety Planning
1. **Vacuum & hardware envelope**:
   - Define the vacuum system (pumps, roughing + turbo, valves, gauges) to match or exceed the paper’s vacuum levels.
   - Confirm flange standards and adaptors in your CAD model.
2. **High‑voltage & interlocks**:
   - Design or reuse high‑voltage power supplies per the paper’s specs:
     - U₀ up to 50 kV with ≈10 ppm total stability (ripple + drift) over tens of seconds.
     - Lens supplies UL with comparable fractional stability.
   - Plan interlocks on chamber doors, vacuum level, and panels.
3. **Lab layout**:
   - Use `CAD files/.../Air table/` assemblies to plan vibration isolation.
   - Ensure adequate space for access around electronics racks and pumps.

### Phase 3 – Mechanical Build
1. **Model clean‑up and checks**:
   - In your CAD tool, open the chosen `complete assembly` and verify:
     - All references resolve (no missing parts).
     - No interferences or collisions between moving parts and the column.
2. **Generate manufacturing packages**:
   - For each subassembly:
     - Produce 2D drawings (`*.dwg`/`*.pdf`) from `*.iam`/`*.ipt` if needed.
     - Export CAM-ready `*.stp` for shops requiring neutral formats.
3. **Fabricate & inspect**:
   - Machine parts, then measure critical dimensions (lens bores, flange faces, alignment features).
   - Assemble subassemblies (e.g. NanoMi internals, chamber, SED) before final stacking.
4. **Column & chamber integration**:
  - Integrate the gun, lenses, apertures, detector, and downstream hardware according to the assembly drawings and paper.
  - Install viewports and feedthroughs where required for electronics and camera.
   - Mount all electron‑optical components on a 127 mm half‑pipe inside the 152 mm column tube, preserving the “optics independent of vacuum envelope” concept from the paper.

### Phase 4 – Electronics Build & Bench Testing
1. **Per‑board build flow** (repeat for each project in `Electronics/`):
   - Open the KiCad project (e.g. `Electronics/Column Deflectors (Non-Scanning)/Deflector & Stigmator Boards V2.1/Board Files/DeflectorStigmatorsV2.1.pro`).
   - Verify design rules, footprints, and schematic integrity.
   - Use `Gerbers/` and drill files (already provided) to order boards.
   - Assemble PCBs and visually inspect solder joints and clearances.
2. **Subsystem-level bench tests**:
   - Deflectors/stigmators:
     - Check each analog output can swing to expected voltages under load.
     - Verify isolation and leakage, especially at high voltage nodes.
   - High‑voltage scan deflectors:
     - Verify high‑voltage stages with dummy loads before connecting to the column.
   - Piezo mover/driver:
     - Test low‑voltage signalling and motion on a dummy mass before installing on the column.
   - STEM boards:
     - Confirm power rails and clocks before FPGA programming.
      - Test basic X–Y scan waveform integrity and detector channel readout using dummy loads before operating with a real sample.

### Phase 5 – STEM Unit, FPGA, and Host Software
1. **FPGA toolchain**:
   - Install Vivado (version similar to that used in `NanoMi/STEM_Image_Generation_Code/README.md`, e.g. 2022.2).
2. **FPGA build**:
   - Open `NanoMi/STEM_Image_Generation_Code/HDL/STEM_Scanner.xpr`.
   - Synthesize and implement the design (`main.vhd`, associated IP).
   - Program the FPGA on the STEM scanner board.
3. **Host-side interface**:
   - Build the C shared library (`NanoMi/STEM_Image_Generation_Code/C_library/`).
   - Install Python 3.12 with `pyqt6`, `pyqtgraph`, and `numpy`.
   - Launch `NanoMi/STEM_Image_Generation_Code/python/STEM_Scanner.py` and confirm communication with the board.
   - Validate:
     - Correct mapping between scan waveform and image coordinates.
     - Stable frame rates and data transfer as described in the paper.

### Phase 6 – Control Software & Configuration
1. **System preparation**:
   - Install openSUSE Tumbleweed or another supported Linux distribution.
   - Install AIOUSB as described in `NanoMi/Software/README.md`.
2. **Python environment**:
   - Install PyQt5 and dependencies for `NanoMi/Software/`, plus any module imports in `AddOnModules`.
3. **Launch NanoMi control UI**:
   - From repo root:
     - `cd NanoMi/Software`
     - `python NANOmi.py`
4. **Map hardware IO**:
   - Use the Hardware module UI to:
     - Scan IO boards.
     - Confirm all analog and digital channels are detected.
   - Save `IoAssignments.txt` and check backup versions (`IoAssignments_date_time.txt`) in `SaveFiles/`.
5. **Configure deflectors & stigmators**:
   - Use the advanced settings in the deflector and stigmator UIs to:
     - Assign each plate to the correct DAC channel as per your wiring.
     - Use `2022 NanoMi paper/XML_shell/DeflectorSettings.xml` as a structural template.
   - Save settings and verify that they persist.
   - Use the plate‑by‑plate control to:
     - Implement the double‑deflector geometry for pure shift or tilt.
     - Implement two quadrupole stigmators rotated by 45° to allow arbitrary astigmatism correction (as in the paper’s stigmator design).
6. **Datasets and state management**:
   - Use the Data Sets UI (`UI_U_DataSets.py`) to:
     - Save instrument states (`DataSets.xml`).
     - Load states and verify that module values update correctly.

### Phase 7 – Camera & External Viewer Integration
1. **Camera stack**:
   - Install gphoto2 and confirm your camera is supported.
   - Install the panta‑rhei image viewer and enable the scripting server.
2. **eye4nanomi configuration**:
   - Run `python NanoMi/eye4nanomi/eye4nanomi.py`.
   - Verify:
     - ZMQ connection to panta‑rhei (`tcp://localhost:8888`).
     - Live view, ISO and shutter control, and image saving.
3. **Link to control software**:
  - Ensure the NanoMi control UI and eye4nanomi are using consistent paths and naming conventions for saved images and datasets.

### Phase 8 – Alignment, Commissioning, and Optimization
1. **Initial beam setup**:
   - Follow the paper’s guidance on:
     - Electron gun conditioning.
     - First beam, focusing, and stigmation.
2. **Deflector and stigmator calibration**:
   - Use deflector modules to:
     - Center the beam and verify linear response.
   - Use stigmator modules to:
     - Minimize astigmatism as seen on the camera.
      - Reproduce tests similar to those in the paper (e.g., imaging a Quantifoil 7×7 μm grid on a 200 mesh support and measuring aspect ratio as a function of stigmator voltage).
3. **STEM imaging**:
   - Bring the STEM unit online:
     - Apply scanning waveforms.
     - Verify image formation and contrast.
      - Use the paper’s reported probe size, FOV, and dwell time as benchmarks for your own instrument.
4. **Optics modelling and feedback**:
   - Use:
     - `NanoMi/nanomi-optics/` to visualize and optimize lens settings.
     - `NanoMi/PythonOpticsCalculations/` to compute focal lengths and aberrations.
     - `NanoMi/RayOptics/` to model the full column.
   - Adjust mechanical alignment and lens currents based on these tools and experimental data.

### Phase 9 – Document and Contribute
1. **Document your build**:
   - Keep a log of:
     - Deviations from CAD or electronics BOM.
     - Alternate components or power supplies.
     - Software changes and script versions.
2. **Share improvements**:
   - Use `AGENTS.md` and the root `README.md` for guidance on:
     - Where to add new CAD or electronics variants.
     - How to structure software contributions.
   - Consider contributing:
     - New board revisions (e.g. updated regulators, connectors).
     - Additional optics models or scripts.
     - Improved documentation for specific lab configurations.

Use this reference as a deep index and multi‑phase checklist. When in doubt, always cross‑check against the 2022 NanoMi paper, the OSF resources, and the KiCad/CAD source files in this repository.
