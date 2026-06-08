#!/usr/bin/env python3
"""Generate the HybridImager V2 aligned 32x32 ALS-PT19 sensor-board draft."""

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
OUT_DIR = ROOT / "hardware/v2-als-pt19-32x32"
ARTIFACT_DIR = OUT_DIR / "artifacts"
GERBER_DIR = OUT_DIR / "gerber"
BOARD_NAME = "hybridimager-v2-als-pt19-32x32"
BOARD = OUT_DIR / f"{BOARD_NAME}.kicad_pcb"
PROJECT = OUT_DIR / f"{BOARD_NAME}.kicad_pro"
SCHEMATIC = OUT_DIR / f"{BOARD_NAME}.kicad_sch"
FP_LIB_TABLE = OUT_DIR / "fp-lib-table"
DATASET = OUT_DIR / "hybridimager-v2-source-dataset.json"
BOM = OUT_DIR / "hybridimager-v2-bom.csv"
README = OUT_DIR / "README.md"
LOCAL_GITIGNORE = OUT_DIR / ".gitignore"
PREVIEW = ARTIFACT_DIR / "hybridimager-v2-full-view-render.png"

GRID = 32
PITCH = 2.54
X0 = 55.0
Y0 = 48.0
PAD_ROW_DX = -0.75
PAD_COL_DX = 0.75
ROW_BUS_DY = -0.72
COL_VIA_DY = 0.72
ROW_HEADER_X = 28.0
COL_HEADER_Y = 29.0
BOARD_MIN_X = 18.0
BOARD_MIN_Y = 18.0
BOARD_MAX_X = 174.0
BOARD_MAX_Y = 146.0


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


def track(name: str, layer: str, x1: float, y1: float, x2: float, y2: float, net_id: int, width: float = 0.2) -> str:
    return f'\t(segment (start {x1:g} {y1:g}) (end {x2:g} {y2:g}) (width {width:g}) (layer "{layer}") (net {net_id}) (uuid "{uid(name)}"))'


def via(name: str, x: float, y: float, net_id: int) -> str:
    return f'\t(via (at {x:g} {y:g}) (size 0.6) (drill 0.3) (layers "F.Cu" "B.Cu") (net {net_id}) (uuid "{uid(name)}"))'


def row_net(row: int) -> tuple[int, str]:
    return 10 + row, f"ROW{row + 1:02d}"


def col_net(col: int) -> tuple[int, str]:
    return 50 + col, f"COL{col + 1:02d}"


def grid_xy(col: int, row: int) -> tuple[float, float]:
    return X0 + col * PITCH, Y0 + row * PITCH


def als_pt19(ref: str, x: float, y: float, row_id: int, row_name: str, col_id: int, col_name: str) -> str:
    return f"""
\t(footprint "ALS-PT19"
\t\t(layer "F.Cu")
\t\t(uuid "{uid(ref)}")
\t\t(at {x:g} {y:g})
\t\t(descr "ALS-PT19 phototransistor footprint copied from CustomSensor/digiOBSCURA geometry")
\t\t(tags "ALS-PT19 phototransistor 32x32 aligned")
{prop("Reference", ref, "0 1.35 0", "F.Fab", True)}
{prop("Value", "ALS-PT19", "0 -1.35 0", "F.Fab", True)}
\t\t(attr smd)
\t\t(fp_rect (start -1.2 -0.4) (end 1.2 0.4) (stroke (width 0.06) (type solid)) (fill none) (layer "F.Fab") (uuid "{uid(ref + ':fab')}"))
\t\t(fp_line (start 0.3 -0.4) (end 0.3 0.4) (stroke (width 0.05) (type solid)) (layer "F.Fab") (uuid "{uid(ref + ':mark')}"))
\t\t(pad "1" smd rect (at -0.75 0) (size 0.8 0.8) (layers "F.Cu" "F.Paste" "F.Mask") (net {row_id} "{row_name}") (pinfunction "ROW") (pintype "passive") (uuid "{uid(ref + ':row')}"))
\t\t(pad "2" smd rect (at 0.75 0) (size 0.8 0.8) (layers "F.Cu" "F.Paste" "F.Mask") (net {col_id} "{col_name}") (pinfunction "COL") (pintype "passive") (uuid "{uid(ref + ':col')}"))
\t)"""


