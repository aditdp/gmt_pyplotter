import time

print("This line will be deleted")
time.sleep(2)
print("\033[1A\033[2K", end="")  # Move cursor up and clear the line
print("This is a new line")
