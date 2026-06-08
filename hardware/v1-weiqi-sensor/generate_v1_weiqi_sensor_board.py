#!/usr/bin/env python3
"""Generate the HybridImager V1 sparse Weiqi sensor-board draft."""

from __future__ import annotations

import csv
import json
import math
import shutil
import uuid
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d.art3d import Poly3DCollection


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "hardware/v1-weiqi-sensor"
ARTIFACT_DIR = OUT_DIR / "artifacts"
GERBER_DIR = OUT_DIR / "gerber"
BOARD_NAME = "hybridimager-v1-weiqi-sensor"
BOARD = OUT_DIR / f"{BOARD_NAME}.kicad_pcb"
PROJECT = OUT_DIR / f"{BOARD_NAME}.kicad_pro"
SCHEMATIC = OUT_DIR / f"{BOARD_NAME}.kicad_sch"
FP_LIB_TABLE = OUT_DIR / "fp-lib-table"
DATASET = OUT_DIR / "hybridimager-v1-source-dataset.json"
BOM = OUT_DIR / "hybridimager-v1-bom.csv"
README = OUT_DIR / "README.md"
LOCAL_GITIGNORE = OUT_DIR / ".gitignore"
PREVIEW = ARTIFACT_DIR / "hybridimager-v1-full-view-render.png"

MODEL_LED = "/usr/share/kicad/3dmodels/LED_THT.3dshapes/LED_D3.0mm_IRBlack.step"
MODEL_SOIC = "/usr/share/kicad/3dmodels/Package_SO.3dshapes/SOIC-8_3.9x4.9mm_P1.27mm.step"
MODEL_QFN = "/usr/share/kicad/3dmodels/Package_DFN_QFN.3dshapes/QFN-48-1EP_7x7mm_P0.5mm_EP5.15x5.15mm.step"
MODEL_2X20 = "/usr/share/kicad/3dmodels/Connector_PinHeader_2.54mm.3dshapes/PinHeader_2x20_P2.54mm_Vertical.step"
MODEL_1X10 = "/usr/share/kicad/3dmodels/Connector_PinHeader_2.54mm.3dshapes/PinHeader_1x10_P2.54mm_Vertical.step"
MODEL_SMA = "/usr/share/kicad/3dmodels/Connector_Coaxial.3dshapes/SMA_Amphenol_132291_Vertical.step"


def uid(name: str) -> str:
    return str(uuid.uuid5(uuid.NAMESPACE_URL, f"lazyingart:hybridimager:{BOARD_NAME}:{name}"))


def prop(name: str, value: str, at: str, layer: str = "F.Fab", hide: bool = False) -> str:
    hidden = "\n\t\t\t(hide yes)" if hide else ""
    return f"""\t\t(property "{name}" "{value}"
\t\t\t(at {at})
\t\t\t(layer "{layer}"){hidden}
\t\t\t(uuid "{uid(f'prop:{name}:{value}:{at}:{layer}')}")
\t\t\t(effects (font (size 0.9 0.9) (thickness 0.12)))
\t\t)"""


def gr_line(layer: str, x1: float, y1: float, x2: float, y2: float, name: str, width: float = 0.12) -> str:
    return f'\t(gr_line (start {x1:g} {y1:g}) (end {x2:g} {y2:g}) (stroke (width {width:g}) (type solid)) (layer "{layer}") (uuid "{uid(name)}"))'


def gr_rect(layer: str, x1: float, y1: float, x2: float, y2: float, name: str, width: float = 0.12) -> str:
    return "\n".join(
        [
            gr_line(layer, x1, y1, x2, y1, f"{name}:top", width),
            gr_line(layer, x2, y1, x2, y2, f"{name}:right", width),
            gr_line(layer, x2, y2, x1, y2, f"{name}:bottom", width),
            gr_line(layer, x1, y2, x1, y1, f"{name}:left", width),
        ]
    )


def track(name: str, layer: str, x1: float, y1: float, x2: float, y2: float, net_id: int = 1, width: float = 0.45) -> str:
    return f'\t(segment (start {x1:g} {y1:g}) (end {x2:g} {y2:g}) (width {width:g}) (layer "{layer}") (net {net_id}) (uuid "{uid(name)}"))'


def via(name: str, x: float, y: float, net_id: int = 1) -> str:
    return f'\t(via (at {x:g} {y:g}) (size 0.8) (drill 0.4) (layers "F.Cu" "B.Cu") (net {net_id}) (uuid "{uid(name)}"))'


def mounting_hole(ref: str, x: float, y: float) -> str:
    return f"""
\t(footprint "MountingHole:MountingHole_3.2mm_M3"
\t\t(layer "F.Cu")
\t\t(uuid "{uid(ref)}")
\t\t(at {x:g} {y:g})
{prop("Reference", ref, "0 -4 0", "F.Fab", True)}
{prop("Value", "M3", "0 4 0", "F.Fab", True)}
\t\t(attr exclude_from_pos_files)
\t\t(fp_circle (center 0 0) (end 3.2 0) (stroke (width 0.15) (type solid)) (fill none) (layer "Cmts.User") (uuid "{uid(ref + ':circle')}"))
\t\t(pad "" np_thru_hole circle (at 0 0) (size 3.2 3.2) (drill 3.2) (layers "*.Cu" "*.Mask") (uuid "{uid(ref + ':pad')}"))
\t)"""


