from itertools import zip_longest
import os
import copy
import subprocess
import cursor

# from gmt_pyplotter import user_input as ui
# from gmt_pyplotter.user_input import printc, printe
# from gmt_pyplotter import utils
import user_input as ui
from user_input import printc, printe
import utils


class FileName:
    def __init__(self) -> str:
        self.output_path = ui.get_save_loc()
        self.output_format = ui.get_file_out_format()
        self.fname = ui.get_file_name(self.output_path, self.output_format)

    @property
    def name(self):
        return self.fname

    @property
    def format(self):
        return self.output_format

    @property
    def dir_output_path(self):
        return self.output_path

    @property
    def file_output_path(self):
        return os.path.join(f"{self.output_path},{self.fname}.{self.output_format}")


class Coordinate:
    def __init__(self):
        self.x1, self.x2 = ui.get_coord_x()
        self.y1, self.y2 = ui.get_coord_y()
        self.width = abs(self.x2 - self.x1)
        self.height = abs(self.y2 - self.y1)

    def mid_x(self):
        return (self.x2 + self.x1) / 2

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
        self.proj = ui.get_projection()
        self.size = ui.get_map_width()

    @property
    def map_size(self):
        return self.size

    @map_size.setter
    def map_size(self, value):
        self.size = value

    @property
    def proj_script(self):
        if self.proj == "M":
            return f"-J{self.proj}{self.size}c"
        elif self.proj == "G":
            return f"-J{self.proj}{Coordinate.mid_x(self)}/{Coordinate.mid_y(self)}/{self.size}c+z100"


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
        self.map_scale_factor = (self.width * 111.1) / (self.size * 0.0001)
        print("  Adding layer for main map..\n")
        self.layers = dict()
        layer = 1
        while layer < 8:
            # for layer in range(1, 7):
            self.layers[f"Layer {layer}"] = self.get_input_map_fill()
            utils.screen_clear()
            MainMap.get_general_info(self)
            MainMap.get_layer_info(self)
            if self.layers[f"Layer {layer}"]["script"] == "cancel":
                del self.layers[f"Layer {layer}"]
                break
            elif self.layers[f"Layer {layer}"]["script"] == "change":
                continue

            add_layer = input("Add another layer (y/n):  ")
            if add_layer.lower() == "y" or add_layer == "yes":
                layer += 1

            elif add_layer.lower() == "n" or add_layer == "no":
                print(f"{layer} layers added to the map")
                break

    def get_input_map_fill(self):
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
                "\x1B[3m  The layers followed by * need internet  connection to    operate\x1B[0m"
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
                        f"    No internet connection, {success_message.lower()}"
                    )
                else:
                    user_layer = (
                        layer_function() if layer_function else {"script": "cancel"}
                    )
                    print(success_message)
                break
            else:
                print("\033[18A")
                printe("    Please choose between 1 to 7")
                printe("    or 0 for cancel adding more layer")

        return user_layer

    @property
    def layer_base(self):
        self.__layer = f"gmt begin {self.name} {self.output_format} \n\tgmt basemap {self.coord_script} {self.proj_script} -Ba -TdjTR+l,,,N+o0.5c -Ve\n"

        self.base_script = {
            "projection": self.proj_script,
            "coordinate": self.coord_script,
            "script": self.__layer,
        }
        return self.base_script, self.__layer

    def layer_coast(self):
        self.__color_land = ui.get_color("land", "seagreen2")
        self.__color_sea = ui.get_color("sea", "lightcyan")
        self.__layer = f"\tgmt coast -S{self.__color_sea}  -EID+g{self.__color_land} -Glightsteelblue2 -TdjTR+l,,,N+o0.5c -Ve\n"
        self.coast = {
            "Type": "coast",
            "Land color": self.__color_land,
            "Sea color": self.__color_sea,
            "script": self.__layer,
        }

        return self.coast

    def grdimage_download(self):
        if self.__grd_masking is True:
            command = "clip"
            replace = "-Sb0/NaN"
        else:
            command = "cut"
            replace = ""
        self.__grd_file = (
            f"{os.path.join(self.dir_output_path ,self.name)}_grd{command}.nc"
        )
        dl_gridfile = subprocess.run(
            f"gmt grd{command} {self.coord_script} {self.__grd_resolution} -G{self.__grd_file} {replace} ",
            text=True,
            shell={os.name == "posix"},
            capture_output=True,
            check=True,
        )
        infow = dl_gridfile.stdout
        print(infow)

    def layer_grdimage(self):
        self.__grd_resolution, res = ui.get_grdimage_resolution()
        self.__grd_cpt_color = ui.get_grdimage_color_palette()
        self.__grd_shading_code, shade = ui.get_grdimage_shading()
        self.__grd_masking = ui.get_grdimage_mask()
        self.grdimage_download()
        self.__grd_color_bar, colorbar = self.grdimage_colorbar()

        self.__layer = f"\tgmt grd2cpt {self.__grd_file} -C{self.__grd_cpt_color} -Z\n\tgmt grdimage {self.__grd_file} {self.__grd_shading_code} -C{self.__grd_cpt_color} -Q -Ve\n{self.__grd_color_bar}"

        self.grdimage = {
            "Type": "earth relief",
            "Shading": shade,
            "Cpt": self.__grd_cpt_color,
            "Resolution": res,
            "Sea mask": self.__grd_masking,
            "Color bar": colorbar,
            "script": self.__layer,
        }
        return self.grdimage

    def grdimage_colorbar_interval(self, command):
        grdinfo = subprocess.run(
            command,
            shell={os.name == "posix"},
            capture_output=True,
            text=True,
            check=True,
        )
        grdinfo = grdinfo.stdout.split()
        elevmax = int(float(grdinfo[5]))
        elevmin = int(float(grdinfo[4]))
        total_elev = elevmax + abs(elevmin)

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
        return interval, elevmin, elevmax

    def grdimage_colorbar(self):
        command = f"gmt grdinfo {self.__grd_file} -Cn -M -G"
        colorbar_interval = self.grdimage_colorbar_interval(command)
        print("  Optional color bar for the grid image: ")
        print("    1. Top")
        print("    2. Right")
        print("    3. Left")
        print("    4. Bottom")
        print("    0. None")
        while True:
            askcolorbar = input("  Colorbar location: ")
            match askcolorbar.upper():
                case "1" | "1." | "TOP":
                    askcolorbar = "Top"
                    position = "TC+o0c/0.75c"

                    break
                case "2" | "2." | "RIGHT":
                    askcolorbar = "Right"
                    position = "MR+o1c/50%"
                    break
                case "3" | "3." | "LEFT":
                    askcolorbar = "Left"
                    position = "ML+o1.5c/50%"
                    break
                case "4" | "4." | "BOTTOM":
                    askcolorbar = "Bottom"
                    position = "BC+o0c/1c"
                    break
                case "0" | "0." | "NONE":
                    askcolorbar = "none"
                    position = "none"
                    break
                case _:
                    printe(f"    '{askcolorbar}' is not a valid input")

        if position == "none":
            colorbar = ""
            printc("  Color bar is 'not added' to the map")
        else:
            printc(f"  Color bar location on '{askcolorbar}' side of the map")
            colorbar = f"\tgmt colorbar -DJ{position}+w50% -Bx{colorbar_interval[0]}+lElevation -By+lMeters\n"

        return colorbar, askcolorbar

    def layer_contour(self):
        self.__ctr_interval, self.__reso = ui.get_contour_interval(
            self.map_scale_factor
        )
        self.__layer = f"\tgmt grdcontour @earth_relief_{self.__reso} -A{self.__ctr_interval * 4}+ap+u\ m -C{self.__ctr_interval} -Wathin,gray50 -Wcfaint,gray70 -LP -Ve\n"
        self.contour = {
            "Type": "contour",
            "Interval": self.__ctr_interval,
            "Resolution": self.__reso,
            "script": self.__layer,
        }
        return self.contour

    def layer_indo_tecto(self):

        map_scale = lambda map_scale: (
            "large" if self.width or self.height > 10 else "small"
        )
        source = ui.get_tecto_source(map_scale)
        fault = os.path.join(
            os.path.dirname(__file__),
            "data",
            f"{(source.replace(', ','')).lower()}.txt",
        )
        color = ui.get_color("Tectonic Line", "black")
        if source == "Sukamto, 2011":
            self.__layer = (
                f"\tgmt  plot {fault} -W1p,{color},solid -Sf+1i/0.2i+l+t -Ve\n"
            )
        else:
            self.__layer = f"\tgmt  plot {fault} -W1p,{color},solid -Ve\n"
        self.indo_tecto = {
            "Type": "tectonic",
            "Source": source,
            "Color": "color",
            "script": self.__layer,
        }
        return self.indo_tecto

    def layer_earthquake(self):
        self.__source = ui.get_eq_catalog_source()
        if self.__source != "cancel":
            self.eq_file = os.path.join(
                self.dir_output_path,
                f"{self.name}_{self.__source}-catalog.txt",
            )
            self.__scaler = float(self.map_size) * 0.0001
            if self.__source != "From user":
                req_type = "earthquake catalog"

                self.__eq_date = ui.get_date_start_end(req_type)
                self.__eq_mag = ui.get_eq_mag_range(req_type)
                self.__eq_depth = ui.get_eq_depth_range(req_type)
            match self.__source:
                case "USGS":
                    self.__lonlatdepmag = f"$3,$2,$4,$5*$5*{str(self.__scaler)}"
                    utils.usgs_downloader(
                        self.eq_file,
                        self.boundary,
                        self.__eq_date,
                        self.__eq_mag,
                        self.__eq_depth,
                    )
                case "ISC":
                    self.__lonlatdepmag = f"$7,$6,$8,$12*$12*{str(self.__scaler)}   "
                    utils.isc_downloader(
                        self.eq_file,
                        self.boundary,
                        self.__eq_date,
                        self.__eq_mag,
                        self.__eq_depth,
                    )
                case "From user":
                    self.eq_file = ui.get_eq_directory()
                    self.column = ui.get_column_order(self.eq_file)
                    self.__eq_date = ("-", "-", "-")
                    self.__eq_mag = (self.column[4][3], self.column[4][4])
                    self.__eq_depth = (self.column[4][1], self.column[4][2])
                    self.__lonlatdepmag = f"${self.column[0]},${self.column[1]},${self.column[2]},${self.column[3]}*${self.column[3]*{str(self.__scaler)}},"
            if os.name == "posix":
                self.__layer = (
                    "\tgmt makecpt -Cred,green,blue -T0,70,150,10000 -N\n"
                    + """\tgawk -F "," '{ print """
                    + self.__lonlatdepmag
                    + "}' "
                    + self.eq_file
                    + """| gmt plot -C -Scc -hi1 -Wfaint -Ve\n"""
                )
            elif os.name == "nt":
                self.__layer = (
                    "\tgmt makecpt -Cred,green,blue -T0,70,150,10000 -N\n"
                    + """\tgawk -F "," "{ print """
                    + self.__lonlatdepmag
                    + '}" '
                    + self.eq_file
                    + """| gmt plot -C -Scc -hi1 -Wfaint -Ve\n"""
                )
            self.earthquake = {
                "Type": "earthquake",
                "Source": self.__source,
                "Depth": f"{self.__eq_depth[0]}-{self.__eq_depth[1]} km",
                "Magnitude": f"{self.__eq_mag[0]}-{self.__eq_mag[1]}",
                "Date start": str(self.__eq_date[0]),
                "Date end": str(self.__eq_date[1]),
                "nDay": str(self.__eq_date[2]),
                "script": self.__layer,
            }
        else:
            self.earthquake = {"script": "change"}
        return self.earthquake

    def layer_focmec(self):
        req_type = "focal mechanism"
        self.fm_file = os.path.join(self.dir_output_path, f"{self.name}_gcmt.txt")
        self.__gcmt_date = ui.get_date_start_end(req_type)
        self.__gcmt_mag = ui.get_eq_mag_range(req_type)
        self.__gcmt_depth = ui.get_eq_depth_range(req_type)
        self.__scaler = float(self.map_size) * 0.02
        self.__layer = "\tgmt makecpt -Cred,green,blue -T0,70,150,10000 -N -Ve\n\tgmt meca {} -Sd{}c+f0 -C -W01p,gray50 -Ve\n".format(
            self.fm_file,
            self.__scaler,
        )
        utils.gcmt_downloader(
            self.fm_file,
            self.boundary,
            self.__gcmt_date,
            self.__gcmt_mag,
            self.__gcmt_depth,
        )
        self.focmec = {
            "Type": "focmech",
            "Source": "Global CMT",
            "Depth": f"{self.__gcmt_depth[0]}-{self.__gcmt_depth[1]} km",
            "Magnitude": f"{self.__gcmt_mag[0]}-{self.__gcmt_mag[1]}",
            "Date start": str(self.__gcmt_date[0]),
            "Date end": str(self.__gcmt_date[1]),
            "nDay": str(self.__gcmt_date[2]),
            "script": self.__layer,
        }
        return self.focmec

    def layer_inset(self):
        width = abs(self.x2 - self.x1)
        height = abs(self.y2 - self.y1)
        ratio = height / width
        if width >= height:
            longer = width
        else:
            longer = height
        ##  untuk ukuran inset dengan persentase dari nilai aspect ratio peta
        match longer:
            case longer if longer < 1.25:
                dilatation = longer * 3.5
            case longer if longer >= 1.25 and longer < 2.5:
                dilatation = longer * 3
            case longer if longer >= 2.5 and longer < 5:
                dilatation = longer * 2.5
            case longer if longer >= 5 and longer < 15:
                dilatation = longer * 2
            case longer if longer >= 15:
                dilatation = longer * 1.5
        center_x = self.x1 + (width / 2)
        center_y = self.y1 + (height / 2)
        x1 = center_x - dilatation
        x2 = center_x + dilatation
        y1 = center_y - dilatation
        y2 = center_y + dilatation
        map_height = self.size * ratio
        if map_height >= self.size:
            self.inset_size = self.size / 3
        else:
            self.inset_size = map_height / 3
        self.inset_coord = (x1, x2, y1, y2)
        self.inset_R = f"-R{self.inset_coord[0]}/{self.inset_coord[1]}/{self.inset_coord[2]}/{self.inset_coord[3]}"
        self.inset_just = ui.get_inset_loc()
        self.inset_offset = self.size * 0.01
        self.rectangle = f">\n{self.x1}\t{self.y1}\n{self.x1}\t{self.y2}\n>\n{self.x1}\t{self.y2}\n{self.x2}\t{self.y2}\n>\n{self.x2}\t{self.y2}\n{self.x2}\t{self.y1}\n>\n{self.x2}\t{self.y1}\n{self.x1}\t{self.y1}"
        utils.file_writer(
            "w", f"rect_{self.name}.txt", self.rectangle, self.dir_output_path
        )
        self.__layer = """\tgmt inset begin -Dj{}+w{:.2f}c/{:.2f}+o{}c
        gmt coast {} -JM{:.2f} -Slightcyan -Glightsteelblue2 -EID+gseagreen2 -Ba+e -BnEwS -Ve--FORMAT_GEO_MAP=ddd:mm --MAP_FRAME_TYPE=inside --FONT_ANNOT_PRIMARY=auto,Courier-Bold,grey40
        gmt plot rect_{}.txt -Wthin,red {} -JM{:.2f} -Ve
        gmt inset end\n\tgmt basemap -Tdj{}+l,,,N+o0.5c -Ve\n """.format(
            self.inset_just[0],
            self.inset_size,
            self.inset_size + (self.inset_size * 0.1),
            self.inset_offset,
            self.inset_R,
            self.inset_size,
            self.name,
            self.inset_R,
            self.inset_size,
            self.inset_just[1],
        )
        print("inset map added..")
        self.inset = {
            "Type": "inset",
            "Loc": self.inset_just[2],
            "script": self.__layer,
        }
        return self.inset

    @property
    def map_layer(self):
        self.total_layers = len(self.layers)
        for layer in range(1, self.total_layers + 1):
            print(self.layers[f"layer{layer}"])
            print("=============================")

    @map_layer.setter
    def map_layer(self, value):
        self.layers = value

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
        utils.file_writer("a", script_name, "gmt end", self.dir_output_path)


class MainMap(Layer):
    """The child class which inherit from Layer class. Have method to display the map parameter information"""

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
 Map size   : {self.size} cm{17*" "} East : {self.x2:<13} North : {self.y2}
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
