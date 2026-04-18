"""
Simulate light hitting a flat dielectric object (PCB slab) and measure
the reflected vs. transmitted flux.

Layout (y-axis, 2-D, units = µm):
  Source at y = -4
  Object slab at y = 0  (thickness 0.5 µm, epsilon = 4.1 ≈ FR4)
  Reflection monitor at y = -2
  Transmission monitor at y = +2
"""

import meep as mp
import matplotlib.pyplot as plt
import numpy as np

RESOLUTION  = 40
CELL_X      = 12.0
CELL_Y      = 16.0
PML_THICK   = 1.0
F0          = 1 / 0.55     # 550 nm green
FWIDTH      = 0.5
N_FREQS     = 60

SOURCE_Y    = -5.0
OBJECT_Y    =  0.0
OBJ_THICK   =  0.5
OBJ_EPS     =  4.1          # FR4 (PCB substrate)
REFL_MON_Y  = -2.0
TRAN_MON_Y  =  2.0

cell = mp.Vector3(CELL_X, CELL_Y, 0)

geometry = [
    mp.Block(
        size=mp.Vector3(mp.inf, OBJ_THICK, mp.inf),
        center=mp.Vector3(0, OBJECT_Y),
        material=mp.Medium(epsilon=OBJ_EPS),
    )
]

sources = [
    mp.Source(
        mp.GaussianSource(frequency=F0, fwidth=FWIDTH),
        component=mp.Ez,
        center=mp.Vector3(0, SOURCE_Y),
        size=mp.Vector3(CELL_X, 0),   # plane wave
    )
]

sim = mp.Simulation(
    cell_size=cell,
    boundary_layers=[mp.PML(PML_THICK)],
    geometry=geometry,
    sources=sources,
    resolution=RESOLUTION,
)

refl_flux_region = mp.FluxRegion(center=mp.Vector3(0, REFL_MON_Y),
                                  size=mp.Vector3(CELL_X, 0), weight=-1)
tran_flux_region = mp.FluxRegion(center=mp.Vector3(0, TRAN_MON_Y),
                                  size=mp.Vector3(CELL_X, 0))

refl_mon = sim.add_flux(F0, FWIDTH, N_FREQS, refl_flux_region)
tran_mon = sim.add_flux(F0, FWIDTH, N_FREQS, tran_flux_region)

# Run without object first to get incident flux
sim.run(until=200)
incident_refl = mp.get_fluxes(refl_mon)
sim.save_flux("incident", refl_mon)

# Reset and run with object
sim.reset_meep()
sim = mp.Simulation(
    cell_size=cell,
    boundary_layers=[mp.PML(PML_THICK)],
    geometry=geometry,
    sources=sources,
    resolution=RESOLUTION,
)
refl_mon2 = sim.add_flux(F0, FWIDTH, N_FREQS, refl_flux_region)
tran_mon2 = sim.add_flux(F0, FWIDTH, N_FREQS, tran_flux_region)
sim.load_minus_flux("incident", refl_mon2)
sim.run(until=200)

freqs       = mp.get_flux_freqs(refl_mon2)
refl_flux   = mp.get_fluxes(refl_mon2)
tran_flux   = mp.get_fluxes(tran_mon2)
wavelen     = [1/f for f in freqs]
reflectance = [-r / t for r, t in zip(refl_flux, tran_flux)]

plt.figure(figsize=(7, 4))
plt.plot(wavelen, reflectance, label="Reflectance")
plt.xlabel("Wavelength (µm)")
plt.ylabel("Reflectance")
plt.title(f"FR4 Slab Reflectance (ε = {OBJ_EPS})")
plt.axvline(0.55, color="green", linestyle="--", label="550 nm")
plt.legend()
plt.tight_layout()
plt.savefig("reflection_spectrum.png", dpi=150)
plt.show()
print("Saved: reflection_spectrum.png")
