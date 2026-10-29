"""Recompose supplied research examples into website covers; no model results synthesized.

Run from any directory with Python and Pillow installed. Source PNGs stay in .local;
the final WebP files are the only published artifacts. Illustrative graph/sample
positions explain the methods and must not be presented as experimental outputs.
"""

from pathlib import Path
import hashlib
import math
import random
import urllib.request

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "assets/images/covers"
SOURCES = ROOT / ".local/cover-sources"
SCALE = 2
SIZE = (1200, 675)
PAPER = "#eeeee6"
PANEL = "#f8f7f2"
GREEN = "#234b3e"
SAGE = "#9baa91"
INK = "#242c27"
OCHRE = "#b78b48"
LINE = "#d2d8ca"
FONT_ROOT = Path("C:/Windows/Fonts")


def font(size, bold=False):
    return ImageFont.truetype(str(FONT_ROOT / ("segoeuib.ttf" if bold else "segoeui.ttf")), round(size * SCALE))


def xy(values):
    return tuple(round(x * SCALE) for x in values)


class Canvas:
    def __init__(self):
        self.im = Image.new("RGB", xy(SIZE), PAPER)
        self.d = ImageDraw.Draw(self.im)

    def text(self, x, y, label, size=36, color=GREEN, anchor="mm", bold=False):
        self.d.text(xy((x, y)), label, font=font(size, bold), fill=color, anchor=anchor)

    def line(self, points, color=GREEN, width=2):
        self.d.line([xy(point) for point in points], fill=color, width=round(width * SCALE), joint="curve")

    def circle(self, x, y, radius, fill, outline=None, width=1):
        self.d.ellipse(xy((x-radius, y-radius, x+radius, y+radius)), fill=fill,
                       outline=outline, width=round(width*SCALE))

    def box(self, box, fill=PANEL, outline=LINE, radius=18, width=1):
        self.d.rounded_rectangle(xy(box), radius=round(radius*SCALE), fill=fill,
                                outline=outline, width=round(width*SCALE))

    def arrow(self, start, end, color=GREEN, width=3, head=11):
        self.line([start, end], color, width)
        angle = math.atan2(end[1]-start[1], end[0]-start[0])
        left = (end[0]-head*math.cos(angle-.55), end[1]-head*math.sin(angle-.55))
        right = (end[0]-head*math.cos(angle+.55), end[1]-head*math.sin(angle+.55))
        self.line([left, end, right], color, width)

    def paste(self, image, box, resample=Image.Resampling.LANCZOS):
        x, y, width, height = box
        image = image.resize(xy((width, height)), resample=resample)
        self.im.paste(image, xy((x, y)), image if image.mode=="RGBA" else None)

    def save(self, filename):
        OUTPUT.mkdir(parents=True, exist_ok=True)
        self.im.resize(SIZE, Image.Resampling.LANCZOS).save(OUTPUT / filename, quality=96, method=6)


def checked_image(path, expected):
    actual = hashlib.sha256(path.read_bytes()).hexdigest()
    if actual != expected:
        raise ValueError(f"Source identity changed: {path.name}; inspect before updating the expected hash")
    return Image.open(path).convert("RGB")


