from . import map_class
from . import utils
import os, sys


try:
    utils.screen_clear()
    utils.header()
    utils.is_gmt_installed()
    utils.screen_clear()
    utils.header()

    map_main = map_class.MainMap()
    utils.screen_clear()
    map_main.general_info()
    map_main.layer_info()
    # print("\nContinue to write the gmt script.. \n(press any key to continue)")
    utils.finalization_bar(0)
    map_main.layer_writer()
    # print("\ncreating the map.. \n(press any key to continue)")
    utils.finalization_bar(1)
    utils.gmt_execute(map_main.name)
    utils.finalization_bar(2)
    print(f" {map_main.name}.png successfully created in output folder")
except KeyboardInterrupt:
    print("\n\nexiting the program..\n")

    print(" End of the program ".center(80, "="))
    try:
        sys.exit(130)
    except SystemExit:
        os._exit(130)

# cek aplikasi dependency: gmt, gawk, awk
