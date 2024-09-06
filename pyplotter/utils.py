import os, subprocess, time
from urllib.request import urlretrieve, urlopen


# import user_input as ui

# from test_class import Coordinate as C_


def header():
    print(80 * "=")
    print("")
    print("GMT pyplotter".center(80, " "))
    print("interactive map ploting with Generic Mapping Tools".center(80, " "))
    print("")
    print(80 * "=")
    print("")
    
    # print(
    #     """there is 4 stage for creating map
    #       1. Main map coordinate
    #       2. Projection
    #       3. """
    # )


def screen_clear():
    if os.name == "posix":
        os.system("clear")
    elif os.name == "nt":
        os.system("cls")
    else:
        os.system("cls")


def file_writer(*args):
    flag = args[0]
    script_name = args[1]
    layer = args[2]
    print(layer)

    with open(
        os.path.join(os.getcwd(), "gmt_pyplotter", "output", script_name), flag
    ) as file:
        file.write(layer)

    # print(args)
    # if os.name == "posix" and kwargs["format"] is None:
    #     with open("output/" + output + ".gmt", flag) as file:
    #         file.write(layer)
    # elif os.name == "nt" and kwargs["format"] is None:
    #     with open("output/" + output + ".bat", flag) as file:
    #         file.write(layer)

    # elif kwargs["format"] is not None:
    #     with open("output/" + output + kwargs["format"], flag) as file:
    #         file.write(layer)


def gcmt_downloader(*args):
    fm_file = args[0]
    coord = args[1]
    date = args[2]
    url_gcmt = "https://www.globalcmt.org/cgi-bin/globalcmt-cgi-bin/CMT5/form?itype=ymd&yr={}&mo={}&day={}&otype=nd&nday={}&llat={}&ulat={}&llon={}&ulon={}&list=6".format(
        date[0].strftime("%Y"),
        date[0].strftime("%m"),
        date[0].strftime("%d"),
        date[2],
        coord[2],
        coord[3],
        coord[0],
        coord[1],
    )
    print(f"retrieving data from:\n {url_gcmt}")
    page = urlopen(url_gcmt)
    html = page.read().decode("utf-8")
    start_index = html.rfind("<pre>") + 6
    end_index = html.rfind("</pre>")
    data_gcmt = html[start_index:end_index]
    print("data acquired..")
    # input("press any key to continue..")
    print(data_gcmt)
    with open(fm_file, "w") as file:
        file.write(data_gcmt)
    print("done..")


def usgs_downloader(*args):
    usgs_cata_file = args[0]
    coord = args[1]
    date = args[2]
    url_usgs = "https://earthquake.usgs.gov/fdsnws/event/1/query?format=csv"
    url_loc = f"minlongitude={coord[0]}&maxlongitude={coord[1]}&minlatitude={coord[2]}&maxlatitude={coord[3]}"
    url_date = f"starttime={date[0]}&endtime={date[1]}"
    url = f"{url_usgs}&{url_date}&{url_loc}"

    print(f"\nRetrieving data from: {url}")
    urlretrieve(url, usgs_cata_file)
    print(f"\n Done.. \n")


def isc_downloader(*args):
    isc_cata_file = args[0]
    coord = args[1]
    date = args[2]
    mag = args[3]
    depth = args[4]
    url_isc = "https://www.isc.ac.uk/cgi-bin/web-db-run?request=COMPREHENSIVE&out_format=CATCSV&bot_lat={}&top_lat={}&left_lon={}&right_lon={}&searchshape=RECT&start_year={}&start_month={}&start_day={}&end_year={}&end_month={}&end_day={}&min_dep={}&max_dep={}&min_mag={}&max_mag={}".format(
        coord[2],
        coord[3],
        coord[0],
        coord[1],
        date[0].strftime("%Y"),
        date[0].strftime("%m"),
        date[0].strftime("%d"),
        date[1].strftime("%Y"),
        date[1].strftime("%m"),
        date[1].strftime("%d"),
        depth[0],
        depth[1],
        mag[0],
        mag[1],
    )
    print(f"data file is located in {isc_cata_file}")
    # input("pause")
    print(f"retrieving data from:\n {url_isc}")
    page = urlopen(url_isc)
    html = page.read().decode("utf-8")
    start_index = html.rfind("<pre>") + 252
    end_index = html.rfind("STOP") - 1
    data_isc = html[start_index:end_index]
    print("data acquired..")
    # input("press any key to continue..")
    print(data_isc)
    with open(isc_cata_file, "w") as file:
        file.write(data_isc)
    print("done..")


def gmt_execute(name):
    loc = os.path.join(os.getcwd(), "gmt_pyplotter", "output")
    match os.name:
        case "posix":
            os.system(f"chmod +x {loc}/{name}.gmt")
            print("make the script executable..")
            os.chdir(loc)
            os.system(f"./{name}.gmt")

        case "nt":
            os.chdir(loc)
            os.system(f"{name}.bat")


import shutil, sys


