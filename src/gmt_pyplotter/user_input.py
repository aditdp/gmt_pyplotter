from gmt_pyplotter import utils
from gmt_pyplotter.data.color_list import unique_color, palette_name
import os.path, re, sys
from cmd import Cmd
from datetime import date
from tkinter.filedialog import askopenfilename, askdirectory


def separator(func):
    def wrapper(*args):
        print(80 * "=")
        func(*args)
        print(80 * "=")

    return wrapper


def printe(error_msg):
    print(f"\033[38;5;227m\033[3m{error_msg}\033[00m")


def printc(conclusion_msg):
    print("-" * 80)
    print(f"\033[38;5;81m{conclusion_msg}\033[00m")
    print("-" * 80)
    print("")


def add_gawk_path():
    print("  Adding GnuWin32 program to 'PATH' environment variable.. ")
    if os.path.isfile(r"C:\Program Files (x86)\GnuWin32\bin\gawk.exe"):
        real_gawk_path = r"C:\Program Files (x86)\GnuWin32\bin"
    else:
        while True:
            print("  Locate the installed GnuWin32 'bin' directory.. ")
            gawk_path_raw = askdirectory(
                initialdir=os.getcwd(),
                mustexist=True,
                title="  Browse for 'GnuWin32/bin' folder.. ",
            )
            gawk_path_win = ""
            gawk_path_split = gawk_path_raw.split("/")

            for x in range(len(gawk_path_split)):
                gawk_path_win += gawk_path_raw[x] + "\\"
            if os.path.isfile(os.path.join(gawk_path_win, "bin", "gawk.exe")):
                real_gawk_path = os.path.join(gawk_path_win, "bin")
                break
            elif os.path.isfile(os.path.join(gawk_path_win, "gawk.exe")):
                real_gawk_path = gawk_path_win
                break
            else:
                printe(f"  '{gawk_path_win}' is not valid GnuWin32 folder")
    printc(f"  gawk path = {real_gawk_path}")
    return real_gawk_path


def save_loc():
    print("\n  Select the output (figure, gmt script & another data) directory ..\n")
    input("  Press 'enter' to open browsing window..")
    while True:
        output_path = askdirectory(
            initialdir=os.getcwd(),
            mustexist=True,
            title="  Select the output directory",
        )
        if output_path:
            break
        else:
            printe("    No directory selected")
            retry = input("  Do you want to retry (y/n)? ")
            match retry.upper():
                case "Y" | "YES" | "YA":
                    continue
                case _:
                    try:
                        print(" End of the program ".center(80, "="))
                        sys.exit(130)
                    except SystemExit:
                        os._exit(130)
                        raise
    if os.name == "nt":
        output_path = output_path.replace("/", "\\")
    if len(output_path) < 59:
        printc(f"  Output directory : \033[3m{output_path}\033[0m")
    else:
        printc(f"  Output directory : \033[3m...{output_path[-54:]}\033[0m")

    return output_path


def file_out_format():
    print(
        """  List supported image ouput format in GMT:
  1. |\033[38;5;81mbmp\033[00m| Microsoft Bit Map
  2. |\033[38;5;81meps\033[00m| Encapsulated PostScript
  3. |\033[38;5;81mjpg\033[00m| Joint Photographic Experts Group Format
  4. |\033[38;5;81mpdf\033[00m| Portable Document Format
  5. |\033[38;5;81mpng\033[00m| Portable Network Graphics \033[38;5;81m[Default]\033[00m
  6. |\033[38;5;81mPNG\033[00m| Portable Network Graphics (with transparency layer)
  7. |\033[38;5;81mppm\033[00m| Portable Pixel Map
  8. |\033[38;5;81mps \033[00m| Plain PostScript
  9. |\033[38;5;81mtif\033[00m| Tagged Image Format File

  Press enter for default 'png'."""
    )
    while True:
        input_file_format = input("  Format of the map: ").strip() or "png"
        match input_file_format:
            case "1" | "1." | "bmp":
                file_format = "bmp"
                break
            case "2" | "2." | "eps":
                file_format = "eps"
                break
            case "3" | "3." | "jpg":
                file_format = "jpg"
                break
            case "4" | "4." | "pdf":
                file_format = "pdf"
                break
            case "5" | "5." | "png":
                file_format = "png"
                break
            case "6" | "6." | "PNG":
                file_format = "PNG"
                break
            case "7" | "7." | "ppm":
                file_format = "ppm"
                break
            case "8" | "8." | "ps":
                file_format = "ps"
                break
            case "9" | "9." | "tif":
                file_format = "tif"
                break
            case _:
                print("\033[2A")
                printe(f"    '{input_file_format}' is not a valid output format")

    printc(f"  File output format = '{file_format}'")
    return file_format


