"""
Model a broadband LED-like point source and measure its radiated flux spectrum.

Geometry (2-D, all units in µm):
  - 16×16 µm cell
  - PML borders (1 µm thick)
  - Point source at origin
  - Flux monitor ring around the source
"""

import meep as mp
import matplotlib.pyplot as plt
import numpy as np

RESOLUTION  = 30
CELL_SIZE   = 16.0
PML_THICK   = 1.0
F_CENTER    = 1 / 0.55      # ~1.818 (green 550 nm)
F_WIDTH     = 0.8           # broad bandwidth (LED-like)
N_FREQS     = 50            # frequency resolution for spectrum
RUN_TIME    = 200

cell = mp.Vector3(CELL_SIZE, CELL_SIZE, 0)

sources = [
    mp.Source(
        mp.GaussianSource(frequency=F_CENTER, fwidth=F_WIDTH),
        component=mp.Ez,
        center=mp.Vector3(0, 0),
    )
]

# Flux box — four surfaces forming a square around the source
flux_region_size = mp.Vector3(8, 8, 0)
flux_monitors = []
for direction, side in [(mp.X, +1), (mp.X, -1), (mp.Y, +1), (mp.Y, -1)]:
    weight = side  # outward normal sign
    center = mp.Vector3(side * 4 if direction == mp.X else 0,
                        side * 4 if direction == mp.Y else 0)
    flux_monitors.append(
        mp.FluxRegion(center=center,
                      size=mp.Vector3(0 if direction == mp.X else 8,
                                      0 if direction == mp.Y else 8),
                      weight=weight)
    )

sim = mp.Simulation(
    cell_size=cell,
    boundary_layers=[mp.PML(PML_THICK)],
    sources=sources,
    resolution=RESOLUTION,
)

total_flux = sim.add_flux(F_CENTER, F_WIDTH, N_FREQS, *flux_monitors)

sim.run(until=RUN_TIME)

# --- Field snapshot ---
ez = sim.get_array(center=mp.Vector3(), size=cell, component=mp.Ez)

fig, axes = plt.subplots(1, 2, figsize=(12, 5))

axes[0].imshow(np.rot90(ez), cmap="RdBu", origin="lower",
               extent=[-CELL_SIZE/2, CELL_SIZE/2, -CELL_SIZE/2, CELL_SIZE/2])
axes[0].set_title("Ez field snapshot")
axes[0].set_xlabel("x (µm)")
axes[0].set_ylabel("y (µm)")

freqs   = mp.get_flux_freqs(total_flux)
flux_v  = mp.get_fluxes(total_flux)
wavelen = [1/f for f in freqs]

axes[1].plot(wavelen, flux_v)
axes[1].set_title("Radiated flux spectrum")
axes[1].set_xlabel("Wavelength (µm)")
axes[1].set_ylabel("Flux (a.u.)")
axes[1].axvline(0.55, color="green", linestyle="--", label="550 nm peak")
axes[1].legend()

plt.tight_layout()
plt.savefig("source_result.png", dpi=150)
plt.show()
print("Saved: source_result.png")
