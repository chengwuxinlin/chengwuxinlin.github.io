"""Draw original method illustrations for forecasting and copper metrology.

These diagrams contain no observations, model outputs, or benchmark results.
All coordinates and curves are chosen only to explain the respective workflows.
Run with Python and Pillow; the shared drawing system uses Windows Segoe UI.
"""

import math

from PIL import Image

from build_research_covers import (
    Canvas, GREEN, LINE, OCHRE, OUTPUT, PANEL, ROOT, SAGE, xy,
)


def dashed(c, start, end, color=SAGE, width=2, dash=8, gap=7):
    length = math.dist(start, end)
    ux, uy = (end[0] - start[0]) / length, (end[1] - start[1]) / length
    for pos in range(0, math.ceil(length), dash + gap):
        last = min(pos + dash, length)
        c.line([(start[0] + ux * pos, start[1] + uy * pos),
                (start[0] + ux * last, start[1] + uy * last)], color, width)


def polygon(c, points, fill):
    c.d.polygon([xy(point) for point in points], fill=fill)


def build_forecasting():
    c = Canvas()
    c.text(310, 76, "Past observations", 38)
    c.text(910, 76, "Future forecasts", 38)
    c.box((65, 132, 1135, 495), fill=PANEL, outline=LINE, radius=18)

    # A quiet chart frame with no tick values: these are explanatory curves,
    # not a time-series dataset, confidence interval, or financial projection.
    for y in [205, 285, 365, 445]:
        c.line([(95, y), (1105, y)], "#e0e3d8", 1)
    cutoff = 645
    c.d.rectangle(xy((cutoff, 134, 1133, 493)), fill="#e7ebdf")
    for y in [205, 285, 365, 445]:
        c.line([(cutoff, y), (1105, y)], "#dce2d4", 1)

    # Deliberately non-monotonic, with no growth/return implication.
    raw = [0, 9, 3, 24, 20, 7, 12, -4, 11, 15, 6, 32, 22, 37, 26,
           30, 18, 26, 11, 16, 33, 23, 39, 30, 47, 36, 22, 34,
           31, 46, 38, 47, 28, 35, 19, 30, 40]
    points = [(105 + i * (cutoff - 105) / (len(raw) - 1), 365 - value * 1.5)
              for i, value in enumerate(raw)]
    c.line(points, GREEN, 4)
    start_y = points[-1][1]

    # Illustration of uncertainty broadening with the forecast horizon.
    # No percentile or confidence level is assigned to the shaded range.
    mid, upper, lower = [], [], []
    for i in range(81):
        t = i / 80
        x = cutoff + t * 450
        y = start_y - 28 * math.sin(t * math.pi * 1.4) + 15 * t
        spread = 6 + 78 * t ** .75
        mid.append((x, y))
        upper.append((x, y - spread))
        lower.append((x, y + spread))
    polygon(c, upper + list(reversed(lower)), "#ced9c3")
    c.line(upper, "#b4c3a9", 1.5)
    c.line(lower, "#b4c3a9", 1.5)

    # Multiple model estimates diverge, while the central line conveys the
    # calibrated combination. Their paths are schematic, not reported scores.
    for offset, color in [(-38, "#9baa91"), (45, "#9baa91")]:
        curve = [(x, y + offset * (i / 80) + 11 * math.sin(i / 80 * 6) * (i / 80))
                 for i, (x, y) in enumerate(mid)]
        for i in range(0, len(curve) - 2, 5):
            c.line(curve[i:i + 3], color, 2)
    c.line(mid, OCHRE, 4)
    c.circle(cutoff, start_y, 7, GREEN, PANEL, 2)
    dashed(c, (cutoff, 151), (cutoff, 438), GREEN, 2, 7, 8)
    c.text(355, 174, "Available evidence", 25, "#586650")
    c.text(906, 174, "Illustrative uncertainty", 25, "#586650")
    c.text(cutoff, 466, "Forecast cutoff", 25, GREEN)

    # A small horizontal workflow ties the intuitive time plot to this
    # project's specialist-pooling and calibration work.
    for i, y in enumerate([540, 553, 566]):
        c.line([(100, y), (137, y)], [GREEN, SAGE, OCHRE][i], 3)
    c.text(155, 553, "Model specialists", 27, GREEN, anchor="lm")
    c.arrow((390, 553), (456, 553), GREEN, 2.5)
    c.box((477, 525, 719, 583), fill="#e2e8d9", outline="#c6d1bd", radius=10)
    c.text(598, 553, "Calibrate", 28, GREEN, bold=True)
    c.arrow((740, 553), (806, 553), GREEN, 2.5)
    c.text(972, 553, "Forecast + uncertainty", 27, GREEN)
    c.line([(60, 611), (1140, 611)], LINE, 1)
    c.text(600, 639, "Method illustration · point-in-time model evaluation", 25, "#586650")
    c.save("forecasting.webp")


