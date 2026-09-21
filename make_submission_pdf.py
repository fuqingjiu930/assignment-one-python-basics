# -*- coding: utf-8 -*-
"""Build the Assignment 1 submission report as a real, selectable-text PDF.

The HTML is laid out by MuPDF's story engine, so the finished PDF contains a
proper text layer: the words can be selected, copied, searched and read by a
screen reader.  It is not a picture of text.

The report is generated from the .py file that is actually submitted, and the
script refuses to run if the required three-line header is not present.
"""
import os
import re

import pymupdf

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "assignment 1_WangZhihan.py")
OUT_PDF = os.path.join(HERE, "Assignment1_WangZhihan.pdf")

# Put your real repository URL here, then run this script again.
GITHUB_URL = "https://github.com/<YOUR-GITHUB-USERNAME>/assignment-one-python-basics"

# A4, with room left at the bottom for the footer line.
MEDIABOX = pymupdf.paper_rect("a4")
CONTENT_RECT = MEDIABOX + (56, 62, -56, -47)
FOOTER_Y = 815


def esc(text):
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


# --------------------------------------------------------------------------
# 1. Check the submitted file before describing it.
# --------------------------------------------------------------------------
lines = open(SRC, encoding="utf-8").read().splitlines()
expected = ["# Name: Wang Zhihan", "# Assignment One", "# ddl is 22/9/2026 23:59pm"]
for got, want in zip(lines, expected):
    if got != want:
        raise SystemExit("Header mismatch:\n  expected: %r\n  found:    %r" % (want, got))
print("header verified:")
for line in expected:
    print("   ", line)

url_is_placeholder = "YOUR-GITHUB-USERNAME" in GITHUB_URL
if url_is_placeholder:
    print("NOTE: the GitHub URL is still a placeholder - replace GITHUB_URL in")
    print("      this script and run it again before uploading to Moodle.")

# --------------------------------------------------------------------------
# 2. Build the document body as one HTML string (styled, no images).
# --------------------------------------------------------------------------
CSS = """
<style>
  * { font-family: sans-serif; color: #191919; }
  .title    { font-size: 23px; font-weight: bold; color: #0f1e3c; margin: 0 0 3px 0; }
  .subtitle { font-size: 11px; color: #5b6472; margin: 0 0 14px 0; }
  .rule     { border-bottom: 1px solid #c6ccd6; margin: 0 0 14px 0; }
  h2        { font-size: 13.5px; font-weight: bold; color: #14406e;
              margin: 16px 0 5px 0; }
  p         { font-size: 11px; line-height: 1.45; margin: 0 0 8px 0; }
  .kv       { font-size: 11px; line-height: 1.45; margin: 0 0 2px 0; }
  pre       { font-family: monospace; font-size: 8.5px; line-height: 1.4;
              background-color: #f3f4f7; border: 1px solid #d4d8e0;
              padding: 6px 8px; margin: 0 0 8px 0; }
  ul        { margin: 0 0 8px 0; padding-left: 18px; }
  li        { font-size: 11px; line-height: 1.45; margin: 0 0 2px 0; }
  .small    { font-size: 9.5px; color: #6b7280; margin: 0 0 4px 0; }
</style>
"""


def h2(text):
    return "<h2>%s</h2>" % esc(text)


def p(text):
    return "<p>%s</p>" % esc(text)


def kv(text):
    return '<div class="kv">%s</div>' % esc(text)


def ul(items):
    return "<ul>%s</ul>" % "".join("<li>%s</li>" % esc(i) for i in items)


def pre(text):
    return "<pre>%s</pre>" % esc(text)


def small(text):
    return '<div class="small">%s</div>' % esc(text)


RULE = '<div class="rule"></div>'

