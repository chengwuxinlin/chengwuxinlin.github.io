"""Compose the two conceptual covers; no industrial data or measured results.

Requires Pillow. Wafer art is generated with the built-in image tool and retained
privately at .local/cover-sources/wafer-illustration.png. Spectra are deliberately
synthetic diagram geometry, not sampled, fitted, or claimed experimental data.
"""
from pathlib import Path
import math
import random
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'assets/images/covers'
OUT.mkdir(parents=True, exist_ok=True)
S = 2
PAPER = '#eeeee6'
INK = '#242c27'
GREEN = '#234b3e'
SAGE = '#91a58e'
OCHRE = '#ae7c36'
MUTED = '#626a61'


def font(size, bold=False):
    return ImageFont.truetype('C:/Windows/Fonts/segoeuib.ttf' if bold else 'C:/Windows/Fonts/segoeui.ttf', size*S)


def text(draw, xy, value, size=36, fill=GREEN, bold=False, anchor=None):
    draw.text(tuple(int(v*S) for v in xy), value, font=font(size,bold), fill=fill, anchor=anchor)


def line(draw, points, fill=GREEN, width=2):
    draw.line([(round(x*S),round(y*S)) for x,y in points],fill=fill,width=round(width*S),joint='curve')


def rect(draw, box, fill, outline=None, width=1, radius=0):
    draw.rounded_rectangle([round(v*S) for v in box],radius=radius*S,fill=fill,outline=outline,width=width*S)


def save(im,name):
    im.resize((1200,675),Image.Resampling.LANCZOS).save(OUT/name,format='WEBP',quality=93,method=6)


# Preserve the image/mask pairing supplied by the generated illustration.
wafer = Image.open(ROOT/'.local/cover-sources/wafer-illustration.png').convert('RGB').resize((1200*S,675*S),Image.Resampling.LANCZOS)
d = ImageDraw.Draw(wafer)
text(d,(324,48),'Wafer image',38,anchor='mt')
text(d,(876,48),'Particle mask',38,anchor='mt')
text(d,(600,594),'Find the particles. Preserve their boundaries.',30,fill=MUTED,anchor='mt')
save(wafer,'wafer-segmentation.webp')


# A method diagram: noise and conditioning are transformed into new spectra.
# The analytic curves below only illustrate the concept; they have no units.
im = Image.new('RGB',(1200*S,675*S),PAPER)
d = ImageDraw.Draw(im)
text(d,(255,48),'Noise + conditions',38,anchor='mt')
text(d,(928,48),'Synthetic spectra',38,anchor='mt')
rect(d,(65,154,446,505),'#f7f7f1',outline='#ccd4c5',radius=8)
rect(d,(737,154,1120,505),'#f7f7f1',outline='#ccd4c5',radius=8)
rng = random.Random(27)
for row,(color,opacity) in enumerate([(GREEN,1),(SAGE,1),(OCHRE,1)]):
    y = 224 + row*105
    line(d,[(87,y),(424,y)],fill='#dce0d5',width=1)
    points = [(89+i*2.35,y+rng.uniform(-28,28)) for i in range(142)]
    line(d,points,fill=color,width=2.3)
    points = []
    for i in range(230):
        x=i/229
        value=(.32*math.exp(-((x-.2-.025*row)/.07)**2)
            +.78*math.exp(-((x-.51+.018*row)/.055)**2)
            +.43*math.exp(-((x-.77-.014*row)/.11)**2))
        points.append((760+x*337,y+22-value*72))
    line(d,[(759,y+22),(1098,y+22)],fill='#dce0d5',width=1)
    line(d,points,fill=color,width=3.4)

line(d,[(474,325),(708,325)],GREEN,2)
line(d,[(696,313),(708,325),(696,337)],GREEN,2)
rect(d,(492,281,691,367),PAPER)
text(d,(592,292),'Diffusion',32,anchor='mt')
text(d,(592,335),'model',28,fill=MUTED,anchor='mt')
for i,w in enumerate([54,80,39]):
    x=145+i*92
    rect(d,(x,535,x+72,541),'#c6cebf',radius=3)
    d.ellipse(((x+w*.65)*S,527*S,(x+w*.65+17)*S,549*S),fill=GREEN)
text(d,(928,531),'New samples',28,fill=MUTED,anchor='mt')
text(d,(600,609),'Generate data for changing conditions.',30,fill=MUTED,anchor='mt')
save(im,'spectral-diffusion.webp')
print('Wrote wafer-segmentation.webp and spectral-diffusion.webp')
