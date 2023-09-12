import sys
import os

# https://stackoverflow.com/questions/3160699/python-progress-bar/34482761#34482761


class Progressbar:
    def __init__(self, count, prefix="", fd=sys.stderr) -> None:
        self.count = count
        self.prefix = prefix

        try:
            self.size = int(os.get_terminal_size().columns / 2) or 60
        except:
            self.size = 60

        self.fd = fd
        self.idx = 0
        self.done = False

    def start(self) -> None:
        self.update(0)

    def increment(self):
        self.idx += 1
        self.update(self.idx)

    def update(self, j):
        if j > self.count or j < 0:
            raise f"cannot update with {j} Bad value min(0) max({self.count})"

        x = int(self.size * j / self.count)
        self.fd.write(
            f"{self.prefix}[{u'█'*x}{('.'*(self.size-x))}] {j}/{self.count}" + "\r"
        )

        self.fd.flush()

    def end(self) -> None:
        if self.done == True:
            return

        self.done = True
        self.fd.write("\n")
        self.fd.flush()
