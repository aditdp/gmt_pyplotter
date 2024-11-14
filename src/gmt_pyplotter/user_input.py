from cmd import Cmd
from datetime import date
from tkinter.filedialog import askopenfilename, askdirectory
import os.path
import re
import sys

from gmt_pyplotter import utils
from gmt_pyplotter.data.color_list import unique_color, palette_name

# import utils
# from data.color_list import unique_color, palette_name


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


def get_save_loc():
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
                    except KeyboardInterrupt:
                        raise SystemExit

    if os.name == "nt":
        output_path = output_path.replace("/", "\\")
    if len(output_path) < 59:
        printc(f"  Output directory : \033[3m{output_path}\033[0m")
    else:
        printc(f"  Output directory : \033[3m...{output_path[-54:]}\033[0m")

    return output_path


def get_file_name(output_dir):
    while True:
        input_file_name = input("  Name of the map: ") or "untitled_map"
        input_file_name = input_file_name.replace(" ", "_")
        for i in ["bmp", "eps", "jpg", "pdf", "png", "ppm", "ps"]:
            path = os.path.join(output_dir, f"{input_file_name}.{i}")
            check_file = os.path.isfile(path)

            if check_file is True:
                printe(
                    f"    The '{input_file_name}.{i}' in output folder, already exist"
                )
                overwrite = input("    Overwrite the file (y/n) ? ")
                if overwrite.upper() in ["N", "NO", ""]:
                    print("    Choose another name")
                    continue
                if overwrite.upper() in ["Y", "YES"]:
                    print("\n    Map file will be overwrite!")
                    printc(f"  Map will be save as {input_file_name}.{i}")
                    break
                else:
                    printe(f"    '{overwrite}' is not valid input")

            else:
                printc(f"  Map will be save as '{input_file_name}'")

                break
        return input_file_name


def get_file_out_format():
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


def get_projection():
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


def get_map_width():
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
                continue
            elif 0 < size < 5:
                print("\033[2A")
                printe("    Error, the map 'size' too small")
                continue
            else:
                printc(f"  Map width is = {size} cm")
                break
        except ValueError:
            print("\033[2A")
            printe("    '{size}' is not a valid input, enter numbers only!")
            continue

    return size


def get_country_id():
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


def get_coord_x():
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
        bound_x1 = get_boundary("  Western boundary (W): ", 106)
        bound_x2 = get_boundary("  Eastern boundary (E): ", 107)

        if bound_x1 < bound_x2:
            printc(f"  Longitude : {bound_x1}  -  {bound_x2} ")
            return bound_x1, bound_x2
        else:
            print("\033[2A")
            printe("\n    Western boundary must be less than eastern boundary\n")


def get_coord_y():
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
        bound_y1 = get_boundary("  Southern boundary (S): ", -8)
        bound_y2 = get_boundary("  Northern boundary (N): ", -6.8)

        if bound_y1 < bound_y2:
            printc(f"  Latitude : {bound_y1}  -  {bound_y2} ")
            return bound_y1, bound_y2
        else:
            print("\033[2A")
            printe("\n    Southern boundary must be less than northern boundary\n")


def show_color_rgb_chart():
    display_rgb_chart = input("  Display the 'Color Chart' from GMT (y/n) ?:  ")
    if display_rgb_chart.upper() in ["Y", "YES"]:
        utils.pictureshow(
            os.path.join(os.path.dirname(__file__), "data", "GMT_RGBchart.png")
        )


def get_color(use: str, default: str):
    print(f"  press 'enter' for default color ({default})")
    while True:
        color = str(input(f"  Choose the color of the {use} :") or f"{default}")
        if color.upper() not in unique_color:
            print("\033[2A")
            printe(f"    '{color}' is not a valid color name in GMT")
            show_color_rgb_chart()

        else:
            break

    return color.lower()


def get_contour_interval(mapscale):
    """Input the contour interval and return the used interval value and earth relief resolution"""
    # magic
    intervals = [
        (2778, 6.25, "01s"),
        (27775, 12.5, "03s"),
        (60000, 25, "15s"),
        (110000, 50, "30s"),
        (277750, 100, "30s"),
        (555500, 125, "30s"),
        (2777750, 250, "01m"),
        (float("inf"), 500, "02m"),
    ]

    for threshold, recomend, resolution in intervals:
        if mapscale < threshold:
            break

    print("  Contour line is annotate every 4 interval")
    print(f"  For this map, interval recomendation = {recomend} meter")
    while True:
        interval = float(input("  Type in the contour interval:  ").strip() or recomend)
        if interval < recomend:
            printe(
                "    The contour interval might be too tight, proceed with cautions.."
            )
            break
        elif interval > 1500.0:
            print("\033[2A")
            printe("    The contour interval is too large..")

        elif interval < 1500.0 and interval >= recomend:
            break
        else:
            print("\033[2A")
            printe(f"    '{interval}' is not a valid input..")

    printc(f"  The contour interval is {interval} meters")
    return interval, resolution


