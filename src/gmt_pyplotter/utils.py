import os, shutil, sys, subprocess, time, cursor
from datetime import datetime, timedelta
from urllib.request import urlretrieve, urlopen
from PIL import Image
from showinfm import show_in_file_manager

match os.name:
    case "posix":
        SHELL = "True"
    case "nt":
        SHELL = "False"


def header():
    print(80 * "=")
    print("")
    print("GMT pyplotter".center(80, " "))
    print("interactive map ploting with Generic Mapping Tools".center(80, " "))
    print("")
    print(80 * "=")


def closing():
    print(" End of the program ".center(80, "="))


def is_connected():
    cursor.hide()
    print("  checking internet connection.")
    time.sleep(0.25)
    print("\033[2A")
    print("  checking internet connection..")
    time.sleep(0.25)
    print("\033[2A")
    print("  checking internet connection...")
    time.sleep(0.25)
    cursor.show()
    try:
        urlopen("https://www.google.com", timeout=5)
        return True
    except TimeoutError("    No internet connection"):
        return False


def app_usage_log(*args):
    log_path = os.path.join(os.path.dirname(__file__), "app_usage.log")
    if os.path.isfile(log_path):

        with open(log_path, "r", encoding="utf-8") as original:
            temp = original.read()
        with open(log_path, "w", encoding="utf-8") as new:

            new.write(
                f"""{datetime.now()}
	File name  = {args[0]}.{args[1]}
	Location   = {args[2]}
 	Coordinate = {args[3]}
	Layers     = {args[4]}
{temp}
"""
            )
    else:
        with open(log_path, "w", encoding="utf-8") as new:

            new.write(
                f"""{datetime.now()}
	File name  = {args[0]}.png
	Location   = {args[1]}
 	Coordinate = {args[2]}
	Layers     = {args[3]}
"""
            )


def system_check():
    log_path = os.path.join(os.path.dirname(__file__), "app_usage.log")
    with open(log_path, "r", encoding="utf-8") as file:
        file.seek(0)
        last_time = file.readline().strip()
        print(last_time)
        if last_time:
            date_time_obj = datetime.strptime(last_time, "%Y-%m-%d %H:%M:%S.%f")
            if datetime.now() > date_time_obj + timedelta(days=1):
                is_gawk_gmt_installed()
        else:
            is_gawk_gmt_installed()


def screen_clear():
    if os.name == "posix":
        os.system("clear")
    elif os.name == "nt":
        os.system("cls")
    else:
        os.system("cls")


def check_terminal_size():
    def print_terminal_size(info):
        for _ in range(current_lines - 5):
            print("")
            print("\033[38;5;208m\033[3mgmt_pyplotter\033[00m")
            print(current_columns * "-")
            print(
                f"Current terminal size: {current_columns} columns, {current_lines} rows"
            )
        print(info)
        input("press \033[3m'Enter'\033[00m after resize the terminal window...")
        cursor.show()

    while True:
        cursor.hide()
        screen_clear()
        current_columns, current_lines = os.get_terminal_size()

        if current_columns > 80 and current_lines > 30:
            cursor.show()
            break
        if current_columns < 80 and current_lines > 30:
            print_terminal_size("resize the terminal width > 80 columns")

        elif current_columns > 80 and current_lines < 30:
            print_terminal_size("resize the terminal height > 30 rows ")

        else:
            print_terminal_size(
                "resize the terminal width > 80 columns and height > 30 rows "
            )


def file_writer(*args):
    flag = args[0]
    script_name = args[1]
    layer = args[2]
    output_dir = args[3]
    print(layer)

    with open(os.path.join(output_dir, script_name), flag, encoding="utf-8") as file:
        file.write(layer)


