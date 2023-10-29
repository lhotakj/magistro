# This is a sample Python script.
import random
from pygame import mixer  # Load the popular external library


def play_success():
    mixer.init()
    mixer.music.load('./sounds/success.mp3')
    mixer.music.play()


def play_fail():
    mixer.init()
    mixer.music.load('./sounds/fail.mp3')
    mixer.music.play()


def teacher():
    for x in range(0, 5):
        number1: int = random.randrange(1, 100)
        result: int = random.randrange(number1, 100)
        number2 = result - number1
        ok: bool = False
        while not ok:
            user_input = int(input(f"{number1} + {number2} = "))
            if user_input != result:
                play_fail()
            else:
                play_success()
                break


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    teacher()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
