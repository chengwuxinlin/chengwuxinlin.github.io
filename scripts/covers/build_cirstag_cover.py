"""Build the CirSTAG project cover from a schematic and published table values.

The circuit drawing is conceptual; it is not the DES benchmark netlist.
The bars are a faithful, zero-based replot of Table I, page 6, DES row:
10x pin-capacitance scaling, 10% nodes perturbed, mean relative change (%)
in GNN-predicted arrival time at primary output pins.

Source: https://www.csl.cornell.edu/~zhiruz/pdfs/cirstag-dac2025.pdf
Unstable/sensitive: 0.5211%; stable: 0.0068%.
Requires Pillow; uses the workstation's Segoe UI fonts.
"""

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "assets/images/covers/cirstag.webp"
SCALE = 2
WIDTH, HEIGHT = 1200, 675
COLORS = {
    "paper": "#eeeee6", "forest": "#234b3e", "sage": "#9baa91",
    "ink": "#242c27", "ochre": "#b78b48", "line": "#ccd1c3",
    "panel": "#f6f5ef", "muted": "#57634f", "light": "#e5e9df",
}
DATA = {"stable": 0.0068, "sensitive": 0.5211}
FONT_DIR = Path("C:/Windows/Fonts")
image = Image.new("RGB", (WIDTH * SCALE, HEIGHT * SCALE), COLORS["paper"])
draw = ImageDraw.Draw(image)


def box(coords):
    return tuple(round(v * SCALE) for v in coords)


def line(points, fill="forest", width=2):
    draw.line([(round(x * SCALE), round(y * SCALE)) for x, y in points],
              fill=COLORS.get(fill, fill), width=round(width * SCALE), joint="curve")


def rect(coords, fill, outline=None, radius=0, width=1):
    kwargs = {"fill": COLORS.get(fill, fill)}
    if outline:
        kwargs.update(outline=COLORS.get(outline, outline), width=round(width * SCALE))
    if radius:
        draw.rounded_rectangle(box(coords), radius=round(radius * SCALE), **kwargs)
    else:
        draw.rectangle(box(coords), **kwargs)


def text(position, value, size=32, color="ink", bold=False, anchor="la"):
    font = ImageFont.truetype(str(FONT_DIR / ("seguisb.ttf" if bold else "segoeui.ttf")),
                              size=round(size * SCALE))
    draw.text((position[0] * SCALE, position[1] * SCALE), value,
              font=font, fill=COLORS[color], anchor=anchor)


def circle(x, y, radius, fill="paper", outline="forest", width=2):
    draw.ellipse(box((x-radius, y-radius, x+radius, y+radius)),
                 fill=COLORS[fill], outline=COLORS[outline], width=round(width*SCALE))


def bezier(points, count=40):
    a, b, c, d = points
    return [((1-t)**3*a[0]+3*(1-t)**2*t*b[0]+3*(1-t)*t*t*c[0]+t**3*d[0],
             (1-t)**3*a[1]+3*(1-t)**2*t*b[1]+3*(1-t)*t*t*c[1]+t**3*d[1])
            for t in (i/count for i in range(count+1))]


def gate_and(x, y):
    # 90x86 AND gate, with a flat input side and rounded output side.
    outline = [(x, y-43), (x+43, y-43)]
    outline += bezier([(x+43,y-43),(x+104,y-43),(x+104,y+43),(x+43,y+43)])
    outline += [(x, y+43), (x, y-43)]
    draw.polygon([(round(a*SCALE),round(b*SCALE)) for a,b in outline], fill=COLORS["panel"])
    line(outline, width=3)


def gate_or(x, y):
    upper = bezier([(x,y-48),(x+55,y-48),(x+81,y-22),(x+105,y)])
    lower = bezier([(x+105,y),(x+81,y+22),(x+55,y+48),(x,y+48)])
    back = bezier([(x,y+48),(x+25,y+16),(x+25,y-16),(x,y-48)])
    outline = upper + lower + back
    draw.polygon([(round(a*SCALE),round(b*SCALE)) for a,b in outline], fill=COLORS["panel"])
    line(outline, width=3)


# Same framing and palette as the other website covers.
text((300, 48), "Circuit graph", size=38, anchor="ma")
text((920, 48), "Delay sensitivity", size=38, anchor="ma")

# Schematic circuit: inputs feed two AND gates, then an OR gate.
for label, y in [("A",221),("B",330),("C",439)]:
    text((70,y),label,size=29,color="muted",anchor="mm")
    circle(105,y,6,fill="forest")
line([(111,221),(158,221),(158,215),(200,215)],width=3)
line([(111,330),(158,330),(158,265),(200,265)],width=3)
line([(158,330),(158,395),(200,395)],width=3)
line([(111,439),(175,439),(175,445),(200,445)],width=3)
circle(158,330,4,fill="forest")
gate_and(200,240)
gate_and(200,420)
line([(288,240),(335,240),(335,303),(391,303)],width=3)
line([(288,420),(335,420),(335,357),(391,357)],width=3)
gate_or(375,330)
line([(480,330),(530,330)],width=3)
circle(530,330,6,fill="forest")

# Highlighted pins indicate the concept of ranking, not measured DES locations.
for x,y in [(200,265),(288,240),(480,330)]:
    circle(x,y,15,fill="paper",outline="ochre",width=2)
    circle(x,y,6,fill="ochre",outline="ochre",width=1)
line([(488,318),(520,265),(556,265)],fill="ochre",width=2)
text((547,228),"Sensitive",size=25,color="muted",anchor="ma")
text((547,258),"pins",size=25,color="muted",anchor="ma")

# Transition arrow between the schematic and the measured example.
line([(575,350),(647,350)],width=2)
line([(635,340),(647,350),(635,360)],width=2)

# Exact published comparison. Bar lengths share a zero baseline and scale.
CHART_LEFT, CHART_RIGHT = 733, 1129
CHART_TOP, AXIS_Y = 209, 439
MAXIMUM = 0.6
for value in [0.0,0.3,0.6]:
    x = CHART_LEFT + value/MAXIMUM*(CHART_RIGHT-CHART_LEFT)
    line([(x,CHART_TOP+24),(x,AXIS_Y)],fill="line",width=1)
    text((x,AXIS_Y+10),f"{value:.1f}%",size=23,color="muted",anchor="ma")
line([(CHART_LEFT,AXIS_Y),(CHART_RIGHT,AXIS_Y)],fill="sage",width=1.5)
for name, label, y, color in [("stable","Stable",224,"forest"),("sensitive","Sensitive",334,"ochre")]:
    value = DATA[name]
    text((CHART_LEFT,y),label,size=30,bold=True)
    text((CHART_RIGHT,y),f"{value:.4f}%",size=30,bold=True,color=color,anchor="ra")
    end = CHART_LEFT + value/MAXIMUM*(CHART_RIGHT-CHART_LEFT)
    rect((CHART_LEFT,y+48,end,y+77),fill=color)

text((600,600),"DES benchmark · 10× capacitance · 10% of nodes",size=28,color="muted",anchor="ma")

OUTPUT.parent.mkdir(parents=True, exist_ok=True)
image.resize((WIDTH,HEIGHT), Image.Resampling.LANCZOS).save(OUTPUT,"WEBP",quality=95,method=6)
print(f"Saved {OUTPUT} ({OUTPUT.stat().st_size:,} bytes; {WIDTH}×{HEIGHT})")
