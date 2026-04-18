"""
Capture the intensity distribution at a camera sensor plane.

Combines source → object reflection → lens → sensor in a single 2-D simulation.

Layout (y-axis, units = µm):
  y = -3  : LED point source
  y =  0  : Object (FR4 slab, 0.5 µm thick)
  y =  4  : Thin GRIN lens
  y =  8  : Camera sensor plane (flux monitor)
"""

import meep as mp
import matplotlib.pyplot as plt
import numpy as np

RESOLUTION   = 25
CELL_X       = 20.0
CELL_Y       = 18.0
PML_THICK    = 1.5
F0           = 1 / 0.55
FWIDTH       = 0.3

SOURCE_Y     = -3.0
OBJECT_Y     =  0.0
OBJ_THICK    =  0.5
OBJ_EPS      =  4.1
LENS_Y       =  4.0
LENS_THICK   =  0.3
FOCAL_LEN    =  4.0
SENSOR_Y     =  8.0
APERTURE_R   =  7.0
N_LENS       =  1.5

cell = mp.Vector3(CELL_X, CELL_Y, 0)

def grin_eps(vec):
    x = vec.x
    if abs(x) > APERTURE_R:
        return 1.0
    n = N_LENS * (1 - x**2 / (2 * FOCAL_LEN * N_LENS))
    return max(n**2, 1.0)

geometry = [
    mp.Block(
        size=mp.Vector3(mp.inf, OBJ_THICK, mp.inf),
        center=mp.Vector3(0, OBJECT_Y),
        material=mp.Medium(epsilon=OBJ_EPS),
    ),
    mp.Block(
        size=mp.Vector3(CELL_X, LENS_THICK, mp.inf),
        center=mp.Vector3(0, LENS_Y),
        material=mp.Medium(epsilon_func=grin_eps),
    ),
]

sources = [
    mp.Source(
        mp.GaussianSource(frequency=F0, fwidth=FWIDTH),
        component=mp.Ez,
        center=mp.Vector3(0, SOURCE_Y),
    )
]

sim = mp.Simulation(
    cell_size=cell,
    boundary_layers=[mp.PML(PML_THICK)],
    geometry=geometry,
    sources=sources,
    resolution=RESOLUTION,
)

sensor_mon = sim.add_flux(
    F0, FWIDTH, 60,
    mp.FluxRegion(center=mp.Vector3(0, SENSOR_Y),
                  size=mp.Vector3(CELL_X * 0.8, 0))
)

sim.run(until=200)

ez       = sim.get_array(center=mp.Vector3(), size=cell, component=mp.Ez)
intensity = np.abs(ez)**2

# Sensor row extraction
ny       = intensity.shape[1]
sensor_j = int((SENSOR_Y + CELL_Y / 2) / CELL_Y * ny)
sensor_j = np.clip(sensor_j, 0, ny - 1)
sensor_profile = intensity[:, sensor_j]
x_vals   = np.linspace(-CELL_X / 2, CELL_X / 2, intensity.shape[0])

fig, axes = plt.subplots(1, 2, figsize=(14, 5))

im = axes[0].imshow(np.rot90(intensity), cmap="inferno", origin="lower",
                    extent=[-CELL_X/2, CELL_X/2, -CELL_Y/2, CELL_Y/2])
for y_line, label, color in [
    (SOURCE_Y, "Source",  "cyan"),
    (OBJECT_Y, "Object",  "lime"),
    (LENS_Y,   "Lens",    "yellow"),
    (SENSOR_Y, "Sensor",  "white"),
]:
    axes[0].axhline(y_line, color=color, linestyle="--", linewidth=0.8, label=label)
axes[0].legend(loc="upper right", fontsize=7)
axes[0].set_title("Full AOI Optical Path — |Ez|²")
axes[0].set_xlabel("x (µm)")
axes[0].set_ylabel("y (µm)")
plt.colorbar(im, ax=axes[0])

axes[1].plot(x_vals, sensor_profile, color="orange")
axes[1].set_title(f"Sensor Intensity Profile (y = {SENSOR_Y} µm)")
axes[1].set_xlabel("x (µm)  →  pixel position")
axes[1].set_ylabel("Intensity |Ez|²")
axes[1].fill_between(x_vals, sensor_profile, alpha=0.3, color="orange")

plt.tight_layout()
plt.savefig("sensor_image.png", dpi=150)
plt.show()
print("Saved: sensor_image.png")
