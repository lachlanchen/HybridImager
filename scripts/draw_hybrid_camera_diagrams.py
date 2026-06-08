#!/usr/bin/env python3
"""Generate deterministic HybridCamera concept diagrams as SVG files."""

from pathlib import Path
import subprocess


ROOT = Path(__file__).resolve().parents[1]
FIGURES = ROOT / "figures"


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def svg_header(width: int, height: int) -> str:
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}">\n'
        "<defs>\n"
        '<filter id="softShadow" x="-20%" y="-20%" width="140%" height="140%">'
        '<feDropShadow dx="0" dy="8" stdDeviation="8" flood-color="#0f172a" flood-opacity="0.18"/>'
        "</filter>\n"
        "</defs>\n"
        '<rect width="100%" height="100%" fill="#f8fafc"/>\n'
    )


def svg_footer() -> str:
    return "</svg>\n"


def board_layout() -> str:
    w, h = 1200, 820
    parts = [svg_header(w, h)]
    parts.append('<text x="60" y="70" font-family="Arial" font-size="34" font-weight="700" fill="#111827">HybridCamera Weiqi-Board Sensor Concept</text>\n')
    parts.append('<text x="60" y="108" font-family="Arial" font-size="18" fill="#475569">Central high dynamic range bucket detector with alternating event and frame tiles</text>\n')
    bx, by, size = 100, 150, 600
    cell = size / 9
    parts.append(f'<rect x="{bx-24}" y="{by-24}" width="{size+48}" height="{size+48}" rx="26" fill="#ffffff" stroke="#cbd5e1" stroke-width="2" filter="url(#softShadow)"/>\n')
    for r in range(9):
        for c in range(9):
            x = bx + c * cell
            y = by + r * cell
            if r == 4 and c == 4:
                fill = "#fef3c7"
                label = "SP"
                stroke = "#d97706"
            elif (r + c) % 2 == 0:
                fill = "#dbeafe"
                label = "EV"
                stroke = "#2563eb"
            else:
                fill = "#dcfce7"
                label = "FR"
                stroke = "#16a34a"
            parts.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{cell:.1f}" height="{cell:.1f}" fill="{fill}" stroke="#111827" stroke-width="1.2"/>\n')
            if r == 4 and c == 4:
                parts.append(f'<circle cx="{x+cell/2:.1f}" cy="{y+cell/2:.1f}" r="{cell*0.33:.1f}" fill="#fde68a" stroke="{stroke}" stroke-width="4"/>\n')
                parts.append(f'<text x="{x+cell/2:.1f}" y="{y+cell/2+8:.1f}" text-anchor="middle" font-family="Arial" font-size="22" font-weight="700" fill="#92400e">{label}</text>\n')
            else:
                parts.append(f'<text x="{x+cell/2:.1f}" y="{y+cell/2+6:.1f}" text-anchor="middle" font-family="Arial" font-size="17" font-weight="700" fill="{stroke}">{label}</text>\n')
    # spectral ring around center
    cx, cy = bx + size / 2, by + size / 2
    parts.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{cell*1.05:.1f}" fill="none" stroke="#7c3aed" stroke-width="7" stroke-dasharray="16 12"/>\n')
    parts.append(f'<text x="{cx:.1f}" y="{cy+cell*1.4:.1f}" text-anchor="middle" font-family="Arial" font-size="15" fill="#6d28d9">spectral ring / filter path</text>\n')
    # control blocks
    blocks = [
        (790, 180, 300, 86, "#eef2ff", "#3730a3", "FPGA / MCU timing hub", "shared timestamp, trigger, FIFO"),
        (790, 305, 300, 86, "#ecfeff", "#0e7490", "Differential ADC", "bucket trace + calibration"),
        (790, 430, 300, 86, "#fff7ed", "#c2410c", "DAC thresholds", "event ON/OFF references"),
        (790, 555, 300, 86, "#f0fdf4", "#15803d", "USB / Ethernet stream", "events, frames, bucket, spectra"),
    ]
    for x, y, bw, bh, fill, stroke, title, sub in blocks:
        parts.append(f'<rect x="{x}" y="{y}" width="{bw}" height="{bh}" rx="14" fill="{fill}" stroke="{stroke}" stroke-width="2"/>\n')
        parts.append(f'<text x="{x+18}" y="{y+34}" font-family="Arial" font-size="20" font-weight="700" fill="{stroke}">{title}</text>\n')
        parts.append(f'<text x="{x+18}" y="{y+63}" font-family="Arial" font-size="15" fill="#475569">{sub}</text>\n')
    arrow = '<path d="M 710 450 C 750 420, 750 245, 790 225" fill="none" stroke="#334155" stroke-width="3" marker-end="url(#arrow)"/>\n'
    parts.insert(1, '<defs><marker id="arrow" markerWidth="10" markerHeight="10" refX="7" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#334155"/></marker></defs>\n')
    parts.append(arrow)
    parts.append('<path d="M 710 450 C 750 450, 750 350, 790 348" fill="none" stroke="#334155" stroke-width="3" marker-end="url(#arrow)"/>\n')
    parts.append('<path d="M 710 450 C 750 470, 750 475, 790 473" fill="none" stroke="#334155" stroke-width="3" marker-end="url(#arrow)"/>\n')
    parts.append('<path d="M 940 516 L 940 555" fill="none" stroke="#334155" stroke-width="3" marker-end="url(#arrow)"/>\n')
    # legend
    legend = [(100, 770, "#dbeafe", "#2563eb", "EV event tile"), (280, 770, "#dcfce7", "#16a34a", "FR frame tile"), (460, 770, "#fef3c7", "#d97706", "SP bucket detector"), (700, 770, "#faf5ff", "#7c3aed", "spectral path")]
    for x, y, fill, stroke, text in legend:
        parts.append(f'<rect x="{x}" y="{y-22}" width="30" height="30" fill="{fill}" stroke="{stroke}" stroke-width="2"/>\n')
        parts.append(f'<text x="{x+42}" y="{y}" font-family="Arial" font-size="16" fill="#334155">{text}</text>\n')
    parts.append(svg_footer())
    return "".join(parts)