def get_grdimage_color_palette():
    display_cpt = (
        input("  Display the 'Color Palette Tables' from GMT (y/n) ?:  ").strip() or "n"
    )
    if display_cpt.upper() in ["Y", "YES"]:
        utils.pictureshow(
            os.path.join(
                os.path.dirname(__file__), "data", "GMT_Color_Palette_Tables.png"
            )
        )

    print("\n  List of CPT name:")
    pl = Cmd()
    pl.columnize(palette_name, displaywidth=80)

    while True:
        color_cpt = input("  Choose the CPT:  ").lower() or "world"
        if color_cpt in palette_name:
            printc(f"  '{color_cpt}' is used for the color palette table")
            break
        elif color_cpt not in palette_name:
            print("\033[2A")
            printe(f"    '{color_cpt}' is not a valid cpt name in GMT")
            continue
        if color_cpt == "jet":
            color_cpt = "matlab/jet"
        if color_cpt == "paired" or color_cpt == "panoply":
            printe(f"    '{color_cpt}' is not not supported")

    return color_cpt


def get_grdimage_shading():
    while True:
        shade = input("  Shade the elevation model (y/n)?  ").strip() or "y"
        if shade.lower() == "y" or shade == "yes":
            shading_code = "-I+d"
            shade = "Yes"
            printc("  The earth relief will shaded")
            break
        elif shade.lower() == "n" or shade == "no":
            shading_code = ""
            shade = "No"
            printc("  The earth relief will not shaded")
            break
        else:
            print("\033[2A")
            printe(f"    '{shade}' is not a valid input..")

    return shading_code, shade


def get_grdimage_resolution(map_scale):
    if map_scale == "large":
        strike = "\033[9m"
    else:
        strike = ""
    while True:
        print("  Choose the image resolution")
        print(
            f"""  SRTMGL1 (internet connection needed)
           {strike} 1. Full   (01 second) \033[0m
            2. Vhigh  (03 second)
            3. High   (15 second)
            4. Medium (01 minute)
            5. Low    (05 minute)
            6. Crude  (10 minute)
            """
        )
        grd_resolution = input("  Image resolution: ").strip() or "2"
        match grd_resolution.lower():
            case "1" | "full" if map_scale == "small":
                resolution = "@earth_relief_01s"
                grd_res = "1 second"
                printc("  using the 'full' image resolution (1 second)")
                break
            case "1" | "full" if map_scale == "large":
                printe("    The map size too large for this resolution")
                continue
            case "2" | "vhigh" | "v high" | "very high" | "v":
                resolution = "@earth_relief_03s"
                grd_res = "3 second"
                printc("  using the 'very high' image resolution (3 second)")
                break
            case "3" | "high":
                resolution = "@earth_relief_15s"
                grd_res = "15 second"
                printc("  using the 'high' image resolution (15 seconds)")
                break
            case "4" | "medium":
                resolution = "@earth_relief_01m"
                grd_res = "1 minute"
                printc("  using the 'medium' image resolution (1 minute)")
                break
            case "5" | "low":
                resolution = "@earth_relief_05m"
                grd_res = "5 minute"
                printc("  using the 'low' image resolution (5 minutes)")
                break
            case "6" | "crude":
                resolution = "@earth_relief_10m"
                grd_res = "10 minute"
                printc("  using the 'crude' image resolution (10 minutes)")
                break
            case _:
                print("\033[2A")
                printe(f"    Error, {grd_resolution} is not a valid input.. ")

    return resolution, grd_res


def get_grdimage_mask():
    while True:
        mask = input("  Masking the sea surface (y/n)?  ").strip() or "y"
        if mask.lower() in ["y", "yes"]:

            printc("  The sea surface will be masked")
            mask = True
            break
        elif mask.lower() in ["n", "no"]:

            mask = False
            printc("  The sea surface will not be masked")
            break
        else:
            print("\033[2A")
            printe(f"    {mask} is not a valid input..")

    return mask


