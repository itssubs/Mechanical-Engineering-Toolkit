class MechanicalComponent:
    def __init__(self, name, material, mass):
        self.name = name
        self.material = material #Material object
        self.mass = mass #kg
    
    @property
    def mass(self):
        return self._mass
    @mass.setter
    def mass(self, value):
        if value <= 0:
            raise ValueError(f"Mass cannot be negative or 0")
        self._mass = value
        
    def __repr__(self):
        return f"{self.__class__.__name__}({self.name})"
    
    def safety_check(self):
        raise NotImplementedError("Subclasses must implement safety_check")
    
    def report(self):
        print(f"Component: {self.name}")
        print(f"Material:  {self.material.name}")
        print(f"Mass:      {self.mass} kg")
        self.safety_check()   # calls the subclass version

class Shaft(MechanicalComponent):
    def __init__(self, name, material, mass, diameter, torque_Nm):
        super().__init__(name, material, mass)
        self.diameter = diameter #m
        self.torque = torque_Nm #Nm

    @property
    def diameter(self):
        return self._diameter
    @diameter.setter
    def diameter(self, value):
        if value <=0:
            raise ValueError(f"Diameter can't be negative or 0")
        self._diameter = value

    @property
    def torque(self):
        return self._torque
    @torque.setter
    def torque(self, value):
        if value <=0:
            raise ValueError(f"Torque can't be negative or 0")
        self._torque = value

    def shear_stress(self):
        import numpy as np
        J = np.pi * (self.diameter ** 4) / 32
        r = self.diameter / 2
        tau = self.torque * r / J
        return tau
    
    def safety_check(self):
        tau = self.shear_stress()
        allowable = self.material.yield_mpa * 1e6 * 0.577  # von Mises
        print(f"Shear stress: {tau/1e6:.2f} MPa")
        print(f"Status: {'SAFE' if tau < allowable else 'FAIL'}")

class PressureVessel(MechanicalComponent):
    def __init__(self, name, material, mass, radius, thickness, pressure):
        super().__init__(name, material, mass)
        self.radius = radius #mm
        self.thickness = thickness #mm
        self.pressure = pressure #Mpa
    
    @property
    def radius(self):
        return self._radius
    @radius.setter
    def radius(self, value):
        if value <=0:
            raise ValueError(f"Radius can't be negative or 0")
        self._radius = value

    @property
    def thickness(self):
        return self._thickness
    @thickness.setter
    def thickness(self, value):
        if value <=0:
            raise ValueError(f"Thickness can't be negative or 0")
        self._thickness = value

    @property
    def pressure(self):
        return self._pressure
    @pressure.setter
    def pressure(self, value):
        if value <=0:
            raise ValueError(f"Pressure can't be negative or 0")
        self._pressure = value

    def hoop_stress(self):
        stress = self.pressure * self.radius / self.thickness
        return stress
    
    def safety_check(self):
        stress = self.hoop_stress()
        allowable = self.material.yield_mpa
        print(f"Hoop stress: {stress:.2f} MPa")
        if 1.5 * stress <= allowable:
            print("Status: SAFE")
        else:
            print("Status: Fail")

class Gear(MechanicalComponent):
    def __init__(self, name, material, mass, pitch_diameter, face_width, tangential_load, overload_factor, dynamic_factor, size_factor, geometry_factor):
        super().__init__(name, material, mass)
        self.pitch_diameter = pitch_diameter
        self.face_width = face_width
        self.tangential_load = tangential_load
        self.overload_factor = overload_factor
        self.dynamic_factor = dynamic_factor
        self.size_factor = size_factor
        self.geometry_factor = geometry_factor
    
    @property
    def pitch_diameter(self):
        return self._pitch_diameter
    @pitch_diameter.setter
    def pitch_diameter(self, value):
        if value <=0:
            raise ValueError(f"Pitch Diameter can't be negative or 0")
        self._pitch_diameter = value

    @property
    def face_width(self):
        return self._face_width
    @face_width.setter
    def face_width(self, value):
        if value <=0:
            raise ValueError(f"Face width can't be negative or 0")
        self._face_width = value
    
    @property
    def tangential_load(self):
        return self._tangential_load
    @tangential_load.setter
    def tangential_load(self, value):
        if value <=0:
            raise ValueError(f"Tangential Load can't be negative or 0")
        self._tangential_load = value

    @property
    def overload_factor(self):
        return self._overload_factor
    @overload_factor.setter
    def overload_factor(self, value):
        if value <=0:
            raise ValueError(f"Overload factor can't be negative or 0")
        self._overload_factor = value

    @property
    def dynamic_factor(self):
        return self._dynamic_factor
    @dynamic_factor.setter
    def dynamic_factor(self, value):
        if value <=0:
            raise ValueError(f"Dynamic factor can't be negative or 0")
        self._dynamic_factor = value

    @property
    def size_factor(self):
        return self._size_factor
    @size_factor.setter
    def size_factor(self, value):
        if value <=0:
            raise ValueError(f"Size factor can't be negative or 0")
        self._size_factor = value

    @property
    def geometry_factor(self):
        return self._geometry_factor
    @geometry_factor.setter
    def geometry_factor(self, value):
        if value <=0:
            raise ValueError(f"Geometry factor can't be negative or 0")
        self._geometry_factor = value

    def contact_stress(self):
        import numpy as np
        Cp = np.sqrt(self.material.E_GPa / (2 * np.pi * (1 - (self.material.poissons ** 2))))
        stress = Cp * np.sqrt((self.tangential_load * self.overload_factor * self.dynamic_factor * self.size_factor) / (self.pitch_diameter * self.face_width * self.geometry_factor))
        return stress
    
    def safety_check(self):
        endurance_limit = 3.45 * self.material.brinell #MPa
        #considering the factor for lubricant, pitchline velocity and surface roughness as 1
        stress = self.contact_stress()
        print(f"Contact Stress: {stress:.2f} MPa")
        print(f"Endurance Limit : {endurance_limit:.2f} MPa")
        if stress <= endurance_limit / 1.5:
            print("Status: Safe")
        else:
            print("Status : Fail")