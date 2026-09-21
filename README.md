# Assignment One — Python Basics

**Name:** Wang Zhihan
**Course:** Edge computing device programming for AI projects
**Deadline:** 22/9/2026 23:59pm

A single-file Python program containing the three tasks of Assignment 1.
It only uses the Python standard library, so it runs on the Jetson Nano with
no installation needed.

## File

| File | Description |
| --- | --- |
| `assignment1_WangZhihan.py` | The whole assignment: Task A, Task B and Task C |

## How to run

On the Jetson Nano (Jetson Nano, Python 3, desktop session needed for Task C):

```bash
cd ~/Desktop
python3 assignment1_WangZhihan.py
```

A menu appears:

```
1. Task A - Simple Calculator
2. Task B - Question Answering Bot
3. Task C - Turtle Drawing
4. Run all three tasks
5. Quit
```

## Task A — Simple Calculator

Prompts for the first number, the second number and then the operator
(`+`, `-`, `*`, `/`), and prints the result.

There are two input styles:

1. **One line** — type `3 + 5` and press Enter.
2. **Step by step** — type a single number/word, and the program then asks
   for first number, second number, operator separately.

Errors are handled instead of crashing:

* dividing by zero prints `Cannot divide by zero`
* a bad operator prints `Invalid operation`
* typing letters where a number is expected asks again

## Task B — Question Answering Bot

Uses `input()` for the question and an `if / elif / else` chain to answer.
It supports the five required keywords:

| Keyword | Answer |
| --- | --- |
| `hello` | Hello! Nice to meet you. |
| `python` | Python is a language, and it is very friendly to beginners. |
| `jetson` | Jetson Nano is an AI computer made by NVIDIA. |
| `ai` | AI means Artificial Intelligence. |
| `name` | My name is Python Bot. |

The matching is case-insensitive and ignores punctuation, so `Hello!`,
`PYTHON?` and `what is AI` all work. Unknown words get a friendly
`Sorry, I don't understand.` reply, and `bye` ends the conversation.

## Task C — Turtle Drawing

Draws five things with `turtle`, using `for` loops, dynamic colours and
changing lengths:

1. a **square**
2. a **triangle**
3. a **star**
4. a **colourful rotating pattern** (six colours, size shrinking each round)
5. a **spider web** (eight colours, 12 spokes)

You can draw one of them or all of them. When the drawing finishes, click the
window to return to the menu. When running automatically the drawing is saved
as `turtle_drawing.eps`.

## Notes

* Task C needs a graphical desktop. On a machine without a display the rest of
  the program still runs, and Task C prints a short message instead of crashing.
* Every function is commented, and the program never exits with a traceback
  even if the input ends early.
