# -*- coding: utf-8 -*-
"""Build the Assignment 1 submission PDF with Pillow (A4, multi-page)."""
import os
import re
import shutil

from PIL import Image, ImageDraw, ImageFont

SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assignment 1_WangZhihan.py")
FINAL = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assignment 1_WangZhihan.py")
OUT_PDF = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Assignment1_WangZhihan.pdf")

GITHUB_LINE = (
    "GitHub link : https://github.com/<YOUR-GITHUB-USERNAME>/"
    "assignment-one-python-basics"
)

# ---------------------------------------------------------------- fonts
def pick_font(candidates, size):
    for path in candidates:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except Exception:
                pass
    return ImageFont.load_default()


SANS = [r"C:\Windows\Fonts\arial.ttf", r"C:\Windows\Fonts\calibri.ttf",
        r"C:\Windows\Fonts\segoeui.ttf", r"C:\Windows\Fonts\DejaVuSans.ttf"]
SANS_B = [r"C:\Windows\Fonts\arialbd.ttf", r"C:\Windows\Fonts\calibrib.ttf",
          r"C:\Windows\Fonts\segoeuib.ttf", r"C:\Windows\Fonts\DejaVuSans-Bold.ttf"]
MONO = [r"C:\Windows\Fonts\consola.ttf", r"C:\Windows\Fonts\cour.ttf",
        r"C:\Windows\Fonts\DejaVuSansMono.ttf"]
MONO_B = [r"C:\Windows\Fonts\consolab.ttf", r"C:\Windows\Fonts\courbd.ttf"]

F_TITLE = pick_font(SANS_B, 40)
F_H1 = pick_font(SANS_B, 25)
F_H2 = pick_font(SANS_B, 20)
F_BODY = pick_font(SANS, 16)
F_BODY_B = pick_font(SANS_B, 16)
F_MONO = pick_font(MONO, 15)
F_MONO_B = pick_font(MONO_B, 15)
F_SMALL = pick_font(SANS, 13)

# ---------------------------------------------------------------- canvas
DPI = 150
A4 = (int(8.27 * DPI), int(11.69 * DPI))          # 1240 x 1753
MARGIN = 96
LINE = 8

pages = []
def new_page():
    img = Image.new("RGB", A4, "white")
    pages.append((img, ImageDraw.Draw(img)))
    return pages[-1]

def text_w(draw, s, font):
    return draw.textlength(s, font=font)

