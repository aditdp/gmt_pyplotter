from itertools import zip_longest
import os
import copy
import cursor
import subprocess

from gmt_pyplotter import user_input as ui
from gmt_pyplotter.user_input import printc, printe
from gmt_pyplotter import utils

# import user_input as ui
# from user_input import printc, printe
# import utils


class FileName:
    def __init__(self) -> str:
        self.output_path = ui.get_save_loc()
        self.fname = ui.get_file_name(self.output_path)
        self.output_format = ui.get_file_out_format()

    @property
    def name(self):
        """return output filename only, without directory and format"""
        return self.fname

    @property
    def format(self):
        """return file output format only"""
        return self.output_format

    @property
    def dir_output_path(self):
        """return output directory only"""
        return self.output_path

    @property
    def file_output_path(self):
        """return output directory + file name + format"""
        return os.path.join(f"{self.output_path},{self.fname}.{self.output_format}")


class Coordinate:
    def __init__(self):
        self.x1, self.x2 = ui.get_coord_x()
        self.y1, self.y2 = ui.get_coord_y()
        self.map_width_deg = abs(self.x2 - self.x1)
        self.map_height_deg = abs(self.y2 - self.y1)
        self.map_aspect_ratio: float = self.map_height_deg / self.map_width_deg

    @property
    def mid_x(self):
        return (self.x2 + self.x1) / 2

    @property
    def mid_y(self):
        return (self.y2 + self.y1) / 2

    @property
    def boundary(self):
        return [self.x1, self.x2, self.y1, self.y2]

    @property
    def coord_script(self):
        return f"-R{self.x1}/{self.x2}/{self.y1}/{self.y2}"


class Projection:
    def __init__(self):
        # self.proj = ui.get_projection()
        self.proj = "M"
        self.map_width_cm = ui.get_map_width()

    @property
    def proj_script(self):
        if self.proj == "M":
            return f"-J{self.proj}{self.map_width_cm}c"
        elif self.proj == "G":
            return f"-J{self.proj}{Coordinate.mid_x(self)}/{Coordinate.mid_y(self)}/{self.map_width_cm}c+z100"

    @property
    def map_height_cm(self):
        width_cm = self.map_width_cm * self.map_aspect_ratio
        return width_cm


lyr1 = "Layer 1"
lyr2 = "Layer 2"
lyr3 = "Layer 3"
lyr4 = "Layer 4"
lyr5 = "Layer 5"
lyr6 = "Layer 6"


