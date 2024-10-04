from tkinter.filedialog import askdirectory

path = askdirectory()

print(path)

pathwindows = path.split("/")

print(pathwindows)
