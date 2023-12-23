import utils, map_class


if __name__ == "__main__":
    utils.screen_clear()
    utils.header()

    map_main = map_class.MainMap()
    utils.screen_clear()
    map_main.general_info()
    map_main.layer_info()

    input("\nContinue to write the gmt script.. \n(press any key to continue)")
    map_main.layer_writer()

    input("\ncreating the map.. \n(press any key to continue)")
    utils.gmt_execute(map_main.name)

    print(f" The map : {map_main.name}.png successfully created in output folder")
    # while True:
    #     edit = input("edit the image (y/n) ?")
    #     match edit:
    #         case "y" | "Y" :
    #             print("which parameter you want to edit")

    #         case "n" | "N":
    #             print("Exiting the program..")
    #             break
    print(" End of the program ".center(80, "="))