class Layer(FileName, Coordinate, Projection):

    def __init__(self):
        FileName.__init__(self)
        Coordinate.__init__(self)
        Projection.__init__(self)
        utils.screen_clear()
        MainMap.get_general_info(self)
        self.map_scale_factor = (self.map_width_deg * 111.1) / (
            self.map_width_cm * 0.0001
        )
        print("  Adding layer for main map..\n")
        self.layers = dict()
        nlayer = 1
        type_usage = []
        while nlayer < 8:
            self.layers[f"Layer {nlayer}"] = self.get_map_layers()
            utils.screen_clear()
            MainMap.get_general_info(self)
            MainMap.get_layer_info(self)
            new_layer = [self.layers[f"Layer {nlayer}"]["Type"]]

            if new_layer[0] not in type_usage:
                type_usage += new_layer
            else:
                printe(
                    f"""    The layer type '{self.layers[f"Layer {nlayer}"]["Type"]}' already added, layer duplication not allowed"""
                )
                self.layers[f"Layer {nlayer}"]["script"] = "change"

            if self.layers[f"Layer {nlayer}"]["script"] == "cancel":
                del self.layers[f"Layer {nlayer}"]
                break
            elif self.layers[f"Layer {nlayer}"]["script"] == "change":
                continue

            add_layer = input("Add another layer (y/n):  ")

            if add_layer.lower() in ["n", "ne", "no", "na"]:
                print(f"{nlayer} layers added to the map")
                break
            else:
                nlayer += 1
        if any(hasattr(self, attr) for attr in ["earthquake", "focmec", "grdimage"]):
            self.layers[f"Layer {len(self.layers)+1}"] = MainMap.legend_constructor(
                self
            )

    def get_map_layers(self):
        """User input for map fill layer"""

        def print_menu():
            print("\n" + "." * 70)
            print("  The map layer:")
            print("  1. Coastal line")
            print("  2. Earth relief*")
            print("  3. Contour line*")
            print("  4. Earthquake plot*")
            print("  5. Focal mechanism plot*")
            print("  6. Indonesia Regional Tectonics")
            print("  7. Map inset")
            print("  0. Cancel")
            print(
                "\x1B[3m  The layers followed by * need internet connection to operate\x1B[0m"
            )
            print("." * 70 + "\n")

        def handle_no_connection(message):
            cursor.hide()
            printe(message)
            input("  Press 'enter' to change Layer")
            cursor.show()
            return {"script": "change"}

        layer_options = {
            "1": (self.layer_coast, "Coastal line layer added.."),
            "2": (self.layer_grdimage, "Earth relief layer added.."),
            "3": (self.layer_contour, "Contour layer added.."),
            "4": (self.layer_earthquake, "Earthquake layer added.."),
            "5": (self.layer_focmec, "Focal mechanism plot layer added.."),
            "6": (self.layer_indo_tecto, "Indo Regional Tectonic layer added.."),
            "7": (self.layer_inset, "Inset map added.."),
            "0": (None, "Cancel adding another layer.."),
        }

        while True:
            print_menu()
            user_map_fill = input("  Choose the map layer: ")

            if user_map_fill in layer_options:
                layer_function, success_message = layer_options[user_map_fill]
                if user_map_fill in ["2", "3", "5"] and not utils.is_connected():
                    user_layer = handle_no_connection(
                        f"    No internet connection, the layer not added.."
                    )
                else:
                    user_layer = (
                        layer_function()
                        if layer_function
                        else {"Type": "cancel", "script": "cancel"}
                    )
                    print(success_message)
                break
            else:
                utils.screen_clear()
                MainMap.get_general_info(self)
                MainMap.get_layer_info(self)

                printe("    Please choose between 1 to 7")
                printe("    or 0 for cancel adding more layer")

        return user_layer

    @property
    def layer_base(self):
        added_gmt_script = f"gmt begin {self.name} {self.output_format} \n\tgmt set MAP_ANNOT_OBLIQUE lon_horizontal,lat_parallel\n\tgmt basemap {self.coord_script} {self.proj_script} -Ba+e -Ve\n"

        self.base_script = {
            "projection": self.proj_script,
            "coordinate": self.coord_script,
            "script": added_gmt_script,
        }
        return self.base_script, added_gmt_script

    def layer_coast(self):
        self.__color_land = ui.get_color("land", "seagreen2")
        self.__color_sea = ui.get_color("sea", "lightcyan")
        added_gmt_script = (
            f"\tgmt coast -S{self.__color_sea}  -G{self.__color_land} -Ve\n"
        )
        self.coast = {
            "Type": "coast",
            "Land color": self.__color_land,
            "Sea color": self.__color_sea,
            "script": added_gmt_script,
        }

        return self.coast

    def layer_grdimage(self):
        if self.map_width_deg > 4 or self.map_height_deg > 4:
            map_scale = "large"
        else:
            map_scale = "small"
        grd_resolution, res = ui.get_grdimage_resolution(map_scale)
        grd_cpt_color = ui.get_grdimage_color_palette()
        grd_shading_code, shade = ui.get_grdimage_shading()
        grd_masking = ui.get_grdimage_mask()
        grd_file = utils.grdimage_download(
            self.name,
            self.dir_output_path,
            self.coord_script,
            grd_resolution,
            grd_masking,
        )
        grd_cpt = f"{self.name}-elev.cpt"
        elevmin, elevmax, interval = self.grdimage_min_max_interval(grd_file)
        if interval == 0:
            printe("    The elevation model not found")
            printe("    Change layer or turn off GRD masking")
            input()
            return {"script": "change"}

        grd2cpt = f"\tgmt grd2cpt {grd_file} -C{grd_cpt_color} -T{elevmin}/{elevmax}/{interval} -Z -H > {grd_cpt}\n"

        grdimage = (
            f"\tgmt grdimage {grd_file} {grd_shading_code} -C{grd_cpt_color} -Q -Ve\n"
        )
        added_gmt_script = grd2cpt + grdimage

        self.cpt_elev_interval = interval
        self.grdimage = {
            "Type": "earth relief",
            "Shading": shade,
            "Cpt Code": grd_cpt_color,
            "Resolution": res,
            "Sea mask": grd_masking,
            "script": added_gmt_script,
        }
        return self.grdimage

    def grdimage_min_max_interval(self, grd_file):
        """Evaluate the grd_file and return the recomended interval for cpt, elevmin, and elevmax"""
        command = f"gmt grdinfo {os.path.join(self.dir_output_path,grd_file)} -Cn -M -G"
        grdinfo = subprocess.run(
            command,
            shell={os.name == "posix"},
            capture_output=True,
            text=True,
            check=True,
        )
        grdinfo = grdinfo.stdout.split()
        elevmax = round(float(grdinfo[5]), -1)
        elevmin = round(float(grdinfo[4]), -1)
        total_elev = elevmax + abs(elevmin)
        interval = 0
        if total_elev in range(5000, 20000):
            interval = 1000
        elif total_elev in range(2500, 5000):
            interval = 500
        elif total_elev in range(1000, 2500):
            interval = 250
        elif total_elev in range(500, 1000):
            interval = 100
        elif total_elev in range(0, 500):
            interval = 50
        return elevmin, elevmax, interval

    # def grdimage_colorbar(self, grd_file):

    #     "not used yet"
    #     command = f"gmt grdinfo {grd_file} -Cn -M -G"
    #     colorbar_interval = self.grdimage_colorbar_interval(command)
    #     print("  Optional color bar for the grid image: ")
    #     print("    1. Top")
    #     print("    2. Right")
    #     print("    3. Left")
    #     print("    4. Bottom")
    #     print("    0. None")
    #     while True:
    #         askcolorbar = input("  Colorbar location: ")
    #         match askcolorbar.upper():
    #             case "1" | "1." | "TOP":
    #                 askcolorbar = "Top"
    #                 position = "TC+o0c/0.75c"

    #                 break
    #             case "2" | "2." | "RIGHT":
    #                 askcolorbar = "Right"
    #                 position = "MR+o1c/50%"
    #                 break
    #             case "3" | "3." | "LEFT":
    #                 askcolorbar = "Left"
    #                 position = "ML+o1.5c/50%"
    #                 break
    #             case "4" | "4." | "BOTTOM":
    #                 askcolorbar = "Bottom"
    #                 position = "BC+o0c/1c"
    #                 break
    #             case "0" | "0." | "NONE":
    #                 askcolorbar = "none"
    #                 position = "none"
    #                 break
    #             case _:
    #                 printe(f"    '{askcolorbar}' is not a valid input")

    #     if position == "none":
    #         colorbar = ""
    #         printc("  Color bar is 'not added' to the map")
    #     else:
    #         printc(f"  Color bar location on '{askcolorbar}' side of the map")
    #         colorbar = f"\tgmt colorbar -DJ{position}+w50% -Bx{colorbar_interval[0]}+lElevation -By+lMeters\n"

    #     return colorbar, askcolorbar

    def layer_contour(self):
        ctr_interval, reso = ui.get_contour_interval(self.map_scale_factor)
        added_gmt_script = f"\tgmt grdcontour @earth_relief_{reso} -A{ctr_interval * 4}+ap+u-m -C{ctr_interval} -Wathin,gray50 -Wcfaint,gray70 -LP -Ve\n"
        self.contour = {
            "Type": "contour",
            "Interval": ctr_interval,
            "Resolution": reso,
            "script": added_gmt_script,
        }
        return self.contour

    def layer_indo_tecto(self):
        if self.map_width_deg > 10 or self.map_height_deg > 10:
            map_scale = "large"
        else:
            map_scale = "small"

        source = ui.get_tecto_source(map_scale)
        fault = os.path.join(
            os.path.dirname(__file__),
            "data",
            f"fault_{(source.replace(', ','')).lower()}.txt",
        )
        color = ui.get_color("Tectonic Line", "black")
        if source == "Sukamto, 2011":
            added_gmt_script = (
                f"\tgmt  plot {fault} -W1p,{color},solid -Sf+1i/0.2i+l+t -Ve\n"
            )
        else:
            added_gmt_script = f"\tgmt  plot {fault} -W1p,{color},solid -Ve\n"
        self.indo_tecto = {
            "Type": "tectonic",
            "Source": source,
            "Color": "color",
            "script": added_gmt_script,
        }
        return self.indo_tecto

    def layer_earthquake(self):
        self.eq_source = ui.get_eq_catalog_source()
        if self.eq_source == "cancel":
            return {"script": "change"}

        eq_file = f"{self.name}-{self.eq_source}_catalog.txt"
        cpt_file = f"{self.name}-depth.cpt"
        self.eq_scaler = float(self.map_width_cm) * 0.0005
        if self.eq_source in ("USGS", "ISC"):
            if hasattr(self, "req_fm_date"):
                self.req_eq_date = self.req_fm_date
                self.req_eq_mag = self.req_fm_mag
                self.req_eq_depth = self.req_fm_depth
            else:
                req_type = "earthquake catalog"
                self.req_eq_date = ui.get_date_start_end(req_type)
                self.req_eq_mag = ui.get_eq_mag_range(req_type)
                self.req_eq_depth = ui.get_eq_depth_range(req_type)

        match self.eq_source:
            case "USGS":
                eq_data_status = utils.usgs_downloader(
                    eq_file,
                    self.dir_output_path,
                    self.boundary,
                    self.req_eq_date,
                    self.req_eq_mag,
                    self.req_eq_depth,
                )
            case "ISC":
                eq_data_status = utils.isc_downloader(
                    eq_file,
                    self.dir_output_path,
                    self.boundary,
                    self.req_eq_date,
                    self.req_eq_mag,
                    self.req_eq_depth,
                )
            case "From user":
                eq_file_from_user = ui.get_eq_directory()

                eq_data_status, order = ui.get_column_order(eq_file_from_user)
                eq_file = f"{self.name}-USER_catalog.txt"
                utils.reorder_columns(
                    eq_file_from_user,
                    os.path.join(self.dir_output_path, eq_file),
                    order,
                )
                parse_eq_date = utils.find_min_max(
                    eq_file, self.dir_output_path, 4, date=True
                )
                if parse_eq_date == None:
                    self.req_eq_date = ("-", "-", "-")
                else:
                    self.req_eq_date = (
                        parse_eq_date["min"],
                        parse_eq_date["max"],
                        parse_eq_date["range"],
                    )

        if eq_data_status in ["bad", "empty"]:
            return {"script": "change"}

        self.real_eq_depth = utils.find_min_max(
            eq_file,
            self.dir_output_path,
            2,
            trim=True,
        )
        self.real_eq_mag = utils.find_min_max(
            eq_file,
            self.dir_output_path,
            3,
        )

        self.cpt_depth_interval: int = round(self.real_eq_depth["trim_range"] / 6, -1)
        interval = self.cpt_depth_interval
        min = self.real_eq_depth["trim_min"]
        max = min + (self.cpt_depth_interval * 6)

        makecpt = f"\tgmt makecpt -Cseis -T{min}/{max}/{interval} --COLOR_BACKGROUND=white --COLOR_FOREGROUND=black -H > {cpt_file}\n"
        gmtmath = f"\tgmt math {eq_file} -C3 SQR {self.eq_scaler} MUL = | "
        gmtplot = f"gmt plot -C{cpt_file} -Scc -Wfaint,grey30 -Ve \n"
        added_gmt_script = makecpt + gmtmath + gmtplot
        try:
            date_start = self.req_eq_date[0].strftime("%Y-%m-%d")
            date_end = self.req_eq_date[1].strftime("%Y-%m-%d")
        except AttributeError:
            date_start = "-"
            date_end = "-"
        self.earthquake = {
            "Type": "earthquake",
            "Source": self.eq_source,
            "nEvent": self.real_eq_depth["count"],
            "Depth": f"{int(self.real_eq_depth['min'])}-{int(self.real_eq_depth['max'])} km",
            "Magnitude": f"{self.real_eq_mag['min']}-{self.real_eq_mag['max']}",
            "Date start": date_start,
            "Date end": date_end,
            "script": added_gmt_script,
        }

        return self.earthquake

    def layer_focmec(self):
        fm_file = f"{self.name}-GCMT.txt"
        cpt_file = f"{self.name}-depth.cpt"
        self.fm_scaler = float(self.map_width_cm) * 0.025
        req_type = "focal mechanism"
        if hasattr(self, "req_eq_date"):
            self.req_fm_date = self.req_eq_date
            self.req_fm_mag = self.req_eq_mag
            self.req_fm_depth = self.req_eq_depth
        else:
            self.req_fm_date = ui.get_date_start_end(req_type)
            self.req_fm_mag = ui.get_eq_mag_range(req_type)
            self.req_fm_depth = ui.get_eq_depth_range(req_type)
        fm_data_status = utils.gcmt_downloader(
            fm_file,
            self.dir_output_path,
            self.boundary,
            self.req_fm_date,
            self.req_fm_mag,
            self.req_fm_depth,
        )
        if fm_data_status == "empty":
            return {"script": "change"}

        self.real_fm_depth = utils.find_min_max(
            fm_file, self.dir_output_path, 2, delimiter="\t"
        )
        self.real_fm_mag = utils.find_min_max(
            fm_file, self.dir_output_path, 13, delimiter="\t"
        )
        create_cpt = ""
        if not hasattr(self, "earthquake"):
            depth_range = int(self.real_fm_depth["range"])
            interval = round(depth_range / 6, -1)
            min = round(self.real_fm_depth["min"], -1)
            max = min + (self.cpt_depth_interval * 6)
            self.cpt_depth_interval = interval
            create_cpt = f"\tgmt makecpt -Cseis -T{min}/{max}/{interval} --COLOR_BACKGROUND=white --COLOR_FOREGROUND=black -H > {cpt_file}\n"

        added_gmt_script = f"{create_cpt}\tgmt meca {fm_file} -Sd{self.fm_scaler}c+f0 -C{cpt_file} -Lfaint,grey30 -Ve\n"
        self.focmec = {
            "Type": "focmech",
            "Source": "Global CMT",
            "nEvent": self.real_fm_depth["count"],
            "Depth": f"{int(self.real_fm_depth['min'])}-{int(self.real_fm_depth['max'])} km",
            "Magnitude": f"{self.real_fm_mag['min']}-{self.real_fm_mag['max']}",
            "Date start": str(self.req_fm_date[0]),
            "Date end": str(self.req_fm_date[1]),
            "script": added_gmt_script,
        }
        return self.focmec

    def layer_inset(self):

        larger = max(self.map_width_deg, self.map_height_deg)

        # magic
        if larger < 1.25:
            dilatation = larger * 3.5
        elif larger < 2.5:
            dilatation = larger * 3
        elif larger < 5:
            dilatation = larger * 2.5
        elif larger < 15:
            dilatation = larger * 2
        else:
            dilatation = larger * 1.5

        inset_x1 = self.mid_x - dilatation
        inset_x2 = self.mid_x + dilatation
        inset_y1 = self.mid_y - dilatation
        inset_y2 = self.mid_y + dilatation

        inset_size = min(self.map_height_cm, self.map_width_cm) / 3
        self.inset_coord = (inset_x1, inset_x2, inset_y1, inset_y2)

        inset_R = f"-R{self.inset_coord[0]:.2f}/{self.inset_coord[1]:.2f}/{self.inset_coord[2]:.2f}/{self.inset_coord[3]:.2f}"
        self.inset_just = ui.get_inset_loc()

        inset_offset = self.map_width_cm * 0.01

        rectangle = f"""# Plot location index on the inset>
{self.x1}\t{self.y1}
{self.x1}\t{self.y2}
>
{self.x1}\t{self.y2}
{self.x2}\t{self.y2}
>
{self.x2}\t{self.y2}
{self.x2}\t{self.y1}
>
{self.x2}\t{self.y1}
{self.x1}\t{self.y1}
"""
        utils.file_writer(
            "w", f"{self.name}-inset_rect.txt", rectangle, self.dir_output_path
        )
        frame = "-Ba+e -BnEwS -Ve --FORMAT_GEO_MAP=ddd:mm --MAP_FRAME_TYPE=inside --FONT_ANNOT_PRIMARY=auto,Courier-Bold,grey40"

        added_gmt_script = """\tgmt inset begin -Dj{}+o{}c {} -JM{:.2f}c
        gmt coast  -Slightcyan -Glightsteelblue2 -EID+gseagreen2 {}
        gmt plot {}-inset_rect.txt -Wthin,red -Ve
    gmt inset end\n""".format(
            self.inset_just[0],
            inset_offset,
            inset_R,
            inset_size,
            frame,
            self.name,
        )
        print("inset map added..")
        self.inset = {
            "Type": "inset",
            "Loc": self.inset_just[1],
            "script": added_gmt_script,
        }
        return self.inset

    def layer_gmt_end(self):
        loc_north = "TR"
        loc_scale = ["BL", "r"]
        try:
            if self.inset_just[0] == "TR":
                loc_north = "TL"
            elif self.inset_just[0] == "BL":
                loc_scale = ["BR", "l"]
        except AttributeError:
            pass
        # magic
        if self.map_width_deg > 4.9:
            width_km = f"{int(round(self.map_width_deg * 111.11 / 6, -2))}k"
        elif self.map_width_deg > 0.28:
            width_km = f"{int(round(self.map_width_deg * 111.11 / 6, -1))}k"
        elif self.map_width_deg > 0.03:
            width_km = f"{int(round(self.map_width_deg * 111.11 / 6))}k"
        else:
            width_km = f"{int(round(self.map_width_deg * 111111 / 6, -2))}e"

        gmt_end = f"\tgmt basemap -Lj{loc_scale[0]}+w{width_km}+l+f+o{self.map_width_cm*0.02:.2f}c/{self.map_width_cm*0.03:.2f}c+a{loc_scale[1]} -Tdj{loc_north}+l,,,N --FONT_LABEL=auto,Courier,grey10 --FONT_ANNOT=auto,Courier-Bold,grey10\ngmt end\n"

        return gmt_end

    def layer_writer(self):
        match os.name:
            case "posix":
                script_name = f"{self.name}.gmt"
            case "nt":
                script_name = f"{self.name}.bat"
        print(f"creating GMT script: {self.name}")
        utils.file_writer("w", script_name, self.layer_base[1], self.dir_output_path)
        for layer in range(1, len(self.layers) + 1):
            utils.file_writer(
                "a",
                script_name,
                (self.layers[f"Layer {layer}"]["script"]),
                self.dir_output_path,
            )

        gmt_end = self.layer_gmt_end()
        utils.file_writer("a", script_name, gmt_end, self.dir_output_path)


