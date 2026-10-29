"""Rebuild the decorative hero manifold; no data or performance claim is encoded.

The SVG is deliberately static. Ambient motion is a separate progressive
enhancement so this illustration is sharp and complete without JavaScript.
"""

from math import cos, pi, sin, sqrt
from pathlib import Path
from xml.etree import ElementTree


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "assets" / "images" / "research-field-v2.svg"
FOREST = "#234b3e"
SAGE = "#9baa91"
PAPER = "#f6f5f0"
OCHRE = "#bc8f4b"


def surface(u, v):
    """A finite, asymmetric smooth sheet in an oblique camera projection."""
    height = sin(pi * u) * sin(pi * v)
    twist = sin(2 * pi * u) * sin(pi * v)
    return (
        76 + 330 * u + 87 * v + 12 * height,
        307 - 139 * u + 116 * v - 132 * height + 32 * twist,
    )


def curve(points, close=False):
    return "M " + " L ".join(f"{x:.1f} {y:.1f}" for x, y in points) + (" Z" if close else "")


def samples(f, count=48):
    return [f(i / count) for i in range(count + 1)]


def path(points, **attrs):
    attr = " ".join(f'{name.replace("_", "-")}="{value}"' for name, value in attrs.items())
    return f'    <path d="{curve(points)}" {attr}/>'


def node(x, y, r=2.8, **attrs):
    attr = " ".join(f'{name.replace("_", "-")}="{value}"' for name, value in attrs.items())
    return f'    <circle cx="{x:.2f}" cy="{y:.2f}" r="{r}" {attr}/>'


def mix(a, b, proportion):
    aa = [int(a[i:i + 2], 16) for i in (1, 3, 5)]
    bb = [int(b[i:i + 2], 16) for i in (1, 3, 5)]
    return "#" + "".join(f"{round(x + (y - x) * proportion):02x}" for x, y in zip(aa, bb))


parts = [f'''<svg xmlns="http://www.w3.org/2000/svg" width="620" height="520" viewBox="0 0 620 520" fill="none">
  <title>A manifold, from geometry to connected ideas</title>
  <desc>A translucent forest-green mathematical surface with fine contour lines, an ochre focal point, and a continuation of connected nodes. Decorative illustration, not research data.</desc>
  <defs>
    <radialGradient id="manifold-halo">
      <stop stop-color="{SAGE}" stop-opacity=".16"/>
      <stop offset=".66" stop-color="{SAGE}" stop-opacity=".045"/>
      <stop offset="1" stop-color="{SAGE}" stop-opacity="0"/>
    </radialGradient>
    <radialGradient id="manifold-ground">
      <stop stop-color="{FOREST}" stop-opacity=".09"/>
      <stop offset="1" stop-color="{FOREST}" stop-opacity="0"/>
    </radialGradient>
    <linearGradient id="manifold-sheet" x1="151" y1="392" x2="387" y2="164" gradientUnits="userSpaceOnUse">
      <stop stop-color="{SAGE}" stop-opacity=".17"/>
      <stop offset=".46" stop-color="{PAPER}" stop-opacity=".46"/>
      <stop offset="1" stop-color="{SAGE}" stop-opacity=".12"/>
    </linearGradient>
    <linearGradient id="manifold-line" x1="113" y1="414" x2="409" y2="171" gradientUnits="userSpaceOnUse">
      <stop stop-color="{FOREST}" stop-opacity=".42"/>
      <stop offset=".42" stop-color="{FOREST}" stop-opacity=".7"/>
      <stop offset="1" stop-color="{FOREST}" stop-opacity=".82"/>
    </linearGradient>
    <linearGradient id="manifold-link" x1="400" y1="193" x2="568" y2="301" gradientUnits="userSpaceOnUse">
      <stop stop-color="{FOREST}" stop-opacity=".5"/>
      <stop offset="1" stop-color="{SAGE}" stop-opacity=".34"/>
    </linearGradient>
    <radialGradient id="manifold-focus">
      <stop stop-color="{OCHRE}" stop-opacity=".19"/>
      <stop offset="1" stop-color="{OCHRE}" stop-opacity="0"/>
    </radialGradient>
  </defs>
  <ellipse cx="340" cy="248" rx="239" ry="207" fill="url(#manifold-halo)"/>
  <ellipse cx="302" cy="402" rx="208" ry="47" transform="rotate(-12 302 402)" fill="url(#manifold-ground)"/>
  <!-- Detached, quiet traces give the floating sheet a ground and depth. -->
  <g stroke="{SAGE}" stroke-width=".7" stroke-linecap="round" fill="none">''']

for index in range(4):
    points = samples(lambda t: (
        64 + 439 * t,
        376 + index * 15 + 24 * sin(pi * t) - 68 * t * t,
    ))
    parts.append(path(points, opacity=f"{.28 - index * .04:.2f}", stroke_dasharray="1 7"))
parts.append("  </g>")

# A faint lower echo makes the surface read as a floating, tangible object.
parts.append(f'  <g stroke="{SAGE}" stroke-width=".65" opacity=".20">')
for v in (.12, .40, .70, 1):
    parts.append(path(samples(lambda t: (surface(t, v)[0] - 2, surface(t, v)[1] + 16))))
