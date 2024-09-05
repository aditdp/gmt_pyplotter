import os.path, re
from cmd import Cmd
from datetime import date


def separator(func):
    def wrapper(*args):
        print(80 * "=")
        func(*args)
        print(80 * "=")

    return wrapper


def file_name():
    while True:
        input_file_name = input("Name of the map: ")
        path = os.path.join(
            os.getcwd(), "gmt_pyplotter", "output", input_file_name, ".png"
        )
        check_file = os.path.isfile(path)

        if check_file == True:
            try:
                print(f"The '{input_file_name}.png' in output folder, already exist")
                overwrite = input("Overwrite the file (y/n) ? ")
                if overwrite == "N" or overwrite == "n":
                    print("Choose another name")
                    continue
                elif overwrite == "Y" or overwrite == "y":
                    print("\nMap file will be overwrite!")
                    break
            except:
                continue
        else:
            print(f"Map will be save as {input_file_name}.png")
            break
    return input_file_name


def input_projection():
    print("Map Projection System (Press 'Enter' for default)")
    print(" (M) Mercator Cylindrical (default)")
    print(" (G) General perspective")
    while True:
        proj = input("Enter the map projection:  ")
        match proj:
            case "":
                proj = "M"
                break
            case "M" | "m":
                proj = "M"
                break
            case "G" | "g":
                proj = "G"
                break
            case _:
                print("Please choose between 'M' or 'G'")
                continue
    return proj


def input_size():
    print("Map size represent the width of the map in centimeter (cm)")
    print("the height will adjust to the coordinate boundary")
    while True:
        try:
            size = float(input("Enter the map size:  ").strip() or "20")
            if size > 50:
                print("Error, the map 'size' too large")
                print("'size' must be less than '50'")
                continue
            elif size < 0:
                print("Error, the map 'size' can not negative")
            elif size > 0 and size < 5:
                print("Error, the map 'size' too small")
            else:
                print("Map width is = {} cm".format(size))
                break
        except ValueError:
            print("error, enter integers only!")
            continue

    return size


def color_land():
    print("leave empty for default color")
    colr_land = str(input("Choose the color of the land :") or "seagreen2")
    return colr_land


def color_sea():
    print("leave empty for default color")
    colr_sea = str(input("Choose the color of the sea : ") or "lightcyan")
    return colr_sea


def color_focmec():
    print("leave empty for default color (red)")
    colr_fm = str(input("Choose the color of the beach ball : ") or "red")
    return colr_fm


def input_country_id():
    print("Country ID is based on the ISO 3166 international standard")
    print(
        """For example:
          (ID) for Indonesia
          (US) for United States of America
          (JP) for Japan"""
    )
    while True:
        country_id = input("Please type the country ID:  ")
        if not re.match("^[A-Z]*$", country_id):
            print("Error! Only capital letters allowed!")
            continue
        elif len(country_id) > 2:
            print("Error! Only 2 characters allowed!")
            continue
        else:
            break

    return f"-R{country_id}"


def input_coord_x():
    """fungsi input koordinat peta dengan geographical projection"""

    while True:
        try:
            bound_x1 = float(input("Western boundary (W): ").strip() or 120)
            if bound_x1 < -180 or bound_x1 > 180:
                print("W-E coordinate range -180 to 180 degree")
                continue
        except ValueError:
            print("Input numbers only!")
            continue

        try:
            bound_x2 = float(input("Eastern boundary (E): ").strip() or 125)
            if bound_x2 < -180 or bound_x2 > 180:
                print("W-E coordinate range -180 to 180 degree")
                continue
        except ValueError:
            print("Input numbers only!")
            continue
        if bound_x1 >= bound_x2:
            print("\nWestern boundary must lesser than eastern boundary\n")
            continue
        elif bound_x1 <= bound_x2:
            bound_x1 = bound_x1
            bound_x2 = bound_x2
            break
    return bound_x1, bound_x2


def input_coord_y():
    while True:
        try:
            bound_y1 = float(input("Southern boundary (S): ").strip() or -9)
            if bound_y1 < -90 or bound_y1 > 90:
                print("N-S coordinate range -90 to 90 degree")
                continue
        except ValueError:
            print("Input numbers only!")
            continue

        try:
            bound_y2 = float(input("Northern boundary (N): ").strip() or -4)
            if bound_y2 < -90 or bound_y2 > 90:
                print("N-S coordinate range -90 to 90 degree")
                continue
        except ValueError:
            print("Input numbers only!")
            continue

        if bound_y1 >= bound_y2:
            print("\nSouthern boundary must lesser than northern boundary\n")
            continue
        elif bound_y1 <= bound_y2:
            # bound_y1 = bound_y1
            # bound_y2 = bound_y2
            break
    return bound_y1, bound_y2