def detector(ref: str, x: float, y: float, net_id: int, net_name: str) -> str:
    return f"""
\t(footprint "Sparse_SP_D3_Photodiode"
\t\t(layer "F.Cu")
\t\t(uuid "{uid(ref)}")
\t\t(at {x:g} {y:g})
\t\t(descr "V1 sparse single-pixel detector placeholder, 3 mm THT photodiode class")
\t\t(tags "single-pixel sparse photodiode weiqi")
{prop("Reference", ref, "0 -4.2 0", "F.SilkS")}
{prop("Value", "SPARSE_PHOTODIODE_D3", "0 4.2 0", "F.Fab", True)}
\t\t(attr through_hole)
\t\t(fp_circle (center 0 0) (end 2.4 0) (stroke (width 0.12) (type solid)) (fill none) (layer "F.SilkS") (uuid "{uid(ref + ':silk')}"))
\t\t(fp_circle (center 0 0) (end 3.1 0) (stroke (width 0.05) (type solid)) (fill none) (layer "F.CrtYd") (uuid "{uid(ref + ':court')}"))
\t\t(fp_text user "{net_name}" (at 0 3.35 0) (layer "F.Fab") (uuid "{uid(ref + ':label')}") (effects (font (size 0.65 0.65) (thickness 0.08))))
\t\t(pad "S" thru_hole rect (at 0 -1.27) (size 1.6 1.6) (drill 0.8) (layers "*.Cu" "*.Mask") (remove_unused_layers no) (net {net_id} "{net_name}") (pinfunction "SIGNAL") (pintype "passive") (uuid "{uid(ref + ':sig')}"))
\t\t(pad "G" thru_hole circle (at 0 1.27) (size 1.6 1.6) (drill 0.8) (layers "*.Cu" "*.Mask") (remove_unused_layers no) (net 1 "GND") (pinfunction "GUARD") (pintype "passive") (uuid "{uid(ref + ':gnd')}"))
\t\t(model "{MODEL_LED}" (offset (xyz 0 0 0)) (scale (xyz 1 1 1)) (rotate (xyz 0 0 0)))
\t)"""


def testpad(ref: str, x: float, y: float, net_id: int, net_name: str) -> str:
    return f"""
\t(footprint "TP_1.7mm_SMD"
\t\t(layer "F.Cu")
\t\t(uuid "{uid(ref)}")
\t\t(at {x:g} {y:g})
{prop("Reference", ref, "0 -1.6 0", "F.Fab", True)}
{prop("Value", net_name, "0 1.6 0", "F.Fab", True)}
\t\t(attr smd exclude_from_pos_files)
\t\t(fp_circle (center 0 0) (end 1.05 0) (stroke (width 0.08) (type solid)) (fill none) (layer "F.SilkS") (uuid "{uid(ref + ':silk')}"))
\t\t(pad "1" smd circle (at 0 0) (size 1.7 1.7) (layers "F.Cu" "F.Mask") (net {net_id} "{net_name}") (pinfunction "PROBE") (pintype "passive") (uuid "{uid(ref + ':pad')}"))
\t)"""


def pinheader_2x20(ref: str, x: float, y: float) -> str:
    pads = []
    for row in range(20):
        py = (row - 9.5) * 2.54
        pads.append(f'\t\t(pad "{row * 2 + 1}" thru_hole rect (at -1.27 {py:g}) (size 1.7 1.7) (drill 0.95) (layers "*.Cu" "*.Mask") (net {100 + row} "EXP_{row + 1:02d}") (pinfunction "EXP_{row + 1:02d}") (pintype "passive") (uuid "{uid(ref + f":pad{row * 2 + 1}")}"))')
        pads.append(f'\t\t(pad "{row * 2 + 2}" thru_hole circle (at 1.27 {py:g}) (size 1.7 1.7) (drill 0.95) (layers "*.Cu" "*.Mask") (net 1 "GND") (pinfunction "GND") (pintype "passive") (uuid "{uid(ref + f":pad{row * 2 + 2}")}"))')
    return f"""
\t(footprint "Connector_PinHeader_2.54mm:PinHeader_2x20_P2.54mm_Vertical"
\t\t(layer "F.Cu")
\t\t(uuid "{uid(ref)}")
\t\t(at {x:g} {y:g})
{prop("Reference", ref, "0 -28 0", "F.SilkS")}
{prop("Value", "AFE_EXPANSION_2x20", "0 28 0", "F.Fab", True)}
\t\t(attr through_hole)
\t\t(fp_rect (start -3.3 -26.2) (end 3.3 26.2) (stroke (width 0.1) (type solid)) (fill none) (layer "F.SilkS") (uuid "{uid(ref + ':rect')}"))
{chr(10).join(pads)}
\t\t(model "{MODEL_2X20}" (offset (xyz 0 0 0)) (scale (xyz 1 1 1)) (rotate (xyz 0 0 0)))
\t)"""