def get_date_start(req_type: str):
    while True:
        date_start = (
            input(
                f"  Enter start date for the {req_type} \n(YYYYMMDD) for full date or\n(YYYY) for year only (1 Jan) :   "
            ).strip()
            or "2019"
        )

        if not re.match(r"^\d*$", date_start):
            print("\033[3A")
            printe(f"    '{date_start}' is not a valid input!")
            continue

        if len(date_start) not in [4, 8]:
            print("\033[3A")
            printe("    Error, input 4 or 8 characters for the year or date!")
            continue

        try:
            if len(date_start) == 4:
                year_start = int(date_start)
                mo_start, day_start = 1, 1
            else:
                year_start = int(date_start[:4])
                mo_start = int(date_start[4:6])
                day_start = int(date_start[6:])

            date_start = date(year_start, mo_start, day_start)

            if date.today() < date_start:
                print("\033[3A")
                printe("    Start date cannot be in the future")
                continue

            printc(f"  Start date :  {date_start.strftime('%B %d, %Y')}")
            break

        except ValueError as error:
            print("\033[3A")
            printe(f"    Error, {error}!")
            continue

    return date_start


def get_date_end(req_type: str):
    while True:
        date_end = (
            input(
                f"  Enter end date for the {req_type} \n(YYYYMMDD) for full date or\n(YYYY) for year only (31 Dec) :  "
            ).strip()
            or "2023"
        )

        if not re.match(r"^\d*$", date_end):
            print("\033[3A")
            printe(f"    '{date_end}' is not a valid input!")
            continue

        if len(date_end) not in [4, 8]:
            print("\033[3A")
            printe("    Error, input 4 or 8 characters for the year or date!")
            continue

        try:
            if len(date_end) == 4:
                year_end = int(date_end)
                mo_end, day_end = 12, 31
            else:
                year_end = int(date_end[:4])
                mo_end = int(date_end[4:6])
                day_end = int(date_end[6:])

            date_end = date(year_end, mo_end, day_end)
            printc(f"  End date :  {date_end.strftime('%B %d, %Y')}")
            break

        except ValueError as error:
            print("\033[3A")
            printe(f"    Error, {error}!")
            continue

    return date_end


def get_date_start_end(req_type: str):

    while True:
        in_date_start = get_date_start(req_type)
        in_date_end = get_date_end(req_type)
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


def get_tecto_source(map_scale):
    if map_scale == "small":
        recom = ["★", " ", " "]
    else:
        recom = [" ", "★", "★"]
    print("  Available tectonic/geological structure data:")
    print(f"   {recom[0]} 1. Compiled from Geological Maps of Indonesia 1:250,000")
    print(
        f"   {recom[1]} 2. Regional Geological Maps of Indonesia (Sukamto et al, 2011)"
    )
    print(f"   {recom[2]} 3. Active Fault Maps of Indonesia (Soehaemi et al, 2021)")
    print("\n   ★ = recomended based on map size")
    while True:
        source = input("  Select the tectonic data source (1/2/3):  ")
        if source in ["1", "1.", "*1", "*1."]:
            source = "Indo-compiled"
        elif source in ["2", "2.", "*2", "*2."]:
            source = "Sukamto, 2011"
        elif source in ["3", "3.", "*3", "*3."]:
            source = "Soehaemi, 2021"
        else:
            printe(f"    '{source}' is not valid input, choose between 1, 2, or 3")
            continue
        return source


def get_inset_loc():
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
            case "1" | "1." | "(1)":
                justify = "TL"
                just_code = "Top Left"
                break
            case "2" | "2." | "(2)":
                justify = "TC"
                just_code = "Top Center"
                break
            case "3" | "3." | "(3)":
                justify = "TR"
                just_code = "Top Right"
                break
            case "4" | "4." | "(4)":
                justify = "ML"
                just_code = "Mid Left"
                break
            case "5" | "5." | "(5)":
                justify = "MC"
                just_code = "Mid Center"
                break
            case "6" | "6." | "(6)":
                justify = "MR"
                just_code = "Mid Right"
                break
            case "7" | "7." | "(7)":
                justify = "BL"
                just_code = "Bot Left"
                break
            case "8" | "8." | "(8)":
                justify = "BC"
                just_code = "Bot Center"
                break
            case "9" | "9." | "(9)":
                justify = "BR"
                just_code = "Bot Right"
                break
            case _:
                print("\033[2A")
                printe("    Error, choose between 1 - 9 !")

    return justify, just_code