def color_palette():
    print("The 'Color Palette Tables' provided in 'example' folder.")
    cpt_list = [
        "cubhelix",
        "dem1",
        "dem4",
        "elevation",
        "abyss",
        "bathy",
        "dem2",
        "dem3",
        "drywet",
        "earth",
        "etopo1",
        "gebco",
        "geo",
        "globe",
        "gray",
        "haxby",
        "ibcso",
        "mag",
        "nighttime",
        "no_green",
        "ocean",
        "paired",
        "rainbow",
        "red2green",
        "relief",
        "seafloor",
        "sealand",
        "seis",
        "split",
        "terra",
        "topo",
        "world",
        "wysiwyg",
        "turbo",
        "cool",
        "copper",
        "hot",
        "jet",
        "polar",
        "inferno",
        "magma",
        "plasma",
        "viridis",
        "panoply",
    ]
    print(f"\nList of CPT name:")
    pl = Cmd()
    pl.columnize(cpt_list, displaywidth=80)

    while True:
        colr_cpt = input("Choose the CPT:  ")
        if colr_cpt in cpt_list:
            print(f" {colr_cpt} is used for the color palette table")
            break
        elif colr_cpt not in cpt_list:
            print(f"{colr_cpt} is not a valid cpt name")
            continue
    return colr_cpt


def grdimage_shading():
    while True:
        shade = input("Shade the elevation model (y/n)?  ")
        if shade == "y" or shade == "Y":
            shading = "-I+d"
            shade = "Yes"
            print("the earth relief will shaded")
            break
        elif shade == "n" or shade == "N":
            shading = ""
            shade = "No"
            print("the earth relief will not shaded")
            break
        else:
            print("not a valid input..")
            continue
    return shading, shade


def grdimage_resolution():
    while True:
        print("Choose the image resolution")
        print(
            """SRTMGL1 (need internet connection)
            1. Full   (01 second)
            2. High   (15 second)
            3. Medium (01 minute)
            4. Low    (05 minute)
            5. Crude  (10 minute)
            """
        )
        grd_resolution = input("Image resolution: ")
        match grd_resolution:
            case "1" | "Full" | "full":
                resolution = "@earth_relief_01s"
                grd_res = "1 second"
                print("using the 'full' image resolution (1 second)")
                break
            case "2" | "High" | "high":
                resolution = "@earth_relief_15s"
                grd_res = "15 second"
                print("using the 'high' image resolution (15 seconds)")
                break
            case "3" | "Medium" | "medium":
                resolution = "@earth_relief_01m"
                grd_res = "1 minute"
                print("using the 'medium' image resolution (1 minute)")
                break
            case "4" | "low" | "Low":
                resolution = "@earth_relief_05m"
                grd_res = "5 minute"
                print("using the 'low' image resolution (5 minutes)")
                break
            case "5" | "Crude" | "crude":
                resolution = "@earth_relief_10m"
                grd_res = "10 minute"
                print("using the 'crude' image resolution (10 minutes)")
                break
            case _:
                print("error, please choose correctly..")
                continue

    return resolution, grd_res


def grdimage_mask():
    while True:
        mask = input("Masking the sea surface (y/n)?  ")
        if mask == "y" or mask == "Y":

            mask = "Yes"
            print("the sea surface will be masked")
            break
        elif mask == "n" or mask == "N":

            mask = "No"
            print("the sea surface will not be masked")
            break
        else:
            print("not a valid input..")
            continue
    return mask


def date_start(*args):
    req_type = args[0]
    while True:
        print(80 * ".")
        input_date_start = input(
            (f"Enter start date for the {req_type} (YYYYMMDD):   ").strip()
            or "20190101"
        )
        if not re.match("^[0-9]*$", input_date_start):
            print("error, input numbers only!")
            continue
        elif len(input_date_start) != 8:
            print("error, input eight characters!")
        else:
            year_start = int(input_date_start[0:4])
            mo_start = int(input_date_start[4:6])
            day_start = int(input_date_start[6:])
            try:
                input_date_start = date(year_start, mo_start, day_start)
                print("start date : ", input_date_start.strftime("%B %d, %Y"))

                break
            except ValueError as error:
                print(f"error, {error}!")
                continue

    return input_date_start


def date_end(*args):
    req_type = args[0]
    while True:
        print(80 * ".")
        input_date_end = input(
            (f"Enter end date for the {req_type} (YYYYMMDD):  ").strip() or "20240101"
        )
        if not re.match("^[0-9]*$", input_date_end):
            print("error, input numbers only!")
            continue
        elif len(input_date_end) != 8:
            print("error, input eight characters!")
        else:
            year_end = int(input_date_end[0:4])
            mo_end = int(input_date_end[4:6])
            day_end = int(input_date_end[6:])
            try:
                input_date_end = date(year_end, mo_end, day_end)
                print("end date : ", input_date_end.strftime("%B %d, %Y"))

                break
            except ValueError as error:
                print(f"error, {error}!")
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
            print("error, the end time must later than the start time")
            continue
        else:
            print(
                f"The data used is {days} days from ",
                in_date_start.strftime("%B %d, %Y"),
                "to",
                in_date_end.strftime("%B %d, %Y"),
            )

            break
    return in_date_start, in_date_end, days


