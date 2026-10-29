#!/usr/bin/env python3
"""Compose the avatar cover from authentic frames of the existing project demo.

Requires Pillow and ffmpeg. The source video is deliberately kept in ignored
.local/cover-sources, not bundled with the website. See the provenance note there.
No frames are generated, recolored, retouched, or represented as input portraits.
"""

from argparse import ArgumentParser
from io import BytesIO
from pathlib import Path
import os
import shutil
import subprocess

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[2]
SIZE = (1200, 675)
BACKGROUND = "#eeeee6"
FOREST = "#234b3e"
SAGE = "#9baa91"
INK = "#242c27"
TIMES = (0.0, 1.0, 3.0)


def font(size, semibold=False):
    windows = Path(os.environ.get("WINDIR", "C:/Windows")) / "Fonts"
    candidates = [
        windows / ("seguisb.ttf" if semibold else "segoeui.ttf"),
        Path("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"),
    ]
    for candidate in candidates:
        if candidate.is_file():
            return ImageFont.truetype(str(candidate), size)
    raise FileNotFoundError("Install Segoe UI or DejaVu Sans before rendering.")


def find_ffmpeg():
    executable = shutil.which("ffmpeg")
    if executable:
        return executable
    scoop = Path.home() / "scoop/apps/ffmpeg/current/bin/ffmpeg.exe"
    if scoop.is_file():
        return str(scoop)
    raise FileNotFoundError("ffmpeg is required to extract source video frames.")


def frame_at(executable, video, seconds):
    result = subprocess.run(
        [executable, "-v", "error", "-ss", str(seconds), "-i", str(video),
         "-frames:v", "1", "-f", "image2pipe", "-vcodec", "png", "-"],
        check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
    )
    return Image.open(BytesIO(result.stdout)).convert("RGB")


def build(source, output):
    if not source.is_file():
        raise FileNotFoundError(
            "Expected the existing project demo at " + str(source)
            + ". Obtain the approved source before building; do not substitute generated frames."
        )
    executable = find_ffmpeg()
    frames = [frame_at(executable, source, seconds) for seconds in TIMES]
    canvas = Image.new("RGB", SIZE, BACKGROUND)
    draw = ImageDraw.Draw(canvas)

    draw.text((60, 59), "Real-time talking avatar", font=font(40, True), fill=INK)

    # A small conversational cue, separate from the preserved source frames.
    draw.rounded_rectangle((1057, 62, 1138, 113), radius=11, outline=FOREST, width=3)
    draw.line([(1071, 112), (1071, 126), (1087, 113)], fill=FOREST, width=3)
    for x in (1079, 1098, 1117):
        draw.ellipse((x - 3, 85, x + 3, 91), fill=FOREST)

    # Full source frames, with no cropping or color processing.
    draw.rounded_rectangle((60, 170, 1140, 550), radius=5, fill=FOREST)
    for x in range(76, 1130, 34):
        draw.rounded_rectangle((x, 177, x + 14, 186), radius=2, fill=BACKGROUND)
        draw.rounded_rectangle((x, 534, x + 14, 543), radius=2, fill=BACKGROUND)
    for x, frame in zip((80, 435, 790), frames):
        canvas.paste(frame.resize((330, 330), Image.Resampling.LANCZOS), (x, 195))

    draw.text((60, 588), "Expression, frame by frame", font=font(36), fill=FOREST)
    # The horizontal sequence signifies motion without inventing an audio trace.
    draw.line((959, 615, 1137, 615), fill=SAGE, width=3)
    draw.line((1123, 605, 1137, 615, 1123, 625), fill=FOREST, width=3)

    output.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(output, "WEBP", quality=90, method=6)
    print(f"Saved {output.relative_to(ROOT) if output.is_relative_to(ROOT) else output}")
    print(f"{SIZE[0]} x {SIZE[1]}, {output.stat().st_size:,} bytes; source frames: {TIMES} s")


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=ROOT / ".local/cover-sources/avatar-demo.mp4")
    parser.add_argument("--output", type=Path, default=ROOT / "assets/images/covers/avatars.webp")
    args = parser.parse_args()
    build(args.source.resolve(), args.output.resolve())
