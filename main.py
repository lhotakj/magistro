#!/usr/bin/python3

import random
import os
import time
import datetime
import re
from colorama import Fore, Style
from slack_sdk import WebClient

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
from pygame import mixer

SEND_SLACK: bool = True

TIME1_QUESTIONS: list = [
    {"How many days are a week?": "7"},
    {"How many days are a working week?": "5"},
    {"How many hours are in a day?": "24"},
    {"How many hours are in two days?": "48"},
    {"How many hours are in 2 days?": "48"},
    {"How many days are in a week?": "7"},
    {"How many days are in two weeks?": "14"},
    {"How many days are in 2 weeks?": "14"},
    {"How many days are in two weeks?": "14"},
    {"How many days are in 2 weeks?": "14"},
    {"How many days are in three weeks?": "21"},
    {"How many days are in 3 weeks?": "21"},
    {"How many days are in four weeks?": "28"},
    {"How many days are in 4 weeks?": "28"},
    {"How many weeks are in a month?": "4"},
    {"How many months are in a year?": "12"},
    {"How many hours are in half a day?": "12"},
    {"How many minutes are in an hour?": "60"},
    {"How many seconds are in a minute?": "60"},
]

TIME2_QUESTIONS: list = [
    {"How many meteorological seasons are in a year?": ["four", "4"]},
    {"When starts the meteorological spring in the Northern Hemisphere (Europe)?": ["mar 1st", "mar 1", "1st mar",
                                                                                    "1 mar", "march 1st", "march 1",
                                                                                    "1st march", "1 march", "1.3",
                                                                                    "1.3.", "3/1"]},
    {"When starts the meteorological summer in the Northern Hemisphere (Europe)?": ["jun 1st", "jun 1", "1st jun",
                                                                                    "1 jun", "june 1st", "june 1",
                                                                                    "1st june", "1 june", "1.6", "1.6.",
                                                                                    "6/1"]},
    {"When starts the meteorological autumn in the Northern Hemisphere (Europe)?": ["sep 1st", "sep 1", "1st sep",
                                                                                    "1 sep", "september 1st",
                                                                                    "september 1", "1st september",
                                                                                    "1 september", "1.9", "1.9.",
                                                                                    "9/1"]},
    {"When starts the meteorological winter in the Northern Hemisphere (Europe)?": ["dec 1st", "dec 1", "1st dec",
                                                                                    "1 dec", "december 1st",
                                                                                    "december 1", "1st december",
                                                                                    "1 december", "1.12", "1.12.",
                                                                                    "12/1"]},

    {"When starts the meteorological autumn in the Southern Hemisphere (Australia)?": ["mar 1st", "mar 1", "1st mar",
                                                                                       "1 mar", "march 1st", "march 1",
                                                                                       "1st march", "1 march", "1.3",
                                                                                       "1.3.", "3/1"]},
    {"When starts the meteorological winter in the Southern Hemisphere (Australia)?": ["jun 1st", "jun 1", "1st jun",
                                                                                       "1 jun", "june 1st", "june 1",
                                                                                       "1st june", "1 june", "1.6",
                                                                                       "1.6.", "6/1"]},
    {"When starts the meteorological spring in the Southern Hemisphere (Australia)?": ["sep 1st", "sep 1", "1st sep",
                                                                                       "1 sep", "september 1st",
                                                                                       "september 1", "1st september",
                                                                                       "1 september", "1.9", "1.9.",
                                                                                       "9/1"]},
    {"When starts the meteorological summer in the Southern Hemisphere (Australia)?": ["dec 1st", "dec 1", "1st dec",
                                                                                       "1 dec", "december 1st",
                                                                                       "december 1", "1st december",
                                                                                       "1 december", "1.12", "1.12.",
                                                                                       "12/1"]},

    {"What season is in Europe when in Australia is spring?": ["autumn", "fall"]},
    {"What season is in Europe when in Australia is summer?": "winter"},
    {"What season is in Europe when in Australia is autumn?": "spring"},
    {"What season is in Europe when in Australia is winter?": "summer"},
    {"What season is in Australia when in Europe is spring?": ["autumn", "fall"]},
    {"What season is in Australia when in Europe is summer?": "winter"},
    {"What season is in Australia when in Europe is autumn?": "spring"},
    {"What season is in Australia when in Europe is winter?": "summer"},
    {"How many days are in a leap year?": "366"},
    {"How many days are in a normal year?": "365"},
    {"What is the name of the shortest month of the leap year?": ["feb", "february"]},
    {"How many days has February in the leap year?": "29"},
    {"How ofter is a leap year?": ["in 4 years", "every 4 years", "4", "4 years", "4 yrs"]},
    {"What is the last month in the year?": ["dec", "December"]},
    {"What is the first month in the year?": ["jan", "january"]},
]


def escape_ansi(line):
    ansi_escape = re.compile(r'(\x9B|\x1B\[)[0-?]*[ -\/]*[@-~]')
    return ansi_escape.sub('', line)


def play(sound: str) -> None:
    mixer.init()
    mixer.music.load(f"./sounds/{sound}.mp3")
    mixer.music.play()