def pinheader_1x10(ref: str, x: float, y: float) -> str:
    names = ["+5V", "+3V3", "GND", "FRAME_TRIG", "EVENT_SYNC", "ADC_CLK", "I2C_SDA", "I2C_SCL", "SCAN_TTL", "GPIO0"]
    net_lookup = {"+5V": 2, "+3V3": 3, "GND": 1, "FRAME_TRIG": 40, "EVENT_SYNC": 41, "ADC_CLK": 42, "I2C_SDA": 43, "I2C_SCL": 44, "SCAN_TTL": 45, "GPIO0": 46}
    pads = []
    for idx, name in enumerate(names):
        py = (idx - 4.5) * 2.54
        shape = "rect" if idx == 0 else "circle"
        pads.append(f'\t\t(pad "{idx + 1}" thru_hole {shape} (at 0 {py:g}) (size 1.7 1.7) (drill 0.95) (layers "*.Cu" "*.Mask") (net {net_lookup[name]} "{name}") (pinfunction "{name}") (pintype "passive") (uuid "{uid(ref + f":pad{idx + 1}")}"))')
    return f"""
\t(footprint "Connector_PinHeader_2.54mm:PinHeader_1x10_P2.54mm_Vertical"
\t\t(layer "F.Cu")
\t\t(uuid "{uid(ref)}")
\t\t(at {x:g} {y:g})
{prop("Reference", ref, "0 -15 0", "F.SilkS")}
{prop("Value", "SYNC_PWR_1x10", "0 15 0", "F.Fab", True)}
\t\t(attr through_hole)
\t\t(fp_rect (start -1.7 -13.5) (end 1.7 13.5) (stroke (width 0.1) (type solid)) (fill none) (layer "F.SilkS") (uuid "{uid(ref + ':rect')}"))
{chr(10).join(pads)}
\t\t(model "{MODEL_1X10}" (offset (xyz 0 0 0)) (scale (xyz 1 1 1)) (rotate (xyz 0 0 0)))
\t)"""


def soic8(ref: str, x: float, y: float, rot: float = 0) -> str:
    pads = []
    for idx in range(4):
        py = (idx - 1.5) * 1.27
        pads.append(f'\t\t(pad "{idx + 1}" smd roundrect (at -2.7 {py:g} {rot:g}) (size 1.5 0.6) (layers "F.Cu" "F.Paste" "F.Mask") (roundrect_rratio 0.2) (net {120 + idx} "{ref}_P{idx + 1}") (pinfunction "P{idx + 1}") (pintype "passive") (uuid "{uid(ref + f":pad{idx + 1}")}"))')
        pads.append(f'\t\t(pad "{8 - idx}" smd roundrect (at 2.7 {py:g} {rot:g}) (size 1.5 0.6) (layers "F.Cu" "F.Paste" "F.Mask") (roundrect_rratio 0.2) (net {124 + idx} "{ref}_P{8 - idx}") (pinfunction "P{8 - idx}") (pintype "passive") (uuid "{uid(ref + f":pad{8 - idx}")}"))')
    return f"""
\t(footprint "Package_SO:SOIC-8_3.9x4.9mm_P1.27mm"
\t\t(layer "F.Cu")
\t\t(uuid "{uid(ref)}")
\t\t(at {x:g} {y:g} {rot:g})
{prop("Reference", ref, "0 -4 0", "F.SilkS")}
{prop("Value", "TIA_PLACEHOLDER", "0 4 0", "F.Fab", True)}
\t\t(attr smd)
\t\t(fp_rect (start -2 -2.55) (end 2 2.55) (stroke (width 0.12) (type solid)) (fill none) (layer "F.SilkS") (uuid "{uid(ref + ':rect')}"))
{chr(10).join(pads)}
\t\t(model "{MODEL_SOIC}" (offset (xyz 0 0 0)) (scale (xyz 1 1 1)) (rotate (xyz 0 0 0)))
\t)"""


def qfn48(ref: str, x: float, y: float) -> str:
    pads = [f'\t\t(pad "EP" smd rect (at 0 0) (size 4.8 4.8) (layers "F.Cu" "F.Paste" "F.Mask") (net 1 "GND") (pinfunction "EP") (pintype "passive") (uuid "{uid(ref + ":ep")}"))']
    for idx in range(12):
        p = idx + 1
        offset = -2.75 + idx * 0.5
        pads.append(f'\t\t(pad "{p}" smd roundrect (at {offset:g} -3.85) (size 0.28 1.0) (layers "F.Cu" "F.Paste" "F.Mask") (roundrect_rratio 0.2) (net {160 + p} "{ref}_P{p}") (pinfunction "P{p}") (pintype "passive") (uuid "{uid(ref + f":pad{p}")}"))')
        pads.append(f'\t\t(pad "{p + 12}" smd roundrect (at 3.85 {offset:g}) (size 1.0 0.28) (layers "F.Cu" "F.Paste" "F.Mask") (roundrect_rratio 0.2) (net {160 + p + 12} "{ref}_P{p + 12}") (pinfunction "P{p + 12}") (pintype "passive") (uuid "{uid(ref + f":pad{p + 12}")}"))')
        pads.append(f'\t\t(pad "{p + 24}" smd roundrect (at {-offset:g} 3.85) (size 0.28 1.0) (layers "F.Cu" "F.Paste" "F.Mask") (roundrect_rratio 0.2) (net {160 + p + 24} "{ref}_P{p + 24}") (pinfunction "P{p + 24}") (pintype "passive") (uuid "{uid(ref + f":pad{p + 24}")}"))')
        pads.append(f'\t\t(pad "{p + 36}" smd roundrect (at -3.85 {-offset:g}) (size 1.0 0.28) (layers "F.Cu" "F.Paste" "F.Mask") (roundrect_rratio 0.2) (net {160 + p + 36} "{ref}_P{p + 36}") (pinfunction "P{p + 36}") (pintype "passive") (uuid "{uid(ref + f":pad{p + 36}")}"))')
    return f"""
\t(footprint "Package_DFN_QFN:QFN-48-1EP_7x7mm_P0.5mm_EP5.15x5.15mm"
\t\t(layer "F.Cu")
\t\t(uuid "{uid(ref)}")
\t\t(at {x:g} {y:g})
{prop("Reference", ref, "0 -5.4 0", "F.SilkS")}
{prop("Value", "TIMESTAMP_MCU_FPGA_PLACEHOLDER", "0 5.4 0", "F.Fab", True)}
\t\t(attr smd)
\t\t(fp_rect (start -3.7 -3.7) (end 3.7 3.7) (stroke (width 0.12) (type solid)) (fill none) (layer "F.SilkS") (uuid "{uid(ref + ':rect')}"))
{chr(10).join(pads)}
\t\t(model "{MODEL_QFN}" (offset (xyz 0 0 0)) (scale (xyz 1 1 1)) (rotate (xyz 0 0 0)))
\t)"""