def gcmt_downloader(*args):
    fm_file = args[0]
    coord = args[1]
    date = args[2]
    url_gcmt = "https://www.globalcmt.org/cgi-bin/globalcmt-cgi-bin/CMT5/form?itype=ymd&yr={}&mo={}&day={}&otype=nd&nday={}&llat={}&ulat={}&llon={}&ulon={}&list=6".format(
        date[0].strftime("%Y"),
        date[0].strftime("%m"),
        date[0].strftime("%d"),
        date[2],
        coord[2],
        coord[3],
        coord[0],
        coord[1],
    )
    print(f"retrieving data from:\n {url_gcmt}")
    page = urlopen(url_gcmt)
    html = page.read().decode("utf-8")
    start_index = html.rfind("<pre>") + 6
    end_index = html.rfind("</pre>")
    data_gcmt = html[start_index:end_index]
    print("data acquired..")
    # input("press any key to continue..")
    print(data_gcmt)
    with open(fm_file, "w", encoding="utf-8") as file:
        file.write(data_gcmt)
    print("done..")


def usgs_downloader(*args):
    usgs_cata_file = args[0]
    coord = args[1]
    date = args[2]
    url_usgs = "https://earthquake.usgs.gov/fdsnws/event/1/query?format=csv"
    url_loc = f"minlongitude={coord[0]}&maxlongitude={coord[1]}&minlatitude={coord[2]}&maxlatitude={coord[3]}"
    url_date = f"starttime={date[0]}&endtime={date[1]}"
    url = f"{url_usgs}&{url_date}&{url_loc}"

    print(f"\nRetrieving data from: {url}")
    urlretrieve(url, usgs_cata_file)
    print("\n Done.. \n")


def isc_downloader(*args):
    isc_cata_file = args[0]
    coord = args[1]
    date = args[2]
    mag = args[3]
    depth = args[4]
    url_isc = "https://www.isc.ac.uk/cgi-bin/web-db-run?request=COMPREHENSIVE&out_format=CATCSV&bot_lat={}&top_lat={}&left_lon={}&right_lon={}&searchshape=RECT&start_year={}&start_month={}&start_day={}&end_year={}&end_month={}&end_day={}&min_dep={}&max_dep={}&min_mag={}&max_mag={}".format(
        coord[2],
        coord[3],
        coord[0],
        coord[1],
        date[0].strftime("%Y"),
        date[0].strftime("%m"),
        date[0].strftime("%d"),
        date[1].strftime("%Y"),
        date[1].strftime("%m"),
        date[1].strftime("%d"),
        depth[0],
        depth[1],
        mag[0],
        mag[1],
    )
    print(f"data file is located in {isc_cata_file}")
    # input("pause")
    print(f"retrieving data from:\n {url_isc}")
    page = urlopen(url_isc)
    html = page.read().decode("utf-8")
    start_index = html.rfind("<pre>") + 252
    end_index = html.rfind("STOP") - 1
    data_isc = html[start_index:end_index]
    print("data acquired..")
    # input("press any key to continue..")
    print(data_isc)
    with open(isc_cata_file, "w", encoding="utf-8") as file:
        file.write(data_isc)
    print("done..")


def gmt_execute(name, output_dir):
    match os.name:
        case "posix":
            os.system(f"chmod +x {output_dir}/{name}.gmt")
            os.chdir(output_dir)
            command = f"./{name}.gmt"

        case "nt":
            os.chdir(output_dir)
            command = f"{name}.bat"

    msg_from_gmt = subprocess.run(
        command,
        shell=SHELL,
        capture_output=True,
        text=True,
        check=False,
    )
    if msg_from_gmt.stderr:
        finalization_bar("fail")
        print(
            f"\033[38;5;196mError while runing GMT script:\033[00m\n{msg_from_gmt.stderr}\n"
        )
        print("GMT script failed to run..")
        closing()

        sys.exit(130)


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
                print("\033[5A")
                print(stage1)
                print(stage2)
                loading_bar(beginloading, 99)
                beginloading += 1.6
                time.sleep(0.1)
                print("\033[5A")
                print(stage11)
                print(stage2)
                loading_bar(beginloading, 99)
                beginloading += 1.6
                time.sleep(0.1)
            print("\033[5A")
            print(stage1done)
            print(stage2)
            loading_bar(30, 99)
            time.sleep(1)
        case 2:
            print("\033[5A")
            print(stage1)
            print(stage2)
            end_time = time.time() + 2.4
            beginloading = 30
            while time.time() < end_time:
                print("\033[5A")
                print(stage1done)
                print(stage2)
                loading_bar(beginloading, 99)
                beginloading += 3
                time.sleep(0.1)
                print("\033[5A")
                print(stage1done)
                print(stage22)
                loading_bar(beginloading, 99)
                beginloading += 3
                time.sleep(0.1)
            print("\033[5A")
            print(stage1done)
            print(stage2done)
            loading_bar(99, 99)

        case "fail":
            print("\033[5A")
            print(stage1)
            print(stage2)
            end_time = time.time() + 1.7
            beginloading = 30
            while time.time() < end_time:
                print("\033[5A")
                print(stage1done)
                print(stage2)
                loading_bar(beginloading, 99)
                beginloading += 3
                time.sleep(0.1)
                print("\033[5A")
                print(stage1done)
                print(stage22)
                loading_bar(beginloading, 99)
                beginloading += 3
                time.sleep(0.1)
            print("\033[5A")
            print(stage1done)
            print(stage2fail)
            loading_bar(81, 99)
    cursor.show()


