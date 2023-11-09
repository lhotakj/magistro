# Simple
import random
import os
import time
import datetime

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
from pygame import mixer


def play_success():
    mixer.init()
    mixer.music.load('./sounds/success.mp3')
    mixer.music.play()


def play_fail():
    mixer.init()
    mixer.music.load('./sounds/fail.mp3')
    mixer.music.play()


def addition() -> tuple[str, str]:
    addend1: int = random.randrange(ADDSUB_MIN_NUMBER, ADDSUB_MAX_NUMBER)
    result: int = random.randrange(addend1, ADDSUB_MAX_RESULT)
    addend2 = result - addend1
    problem_text: str = f"{addend1} + {addend2} = "
    return str(result), problem_text


def subtraction() -> tuple[str, str]:
    addend1: int = random.randrange(ADDSUB_MIN_NUMBER, ADDSUB_MAX_NUMBER)
    result: int = random.randrange(addend1, ADDSUB_MAX_RESULT)
    addend2 = result - addend1
    problem_text: str = f"{result} - {addend1} = "
    return str(addend2), problem_text


def format_time_elapsed(dif: float) -> str:
    hours, rem = divmod(dif, 3600)
    minutes, seconds = divmod(rem, 60)
    return "{:0>2}:{:0>2}:{:05.2f}".format(int(hours), int(minutes), seconds)


def print_log(text: str, new_line: bool = True, std_out: bool = True):
    if std_out:
        print(text)
    with open("./results.txt", "a") as file:
        file.write(text + os.linesep if new_line else '')


def teacher():
    print_log("===========================")
    print_log(f"Welcome {os.getenv('USER', '')}, get ready for solving {TOTAL_PROBLEMS} math "
              f"problems using {', '.join(OPERATIONS)}. Good luck ")
    print_log("Started at " + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    print_log("---------------------------")
    start = time.time()
    failed = 0
    attempts = 0
    for x in range(0, TOTAL_PROBLEMS):
        result, problem_text = eval(random.choice(OPERATIONS) + "()")
        ok: bool = False
        while not ok:
            attempts += 1
            print_log(text=problem_text, new_line=False, std_out=False)
            user_input = input(problem_text)
            print_log(text=problem_text + user_input, new_line=True, std_out=False)
            if user_input != result:
                failed += 1
                play_fail()
            else:
                play_success()
                break

    end = time.time()

    print_log("---------------------------")
    print_log(f"Total elapsed time (hh:mm:ss.ff) {format(format_time_elapsed(end - start))}")
    print_log(
        f"Total time per single problem (hh:mm:ss.ff) {format(format_time_elapsed(float(end - start) / TOTAL_PROBLEMS))}")
    print_log(f"Total number of problems {TOTAL_PROBLEMS}")
    print_log(f"Total failed attempts {failed}")
    print_log(f"Success rate {round(TOTAL_PROBLEMS / attempts, 4) * 100}%")
    print_log("===========================")


TOTAL_PROBLEMS: int = 2
OPERATIONS: list = ['addition', 'subtraction']
ADDSUB_MAX_RESULT: int = 100
ADDSUB_MIN_NUMBER: int = 30
ADDSUB_MAX_NUMBER: int = 90

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    teacher()
