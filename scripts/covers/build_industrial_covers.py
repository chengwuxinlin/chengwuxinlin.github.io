"""Compose LEMA covers from the supplied inspection examples.

Only original source pixels, proportional resizing, and editorial labels are
used. The source's red annotations are retained, not inferred model outputs.
No masks, measurements, predictions, or additional inspection samples are made.
Run from any directory with Python and Pillow installed.
"""

from PIL import Image

from build_research_covers import (
    Canvas, ROOT, OUTPUT, GREEN, LINE, PANEL, checked_image,
)


VIAL_SOURCE_HASH = "a465a03c472db766126be7d7fe663d4aeb4aa57e767b65141a8ce2ce3d3555e6"
HAIR_SOURCE_HASH = "965706db4450c5015209c3efa5fb4ef5a597ff3aba60f667138a6aece8b412c9"
MUTED = "#586650"


def paste_fit(canvas, image, box):
    """Contain the unmodified example within a box without stretching it."""
    x, y, width, height = box
    ratio = min(width / image.width, height / image.height)
    draw_width, draw_height = image.width * ratio, image.height * ratio
    canvas.paste(image, (
        x + (width - draw_width) / 2,
        y + (height - draw_height) / 2,
        draw_width, draw_height,
    ))


def build_vial():
    source = checked_image(ROOT / "images/lema.png", VIAL_SOURCE_HASH)
    c = Canvas()
    c.text(600, 62, "Vial classification", 42)
    c.text(600, 108, "Two classes, subtle visual differences", 25, color=MUTED)

    # The two original labels are reproduced exactly. These are two distinct
    # examples, not a before/after pair, success/failure pair, or model outputs.
    examples = [
        ("Negative", (15, 0, 508, 467), (50, 145, 575, 594)),
        ("Positive", (601, 0, 1093, 467), (625, 145, 1150, 594)),
    ]
    for label, crop, panel in examples:
        left, top, right, bottom = panel
        c.box(panel, fill=PANEL, outline=LINE, radius=16)
        c.text((left + right) / 2, 176, label, 31)
        # Crop away only the old page's duplicate label and whitespace. All
        # relevant vial pixels and red source annotations remain in each crop.
        paste_fit(c, source.crop(crop), (left + 18, 207, right - left - 36, 369))

    c.line([(60, 615), (1140, 615)], color=LINE, width=1)
    c.text(600, 643, "Source examples · original class labels and annotations", 24, color=MUTED)
    c.save("vial-inspection.webp")


def build_hair():
    source = checked_image(ROOT / "images/hair.png", HAIR_SOURCE_HASH)
    c = Canvas()
    c.text(600, 61, "Finding a fine contaminant", 42)
    c.text(300, 131, "Inspection image", 31)
    c.text(941, 131, "Magnified hair strand", 31)
    c.box((43, 170, 576, 596), fill=PANEL, outline=LINE, radius=16)
    c.box((725, 170, 1157, 596), fill=PANEL, outline=LINE, radius=16)

    # A complete overview preserves the source's red arrow and rectangle.
    overview_box = (57, 183, 505, 400)
    paste_fit(c, source, overview_box)

    # This square lies immediately inside the original red rectangle; the
    # curved strand is exactly the one visible in the overview, enlarged only.
    detail_crop = (934, 384, 1283, 733)
    paste_fit(c, source.crop(detail_crop), (747, 190, 388, 388))

    # Editorial connector from the original annotation to its matching detail.
    # It is not an additional detection box or a localization prediction.
    overview_ratio = min(overview_box[2] / source.width, overview_box[3] / source.height)
    overview_left = overview_box[0] + (overview_box[2] - source.width * overview_ratio) / 2
    overview_top = overview_box[1] + (overview_box[3] - source.height * overview_ratio) / 2
    origin = (overview_left + 1294 * overview_ratio, overview_top + 560 * overview_ratio)
    c.line([origin, (610, origin[1]), (610, 384), (688, 384)], color=GREEN, width=2)
    c.arrow((688, 384), (724, 384), color=GREEN, width=2, head=10)
    c.text(647, 422, "Detail", 22, color=MUTED)

    c.line([(60, 615), (1140, 615)], color=LINE, width=1)
    c.text(600, 643, "Same source image · original annotation and magnified detail", 24, color=MUTED)
    c.save("hair-detection.webp")


if __name__ == "__main__":
    build_vial()
    build_hair()
    for name in ("vial-inspection.webp", "hair-detection.webp"):
        path = OUTPUT / name
        print(f"{path.relative_to(ROOT)}: {Image.open(path).size}, {path.stat().st_size:,} bytes")