def info_display(args):
    pr1 = args[0]
    pr2 = args[1]
    pr3 = args[2]
    pr4 = args[3]
    pr5 = args[4]
    pr6 = args[5]
    pr21 = args[6]
    pr31 = args[7]
    duration_total = 5
    duration_blink = 0.1
    end_time = time.time() + duration_total
    begin_loading = args[8]
    cursor.hide()

    while time.time() < end_time:

        print("\033[0;0H")
        logo_brin(pr1, pr2, pr3, pr4, pr5, pr6)
        loading_bar(begin_loading, 100)

        time.sleep(duration_blink)

        print("\033[0;0H")
        logo_brin(pr1, pr21, pr31, pr4, pr5, pr6)
        loading_bar(begin_loading, 100)
        begin_loading += 2
        time.sleep(duration_blink)
    cursor.show()


def info_generator(status: int, apps: str, version=""):
    # variable for coloring the print output
    bg_reset = "\033[0;0m"
    bg_green = "\033[48;5;46m\033[38;5;198m"
    bg_yellow = "\033[48;5;226m\033[38;5;198m"
    bg_red = "\033[48;5;196m"
    if apps == "gawk":
        apps_long = "GNU AWK"
        process = 2
        app_color = "\033[38;5;208m"
    else:
        apps_long = "Generic Mapping Tools"
        process = 52
        app_color = "\033[38;5;33m"

    match status:
        case 1:  # Apps installed, version match
            bg_color1 = bg_green
            bg_color2 = bg_green

            pr4 = f"{app_color}{apps.upper()}{bg_reset} version supported"
            pr5 = ""
            pr6 = ""

        case 2:  # Apps installed, version not match
            bg_color1 = bg_yellow
            bg_color2 = bg_red
            pr4 = f"{app_color}{apps.upper()}{bg_reset} version not supported"
            pr5 = f"Update {app_color}{apps.upper()}{bg_reset} version.."
            pr6 = "Press any key to quit ..."

        case 3:  # Apps not installed
            bg_color1 = bg_red
            bg_color2 = bg_red
            pr4 = f"{app_color}{apps_long} not found"
            pr5 = f"Please install the {app_color}{apps.upper()}{bg_reset} program!"
            pr6 = "Press any key to quit ..."

    pr1 = f"{app_color}{apps_long}{bg_reset} in this system:"
    pr2 = f"   Location : {shutil.which(apps)}"
    pr3 = f"   Version  : {version}"
    pr21 = f"   Location : {bg_color1}{shutil.which(apps)}{bg_reset}"
    pr31 = f"   Version  : {bg_color2}{version}{bg_reset}"
    return [pr1, pr2, pr3, pr4, pr5, pr6, pr21, pr31, process]


