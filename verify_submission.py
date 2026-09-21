# -*- coding: utf-8 -*-
"""Final verification of the Assignment 1 submission.

Checks the exact file name, the required header, the behaviour of all three
tasks, and the submission PDF.  Exits 0 only when everything passes.
"""
import importlib.util
import io
import os
import re
import sys
import tempfile
from contextlib import redirect_stdout

ROOT = os.path.dirname(os.path.abspath(__file__))
FINAL_PY = os.path.join(ROOT, "assignment 1_WangZhihan.py")
PDF = os.path.join(ROOT, "Assignment1_WangZhihan.pdf")

RESULTS = []


def report(label, ok, detail=""):
    RESULTS.append(ok)
    print("  [%s] %s%s" % ("PASS" if ok else "FAIL", label,
                           ("  -- " + detail) if detail else ""))


def load():
    spec = importlib.util.spec_from_file_location("asg_final", FINAL_PY)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def drive(m, fn, answers):
    queue = list(answers)

    def fake_ask(prompt=""):
        print(prompt, end="")
        if not queue:
            raise EOFError("queue empty")
        return queue.pop(0)

    m.ask = fake_ask
    buf = io.StringIO()
    err = None
    with redirect_stdout(buf):
        try:
            fn(m)
        except Exception as exc:
            err = exc
    return buf.getvalue(), queue, err


print("=" * 70)
print("1. FILE NAME AND HEADER (slide 37 requirements)")
print("=" * 70)
report("file is named exactly 'assignment 1_WangZhihan.py'",
       os.path.basename(FINAL_PY) == "assignment 1_WangZhihan.py")
src = open(FINAL_PY, encoding="utf-8").read()
lines = src.splitlines()
report("line 1 is '# Name: Wang Zhihan'", lines[0] == "# Name: Wang Zhihan", repr(lines[0]))
report("line 2 is '# Assignment One'", lines[1] == "# Assignment One", repr(lines[1]))
report("line 3 is '# ddl is 22/9/2026 23:59pm'",
       lines[2] == "# ddl is 22/9/2026 23:59pm", repr(lines[2]))
report("only the standard library is used",
       "import turtle" in src and "pip install" not in src)

print()
print("=" * 70)
print("2. TASK A - SIMPLE CALCULATOR")
print("=" * 70)
m = load()
out, left, err = drive(m, lambda mm: mm.calculator(),
                       ["7 + 2", "7 - 2", "7 * 2", "7 / 2", "quit"])
report("no crash", err is None, repr(err))
for frag in ["Result: 7 + 2 = 9", "Result: 7 - 2 = 5",
             "Result: 7 * 2 = 14", "Result: 7 / 2 = 3.5"]:
    report("prints %r" % frag, frag in out)
report("all scripted answers consumed", not left, repr(left))

m = load()
out, left, err = drive(m, lambda mm: mm.calculator(),
                       ["x", "8", "3", "-", "quit"])
report("prompts for first number", "Enter first number" in out)
report("prompts for second number", "Enter second number" in out)
report("prompts for the operator", "Choose operation" in out)
report("step-by-step result is correct", "Result: 8 - 3 = 5" in out)
report("all scripted answers consumed", not left, repr(left))

m = load()
out, left, err = drive(m, lambda mm: mm.calculator(),
                       ["5 / 0", "abc + 3", "7 ^ 2", "hello", "3", "abc", "4", "+", "quit"])
report("divide by zero is handled", "Cannot divide by zero" in out)
report("bad format is handled", "Format not understood" in out)
report("bad operator is handled", "Invalid operation" in out)
report("non-number is handled", "That is not a number" in out)
report("recovers and still computes", "Result: 3 + 4 = 7" in out)
report("no crash", err is None, repr(err))

print()
print("=" * 70)
print("3. TASK B - QA BOT")
print("=" * 70)
m = load()
out, left, err = drive(m, lambda mm: mm.qa_bot(),
                       ["hello", "python", "jetson", "ai", "name", "bye"])
report("no crash", err is None, repr(err))
for frag in ["Hello! Nice to meet you.", "Python is a language",
             "Jetson Nano is an AI computer", "AI means Artificial Intelligence",
             "My name is Python Bot."]:
    report("answers %r" % frag, frag in out)
report("at least 5 keywords defined", len(m.KEYWORDS) >= 5, str(m.KEYWORDS))
report("uses if/elif/else logic", "elif" in src and "else" in src)
report("uses input()", "input(" in src)

m = load()
out, left, err = drive(m, lambda mm: mm.qa_bot(),
                       ["Hello!", "PYTHON?", "Tell me about the JETSON please",
                        "what is AI", "banana", "bye"])
report("handles capital letters and punctuation",
       "Hello! Nice to meet you." in out and "Python is a language" in out)
report("handles a full sentence", "Jetson Nano is an AI computer" in out)
report("handles an unknown question", "Sorry, I don't understand" in out)
report("no crash", err is None, repr(err))

print()
print("=" * 70)
print("4. TASK C - TURTLE DRAWING")
print("=" * 70)
m = load()
tmp = tempfile.mkdtemp()
old_cwd = os.getcwd()
err = None
buf = io.StringIO()
try:
    os.chdir(tmp)
    with redirect_stdout(buf):
        m.turtle_drawing(mode="demo")
except Exception as exc:
    err = exc
finally:
    os.chdir(old_cwd)
report("draws without crashing", err is None, repr(err))
eps = os.path.join(tmp, "turtle_drawing.eps")
report("produces a drawing file", os.path.exists(eps))
if os.path.exists(eps):
    raw = open(eps, errors="replace").read()
    segments = len(re.findall(r"\blineto\b", raw)) + len(re.findall(r"\bcurveto\b", raw))
    colours = set(re.findall(r"[\d.]+ [\d.]+ [\d.]+ setrgbcolor", raw))
    report("draws many segments", segments > 40, "%d segments" % segments)
    report("uses multiple colours", len(colours) >= 6, "%d colours" % len(colours))
report("has square / triangle / star / pattern / web functions",
       all(hasattr(m, n) for n in ("draw_square", "draw_triangle", "draw_star",
                                   "draw_rainbow_pattern", "draw_spider_web")))
report("uses for loops", src.count("for ") >= 6)

print()
print("=" * 70)
print("5. SUBMISSION PDF")
print("=" * 70)
report("PDF exists", os.path.exists(PDF),
       "%d bytes" % os.path.getsize(PDF) if os.path.exists(PDF) else "")
try:
    import pymupdf
    doc = pymupdf.open(PDF)
    p = doc[0]
    report("PDF opens", True, "%d page(s)" % doc.page_count)
    report("is A4 size", abs(p.rect.width - 595) < 3 and abs(p.rect.height - 841) < 3,
           "%.0f x %.0f pt" % (p.rect.width, p.rect.height))
except Exception as exc:
    report("PDF opens", False, repr(exc))

print()
print("=" * 70)
passed = sum(1 for r in RESULTS if r)
print("SUMMARY: %d/%d checks passed" % (passed, len(RESULTS)))
print("=" * 70)
sys.exit(0 if passed == len(RESULTS) else 1)
