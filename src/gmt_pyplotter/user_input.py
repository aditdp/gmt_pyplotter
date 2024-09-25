import os.path, re, sys, utils
from data.color_list import unique_color, palette_name
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


def save_loc():
    print("\n  Select the output (figure, gmt script & another data) directory ..\n")
    while True:
        output_path = askdirectory(
            initialdir=os.getcwd(),
            mustexist=True,
            title="  Select the output directory",
        )
        if output_path:
            break
        else:
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

    printc(f"  Output directory : \033[3m{output_path}\033[0m")

    return output_path


def file_name(output_dir):
    while True:
        input_file_name = input("  Name of the map: ")
        path = os.path.join(output_dir, f"{input_file_name}.png")
        check_file = os.path.isfile(path)

        if check_file == True:
            try:
                printe(
                    f"    The '{input_file_name}.png' in output folder, already exist"
                )
                overwrite = input("    Overwrite the file (y/n) ? ")
                if overwrite == "N" or overwrite == "n":
                    print("    Choose another name")
                    continue
                elif overwrite == "Y" or overwrite == "y":
                    print("\n    Map file will be overwrite!")
                    break
            except:
                continue
        else:
            printc(f"  Map will be save as {input_file_name}.png")

            break
    return input_file_name


def input_projection():
    print("  Map Projection System (Press 'Enter' for default)")
    print("   (M) Mercator Cylindrical (default)")
    print("   (G) General perspective")
    while True:
        proj = input("  Enter the map projection:  ")
        match proj:
            case "":
                proj = "M"
                printc("Map projection : Mercator")
                break
            case "M" | "m":
                proj = "M"
                printc("Map projection : Mercator")
                break
            case "G" | "g":
                proj = "G"
                printc("Map projection : General Perspective")
                break
            case _:
                printe("    Please choose between 'M' or 'G'")
                continue
    return proj


def input_size():
    print("  Map size represent the width of the map in centimeter (cm)")
    print("  the height will adjust to the coordinate boundary")
    while True:
        try:
            size = float(input("  Enter the map size:  ").strip() or "20")
            if size > 50:
                printe("    Error, the map 'size' too large")
                printe("    'size' must be less than '50'")
                continue
            elif size < 0:
                printe("    Error, the map 'size' can not negative")
            elif size > 0 and size < 5:
                printe("    Error, the map 'size' too small")
            else:
                printc("  Map width is = {} cm".format(size))
                break
        except ValueError:
            printe("    Error, enter integers only!")
            continue

    return size


def color_rgb_chart():
    display_rgb_chart = input(
        "  Display the 'Color Palette Tables' from GMT (y/n) ?:  "
    )
    match display_rgb_chart:
        case "y" | "yes" | "Y" | "Yes" | "YES":
            utils.pictureshow(
                os.path.join(os.path.dirname(__file__), "data", "GMT_RGBchart.png")
            )
        case _:
            pass


def color_land():
    print("  leave empty for default color (seagreen2)")
    while True:
        colr_land = str(input("  Choose the color of the land :") or "seagreen2")
        if colr_land not in unique_color:
            printe(f"    '{colr_land}' is not a valid color name in GMT")
            color_rgb_chart()
            continue
        else:
            break

    return colr_land


def color_sea():
    print("  leave empty for default color (lightcyan)")
    while True:
        colr_sea = str(input("  Choose the color of the sea : ") or "lightcyan")
        if colr_sea not in unique_color:
            printe(f"    '{colr_sea}' is not a valid color name in GMT")
            color_rgb_chart()
            continue
        else:
            break
    return colr_sea


def color_focmec():
    print("  leave empty for default color (red)")
    colr_fm = str(input("  Choose the color of the beach ball : ") or "red")
    return colr_fm


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
            printe("    Error! Only capital letters allowed!")
            continue
        elif len(country_id) > 2:
            printe("    Error! Only 2 characters allowed!")
            continue
        else:
            break

    return f"-R{country_id}"


