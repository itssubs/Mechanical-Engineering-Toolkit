class Beam:
    def __init__(self, name, material, profile, length):
        self.name = name
        self.length = length #m
        self.material = material
        self.profile = profile
        self.loads = []
    
    @property
    def length(self):
        return self._length
    
    @length.setter
    def length(self, value):
        if value <= 0:
            raise ValueError(f'Length should be greater than 0')
        self._length = value

    def add_load(self, position, force_kN):
        if 0 < position < self.length:
            self.loads.append((position, force_kN * 1000))
            # CRITICAL FIX: Macaulay's method requires loads sorted by position
            self.loads.sort(key=lambda x: x[0])
        else:
            raise ValueError(f"Position {position} outside beam length")

    @property 
    def reactions(self):
        """Calculates and returns support reactions R_A and R_B."""
        R_A = 0
        R_B = 0
        for pos, force in self.loads:
            R_A += (force * (self.length - pos)) / self.length
            R_B += (force * pos) / self.length
        return R_A, R_B

    @property
    def max_bending_moment(self):
        """Calculates the absolute maximum bending moment along the beam."""
        R_A, _ = self.reactions
        
        moments = []
        previous_pos = 0
        current_moment = 0
        current_shear = R_A
        
        for position, magnitude in self.loads:
            distance = position - previous_pos
            current_moment += current_shear * distance
            moments.append(current_moment)
            current_shear -= magnitude
            previous_pos = position
            
        return max(moments) # Final maximum moment in Nm
    
    def calculate_deflection(self, x):
        """Calculates vertical deflection at position x using Macaulay's method."""
        R_A, _ = self.reactions
        # GPa * mm4 * 10^-3 converts cleanly to N*m2
        E_Pa = self.material.E_GPa * (10 **9)
        I_m4 = self.profile.Ixx
        EI = E_Pa * I_m4
        
        def macaulay(x, a, n):
            return (x - a)**n if x > a else 0

        # 1. Deflection terms
        deflection_terms = (R_A * (x**3)) / 6
        for a, P in self.loads:
            deflection_terms -= (P * macaulay(x, a, 3)) / 6
            
        # 2. Integration constant C1
        C1_terms = (R_A * (self.length**3)) / 6
        for a, P in self.loads:
            C1_terms -= (P * macaulay(self.length, a, 3)) / 6
        C1 = -C1_terms / self.length
        
        # 3. Final deflection v(x)
        v_x = (1 / EI) * (deflection_terms + C1 * x)
        return v_x

    def max_deflection(self,resolution=0.0001):
        import numpy as np

        num_points = int(self.length / resolution) + 1
        x_values = np.linspace(0, self.length, num_points)
        deflections = [self.calculate_deflection(x) for x in x_values]

        max_downward_deflection = min(deflections)
        max_index = deflections.index(max_downward_deflection)
        position_of_max = x_values[max_index]
        
        return abs(max_downward_deflection) * 1000, position_of_max
    
    def plot_diagrams(self, resolution=0.01):
        """Plots the Shear Force, Bending Moment, and Deflection diagrams."""
        import numpy as np
        import matplotlib.pyplot as plt

        # 1. Generate arrays of points along the length of the beam
        num_points = int(self.length / resolution) + 1
        x_values = np.linspace(0, self.length, num_points)
        
        shears = []
        moments = []
        deflections = []
        
        R_A, _ = self.reactions

        # 2. Calculate values at every point x along the beam
        for x in x_values:
            # --- Shear Calculation ---
            # Start with R_A, subtract any load that has been passed by point 'x'
            current_shear = R_A
            for a, P in self.loads:
                if x >= a:
                    current_shear -= P
            shears.append(current_shear / 1000) # Convert N to kN for cleaner plotting
            
            # --- Bending Moment Calculation ---
            current_moment = R_A * x
            for a, P in self.loads:
                if x > a:
                    current_moment -= P * (x - a)
            moments.append(current_moment / 1000) # Convert Nm to kNm

            # --- Deflection Calculation ---
            # Multiply by 1000 to plot in millimeters (mm)
            defl = self.calculate_deflection(x) * 1000
            deflections.append(defl)

        # 3. Create a multi-plot layout (3 rows, 1 column)
        fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(8, 8), sharex=True)
        fig.suptitle(f"Beam Analysis Diagrams ({self.material.name})", fontsize=16, fontweight='bold')

        # Subplot 1: Shear Force Diagram
        ax1.plot(x_values, shears, color='crimson', lw=2)
        ax1.fill_between(x_values, shears, color='crimson', alpha=0.15)
        ax1.axhline(0, color='black', lw=1, ls='--')
        ax1.set_ylabel("Shear Force (kN)", fontweight='bold')
        ax1.set_title("Shear Force Diagram (SFD)")
        ax1.grid(True, linestyle=':', alpha=0.6)

        # Subplot 2: Bending Moment Diagram
        ax2.plot(x_values, moments, color='darkblue', lw=2)
        ax2.fill_between(x_values, moments, color='darkblue', alpha=0.15)
        ax2.axhline(0, color='black', lw=1, ls='--')
        ax2.set_ylabel("Bending Moment (kNm)", fontweight='bold')
        ax2.set_title("Bending Moment Diagram (BMD)")
        ax2.grid(True, linestyle=':', alpha=0.6)

        # Subplot 3: Deflection Profile
        # Inverted axis because structural engineers visually like downward deflection pointing down
        ax3.plot(x_values, deflections, color='forestgreen', lw=2)
        ax3.fill_between(x_values, deflections, color='forestgreen', alpha=0.15)
        ax3.axhline(0, color='black', lw=1, ls='--')
        ax3.set_xlabel("Beam Length (m)", fontweight='bold')
        ax3.set_ylabel("Deflection (mm)", fontweight='bold')
        ax3.set_title("Elastic Deflection Curve")
        ax3.grid(True, linestyle=':', alpha=0.6)

        # Polish and display
        plt.tight_layout()
        plt.show()
    
    def __str__(self):
        return f"Beam (Length: {self.length}m, Material: {self.material.name})"
    