def sma(ref: str, x: float, y: float, net_id: int, net_name: str) -> str:
    return f"""
\t(footprint "Connector_Coaxial:SMA_Amphenol_132291_Vertical"
\t\t(layer "F.Cu")
\t\t(uuid "{uid(ref)}")
\t\t(at {x:g} {y:g})
{prop("Reference", ref, "0 -5.5 0", "F.SilkS")}
{prop("Value", net_name, "0 5.5 0", "F.Fab", True)}
\t\t(attr through_hole)
\t\t(fp_circle (center 0 0) (end 4.1 0) (stroke (width 0.12) (type solid)) (fill none) (layer "F.SilkS") (uuid "{uid(ref + ':circle')}"))
\t\t(pad "1" thru_hole circle (at 0 0) (size 2.2 2.2) (drill 1.3) (layers "*.Cu" "*.Mask") (net {net_id} "{net_name}") (pinfunction "SIG") (pintype "passive") (uuid "{uid(ref + ':sig')}"))
\t\t(pad "2" thru_hole circle (at -2.54 -2.54) (size 1.6 1.6) (drill 1.0) (layers "*.Cu" "*.Mask") (net 1 "GND") (pinfunction "GND") (pintype "passive") (uuid "{uid(ref + ':g1')}"))
\t\t(pad "3" thru_hole circle (at 2.54 -2.54) (size 1.6 1.6) (drill 1.0) (layers "*.Cu" "*.Mask") (net 1 "GND") (pinfunction "GND") (pintype "passive") (uuid "{uid(ref + ':g2')}"))
\t\t(pad "4" thru_hole circle (at -2.54 2.54) (size 1.6 1.6) (drill 1.0) (layers "*.Cu" "*.Mask") (net 1 "GND") (pinfunction "GND") (pintype "passive") (uuid "{uid(ref + ':g3')}"))
\t\t(pad "5" thru_hole circle (at 2.54 2.54) (size 1.6 1.6) (drill 1.0) (layers "*.Cu" "*.Mask") (net 1 "GND") (pinfunction "GND") (pintype "passive") (uuid "{uid(ref + ':g4')}"))
\t\t(model "{MODEL_SMA}" (offset (xyz 0 0 0)) (scale (xyz 1 1 1)) (rotate (xyz 0 0 0)))
\t)"""


def zone(layer: str) -> str:
    return f"""
\t(zone
\t\t(net 1)
\t\t(net_name "GND")
\t\t(layer "{layer}")
\t\t(uuid "{uid('zone:' + layer)}")
\t\t(hatch edge 0.508)
\t\t(connect_pads yes (clearance 0.35))
\t\t(min_thickness 0.254)
\t\t(filled_areas_thickness no)
\t\t(fill yes (thermal_gap 0.508) (thermal_bridge_width 0.508))
\t\t(polygon
\t\t\t(pts
\t\t\t\t(xy 50 55) (xy 155 55) (xy 155 145) (xy 50 145)
\t\t\t)
\t\t)
\t)"""


def detector_positions() -> list[tuple[int, int]]:
    return [
        (-3, -3), (0, -3), (3, -3),
        (-1, -2), (1, -2),
        (-2, -1), (0, -1), (2, -1),
        (-3, 0), (-1, 0), (1, 0), (3, 0),
        (-2, 1), (0, 1), (2, 1),
        (-1, 2), (1, 2),
        (-3, 3), (0, 3), (3, 3),
        (0, 0),
    ]