def signal_chain() -> str:
    w, h = 1200, 660
    parts = [svg_header(w, h)]
    parts.append('<defs><marker id="arrow2" markerWidth="10" markerHeight="10" refX="7" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#334155"/></marker></defs>\n')
    parts.append('<text x="60" y="70" font-family="Arial" font-size="34" font-weight="700" fill="#111827">HybridCamera Signal Chain</text>\n')
    rows = [
        ("Single-pixel bucket", "Photodiode / scintillator", "TIA + gain switch", "Differential ADC", "#fef3c7", "#b45309"),
        ("Event tiles", "Log/change detector", "Comparator + hysteresis", "Timestamp FIFO", "#dbeafe", "#1d4ed8"),
        ("Frame tiles", "Global shutter sensor", "MIPI / DVP capture", "Frame buffer", "#dcfce7", "#15803d"),
        ("Spectral branch", "Filter / grating", "Bucket or array readout", "Spectral bins", "#f3e8ff", "#7e22ce"),
    ]
    start_x = 60
    for i, (label, a, b, c, fill, stroke) in enumerate(rows):
        y = 125 + i * 115
        parts.append(f'<text x="{start_x}" y="{y+38}" font-family="Arial" font-size="18" font-weight="700" fill="{stroke}">{label}</text>\n')
        for j, text in enumerate([a, b, c]):
            x = 285 + j * 245
            parts.append(f'<rect x="{x}" y="{y}" width="190" height="68" rx="12" fill="{fill}" stroke="{stroke}" stroke-width="2"/>\n')
            parts.append(f'<text x="{x+95}" y="{y+40}" text-anchor="middle" font-family="Arial" font-size="15" font-weight="700" fill="#0f172a">{text}</text>\n')
            if j < 2:
                parts.append(f'<path d="M {x+190} {y+34} L {x+240} {y+34}" fill="none" stroke="#334155" stroke-width="3" marker-end="url(#arrow2)"/>\n')
        parts.append(f'<path d="M 1020 {y+34} L 1090 300" fill="none" stroke="#334155" stroke-width="2.5" marker-end="url(#arrow2)"/>\n')
    parts.append('<rect x="1020" y="265" width="140" height="95" rx="16" fill="#ffffff" stroke="#0f172a" stroke-width="2.5" filter="url(#softShadow)"/>\n')
    parts.append('<text x="1090" y="304" text-anchor="middle" font-family="Arial" font-size="18" font-weight="700" fill="#0f172a">Fusion</text>\n')
    parts.append('<text x="1090" y="330" text-anchor="middle" font-family="Arial" font-size="14" fill="#475569">calibrate + reconstruct</text>\n')
    parts.append('<text x="1090" y="350" text-anchor="middle" font-family="Arial" font-size="14" fill="#475569">scene / scan / spectrum</text>\n')
    parts.append(svg_footer())
    return "".join(parts)


def maybe_convert(svg_path: Path) -> None:
    png_path = svg_path.with_suffix(".png")
    try:
        subprocess.run(["convert", str(svg_path), str(png_path)], check=True)
    except Exception:
        # The SVG remains the source of truth; PNG conversion is a convenience.
        pass


def main() -> None:
    outputs = {
        FIGURES / "hybrid_board_layout.svg": board_layout(),
        FIGURES / "hybrid_signal_chain.svg": signal_chain(),
    }
    for path, text in outputs.items():
        write(path, text)
        maybe_convert(path)
    print("Generated HybridCamera diagrams in figures/")


if __name__ == "__main__":
    main()
