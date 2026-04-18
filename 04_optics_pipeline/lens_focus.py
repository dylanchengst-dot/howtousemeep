"""
Model a thin converging lens using a GRIN (gradient-index) slab and show
that a point source below the lens produces a focused spot above it.

Layout (y-axis, 2-D, units = µm):
  Source at y = -4  (below lens)
  Lens slab at y = 0  (thin GRIN layer)
  Focal plane at y = +4  (above lens)
"""

import meep as mp
import matplotlib.pyplot as plt
import numpy as np

RESOLUTION  = 30
CELL_X      = 20.0
CELL_Y      = 20.0
PML_THICK   = 1.5
F0          = 1 / 0.55
FWIDTH      = 0.2
FOCAL_LEN   = 4.0          # µm — focal length in model
LENS_Y      = 0.0
LENS_THICK  = 0.3
N_BACKGROUND = 1.5         # lens base index
SOURCE_Y    = -4.0
SENSOR_Y    = FOCAL_LEN    # place sensor at focal plane

cell = mp.Vector3(CELL_X, CELL_Y, 0)

# GRIN lens: vary epsilon along x so that the phase delay mimics a thin lens.
# n(x) = n0 * (1 - x²/(2*f*n0))  for |x| < R_aperture
aperture_r = 6.0   # half-width of lens aperture

def grin_eps(vec):
    x = vec.x
    if abs(x) > aperture_r:
        return 1.0   # outside aperture → air
    n = N_BACKGROUND * (1 - x**2 / (2 * FOCAL_LEN * N_BACKGROUND))
    return max(n**2, 1.0)

lens_material = mp.Medium(epsilon_func=grin_eps)

geometry = [
    mp.Block(
        size=mp.Vector3(CELL_X, LENS_THICK, mp.inf),
        center=mp.Vector3(0, LENS_Y),
        material=lens_material,
    )
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

# Sensor flux monitor at focal plane
sensor_mon = sim.add_flux(
    F0, FWIDTH, 40,
    mp.FluxRegion(center=mp.Vector3(0, SENSOR_Y),
                  size=mp.Vector3(CELL_X * 0.8, 0))
)

sim.run(until=150)

ez = sim.get_array(center=mp.Vector3(), size=cell, component=mp.Ez)
intensity = np.abs(ez)**2

fig, axes = plt.subplots(1, 2, figsize=(13, 5))

im = axes[0].imshow(np.rot90(intensity), cmap="hot", origin="lower",
                    extent=[-CELL_X/2, CELL_X/2, -CELL_Y/2, CELL_Y/2])
axes[0].axhline(LENS_Y,   color="cyan",  linestyle="--", label="Lens")
axes[0].axhline(SENSOR_Y, color="white", linestyle="--", label="Focal plane")
axes[0].set_title("|Ez|² — GRIN lens focusing")
axes[0].set_xlabel("x (µm)")
axes[0].set_ylabel("y (µm)")
axes[0].legend(loc="upper right")
plt.colorbar(im, ax=axes[0])

# Cross-section at focal plane
mid_row = int((SENSOR_Y + CELL_Y/2) / CELL_Y * intensity.shape[1])
x_vals  = np.linspace(-CELL_X/2, CELL_X/2, intensity.shape[0])
axes[1].plot(x_vals, intensity[:, mid_row])
axes[1].set_title("Intensity at focal plane (y = {:.0f} µm)".format(SENSOR_Y))
axes[1].set_xlabel("x (µm)")
axes[1].set_ylabel("|Ez|²")

plt.tight_layout()
plt.savefig("lens_focus.png", dpi=150)
plt.show()
print("Saved: lens_focus.png")