def board_text() -> str:
    nets = ['\t(net 0 "")', '\t(net 1 "GND")', '\t(net 2 "+5V")', '\t(net 3 "+3V3")']
    for idx in range(21):
        nets.append(f'\t(net {10 + idx} "SP{idx + 1:02d}")')
    for net_id, name in [(40, "FRAME_TRIG"), (41, "EVENT_SYNC"), (42, "ADC_CLK"), (43, "I2C_SDA"), (44, "I2C_SCL"), (45, "SCAN_TTL"), (46, "GPIO0"), (47, "SYNC_IN"), (48, "SYNC_OUT")]:
        nets.append(f'\t(net {net_id} "{name}")')
    for idx in range(20):
        nets.append(f'\t(net {100 + idx} "EXP_{idx + 1:02d}")')
    for idx in range(80):
        nets.append(f'\t(net {120 + idx} "LOCAL_{idx + 1:02d}")')

    footprints = [
        mounting_hole("H1", 57, 62),
        mounting_hole("H2", 148, 62),
        mounting_hole("H3", 148, 138),
        mounting_hole("H4", 57, 138),
        pinheader_2x20("J1", 145, 100),
        pinheader_1x10("J2", 55, 100),
        soic8("U1", 128, 76, 90),
        soic8("U2", 128, 100, 90),
        soic8("U3", 128, 124, 90),
        qfn48("U4", 111, 137),
        sma("J3", 67, 137, 47, "SYNC_IN"),
        sma("J4", 83, 137, 48, "SYNC_OUT"),
    ]
    segments = []
    detector_ground_rows: dict[float, list[float]] = {}
    pitch = 8.5
    center_x, center_y = 91, 100
    for idx, (gx, gy) in enumerate(detector_positions(), start=1):
        x = center_x + gx * pitch
        y = center_y + gy * pitch
        net_id = 10 + idx - 1
        net_name = f"SP{idx:02d}"
        tp_x = x + 3.8
        tp_y = y - 1.27
        footprints.append(detector(f"PD{idx:02d}", x, y, net_id, net_name))
        footprints.append(testpad(f"TP{idx:02d}", tp_x, tp_y, net_id, net_name))
        segments.append(track(f"seg:sp{idx}", "F.Cu", x, y - 1.27, tp_x, tp_y, net_id, 0.22))
        detector_ground_rows.setdefault(round(y + 1.27, 3), []).append(x)

    left_bus_x = 60.5
    right_bus_x = 146.27
    top_bus_y = 66.5
    for row_idx, (ground_y, xs) in enumerate(sorted(detector_ground_rows.items())):
        segments.append(track(f"gnd:det-row:{row_idx}", "B.Cu", left_bus_x, ground_y, max(xs), ground_y, 1, 0.45))
    segments.extend(
        [
            track("gnd:left-bus", "B.Cu", left_bus_x, top_bus_y, left_bus_x, 139.54, 1, 0.55),
            track("gnd:top-tie", "B.Cu", left_bus_x, top_bus_y, right_bus_x, top_bus_y, 1, 0.55),
            track("gnd:j1-bus", "B.Cu", right_bus_x, top_bus_y, right_bus_x, 124.13, 1, 0.55),
            track("gnd:j2", "B.Cu", 55.0, 93.65, left_bus_x, 93.65, 1, 0.55),
            track("gnd:sma-top", "B.Cu", left_bus_x, 134.46, 85.54, 134.46, 1, 0.55),
            track("gnd:sma-bottom", "B.Cu", left_bus_x, 139.54, 85.54, 139.54, 1, 0.55),
            via("gnd:u4-ep-via", 111, 137, 1),
            track("gnd:u4-vertical", "B.Cu", 111, 137, 111, 132, 1, 0.45),
            track("gnd:u4-return", "B.Cu", left_bus_x, 132, 111, 132, 1, 0.45),
        ]
    )

    drawings = [
        gr_rect("Edge.Cuts", 50, 55, 155, 145, "edge", 0.15),
        gr_rect("Dwgs.User", 62, 70, 120, 130, "sensor-island", 0.18),
        gr_rect("F.Fab", 63.5, 71.5, 118.5, 128.5, "sensor-active", 0.10),
        '\t(gr_text "HybridImager V1 Weiqi Sparse Sensor" (at 102 59.5 0) (layer "F.SilkS") (uuid "' + uid("text:title") + '") (effects (font (size 1.4 1.4) (thickness 0.18))))',
        '\t(gr_text "21 sparse single-pixel sites; AFE placeholders; sync first" (at 102 142 0) (layer "F.SilkS") (uuid "' + uid("text:subtitle") + '") (effects (font (size 0.95 0.95) (thickness 0.13))))',
        '\t(gr_text "Detector island" (at 91 68 0) (layer "F.SilkS") (uuid "' + uid("text:detector") + '") (effects (font (size 0.9 0.9) (thickness 0.12))))',
        '\t(gr_text "AFE placeholders" (at 129 63 0) (layer "F.SilkS") (uuid "' + uid("text:afe") + '") (effects (font (size 0.8 0.8) (thickness 0.11))))',
    ]

    return f"""(kicad_pcb
\t(version 20240108)
\t(generator "hybridimager-v1-generator")
\t(generator_version "1.0")
\t(general
\t\t(thickness 1.6)
\t\t(legacy_teardrops no)
\t)
\t(paper "A4")
\t(title_block
\t\t(title "HybridImager V1 Weiqi Sparse Sensor Board")
\t\t(date "2026-06-08")
\t\t(rev "0.1.0-draft")
\t\t(company "LazyingArt LLC / HybridImager")
\t)
\t(layers
\t\t(0 "F.Cu" signal)
\t\t(31 "B.Cu" signal)
\t\t(32 "B.Adhes" user "B.Adhesive")
\t\t(33 "F.Adhes" user "F.Adhesive")
\t\t(34 "B.Paste" user)
\t\t(35 "F.Paste" user)
\t\t(36 "B.SilkS" user "B.Silkscreen")
\t\t(37 "F.SilkS" user "F.Silkscreen")
\t\t(38 "B.Mask" user)
\t\t(39 "F.Mask" user)
\t\t(40 "Dwgs.User" user "User.Drawings")
\t\t(41 "Cmts.User" user "User.Comments")
\t\t(42 "Eco1.User" user "User.Eco1")
\t\t(43 "Eco2.User" user "User.Eco2")
\t\t(44 "Edge.Cuts" user)
\t\t(45 "Margin" user)
\t\t(46 "B.CrtYd" user "B.Courtyard")
\t\t(47 "F.CrtYd" user "F.Courtyard")
\t\t(48 "B.Fab" user)
\t\t(49 "F.Fab" user)
\t\t(50 "User.1" user)
\t\t(51 "User.2" user)
\t\t(52 "User.3" user)
\t\t(53 "User.4" user)
\t\t(54 "User.5" user)
\t\t(55 "User.6" user)
\t\t(56 "User.7" user)
\t\t(57 "User.8" user)
\t\t(58 "User.9" user)
\t)
\t(setup
\t\t(pad_to_mask_clearance 0.05)
\t\t(allow_soldermask_bridges_in_footprints no)
\t\t(pcbplotparams
\t\t\t(layerselection 0x00010fc_ffffffff)
\t\t\t(usegerberextensions no)
\t\t\t(usegerberattributes yes)
\t\t\t(usegerberadvancedattributes yes)
\t\t\t(creategerberjobfile yes)
\t\t\t(outputformat 1)
\t\t\t(outputdirectory "gerber/")
\t\t)
\t)
{chr(10).join(nets)}
{chr(10).join(footprints)}
{chr(10).join(drawings)}
{chr(10).join(segments)}
{zone("B.Cu")}
)"""


