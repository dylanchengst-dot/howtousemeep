"""
Run the full AOI MEEP simulation.

Runs two passes:
  Pass 1 — no defect  (reference image)
  Pass 2 — with defect (scratch in solder mask)

Saves field arrays to .npy files for aoi_analyze.py.
"""

import meep as mp
import numpy as np
import os
from aoi_geometry import (
    build_geometry, grin_eps,
    CELL_X, CELL_Y, PML_THICK,
    F0, FWIDTH,
    SOURCE_Y, SENSOR_Y, LENS_Y, OBJECT_Y,
)

RESOLUTION = 25
RUN_TIME   = 250
OUT_DIR    = "output"

os.makedirs(OUT_DIR, exist_ok=True)


def run_simulation(include_defect: bool) -> np.ndarray:
    label = "defect" if include_defect else "reference"
    print(f"\n=== Running {label} simulation ===")

    cell = mp.Vector3(CELL_X, CELL_Y, 0)

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
        geometry=build_geometry(include_defect=include_defect),
        sources=sources,
        resolution=RESOLUTION,
    )

    sensor_mon = sim.add_flux(
        F0, FWIDTH, 80,
        mp.FluxRegion(center=mp.Vector3(0, SENSOR_Y),
                      size=mp.Vector3(CELL_X * 0.85, 0))
    )

    sim.run(until=RUN_TIME)

    ez = sim.get_array(center=mp.Vector3(), size=cell, component=mp.Ez)
    intensity = np.abs(ez) ** 2

    np.save(os.path.join(OUT_DIR, f"intensity_{label}.npy"), intensity)
    np.save(os.path.join(OUT_DIR, f"freqs_{label}.npy"),
            np.array(mp.get_flux_freqs(sensor_mon)))
    np.save(os.path.join(OUT_DIR, f"flux_{label}.npy"),
            np.array(mp.get_fluxes(sensor_mon)))

    print(f"  Saved intensity_{label}.npy, flux_{label}.npy")
    return intensity


if __name__ == "__main__":
    ref   = run_simulation(include_defect=False)
    defct = run_simulation(include_defect=True)

    print("\nSimulation complete.")
    print(f"Field array shape : {ref.shape}")
    print(f"Output files in   : {OUT_DIR}/")
    print("Next step: python aoi_analyze.py")