def inset_loc():
    while True:
        print("         Inset map plot location:          ")
        print("__________________________________________ ")
        print("|    (1)   |   |    (2)   |   |    (3)   |")
        print("|__________|   |__________|   |__________|")
        print("|___________    ___________    __________|")
        print("|    (4)   |   |    (5)   |   |    (6)   |")
        print("|__________|   |__________|   |__________|")
        print("|___________    ___________    __________|")
        print("|    (7)   |   |    (8)   |   |    (9)   |")
        print("|__________|___|__________|___|__________|")
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
                print("Error, choose between 1 - 9 !")
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
            print(f"Enter the minimum magnitude for the {req_type}")
            min_eq_mag = int(
                input("\x1B[3m(leave empty for default value)\x1b[0m  :   ").strip()
                or "0"
            )

            if min_eq_mag < 0 or min_eq_mag > 10:
                print("Magnitude range between 0 to 10")
                continue
        except ValueError:
            print("Input numbers only!")
            continue

        try:
            print(80 * ".")
            print(f"Enter the maximum magnitude for the {req_type}")
            max_eq_mag = int(
                input("\x1B[3m(leave empty for default value)\x1b[0m  :   ").strip()
                or "10"
            )

            if max_eq_mag < 0 or max_eq_mag > 10:
                print("Magnitude range between 0 to 10")
                continue
        except ValueError:
            print("Input numbers only!")
            continue

        if min_eq_mag >= max_eq_mag:
            print("\nThe minimum magnitude must be lower than the maximum\n")
            continue
        elif min_eq_mag < max_eq_mag:
            break
    return min_eq_mag, max_eq_mag


def eq_depth_range(*args):
    req_type = args[0]
    while True:
        try:
            print(80 * ".")
            print(f"Enter the minimum depth for the {req_type}")
            min_eq_depth = int(
                input("\x1B[3m(leave empty for default value)\x1b[0m  :   ").strip()
                or "0"
            )

            if min_eq_depth < 0 or min_eq_depth > 1000:
                print("The depth range between 0 to 1000")
                continue
        except ValueError:
            print("Input numbers only!")
            continue

        try:
            print(80 * ".")
            print(f"Enter the maximum depth for the {req_type}")
            max_eq_depth = int(
                input("\x1B[3m(leave empty for default value)\x1b[0m  :   ").strip()
                or "1000"
            )

            if max_eq_depth < 0 or max_eq_depth > 1000:
                print("The depth range between 0 to 1000")
                continue
        except ValueError:
            print("Input numbers only!")
            continue

        if min_eq_depth >= max_eq_depth:
            print("\nMinimum depth must be lower than maximum\n")
            continue
        elif min_eq_depth < max_eq_depth:
            break
    return min_eq_depth, max_eq_depth


def eq_catalog_source():
    while True:
        print("Choose the earthquake catalog service: ")
        print("  1. USGS - NEIC PDE")
        print("  2. ISC Bulletin")
        # print("  3. GlobalCMT")
        eq_cata = input("Earthquake catalog:  ")
        match eq_cata:
            case "1" | "1." | "USGS" | "usgs" | "NEIC":
                eq_cata = "USGS"
                print(80 * ".")
                print(
                    "using earthquake catalog from USGS Preliminary Determination of Epicenters"
                )
                print(70 * ".")
                break
            case "2" | "2." | "ISC" | "isc" | "ISC Bulletin":
                eq_cata = "ISC"
                print(70 * ".")
                print(
                    "using earthquake catalog from International Seismology Centre Bulletin"
                )
                break
            # case "3" | "3." | "GCMT" | "gcmt" | "GlobalCMT":
            #     eq_cata = "GlobalCMT"
            #     print("using earthquake catalog from Blobal Centroid Moment Tensor")
            #     break
            case _:
                print("error, pleace choose correctly..")
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
    # file name, longitude, lattitude, magnitude, depth
    print("Place the earthquake info in data directory before proceed..")
    print("column order separate with space and the first column start from 1")
    print("for example: 1 2 3 4")
    print("|longitude|--|lattitude|--|magnitude|--|depth|")
    eq_column_order = list(map(input("the column order:  ").strip().split))[:4]
    eq_column_lon = eq_column_order[0]
    eq_column_lat = eq_column_order[1]
    eq_column_dep = eq_column_order[2]
    eq_column_mag = eq_column_order[3]
    print("Load the earthquake data from user")
    eq_user_fname = input("\nfile name:  ")
    path = os.path.join(os.getcwd(), "gmt_pyplotter", "data", ".png")
