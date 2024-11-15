import os, shutil, sys, subprocess, time, cursor, csv, math
from datetime import datetime, timedelta
from dateutil import parser
from functools import wraps
from urllib.request import urlretrieve, urlopen
from PIL import Image
from showinfm import show_in_file_manager

match os.name:
    case "posix":
        shel = "True"
    case "nt":
        shel = "False"


def header():
    print(80 * "=")
    print("")
    print("GMT pyplotter".center(80, " "))
    print("interactive map ploting with Generic Mapping Tools".center(80, " "))
    print("")
    print(80 * "=")


def closing():
    print(" End of the program ".center(80, "="))


def disable_input(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if os.name == "posix":
            import termios
            import tty

            fd = sys.stdin.fileno()
            original_attributes = termios.tcgetattr(fd)
            tty.setcbreak(fd)
        elif os.name == "nt":
            import msvcrt

        result = None
        try:
            result = func(*args, **kwargs)
        except KeyboardInterrupt:
            print("\n\n    KeyboardInterrupt: Exiting the program..\n")
            closing()
            cursor.show()
            try:
                sys.exit(130)
            except SystemExit:
                os._exit(130)
        finally:
            if os.name == "posix":
                termios.tcsetattr(fd, termios.TCSANOW, original_attributes)
            elif os.name == "nt":
                while msvcrt.kbhit():
                    msvcrt.getch()  # Clear the buffer
        return result

    return wrapper


@disable_input
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


@disable_input
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

        if last_time:
            date_time_obj = datetime.strptime(last_time, "%Y-%m-%d %H:%M:%S.%f")
            if datetime.now() > date_time_obj + timedelta(days=1):
                is_gmt_installed()
        else:
            is_gmt_installed()


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
        print(f"Current terminal size: {current_columns} columns, {current_lines} rows")
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


import csv


def find_min_max(
    filename: str,
    file_path: str,
    column_index: int,
    delimiter="\t",
    trim=False,
    date=False,
):
    """
    Returns:
    a dictionary:
    {
    "min" : minimum value
    "max" : maximum value
    "count" : total line count
    "range" :  max - min
    "trim_min" : minimum value of trimmed data (5 percent)
    "trim_max" : maximum value of trimmed data (5 percent)
    "trim_range" : trim_max - trim_min
    """

    line_count = 0
    data = []

    with open(os.path.join(file_path, filename), "r") as file:
        for line in file:
            values = line.strip().split(delimiter)
            if date == False:
                try:
                    data.append(float(values[column_index]))
                except (ValueError, IndexError):
                    continue
            if date == True:
                try:
                    data.append(parser.parse(values[column_index], ignoretz=True))
                except (ValueError, IndexError):
                    continue
            line_count += 1
    if line_count == 0:
        return None
    minimum = min(data)
    maximum = max(data)
    range = maximum - minimum
    info = {
        "min": minimum,
        "max": maximum,
        "count": line_count,
        "range": range,
    }
    # min max value from trimmed 5 percent top and bottom of data
    if trim == True:
        trim_count = int(len(data) * (0.02))
        sorted_data = sorted(data)
        if trim_count == 0:
            trimmed_data = sorted_data
        else:
            trimmed_data = sorted_data[trim_count:-trim_count]
        trim_min = min(trimmed_data)
        trim_max = max(trimmed_data)
        trim_range = trim_max - trim_min

        info = {
            "min": minimum,
            "max": maximum,
            "count": line_count,
            "range": range,
            "trim_min": round(trim_min, -1),
            "trim_max": round(trim_max, -1),
            "trim_range": trim_range,
        }
        return info
    return info


@disable_input
def file_writer(
    flag: str,
    script_name_format: str,
    text: str,
    output_dir: str,
):

    with open(
        os.path.join(output_dir, script_name_format), flag, encoding="utf-8"
    ) as file:
        file.write(text)


def is_file_empty(filepath, filename):
    file = os.path.join(filepath, filename)
    return os.path.getsize(file) == 0


def reorder_columns(input_file, output_file, new_order):
    with open(input_file, "r", encoding="utf-8") as infile:
        reader = csv.reader(infile)

        # Write reordered columns to new file
        with open(output_file, "w", newline="", encoding="utf-8") as outfile:
            writer = csv.writer(outfile, delimiter="\t")
            for row in reader:
                reordered_row = [row[i].strip() for i in new_order]
                writer.writerow(reordered_row)


@disable_input
def gcmt_downloader(fm_file, file_path, coord, date, mag, depth):

    url_gcmt = "https://www.globalcmt.org/cgi-bin/globalcmt-cgi-bin/CMT5/form?itype=ymd&yr={}&mo={}&day={}&otype=nd&nday={}&lmw={}&umw={}&llat={}&ulat={}&llon={}&ulon={}&lhd={}&uhd={}&list=6".format(
        date[0].strftime("%Y"),
        date[0].strftime("%m"),
        date[0].strftime("%d"),
        date[2],
        mag[0],
        mag[1],
        coord[2],
        coord[3],
        coord[0],
        coord[1],
        depth[0],
        depth[1],
    )

    print(f"  retrieving data from:\n {url_gcmt}")
    page = urlopen(url_gcmt)
    html = page.read().decode("utf-8")
    start_index = html.rfind("<pre>") + 6
    end_index = html.rfind("</pre>")
    data_gcmt = html[start_index:end_index]
    print("data acquired..")
    # input("press any key to continue..")
    print(data_gcmt)
    file_writer("w", f"{fm_file[0:-4]}_ORI.txt", data_gcmt, file_path)
    if is_file_empty(file_path, f"{fm_file[0:-4]}_ORI.txt") == False:
        add_mag_to_meca_file(
            os.path.join(file_path, f"{fm_file[0:-4]}_ORI.txt"),
            os.path.join(file_path, fm_file),
        )

        print("done..")
        status = "good"
    else:
        print("   No earthquake event found..")
        status = "empty"
    return status


def calculate_mw(mrr, mtt, mpp, mrt, mrp, mtp, iexp):
    """# Calculate the seismic moment M0"""
    m0 = (
        math.sqrt(0.5 * (mrr**2 + mtt**2 + mpp**2 + 2 * (mrt**2 + mrp**2 + mtp**2)))
        * 10**iexp
    )
    # Calculate the moment magnitude Mw
    mw = (2 / 3) * math.log10(m0) - 10.7
    return round(mw, 1)


def add_mag_to_meca_file(input_file, output_file, delimiter=" ", output_delimiter="\t"):
    """read the input file and insert the Mw value to the last column of meca file and save as output file name"""
    with open(input_file, "r") as infile, open(output_file, "w", newline="") as outfile:
        reader = csv.reader((line.rstrip() for line in infile), delimiter=delimiter)
        writer = csv.writer(outfile, delimiter=output_delimiter)

        # Process each row and calculate Mw
        for row in reader:
            try:
                # Check if row is correctly split
                if len(row) != 13:
                    raise ValueError("Row does not contain exactly 13 values")

                lon = float(row[0])
                lat = float(row[1])
                depth = float(row[2])
                mrr = float(row[3])
                mtt = float(row[4])
                mpp = float(row[5])
                mrt = float(row[6])
                mrp = float(row[7])
                mtp = float(row[8])
                iexp = int(row[9])
                x = row[10]
                y = row[11]
                name = row[12]

                # Calculate Mw
                mw = calculate_mw(mrr, mtt, mpp, mrt, mrp, mtp, iexp)

                # Write the new row with Mw appended
                writer.writerow(row + [mw])
            except ValueError as e:
                print(f"    Error processing row: {row}. Error: {e}")


@disable_input
def usgs_downloader(eq_file: str, file_path: str, coord, date, mag, depth):
    url_usgs = "https://earthquake.usgs.gov/fdsnws/event/1/query?format=csv"
    url_loc = f"minlongitude={coord[0]}&maxlongitude={coord[1]}&minlatitude={coord[2]}&maxlatitude={coord[3]}"
    url_date = f"starttime={date[0]}&endtime={date[1]}"
    url_mag = f"minmagnitude={mag[0]}&maxmagnitude={mag[1]}"
    url_dep = f"mindepth={depth[0]}&maxdepth={depth[1]}"
    url = f"{url_usgs}&{url_date}&{url_loc}&{url_mag}&{url_dep}"
    print(f"\nRetrieving data from: {url}")
    print("\n    This may take a while...")
    urlretrieve(url, os.path.join(file_path, f"{eq_file[0:-4]}_ORI.txt"))
    if is_file_empty(file_path, f"{eq_file[0:-4]}_ORI.txt") == False:

        reorder_columns(
            os.path.join(file_path, f"{eq_file[0:-4]}_ORI.txt"),
            os.path.join(file_path, eq_file),
            [2, 1, 3, 4, 0],
        )
        print("\n Done.. \n")
        status = "good"
    else:
        print("   No earthquake event found..")
        status = "empty"
    return status


@disable_input
def isc_downloader(eq_file, file_path, coord, date, mag, depth):

    url_isc = "https://www.isc.ac.uk/cgi-bin/web-db-run?request=COMPREHENSIVE&out_format=CATCSV&searchshape=RECT"

    url_loc = "&bot_lat={}&top_lat={}&left_lon={}&right_lon={}".format(
        coord[2],
        coord[3],
        coord[0],
        coord[1],
    )
    url_date = "&start_year={}&start_month={}&start_day={}&end_year={}&end_month={}&end_day={}".format(
        date[0].strftime("%Y"),
        date[0].strftime("%m"),
        date[0].strftime("%d"),
        date[1].strftime("%Y"),
        date[1].strftime("%m"),
        date[1].strftime("%d"),
    )
    url_dep = "&min_dep={}&max_dep={}&min_mag={}&max_mag={}".format(
        depth[0],
        depth[1],
        mag[0],
        mag[1],
    )
    url = url_isc + url_loc + url_date + url_dep
    print(f"\nEq data save as {eq_file}\n")
    # input("pause")
    print(f"retrieving data from:\n{url}")
    print("\n\nMay be take some time ..")
    page = urlopen(url)
    html = page.read().decode("utf-8")
    start_index = html.rfind("EVENTID") - 2
    end_index = html.rfind("STOP") - 1
    data_isc = html[start_index:end_index]
    print("data acquired..")
    # input("press any key to continue..")
    # print(data_isc)
    file_writer("w", f"{eq_file[0:-4]}_ORI.txt", data_isc, file_path)
    if is_file_empty(file_path, f"{eq_file[0:-4]}_ORI.txt") == False:
        reorder_columns(
            os.path.join(file_path, f"{eq_file[0:-4]}_ORI.txt"),
            os.path.join(file_path, eq_file),
            [6, 5, 7, 11, 3, 4],
        )
        print("done..")
        status = "good"
    else:
        print("   No earthquake event found..")
        status = "empty"
    return status


@disable_input
def grdimage_download(name, outputdir, coord_script, resolution, masking):
    """downloading grdimage data and returning the 'grd filename'"""
    if masking is True:
        command = "clip"
        replace = "-Sb1/NaN"
    else:
        command = "cut"
        replace = ""
    grd_file = f"{name}-GRD.nc"
    dl_gridfile = subprocess.run(
        f"gmt grd{command} {coord_script} {resolution} -G{os.path.join(outputdir ,grd_file)} {replace} ",
        text=True,
        shell={os.name == "posix"},
        capture_output=True,
        check=True,
    )
    infow = dl_gridfile.stdout
    print(infow)
    return grd_file


@disable_input
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
        shell=shel,
        capture_output=True,
        text=True,
        check=False,
    )
    if msg_from_gmt.stderr:
        finalization_bar("fail")
        print(
            f"\n\n\033[38;5;196mError while runing GMT script:\033[00m\n{msg_from_gmt.stderr}\n"
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


def date_min_max(file_path: str, column: int):
    pass
    # with open(file_path, )


@disable_input
def info_display(args):
    pr1 = args[0]
    pr2 = args[1]
    pr3 = args[2]
    pr4 = args[3]
    pr5 = args[4]
    pr6 = args[5]
    pr21 = args[6]
    pr31 = args[7]
    duration_total = 3
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
        begin_loading += 7
        time.sleep(duration_blink)
    cursor.show()


def info_generator(status: int, apps: str, version=""):
    # variable for coloring the print output
    bg_reset = "\033[0;0m"
    bg_green = "\033[48;5;46m\033[38;5;198m"
    bg_yellow = "\033[48;5;226m\033[38;5;198m"
    bg_red = "\033[48;5;196m"

    apps_long = "Generic Mapping Tools"
    process = 2
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


def is_gmt_installed():
    """Check is GMT installed in the system with supported version."""

    gmt_path = shutil.which("gmt")

    if gmt_path:
        if len(gmt_path) > 23:
            gmt_path = f"...{gmt_path[-20:]}"

        getgmtversion = subprocess.Popen(
            "gmt --version", shell=shel, stdout=subprocess.PIPE
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
        gmt_default = r"C:\programs\gmt6\bin\gmt.exe"
        info_stat = info_generator(3, "gmt")
        screen_clear()
        info_display(info_stat)
        input()
        print("")
        closing()
        if os.path.isfile(gmt_default) == True:
            print("\033[38;5;46m\n")
            print(r"GMT found at 'C:\programs\gmt6\bin' ")
            print(
                "\033[38;5;220m\033[3mUpdating 'Path' Environment Variable...\033[0m\033[38;5;81m"
            )
            time.sleep(2)
            os.system(
                r"""For /F "Skip=2Tokens=1-2*" %A In ('Reg Query HKCU\Environment /V PATH 2^>Nul') Do setx PATH "%C;C:\programs\gmt6\bin """
            )
            time.sleep(1)
            sys.exit(
                "\n\033[38;5;196mReopen the terminal for the changes take effect \033[0;0m\n"
            )
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