def build_copper_dishing():
    c = Canvas()
    c.text(365, 76, "Copper dishing", 39)
    c.text(975, 76, "ML metrology", 38)
    c.box((57, 133, 735, 581), fill=PANEL, outline=LINE, radius=18)
    c.box((814, 237, 1137, 402), fill=PANEL, outline=LINE, radius=18)

    # A planar dielectric surrounds a recessed copper feature. This is an
    # explanatory cross-section, not a measured profile or scaled geometry.
    left, right, top, bottom = 93, 700, 270, 535
    copper_l, copper_r = 245, 555
    polygon(c, [(left, top), (copper_l, top), (copper_l, bottom),
                (copper_r, bottom), (copper_r, top), (right, top),
                (right, bottom + 20), (left, bottom + 20)], "#d7dfce")
    # Subtle material lines, kept behind labels and outside the copper region.
    for y in range(292, 535, 25):
        c.line([(left + 4, y), (copper_l - 4, y)], "#c4ceba", 1)
        c.line([(copper_r + 4, y), (right - 4, y)], "#c4ceba", 1)

    surface = []
    for i in range(101):
        t = i / 100
        surface.append((copper_l + t * (copper_r - copper_l), top + 92 * math.sin(math.pi * t) ** .72))
    polygon(c, surface + [(copper_r, bottom), (copper_l, bottom)], "#c29456")
    # Slight material shading adds depth without making the section look like
    # an experimental heatmap, predicted field, or numeric measurement.
    for y in range(385, bottom, 4):
        blend = (y - 385) / (bottom - 385)
        color = tuple(round(a + (b - a) * blend) for a, b in zip((194,148,86),(180,132,70)))
        c.line([(copper_l + 2, y), (copper_r - 2, y)], color, 4)
    c.line(surface, "#916b36", 4)
    c.line([(left, top), (copper_l, top)], GREEN, 3)
    c.line([(copper_r, top), (right, top)], GREEN, 3)
    c.line([(copper_l, top), (copper_l, bottom), (copper_r, bottom), (copper_r, top)], "#9e7945", 2)

    # The reference line lies at the surrounding polished plane. The arrow
    # measures vertically to the center of the recessed copper surface.
    dashed(c, (copper_l - 8, top), (copper_r + 8, top), GREEN, 2, 7, 6)
    c.text(400, 222, "Polished reference plane", 28, GREEN)
    center_x = (copper_l + copper_r) / 2
    center_y = top + 92
    c.arrow((center_x, top + 5), (center_x, center_y - 4), GREEN, 2.5, 9)
    c.arrow((center_x, center_y - 4), (center_x, top + 5), GREEN, 2.5, 9)
    c.text(center_x + 22, 312, "depth", 27, GREEN, anchor="lm", bold=True)
    c.text(400, 461, "Copper", 33, "#fffaf1", bold=True)
    c.text(170, 445, "Dielectric", 24, GREEN)
    c.text(629, 445, "Dielectric", 24, GREEN)

    # Measurements enter an estimator; its output is a depth estimate. The
    # three data marks and network connections are symbolic, not sensor data.
    c.arrow((744, 320), (800, 320), GREEN, 3)
    c.text(975, 193, "Measurements → estimate", 25, "#586650")
    for i, h in enumerate([33, 58, 43]):
        c.line([(846 + i * 16, 351), (846 + i * 16, 351 - h)], OCHRE, 5)
    c.arrow((896, 322), (922, 322), GREEN, 2, 7)
    nodes = [(944, 291), (944, 351), (994, 307), (994, 339), (1040, 322)]
    for a, b in [(0,2), (0,3), (1,2), (1,3), (2,4), (3,4)]:
        c.line([nodes[a], nodes[b]], SAGE, 2)
    for x,y in nodes:
        c.circle(x, y, 6, GREEN)
    c.text(975, 373, "Learn from physical signals", 23, GREEN)
    c.arrow((975, 413), (975, 453), GREEN, 3)
    c.box((827, 467, 1123, 550), fill="#e2e8d9", outline="#c6d1bd", radius=12)
    c.text(975, 508, "Depth estimate", 30, GREEN, bold=True)
    c.line([(60, 611), (1140, 611)], LINE, 1)
    c.text(600, 639, "Conceptual cross-section · semiconductor metrology", 25, "#586650")
    c.save("copper-dishing.webp")


if __name__ == "__main__":
    build_forecasting()
    build_copper_dishing()
    for filename in ["forecasting.webp", "copper-dishing.webp"]:
        path = OUTPUT / filename
        print(f"{path.relative_to(ROOT)}: {Image.open(path).size}, {path.stat().st_size:,} bytes")
