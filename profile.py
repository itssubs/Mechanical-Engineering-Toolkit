class SectionProfile:
    def __init__(self, name):
        self.name = name

class Rectangular(SectionProfile):
    def __init__(self, width, height, name):
        super().__init__(name)
        self.width = width #m
        self.height = height #m
    
    @property
    def width(self):
        return self._width
    @width.setter
    def width(self, value):
        if value <= 0:
            raise ValueError(f"Width should be greater than 0")
        self._width = value

    @property
    def height(self):
        return self._height
    @height.setter
    def height(self, value):
        if value <= 0:
            raise ValueError(f"Height should be greater than 0")
        self._height = value

    @property
    def area(self):
        return self.width * self.height
    
    @property
    def Ixx(self):
        return self.width * (self.height ** 3) / 12
    
    @property
    def Iyy(self):
        return self.height * (self.width ** 3) / 12
    
    @property
    def Izz(self):
        return self.Ixx + self.Iyy
    
class Circular(SectionProfile):
    def __init__(self, radius, name):
        super().__init__(name)
        self.radius = radius

    @property
    def radius(self):
        return self._radius
    
    @radius.setter
    def radius(self, value):
        if value <= 0:
            raise ValueError(f"Radius should greater than 0")
        self._radius = value
        
    @property
    def area(self):
        return 3.14159 * (self.radius ** 2)
    
    @property
    def Ixx(self):
        return 3.14159 * (self.radius ** 4) / 4
    
    @property
    def Iyy(self):
        return 3.14159 * (self.radius ** 4) / 4
    
    @property
    def Izz(self):
        return self.Ixx + self.Iyy
    
class I(SectionProfile):
    def __init__(self, wb, wt, tt, tb, h, t, name):
        super().__init__(name)
        self.wb = wb
        self.wt = wt
        self.tt = tt
        self.tb = tb
        self.h = h
        self.t = t
    
    @property
    def wb(self):
        return self._wb
    
    @wb.setter
    def wb(self, value):
        if value <= 0:
            raise ValueError(f"Bottom flange width should greater than 0")
        self._wb = value
    
    @property
    def wt(self):
        return self._wt
    
    @wt.setter
    def wt(self, value):
        if value <= 0:
            raise ValueError(f"Bottom flange thickness should greater than 0")
        self._wt = value

    @property
    def tt(self):
        return self._tt
    
    @tt.setter
    def tt(self, value):
        if value <= 0:
            raise ValueError(f"Top flange thickness should greater than 0")
        self._tt = value

    @property
    def tb(self):
        return self._tb
    
    @tb.setter
    def tb(self, value):
        if value <= 0:
            raise ValueError(f"Top flange width should greater than 0")
        self._tb = value

    @property
    def h(self):
        return self._h
    
    @h.setter
    def h(self, value):
        if value <= 0:
            raise ValueError(f"Inner web height should greater than 0")
        self._h = value

    @property
    def t(self):
        return self._t
    
    @t.setter
    def t(self, value):
        if value <= 0:
            raise ValueError(f"Thickness should greater than 0")
        self._t = value

    @property
    def area(self):
        return (self.wt * self.tt) + (self.wb * self.tb) + (self.h * self.t)
    
    @property
    def Ixx(self):

        A_t = self.wt * self.tt
        y_t = self.h - (self.tt / 2)

        A_b = self.wb * self.tb
        y_b = self.tb / 2

        h_w = self.h - self.tt - self.tb
        A_w = self.t * h_w
        y_w = self.tb + (h_w / 2)

        total_area = A_t + A_b + A_w
        y_bar = ((A_t * y_t) + (A_b * y_b) + (A_w * y_w)) / total_area

        Ixx_top = (1/12 * self.wt * self.tt**3) + (A_t * (y_t - y_bar)**2)
        Ixx_bottom = (1/12 * self.wb * self.tb**3) + (A_b * (y_b - y_bar)**2)
        Ixx_web = (1/12 * self.t * h_w**3) + (A_w * (y_w - y_bar)**2)

        return Ixx_top + Ixx_bottom + Ixx_web

    @property
    def Iyy(self):
        h_w = self.h - self.tt - self.tb
        Iyy_top = 1/12 * self.tt * self.wt**3
        Iyy_bottom = 1/12 * self.tb * self.wb**3
        Iyy_web = 1/12 * h_w * self.t**3

        return Iyy_top + Iyy_bottom + Iyy_web
    
    @property
    def Izz(self):
        return self.Ixx + self.Iyy