class MainMap(Layer):
    """The child class which inherit from Layer class. Have method to display the map parameter information and generate legend"""

    def __init__(self):
        Layer.__init__(self)
        self.__columns = None

    def get_general_info(self):
        """Printing basic map parameter
        Output location; File name; Projection, Map width and Coordinate"""
        if self.proj == "M":
            proj = "Mercators"
        elif self.proj == "G":
            proj = "Globe"
        general = f"""
{"  MAP PARAMETER  ".center(80, "=")} 
 Output dir : {self.output_path}
 File name  : {self.name:<20} Coordinate :
 Projection : {proj:<24} West : {self.x1:<13} South : {self.y1}
 Map size   : {self.map_width_cm} cm{17*" "} East : {self.x2:<13} North : {self.y2}
"""
        print(general)

    def print_1_layer(self, layer_print: dict):
        print(f"  {lyr1}")
        print((80 * "-"))
        for key, val in layer_print[lyr1].items():
            print(f"  {key:<10}: {val}")

    def print_2_layer(self, layer_print: dict):
        dkeys = list(zip_longest(layer_print[lyr1], layer_print[lyr2], fillvalue=" "))
        dvalues = list(
            zip_longest(
                layer_print[lyr1].values(),
                layer_print[lyr2].values(),
                fillvalue=" ",
            )
        )
        print(" ", (21 * " ").join(self.__columns))
        print((80 * "-"))
        for l1, l2 in zip(dkeys, dvalues):
            print(f"  {l1[0]:<10}: {l2[0]:<15} {l1[1]:<10}: {l2[1]:<15}")

    def print_3_layer(self, layer_print: dict):
        dkeys = list(
            zip_longest(
                layer_print[lyr1],
                layer_print[lyr2],
                layer_print[lyr3],
                fillvalue=" ",
            )
        )

        dvalues = list(
            zip_longest(
                layer_print[lyr1].values(),
                layer_print[lyr2].values(),
                layer_print[lyr3].values(),
                fillvalue=" ",
            )
        )

        print(" ", (21 * " ").join(self.__columns))
        print((80 * "-"))
        for l1, l2 in zip(dkeys, dvalues):
            print(
                f"  {l1[0]:<10}: {l2[0]:<15} {l1[1]:<10}: {l2[1]:<15} {l1[2]:<10}: {l2[2]:<15} "
            )

    def print_4_layer(self, layer_print: dict):
        dkeys = list(
            zip_longest(
                layer_print[lyr1],
                layer_print[lyr2],
                layer_print[lyr3],
                layer_print[lyr4],
                fillvalue=" ",
            )
        )

        dvalues = list(
            zip_longest(
                layer_print[lyr1].values(),
                layer_print[lyr2].values(),
                layer_print[lyr3].values(),
                layer_print[lyr4].values(),
                fillvalue=" ",
            )
        )

        print(" ", (21 * " ").join(self.__columns[0:3]))
        print((80 * "-"))
        for l1, l2 in zip(dkeys, dvalues):
            print(
                f"  {l1[0]:<10}: {l2[0]:<15} {l1[1]:<10}: {l2[1]:<15} {l1[2]:<10}: {l2[2]:<15} "
            )
        print((80 * "-"))
        print(" ", (21 * " ").join(self.__columns[3:4]))
        print((80 * "-"))
        for l1, l2 in zip(dkeys, dvalues):
            print(f"  {l1[3]:<10}: {l2[3]:<15} ")

    def print_5_layer(self, layer_print: dict):
        dkeys = list(
            zip_longest(
                layer_print[lyr1],
                layer_print[lyr2],
                layer_print[lyr3],
                layer_print[lyr4],
                layer_print[lyr5],
                fillvalue=" ",
            )
        )

        dvalues = list(
            zip_longest(
                layer_print[lyr1].values(),
                layer_print[lyr2].values(),
                layer_print[lyr3].values(),
                layer_print[lyr4].values(),
                layer_print[lyr5].values(),
                fillvalue=" ",
            )
        )

        print(" ", (21 * " ").join(self.__columns[0:3]))
        print((80 * "-"))
        for l1, l2 in zip(dkeys, dvalues):
            print(
                f"  {l1[0]:<10}: {l2[0]:<15} {l1[1]:<10}: {l2[1]:<15} {l1[2]:<10}: {l2[2]:<15} "
            )
        print((80 * "-"))
        print(" ", (21 * " ").join(self.__columns[3:5]))
        print((80 * "-"))
        for l1, l2 in zip(dkeys, dvalues):
            print(f"  {l1[3]:<10}: {l2[3]:<15} {l1[4]:<10}: {l2[4]:<15} ")

    def print_6_layer(self, layer_print: dict):
        dkeys = list(
            zip_longest(
                layer_print[lyr1],
                layer_print[lyr2],
                layer_print[lyr3],
                layer_print[lyr4],
                layer_print[lyr5],
                layer_print[lyr6],
                fillvalue=" ",
            )
        )

        dvalues = list(
            zip_longest(
                layer_print[lyr1].values(),
                layer_print[lyr2].values(),
                layer_print[lyr3].values(),
                layer_print[lyr4].values(),
                layer_print[lyr5].values(),
                layer_print[lyr6].values(),
                fillvalue=" ",
            )
        )

        print(" ", (21 * " ").join(self.__columns[0:3]))
        print((80 * "-"))
        for l1, l2 in zip(dkeys, dvalues):
            print(
                f"  {l1[0]:<10}: {l2[0]:<15} {l1[1]:<10}: {l2[1]:<15} {l1[2]:<10}: {l2[2]:<15} "
            )
        print((80 * "-"))
        print(" ", (21 * " ").join(self.__columns[3:5]))
        print((80 * "-"))
        for l1, l2 in zip(dkeys, dvalues):
            print(
                f"  {l1[3]:<10}: {l2[3]:<15} {l1[4]:<10}: {l2[4]:<15} {l1[5]:<10}: {l2[5]:<15} "
            )

    def get_layer_info(self):
        """Printing the layer info"""

        layer_print = copy.deepcopy(self.layers)
        for layer in range(1, len(layer_print) + 1):
            del layer_print[f"Layer {layer}"]["script"]
        self.__columns = list(layer_print.keys())
        print("  LAYERS  ".center(80, "="))
        print("")

        match len(layer_print):
            case 1:
                self.print_1_layer(layer_print)
            case 2:
                self.print_2_layer(layer_print)
            case 3:
                self.print_3_layer(layer_print)
            case 4:
                self.print_4_layer(layer_print)
            case 5:
                self.print_5_layer(layer_print)
            case 6:
                self.print_6_layer(layer_print)
        print((80 * "="))

    def plot_beachball(self):
        beach_ball = f"""gmt begin {self.name}-fm eps\n\techo 1.5 1.5 50 163 80 -21 6 0 0 | gmt meca -R1/2/1/2 -JM10c -Sa1c -Ggrey40 -E-\ngmt end\n"""
        if os.name == "posix":
            os.system(beach_ball)
        else:
            utils.file_writer(
                "w", f"{self.name}plot.bat", beach_ball, self.dir_output_path
            )
            os.system(os.path.join(self.dir_output_path, f"{self.name}plot.bat"))
            os.remove(os.path.join(self.dir_output_path, f"{self.name}plot.bat"))

    def legend_constructor(self):
        """try horizontal legend first"""
        eq = "No"
        fm = "No"
        el = "No"
        legend_plot = ""
        depth_colorbar_plot = ""
        elev_colorbar_plot = ""
        # magic
        legend_file = f"{self.name}-LEGEND.txt"
        if hasattr(self, "earthquake"):
            eq = "Yes"
            min_depth = self.real_eq_depth["trim_min"]
            legend_width = round(self.map_width_cm * 0.75)
            try:
                date = f"{self.req_eq_date[0].strftime('%b %d, %Y')}\nL -\nL 10p,Helvetica C to {self.req_eq_date[1].strftime('%b %d, %Y')}"
            except AttributeError:
                date = "--- to ---"
            eq_mag_min = round(self.real_eq_mag["min"])
            eq_mag_max = round(self.real_eq_mag["max"])
            eq_mag_range = eq_mag_max - eq_mag_min + 1
            top_label_col = f"N 2"
            top_label = f"""L 10p,Helvetica c Earthquakes
L -
L 10p,Helvetica c {self.real_eq_mag['count']} events"""
            mag_circle_col = "N 0.5 1 " + "1 " * eq_mag_range + str(eq_mag_range + 1.5)
            # source = self.eq_source
            mag_circle = "L - \n"
            for i in range(eq_mag_min, eq_mag_max + 1):
                mag_circle += f"S C c {i*i*self.eq_scaler}c - faint,grey30 -\n"
                if i == eq_mag_max:
                    mag_circle += "L - \n"
            bot_label = "L -\n"
            for i in range(eq_mag_min, eq_mag_max + 1):
                bot_label += f"L 10p,Helvetica C M {i} \n"
                if i == eq_mag_max:
                    bot_label += "L - \n"
            if hasattr(self, "focmec"):
                fm = "Yes"
                legend_width = self.map_width_cm
                self.plot_beachball()
                date = f"{self.req_eq_date[0].strftime('%b %d, %Y')} to {self.req_eq_date[1].strftime('%b %d, %Y')}"
                fm_mag_min = round(self.real_fm_mag["min"])
                fm_mag_max = round(self.real_fm_mag["max"]) + 1
                fm_mag_range = fm_mag_max - fm_mag_min + 1
                top_label_col = f"N 0.5 {eq_mag_range} 1 {fm_mag_range} 1 {eq_mag_range+2.5+fm_mag_range}"
                top_label = f"""L -
L 10p,Helvetica c Earthquakes 
L -
L 10p,Helvetica c Focal mechanism 
L -
L -
L -
L 10p,Helvetica c {self.real_eq_mag['count']} events
L -
L 10p,Helvetica c {self.real_fm_mag['count']} events
L -
L -
"""
                mag_circle_col = (
                    "N 0.5 1 1 "
                    + "1 " * (eq_mag_range + fm_mag_range)
                    + str(eq_mag_range + 2.5 + fm_mag_range)
                )

                for i in range(fm_mag_min, fm_mag_max + 1):
                    mag_circle += f"S C k{self.name}-fm.eps {i*self.fm_scaler/5}c - faint,grey30 -\n"
                    if i == fm_mag_max:
                        mag_circle += "L -\n"

                for i in range(fm_mag_min, fm_mag_max + 1):
                    bot_label += f"L 10p,Helvetica C M {i}\n"
                    if i == fm_mag_max:
                        bot_label += "L -\n"

        elif hasattr(self, "focmec"):
            fm = "Yes"
            min_depth = round(self.real_fm_depth["min"], -1)
            self.plot_beachball()
            date = f"{self.req_fm_date[0].strftime('%b %d, %Y')}\nL -\nL 10p,Helvetica C to {self.req_fm_date[1].strftime('%b %d, %Y')}"
            fm_mag_min = round(self.real_fm_mag["min"])
            fm_mag_max = round(self.real_fm_mag["max"]) + 1
            fm_mag_range = fm_mag_max - fm_mag_min + 1
            legend_width = round(self.map_width_cm * 0.75)
            top_label_col = f"N 2"
            top_label = f"L 10p,Helvetica c Focal Mechanism\nL -\nL 10p,Helvetica c {self.real_fm_mag['count']} events"
            mag_circle_col = "N 0.5 1 " + "1 " * fm_mag_range + str(fm_mag_range + 1.5)
            mag_circle = "L - \n"
            for i in range(fm_mag_min, fm_mag_max + 1):
                mag_circle += (
                    f"S C k{self.name}-fm.eps {i*self.fm_scaler/5}c - faint,grey30 -\n"
                )
                if i == fm_mag_max:
                    mag_circle += "L -\n"
            bot_label = "L -\n"
            for i in range(fm_mag_min, fm_mag_max + 1):
                bot_label += f"L 10p,Helvetica C M {i}\n"
                if i == fm_mag_max:
                    bot_label += "L - \n"
        if "Yes" in (eq, fm):
            legend_text = f"""# script for plot legend 
H 12p,Helvetica-Bold L E G E N D
G 0.5c
N 2
L 10p,Helvetica C Data during {date}
G 0.3c
{top_label_col}
{top_label}
G 0.2c
{mag_circle_col}
G 0.2c
{mag_circle}
G 0.2c
{bot_label}
G 0.1c"""
            utils.file_writer("w", legend_file, legend_text, self.dir_output_path)

            legend_plot = f"\tgmt legend -DJBC+o0c/1c+w{legend_width}c -F+p1p+gwhite+r {legend_file}\n"
            depth_label = f"-B{self.cpt_depth_interval}+{min_depth} -Bx+lEq_depth -By+lkm --FONT_LABEL=10p --MAP_FRAME_PEN=0.75p\n"
            depth_colorbar_plot = f"\tgmt colorbar -DJBC+o{legend_width*0.25}c/2.3c+w{legend_width*0.3}c+h+e0.3c -C{self.name}-depth.cpt {depth_label}"

        if hasattr(self, "grdimage"):
            el = "Yes"
            offset = "0c/1c"
            font = "12p"
            width = self.map_width_cm * 0.3
            if "Yes" in (fm, eq):
                offset = f"{legend_width*0.25}c/4.5c"
                font = "10p"
                width = legend_width * 0.3
            elev_label = f"-B{self.cpt_elev_interval} -Bx+lElevation -By+lmeter --FONT_LABEL={font} --MAP_FRAME_PEN=0.75p\n"
            elev_colorbar_plot = f"\tgmt colorbar -DJBC+o{offset}+w{width}c+h -C{self.name}-elev.cpt {elev_label}"

        added_gmt_script = legend_plot + depth_colorbar_plot + elev_colorbar_plot
        self.legend = {
            "Type": "legend",
            "Earthquake": eq,
            "FocMech": fm,
            "Elevation": el,
            "script": added_gmt_script,
        }
        return self.legend