def input_coord_x():
    """fungsi input koordinat peta dengan geographical projection"""

    while True:
        try:
            bound_x1 = float(input("  Western boundary (W): ").strip() or 120)
            if bound_x1 < -180 or bound_x1 > 180:
                printe("    W-E coordinate range -180 to 180 degree")
                continue
        except ValueError:
            print("    Input numbers only!")
            continue

        try:
            bound_x2 = float(input("  Eastern boundary (E): ").strip() or 125)
            if bound_x2 < -180 or bound_x2 > 180:
                printe("    W-E coordinate range -180 to 180 degree")
                continue
        except ValueError:
            printe("  Input numbers only!")
            continue
        if bound_x1 >= bound_x2:
            printe("\n    Western boundary must lesser than eastern boundary\n")
            continue
        elif bound_x1 <= bound_x2:
            printc(f"  Longitude : {bound_x1}  -  {bound_x2} ")
            break
    return bound_x1, bound_x2


def input_coord_y():
    while True:
        try:
            bound_y1 = float(input("  Southern boundary (S): ").strip() or -9)
            if bound_y1 < -90 or bound_y1 > 90:
                printe("    N-S coordinate range -90 to 90 degree")
                continue
        except ValueError:
            printe("    Input numbers only!")
            continue

        try:
            bound_y2 = float(input("  Northern boundary (N): ").strip() or -4)
            if bound_y2 < -90 or bound_y2 > 90:
                printe("    N-S coordinate range -90 to 90 degree")
                continue
        except ValueError:
            printe("    Input numbers only!")
            continue

        if bound_y1 >= bound_y2:
            printe("\n    Southern boundary must lesser than northern boundary\n")
            continue
        elif bound_y1 <= bound_y2:
            printc(f"  Lattitude : {bound_y1}  -  {bound_y2} ")
            break
    return bound_y1, bound_y2


def color_palette():
    display_cpt = input("  Display the 'Color Palette Tables' from GMT (y/n) ?:  ")
    match display_cpt:
        case "y" | "yes" | "Y" | "Yes" | "YES":
            utils.pictureshow(
                os.path.join(
                    os.path.dirname(__file__), "data", "GMT_Color_Palette_Tables.png"
                )
            )
        case _:
            pass

    print(f"\n  List of CPT name:")
    pl = Cmd()
    pl.columnize(palette_name, displaywidth=80)

    while True:
        colr_cpt = input("  Choose the CPT:  ")
        if colr_cpt in palette_name:
            printc(f"  {colr_cpt} is used for the color palette table")
            break
        elif colr_cpt not in palette_name:
            printe(f"    {colr_cpt} is not a valid cpt name in GMT")
            continue
    return colr_cpt


def grdimage_shading():
    while True:
        shade = input("  Shade the elevation model (y/n)?  ")
        if shade == "y" or shade == "Y":
            shading = "-I+d"
            shade = "Yes"
            printc("  The earth relief will shaded")
            break
        elif shade == "n" or shade == "N":
            shading = ""
            shade = "No"
            printc("  The earth relief will not shaded")
            break
        else:
            printe("    Not a valid input..")
            continue
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
        grd_resolution = input("  Image resolution: ")
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
                printe("    error, please choose correctly..")
                continue

    return resolution, grd_res


def grdimage_mask():
    while True:
        mask = input("  Masking the sea surface (y/n)?  ")
        if mask == "y" or mask == "Y":

            mask = "Yes"
            printc("  The sea surface will be masked")
            break
        elif mask == "n" or mask == "N":

            mask = "No"
            printc("  The sea surface will not be masked")
            break
        else:
            printe("    Not a valid input..")
            continue
    return mask