def aligned_row_header() -> str:
    pads = []
    for row in range(GRID):
        net_id, net_name = row_net(row)
        _, y = grid_xy(0, row)
        pads.append(
            f'\t\t(pad "{row + 1}" thru_hole oval (at {ROW_HEADER_X:g} {y:g}) (size 1.55 1.15) (drill 0.7) (layers "*.Cu" "*.Mask") (net {net_id} "{net_name}") (pinfunction "{net_name}") (pintype "passive") (uuid "{uid(f"JROW:pad{row + 1}")}"))'
        )
    return f"""
\t(footprint "Aligned_Row_Header_1x32_2.54mm"
\t\t(layer "F.Cu")
\t\t(uuid "{uid('JROW')}")
\t\t(at 0 0)
{prop("Reference", "JROW", f"{ROW_HEADER_X:g} {Y0 - 5:g} 0", "F.SilkS")}
{prop("Value", "ROW_EDGE_1x32_ALIGNED", f"{ROW_HEADER_X:g} {Y0 + GRID * PITCH + 2:g} 0", "F.Fab", True)}
\t\t(attr through_hole)
{chr(10).join(pads)}
\t)"""


def aligned_col_header() -> str:
    pads = []
    for col in range(GRID):
        net_id, net_name = col_net(col)
        x, _ = grid_xy(col, 0)
        x += PAD_COL_DX
        pads.append(
            f'\t\t(pad "{col + 1}" thru_hole oval (at {x:g} {COL_HEADER_Y:g} 90) (size 1.55 1.15) (drill 0.7) (layers "*.Cu" "*.Mask") (net {net_id} "{net_name}") (pinfunction "{net_name}") (pintype "passive") (uuid "{uid(f"JCOL:pad{col + 1}")}"))'
        )
    return f"""
\t(footprint "Aligned_Col_Header_1x32_2.54mm"
\t\t(layer "F.Cu")
\t\t(uuid "{uid('JCOL')}")
\t\t(at 0 0)
{prop("Reference", "JCOL", f"{X0 + 34:g} {COL_HEADER_Y - 4:g} 0", "F.SilkS")}
{prop("Value", "COL_EDGE_1x32_ALIGNED", f"{X0 + 34:g} {COL_HEADER_Y + 4:g} 0", "F.Fab", True)}
\t\t(attr through_hole)
{chr(10).join(pads)}
\t)"""


def control_header() -> str:
    names = ["A0", "A1", "A2", "A3", "A4", "ROW_CS", "COL_CS", "WR", "EN", "OUTROW", "OUTCOL", "+3V3", "GND"]
    net_lookup = {name: 90 + idx for idx, name in enumerate(names)}
    net_lookup["+3V3"] = 2
    net_lookup["GND"] = 1
    pads = []
    x = 161.5
    y0 = 55.0
    for idx, name in enumerate(names):
        y = y0 + idx * 3.0
        shape = "rect" if idx == 0 else "oval"
        pads.append(
            f'\t\t(pad "{idx + 1}" thru_hole {shape} (at {x:g} {y:g}) (size 1.6 1.2) (drill 0.75) (layers "*.Cu" "*.Mask") (net {net_lookup[name]} "{name}") (pinfunction "{name}") (pintype "passive") (uuid "{uid(f"JCTL:pad{idx + 1}")}"))'
        )
    return f"""
\t(footprint "Control_Header_1x13_3mm"
\t\t(layer "F.Cu")
\t\t(uuid "{uid('JCTL')}")
\t\t(at 0 0)
{prop("Reference", "JCTL", f"{x:g} {y0 - 5:g} 0", "F.SilkS")}
{prop("Value", "ADDR_SYNC_PWR", f"{x:g} {y0 + len(names) * 3:g} 0", "F.Fab", True)}
\t\t(attr through_hole)
{chr(10).join(pads)}
\t)"""