def file_name(output_dir, file_format):
    while True:
        input_file_name = input("  Name of the map: ")
        input_file_name = input_file_name.replace(" ", "_")
        path = os.path.join(output_dir, f"{input_file_name}.{file_format}")
        check_file = os.path.isfile(path)

        if check_file == True:
            try:
                printe(
                    f"    The '{input_file_name}.{file_format}' in output folder, already exist"
                )
                overwrite = input("    Overwrite the file (y/n) ? ")
                if overwrite == "N" or overwrite == "n":
                    print("    Choose another name")
                    continue
                elif overwrite == "Y" or overwrite == "y":
                    print("\n    Map file will be overwrite!")
                    printc(f"  Map will be save as {input_file_name}.{file_format}")
                    break
            except:
                continue
                raise
        else:
            printc(f"  Map will be save as {input_file_name}.{file_format}")

            break
    return input_file_name


def input_projection():
    print("  Map Projection System (Press 'Enter' for default)")
    print("   (M) Mercator Cylindrical (default)")
    print("   (G) General perspective")
    while True:
        proj = input("  Enter the map projection:  ").strip() or "M"
        match proj.upper():
            case "M" | "Mercator":
                proj = "M"
                printc("  Map projection : Mercator")
                break
            case "G" | "General":
                proj = "G"
                printc("  Map projection : General Perspective")
                break
            case _:
                print("\033[2A")
                printe("    Please choose between 'M' or 'G'")

    return proj


def input_size():
    print("  Map size represent the width of the map in centimeter (cm)")
    print("  The height will adjust to the coordinate boundary")
    print("  Default size = 20 cm")
    while True:
        try:
            size = float(input("  Enter the map size:  ").strip() or 20)
            if size > 50:
                print("\033[2A")
                printe("    Error, 'size' must be less than '50'")
                continue
            elif size < 0:
                print("\033[2A")
                printe("    Error, the map 'size' can not negative")
            elif size > 0 and size < 5:
                print("\033[2A")
                printe("    Error, the map 'size' too small")
            else:
                printc("  Map width is = {} cm".format(size))
                break
        except ValueError:
            print("\033[2A")
            printe("    '{size}' is not a valid input, enter numbers only!")
            continue

    return size


def input_country_id():
    print("  Country ID is based on the ISO 3166 international standard")
    print(
        """  For example:
          (ID) for Indonesia
          (US) for United States of America
          (JP) for Japan"""
    )
    while True:
        country_id = input("  Please type the country ID:  ")
        if not re.match("^[A-Z]*$", country_id):
            print("\033[2A")
            printe("    Error! Only capital letters allowed!")

        elif len(country_id) > 2:
            print("\033[2A")
            printe("    Error! Only 2 characters allowed!")

        else:
            break

    return f"-R{country_id}"


ERROR_NUM = "    Error, input number only"


def input_coord_x():
    def get_boundary(prompt, default):
        while True:
            try:
                boundary = float(input(prompt).strip() or default)
                if -180 <= boundary <= 180:
                    return boundary
                else:
                    print("\033[2A")
                    printe("    W-E coordinate range -180 to 180 degree")
            except ValueError:
                print("\033[2A")
                printe("  Input numbers only!")

    while True:
        bound_x1 = get_boundary("  Western boundary (W): ", 107)
        bound_x2 = get_boundary("  Eastern boundary (E): ", 108)

        if bound_x1 < bound_x2:
            printc(f"  Longitude : {bound_x1}  -  {bound_x2} ")
            return bound_x1, bound_x2
        else:
            print("\033[2A")
            printe("\n    Western boundary must be less than eastern boundary\n")


