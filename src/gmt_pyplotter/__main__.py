from gmt_pyplotter import map_class, utils
from gmt_pyplotter import user_input as ui
import os, sys


def main():
    try:
        utils.check_terminal_size()
        utils.system_check()
        utils.screen_clear()
        utils.header()

        map_main = map_class.MainMap()
        utils.screen_clear()
        map_main.general_info()
        map_main.layer_info()

        map_main.layer_writer()

        utils.finalization_bar(1)
        utils.gmt_execute(map_main.name, map_main.dir_output_path)
        utils.finalization_bar(2)
        print("\n\n")
        ui.printc(
            f"  {map_main.name}.{map_main.format} successfully created in output folder"
        )
        print("\n")
        utils.pictureshow(
            os.path.join(
                map_main.dir_output_path,
                f"{map_main.name}.{map_main.format}",
            )
        )
        utils.app_usage_log(
            map_main.name,
            map_main.format,
            map_main.dir_output_path,
            map_main.boundary,
            map_main.layers,
        )
        utils.closing()
    except KeyboardInterrupt:
        ui.printe("\n\n    KeyboardInterrupt: Exiting the program..\n")
        utils.closing()
        try:
            sys.exit(130)
        except SystemExit():
            os._exit(130)


# cek aplikasi dependency: gmt, gawk, awk   : done
# fix finalization bar                      : done
# layer kontur tidak mau plot               : done
# layer tektonik belum ada info             : done
# eq legend and colorbar                    : not yet
# cek semua fungsi                          : done
# color land sea focmec, error code         : done
# output format ditambahkan                 : done
# color_bar location                        : done
# grdimage belom fix untuk download
# pindahan utils download ke map class