def adg732_placeholder(ref: str, x: float, y: float) -> str:
    pads = []
    for idx in range(12):
        p = idx + 1
        offset = -2.75 + idx * 0.5
        pads.append(f'\t\t(pad "{p}" smd roundrect (at {offset:g} -3.85) (size 0.28 1.0) (layers "F.Cu" "F.Paste" "F.Mask") (roundrect_rratio 0.2) (uuid "{uid(ref + f":pad{p}")}"))')
        pads.append(f'\t\t(pad "{p + 12}" smd roundrect (at 3.85 {offset:g}) (size 1.0 0.28) (layers "F.Cu" "F.Paste" "F.Mask") (roundrect_rratio 0.2) (uuid "{uid(ref + f":pad{p + 12}")}"))')
        pads.append(f'\t\t(pad "{p + 24}" smd roundrect (at {-offset:g} 3.85) (size 0.28 1.0) (layers "F.Cu" "F.Paste" "F.Mask") (roundrect_rratio 0.2) (uuid "{uid(ref + f":pad{p + 24}")}"))')
        pads.append(f'\t\t(pad "{p + 36}" smd roundrect (at -3.85 {-offset:g}) (size 1.0 0.28) (layers "F.Cu" "F.Paste" "F.Mask") (roundrect_rratio 0.2) (uuid "{uid(ref + f":pad{p + 36}")}"))')
    return f"""
\t(footprint "ADG732_TQFP48_PLACEHOLDER"
\t\t(layer "F.Cu")
\t\t(uuid "{uid(ref)}")
\t\t(at {x:g} {y:g})
{prop("Reference", ref, "0 -5.4 0", "F.SilkS")}
{prop("Value", "ADG732_32_TO_1_PLACEHOLDER", "0 5.4 0", "F.Fab", True)}
\t\t(attr smd)
\t\t(fp_rect (start -3.7 -3.7) (end 3.7 3.7) (stroke (width 0.12) (type solid)) (fill none) (layer "F.SilkS") (uuid "{uid(ref + ':rect')}"))
{chr(10).join(pads)}
\t)"""


def mounting_hole(ref: str, x: float, y: float) -> str:
    return f"""
\t(footprint "MountingHole_3.2mm_M3"
\t\t(layer "F.Cu")
\t\t(uuid "{uid(ref)}")
\t\t(at {x:g} {y:g})
{prop("Reference", ref, "0 -4 0", "F.Fab", True)}
{prop("Value", "M3", "0 4 0", "F.Fab", True)}
\t\t(attr exclude_from_pos_files)
\t\t(fp_circle (center 0 0) (end 3.2 0) (stroke (width 0.15) (type solid)) (fill none) (layer "Cmts.User") (uuid "{uid(ref + ':circle')}"))
\t\t(pad "" np_thru_hole circle (at 0 0) (size 3.2 3.2) (drill 3.2) (layers "*.Cu" "*.Mask") (uuid "{uid(ref + ':pad')}"))
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
\t\t\t\t(xy {BOARD_MIN_X:g} {BOARD_MIN_Y:g}) (xy {BOARD_MAX_X:g} {BOARD_MIN_Y:g}) (xy {BOARD_MAX_X:g} {BOARD_MAX_Y:g}) (xy {BOARD_MIN_X:g} {BOARD_MAX_Y:g})
\t\t\t)
\t\t)
\t)"""


