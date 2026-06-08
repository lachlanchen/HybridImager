# HybridCamera

HybridCamera is a research and design workspace for a mixed sensing board: a high-dynamic-range single-pixel detector at the center, alternating event and frame-mode tiles around it, and optional spectral/electron-microscopy detector branches. The layout is intentionally "Weiqi-board" like: local pixels are arranged as a checkerboard of complementary sensing modes, while the central bucket detector supplies absolute intensity and high dynamic range.

## Repository Layout

- `init/` records what was copied from prior local work and how this repo was initialized.
- `references/` contains cited research notes on event sensors, single-pixel imaging, PCB/circuit design, wiring, and reconstruction.
- `publications/` contains the LaTeX concept paper.
- `figures/` stores deterministic SVG/PNG diagrams plus AgInTi-generated concept images.
- `hardware/`, `firmware/`, and `algorithms/` are implementation staging areas.
- `copied-context/` preserves relevant snapshots from `CustomSensor`, `NanoMi`, and AppAutoAction notes.

## Prior Work Check

Yes, `../CustomSensor` already contains related research. Its documents cover a digiOBSCURA 32x32 phototransistor camera, firmware differencing, comparator-assisted event mode, TIA/buffer upgrades, and a full event-sensor redesign path. This repo uses that work as the DIY baseline, but extends the scope to a hybrid scientific detector that combines single-pixel, spectral, frame, and event data streams.

## Generate Figures and Paper

```bash
python3 scripts/draw_hybrid_camera_diagrams.py
cd publications
pdflatex -interaction=nonstopmode -halt-on-error hybrid_camera_concept.tex
pdflatex -interaction=nonstopmode -halt-on-error open_camera_project_survey.tex
```

AgInTi concept art can be generated with:

```bash
node ../Agent/AgInTiFlow/bin/aginti-cli.js image --json --provider venice \
  --format png --output-dir figures/aginti --output-stem hybrid-camera-concept \
  --aspect-ratio 16:9 --image-size 2K "technical hybrid scientific camera board..."
```

## Design Thesis

The first build should not attempt a full custom event-imager ASIC. Use commercial event/frame modules or tiled photodiode/comparator subarrays, a central low-noise TIA bucket detector, synchronized ADC/event capture, and calibration targets. The reconstruction layer then fuses sparse event timing, frame texture, single-pixel absolute intensity, and spectral measurements into a shared latent scene or scan grid.

## Open Project Survey

The current survey is in `references/open_camera_project_survey.md` and compiled
as `publications/open_camera_project_survey.pdf`. It documents cloned open
single-pixel, event-camera, and frame-camera projects, plus buying/sourcing notes
for ONE-PIX, UPOLabs, DLP/DMD parts, Prophesee/Sony IMX636 event cameras, and
Shapr3D export guidance. Preferred Shapr3D export package: `STEP`, native
`.shapr`, `Parasolid`, `DXF from sketch`, and one `3MF` or `STL` preview.