def input_coord_y():
    def get_boundary(prompt, default):
        while True:
            try:
                boundary = float(input(prompt).strip() or default)
                if -90 <= boundary <= 90:
                    return boundary
                else:
                    print("\033[2A")
                    printe("    N-S coordinate range -90 to 90 degree")
            except ValueError:
                print("\033[2A")
                printe("  Input numbers only!")

    while True:
        bound_y1 = get_boundary("  Southern boundary (S): ", -7)
        bound_y2 = get_boundary("  Northern boundary (N): ", -6)

        if bound_y1 < bound_y2:
            printc(f"  Latitude : {bound_y1}  -  {bound_y2} ")
            return bound_y1, bound_y2
        else:
            print("\033[2A")
            printe("\n    Southern boundary must be less than northern boundary\n")


def color_rgb_chart():
    display_rgb_chart = input("  Display the 'Color Chart' from GMT (y/n) ?:  ")
    match display_rgb_chart.upper():
        case "Y" | "YES":
            utils.pictureshow(
                os.path.join(os.path.dirname(__file__), "data", "GMT_RGBchart.png")
            )


def color_land():
    print("  press 'enter' for default color (seagreen2)")
    while True:
        colr_land = str(input("  Choose the color of the land :") or "seagreen2")
        if colr_land.upper() not in unique_color:
            print("\033[2A")
            printe(f"    '{colr_land}' is not a valid color name in GMT")
            color_rgb_chart()

        else:
            break

    return colr_land.lower()


def color_sea():
    print("  press 'enter' for default color (lightcyan)")
    while True:
        colr_sea = str(input("  Choose the color of the sea : ") or "lightcyan")
        if colr_sea.upper() not in unique_color:
            print("\033[2A")
            printe(f"    '{colr_sea}' is not a valid color name in GMT")
            color_rgb_chart()

        else:
            break
    return colr_sea


def color_focmec():
    print("  press 'enter' for default color (red)")
    colr_fm = str(input("  Choose the color of the beach ball : ") or "red")
    return colr_fm


def contour_interval(mapscale):
    """Input the contour interval and return the used interval value and earth relief resolution"""
    match mapscale:
        case num if num < 2778:
            recom = 6.25
            resolution = "01s"
        case num if num in range(2778, 27775):
            recom = 12.5
            resolution = "03s"
        case num if num in range(27775, 60000):
            recom = 25
            resolution = "15s"
        case num if num in range(60000, 110000):
            recom = 50
            resolution = "30s"
        case num if num in range(110000, 277750):
            recom = 100
            resolution = "30s"
        case num if num in range(277750, 555500):
            recom = 125
            resolution = "30s"
        case num if num in range(555500, 2777750):
            recom = 250
            resolution = "01m"
        case num if num >= 2777750:
            recom = 500
            resolution = "02m"

    print("  Contour line is annotate every 4 interval")
    print(f"  For this map, interval recomendation = {recom} meter")
    while True:
        interval = float(input("  Type in the contour interval:  ").strip() or recom)
        if interval < recom:
            printe(
                "    The contour interval might be too tight, proceed with cautions.."
            )
            break
        elif interval > 1500.0:
            print("\033[2A")
            printe("    The contour interval is too large..")

        elif interval < 1500.0 and interval >= recom:
            break
        else:
            print("\033[2A")
            printe(f"    '{interval}' is not a valid input..")

    printc(f"  The contour interval is {interval} meters")
    return interval, resolution


def grdimage_color_palette():
    display_cpt = (
        input("  Display the 'Color Palette Tables' from GMT (y/n) ?:  ").strip() or "n"
    )
    match display_cpt.upper():
        case "Y" | "YES":
            utils.pictureshow(
                os.path.join(
                    os.path.dirname(__file__), "data", "GMT_Color_Palette_Tables.png"
                )
            )

    print("\n  List of CPT name:")
    pl = Cmd()
    pl.columnize(palette_name, displaywidth=80)

    while True:
        colr_cpt = input("  Choose the CPT:  ").lower()
        if colr_cpt in palette_name:
            printc(f"  '{colr_cpt}' is used for the color palette table")
            break
        elif colr_cpt not in palette_name:
            print("\033[2A")
            printe(f"    '{colr_cpt}' is not a valid cpt name in GMT")
            continue
        if colr_cpt == "jet":
            colr_cpt = "matlab/jet"
        if colr_cpt == "paired" or colr_cpt == "panoply":
            printe(f"    '{colr_cpt}' is not not supported")

    return colr_cpt