def board_text() -> str:
    nets = ['\t(net 0 "")', '\t(net 1 "GND")', '\t(net 2 "+3V3")']
    for row in range(GRID):
        net_id, net_name = row_net(row)
        nets.append(f'\t(net {net_id} "{net_name}")')
    for col in range(GRID):
        net_id, net_name = col_net(col)
        nets.append(f'\t(net {net_id} "{net_name}")')
    for idx, name in enumerate(["A0", "A1", "A2", "A3", "A4", "ROW_CS", "COL_CS", "WR", "EN", "OUTROW", "OUTCOL"]):
        nets.append(f'\t(net {90 + idx} "{name}")')

    footprints = [
        mounting_hole("H1", 25, 25),
        mounting_hole("H2", 167, 25),
        mounting_hole("H3", 167, 139),
        mounting_hole("H4", 25, 139),
        aligned_row_header(),
        aligned_col_header(),
        control_header(),
        adg732_placeholder("UROW", 150, 76),
        adg732_placeholder("UCOL", 150, 108),
    ]
    segments: list[str] = []
    vias: list[str] = []

    for row in range(GRID):
        row_id, row_name = row_net(row)
        _, y = grid_xy(0, row)
        row_bus_y = y + ROW_BUS_DY
        bus_start_x = 31.0
        bus_end_x = X0 + (GRID - 1) * PITCH + PAD_ROW_DX
        segments.append(track(f"row:{row}:header", "F.Cu", ROW_HEADER_X, y, bus_start_x, row_bus_y, row_id, 0.2))
        segments.append(track(f"row:{row}:bus", "F.Cu", bus_start_x, row_bus_y, bus_end_x, row_bus_y, row_id, 0.2))
        for col in range(GRID):
            col_id, col_name = col_net(col)
            x, y = grid_xy(col, row)
            ref = f"Q{row + 1:02d}{col + 1:02d}"
            footprints.append(als_pt19(ref, x, y, row_id, row_name, col_id, col_name))
            pad1_x = x + PAD_ROW_DX
            pad2_x = x + PAD_COL_DX
            via_y = y + COL_VIA_DY
            segments.append(track(f"row:{row}:stub:{col}", "F.Cu", pad1_x, y, pad1_x, row_bus_y, row_id, 0.2))
            segments.append(track(f"col:{col}:stub:{row}", "F.Cu", pad2_x, y, pad2_x, via_y, col_id, 0.2))
            vias.append(via(f"col:{col}:via:{row}", pad2_x, via_y, col_id))

    for col in range(GRID):
        col_id, _ = col_net(col)
        x, _ = grid_xy(col, 0)
        col_x = x + PAD_COL_DX
        last_y = Y0 + (GRID - 1) * PITCH + COL_VIA_DY
        segments.append(track(f"col:{col}:bus", "B.Cu", col_x, COL_HEADER_Y, col_x, last_y, col_id, 0.2))

    drawings = [
        gr_rect("Edge.Cuts", BOARD_MIN_X, BOARD_MIN_Y, BOARD_MAX_X, BOARD_MAX_Y, "edge", 0.15),
        gr_rect("F.SilkS", X0 - 2.0, Y0 - 2.0, X0 + (GRID - 1) * PITCH + 2.0, Y0 + (GRID - 1) * PITCH + 2.0, "active-array", 0.18),
        '\t(gr_text "HybridImager V2 ALS-PT19 32x32 aligned matrix" (at 91 22.5 0) (layer "F.SilkS") (uuid "' + uid("text:title") + '") (effects (font (size 1.35 1.35) (thickness 0.18))))',
        '\t(gr_text "Rows: aligned left header / Columns: aligned top header / pitch 2.54 mm" (at 94 142 0) (layer "F.SilkS") (uuid "' + uid("text:subtitle") + '") (effects (font (size 0.95 0.95) (thickness 0.13))))',
        '\t(gr_text "UROW ADG732" (at 150 67 0) (layer "F.SilkS") (uuid "' + uid("text:urow") + '") (effects (font (size 0.85 0.85) (thickness 0.11))))',
        '\t(gr_text "UCOL ADG732" (at 150 99 0) (layer "F.SilkS") (uuid "' + uid("text:ucol") + '") (effects (font (size 0.85 0.85) (thickness 0.11))))',
    ]

    return f"""(kicad_pcb
\t(version 20240108)
\t(generator "hybridimager-v2-generator")
\t(generator_version "1.0")
\t(general
\t\t(thickness 1.6)
\t\t(legacy_teardrops no)
\t)
\t(paper "A4")
\t(title_block
\t\t(title "HybridImager V2 ALS-PT19 32x32 Aligned Sensor Board")
\t\t(date "2026-06-08")
\t\t(rev "0.2.0-draft")
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
{chr(10).join(vias)}
{zone("B.Cu")}
)"""


