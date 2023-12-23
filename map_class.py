import user_input as ui
import utils
import os, copy
from itertools import zip_longest


class FileName:
    def __init__(self) -> str:
        self.fname = ui.file_name()

    @property
    def name(self):
        return self.fname

    # @name.setter
    # def name(self, new_name):
    #     self.fname = new_name


class Coordinate:
    def __init__(self):
        self.bound_x1, self.bound_x2 = ui.input_coord_x()
        self.bound_y1, self.bound_y2 = ui.input_coord_y()

    def mid_x(self):
        return (self.bound_x2 + self.bound_x1) / 2

    def mid_y(self):
        return (self.bound_y2 + self.bound_y1) / 2

    @property
    def x1(self):
        return self.bound_x1

    @x1.setter
    def x1(self, value: float):
        self.bound_x1 = value

    @property
    def x2(self):
        return self.bound_x2

    @x2.setter
    def x2(self, value: float):
        self.bound_x2 = value

    @property
    def y1(self):
        return self.bound_y1

    @y1.setter
    def y1(self, value: float):
        self.bound_y1 = value

    @property
    def y2(self):
        return self.bound_y2

    @y2.setter
    def y2(self, value: float):
        self.bound_y2 = value

    @property
    def boundary(self):
        print("getting the coordinate from main map..")
        return [self.bound_x1, self.bound_x2, self.bound_y1, self.bound_y2]

    @property
    def coord_script(self):
        return f"-R{self.bound_x1}/{self.bound_x2}/{self.bound_y1}/{self.bound_y2}"


class Projection:
    def __init__(self):
        self.proj = ui.input_projection()
        self.size = ui.input_size()

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


# class InsetMap(Coordinate, Projection):
#     def __init__(self):
#         Coordinate.__init__(self)
#         Projection.__init__(self)


