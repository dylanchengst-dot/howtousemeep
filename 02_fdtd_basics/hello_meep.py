"""Minimal MEEP simulation — a point source radiating in free space."""

import meep as mp
import matplotlib.pyplot as plt
import numpy as np

RESOLUTION = 20       # grid points per µm
CELL_SIZE  = 10       # µm, square cell
FREQUENCY  = 2.0      # 1/λ, λ = 0.5 µm (green light)
PML_THICK  = 1.0      # µm
RUN_TIME   = 50       # MEEP time units

cell = mp.Vector3(CELL_SIZE, CELL_SIZE, 0)

sources = [
    mp.Source(
        mp.GaussianSource(frequency=FREQUENCY, fwidth=0.5),
        component=mp.Ez,
        center=mp.Vector3(0, 0),
    )
]

sim = mp.Simulation(
    cell_size=cell,
    boundary_layers=[mp.PML(PML_THICK)],
    sources=sources,
    resolution=RESOLUTION,
)

sim.run(until=RUN_TIME)

ez = sim.get_array(center=mp.Vector3(), size=cell, component=mp.Ez)

plt.figure(figsize=(6, 6))
plt.imshow(np.rot90(ez), cmap="RdBu", origin="lower",
           extent=[-CELL_SIZE/2, CELL_SIZE/2, -CELL_SIZE/2, CELL_SIZE/2])
plt.colorbar(label="Ez field amplitude")
plt.title("Hello MEEP — Point Source in Free Space")
plt.xlabel("x (µm)")
plt.ylabel("y (µm)")
plt.tight_layout()
plt.savefig("hello_meep_ez.png", dpi=150)
plt.show()
print("Saved: hello_meep_ez.png")