def schematic_text() -> str:
    return f"""(kicad_sch
\t(version 20231120)
\t(generator "hybridimager-v1-generator")
\t(generator_version "1.0")
\t(uuid "{uid("schematic")}")
\t(paper "A4")
\t(title_block
\t\t(title "HybridImager V1 Weiqi Sparse Sensor Board")
\t\t(date "2026-06-08")
\t\t(rev "0.1.0-draft")
\t)
\t(lib_symbols)
\t(text "Board-first schematic stub. V1 validates sparse single-pixel placement, sync connectors, and AFE/mezzanine mechanical space before detailed analog design." (at 30 40 0)
\t\t(effects (font (size 1.27 1.27)) (justify left bottom))
\t\t(uuid "{uid("sch:text")}")
\t)
\t(sheet_instances (path "/" (page "1")))
)"""


def project_text() -> str:
    return json.dumps(
        {
            "meta": {"filename": PROJECT.name, "version": 1},
            "board": {
                "design_settings": {
                    "rule_severities": {
                        "lib_footprint_mismatch": "ignore",
                        "lib_footprint_issues": "ignore",
                        "missing_courtyard": "ignore",
                        "silk_over_copper": "ignore",
                    }
                }
            },
        },
        indent=2,
    ) + "\n"


def dataset() -> dict:
    return {
        "board": BOARD_NAME,
        "version": "0.1.0-draft",
        "date": "2026-06-08",
        "scope": "First HybridImager sensor-board draft for optical bench experiments, not fabrication-approved.",
        "single_pixel_policy": "Sparse multi-site bucket detector array, not one central detector only.",
        "detector_array": {
            "count": 21,
            "grid": "7x7 conceptual Weiqi grid with 21 populated detector sites",
            "pitch_mm": 8.5,
            "footprint": "3 mm THT photodiode-class placeholder with adjacent signal testpad",
            "recommended_first_detector_options": [
                "low-capacitance silicon photodiode in 3 mm / TO-style package for bright optical bench tests",
                "large-area low-noise photodiode module for bucket/spectral experiments after layout validation",
                "SiPM/APD adapter as a later shielded daughterboard, not direct V1 default",
            ],
        },
        "architecture": [
            "Sparse single-pixel detector island on the front side.",
            "Per-site signal testpads for direct TIA/comparator probing.",
            "AFE placeholders for TIA gain banks.",
            "QFN timing placeholder for MCU/FPGA timestamp authority.",
            "2x20 expansion header for future analog/event tile mezzanine.",
            "1x10 power/sync header and two SMA sync connectors.",
        ],
        "validation_intent": [
            "Confirm optical spacing and sparse reconstruction geometry.",
            "Measure dark current/noise per site with external TIA fixtures.",
            "Validate timestamp and trigger wiring before dense custom electronics.",
            "Use this board as mechanical/electrical skeleton for the next detailed analog schematic.",
        ],
        "known_limits": [
            "Board-first schematic stub; detailed TIA/comparator values are not finalized.",
            "Photodiode package is a render/placement placeholder, not a locked BOM part.",
            "Expansion header pads are mechanical/electrical placeholders and not routed to all detector sites in this draft.",
            "Human review is required before fabrication.",
        ],
        "references": [
            {"name": "HybridImager board architecture", "path": "hardware/board_architecture.md"},
            {"name": "PCB and circuits notes", "path": "references/pcb_and_circuits.md"},
            {"name": "Open camera project survey", "path": "references/open_camera_project_survey.md"},
        ],
    }


