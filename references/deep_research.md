# Deep Research Notes

## Concept

The target device is a hybrid scientific camera/detector that combines four measurement types on one controlled board:

1. **Single-pixel bucket channel** for high dynamic range, lock-in detection, spectroscopy, or electron-counting style intensity integration.
2. **Event channel** for low-latency temporal contrast and sparse high-speed motion/scan changes.
3. **Frame channel** for absolute texture, geometry, calibration, and human-readable preview.
4. **Spectral channel** using filters, grating, scintillator spectrum, or a small spectrometer input.

The proposed pixel organization is "Weiqi-board" inspired: a central bucket detector, surrounded by alternating event and frame tiles. This is easier to prototype than a monolithic custom pixel ASIC because each sensing mode can start as a replaceable module.

## Event Sensors

The classic DVS paper by Lichtsteiner, Posch, and Delbruck describes a 128x128 temporal-contrast CMOS sensor where each pixel independently emits asynchronous events after local relative intensity changes, with 120 dB dynamic range and 15 us latency ([PDF](https://tilde.ini.uzh.ch/~tobi/wiki/lib/exe/fetch.php?media=lichtsteiner_dvs_jssc08.pdf)). The broader event-camera field is summarized by Gallego et al., who emphasize asynchronous sensing, high dynamic range, low latency, and low power ([survey](https://portal.fis.tum.de/en/publications/event-based-vision-a-survey/)).

DAVIS shows the most relevant precedent for this project: it outputs DVS events and global-shutter APS frames concurrently while sharing one photodiode between DVS and APS circuits ([EPFL record](https://infoscience.epfl.ch/entities/publication/18690ec7-3340-4648-a9b1-862a9b5673c5)). Prophesee/Sony IMX636 is a practical commercial reference: 1280x720 event resolution, 4.86 um pixels, less than 100 us latency at 1000 lux, and dynamic range above 86 dB or 120 dB depending on illumination span ([Prophesee](https://www.prophesee.ai/event-based-sensor-imx636-sony-prophesee/)).

## Single-Pixel Imaging

Single-pixel imaging reconstructs a scene from coded measurements rather than a dense pixel array. The Nature Photonics review by Edgar et al. covers compressed sensing, 3D, polarimetric, and spectrometer variants ([review](https://www.nature.com/articles/s41566-018-0300-7)). Recent cascaded compressed-sensing work shows that single-pixel cameras can be extended to higher-dimensional optical data such as light fields and hyperspectral-like measurements ([PhotoniX](https://link.springer.com/article/10.1186/s43074-024-00152-5)).

For this project, the single-pixel path is valuable because one carefully designed detector can outperform small pixels in dynamic range, noise, spectral flexibility, and radiation tolerance. It can also provide a robust scalar constraint for event/frame reconstruction.

## Electron Microscopy Motivation

NanoMi provides the open hardware/software microscope context: an open-source electron microscope platform with modular, UHV-compatible components for TEM, SEM, STEM, and diffraction experiments ([NRC page](https://nrc.canada.ca/en/research-development/nanomi-worlds-first-open-source-transmission-electron-microscope), [publication record](https://nrc-publications.canada.ca/eng/view/object/?id=02fb266b-721d-4a35-b825-0af8044db446)). Event-driven electron detection is also relevant: Timepix3-based 4D STEM work reports dwell times down to 100 ns by avoiding frame-driven readout limits ([arXiv](https://arxiv.org/abs/2107.02864)). The 4D Camera paper reports an 87 kHz direct electron detector and sparse electron-counting reductions of 10x to 300x ([arXiv](https://arxiv.org/abs/2305.11961)).

## Open-Source Software Anchors

OpenEB is Prophesee's open event-based framework, with HAL, base, core, ML, stream, and UI modules for camera operation and event processing ([GitHub](https://github.com/prophesee-ai/openeb)). Prophesee also maintains starter examples for live/recorded event retrieval, visualization, time surfaces, and optical flow demos ([GitHub](https://github.com/prophesee-ai/event-based-get-started)).

For reconstruction, E2VID converts event streams into videos so standard vision algorithms can be reused ([paper PDF](https://vladlen.info/papers/E2VID.pdf), [code](https://github.com/uzh-rpg/rpg_e2vid)). SPyRiT is a PyTorch toolbox for single-pixel image reconstruction and is a strong software reference for the bucket-detector branch ([GitHub](https://github.com/openspyrit/spyrit)).

## Recommended Prototype Path

1. Build a benchtop board with central photodiode/TIA, one frame camera module, and one event camera module sharing a trigger clock.
2. Add a tiled comparator photodiode subarray derived from `CustomSensor` to test DIY event behavior.
3. Add a filter wheel, grating, or spectrometer input to the bucket channel.
4. Integrate with scan signals from NanoMi-style SEM/STEM experiments.
5. Move from board-level fusion to custom pixel/tile silicon only after the timing model, data format, and reconstruction objective are validated.
