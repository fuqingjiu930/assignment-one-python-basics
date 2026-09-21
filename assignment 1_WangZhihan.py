# Name: Wang Zhihan
# Assignment One
# ddl is 22/9/2026 23:59pm
#
# ELEC7023 / Edge computing device programming for AI projects
# Assignment 1: Python Basics  --  Task A Calculator, Task B QA Bot, Task C Turtle Drawing
#
# How to run on the Jetson Nano:
#     cd ~/Desktop
#     python3 assignment1_WangZhihan.py
# Then choose 1 / 2 / 3 in the menu, or 4 to run all three tasks one by one.

import time

try:
    import turtle          # Task C uses Python's built-in turtle graphics
except Exception:          # on a machine without a display / Tk, keep the rest working
    turtle = None

# ---------------------------------------------------------------------------
# Task A: Simple Calculator
# ---------------------------------------------------------------------------
def calculate(num1, num2, op):
    """Return the result of num1 <op> num2.

    Returns None when the operator is invalid, or the string 'Error'
    when the user tries to divide by zero.
    """
    if op == "+":
        return num1 + num2
    elif op == "-":
        return num1 - num2
    elif op == "*":
        return num1 * num2
    elif op == "/":
        if num2 == 0:
            return "Error"
        return num1 / num2
    else:
        return None


def format_number(value):
    """Show 8.0 as '8' but keep 2.5 as '2.5', so the result looks clean."""
    if isinstance(value, float) and value.is_integer():
        return str(int(value))
    return str(value)


def ask(prompt):
    """input() that returns None instead of crashing when the input ends.

    Typing interactively this behaves exactly like input().  It only matters
    if the input is piped in or closed early, where the program should stop
    politely instead of showing a traceback.
    """
    try:
        return input(prompt)
    except EOFError:
        print()
        print("Input closed, goodbye!")
        return None


def read_number(prompt):
    """Ask until the user really types a number."""
    while True:
        text = ask(prompt)
        if text is None:
            return None
        try:
            return float(text.strip())
        except ValueError:
            print("  -> That is not a number, please try again.")


def calculator():
    print("=" * 50)
    print("Task A: Simple Calculator")
    print("=" * 50)
    while True:
        print()
        print("Type your calculation in one line, for example:  3 + 5")
        print("(you can also write 'quit' to leave the calculator)")
        line = ask("Enter calculation: ")
        if line is None:
            return
        line = line.strip()

        if line.lower() in ("quit", "q", "exit", "back"):
            print("Calculator closed.")
            return

        # Let the user type the whole expression in one line.
        parts = line.split()
        if len(parts) == 3:
            try:
                num1 = float(parts[0])
                num2 = float(parts[2])
                op = parts[1]
            except ValueError:
                print("  -> Format not understood. Please use: <number> <operator> <number>")
                continue
        else:
            # Otherwise ask for the three pieces one by one.
            print("  -> Please enter the three parts step by step.")
            num1 = read_number("Enter first number : ")
            if num1 is None:
                return
            num2 = read_number("Enter second number: ")
            if num2 is None:
                return
            raw_op = ask("Choose operation (+, -, *, /): ")
            if raw_op is None:
                return
            op = raw_op.strip()

        result = calculate(num1, num2, op)
        if result is None:
            print("  -> Invalid operation, please use one of + - * /")
        elif result == "Error":
            print("  -> Cannot divide by zero")
        else:
            print("Result: %s %s %s = %s"
                  % (format_number(num1), op, format_number(num2), format_number(result)))


# ---------------------------------------------------------------------------
# Task B: QA Bot  (at least 5 keywords: hello, python, jetson, ai, name)
# ---------------------------------------------------------------------------
KEYWORDS = ["hello", "python", "jetson", "ai", "name"]

ANSWERS = {
    "hello": "Bot: Hello! Nice to meet you.",
    "python": "Bot: Python is a language, and it is very friendly to beginners.",
    "jetson": "Bot: Jetson Nano is an AI computer made by NVIDIA.",
    "ai": "Bot: AI means Artificial Intelligence.",
    "name": "Bot: My name is Python Bot.",
}

EXACT_ANSWERS = [
    (["what is your name", "what's your name", "your name"],
     "Bot: My name is Python Bot."),
    (["who are you"],
     "Bot: I am a small question-answering bot written in Python."),
    (["how are you"],
     "Bot: I am fine, thank you for asking!"),
]


def clean_text(text):
    """Lower the text and drop punctuation, so 'Hello!' still matches 'hello'."""
    lowered = text.lower()
    cleaned = ""
    for ch in lowered:
        if ch.isalnum() or ch == " ":
            cleaned += ch
        else:
            cleaned += " "
    return cleaned.strip()


def qa_bot():
    print("=" * 50)
    print("Task B: Question Answering Bot")
    print("=" * 50)
    print("Keywords I know: " + ", ".join(KEYWORDS))
    print("(type 'bye' to stop talking to the bot)")
    while True:
        question = ask("Ask me something: ")
        if question is None:
            return
        question = question.strip()
        if question == "":
            print("Bot: Please type something so I can answer you.")
            continue

        cleaned = clean_text(question)
        if cleaned in ("bye", "quit", "exit", "q"):
            print("Bot: Goodbye! See you next time.")
            return

        answer = None

        # 1) The most specific questions first.
        for phrases, reply in EXACT_ANSWERS:
            for phrase in phrases:
                if phrase in cleaned:
                    answer = reply
                    break
            if answer is not None:
                break

        # 2) Then look for the required keywords.
        if answer is None:
            words = cleaned.split()
            for keyword in KEYWORDS:
                if keyword in words:
                    answer = ANSWERS[keyword]
                    break

        if answer is None:
            answer = "Bot: Sorry, I don't understand. Please try: " + ", ".join(KEYWORDS)
        print(answer)


