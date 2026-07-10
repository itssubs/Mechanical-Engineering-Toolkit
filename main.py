from material import Material
from database import Materialdatabase
from beam import Beam
from profile import Rectangular, Circular, I
from components import Shaft, PressureVessel, Gear

print("="*70)
print("DATABASE TEST")
print("="*70)

db = Materialdatabase("materials.csv")

steel = db.get("Steel")
al = db.get("Aluminium")
ti = db.get("Titanium")

print(steel)
print()
print(al)
print()
print(ti)

print("\nStrong materials (>200 MPa)\n")

for mat in db.filter_by_strength(200):
    print(mat.name)

print("\nBest Strength to Weight")

best = db.best_strength_to_weight()

print(best)

db.to_excel("materials.xlsx")

print("\nExcel file exported successfully.")

print("\n")
print("="*70)
print("RECTANGULAR PROFILE")
print("="*70)

rect = Rectangular(
    width=0.12,
    height=0.25,
    name="Rect 120x250"
)

print(f"Area : {rect.area:.3f} m2")
print(f"Ixx : {rect.Ixx} m4")
print(f"Iyy : {rect.Iyy} m4")
print(f"Izz : {rect.Izz} m4")

print("\n")
print("="*70)
print("CIRCULAR PROFILE")
print("="*70)

circle = Circular(
    radius=0.05,
    name="50 mm Radius"
)

print(f"Area : {circle.area:.3f} m2")
print(f"Ixx : {circle.Ixx} m4")
print(f"Iyy : {circle.Iyy} m4")
print(f"Izz : {circle.Izz} m4")

print("\n")
print("="*70)
print("I PROFILE")
print("="*70)

section = I(
    wb=0.20,
    wt=0.20,
    tb=0.02,
    tt=0.02,
    h=0.30,
    t=0.01,
    name="I200"
)

print(f"Area : {section.area:.3f} m2")
print(f"Ixx : {section.Ixx} m4")
print(f"Iyy : {section.Iyy} m4")
print(f"Izz : {section.Izz} m4")

print("\n")
print("="*70)
print("SHAFT")
print("="*70)

shaft = Shaft(
    name="Drive Shaft",
    material=steel,
    mass=18,
    diameter=0.05,
    torque_Nm=650
)

shaft.report()

print("\n")
print("="*70)
print("PRESSURE VESSEL")
print("="*70)

vessel = PressureVessel(
    name="Tank",
    material=steel,
    mass=80,
    radius=400,
    thickness=12,
    pressure=3
)

vessel.report()

print("\n")
print("="*70)
print("GEAR")
print("="*70)

gear = Gear(
    name="Pinion",
    material=steel,
    mass=4,
    pitch_diameter=120,
    face_width=20,
    tangential_load=2500,
    overload_factor=1.25,
    dynamic_factor=1.15,
    size_factor=1,
    geometry_factor=0.13
)

gear.report()


print("\n")
print("="*70)
print("BEAM")
print("="*70)

beam = Beam(
    name="Beam 1",
    material=steel,
    profile=rect,
    length=5
)

beam.add_load(1,20)
beam.add_load(2.5,15)
beam.add_load(4,10)

RA, RB = beam.reactions

print(f"Reaction A = {RA:.2f} N")
print(f"Reaction B = {RB:.2f} N")

print(f"Maximum Moment = {beam.max_bending_moment:.2f} Nm")

max_def, pos = beam.max_deflection()

print(f"Maximum Deflection = {max_def:.4f} mm")
print(f"Occurs at {pos:.3f} m")
beam.plot_diagrams()

