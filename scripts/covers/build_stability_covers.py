"""Build conceptual SALMAN and SAGMAN covers in the site's shared visual style.

All positions, text examples, and graph relationships below are explanatory
illustrations. They are not model outputs, measured embeddings, or paper figures.
Primary concept sources:
  SALMAN: https://arxiv.org/abs/2508.18306
  SAGMAN: https://arxiv.org/abs/2402.08653

Run with Python and Pillow. No downloads or private data are required.
"""

from math import hypot

from build_research_covers import Canvas, GREEN, INK, LINE, OCHRE, PANEL, PAPER, SAGE


MUTED = "#67725f"
PALE_OCHRE = "#eae0cc"
PALE_GREEN = "#e2e7dc"


def dashed(c, start, end, color=SAGE, width=2, dash=7, gap=7):
    dx, dy = end[0] - start[0], end[1] - start[1]
    length = hypot(dx, dy)
    distance = 0
    while distance < length:
        stop = min(distance + dash, length)
        c.line([(start[0] + dx * distance / length, start[1] + dy * distance / length),
                (start[0] + dx * stop / length, start[1] + dy * stop / length)], color, width)
        distance += dash + gap


def footer(c, message):
    c.line([(60, 571), (1140, 571)], LINE, 1)
    c.text(60, 608, message, 29, GREEN, anchor="lm")
    c.text(1140, 646, "Method illustration", 23, MUTED, anchor="rm")


def letter_node(c, x, y, letter, color=GREEN, radius=23):
    c.circle(x, y, radius, PAPER, color, 2.8)
    c.text(x, y - 1, letter, 26, color, bold=True)


def model_box(c, label, x=600, y=330):
    c.box((x - 72, y - 55, x + 72, y + 55), PANEL, LINE, radius=19, width=1.5)
    # Quiet stacked strokes read as a computational layer without inventing
    # a scientific architecture or relying on an ambiguous decorative icon.
    for offset in (-12, 0, 12):
        c.line([(x - 29, y - 24 + offset), (x + 29, y - 24 + offset)], SAGE, 2)
    c.text(x, y + 23, label, 31, GREEN, bold=True)


def build_salman():
    c = Canvas()
    c.text(242, 79, "Text variants", 38)
    c.text(930, 79, "Output relationships", 38)

    # Two explicitly illustrative wording variants; no model response is shown.
    for y, label, article, color in [(234, "A", "the", GREEN), (407, "B", "this", OCHRE)]:
        c.box((65, y - 66, 423, y + 66), PANEL, LINE, radius=17)
        letter_node(c, 109, y, label, color, radius=22)
        c.text(158, y - 24, "Explain", 34, INK, anchor="lm")
        c.text(158, y + 24, article, 34, color, anchor="lm", bold=True)
        width = 57 if article == "the" else 66
        c.text(158 + width + 12, y + 24, "result.", 34, INK, anchor="lm")
    c.text(244, 517, "Small wording change", 28, MUTED)

    # Both variants enter the same language-model stage.
    c.line([(439, 234), (473, 234), (473, 330)], SAGE, 2)
    c.line([(439, 407), (473, 407), (473, 330)], SAGE, 2)
    c.arrow((473, 330), (514, 330), GREEN, 2.5, head=10)
    model_box(c, "LLM")
    c.arrow((687, 330), (739, 330), GREEN, 2.5, head=10)

    # Relationships are schematic. The amber variant is intentionally displaced
    # to explain distortion; no distance scale or actual prediction is implied.
    nodes = [(794, 263), (817, 412), (873, 194), (887, 333),
             (959, 251), (973, 419), (1050, 366)]
    edges = [(0, 2), (0, 3), (0, 4), (1, 3), (1, 5), (2, 4),
             (3, 4), (3, 5), (4, 6), (5, 6)]
    for a, b in edges:
        c.line([nodes[a], nodes[b]], SAGE, 2)
    for i, (x, y) in enumerate(nodes):
        if i != 3:
            c.circle(x, y, 7, GREEN, PAPER, 1.5)
    letter_node(c, 887, 333, "A")
    # A dashed comparison connects the two selected text samples' relationship.
    dashed(c, (908, 317), (1073, 204), OCHRE, width=2.5)
    c.line([(959, 251), (1091, 192), (1050, 366)], OCHRE, 1.7)
    c.circle(1091, 192, 38, None, "#d7c6a5", 1.3)
    letter_node(c, 1091, 192, "B", OCHRE)
    c.text(939, 517, "Compare sample similarity", 28, MUTED)

    footer(c, "Find language-model inputs with fragile mappings")
    c.save("salman.webp")


def build_sagman():
    c = Canvas()
    c.text(265, 79, "Graph input", 38)
    c.text(932, 79, "Model relationships", 38)

    left = [(104, 268), (189, 192), (290, 223), (406, 288),
            (119, 398), (238, 332), (352, 420)]
    edges = [(0, 1), (0, 4), (0, 5), (1, 2), (1, 5),
             (2, 3), (2, 5), (3, 6), (4, 5), (5, 6)]
    for a, b in edges:
        c.line([left[a], left[b]], SAGE, 2.3)

    # A single changed input edge is highlighted. The plus badge makes the
    # perturbation visible even in a small card, without an ambiguous icon.
    dashed(c, left[4], left[2], OCHRE, width=3, dash=9, gap=7)
    c.circle(195, 319, 18, PALE_OCHRE, OCHRE, 1.5)
    c.line([(187, 319), (203, 319)], OCHRE, 2.4)
    c.line([(195, 311), (195, 327)], OCHRE, 2.4)
    for i, (x, y) in enumerate(left):
        if i == 2:
            letter_node(c, x, y, "A", OCHRE)
        else:
            c.circle(x, y, 10, GREEN, PAPER, 2)
    c.text(265, 517, "Change a connection", 28, MUTED)

    c.arrow((442, 330), (514, 330), GREEN, 2.5, head=10)
    model_box(c, "GNN")
    c.arrow((687, 330), (746, 330), GREEN, 2.5, head=10)

    # Identical node identities and connectivity, with illustrative output
    # coordinates. The changed relationship is a method explanation, not a run.
    right = [(790, 268), (858, 192), (1091, 180), (1086, 288),
             (792, 398), (923, 332), (1035, 420)]
    for a, b in edges:
        color = OCHRE if 2 in (a, b) else SAGE
        c.line([right[a], right[b]], color, 2.3 if color == SAGE else 1.8)
    # Corresponding dashed input edge in the output graph.
    dashed(c, right[4], right[2], OCHRE, width=2, dash=8, gap=7)
    previous = (955, 223)
    c.circle(*previous, 12, PAPER, SAGE, 1.5)
    dashed(c, (971, 218), (1063, 189), OCHRE, 2)
    c.arrow((1035, 198), (1066, 189), OCHRE, 2.4, head=9)
    for i, (x, y) in enumerate(right):
        if i == 2:
            c.circle(x, y, 38, None, "#d7c6a5", 1.3)
            letter_node(c, x, y, "A", OCHRE)
        else:
            c.circle(x, y, 10, GREEN, PAPER, 2)
    c.text(945, 517, "Locate sensitive nodes", 28, MUTED)

    footer(c, "Trace graph changes through a neural network")
    c.save("sagman.webp")


if __name__ == "__main__":
    build_salman()
    build_sagman()
    print("Built salman.webp and sagman.webp (1200 x 675; conceptual illustrations)")