def is_gmt_installed():
    """Check whether program_name is installed."""
    match os.name:
        case "posix":
            shelll = "True"
        case "nt":
            shelll = "False"
    gmt_location = shutil.which("gmt")
    if gmt_location:
        getVersion = subprocess.Popen(
            "gmt --version", shell=shelll, stdout=subprocess.PIPE
        ).stdout
        gmt_ver = getVersion.read()
        ver_number = gmt_ver.decode().rstrip()
        
        if float(ver_number[0:3]) >= 6.2:
            logo_brin(f"GMT is installed at : {gmt_location}",f"GMT version {ver_number}"," ")
            
            # print("\nloading..")
            time.sleep(0)
            loading_bar(0,100)
        else:
            logo_brin("Please install GMT version 6.2.0 or latter..","https://docs.generic-mapping-tools.org/latest/install.html","")
                    
            input("Press any key to abort ..")
            sys.exit(" Upgrade the GMT version to 6.2.0 or latter ..")

    else:
        logo_brin()
        print(
            "Generic Mapping Tools is required, please download and install GMT version 6.2.0 or latter.."
        )
        print("https://docs.generic-mapping-tools.org/latest/install.html")
        input("Press any key to abort ..")
        sys.exit("GMT is not installed")

def logo_brin(*args):
    pr1 = args[0]
    pr2 = args[1]
    pr3 = args[2]
    print(f'''\033[91m
                 ↑↑↑↑↑↑↑↑↑↑↑↑             
                  ↑↑↑↑↑↑↑↑↑↑↑↑↑↑       
       ↑↑↑↑↑↑      ↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑        \033[00m {pr1} \033[91m
     ↑↑↑↑↑↑↑↑↑↑     ↑↑↑↑↑↑↑↑↑ ↑↑↑↑↑↑      \033[00m {pr2} \033[91m
    ↑↑↑↑↑↑↑↑↑↑↑↑↑    ↑↑↑↑↑↑↑↑  ↑↑↑↑↑↑↑    \033[00m {pr3} \033[91m
   ↑↑↑↑↑↑↑↑↑↑↑↑↑↑    ↑↑↑↑↑        ↑↑↑↑↑   
   ↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑   ↑↑↑↑↑↑↑    ↑↑↑↑↑↑↑↑  
   ↑↑↑↑↑↑↑↑↑↑↑↑↑↑    ↑↑↑↑↑↑↑↑  ↑↑↑↑↑↑↑↑↑  
    ↑↑↑↑↑↑↑↑↑↑↑↑      ↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑ 
      ↑↑↑↑↑↑↑↑↑        ↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑ 
                                          
 ↑↑                   ↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑ 
 ↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑    ↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑  
 ↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑   ↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑  
  ↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑  ↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑   
   ↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑  ↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑    
    ↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑  ↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑     \033[00m _____________________________________\033[91m
      ↑↑↑↑↑↑↑   ↑   ↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑      \033[00m  © BRIN \033[91m     
        ↑↑↑↑↑↑↑↑   ↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑        \033[00m  Badan Riset dan Inovasi Nasional\033[91m 
          ↑↑↑↑↑↑  ↑↑↑↑↑↑↑↑↑↑↑↑↑↑          \033[00m \x1B[3m National Research and Innovation \033[91m 
                ↑↑↑↑↑↑↑↑↑↑↑↑              \033[00m \x1B[3m Agency of Indonesia  ''') 

def loading_bar(begin, end):
    print(f'\n')
    for x in range(begin, end + 1):
        percent = 73 * (x / end)
        bar = "█" * int(percent) + "-" * (73 - int(percent))
        print(f"\r|{bar}| {100*x/end:.0f}%", end="\r")
        x + 1
        time.sleep(0.02)
        
def finalization_bar():
    loading_bar
    print()
    
    #  ↑↑↑↑↑↑↑      ↑↑↑↑↑↑     ↑    ↑↑     ↑ 
#  ↑     ↑↑     ↑     ↑    ↑    ↑ ↑↑   ↑ 
#  ↑↑↑↑↑↑↑↑     ↑↑↑↑↑↑↑    ↑    ↑   ↑↑ ↑ 
#  ↑     ↑↑     ↑     ↑    ↑    ↑     ↑↑ 
#  ↑↑↑↑↑↑↑      ↑     ↑    ↑    ↑      ↑             
# 
#   ██████████   ██████████    ███   █████    ███
#   ███     ███  ███     ███   ███   ██████   ███ 
#   ███     ███  ███     ███   ███   ███ ███  ███ 
#   ██████████   ██████████    ███   ███  ███ ███ 
#   ███     ███  ███     ███   ███   ███   ██████ 
#   ███     ███  ███     ███   ███   ███    █████ 
#   ██████████   ███     ███   ███   ███     ████
#   
# ______   ______ _____ __   _
# |_____] |_____/   |   | \  |
# |_____] |    \_ __|__ |  \_|
# 
# 
#  __   __        
# |__) |__) | |\ |
# |__) |  \ | | \|
# 