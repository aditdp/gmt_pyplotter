
import user_input

# class Coordinate_square:
#     def __init__(self, name, left, right, bottom, top):#         self.name = name
#         self.west = left
#         self.east = right
#         self.south = bottom
# #         self.north = top     

def gmt_writer(*args):
    file_name = args[0]
    with open(file_name+".gmt","a") as file:
        file.write(args[1])

def map_base(*arg):
    file_name = arg[0]
    gmt_J = arg[1]
    gmt_R = arg[2]
    with open(file_name +".gmt","w") as file:
        file.write(f"gmt begin {file_name} png\n\tgmt basemap {gmt_R} {gmt_J} -Ba\n")

def map_coast(*arg):
    file_name = arg[0]
    colr_land = user_input.color_land()
    colr_sea = user_input.color_sea()
    layer = f"\tgmt coast -S{colr_sea} -G{colr_land}\n"
    gmt_writer(file_name, layer)

def map_grdimage(*name):
    file_name = name[0]
    shading = user_input.grdimage_shading()
    cpt_color = user_input.color_pallete()
    grd_resolution = user_input.
    layer = f"\tgmt grdimage @earth_relief_01s {shading} {cpt_color} \n"
    gmt_writer(file_name, layer)

def map_contour(*name):
    contour_interval = ""
    contour_major = ""
    contour_color = ""
    
    file_name = name

def map_indo_tecto(*name):
    file_name = name
    
def map_eartquake(*name):
    source = "usgs"
    time_start = ""
    time_end = ""
    number_day = ""
    mag_min = ""
    mag_max = ""
    depth_min = ""
    depth_max = ""
    legend_loc =  ""
    
    file_name = name    
    
def map_focmec(*name):
    file_name = name
    source = "Global CMT"
    time_start = ""
    time_end =""
    number_day =""
    mag_min = ""
    mag_max = ""
    depth_min = ""
    depth_max = ""
    legend_loc = ""
    
def map_inset():
    Coordinate = "manual or ID"
    print("inset map added..")
    
    
#def map_marker():
    
   
#================================================================================