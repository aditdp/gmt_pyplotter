import os.path, map_overlay


def map_layout():
    ''' User input for map layout '''
    while True:
        print(" Interactive GMT ".center(50,"="))
        print("\n"+"Map type:")
        print("1. Single map")
        print("2. Multiple maps in one figure")
        print("0. Cancel")
        print("\n"+50*"=")
        user_map_type = input("Choose the map type: ")
        if user_map_type == "1":
            print("\nWill create single map\n")
            print("Done")
            break
            
        elif user_map_type == "2":
            print("\nWill create multiple map\n")
            break
        elif user_map_type == "0":
            print("\nCanceling..\n")
            break
        else:
            print("Please choose between 1 or 2..\n")
            continue
    return user_map_type

def file_name():
    while True:
        output_name = input("Name of the map: ")
        path = (f"./output/{output_name}.png")
        check_file = os.path.isfile(path)
    
        if check_file == True:
            try:
                print(f"The '{output_name}.png' in output folder, already exist")
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
            print(f"Map will be save as {output_name}.png")
            break
    return output_name

def projection():
    print("Proyeksi peta (tekan 'Enter' akan menggunakan default)")
    proj = input("Proyeksi peta:  ")
    if proj == "":
        proj = "M"
    print("Ukuran peta merupakan lebar peta dengan tinggi peta menyesuaikan batas koordinat nantinya")
    size = input("Masukan ukuran peta dalam centimeter: ")
    gmt_J = "-J"+proj+str(size)+"c"
    print(gmt_J)
    return gmt_J
        
def map_fill(*args):
    name_in = args[0]
    '''User input for map fill layer'''
    while True:
        print("\nThe map layer:")
        print("1. Coastal line")
        print("2. Earth relief")
        print("3. Contour line")
        print("4. Earthquake plot")
        print("5. Focal mechanism plot")
        print("6. Indonesia Regional Tectonics")
        print("0. Cancel")
        user_map_fill = input ("Choose the map layer: ")
        
        if user_map_fill == "1":
            
            map_overlay.map_coast(name_in)
            print("Coastal line layer added..")
            break
            
        elif user_map_fill == "2":
            
            map_overlay.map_grdimage(name_in)
            print("Earth relief layer added..")
            user_map_fill = "grdimage"
            break
            
        elif user_map_fill == "3":
            
            map_overlay.map_(name_in)
            print("Contour layer added..")
            user_map_fill = "contour"
            break
            
        elif user_map_fill == "4":
            
            map_overlay.map_(name_in)
            print("Earthquake layer added..")
            user_map_fill = "plot"
            break
            
        elif user_map_fill == "5":
            
            map_overlay.map_(name_in)
            print("Focal mechanism plot layer added..")
            user_map_fill = "meca"
            break
            
        elif user_map_fill == "6":
            map_overlay.map_(name_in)
            print("Indo Regional Tectonic layer added..")
            user_map_fill = "plot"
            break
        
        else:
            print("Please choose between 1 to 6")
            print("or 0 for cancel adding more layer")
            continue
        
    return user_map_fill

def color_land():
    print('leave empty for default color')
    colr_land = str(input("Choose the color of the land :") or "lightgreen")
    return colr_land

def color_sea():
    print('leave empty for default color')
    colr_sea = str(input("Choose the color of the sea : ") or "azure")
    return colr_sea

def color_focmec():
    print('leave empty for default color (red)')
    colr_fm = str(input("Choose the color of the beach ball : ") or "red")
    return colr_fm

def input_coordinate():
    ''' fungsi input koordinat peta dengan geographical projection'''

    while True:
        try:
            bound_x1 = float(input("Western boundary (W): "))
            if bound_x1 < -180 or bound_x1 > 180:
                print("W-E coordinate range -180 to 180 degree")
                continue
        except ValueError:
            print("Input numbers only")
            continue
        
        try:
            bound_x2 = float(input("Eastern boundary (E): "))
            if bound_x2 < -180 or bound_x2 > 180:
                print("W-E coordinate range -180 to 180 degree")
                continue
        except ValueError:
            print("Input numbers only")
            continue
        if bound_x1 >= bound_x2:
            print("\nWestern boundary must lesser than eastern boundary\n")
            continue
        elif bound_x1 <= bound_x2:
            bound_x1 = str(bound_x1)
            bound_x2 = str(bound_x2)
            break
    while True:
        try:
            bound_y1 = float(input("Southern boundary (S): "))
            if bound_y1 < -90 or bound_y1 > 90:
                print("Koordinat N-S antara -90 sampai 90 derajat")
                continue
        except ValueError:
            print("Masukan nilai angka")
            continue
        
        try:
            bound_y2 = float(input("Northern boundary (N): "))
            if bound_y2 < -90 or bound_y2 > 90:
                print("Koordinat N-S antara -90 sampai 90 derajat")
                continue
        except ValueError:
            print("Masukan nilai angka")
            continue
        
        if bound_y1 >= bound_y2:
            print("\nkoordinat batas selatan harus lebih kecil dari batas utara\n")
            continue
        elif bound_y1 <= bound_y2:
            bound_y1 = str(bound_y1)
            bound_y2 = str(bound_y2)
            break
    return [bound_x1,bound_x2,bound_y1,bound_y2]

def color_pallete():
    print("The 'Color Palette Tables' provided in 'example' folder.")
    colr_cpt = input("Choose the CPT:  ")
    cpt_color = f"-S{colr_cpt}"
    return cpt_color

def grdimage_shading():
    shade = input("Shade the elevation model (y/n)?  ")
    if shade == "y" or shade == "Y":
        shading = "-I+d"
    else:
        shading = ""
    return shading
    
def grd_res():
    print("Choose the image resolution")
    print('''SRTMGL1 (need internet connection)
          1. Full   (01 second)
          2. High   (15 second)
          3. Medium (01 minute)
          4. Low    (05 minute)
          5. Crude  (10 minute)
          ''')
    grd_resolution = input("Image resolution: ")
    if 





