def grdimage_shading():
    while True:
        shade = input("  Shade the elevation model (y/n)?  ").strip() or "y"
        if shade.lower() == "y" or shade == "yes":
            shading = "-I+d"
            shade = "Yes"
            printc("  The earth relief will shaded")
            break
        elif shade.lower() == "n" or shade == "no":
            shading = ""
            shade = "No"
            printc("  The earth relief will not shaded")
            break
        else:
            print("\033[2A")
            printe(f"    '{shade}' is not a valid input..")

    return shading, shade


def grdimage_resolution():
    while True:
        print("  Choose the image resolution")
        print(
            """  SRTMGL1 (internet connection needed)
            1. Full   (01 second)
            2. High   (15 second)
            3. Medium (01 minute)
            4. Low    (05 minute)
            5. Crude  (10 minute)
            """
        )
        grd_resolution = input("  Image resolution: ").strip() or "2"
        match grd_resolution:
            case "1" | "Full" | "full":
                resolution = "@earth_relief_01s"
                grd_res = "1 second"
                printc("  using the 'full' image resolution (1 second)")
                break
            case "2" | "High" | "high":
                resolution = "@earth_relief_15s"
                grd_res = "15 second"
                printc("  using the 'high' image resolution (15 seconds)")
                break
            case "3" | "Medium" | "medium":
                resolution = "@earth_relief_01m"
                grd_res = "1 minute"
                printc("  using the 'medium' image resolution (1 minute)")
                break
            case "4" | "low" | "Low":
                resolution = "@earth_relief_05m"
                grd_res = "5 minute"
                printc("  using the 'low' image resolution (5 minutes)")
                break
            case "5" | "Crude" | "crude":
                resolution = "@earth_relief_10m"
                grd_res = "10 minute"
                printc("  using the 'crude' image resolution (10 minutes)")
                break
            case _:
                print("\033[2A")
                printe(f"    Error, {grd_resolution} is not a valid input.. ")

    return resolution, grd_res


def grdimage_mask():
    while True:
        mask = input("  Masking the sea surface (y/n)?  ").strip() or "y"
        if mask.lower() == "y" or mask == "yes":

            printc("  The sea surface will be masked")
            mask = True
            break
        elif mask.lower() == "n" or mask == "no":

            mask = False
            printc("  The sea surface will not be masked")
            break
        else:
            print("\033[2A")
            printe(f"    {mask} is not a valid input..")

    return mask


def date_start(req_type):
    while True:
        input_date_start = (
            input(
                f"  Enter start date for the {req_type} \n(YYYYMMDD) for full date or\n(YYYY) for year only (1 Jan) :   "
            ).strip()
            or "2019"
        )

        if not re.match(r"^\d*$", input_date_start):
            print("\033[3A")
            printe(ERROR_NUM)
            continue

        if len(input_date_start) not in [4, 8]:
            print("\033[3A")
            printe("    Error, input 4 or 8 characters for the year or date!")
            continue

        try:
            if len(input_date_start) == 4:
                year_start = int(input_date_start)
                mo_start, day_start = 1, 1
            else:
                year_start = int(input_date_start[:4])
                mo_start = int(input_date_start[4:6])
                day_start = int(input_date_start[6:])

            input_date_start = date(year_start, mo_start, day_start)

            if date.today() < input_date_start:
                print("\033[3A")
                printe("    Start date cannot be in the future")
                continue

            printc(f"  Start date :  {input_date_start.strftime('%B %d, %Y')}")
            break

        except ValueError as error:
            print("\033[3A")
            printe(f"    Error, {error}!")
            continue

    return input_date_start


def date_end(req_type):
    while True:
        input_date_end = (
            input(
                f"  Enter end date for the {req_type} \n(YYYYMMDD) for full date or\n(YYYY) for year only (31 Dec) :  "
            ).strip()
            or "2023"
        )

        if not re.match(r"^\d*$", input_date_end):
            print("\033[3A")
            printe(ERROR_NUM)
            continue

        if len(input_date_end) not in [4, 8]:
            print("\033[3A")
            printe("    Error, input 4 or 8 characters for the year or date!")
            continue

        try:
            if len(input_date_end) == 4:
                year_end = int(input_date_end)
                mo_end, day_end = 12, 31
            else:
                year_end = int(input_date_end[:4])
                mo_end = int(input_date_end[4:6])
                day_end = int(input_date_end[6:])

            input_date_end = date(year_end, mo_end, day_end)
            printc(f"  End date :  {input_date_end.strftime('%B %d, %Y')}")
            break

        except ValueError as error:
            print("\033[3A")
            printe(f"    Error, {error}!")
            continue

    return input_date_end


