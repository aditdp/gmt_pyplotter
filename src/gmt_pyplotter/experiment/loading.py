import sys, os, time, cursor


def screen_clear():
    if os.name == "posix":
        os.system("clear")
    elif os.name == "nt":
        os.system("cls")
    else:
        os.system("cls")


def loading_bar(iteration, total, bar_length=73):
    progress = iteration / total
    arrow = "█" * int(round(progress * bar_length))
    spaces = "-" * (bar_length - len(arrow))
    sys.stdout.write(f"\r|{arrow}{spaces}| {int(progress * 100)}%")
    sys.stdout.flush()


def finalization_bar(stage):
    cursor.hide()
    stage1 = "\n    Writing the script    [..  ]"
    stage11 = "\n    \033[38;5;228mWriting the script\033[00m    [  ..]"
    stage2 = "    Generating the map    [..  ]\n"
    stage22 = "\033[38;5;228m    Generating the map\033[00m    [  ..]\n"
    stage1done = "\n    Writing the script    [\033[38;5;40mdone\033[00m]"
    stage2done = "    Generating the map    [\033[38;5;40mdone\033[00m]\n"
    stage2fail = "    Generating the map    [\033[38;5;196mfail\033[00m]\n"

    match stage:
        case 1:
            print(stage1)
            print(stage2)
            end_time = time.time() + 2
            beginloading = 0
            while time.time() < end_time:
                print(f"\033[5A")
                print(stage1)
                print(stage2)
                loading_bar(beginloading, 99)
                beginloading += 1.6
                time.sleep(0.1)
                print(f"\033[5A")
                print(stage11)
                print(stage2)
                loading_bar(beginloading, 99)
                beginloading += 1.6
                time.sleep(0.1)
            print(f"\033[5A")
            print(stage1done)
            print(stage2)
            loading_bar(30, 99)
            time.sleep(1)
        case 2:
            print(stage1)
            print(stage2)
            end_time = time.time() + 2.4
            beginloading = 30
            while time.time() < end_time:
                print(f"\033[5A")
                print(stage1done)
                print(stage2)
                loading_bar(beginloading, 99)
                beginloading += 3
                time.sleep(0.1)
                print(f"\033[5A")
                print(stage1done)
                print(stage22)
                loading_bar(beginloading, 99)
                beginloading += 3
                time.sleep(0.1)
            print(f"\033[5A")
            print(stage1done)
            print(stage2done)
            print(f"\033[1A")
            time.sleep(1)

        case "fail":
            print(stage1)
            print(stage2)
            end_time = time.time() + 1.7
            beginloading = 30
            while time.time() < end_time:
                print(f"\033[5A")
                print(stage1done)
                print(stage2)
                loading_bar(beginloading, 99)
                beginloading += 3
                time.sleep(0.1)
                print(f"\033[5A")
                print(stage1done)
                print(stage22)
                loading_bar(beginloading, 99)
                beginloading += 3
                time.sleep(0.1)
            print(f"\033[5A")
            print(stage1done)
            print(stage2fail)
            loading_bar(81, 99)
    cursor.show()


print("aslkdfjsdalfk")
# finalization_bar(0)
# screen_clear()
finalization_bar(1)
# screen_clear()
# finalization_bar(2)
