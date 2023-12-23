import os, datetime
from urllib.request import urlretrieve, urlopen


# import user_input as ui

# from test_class import Coordinate as C_


def header():
    print("Welcome to interactive GMT..")
    print("interactive way of ploting maps with Generic Mapping Tools\n")
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


def file_writer(*args, **kwargs):
    flag = args[0]
    output = args[1]
    layer = args[2]
    with open("output/" + output + kwargs["format"], flag) as file:
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


def usgs_downloader(*args):
    eq_file = args[0]
    coord = args[1]
    date = args[2]
    url_usgs = "https://earthquake.usgs.gov/fdsnws/event/1/query?format=csv"
    url_loc = f"minlongitude={coord[0]}&maxlongitude={coord[1]}&minlatitude={coord[2]}&maxlatitude={coord[3]}"
    url_date = f"starttime={date[0]}&endtime={date[1]}"
    url = f"{url_usgs}&{url_date}&{url_loc}"

    print(f"\nRetrieving data from: {url}")
    urlretrieve(url, eq_file)
    print(f"\n Done.. \n")


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
    input("press any key to continue..")
    print(data_gcmt)
    with open(f"data/{fm_file}.csv", "w") as file:
        file.write(data_gcmt)
    print("done..")


def gmt_execute(name):
    if os.name == "posix":
        os.chdir(os.getcwd() + "/output")
        os.system(f"{os.getcwd()}/{name}.gmt")

    elif os.name == "nt":
        os.chdir(os.getcwd() + "/output")
        os.system(f"{os.getcwd()}/{name}.bat")
