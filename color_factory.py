
class ColorFactoryInterface():
    def __iter__(self):
        pass

    def __next__(self):
        pass


class ColorFactorySimple (ColorFactoryInterface):
    def __init__(self, inc=5):
        self.r, self.g, self.b = 0,0,0
        self.depth = 3
        self.inc =  inc
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

    # TODO remove duplicates

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