# ---------------------------------------------------------------------------
# Task C: Turtle Drawing  (square, triangle, star, colourful pattern, random)
# ---------------------------------------------------------------------------
def draw_square(size):
    for _ in range(4):
        turtle.forward(size)
        turtle.left(90)


def draw_triangle(size):
    for _ in range(3):
        turtle.forward(size)
        turtle.left(120)


def draw_star(size):
    for _ in range(5):
        turtle.forward(size)
        turtle.right(144)


def draw_rainbow_pattern(size):
    colors = ["red", "orange", "yellow", "green", "blue", "purple"]
    for i in range(6):
        turtle.pencolor(colors[i])
        for _ in range(4):
            turtle.forward(size)
            turtle.left(90)
        turtle.left(60)
        size = size * 0.75


def draw_spider_web(turns):
    colors = ["HotPink", "OrangeRed", "Gold", "LimeGreen",
              "DodgerBlue", "MediumPurple", "DeepSkyBlue", "Crimson"]
    turtle.pensize(2)
    for i in range(turns):
        turtle.pencolor(colors[i % len(colors)])
        turtle.forward(300)
        turtle.backward(300)
        turtle.left(360 / turns)


def turtle_drawing(mode="interactive"):
    if turtle is None:
        print("turtle is not available on this computer.")
        return

    print("=" * 50)
    print("Task C: Turtle Drawing")
    print("=" * 50)
    print("A window will open and draw:")
    print("  1. a square   2. a triangle   3. a star")
    print("  4. a colourful rotating pattern   5. a spider web")

    if mode == "demo":
        # Used for an automatic test run (no keyboard needed).
        choices = [1, 2, 3, 4, 5]
    else:
        raw = ask("Choose 1-5 (or press Enter to draw all): ")
        if raw is None:
            return
        raw = raw.strip()
        if raw == "":
            choices = [1, 2, 3, 4, 5]
        elif raw in ("1", "2", "3", "4", "5"):
            choices = [int(raw)]
        else:
            print("  -> Not a valid choice, I will draw all of them.")
            choices = [1, 2, 3, 4, 5]

    turtle.speed(0)          # fastest drawing speed
    turtle.bgcolor("black")
    turtle.pensize(3)
    turtle.penup()
    turtle.goto(-150, 100)
    turtle.pendown()

    for choice in choices:
        if choice == 1:
            turtle.pencolor("cyan")
            turtle.write("Square", font=("Arial", 12, "bold"))
            draw_square(120)
            turtle.penup()
            turtle.forward(200)
            turtle.pendown()

        elif choice == 2:
            turtle.pencolor("yellow")
            turtle.write("Triangle", font=("Arial", 12, "bold"))
            draw_triangle(120)
            turtle.penup()
            turtle.forward(200)
            turtle.pendown()

        elif choice == 3:
            turtle.pencolor("lime")
            turtle.write("Star", font=("Arial", 12, "bold"))
            draw_star(140)
            turtle.penup()
            turtle.forward(200)
            turtle.pendown()

        elif choice == 4:
            turtle.pencolor("white")
            turtle.write("Pattern", font=("Arial", 12, "bold"))
            draw_rainbow_pattern(120)
            turtle.penup()
            turtle.forward(250)
            turtle.pendown()

        elif choice == 5:
            turtle.pencolor("white")
            turtle.write("Web", font=("Arial", 12, "bold"))
            draw_spider_web(12)
            turtle.penup()
            turtle.forward(250)
            turtle.pendown()

    turtle.hideturtle()

    if mode == "demo":
        print("Demo drawing finished. Saving screenshot and closing the window.")
        try:
            canvas = turtle.getcanvas()
            canvas.postscript(file="turtle_drawing.eps")
            print("Vector copy saved as turtle_drawing.eps")
        except Exception as err:
            print("Could not save the EPS copy:", err)
        time.sleep(1)
        try:
            turtle.bye()
        except Exception:
            pass
        return

    print()
    print("The drawing is finished. Close the turtle window (or press any key in it)")
    print("to come back to the menu.")
    try:
        turtle.Screen().exitonclick()
    except Exception:
        pass


# ---------------------------------------------------------------------------
# Menu
# ---------------------------------------------------------------------------
def run_all():
    calculator()
    print()
    qa_bot()
    print()
    turtle_drawing()


def main():
    print()
    print("##################################################")
    print("#  Assignment 1: Python Basics                   #")
    print("#  Name: Wang Zhihan                             #")
    print("##################################################")
    while True:
        print()
        print("Please choose a task:")
        print("  1. Task A - Simple Calculator")
        print("  2. Task B - Question Answering Bot")
        print("  3. Task C - Turtle Drawing")
        print("  4. Run all three tasks")
        print("  5. Quit")
        choice = ask("Your choice (1-5): ")
        if choice is None:
            break
        choice = choice.strip()

        if choice == "1":
            calculator()
        elif choice == "2":
            qa_bot()
        elif choice == "3":
            turtle_drawing()
        elif choice == "4":
            run_all()
        elif choice in ("5", "q", "quit", "exit"):
            print("Bye! Thanks for using this program.")
            break
        else:
            print("  -> Please type a number from 1 to 5.")


if __name__ == "__main__":
    main()
