# Mechanical-Engineering-Toolkit

So this marks the weekly project for this week, week-5 and it is a mechanical engineering Toolkit.
# Mechanical Engineering Toolkit (MET)

> A Python-based Mechanical Engineering analysis toolkit built using Object-Oriented Programming.

## Overview

Mechanical Engineering Toolkit (MET) is an open-source Python project aimed at providing reusable engineering analysis tools for students, hobbyists, and engineers.

The project is being developed from scratch as both a learning journey in python and a practical engineering design package.

Current development focuses on building a solid object-oriented architecture that can later support advanced engineering calculations, visualization, and a graphical user interface.

## Current Features (v0.1.0)

### Materials

* Material class with engineering properties
* Material database
* CSV import/export support
* Material search and filtering

### Cross Sections

* Rectangular sections
* Circular sections
* I-sections
* Automatic calculation of:

  * Cross-sectional Area
  * Second Moment of Area (Ixx, Iyy)
  * Polar Moment of Inertia

### Beam Analysis

* Simply supported beams
* Multiple point loads
* Support reactions
* Shear Force Diagram (SFD)
* Bending Moment Diagram (BMD)
* Deflection calculation
* Deflection plotting

### Machine Components

* Shaft analysis
* Pressure vessel analysis
* Gear analysis
* Safety factor calculations

### Software Features

* Object-Oriented Design
* Encapsulation
* Inheritance
* Polymorphism
* Data validation using properties
* Matplotlib visualization

## Project Structure

```text
project/
│
├── main.py
├── material.py
├── database.py
├── profile.py
├── beam.py
├── components.py
└── materials.csv
```

---

Install dependencies

```bash
pip install numpy matplotlib pandas scipy
```

Run

```bash
python main.py
```

## Roadmap

### Version 0.2

* Distributed loads
* Beam stress analysis
* Additional support conditions
* Improved reports
* More engineering components

### Version 0.5

* Expanded machine design modules
* Advanced material selection
* Optimization tools
* Improved plotting

### Version 1.0

* Graphical User Interface (GUI)
* Project saving/loading
* Report generation
* Professional engineering workflow
* Stable public release

## Purpose

This project is being developed as a long-term engineering software project to combine mechanical engineering principles with modern Python programming practices.

The goal is to create a modular, extensible toolkit that can grow into a complete engineering design and analysis package.
## Contributing

Suggestions, improvements, and pull requests are always welcome.


This project is released under the MIT License.