def is_gawk_gmt_installed():
    """Check whether GAWK and GMT is installed in the system."""
    from gmt_pyplotter.user_input import add_gawk_path

    gmt_location = shutil.which("gmt")
    gawk_location = shutil.which("gawk")
    if gawk_location:
        getgawkversion = subprocess.Popen(
            "gawk --version", shell=SHELL, stdout=subprocess.PIPE
        ).stdout
        gawk_ver = getgawkversion.read()
        gawk_ver = gawk_ver[8:13]
        gawk_ver = gawk_ver.decode().rstrip()
        info_stat = info_generator(1, "gawk", gawk_ver)
        info_display(info_stat)
        # time.sleep(1)
    else:
        gawk_default_path = r"C:\Program Files (x86)\GnuWin32\bin\gawk.exe"

        if os.path.isfile(gawk_default_path):
            print("  'gawk' is installed but not added to 'PATH' environment variable")
            print("  Adding 'gawk' to 'PATH'...")
            os.system(
                r"""For /F "Skip=2Tokens=1-2*" %A In ('Reg Query HKCU\Environment /V PATH 2^>Nul') Do setx PATH "%C;C:\Program Files (x86)\GnuWin32\bin"""
            )
        else:
            info_stat = info_generator(3, "gawk")
            screen_clear()
            info_display(info_stat)
            instal_gawk = input(
                "\n\n  Do you want to install 'gawk' (GnuWin32) now (y/n)?  "
            )
            match instal_gawk:
                case "y" | "yes" | "Y" | "Yes" | "YES":
                    gawk_installer_path = os.path.join(
                        os.path.dirname(__file__), "data", "gawk-3.1.6-1-setup.exe"
                    )

                    subprocess.call(gawk_installer_path)
                    print("")

                    gawk_path = add_gawk_path()
                    edit_path = (
                        r"""For /F "Skip=2Tokens=1-2*" %A In ('Reg Query HKCU\Environment /V PATH 2^>Nul') Do setx PATH "%C;"""
                        + gawk_path
                    )
                    os.system(edit_path)

        closing()
        sys.exit("\nRestart the terminal before run 'gmt_pyplotter' again..")
    if gmt_location:
        if len(gmt_location) > 23:
            gmt_location = f"...{gmt_location[-20:]}"

        getgmtversion = subprocess.Popen(
            "gmt --version", shell=SHELL, stdout=subprocess.PIPE
        ).stdout
        gmt_ver = getgmtversion.read()
        gmt_ver = gmt_ver.decode().rstrip()

        screen_clear()
        if float(gmt_ver[0:3]) >= 6.4:
            info_stat = info_generator(1, "gmt", gmt_ver)
            info_display(info_stat)

        else:
            info_stat = info_generator(2, "gmt", gmt_ver)
            info_display(info_stat)

            input()
            print("")
            closing()
            sys.exit(
                " \n\033[38;5;196mError: \033[38;5;220m\033[3mgmt_pyplotter\033[0m\033[38;5;220m requires GMT version to 6.4.0 or latter to operate\n      Please update the GMT before running the program\n       https://docs.generic-mapping-tools.org/latest/install.html\033[0;0m \n"
            )

    else:
        info_stat = info_generator(3, "gmt")
        screen_clear()
        info_display(info_stat)
        input()
        print("")
        closing()
        sys.exit(
            " \n\033[38;5;196mError: \033[38;5;220m\033[3mgmt_pyplotter\033[0m\033[38;5;220m requires Generic Mapping Tools to operate\n       Please install GMT before running the program\n       https://docs.generic-mapping-tools.org/latest/install.html\033[0;0m \n"
        )


def logo_brin(*args):
    pr1 = args[0]
    pr2 = args[1]
    pr3 = args[2]
    pr4 = args[3]
    pr5 = args[4]
    pr6 = args[5]
    header()
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


def pictureshow(path):
    img = Image.open(path)
    img.show()


def show_output_image_and_directory(path):
    show_in_file_manager(path)
    try:
        pictureshow(path)
    except IOError:
        try:
            match sys.platform:
                case "win32":
                    subprocess.Popen(path, shell=True)

                case "darwin":
                    subprocess.Popen(["open", "-R", path], shell=True)
                case "linux":
                    subprocess.Popen(f"xdg-open {path}", shell=True)
        except SyntaxError:
            print("    Cannot show the map..")
