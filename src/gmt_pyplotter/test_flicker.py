# import time
# import os

# clear = lambda: os.system("cls")


# def gra():
#     koniec = "0"
#     while koniec != "1":
#         for i in range(4):
#             for j in range(10):
#                 print("[___]")
#             print("\n")
#         for i in range(10):
#             print("\n")
#         for i in range(10):
#             print(" ")
#         print("~~~~~~~~~~")
#         time.sleep(0.1)
#         clear()


# gra()


# I figured it out... You can use ANSI codes to move the cursor then clear the lines without any BLINK!

# print('\033[4A\033[2K', end='')
# \033[4A Moves the cursor 4 lines up (\033[{lines}A you can replace lines with however many you need) \033[2K Clears all those lines without the screen blinking. You can use it in a simple typewrite function that needs a constant message or a box around it like this:

from time import sleep


# def typewrite(text: str):
#     lines = text.split("\n")
#     for line in lines:
#         display = ""
#         for char in line:
#             display += char
#             print(
#                 f"╭─ SOME MESSAGE OR SOMEONES NAME ────────────────────────────────────────────╮"
#             )
#             print(f"│ {display:74} │")  # :74 is the same as ' ' * 74
#             print(
#                 f"╰────────────────────────────────────────────────────────────────────────────╯"
#             )

#             sleep(0.05)

#             print("\033[3A\033[2K", end="")


def typewrite(text: str):
    lines = text.split("\n")
    for line in lines:
        display = ""
        for char in line:
            display += char
            print("")
            print(
                f"╭─ SOME MESSAGE OR SOMEONES NAME ────────────────────────────────────────────╮"
            )
            print(f"│ {display:74} │")  # :74 is the same as ' ' * 74
            print(
                f"╰────────────────────────────────────────────────────────────────────────────╯"
            )

            sleep(0.05)

            print("\033[4A\033[2K", end="")


typewrite("absdakslfjal lkasflkds asldkfjlk aksljfs")