def write_bom() -> None:
    rows = [
        ["Id", "Designator", "Quantity", "Footprint", "Designation", "Status"],
        ["1", "PD01-PD21", "21", "Sparse_SP_D3_Photodiode", "3 mm photodiode-class sparse single-pixel detector", "placeholder"],
        ["2", "TP01-TP21", "21", "TP_1.7mm_SMD", "Per-site detector signal probe pad", "draft"],
        ["3", "U1-U3", "3", "SOIC-8", "TIA / comparator AFE placeholder", "not valued"],
        ["4", "U4", "1", "QFN-48", "MCU/FPGA timestamp placeholder", "not valued"],
        ["5", "J1", "1", "PinHeader_2x20_P2.54mm", "AFE/event expansion header", "draft"],
        ["6", "J2", "1", "PinHeader_1x10_P2.54mm", "Power and sync header", "draft"],
        ["7", "J3,J4", "2", "Vertical SMA", "Sync in/out coax connectors", "draft"],
        ["8", "H1-H4", "4", "M3 NPTH", "Mounting holes", "draft"],
    ]
    with BOM.open("w", newline="", encoding="utf-8") as handle:
        csv.writer(handle, lineterminator="\n").writerows(rows)


def write_readme() -> None:
    README.write_text(
        f"""# HybridImager V1 Weiqi Sparse Sensor Board

![Full-view render](artifacts/hybridimager-v1-full-view-render.png)

![KiCad full board render](artifacts/hybridimager-v1-kicad-render-full.png)

This is the first board-level HybridImager sensor draft. It deliberately uses a
**sparse multi-site single-pixel detector array** instead of one central bucket
only. The geometry follows a Weiqi-like 7x7 conceptual grid with 21 populated
detector sites.

## Immediate Scope

- Validate detector spacing and sparse reconstruction geometry.
- Provide per-site signal pads for external TIA/comparator experiments.
- Reserve board area for three TIA banks, one timestamp MCU/FPGA, sync SMA
  connectors, power/sync header, and a 2x20 expansion header.
- Keep V1 buildable and inspectable before committing to dense custom sensor
  electronics or ASIC work.

## Files

- `{BOARD.name}`: generated KiCad board.
- `{PROJECT.name}`: KiCad project file.
- `{SCHEMATIC.name}`: board-first schematic stub.
- `{DATASET.name}`: source assumptions and design dataset.
- `{BOM.name}`: draft BOM.
- `artifacts/hybridimager-v1-full-view-render.png`: generated full-view 3D concept render.
- `artifacts/hybridimager-v1-kicad-render-full.png`: KiCad-native zoomed-out render.
- `artifacts/hybridimager-v1-kicad-render-close.png`: KiCad-native closer render.
- `artifacts/{BOARD_NAME}.step`: STEP export.
- `gerber/`: Gerber and drill outputs.

## Reproduce

```bash
python3 scripts/generate_v1_weiqi_sensor_board.py
kicad-cli pcb upgrade hardware/v1-weiqi-sensor/{BOARD.name}
kicad-cli pcb drc --format json --severity-all -o hardware/v1-weiqi-sensor/artifacts/drc.json hardware/v1-weiqi-sensor/{BOARD.name}
kicad-cli pcb export step --force --include-pads --include-tracks --include-silkscreen --include-soldermask -o hardware/v1-weiqi-sensor/artifacts/{BOARD_NAME}.step hardware/v1-weiqi-sensor/{BOARD.name}
kicad-cli pcb export gerbers --layers F.Cu,B.Cu,F.SilkS,B.SilkS,F.Mask,B.Mask,Edge.Cuts,F.Fab,B.Fab --precision 6 --check-zones -o hardware/v1-weiqi-sensor/gerber hardware/v1-weiqi-sensor/{BOARD.name}
kicad-cli pcb export drill --generate-map --map-format svg --generate-report --report-path hardware/v1-weiqi-sensor/artifacts/drill-report.txt -o hardware/v1-weiqi-sensor/gerber hardware/v1-weiqi-sensor/{BOARD.name}
xvfb-run -a kicad-cli pcb render --output hardware/v1-weiqi-sensor/artifacts/hybridimager-v1-kicad-render-full.png --width 1800 --height 1200 --background opaque --quality high --floor --perspective --rotate 315,0,35 --zoom 1.0 hardware/v1-weiqi-sensor/{BOARD.name}
```

## Engineering Status

Current generated validation: KiCad DRC reports 0 violations and 0 unconnected
items after running the commands above.

This is still an engineering draft. It is useful for visual review, mechanical
planning, sparse-detector geometry, and next-step analog partitioning. It still
needs a detailed schematic, selected photodiode parts, TIA gain/noise analysis,
layout review, and fabrication review before ordering boards.
""",
        encoding="utf-8",
    )


def box(ax, x1, y1, z1, x2, y2, z2, color, alpha=1.0):
    verts = [
        [(x1, y1, z1), (x2, y1, z1), (x2, y2, z1), (x1, y2, z1)],
        [(x1, y1, z2), (x2, y1, z2), (x2, y2, z2), (x1, y2, z2)],
        [(x1, y1, z1), (x2, y1, z1), (x2, y1, z2), (x1, y1, z2)],
        [(x2, y1, z1), (x2, y2, z1), (x2, y2, z2), (x2, y1, z2)],
        [(x2, y2, z1), (x1, y2, z1), (x1, y2, z2), (x2, y2, z2)],
        [(x1, y2, z1), (x1, y1, z1), (x1, y1, z2), (x1, y2, z2)],
    ]
    poly = Poly3DCollection(verts, facecolors=color, edgecolors="#111827", linewidths=0.35, alpha=alpha)
    ax.add_collection3d(poly)


