# Section 2 — FDTD Basics with MEEP

## What is FDTD?

**Finite-Difference Time-Domain (FDTD)** is a numerical method that solves
Maxwell's equations by discretizing space and time into a grid.

```
Maxwell's equations → discrete grid (Yee cell) → time-step loop → field data
```

Key concepts you will encounter in every MEEP simulation:

| Concept | What it means |
|---------|---------------|
| **Resolution** | Grid points per unit length (higher = more accurate, slower) |
| **Cell** | The simulation volume |
| **PML** | Perfectly Matched Layer — absorbing boundary that prevents reflections |
| **Source** | Where electromagnetic energy enters the simulation |
| **Monitor** | A surface or point where field data is recorded |
| **Time step** | MEEP chooses this automatically from the Courant condition |

---

## MEEP's Unit System

MEEP uses **dimensionless units** where the speed of light `c = 1`.

| Physical quantity | MEEP unit |
|-------------------|-----------|
| Length | You define 1 unit (e.g. 1 µm) |
| Frequency | `c / length_unit` |
| Time | `length_unit / c` |

For visible light (wavelength ~0.5 µm), set 1 MEEP unit = 1 µm.
Then a 500 nm wavelength → frequency = `1 / 0.5 = 2.0`.

---

## Anatomy of a MEEP Script

```python
import meep as mp

# 1. Define the simulation cell
cell = mp.Vector3(10, 10, 0)   # 2-D: 10×10 µm

# 2. Add materials / geometry
geometry = [
    mp.Block(size=mp.Vector3(mp.inf, 1, mp.inf),
             center=mp.Vector3(0, -2),
             material=mp.Medium(epsilon=2.25))  # glass-like slab
]

# 3. Add sources
sources = [
    mp.Source(mp.GaussianSource(frequency=2.0, fwidth=0.5),
              component=mp.Ez,
              center=mp.Vector3(0, 0))
]

# 4. Absorbing boundaries
pml_layers = [mp.PML(1.0)]

# 5. Build simulation object
sim = mp.Simulation(cell_size=cell,
                    boundary_layers=pml_layers,
                    geometry=geometry,
                    sources=sources,
                    resolution=20)

# 6. Run
sim.run(until=50)
```

---

## Running the Hello-World Simulation

```bash
conda activate meep-env
cd 02_fdtd_basics
python hello_meep.py
```

You should see a matplotlib window showing the Ez field spreading outward from
a point source.

---

## Visualising Results

MEEP can output field data in two ways:

```python
# Option A — direct numpy array (preferred for scripting)
ez_data = sim.get_array(center=mp.Vector3(), size=cell, component=mp.Ez)

# Option B — HDF5 file (useful for large 3-D runs)
sim.run(mp.at_end(mp.output_efield_z), until=50)
```

---

Next: [Section 3 — Modeling a Light Source](../03_light_source/README.md)
