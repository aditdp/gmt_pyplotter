# from datetime import date
import os


# end = date(2024, 2, 10)
# selisih = date.today() - end
# print(selisih)
# print(date.today())


class FileName:
    def __init__(self) -> str:
        self.output_path = os.getcwd()
        self.fname = "baru"

    @property
    def name(self):
        return self.fname

    @property
    def dir_output_path(self):
        return self.output_path

    @property
    def fig_output_path(self):
        return os.path.join(f"{self.output_path}{self.fname}.png")


baru = FileName()
print(baru.fname)
print(baru.name)
print(baru.fig_output_path)
nama = baru.fig_output_path

print(f"nama adalah = {nama}")