def build_spade():
    source = checked_image(ROOT / "images/SPADE.png",
        "d0b3fe61f5f94835de1b7959eaf0745d8e571886ba3bae3dea38d1e60924258a")
    c = Canvas()
    c.text(205, 87, "Input images", 38)
    c.text(602, 87, "Model sensitivity", 38)
    c.text(1004, 87, "Fragile examples", 36)
    # Exact source digit examples from the published non-robust-sample panel.
    cols = [787, 887, 987]
    rows = [62, 157, 253]
    tiles = [source.crop((x, y, x+83, y+83)) for y in rows for x in cols]
    for i, tile in enumerate(tiles):
        x = 60 + (i % 3) * 103
        y = 205 + (i // 3) * 110
        c.box((x-5, y-5, x+93, y+93), fill=PANEL, radius=10)
        c.paste(tile, (x, y, 88, 88), Image.Resampling.NEAREST)
    c.arrow((378, 360), (425, 360))
    # Original schematic graph, deliberately without numeric scores/ranking.
    nodes = [(471,293), (548,229), (634,245), (723,292), (480,393),
             (568,332), (657,348), (723,420), (536,476), (626,479)]
    edges = [(0,1),(0,4),(0,5),(1,2),(1,5),(2,3),(2,5),(2,6),
             (3,6),(3,7),(4,5),(4,8),(5,6),(5,8),(5,9),(6,7),(6,9),(7,9),(8,9)]
    for a,b in edges:
        c.line([nodes[a], nodes[b]], color="#b6c2ad", width=2)
    for a,b in [(1,5),(5,6),(6,7)]:
        c.line([nodes[a],nodes[b]], color=OCHRE, width=3)
    for i,(x,y) in enumerate(nodes):
        c.circle(x,y,11, GREEN if i not in [1,5,6] else OCHRE, PAPER, 2)
    for i in [1,5,6]:
        x,y=nodes[i]
        c.circle(x,y,23,None,OCHRE,1)
    c.arrow((773, 360), (824, 360))
    # Selected examples are all taken from the same non-robust source grid.
    for i, tile in enumerate([tiles[0], tiles[2], tiles[7]]):
        x,y=920,164+i*142
        c.box((x-10,y-10,x+126,y+126), fill="#e9dfc9", outline=OCHRE, radius=14, width=2)
        c.paste(tile,(x,y,116,116), Image.Resampling.NEAREST)
    c.line([(60,601),(1140,601)],color=LINE,width=1)
    c.text(600,631,"Find vulnerable inputs before relying on a model",27,color="#586650")
    c.save("spade.webp")


def domain_mask(u,v):
    """Illustrative annular channel domain, normalized to the source geometry."""
    return (((abs(v) <= .36 and abs(u) <= 2.3) or u*u+v*v<=.86**2)
            and u*u+v*v >= .41**2)


def flow_domain(c, cx, cy, selected=False):
    # Same schematic geometry for both panels; point locations are illustrative.
    scale=93
    outer=(cx-.86*scale,cy-.86*scale,cx+.86*scale,cy+.86*scale)
    c.d.rectangle(xy((cx-2.3*scale,cy-.36*scale,cx+2.3*scale,cy+.36*scale)), fill="#e1e6da")
    c.d.ellipse(xy(outer),fill="#e1e6da")
    c.circle(cx,cy,.41*scale,PAPER)
    # Domain outline is the union of channel and ring, with a central hole.
    intersection=math.sqrt(.86**2-.36**2)
    for sign in [-1,1]:
        y=cy+sign*.36*scale
        c.line([(cx-2.3*scale,y),(cx-intersection*scale,y)],SAGE,1.5)
        c.line([(cx+intersection*scale,y),(cx+2.3*scale,y)],SAGE,1.5)
    c.line([(cx-2.3*scale,cy-.36*scale),(cx-2.3*scale,cy+.36*scale)],SAGE,1.5)
    c.line([(cx+2.3*scale,cy-.36*scale),(cx+2.3*scale,cy+.36*scale)],SAGE,1.5)
    start=math.asin(.36/.86)
    for begin,end in [(start,math.pi-start),(math.pi+start,2*math.pi-start)]:
        points=[(cx+.86*scale*math.cos(t),cy+.86*scale*math.sin(t))
                for t in [begin+(end-begin)*i/80 for i in range(81)]]
        c.line(points,SAGE,1.5)
    c.circle(cx,cy,.41*scale,None,SAGE,1.5)
    rng=random.Random(491)
    points=[]
    while len(points)<175:
        u,v=rng.uniform(-2.22,2.22),rng.uniform(-.82,.82)
        if domain_mask(u,v): points.append((u,v))
    if selected:
        # Chosen to communicate adaptive sampling, not a claimed algorithm run.
        chosen=[]
        for i,(u,v) in enumerate(points):
            if ((.43 < math.hypot(u,v)<.78 and i%2==0) or i%10==0):
                chosen.append((u,v))
        for u,v in points:
            c.circle(cx+u*scale,cy+v*scale,1.3,"#c3cdb9")
        for i,(u,v) in enumerate(chosen):
            c.circle(cx+u*scale,cy+v*scale,4.2,OCHRE if i%4==0 else GREEN)
    else:
        for u,v in points: c.circle(cx+u*scale,cy+v*scale,2.5,"#76886e")


def build_sgm():
    source_path=SOURCES/"sgm-pinn-pressure-errors.png"
    if not source_path.exists():
        SOURCES.mkdir(parents=True,exist_ok=True)
        urllib.request.urlretrieve("https://arxiv.org/html/2407.07358v1/results/Pressure_Vis_AR_1.0.png",source_path)
    source=checked_image(source_path,
        "b3f8368702cdc8bcfa23f39c5d8bb033a430cbfac0112a5454be74e5733759e8")
    c=Canvas()
    c.text(291,74,"Flow-domain points",37)
    c.text(291,389,"Informative subset",37)
    c.text(879,74,"Pressure error",38)
    flow_domain(c,291,210,selected=False)
    c.arrow((291,309),(291,344),width=3)
    flow_domain(c,291,502,selected=True)
    c.arrow((527,501),(578,501),width=3)
    c.line([(578,501),(578,339),(623,339)],GREEN,3)
    c.arrow((607,339),(637,339),width=3)
    # Crop the measured field out of its screenshot frame. A domain mask removes
    # only the slate page background/text; all retained field colors come from
    # the source image, not a synthetic simulation or a re-inferred color scale.
    c.box((637,173,1140,526),fill=PANEL,outline=LINE,radius=18)
    field=source.crop((26,20,495,162)).convert("RGBA")
    mask=Image.new("L",field.size,0)
    md=ImageDraw.Draw(mask)
    md.rectangle((0,35,468,105),fill=255)
    md.ellipse((165,0,306,141),fill=255)
    md.ellipse((200,37,268,105),fill=0)
    # Remove residual frame pixels at the screenshot's antialiased boundary.
    # The slate background is distinct from every color on the field scale.
    background=source.getpixel((10,190))
    for y in range(field.height):
        for x in range(field.width):
            pixel=field.getpixel((x,y))[:3]
            if max(abs(a-b) for a,b in zip(pixel,background))<16:
                mask.putpixel((x,y),0)
    field.putalpha(mask)
    c.paste(field,(658,255,402,122))
    c.text(850,215,"SGM-S · 350K iterations",27,color=GREEN)
    # Original complete vertical color ramp (low .01 to high .07), resized only.
    colorbar=source.crop((525,29,563,601))
    c.paste(colorbar,(1080,254,17,190))
    c.text(1089,225,"0.07",23,color=GREEN)
    c.text(1089,470,"0.01",23,color=GREEN)
    c.text(850,430,"Absolute pressure error",27,color=GREEN)
    c.text(850,471,"Published result · 4.1 h",24,color="#586650")
    c.line([(60,608),(1140,608)],color=LINE,width=1)
    c.text(600,638,"Focus training on informative parts of the flow",27,color="#586650")
    c.save("sgm-pinn.webp")


if __name__=="__main__":
    build_spade()
    build_sgm()
    for name in ["spade.webp","sgm-pinn.webp"]:
        path=OUTPUT/name
        print(f"{path.relative_to(ROOT)}: {Image.open(path).size}, {path.stat().st_size:,} bytes")