body = "".join([
    '<div class="title">Assignment One: Python Basics</div>',
    '<div class="subtitle">Edge computing device programming for AI projects</div>',
    RULE,

    h2("Student"),
    kv("Name: Wang Zhihan"),
    kv("Submission file: assignment 1_WangZhihan.py"),
    kv("Deadline: 22/09/2026 11:59pm"),

    h2("GitHub link"),
    kv(GITHUB_URL),

    h2("Description"),
    p("This is my submission for Assignment 1: Python Basics. All three tasks are "
      "implemented in one single Python file, assignment 1_WangZhihan.py, which is "
      "stored in the GitHub repository linked above. The program only uses the "
      "Python standard library, so it runs on the Jetson Nano without installing "
      "anything extra. Starting the file shows a small menu, where each task can "
      "be opened on its own or all three can be run one after another."),

    h2("Task A - Simple Calculator"),
    p("The calculator asks for the first number, the second number and then the "
      "operator (+, -, *, /), and prints the result in a clear form such as "
      "\"Result: 3 + 5 = 8\". A whole expression can also be typed on one line, "
      "for example 3 + 5. Input mistakes are handled instead of stopping the "
      "program:"),
    ul(["dividing by zero prints \"Cannot divide by zero\"",
        "an operator other than + - * / prints \"Invalid operation\"",
        "letters typed where a number is expected are asked for again",
        "a line that is not a proper expression is reported and asked again"]),

    h2("Task B - Question Answering Bot"),
    p("The question is received with input() and the reply is chosen with an "
      "if / elif / else chain. The bot supports the five required keywords:"),
    pre("hello   -> Bot: Hello! Nice to meet you.\n"
        "python  -> Bot: Python is a language, and it is very friendly to beginners.\n"
        "jetson  -> Bot: Jetson Nano is an AI computer made by NVIDIA.\n"
        "ai      -> Bot: AI means Artificial Intelligence.\n"
        "name    -> Bot: My name is Python Bot."),
    p("The matching ignores capital letters and punctuation, so Hello!, PYTHON? "
      "and \"what is AI\" are all understood, and a whole sentence such as "
      "\"Tell me about the JETSON please\" is recognised too. Any other question "
      "gets a friendly \"Sorry, I don't understand.\" reply, and typing bye ends "
      "the conversation."),

    h2("Task C - Turtle Drawing"),
    p("The drawing task uses turtle with for loops, changing colours and changing "
      "lengths. It can draw:"),
    ul(["a square, a triangle and a five-pointed star",
        "a colourful rotating pattern that uses six colours and shrinks each round",
        "a spider web with twelve spokes in eight different colours"]),
    p("The five pictures can be drawn one at a time or all together. When the "
      "drawing is finished, clicking the window returns to the menu."),

    h2("Testing"),
    p("The program was tested before submitting. The calculator was checked with "
      "all four operators, with decimal numbers, with a division by zero and with "
      "wrong input; the bot was checked with the five keywords in upper and lower "
      "case and with unknown questions; and the turtle drawing was checked by "
      "saving the drawing and confirming that all five pictures are produced. The "
      "program did not stop with an error in any of these tests. The checking "
      "script, verify_submission.py, is included in the repository."),

    RULE,
    small("Submitted file: assignment 1_WangZhihan.py    |    "
          "Report: Assignment1_WangZhihan.pdf"),
    small("Required file header: # Name: Wang Zhihan / # Assignment One / "
          "# ddl is 22/9/2026 23:59pm"),
])

html = CSS + body

# --------------------------------------------------------------------------
# 3. Lay the HTML out across A4 pages.
# --------------------------------------------------------------------------
writer = pymupdf.DocumentWriter(OUT_PDF)
story = pymupdf.Story(html=html, em=12)
story.write_stabilized(
    writer,
    lambda positions: html,                                   # content per pass
    lambda rect_num, filled: (MEDIABOX, CONTENT_RECT, pymupdf.Identity),
)
writer.close()

# --------------------------------------------------------------------------
# 4. Add the footer to every page, then save.
# --------------------------------------------------------------------------
doc = pymupdf.open(OUT_PDF)
total = doc.page_count
for number, page in enumerate(doc, start=1):
    page.insert_text(
        (56, FOOTER_Y),
        "Assignment One - Python Basics - Wang Zhihan - page %d of %d"
        % (number, total),
        fontname="helv", fontsize=7.5, color=(0.55, 0.58, 0.63),
    )
doc.subset_fonts()
doc.saveIncr()

# --------------------------------------------------------------------------
# 5. Verify the finished PDF really has a text layer.
# --------------------------------------------------------------------------
doc = pymupdf.open(OUT_PDF)
text = "\n".join(page.get_text() for page in doc)
flat = re.sub(r"\s+", " ", text)
checks = [
    ("opened as A4", abs(doc[0].rect.width - 595) < 2 and abs(doc[0].rect.height - 842) < 2),
    ("has selectable text", len(text) > 1500),
    ("title is text", "Assignment One: Python Basics" in flat),
    ("name is text", "Wang Zhihan" in flat),
    ("GitHub line is text", "github.com" in flat),
    ("calculator text present", "Simple Calculator" in flat),
    ("QA bot text present", "Question Answering Bot" in flat),
    ("turtle text present", "Turtle Drawing" in flat),
    ("keywords list present", "Jetson Nano is an AI computer" in flat),
    ("footer present", "page 1 of" in flat),
]
print()
print("PDF      :", os.path.basename(OUT_PDF), os.path.getsize(OUT_PDF), "bytes")
print("PAGES    :", doc.page_count)
print("TEXT     :", len(text), "characters of real text")
print("FONTS    :", sorted({f[3] for page in doc for f in page.get_fonts()}))
print()
ok = True
for label, passed in checks:
    print("  [%s] %s" % ("PASS" if passed else "FAIL", label))
    ok = ok and passed
print()
print("RESULT:", "ALL CHECKS PASSED" if ok else "SOME CHECKS FAILED")
if url_is_placeholder:
    print("REMINDER: replace the placeholder GitHub URL and run this script again.")
raise SystemExit(0 if ok else 1)