def date_start_end(*args):
    req_type = args[0]
    while True:
        in_date_start = date_start(req_type)
        in_date_end = date_end(req_type)
        delta = in_date_end - in_date_start
        days = delta.days
        if days <= 0:
            printe("    Error, the end time must later than the start time")

        else:
            printc(
                f"  The data used is {days} days from {in_date_start.strftime('%B %d, %Y')} to {in_date_end.strftime('%B %d, %Y')}"
            )
            break
    return in_date_start, in_date_end, days


def inset_loc():
    while True:
        print("         Inset map plot location:          ")
        print(" __________________________________________ ")
        print(" |    (1)   |   |    (2)   |   |    (3)   |")
        print(" |__________|   |__________|   |__________|")
        print(" |___________    ___________    __________|")
        print(" |    (4)   |   |    (5)   |   |    (6)   |")
        print(" |__________|   |__________|   |__________|")
        print(" |___________    ___________    __________|")
        print(" |    (7)   |   |    (8)   |   |    (9)   |")
        print(" |__________|___|__________|___|__________|\n")
        justify = input("Enter the location of map inset:  ")
        match justify:
            case "1":
                justify = "TL"
                just_code = "Top Left"
                break
            case "2":
                justify = "TC"
                just_code = "Top Center"
                break
            case "3":
                justify = "TR"
                just_code = "Top Right"
                break
            case "4":
                justify = "ML"
                just_code = "Mid Left"
                break
            case "5":
                justify = "MC"
                just_code = "Mid Center"
                break
            case "6":
                justify = "MR"
                just_code = "Mid Right"
                break
            case "7":
                justify = "BL"
                just_code = "Bot Left"
                break
            case "8":
                justify = "BC"
                just_code = "Bot Center"
                break
            case "9":
                justify = "BR"
                just_code = "Bot Right"
                break
            case _:
                print("\033[2A")
                printe("    Error, choose between 1 - 9 !")

    if justify == "TR":
        just_north = "TL"
    else:
        just_north = "TR"
    return justify, just_north, just_code


def eq_mag_range(req_type):
    DEFAULT = "  \x1B[3m(press 'enter' for default value)\x1b[0m  :   "

    def get_magnitude(prompt, default):
        while True:
            try:
                print(prompt)
                magnitude = int(input(DEFAULT).strip() or default)
                if 0 <= magnitude <= 10:
                    return magnitude
                else:
                    print("\033[3A")
                    printe("    Magnitude range between 0 to 10")
            except ValueError:
                print("\033[3A")
                printe("    Error, input numbers only!")

    while True:
        min_eq_mag = get_magnitude(
            f"  Enter the minimum magnitude for the {req_type}", "0"
        )
        max_eq_mag = get_magnitude(
            f"  Enter the maximum magnitude for the {req_type}", "10"
        )

        if min_eq_mag < max_eq_mag:
            printc(f"  Magnitude = {min_eq_mag} - {max_eq_mag} ")
            return min_eq_mag, max_eq_mag
        else:
            print("\033[3A")
            printe("\n    The minimum magnitude must be lower than the maximum\n")


def eq_depth_range(req_type):
    DEFAULT = "  \x1B[3m(press 'enter' for default value)\x1b[0m  :   "

    def get_depth(prompt, default):
        while True:
            try:
                print(prompt)
                depth = int(input(DEFAULT).strip() or default)
                if 0 <= depth <= 1000:
                    return depth
                else:
                    print("\033[3A")
                    printe("    The depth range between 0 to 1000")
            except ValueError:
                print("\033[3A")
                printe("    Error, input numbers only!")

    while True:
        min_eq_depth = get_depth(f"  Enter the minimum depth for the {req_type}", "0")
        max_eq_depth = get_depth(
            f"  Enter the maximum depth for the {req_type}", "1000"
        )

        if min_eq_depth < max_eq_depth:
            printc(f"  Depth = {min_eq_depth} - {max_eq_depth} Km")
            return min_eq_depth, max_eq_depth
        else:
            print("\033[3A")
            printe("\n    Minimum depth must be lower than maximum\n")