parts.append("  </g>")

boundary = [surface(0, 0), surface(1, 0), surface(1, 1), surface(0, 1)]
parts.append(f'  <path d="{curve(boundary, True)}" fill="url(#manifold-sheet)"/>')

# Small shaded quadrilaterals describe the actual surface curvature. The
# underlying gradient keeps their joins quiet at fractional pixel scales.
parts.append('  <g stroke="none">')
for j in range(18):
    for i in range(24):
        u, v = (i + .5) / 24, (j + .5) / 18
        du = pi * cos(pi * u) * sin(pi * v) - .43 * cos(2 * pi * u) * sin(pi * v)
        dv = pi * sin(pi * u) * cos(pi * v) - .24 * sin(2 * pi * u) * cos(pi * v)
        normal = sqrt(du * du + dv * dv + 1)
        illumination = max(0, min(1, (-.26 * du + .4 * dv + .88) / normal))
        shade = mix(SAGE, PAPER, .28 + illumination * .72)
        corners = [surface(i / 24, j / 18), surface((i + 1) / 24, j / 18),
                   surface((i + 1) / 24, (j + 1) / 18), surface(i / 24, (j + 1) / 18)]
        parts.append(f'    <path d="{curve(corners, True)}" fill="{shade}" fill-opacity=".48"/>')
parts.append("  </g>")

parts.append('  <g stroke="url(#manifold-line)" stroke-linecap="round" stroke-linejoin="round">')
for j in range(21):
    v = j / 20
    parts.append(path(samples(lambda t: surface(t, v)), stroke_width=".68" if j % 5 else ".94"))
for i in range(27):
    u = i / 26
    parts.append(path(samples(lambda t: surface(u, t)), stroke_width=".62" if i % 6 else ".9"))
parts.append("  </g>")

# One illuminated ridge and a darker leading edge strengthen perspective.
parts.append(path(samples(lambda t: surface(t, .39)), stroke=PAPER, stroke_width="2.4", opacity=".53"))
parts.append(path(samples(lambda t: surface(t, .39)), stroke=FOREST, stroke_width=".86", opacity=".77"))
parts.append(path(samples(lambda t: surface(t, 1)), stroke=FOREST, stroke_width="1.25", opacity=".66"))
parts.append(path(samples(lambda t: surface(1, t)), stroke=FOREST, stroke_width="1.15", opacity=".72"))

# The graph meets the sheet at real boundary points; it remains sparse enough
# to read at the final layout's smaller mobile size.
a, b, c = surface(1, 0), surface(1, .46), surface(1, 1)
graph_nodes = [a, (491, 121), (549, 177), (575, 257), (535, 332), (443, 366), b, c]
graph_edges = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5),
               (0, 2), (0, 6), (1, 6), (2, 6), (2, 7),
               (3, 6), (3, 7), (4, 7), (5, 7)]
parts.append('  <g stroke="url(#manifold-link)" stroke-width=".85" stroke-linejoin="round">')
for start, end in graph_edges:
    parts.append(path([graph_nodes[start], graph_nodes[end]]))
parts.append("  </g>")

parts.append(f'  <g fill="{PAPER}" stroke="{FOREST}" stroke-width="1.05">')
for index, (x, y) in enumerate(graph_nodes):
    parts.append(node(x, y, [3.4, 3.2, 3.8, 2.8, 2.8, 2.5, 3.1, 3.5][index], opacity=".83"))
parts.append("  </g>")

parts.append(f'  <g fill="{FOREST}">')
for u, v, radius in [(0, 0, 2.5), (0, 1, 2.5), (.19, .75, 1.8), (.43, .39, 2.3), (.69, .20, 1.7)]:
    parts.append(node(*surface(u, v), radius, opacity=".83"))
parts.append("  </g>")

# An ochre focal point sits on the sheet, with perspective rings following
# local surface coordinates instead of a flat screen-space target symbol.
focus_u, focus_v = .84, .44
fx, fy = surface(focus_u, focus_v)
parts.append(f'  <circle cx="{fx:.2f}" cy="{fy:.2f}" r="42" fill="url(#manifold-focus)"/>')
parts.append(f'  <g stroke="{OCHRE}" stroke-linecap="round">')
for radius, opacity in [(.055, .77), (.095, .42), (.14, .2)]:
    ring = samples(lambda t: surface(focus_u + radius * cos(2 * pi * t), focus_v + radius * 1.55 * sin(2 * pi * t)), 72)
    parts.append(path(ring, stroke_width=".9", opacity=str(opacity)))
parts.append(path(samples(lambda t: surface(.70 + .14 * t, .48 - .04 * t)), stroke_width="1.5", opacity=".87"))
parts.append(f'    <circle cx="{fx:.2f}" cy="{fy:.2f}" r="5.2" fill="{OCHRE}" stroke="{PAPER}" stroke-width="1.6"/>')
parts.append("  </g>")
parts.append("</svg>\n")

svg = "\n".join(parts)
ElementTree.fromstring(svg)
OUTPUT.write_text(svg, encoding="utf-8", newline="\n")
print(f"Wrote {OUTPUT.relative_to(ROOT)} ({len(svg):,} characters)")
