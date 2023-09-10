import math
from typing import Final

class ColorFactoryInterface():
    def __iter__(self):
        pass

    def __next__(self):
        pass
    def total(self) -> int:
        pass

class ColorFactorySimple (ColorFactoryInterface):
    def __init__(self, inc=5):
        self.r, self.g, self.b = 0,0,0
        self.depth = 3
        self.inc : Final =  inc

        self.count = 0
        self.__len__ = self.total
    def __iter__(self):
        return self
    
    def cval (_,val):
        return min(val, 255)
    def __next__(self):
        vals = (self.cval(self.r),
                 self.cval(self.g),
                  self.cval(self.b))

    #   for r in range(18):
    #     for g in range(18):
    #         for b in range(18):

        if self.depth <= 1: raise StopIteration
        self.count += 1

        if self.depth == 3:
            self.b += self.inc
            if self.b - 254 >= self.inc:
                self.depth -= 1
                self.b = 0
        if self.depth == 2: 
            self.g += self.inc
            if self.g -  254 >= self.inc:
                self.depth -= 1
                self.g = 0
            else: self.depth += 1
        if self.depth == 1:
            self.r += self.inc
            if self.r - 254 >= self.inc:
                self.depth -= 1
                self.r = 0
            else: self.depth += 1

        return vals

    def total(self) -> int:
        x = math.ceil(255 / self.inc )

        if x > 127:
            x -= 1 # how this thing works i do not know

        # return ((x + 1) * x + 1) * (x + 1) + x
        return (x + 1)**3 - x ** 2 # Don't forget the reset "a.k.a" 0th mode and then remove dupes 