def send_message(intro: str, text: str):
    if SEND_SLACK:
        print_log(text="Sending Slack notification", new_line=True, std_out=True)
        if "SLACK_BOT_TOKEN" not in os.environ:
            print("Environment variable SLACK_BOT_TOKEN not provided. Slack notification skipped")
            return None
        if "SLACK_CHANNEL_ID" not in os.environ:
            print("Environment variable SLACK_CHANNEL_ID not provided. Slack notification skipped")
            return None

        client = WebClient(token=os.environ.get("SLACK_BOT_TOKEN"))

        # Specify the channel ID and the message text
        channel_id = os.environ.get("SLACK_CHANNEL_ID")

        # Send the message to the channel
        result = None
        try:
            result = client.chat_postMessage(channel=channel_id, text='.', mrkdwn=True, blocks=[
                {"type": "section", "text": {"type": "plain_text", "text": intro}},
                {"type": "section", "text": {"type": "mrkdwn", "text": text}}
            ])
        except:
            print_log(text="Error while sending Slack", new_line=True, std_out=True)
            print_log(text=str(result), new_line=True, std_out=True)


def verbal_question(dictionary_name: list) -> tuple[list[str], str]:
    problems: list = dictionary_name
    problem: dict = problems[random.randrange(0, len(problems) - 1)]
    question: str = list(problem.keys())[0] + " "
    answers: str | list = list(problem.values())[0]
    answers = answers if isinstance(answers, list) else [answers]
    return answers, question


def time1() -> tuple[list[str], str]:
    return verbal_question(TIME1_QUESTIONS)


def time2() -> tuple[list[str], str]:
    return verbal_question(TIME2_QUESTIONS)


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
    slack_report: str = ""
    user: str = os.getenv('USER', '')
    if user == '':
        user = os.getenv('USERNAME', '')
    if user == '':
        user = "<unknown user>"
    print(Style.RESET_ALL)
    play("intro")
    print("                       _     _             ")
    print("                      (_)   | |            ")
    print(" _ __ ___   __ _  __ _ _ ___| |_ _ __ ___  ")
    print("| '_ ` _ \ / _` |/ _` | / __| __| '__/ _ \ ")
    print("| | | | | | (_| | (_| | \__ \ |_| | | (_) |")
    print("|_| |_| |_|\__,_|\__, |_|___/\__|_|  \___/ ")
    print("                  __/ |                    ")
    print("                 |___/  version 1.2.       ")
    print_log("===========================================")
    print_log("===========================================")
    print_log(f"Welcome {user}, get ready for solving {Fore.GREEN}{TOTAL_PROBLEMS}{Style.RESET_ALL} "
              f"tasks using {', '.join(OPERATIONS)}. Good luck!")
    print_log("Started at " + Fore.GREEN + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + Style.RESET_ALL)
    print_log("-------------------------------------------")
    start = time.time()
    failed = 0
    attempts = 0
    play("start")
    for x in range(0, TOTAL_PROBLEMS):
        if x == TOTAL_PROBLEMS - 1:
            play("final")
        result, problem_text = eval(random.choice(OPERATIONS) + "()")
        ok: bool = False
        problem_text_raw: str = problem_text
        problem_text = ("#" + str(x + 1) + "/" + str(TOTAL_PROBLEMS) + ": ").ljust(
            8) + Fore.LIGHTWHITE_EX + problem_text + Style.RESET_ALL
        errors: int = 0
        while not ok:
            attempts += 1
            print_log(text=problem_text, new_line=False, std_out=False)
            user_input = input(problem_text).lower()
            print_log(text=problem_text + user_input, new_line=True, std_out=False)
            if isinstance(result, list):
                if user_input not in result:
                    failed += 1
                    errors += 1
                    play("fail")
                else:
                    play("success")
                    break
            else:
                if user_input != result:
                    failed += 1
                    errors += 1
                    play("fail")
                else:
                    play("success")
                    break

        slack_report += ("#" + (str(x + 1) + ": ").ljust(4)) + problem_text_raw + user_input + " "
        if errors == 0:
            slack_report += "✅"
        else:
            slack_report += "❌ " + str(errors) + " attempts"
        slack_report += "\n"

    end = time.time()
    play("outro")

    print_log("-------------------------------------------")
    print_log(f"Total number of problems {TOTAL_PROBLEMS}")
    print_log(f"Total elapsed time (hh:mm:ss.ff) {format(format_time_elapsed(end - start))}")
    print_log(
        f"Total time per single question (hh:mm:ss.ff) "
        f"{format(format_time_elapsed(float(end - start) / TOTAL_PROBLEMS))}")
    print_log(f"Total failed attempts {failed}")
    print_log(f"Success rate {round(TOTAL_PROBLEMS / attempts, 4) * 100}%")
    print_log("===========================================")
    slack_report += f"------------------------------------------\n"
    slack_report += f"Selected topics: {', '.join(OPERATIONS)}\n"
    slack_report += f"Total number of problems: {TOTAL_PROBLEMS}\n"
    slack_report += f"Total time per single question: {format(format_time_elapsed(float(end - start) / TOTAL_PROBLEMS))}\n"
    slack_report += f"Total failed attempts: {failed}\n"

    if SEND_SLACK:
        send_message(
            intro=f"User *{user}* just finished magistro tasks with the following results",
            text="```" + slack_report + "```")
    input("Press any key to close the window ...")


TOTAL_PROBLEMS: int = 2
# OPERATIONS: list = ['addition', 'subtraction', 'multiplication', 'division']
# OPERATIONS: list = ['time1', 'time2']
OPERATIONS: list = ['addition']
ADD_SUB_MAX_RESULT: int = 100
ADD_SUB_MIN_NUMBER: int = 30
ADD_SUB_MAX_NUMBER: int = 90
MUL_DIV_MIN_NUMBER: int = 2
MUL_DIV_MAX_NUMBER: int = 10

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    teacher()
