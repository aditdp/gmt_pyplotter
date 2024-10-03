import time, os, cursor, sys


def header():
    print(80 * "=")
    print("")
    print("GMT pyplotter".center(80, " "))
    print("interactive map ploting with Generic Mapping Tools".center(80, " "))
    print("")
    print(80 * "=")


def logo_brin(*args):
    pr1 = args[0]
    pr2 = args[1]
    pr3 = args[2]
    pr4 = args[3]
    pr5 = args[4]
    pr6 = args[5]
    # header()
    print(
        f""" \033[38;5;196m
                 ↑↑↑↑↑↑↑↑↑↑↑↑             \033[00m  {pr1} \033[38;5;196m
                  ↑↑↑↑↑↑↑↑↑↑↑↑↑↑          \033[00m  {pr2} \033[38;5;196m
       ↑↑↑↑↑↑      ↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑        \033[00m  {pr3} \033[38;5;196m
     ↑↑↑↑↑↑↑↑↑↑     ↑↑↑↑↑↑↑↑↑ ↑↑↑↑↑↑      
    ↑↑↑↑↑↑↑↑↑↑↑↑↑    ↑↑↑↑↑↑↑↑  ↑↑↑↑↑↑↑    
   ↑↑↑↑↑↑↑↑↑↑↑↑↑↑    ↑↑↑↑↑        ↑↑↑↑↑   \033[00m  {pr4} \033[38;5;196m
   ↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑   ↑↑↑↑↑↑↑    ↑↑↑↑↑↑↑↑  \033[00m  {pr5} \033[38;5;196m
   ↑↑↑↑↑↑↑↑↑↑↑↑↑↑    ↑↑↑↑↑↑↑↑  ↑↑↑↑↑↑↑↑↑  
    ↑↑↑↑↑↑↑↑↑↑↑↑      ↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑ 
      ↑↑↑↑↑↑↑↑↑        ↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑ \033[00m  {pr6} \033[38;5;196m
                                          
 ↑↑                   ↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑ 
 ↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑    ↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑  
 ↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑   ↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑  
  ↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑  ↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑   
   ↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑  ↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑    
    ↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑  ↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑     \033[00m  ___________________________________\033[38;5;196m
      ↑↑↑↑↑↑↑   ↑   ↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑      \033[00m  © BRIN \033[38;5;196m   
        ↑↑↑↑↑↑↑↑   ↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑        \033[00m  Badan Riset dan Inovasi Nasional\033[38;5;196m
          ↑↑↑↑↑↑  ↑↑↑↑↑↑↑↑↑↑↑↑↑↑          \033[00m \x1B[3m National Research and Innovation \033[38;5;196m
                ↑↑↑↑↑↑↑↑↑↑↑↑              \033[00m \x1B[3m Agency of Indonesia \033[00m \n"""
    )


def blink():
    duration_total = 5
    duration_blink = 0.25
    end_time = time.time() + duration_total
    cursor.hide()
    pr1 = f"generic mapping tools in this system:"
    pr2 = f"   Location : \033[48;5;46m\033[38;5;198mGMT/location/bin\033[0;0m"
    pr3 = f"   Version  : \033[48;5;46m6.1.2\033[0;0m"
    pr4 = f"gmt version supported"
    pr21 = f"   Location : GMT/location/bin"
    pr31 = f"   Version  : 6.1.2"
    os.system("clear")
    header()
    iteration = 5
    while time.time() < end_time:

        print(f"\033[6;0H")
        logo_brin(pr1, pr2, pr3, pr4, "", "")
        display_progress_bar(iteration, 100)
        iteration += 5
        time.sleep(duration_blink)

        print(f"\033[6;0H")
        logo_brin(pr1, pr21, pr31, pr4, "", "")
        display_progress_bar(iteration, 100)
        iteration += 5
        time.sleep(duration_blink)
    cursor.show()


def display_progress_bar(iteration, total, bar_length=73):
    progress = iteration / total
    arrow = "█" * int(round(progress * bar_length))
    spaces = "-" * (bar_length - len(arrow))
    sys.stdout.write(f"\r|{arrow}{spaces}| {int(progress * 100)}%")
    sys.stdout.flush()


def loading_bar(begin, step):
    print(f"\n")
    for x in range(begin, step):
        percent = 75 * (x / 100)
        bar = "█" * int(percent) + "-" * (75 - int(percent))
        print(f"\r|{bar}| {100*x/100}%", end="\r")

        time.sleep(0.01)


blink()