def schematic_text() -> str:
    return f"""(kicad_sch
\t(version 20231120)
\t(generator "hybridimager-v2-generator")
\t(generator_version "1.0")
\t(uuid "{uid("schematic")}")
\t(paper "A4")
\t(title_block
\t\t(title "HybridImager V2 ALS-PT19 32x32 Aligned Sensor Board")
\t\t(date "2026-06-08")
\t\t(rev "0.2.0-draft")
\t)
\t(lib_symbols)
\t(text "Board-first schematic stub. V2 uses the CustomSensor/digiOBSCURA ALS-PT19 32x32 matrix idea, but aligns all pads and headers on a 2.54 mm grid for cleaner routing and probing." (at 30 40 0)
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
        "version": "0.2.0-draft",
        "date": "2026-06-08",
        "scope": "Dense 32x32 aligned sensor-matrix draft using the same CustomSensor/digiOBSCURA ALS-PT19 phototransistor choice.",
        "custom_sensor_reference": {
            "repo": "/home/lachlan/ProjectsLFS/CustomSensor",
            "board": "PCB/image_sensor/digiobscura.kicad_pcb",
            "footprint": "PCB/image_sensor/project_libs/project_footprints.pretty/ALS-PT19.kicad_mod",
            "documented_part": "1024 x ALS-PT19 phototransistors",
            "original_pitch_mm": 2.0,
            "original_rotation_deg": 45,
        },
        "v2_changes": [
            "Use unrotated ALS-PT19 footprints so pad 1 and pad 2 are visually and electrically aligned.",
            "Increase pitch to 2.54 mm to prevent adjacent pad overlap and provide routable clearance.",
            "Route ROW nets as horizontal F.Cu buses and COL nets as vertical B.Cu buses through per-pixel vias.",
            "Align ROW header pads directly with matrix rows and COL header pads directly with matrix columns.",
            "Keep ADG732 row/column mux placeholders for the CustomSensor addressing model.",
        ],
        "detector_array": {
            "part": "ALS-PT19 phototransistor",
            "count": GRID * GRID,
            "grid": "32x32",
            "pitch_mm": PITCH,
            "populated_area_mm": round((GRID - 1) * PITCH, 3),
            "row_header": "1x32 aligned through-hole pads on the left edge",
            "col_header": "1x32 aligned through-hole pads on the top edge",
        },
        "known_limits": [
            "Board-first schematic stub; ADG732 mux connections are placeholders, not final schematic capture.",
            "ALS-PT19 geometry is sourced from the local CustomSensor footprint, not a freshly verified vendor land-pattern.",
            "Human review is required before fabrication, especially crosstalk, optical baffling, solderability, and mux loading.",
        ],
    }


def write_bom() -> None:
    rows = [
        ["Id", "Designator", "Quantity", "Footprint", "Designation", "Status"],
        ["1", "Q0101-Q3232", "1024", "ALS-PT19", "ALS-PT19 phototransistor", "CustomSensor reference"],
        ["2", "JROW", "1", "Aligned_Row_Header_1x32_2.54mm", "Row edge header aligned to sensor rows", "draft"],
        ["3", "JCOL", "1", "Aligned_Col_Header_1x32_2.54mm", "Column edge header aligned to sensor columns", "draft"],
        ["4", "JCTL", "1", "Control_Header_1x13_3mm", "Address, mux, power, and analog I/O header", "draft"],
        ["5", "UROW,UCOL", "2", "ADG732_TQFP48_PLACEHOLDER", "32:1 row/column analog mux placeholder", "not routed"],
        ["6", "H1-H4", "4", "M3 NPTH", "Mounting holes", "draft"],
    ]
    with BOM.open("w", newline="", encoding="utf-8") as handle:
        csv.writer(handle, lineterminator="\n").writerows(rows)


def write_readme() -> None:
    README.write_text(
        f"""# HybridImager V2 ALS-PT19 32x32 Aligned Sensor Board