def date_start(*args):
    req_type = args[0]
    while True:
        print(80 * ".")
        input_date_start = input(
            (
                f"  Enter start date for the {req_type} \n(YYYYMMDD) for full date or\n(YYYY) for year only (1 Jan) :   "
            ).strip()
            or "20190101"
        )
        if not re.match("^[0-9]*$", input_date_start):
            printe("    Error, input numbers only!")
            continue
        elif len(input_date_start) != 8 or len(input_date_start) != 4:
            printe("    Error, input 4 or 8 characters for the year or date !")
        else:
            if len(input_date_start) == 4:
                year_start = int(input_date_start)
                mo_start = 1
                day_start = 1
            elif len(input_date_start) == 8:
                year_start = int(input_date_start[0:4])
                mo_start = int(input_date_start[4:6])
                day_start = int(input_date_start[6:])
            try:
                input_date_start = date(year_start, mo_start, day_start)
                if date.today() - input_date_start < 0:
                    printe("    Start date cannot from future")
                    continue
                else:
                    printc("  Start date : ", input_date_start.strftime("%B %d, %Y"))
                    break

            except ValueError as error:
                printe(f"    Error, {error}!")
                continue

    return input_date_start


def date_end(*args):
    req_type = args[0]
    while True:
        print(80 * ".")
        input_date_end = input(
            (
                f"  Enter end date for the {req_type} \n(YYYYMMDD) for full date or\n(YYYY) for year only (31 Dec) :  "
            ).strip()
            or "  20240101"
        )
        if not re.match("^[0-9]*$", input_date_end):
            printe("    Error, input numbers only!")
            continue
        elif len(input_date_end) != 4 or len(input_date_end) != 8:
            printe("    Error, input 4 or 8 characters for the year or date !")
        else:
            if len(input_date_end) == 4:
                year_end = int(input_date_end)
                mo_end = 12
                day_end = 31
            elif len(input_date_end) == 8:
                year_end = int(input_date_end[0:4])
                mo_end = int(input_date_end[4:6])
                day_end = int(input_date_end[6:])
            try:
                input_date_end = date(year_end, mo_end, day_end)
                printc("  End date : ", input_date_end.strftime("%B %d, %Y"))

                break
            except ValueError as error:
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
            continue
        else:
            printc(
                f"  The data used is {days} days from ",
                in_date_start.strftime("%B %d, %Y"),
                "to",
                in_date_end.strftime("%B %d, %Y"),
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
        print(" |__________|___|__________|___|__________|")
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
                printe("    Error, choose between 1 - 9 !")
                continue
    if justify == "TR":
        just_north = "TL"
    else:
        just_north = "TR"
    return justify, just_north, just_code


def eq_mag_range(*args):
    req_type = args[0]
    while True:
        try:
            print(80 * ".")
            print(f"  Enter the minimum magnitude for the {req_type}")
            min_eq_mag = int(
                input("  \x1B[3m(leave empty for default value)\x1b[0m  :   ").strip()
                or "0"
            )

            if min_eq_mag < 0 or min_eq_mag > 10:
                printe("    Magnitude range between 0 to 10")
                continue
        except ValueError:
            printe("    Input numbers only!")
            continue

        try:
            print(80 * ".")
            print(f"  Enter the maximum magnitude for the {req_type}")
            max_eq_mag = int(
                input("  \x1B[3m(leave empty for default value)\x1b[0m  :   ").strip()
                or "10"
            )

            if max_eq_mag < 0 or max_eq_mag > 10:
                printe("  Magnitude range between 0 to 10")
                continue
        except ValueError:
            printe("    Input numbers only!")
            continue

        if min_eq_mag >= max_eq_mag:
            printe("\n    The minimum magnitude must be lower than the maximum\n")
            continue
        elif min_eq_mag < max_eq_mag:
            break
    return min_eq_mag, max_eq_mag


def eq_depth_range(*args):
    req_type = args[0]
    while True:
        try:
            print(80 * ".")
            print(f"  Enter the minimum depth for the {req_type}")
            min_eq_depth = int(
                input("  \x1B[3m(leave empty for default value)\x1b[0m  :   ").strip()
                or "0"
            )

            if min_eq_depth < 0 or min_eq_depth > 1000:
                printe("    The depth range between 0 to 1000")
                continue
        except ValueError:
            printe("    Input numbers only!")
            continue

        try:
            print(80 * ".")
            print(f"  Enter the maximum depth for the {req_type}")
            max_eq_depth = int(
                input("  \x1B[3m(leave empty for default value)\x1b[0m  :   ").strip()
                or "1000"
            )

            if max_eq_depth < 0 or max_eq_depth > 1000:
                printe("    The depth range between 0 to 1000")
                continue
        except ValueError:
            printe("    Input numbers only!")
            continue

        if min_eq_depth >= max_eq_depth:
            printe("\n    Minimum depth must be lower than maximum\n")
            continue
        elif min_eq_depth < max_eq_depth:
            break
    return min_eq_depth, max_eq_depth


def eq_catalog_source():
    while True:
        print("  Choose the earthquake catalog service: ")
        print("    1. USGS - NEIC PDE")
        print("    2. ISC Bulletin")
        print("    3. User supplied")
        # print("  3. GlobalCMT")
        eq_cata = input("  Earthquake catalog:  ")
        match eq_cata:
            case "1" | "1." | "USGS" | "usgs" | "NEIC":
                eq_cata = "USGS"
                print(80 * ".")
                printc(
                    "  using earthquake catalog from USGS Preliminary Determination of Epicenters"
                )
                print(70 * ".")
                break
            case "2" | "2." | "ISC" | "isc" | "ISC Bulletin":
                eq_cata = "ISC"
                print(70 * ".")
                printc(
                    "  using earthquake catalog from International Seismology Centre Bulletin"
                )
                break
            case "3" | "3." | "User supplied" | "gcmt" | "GlobalCMT":
                eq_cata = "From user"
                printc("  using earthquake catalog from Global Centroid Moment Tensor")
                break
            # case "3" | "3." | "GCMT" | "gcmt" | "GlobalCMT":
            #     eq_cata = "GlobalCMT"
            #     print("using earthquake catalog from Blobal Centroid Moment Tensor")
            #     break
            case _:
                printe("error, pleace choose correctly..")
                continue
    return eq_cata


# def north_arrow():


def eq_legend():
    calculation = 10
    return calculation


# def map_layout():
#     """User input for map layout"""
#     while True:
#         print(" Please choose the map type ".center(50, "="))
#         print("\n" + "Map type:")
#         print("1. Single map")
#         print("2. Multiple maps in one figure")
#         print("0. Cancel")
#         print("\n" + 50 * "=")
#         user_map_type = input("Choose the map type: ")
#         if user_map_type == "1":
#             print("\nWill create single map\n")
#             print("Done")
#             break

#         elif user_map_type == "2":
#             print("\nWill create multiple map\n")
#             break
#         elif user_map_type == "0":
#             print("\nCanceling..\n")
#             break
#         else:
#             print("Please choose between 1 or 2..\n")
#             continue
#     return user_map_type


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
    while True:
        print("  column order separate with space and the first column start from 1")
        print("  data required : longitude, lattitude, depth, magnitude")
        # print("6 column if date and time in different column, or 5 if combined")
        print("  for example: 1 2 3 4 ")
        print("  |longitude|--|lattitude|--|depth|--|magnitude|--|Date-Time|")
        eq_column_order = list(map(input("  the column order:  ").strip().split))[:4]
        eq_column_lon = eq_column_order[0]
        eq_column_lat = eq_column_order[1]
        eq_column_dep = eq_column_order[2]
        eq_column_mag = eq_column_order[3]
        col_check = eq_column_check(eq_path, eq_column_order)
        if col_check[0] == "good":
            break
        else:
            printe("    The column order not match with the data")
            continue

    return eq_column_lon, eq_column_lat, eq_column_dep, eq_column_mag, col_check


def eq_column_check(eq_path, column_order):
    print(eq_path, column_order)
    with open(eq_path) as f:
        for columns in f:
            lon = columns[{column_order[0]}]
            if lon < -180 or lon > 180:
                printe(
                    "    Error: longitude value should between -180 and 180 degree. \n    Check the column order"
                )
                status = "bad"
                break

            lat = columns[{column_order[1]}]
            if lat < -90 or lat > 90:
                printe(
                    "    Error: lattitude value should between -90 and 90 degree. \n    Check the column order"
                )
                status = "bad"
                break
            eq_data_dep = []
            depth = columns[{column_order[2]}]
            if depth < 0 or depth > 1000:
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