def cylinder(ax, x, y, z, radius, height, color, alpha=1.0, segments=32):
    theta = np.linspace(0, 2 * np.pi, segments)
    xs = x + radius * np.cos(theta)
    ys = y + radius * np.sin(theta)
    top = list(zip(xs, ys, np.full_like(xs, z + height)))
    bottom = list(zip(xs, ys, np.full_like(xs, z)))
    sides = []
    for i in range(segments - 1):
        sides.append([bottom[i], bottom[i + 1], top[i + 1], top[i]])
    sides.append([bottom[-1], bottom[0], top[0], top[-1]])
    ax.add_collection3d(Poly3DCollection([top, bottom] + sides, facecolors=color, edgecolors="#0f172a", linewidths=0.25, alpha=alpha))


def write_preview() -> None:
    fig = plt.figure(figsize=(13, 9), dpi=160)
    ax = fig.add_subplot(111, projection="3d")
    ax.set_facecolor("#f8fafc")
    box(ax, 0, 0, 0, 105, 90, 1.6, "#155e52")
    box(ax, 12, 15, 1.65, 70, 75, 1.9, "#1f8a70", 0.55)
    pitch = 8.5
    cx, cy = 41, 45
    for idx, (gx, gy) in enumerate(detector_positions(), start=1):
        x = cx + gx * pitch
        y = cy + gy * pitch
        cylinder(ax, x, y, 1.8, 1.75, 3.2, "#111827", 0.95)
        cylinder(ax, x + 3.8, y - 1.27, 1.72, 0.95, 0.22, "#d4af37", 1.0)
    for y in [21, 45, 69]:
        box(ax, 76, y - 3.2, 1.7, 84, y + 3.2, 3.2, "#020617")
        for pin in range(8):
            px = 75.0 if pin < 4 else 85.0
            py = y - 1.9 + (pin % 4) * 1.27
            box(ax, px - 0.45, py - 0.16, 1.72, px + 0.45, py + 0.16, 1.9, "#c084fc")
    box(ax, 58, 78, 1.7, 68, 88, 3.0, "#0f172a")
    for x in [93, 95.54]:
        for row in range(20):
            cylinder(ax, x, 45 + (row - 9.5) * 2.0, 1.7, 0.45, 4.0, "#d6a55c", 1.0, 16)
    for x in [17, 33]:
        cylinder(ax, x, 82, 1.7, 4.0, 3.0, "#cbd5e1", 0.95)
        cylinder(ax, x, 82, 4.8, 1.25, 1.2, "#334155", 1.0)
    for x, y in [(7, 7), (98, 7), (98, 83), (7, 83)]:
        cylinder(ax, x, y, 1.7, 1.6, 0.25, "#e2e8f0", 1.0)
    ax.text(5, 5, 4.5, "HybridImager V1", color="#0f172a", fontsize=12, weight="bold")
    ax.text(13, 12, 3.5, "21 sparse single-pixel detector sites", color="#0f172a", fontsize=8)
    ax.set_xlim(-5, 110)
    ax.set_ylim(-5, 95)
    ax.set_zlim(0, 14)
    ax.view_init(elev=27, azim=-43)
    ax.set_axis_off()
    plt.tight_layout()
    fig.savefig(PREVIEW, bbox_inches="tight", pad_inches=0.05)
    plt.close(fig)


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)
    GERBER_DIR.mkdir(parents=True, exist_ok=True)
    BOARD.write_text(board_text(), encoding="utf-8")
    PROJECT.write_text(project_text(), encoding="utf-8")
    SCHEMATIC.write_text(schematic_text(), encoding="utf-8")
    FP_LIB_TABLE.write_text(
        """(fp_lib_table
\t(version 7)
\t(lib (name "MountingHole")(type "KiCad")(uri "/usr/share/kicad/footprints/MountingHole.pretty")(options "")(descr "KiCad mounting holes"))
\t(lib (name "Connector_PinHeader_2.54mm")(type "KiCad")(uri "/usr/share/kicad/footprints/Connector_PinHeader_2.54mm.pretty")(options "")(descr "KiCad 2.54 mm pin headers"))
\t(lib (name "Package_SO")(type "KiCad")(uri "/usr/share/kicad/footprints/Package_SO.pretty")(options "")(descr "KiCad SO packages"))
\t(lib (name "Package_DFN_QFN")(type "KiCad")(uri "/usr/share/kicad/footprints/Package_DFN_QFN.pretty")(options "")(descr "KiCad DFN/QFN packages"))
\t(lib (name "Connector_Coaxial")(type "KiCad")(uri "/usr/share/kicad/footprints/Connector_Coaxial.pretty")(options "")(descr "KiCad coaxial connectors"))
)
""",
        encoding="utf-8",
    )
    LOCAL_GITIGNORE.write_text("*.kicad_prl\n*.kicad_prl.*\nfp-info-cache\n", encoding="utf-8")
    DATASET.write_text(json.dumps(dataset(), indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    write_bom()
    write_readme()
    write_preview()
    shutil.copy2(Path(__file__), OUT_DIR / "generate_v1_weiqi_sensor_board.py")
    print(f"Wrote {OUT_DIR.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