![Full-view concept render](artifacts/hybridimager-v2-full-view-render.png)

![KiCad full board render](artifacts/hybridimager-v2-kicad-render-full.png)

V2 moves from the sparse V1 detector carrier to a dense `32x32` matrix using
the same `ALS-PT19` phototransistor family documented in `CustomSensor`.

## What Changed From V1

- `1024` ALS-PT19 detector sites instead of 21 sparse sites.
- Unrotated footprints on a `2.54 mm` pitch so pins are aligned and pads do not overlap.
- Row pins align to the left edge header; column pins align to the top edge header.
- Row nets route horizontally on `F.Cu`; column nets route vertically on `B.Cu`.
- ADG732 row/column mux footprints remain as placement placeholders for the CustomSensor addressing model.

## Files

- `{BOARD.name}`: generated KiCad board.
- `{PROJECT.name}`: KiCad project file.
- `{SCHEMATIC.name}`: board-first schematic stub.
- `{DATASET.name}`: source assumptions and CustomSensor reference dataset.
- `{BOM.name}`: draft BOM.
- `artifacts/hybridimager-v2-full-view-render.png`: generated full-view 3D concept render.
- `artifacts/hybridimager-v2-kicad-render-full.png`: KiCad-native zoomed-out render.
- `artifacts/hybridimager-v2-kicad-render-close.png`: KiCad-native closer render.
- `artifacts/{BOARD_NAME}.step`: lightweight board-level STEP export.
- `gerber/`: Gerber and drill outputs.

## Reproduce

```bash
python3 scripts/generate_v2_als_pt19_32x32_board.py
kicad-cli pcb upgrade hardware/v2-als-pt19-32x32/{BOARD.name}
kicad-cli pcb drc --format json --severity-all -o hardware/v2-als-pt19-32x32/artifacts/drc.json hardware/v2-als-pt19-32x32/{BOARD.name}
kicad-cli pcb export step --force -o hardware/v2-als-pt19-32x32/artifacts/{BOARD_NAME}.step hardware/v2-als-pt19-32x32/{BOARD.name}
kicad-cli pcb export gerbers --layers F.Cu,B.Cu,F.SilkS,B.SilkS,F.Mask,B.Mask,Edge.Cuts,F.Fab,B.Fab --precision 6 --check-zones -o hardware/v2-als-pt19-32x32/gerber hardware/v2-als-pt19-32x32/{BOARD.name}
kicad-cli pcb export drill --generate-map --map-format svg --generate-report --report-path hardware/v2-als-pt19-32x32/artifacts/drill-report.txt -o hardware/v2-als-pt19-32x32/gerber hardware/v2-als-pt19-32x32/{BOARD.name}
xvfb-run -a kicad-cli pcb render --output hardware/v2-als-pt19-32x32/artifacts/hybridimager-v2-kicad-render-full.png --width 1800 --height 1200 --background opaque --quality high --floor --perspective --rotate 315,0,35 --zoom 0.95 hardware/v2-als-pt19-32x32/{BOARD.name}
```

## Engineering Status