def wrap(draw, text, font, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if text_w(draw, trial, font) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

CUR = {"img": None, "d": None, "y": 0}

def start_page():
    img, d = new_page()
    CUR["img"], CUR["d"], CUR["y"] = img, d, MARGIN

def space(h):
    CUR["y"] += h

def need(h):
    if CUR["y"] + h > A4[1] - MARGIN:
        start_page()

def style_of(style):
    return {
        "title": (F_TITLE, (15, 30, 60)),
        "h1": (F_H1, (15, 30, 60)),
        "h2": (F_H2, (20, 60, 110)),
        "body": (F_BODY, (25, 25, 25)),
        "bullet": (F_BODY, (25, 25, 25)),
        "mono": (F_MONO, (10, 10, 10)),
        "small": (F_SMALL, (90, 90, 90)),
    }[style]

def emit(style, text, indent=0, gap_after=LINE, color=None, bold=False):
    font, col = style_of(style)
    if bold:
        font = pick_font(SANS_B, font.size)
    if color:
        col = color
    max_w = A4[0] - 2 * MARGIN - indent
    lines = wrap(CUR["d"], text, font, max_w)
    lh = int(font.size * 1.45)
    need(lh * len(lines) + gap_after)
    for ln in lines:
        CUR["d"].text((MARGIN + indent, CUR["y"]), ln, font=font, fill=col)
        CUR["y"] += lh
    CUR["y"] += gap_after

def emit_bullet(text, indent=24, gap_after=6):
    font, col = style_of("bullet")
    bullet = "\u2022  "
    max_w = A4[0] - 2 * MARGIN - indent - 20
    lines = wrap(CUR["d"], text, font, max_w)
    lh = int(font.size * 1.45)
    need(lh * len(lines) + gap_after)
    CUR["d"].text((MARGIN + indent, CUR["y"]), bullet, font=font, fill=col)
    for ln in lines:
        CUR["d"].text((MARGIN + indent + 22, CUR["y"]), ln, font=font, fill=col)
        CUR["y"] += lh
    CUR["y"] += gap_after

def emit_code(text, indent=24):
    font, col = style_of("mono")
    lines = text.split("\n")
    lh = int(font.size * 1.45)
    h = lh * len(lines) + 16
    need(h)
    top = CUR["y"] - 4
    CUR["d"].rectangle(
        [MARGIN + indent - 10, top, A4[0] - MARGIN - 10, top + h],
        fill=(243, 244, 247), outline=(210, 214, 222))
    y = top + 8
    for ln in lines:
        CUR["d"].text((MARGIN + indent, y), ln, font=font, fill=col)
        y += lh
    CUR["y"] = top + h + LINE

def emit_rule():
    need(20)
    CUR["d"].line([MARGIN, CUR["y"], A4[0] - MARGIN, CUR["y"]],
                  fill=(200, 205, 215), width=2)
    CUR["y"] += 18

# ---------------------------------------------------------------- rename file
if os.path.exists(FINAL):
    os.remove(FINAL)
shutil.copyfile(SRC, FINAL)
print("FINAL FILE :", os.path.basename(FINAL), os.path.getsize(FINAL), "bytes")

header = "\n".join(open(FINAL, encoding="utf-8").read().splitlines()[:3])
print("HEADER     :", header.replace("\n", " | "))
for want in ("# Name: Wang Zhihan", "# Assignment One", "# ddl is 22/9/2026 23:59pm"):
    print("  header has %-32s %s" % (want, want in header))

# ---------------------------------------------------------------- content
start_page()

emit("title", "Assignment One: Python Basics", gap_after=4)
emit("small", "Edge computing device programming for AI projects", gap_after=18)
emit_rule()

emit("h2", "Student", gap_after=4)
emit("body", "Name: Wang Zhihan", gap_after=2)
emit("body", "Deadline: 22/09/2026 11:59pm", gap_after=16)

emit("h2", "GitHub link", gap_after=4)
emit("mono", GITHUB_LINE, gap_after=16)

emit("h2", "Description", gap_after=6)
emit("body",
     "This is my submission for Assignment 1: Python Basics. All three tasks are "
     "implemented in one single Python file, assignment 1_WangZhihan.py, which is "
     "uploaded to the GitHub repository linked above. The program only uses the "
     "Python standard library, so it runs on the Jetson Nano with no extra "
     "installation. When the file is started it shows a small menu, and each task "
     "can be opened on its own or all three can be run one after another.",
     gap_after=14)

emit("h2", "Task A - Simple Calculator", gap_after=4)
emit("body",
     "The calculator asks for the first number, the second number and then the "
     "operator (+, -, *, /), and prints the result in a clear form such as "
     "\"Result: 3 + 5 = 8\". It also accepts a whole expression typed on one line, "
     "for example 3 + 5. Input errors are handled instead of crashing the program:",
     gap_after=6)
emit_bullet("dividing by zero prints \"Cannot divide by zero\"")
emit_bullet("an operator other than + - * / prints \"Invalid operation\"")
emit_bullet("letters typed where a number is expected are asked for again")
emit_bullet("a line that is not a proper expression is reported and asked again")

emit("h2", "Task B - Question Answering Bot", gap_after=4)
emit("body",
     "The bot receives the question with input() and chooses the reply with an "
     "if / elif / else chain. It supports the five required keywords:",
     gap_after=6)
emit_code("hello   -> Bot: Hello! Nice to meet you.\n"
          "python  -> Bot: Python is a language, and it is very friendly to beginners.\n"
          "jetson  -> Bot: Jetson Nano is an AI computer made by NVIDIA.\n"
          "ai      -> Bot: AI means Artificial Intelligence.\n"
          "name    -> Bot: My name is Python Bot.")
emit("body",
     "The matching ignores capital letters and punctuation, so Hello!, PYTHON? and "
     "\"what is AI\" are all understood. Any other question is answered with a "
     "friendly \"Sorry, I don't understand.\", and typing bye ends the conversation.",
     gap_after=14)

emit("h2", "Task C - Turtle Drawing", gap_after=4)
emit("body",
     "The drawing task uses turtle with for loops, changing colours and changing "
     "lengths. It can draw:", gap_after=6)
emit_bullet("a square, a triangle and a five-pointed star")
emit_bullet("a colourful rotating pattern that uses six colours and shrinks each round")
emit_bullet("a spider web with twelve spokes in eight different colours")
emit("body",
     "The five pictures can be drawn one by one or all together. When the drawing "
     "is finished, clicking the window returns to the menu.",
     gap_after=14)

emit("h2", "Testing", gap_after=4)
emit("body",
     "I tested the program before submitting. The calculator was checked with all "
     "four operators, with decimal numbers, with a division by zero and with wrong "
     "input; the bot was checked with the five keywords in upper and lower case and "
     "with unknown questions; and the turtle drawing was checked by saving the "
     "drawing and confirming that all five pictures are produced. The program did "
     "not stop with an error in any of these tests.",
     gap_after=14)

emit_rule()
emit("small",
     "File submitted: assignment 1_WangZhihan.py        "
     "Report: Assignment1_WangZhihan.pdf")

# ---------------------------------------------------------------- save
pages[0][0].save(OUT_PDF, "PDF", resolution=DPI, save_all=True,
                append_images=[p[0] for p in pages[1:]])
print("PDF        :", os.path.basename(OUT_PDF), os.path.getsize(OUT_PDF), "bytes")
print("PAGES      :", len(pages))