def get_eq_mag_range(req_type):
    DEFAULT = "  \x1B[3m(press 'enter' for default value)\x1b[0m  :   "

    def get_magnitude(prompt, default):
        while True:
            try:
                print(prompt)
                magnitude = int(input(DEFAULT).strip() or default)
                if 1 < magnitude <= 10:
                    return magnitude
                else:
                    print("\033[3A")
                    printe("    Magnitude range between 1 to 10")
            except ValueError:
                print("\033[3A")
                printe("    Error, input numbers only!")

    while True:
        min_eq_mag = get_magnitude(
            f"  Enter the minimum magnitude for the {req_type}", "3"
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


def get_eq_depth_range(req_type):
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


def get_eq_catalog_source():
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


def get_eq_directory():
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
    if len(eq_path) > 60:
        print_path = f"...{eq_path[-58:]}"
    else:
        print_path = eq_path
    printc(f"  Earthquake data : {print_path}")
    return eq_path


def get_user_data_delimiter():
    delimiters = [",", "\t", ";", "|", ":", " "]
    delimiter_names = {
        ",": "Comma     ",
        ";": "Semicolon ",
        ":": "Colon     ",
        "|": "Pipe      ",
        "\t": "Tab       ",
        " ": "Space     ",
    }

    print("  Available delimiters:")
    for i, delimiter in enumerate(delimiters, start=1):

        display_delimiter = repr(delimiter)
        delimiter_name = delimiter_names.get(delimiter, "Unknown")
        print(f"    {i}.  {delimiter_name} ({display_delimiter})")

    while True:
        try:
            user_choice = int(input("Please choose a delimiter by number: ")) - 1
            if 0 <= user_choice < len(delimiters):
                user_delimiter = delimiters[user_choice]

                return user_delimiter

            else:
                print(
                    f"Invalid choice. Please enter a number between 1 and {len(delimiters)}."
                )
        except ValueError:
            print(
                f"Invalid input. Please enter a number between 1 and {len(delimiters)}."
            )


def get_column_order(eq_path):
    """User inputing column order for lon lat dep mag,
    return data status "good"/"bad" and list column index  [lon, lat, dep, mag]"""

    # file name, longitude, lattitude, magnitude, depth
    print("\n  Reorder the earthquake data column\n")
    print(
        " \033[38;5;227m column order : longitude, lattitude, depth, magnitude,\033[0m additional: Date/Time"
    )
    # print("6 column if date and time in different column, or 5 if combined")
    print("  For example, column order of USGS data :")
    print("  0                         1         2          3      4    5     ")
    print("  time,                     latitude, longitude, depth, mag, magType,...")
    print("  2023-12-13T23:35:10.892Z, -6.8597,  106.5246,  10.4,  4.5, mb,,....")
    print("  2023-12-07T19:00:46.583Z, -6.985,   106.5272,  8.978, 4,   mb,....")
    print("\n \033[38;5;227m Input as:  2,1,3,4,0 \033[0m\n")

    print("\n  The first 6 row of 'user' data :")
    print("_ " * 40)
    with open(eq_path, "r", encoding="utf-8") as sample:
        for _ in range(6):
            line = sample.readline().strip()
            if line:
                print(f"    {line[:74]}")
            else:

                break
    print("_ " * 40)
    print("")
    while True:
        eq_column_order = input(
            f"  the column order(lon,lat,dep,mag,[time]/[date,time]): "
        )
        eq_column_order = [int(num.strip()) for num in eq_column_order.split(",")]
        if len(eq_column_order) != len(set(eq_column_order)):
            printe("    Error, no column duplicate allowed..")
            continue
        col_check = check_eq_column(eq_path, eq_column_order[:4])
        if col_check == "bad":
            print("\033[1A")
            printe("    The column order not match with the data")
            try_again = input("    Try again (y/n)? ").strip() or "y"
            if try_again.lower() in ["n", "no", "na"]:
                break
            else:
                continue
        else:
            break

    return col_check, eq_column_order


def check_eq_column(eq_path, order: list):
    """Check every column if its match the data (lon, lat, depth, magnitude)"""
    try:
        delimiter = get_user_data_delimiter()

    except:
        printe("    The delimiter is not correct..")

    with open(eq_path, encoding="utf-8") as f:
        f.readline()
        for line in f:
            columns = line.strip().split(delimiter)

            lon = float(columns[order[0]].strip())
            if int(lon) < -180 or int(lon) > 180:
                print("\033[1A")
                printe(
                    "    Error: longitude value should between -180 and 180 degree. \n    Check the column order"
                )
                status = "bad"
                break

            lat = float(columns[order[1]].strip())
            if int(lat) < -90 or int(lat) > 90:
                print("\033[1A")
                printe(
                    "    Error: lattitude value should between -90 and 90 degree. \n    Check the column order"
                )
                status = "bad"
                break

            depth = float(columns[order[2]].strip())
            if int(depth) < 0 or int(depth) > 1000:
                print("\033[1A")
                printe(
                    "    Error: depth value should between 0 and 1000 km. \n    Check the column order"
                )
                status = "bad"
                break

            mag = float(columns[order[3]].strip())
            if int(mag) < 0 or int(mag) > 10:
                print("\033[1A")
                printe(
                    "    Error: magnitude value should between 0 - 10. \n    Check the column order"
                )
                status = "bad"
                break

            status = "good"
    return status
