#!/usr/bin/python3

import random
import os
import time
import datetime
import re
from colorama import Fore, Style

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
from pygame import mixer

TIME1_QUESTIONS: list = [
    {"How many hours are in a day?": "24"},
    {"How many hours are in two days?": "48"},
    {"How many days are in a week?": "7"},
    {"How many days are in a two weeks?": "14"},
    {"How many days are in a three weeks?": "21"},
    {"How many days are in a four weeks?": "28"},
    {"How many weeks are in a month?": "4"},
    {"How many months are in a year?": "12"},
    {"How many days are in a leap year?": "366"},
    {"How many days are in a normal year?": "365"},
    {"What is the name of the shortest month of the year?": ["feb", "february"]},
    {"How many hours are in half a day?": "12"},
    {"How many minutes are in an hour?": "60"},
    {"How many seconds are in a minute?": "60"},
]


def escape_ansi(line):
    ansi_escape = re.compile(r'(\x9B|\x1B\[)[0-?]*[ -\/]*[@-~]')
    return ansi_escape.sub('', line)


def play(sound: str) -> None:
    mixer.init()
    mixer.music.load(f"./sounds/{sound}.mp3")
    mixer.music.play()


def time1() -> tuple[list[str], str]:
    problems: list = TIME1_QUESTIONS
    problem: dict = problems[random.randrange(0, len(problems) - 1)]
    question: str = list(problem.keys())[0] + " "
    answers: str | list = list(problem.values())[0]
    answers = answers if isinstance(answers, list) else [answers]
    return answers, question


def addition() -> tuple[str, str]:
    addend1: int = random.randrange(ADD_SUB_MIN_NUMBER, ADD_SUB_MAX_NUMBER)
    result: int = random.randrange(addend1, ADD_SUB_MAX_RESULT)
    addend2 = result - addend1
    problem_text: str = f"{addend1} + {addend2} = "
    return str(result), problem_text


def subtraction() -> tuple[str, str]:
    addend1: int = random.randrange(ADD_SUB_MIN_NUMBER, ADD_SUB_MAX_NUMBER)
    result: int = random.randrange(addend1, ADD_SUB_MAX_RESULT)
    addend2 = result - addend1
    problem_text: str = f"{result} - {addend1} = "
    return str(addend2), problem_text


def multiplication() -> tuple[str, str]:
    multiplier1: int = random.randrange(MUL_DIV_MIN_NUMBER, MUL_DIV_MAX_NUMBER)
    multiplier2: int = random.randrange(MUL_DIV_MIN_NUMBER, MUL_DIV_MAX_NUMBER)
    result: int = multiplier1 * multiplier2
    problem_text: str = f"{multiplier1} * {multiplier2} = "
    return str(result), problem_text


def division() -> tuple[str, str]:
    multiplier1: int = random.randrange(MUL_DIV_MIN_NUMBER, MUL_DIV_MAX_NUMBER)
    multiplier2: int = random.randrange(MUL_DIV_MIN_NUMBER, MUL_DIV_MAX_NUMBER)
    result: int = multiplier1 * multiplier2
    problem_text: str = f"{result} / {multiplier2} = "
    return str(multiplier1), problem_text


def format_time_elapsed(dif: float) -> str:
    hours, rem = divmod(dif, 3600)
    minutes, seconds = divmod(rem, 60)
    return "{:0>2}:{:0>2}:{:05.2f}".format(int(hours), int(minutes), seconds)


def print_log(text: str, new_line: bool = True, std_out: bool = True):
    if std_out:
        print(text)
    with open("./results.txt", "a") as file:
        file.write(escape_ansi(text) + os.linesep if new_line else '')


def teacher():
    print(Style.RESET_ALL)
    play("intro")
    print_log("===========================")
    print_log(f"Welcome {os.getenv('USER', '')}, get ready for solving {Fore.GREEN}{TOTAL_PROBLEMS}{Style.RESET_ALL} "
              f"problems using {', '.join(OPERATIONS)}. Good luck!")
    print_log("Started at " + Fore.GREEN + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + Style.RESET_ALL)
    print_log("---------------------------")
    start = time.time()
    failed = 0
    attempts = 0
    play("start")
    for x in range(0, TOTAL_PROBLEMS):
        if x == TOTAL_PROBLEMS:
            play("final")
        result, problem_text = eval(random.choice(OPERATIONS) + "()")
        ok: bool = False
        problem_text = ("#" + str(x + 1) + "/" + str(TOTAL_PROBLEMS) + ": ").ljust(
            8) + Fore.LIGHTWHITE_EX + problem_text + Style.RESET_ALL

        while not ok:
            attempts += 1
            print_log(text=problem_text, new_line=False, std_out=False)
            user_input = input(problem_text).lower()
            print_log(text=problem_text + user_input, new_line=True, std_out=False)
            if isinstance(result, list):
                if user_input not in result:
                    failed += 1
                    play("fail")
                else:
                    play("success")
                    break
            else:
                if user_input != result:
                    failed += 1
                    play("fail")
                else:
                    play("success")
                    break

    end = time.time()

    play("outro")

    print_log("---------------------------")
    print_log(f"Total elapsed time (hh:mm:ss.ff) {format(format_time_elapsed(end - start))}")
    print_log(
        f"Total time per single problem (hh:mm:ss.ff) {format(format_time_elapsed(float(end - start) / TOTAL_PROBLEMS))}")
    print_log(f"Total number of problems {TOTAL_PROBLEMS}")
    print_log(f"Total failed attempts {failed}")
    print_log(f"Success rate {round(TOTAL_PROBLEMS / attempts, 4) * 100}%")
    print_log("===========================")


TOTAL_PROBLEMS: int = 2
# OPERATIONS: list = ['addition', 'subtraction', 'multiplication', 'division']
OPERATIONS: list = ['time1']
ADD_SUB_MAX_RESULT: int = 100
ADD_SUB_MIN_NUMBER: int = 30
ADD_SUB_MAX_NUMBER: int = 90
MUL_DIV_MIN_NUMBER: int = 2
MUL_DIV_MAX_NUMBER: int = 10

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    teacher()