class Layer(FileName, Coordinate, Projection):
    def __init__(self):
        FileName.__init__(self)
        Coordinate.__init__(self)
        Projection.__init__(self)
        utils.screen_clear()
        MainMap.general_info(self)
        print("Adding layer for main map..\n")
        self.layers = dict()
        for layer in range(1, 6):
            self.layers[f"Layer {layer}"] = self.input_map_fill()
            utils.screen_clear()
            MainMap.general_info(self)
            MainMap.layer_info(self)
            if self.layers[f"Layer {layer}"]["script"] == "cancel":
                del self.layers[f"Layer {layer}"]
                break

            add_layer = input("Add another layer (y/n):  ")
            if add_layer == "y" or add_layer == "Y":
                continue
            elif add_layer == "n" or add_layer == "N":
                print(f"{layer} layers added to the map")
                break

    def input_map_fill(self):
        """User input for map fill layer"""

        while True:
            print("\nThe map layer:")
            print("1. Coastal line")
            print("2. Earth relief")
            print("3. Contour line")
            print("4. Earthquake plot")
            print("5. Focal mechanism plot")
            print("6. Indonesia Regional Tectonics")
            print("7. Map inset")
            print("0. Cancel")
            user_map_fill = input("Choose the map layer: ")

            if user_map_fill == "1":
                user_layer = self.layer_coast()
                print("Coastal line layer added..")
                user_map_fill = "coast"
                break

            elif user_map_fill == "2":
                user_layer = self.layer_grdimage()
                print("Earth relief layer added..")
                user_map_fill = "grdimage"
                break

            elif user_map_fill == "3":
                user_layer = self.layer_contour()
                print("Contour layer added..")
                user_map_fill = "contour"
                break

            elif user_map_fill == "4":
                user_layer = self.layer_earthquake()
                print("Earthquake layer added..")
                user_map_fill = "plot"
                break

            elif user_map_fill == "5":
                user_layer = self.layer_focmec()
                print("Focal mechanism plot layer added..")
                user_map_fill = "meca"
                break

            elif user_map_fill == "6":
                user_layer = self.layer_indo_tecto()
                print("Indo Regional Tectonic layer added..")
                user_map_fill = "plot"
                break

            elif user_map_fill == "7":
                user_layer = self.layer_inset()
                print("Inset map added..")
                user_map_fill = "inset"
                break

            elif user_map_fill == "0":
                print("Cancel adding another layer..")
                user_layer = {"script": "cancel"}
                break

            else:
                print("Please choose between 1 to 6")
                print("or 0 for cancel adding more layer")
                continue
        return user_layer

    @property
    def layer_base(self):
        self.__layer = f"gmt begin {self.name} png \n\tgmt basemap {self.coord_script} {self.proj_script} -Ba\n"

        self.base_script = {
            "projection": self.proj_script,
            "coordinate": self.coord_script,
            "script": self.__layer,
        }
        return self.base_script, self.__layer

    def layer_coast(self):
        self.__colr_land = ui.color_land()
        self.__colr_sea = ui.color_sea()
        self.__layer = f"\tgmt coast -S{self.__colr_sea} -G{self.__colr_land}\n"
        self.coast = {
            "Type": "coast",
            "Land color": self.__colr_land,
            "Sea color": self.__colr_sea,
            "script": self.__layer,
        }

        return self.coast

    def layer_grdimage(self):
        self.__shading, shade = ui.grdimage_shading()
        self.__cpt_color = ui.color_palette()
        self.__resolution, res = ui.grdimage_resolution()
        self.__layer = f"\tgmt grdimage {self.__resolution} {self.__shading} -S{self.__cpt_color} \n"

        self.grdimage = {
            "Type": "earth relief",
            "shading": shade,
            "cpt": self.__cpt_color,
            "resolution": res,
            "script": self.__layer,
        }
        return self.grdimage

    def layer_contour(self):
        self.__contours_major = input("Major contours interval (meters):  ")
        self.__contours_minor = input("Minor contours interval (meters):  ")
        self.__layer = f"\tgmt grdcontour @earth_relief_15s -A{self.__contours_major} -C{self.__contours_minor} -Wathin,gray50 -Wcfaint,gray90"

        self.contour = {
            "Type": "contour",
            "Interval": self.__contours_major,
            "Interval2": self.__contours_minor,
            "script": self.__layer,
        }
        return self.contour

    def layer_indo_tecto(self):
        fault = os.getcwd() + "/data/fault_sukamto2011"
        self.__layer = f"\tgmt  plot {fault} -W1p,black,solid -Sf+1i/0.2i+l+t\n"

        self.indo_tecto = {"script": self.__layer}
        return self.indo_tecto

    def layer_earthquake(self):
        self.eq_file = f"{os.getcwd()}/data/{self.name}_usgs.txt"
        self.__scaler = float(self.map_size) * 0.0005

        self.__usgs_date = ui.date_start_end()
        if os.name == "posix":
            self.__layer = (
                f"\tgmt makecpt -Cred,green,blue -T0,70,150,10000 -N\n"
                + """\tgawk -F "," '{ print $3,$2,$4,$5*$5*"""
                + str(self.__scaler)
                + "}' "
                + self.eq_file
                + """| gmt plot -C -Scc -hi1 -Wfaint\n"""
            )
        elif os.name == "nt":
            self.__layer = (
                f"\tgmt makecpt -Cred,green,blue -T0,70,150,10000 -N\n"
                + """\tgawk -F "," "{ print $3,$2,$4,$5*$5*"""
                + str(self.__scaler)
                + '}" '
                + self.eq_file
                + """| gmt plot -C -Scc -hi1 -Wfaint\n"""
            )
        utils.usgs_downloader(self.eq_file, self.boundary, self.__usgs_date)
        self.earthquake = {
            "Type": "earthquake plot",
            "Source": "USGS",
            "Date start": str(self.__usgs_date[0]),
            "Date end": str(self.__usgs_date[1]),
            "nDay": str(self.__usgs_date[2]),
            "script": self.__layer,
        }

        return self.earthquake

    def layer_focmec(self):
        self.fm_file = f"{self.name}_gcmt"
        self.__gcmt_date = ui.date_start_end()
        self.__scaler = float(self.map_size) * 0.02
        self.__layer = "\tgmt makecpt -Cred,green,blue -T0,70,150,10000 -N\n\tgmt meca ../data/{}.csv -Sd{}c+f0 -C -W0.1p,gray50\n".format(
            self.fm_file,
            self.__scaler,
        )
        utils.gcmt_downloader(self.fm_file, self.boundary, self.__gcmt_date)
        self.focmec = {
            "Type": "focal mechanism",
            "Source": "Global CMT",
            "Date start": str(self.__gcmt_date[0]),
            "Date end": str(self.__gcmt_date[1]),
            "nDay": str(self.__gcmt_date[2]),
            "script": self.__layer,
        }

        return self.focmec

    def layer_inset(self):
        x_add = (self.x2 - self.x1) * 3
        y_add = (self.y2 - self.y1) * 3
        x1 = self.x1 - x_add
        x2 = self.x2 + x_add
        y1 = self.y1 - y_add
        y2 = self.y2 + y_add
        ratio = (self.y2 - self.y1) / (self.x2 - self.x1)
        self.inset_coord = (x1, x2, y1, y2)

        self.inset_R = f"-R{self.inset_coord[0]}/{self.inset_coord[1]}/{self.inset_coord[2]}/{self.inset_coord[3]}"
        self.inset_width = self.size / 3
        self.inset_height = self.inset_width * ratio
        self.inset_just = ui.inset_loc()
        self.inset_offset = self.size / 50
        self.rectangle = f">\n{self.x1}\t{self.y1}\n{self.x1}\t{self.y2}\n>\n{self.x1}\t{self.y2}\n{self.x2}\t{self.y2}\n>\n{self.x2}\t{self.y2}\n{self.x2}\t{self.y1}\n>\n{self.x2}\t{self.y1}\n{self.x1}\t{self.y1}"
        utils.file_writer("w", f"rect_{self.name}", self.rectangle, format=".txt")

        self.__layer = """\tgmt inset begin -Dj{}+w{:.2f}c/{:.2f}c+o{:.2f}c -F+c0.1c
        gmt coast {} -JM{:.2f} -Sazure -Glightgreen -Ba -BneWS -X0.8c -Y0.5c --FORMAT_GEO_MAP=ddd:mm --MAP_FRAME_TYPE=plain
        gmt plot rect_{}.txt -Wthin,red {} -JM{:.2f}
    gmt inset end\n""".format(
            self.inset_just,
            self.inset_width,
            self.inset_height,
            self.inset_offset,
            self.inset_R,
            self.inset_width - 1,
            self.name,
            self.inset_R,
            self.inset_width - 1,
        )

        print("inset map added..")

        self.inset = {
            "Type": "inset",
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
                extension = ".gmt"
            case "nt":
                extension = ".bat"
        print(f"nama file: {self.name}")
        utils.file_writer("w", self.name, self.layer_base[1], format=extension)

        for layer in range(1, len(self.layers) + 1):
            utils.file_writer(
                "a",
                self.name,
                (self.layers[f"Layer {layer}"]["script"]),
                format=extension,
            )
        utils.file_writer("a", self.name, "gmt end", format=extension)


class MainMap(Layer):
    def __init__(self):
        Layer.__init__(self)

    def general_info(self):
        """Printing basic map parameter"""
        if self.proj == "M":
            proj = "Mercators"
        elif self.proj == "G":
            proj = "Globe"
        general = f"""
{"  MAP PARAMETER  ".center(80, "=")} 

    File name  : {self.name:<20} Coordinate :
    Projection : {proj:<24} West : {self.x1:<13} South : {self.y1}
    Map size   : {self.size} cm{19*" "} East : {self.x2:<13} North : {self.y2}
        
        """
        print(general)

    def layer_info(self):
        """Printing the layer info"""
        layer_print = copy.deepcopy(self.layers)
        for layer in range(1, len(layer_print) + 1):
            del layer_print[f"Layer {layer}"]["script"]
        self.__columns = list(layer_print.keys())
        print("  LAYERS  ".center(80, "="))
        print("")

        match len(layer_print):
            case 1:
                print("  Layer 1")
                print((80 * "-"))
                for key, val in layer_print["Layer 1"].items():
                    print(f"  {key:<10}: {val}")

            case 2:
                dkeys = list(
                    zip_longest(
                        layer_print["Layer 1"], layer_print["Layer 2"], fillvalue=" "
                    )
                )

                dvalues = list(
                    zip_longest(
                        layer_print["Layer 1"].values(),
                        layer_print["Layer 2"].values(),
                        fillvalue=" ",
                    )
                )

                print(" ", (21 * " ").join(self.__columns))
                print((80 * "-"))
                for l1, l2 in zip(dkeys, dvalues):
                    print(f"  {l1[0]:<10}: {l2[0]:<15} {l1[1]:<10}: {l2[1]:<15}")

            case 3:
                dkeys = list(
                    zip_longest(
                        layer_print["Layer 1"],
                        layer_print["Layer 2"],
                        layer_print["Layer 3"],
                        fillvalue=" ",
                    )
                )

                dvalues = list(
                    zip_longest(
                        layer_print["Layer 1"].values(),
                        layer_print["Layer 2"].values(),
                        layer_print["Layer 3"].values(),
                        fillvalue=" ",
                    )
                )

                print(" ", (21 * " ").join(self.__columns))
                print((80 * "-"))
                for l1, l2 in zip(dkeys, dvalues):
                    print(
                        f"  {l1[0]:<10}: {l2[0]:<15} {l1[1]:<10}: {l2[1]:<15} {l1[2]:<10}: {l2[2]:<15} "
                    )

            case 4:
                dkeys = list(
                    zip_longest(
                        layer_print["Layer 1"],
                        layer_print["Layer 2"],
                        layer_print["Layer 3"],
                        layer_print["Layer 4"],
                        fillvalue=" ",
                    )
                )

                dvalues = list(
                    zip_longest(
                        layer_print["Layer 1"].values(),
                        layer_print["Layer 2"].values(),
                        layer_print["Layer 3"].values(),
                        layer_print["Layer 4"].values(),
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

            case 5:
                dkeys = list(
                    zip_longest(
                        layer_print["Layer 1"],
                        layer_print["Layer 2"],
                        layer_print["Layer 3"],
                        layer_print["Layer 4"],
                        layer_print["Layer 5"],
                        fillvalue=" ",
                    )
                )

                dvalues = list(
                    zip_longest(
                        layer_print["Layer 1"].values(),
                        layer_print["Layer 2"].values(),
                        layer_print["Layer 3"].values(),
                        layer_print["Layer 4"].values(),
                        layer_print["Layer 5"].values(),
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
        print((80 * "="))

    def gmt_execute(self):
        os.chdir(os.getcwd() + "/output")
        os.system(f"{os.getcwd()}/{self.name}.bat")
