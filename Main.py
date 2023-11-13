
import os
import user_input, map_overlay

os.system("clear")
print("Welcome to interactive GMT")

layout = user_input.map_layout()
output_name = user_input.file_name()

print("Main map coordinate..")
batas = user_input.input_coordinate()
print(batas)
print(type(batas))


gmt_R = f"-R{batas[0]}/{batas[1]}/{batas[2]}/{batas[3]}"
print(gmt_R)

gmt_J = user_input.projection()

map_overlay.map_base(output_name,gmt_R,gmt_J)

map_fill_dict = {}
for layer in range(1, 6):
    map_fill_dict["map_layer_{0}".format(layer)] = user_input.map_fill(output_name)
    add_layer = input("Add another layer (y/n): ")
    if add_layer == "y" or add_layer == "Y":
        continue
    else:
        with open(output_name +".gmt","a") as file:
            file.write(f"gmt end") 
        break
    
print(map_fill_dict)

while True:
    print("\n"+50*"=")
    is_done = input("Create another map (y/n)? ")
    if is_done == "n" or is_done == "N":
        os.system(f"chmod 777 {output_name}.gmt")
        os.system(f"./{output_name}.gmt")
        print("\n"+15*"="+" End of the programs "+15*"="+"\n")
        break
        

