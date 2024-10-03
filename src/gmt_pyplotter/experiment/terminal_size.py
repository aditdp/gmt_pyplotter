import os, cursor


# def get_terminal_size():
#     size = os.get_terminal_size()
#     return size.columns, size.lines


def check_terminal_size():
    while True:
        cursor.hide()
        os.system("clear")
        current_columns, current_lines = os.get_terminal_size()

        if current_columns > 80 and current_lines > 30:
            cursor.show()
            break
        elif current_columns < 80 and current_lines > 30:
            for x in range(current_lines - 5):
                print("")
            print("\033[38;5;208m\033[3mgmt_pyplotter\033[00m")
            print(current_columns * "-")
            print(
                f"Current terminal size: {current_columns} columns, {current_lines} rows"
            )
            print("resize the terminal width > 80 columns")
            input("press \033[3m'Enter'\033[00m after resize the terminal window...")
            cursor.show()
            continue
        elif current_columns > 80 and current_lines < 30:
            for x in range(current_lines - 5):
                print("")
            print("\033[38;5;208m\033[3mgmt_pyplotter\033[00m")
            print(current_columns * "-")
            print(
                f"Current terminal size: {current_columns} columns, {current_lines} rows"
            )
            print("resize the terminal height > 30 rows ")
            input("press \033[3m'Enter'\033[00m after resize the terminal window...")
            cursor.show()
            continue
        else:
            for x in range(current_lines - 5):
                print("")
            print("\033[38;5;208m\033[3mgmt_pyplotter\033[00m")
            print(current_columns * "-")
            print(
                f"Current terminal size: {current_columns} columns, {current_lines} rows"
            )
            print("resize the terminal width > 80 columns and height > 30 rows ")
            input("press \033[3m'Enter'\033[00m after resize the terminal window...")
            cursor.show()
            continue


check_terminal_size()