def eq_catalog_source():
    print("  Choose the earthquake catalog service: ")
    print("    1. USGS - NEIC PDE")
    print("    2. ISC Bulletin")
    print("    3. User supplied")
    print("    0. Cancel")
    # print("  3. GlobalCMT")
    while True:
        eq_cata = input("  Earthquake catalog:  ")
        match eq_cata:
            case "1" | "1." | "USGS" | "usgs" | "NEIC":
                if utils.is_connected():
                    eq_cata = "USGS"
                    printc(
                        "  Using earthquake catalog from USGS Preliminary Determination of Epicenters"
                    )
                    break
                else:
                    print("\033[3A")
                    printe(
                        "    No internet connection, choose 'User supplied' or cancel"
                    )

            case "2" | "2." | "ISC" | "isc" | "ISC Bulletin":
                if utils.is_connected():
                    eq_cata = "ISC"

                    printc(
                        "  using earthquake catalog from International Seismology Centre Bulletin"
                    )
                    break
                else:
                    print("\033[3A")
                    printe(
                        "    No internet connection, choose 'User supplied' or cancel"
                    )

            case "3" | "3." | "User supplied" | "user supplied" | "user":
                eq_cata = "From user"
                printc("  using earthquake catalog from Global Centroid Moment Tensor")
                break
            # case "3" | "3." | "GCMT" | "gcmt" | "GlobalCMT":
            #     eq_cata = "GlobalCMT"
            #     print("using earthquake catalog from Blobal Centroid Moment Tensor")
            #     break
            case "0" | "0." | "Cancel" | "cancel" | "CANCEL":
                eq_cata = "cancel"
                break
            case _:
                print("\033[2A")
                printe("    Error, pleace choose correctly..")

    return eq_cata


def eq_legend():
    calculation = 10
    return calculation


def load_eq():
    print("  Loading the earthquake data from user")

    eq_path = askopenfilename(
        initialdir=os.getcwd(),
        filetypes=(
            ("txt files..    ", "*.txt"),
            ("csv files..   ", "*.csv"),
            ("dat files..   ", "*.dat"),
            ("all types..   ", "*"),
        ),
        title="  Open earthquake data location",
    )

    printc(f"Earthquake data : {eq_path}")
    return eq_path


def column_order(eq_path):

    # file name, longitude, lattitude, magnitude, depth
    print("  column order separate with space and the first column start from 1")
    print("  data required : longitude, lattitude, depth, magnitude")
    # print("6 column if date and time in different column, or 5 if combined")
    print("  for example: 1 2 3 4 ")
    print("  |longitude|--|lattitude|--|depth|--|magnitude|--|Date-Time|")
    while True:
        eq_column_order = list(map(input("  the column order:  ").strip().split))[:4]
        eq_column_lon = eq_column_order[0]
        eq_column_lat = eq_column_order[1]
        eq_column_dep = eq_column_order[2]
        eq_column_mag = eq_column_order[3]
        col_check = eq_column_check(eq_path, eq_column_order)
        if col_check[0] == "good":
            break
        else:
            print("\033[1A")
            printe("    The column order not match with the data")

    return eq_column_lon, eq_column_lat, eq_column_dep, eq_column_mag, col_check


def eq_column_check(eq_path, column_order):
    print(eq_path, column_order)
    with open(eq_path) as f:
        for columns in f:
            lon = columns[{column_order[0]}]
            if lon < -180 or lon > 180:
                print("\033[1A")
                printe(
                    "    Error: longitude value should between -180 and 180 degree. \n    Check the column order"
                )
                status = "bad"
                break

            lat = columns[{column_order[1]}]
            if lat < -90 or lat > 90:
                print("\033[1A")
                printe(
                    "    Error: lattitude value should between -90 and 90 degree. \n    Check the column order"
                )
                status = "bad"
                break
            eq_data_dep = []
            depth = columns[{column_order[2]}]
            if depth < 0 or depth > 1000:
                print("\033[1A")
                printe(
                    "    Error: depth value should between 0 and 1000 km. \n    Check the column order"
                )
                status = "bad"
                break
            else:
                eq_data_dep.append(depth)
            eq_data_mag = []
            mag = columns[{column_order[3]}]
            if mag < 0 or mag > 10:
                print("\033[1A")
                printe(
                    "    Error: magnitude value should between 0 - 10. \n    Check the column order"
                )
                status = "bad"
                break
            else:
                eq_data_mag.append(mag)
                status = "good"
    return (
        status,
        min(eq_data_dep),
        max(eq_data_dep),
        min(eq_data_mag),
        max(eq_data_mag),
    )