Current generated validation: KiCad DRC reports 0 violations and 0 unconnected
items. Full-detail STEP with pad/track solidification is intentionally avoided
for this dense 1024-sensor matrix because it is much slower; use Gerbers for
electrical manufacturing geometry and the lightweight STEP for mechanical board
outline review.

This is a dense matrix layout draft, not a fabrication-approved design. It
still needs final ADG732 schematic wiring, optical masking/baffling decisions,
row/column crosstalk review, solderability review, and firmware pin mapping.
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
    ax.add_collection3d(Poly3DCollection(verts, facecolors=color, edgecolors="#0f172a", linewidths=0.15, alpha=alpha))


def cylinder(ax, x, y, z, radius, height, color, alpha=1.0, segments=18):
    theta = np.linspace(0, 2 * math.pi, segments)
    xs = x + radius * np.cos(theta)
    ys = y + radius * np.sin(theta)
    top = list(zip(xs, ys, np.full_like(xs, z + height)))
    bottom = list(zip(xs, ys, np.full_like(xs, z)))
    sides = [[bottom[i], bottom[(i + 1) % segments], top[(i + 1) % segments], top[i]] for i in range(segments)]
    ax.add_collection3d(Poly3DCollection([top, bottom] + sides, facecolors=color, edgecolors="#111827", linewidths=0.1, alpha=alpha))


def write_preview() -> None:
    fig = plt.figure(figsize=(13, 9), dpi=160)
    ax = fig.add_subplot(111, projection="3d")
    ax.set_facecolor("#f8fafc")
    box(ax, 0, 0, 0, BOARD_MAX_X - BOARD_MIN_X, BOARD_MAX_Y - BOARD_MIN_Y, 1.6, "#155e52")
    ox = X0 - BOARD_MIN_X
    oy = Y0 - BOARD_MIN_Y
    for row in range(GRID):
        for col in range(GRID):
            x = ox + col * PITCH
            y = oy + row * PITCH
            box(ax, x - 1.0, y - 0.35, 1.65, x + 1.0, y + 0.35, 2.2, "#111827")
            box(ax, x - 0.95, y - 0.62, 1.62, x - 0.55, y - 0.42, 1.72, "#d4af37")
            box(ax, x + 0.55, y + 0.42, 1.62, x + 0.95, y + 0.62, 1.72, "#d4af37")
    for row in range(GRID):
        y = oy + row * PITCH
        cylinder(ax, ROW_HEADER_X - BOARD_MIN_X, y, 1.7, 0.42, 1.0, "#eab308")
    for col in range(GRID):
        x = ox + col * PITCH + PAD_COL_DX
        cylinder(ax, x, COL_HEADER_Y - BOARD_MIN_Y, 1.7, 0.42, 1.0, "#eab308")
    box(ax, 126, 54, 1.7, 134, 62, 3.0, "#020617")
    box(ax, 126, 86, 1.7, 134, 94, 3.0, "#020617")
    ax.text(10, 8, 5.0, "HybridImager V2", color="#0f172a", fontsize=13, weight="bold")
    ax.text(10, 13, 4.2, "32x32 ALS-PT19 aligned matrix", color="#0f172a", fontsize=8)
    ax.set_xlim(-5, BOARD_MAX_X - BOARD_MIN_X + 5)
    ax.set_ylim(-5, BOARD_MAX_Y - BOARD_MIN_Y + 5)
    ax.set_zlim(0, 12)
    ax.view_init(elev=30, azim=-47)
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
    FP_LIB_TABLE.write_text('(fp_lib_table\n\t(version 7)\n)\n', encoding="utf-8")
    LOCAL_GITIGNORE.write_text("*.kicad_prl\n*.kicad_prl.*\nfp-info-cache\n", encoding="utf-8")
    DATASET.write_text(json.dumps(dataset(), indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    write_bom()
    write_readme()
    write_preview()
    shutil.copy2(Path(__file__), OUT_DIR / "generate_v2_als_pt19_32x32_board.py")
    print(f"Wrote {OUT_DIR.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
