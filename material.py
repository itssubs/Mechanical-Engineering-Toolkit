class Material:
    def __init__(self, name, yield_mpa, density, E_GPa, brinell, poissons):
        self.name = name
        self.yield_mpa = yield_mpa #MPa
        self.density = density #kg/m3
        self.E_GPa = E_GPa #GPa
        self.brinell = brinell #HB
        self.poissons = poissons 

    @property
    def yield_mpa(self):
        return self._yield_mpa
    
    @yield_mpa.setter
    def yield_mpa(self, value):
        if value <= 0:
            raise ValueError("Yield Strength should be greater than 0")
        self._yield_mpa = value

    @property
    def density(self):
        return self._density
    
    @density.setter
    def density(self, value):
        if value <= 0:
            raise ValueError("Density should be greater than 0")
        self._density = value

    @property
    def E_GPa(self):
        return self._E_GPa
    
    @E_GPa.setter
    def E_GPa(self, value):
        if value <= 0:
            raise ValueError("Young's Modulus should be greater than 0")
        self._E_GPa = value

    @property
    def brinell(self):
        return self._brinell
    
    @brinell.setter
    def brinell(self, value):
        if value <= 0:
            raise ValueError("Brinell should be greater than 0")
        self._brinell = value
    
    @property
    def poissons(self):
        return self._poissons
    
    @poissons.setter
    def poissons(self, value):
        if value <= 0:
            raise ValueError("Poissons ratio should be greater than 0")
        self._poissons = value

    def __str__(self):
        return (f"Material = {self.name} \nYield Strength = {self.yield_mpa} MPa \nDensity = {self.density} kg/m3 \nYoung's modulus = {self.E_GPa} GPa \nBrinell Hardness number = {self.brinell} HB \nPoissons Ratio = {self.poissons}")