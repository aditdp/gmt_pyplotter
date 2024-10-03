import subprocess

command = "gmt grdinfo -R120.0/125.0/-9.0/-4.0 @earth_relief_15s -Cn -M -G"


msg_from_gmt = subprocess.run(command, shell=True, capture_output=True, text=True)
inform = msg_from_gmt.stdout.split()
print(type(msg_from_gmt.stdout))
elev_max = int(inform[5])
print(type(elev_max), f"ketinggian max = {elev_max}")
print(f"kedalaman max = {inform[4]}")
print(f"dari python :{int(inform[5])}")

total_elev = inform[5] + abs(inform[4])
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
