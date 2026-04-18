"""
Define and visualise the full AOI system geometry.

All units in µm.  Call build_geometry() from aoi_simulate.py.

Layout (y-axis):
  y = -3  : LED source
  y =  0  : PCB object (FR4 + copper trace + solder mask)
  y =  4  : GRIN lens
  y =  8  : Camera sensor plane
"""

import meep as mp
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

# ── Shared constants ────────────────────────────────────────────────────────
CELL_X      = 24.0
CELL_Y      = 20.0
PML_THICK   = 1.5
F0          = 1 / 0.55
FWIDTH      = 0.3

SOURCE_Y    = -3.0
OBJECT_Y    =  0.0
FR4_THICK   =  0.5
TRACE_W     =  1.0    # copper trace width
TRACE_EPS   = -1e6    # approximate perfect electric conductor
FR4_EPS     =  4.1
SMASK_EPS   =  3.5
SMASK_THICK =  0.1
LENS_Y      =  4.0
LENS_THICK  =  0.3
FOCAL_LEN   =  4.0
APERTURE_R  =  9.0
N_LENS      =  1.5
SENSOR_Y    =  8.0


def grin_eps(vec):
    x = vec.x
    if abs(x) > APERTURE_R:
        return 1.0
    n = N_LENS * (1 - x**2 / (2 * FOCAL_LEN * N_LENS))
    return max(n**2, 1.0)


def build_geometry(include_defect=False):
    """Return list of MEEP geometry objects for the AOI scene."""
    geom = []

    # FR4 substrate
    geom.append(mp.Block(
        size=mp.Vector3(mp.inf, FR4_THICK, mp.inf),
        center=mp.Vector3(0, OBJECT_Y),
        material=mp.Medium(epsilon=FR4_EPS),
    ))

    # Copper trace (centred on PCB surface)
    geom.append(mp.Block(
        size=mp.Vector3(TRACE_W, FR4_THICK, mp.inf),
        center=mp.Vector3(0, OBJECT_Y),
        material=mp.metal,
    ))

    # Solder mask over the FR4 (not over the exposed pad)
    for x_center in [-4.0, 4.0]:
        geom.append(mp.Block(
            size=mp.Vector3(5.0, SMASK_THICK, mp.inf),
            center=mp.Vector3(x_center, OBJECT_Y + FR4_THICK/2 + SMASK_THICK/2),
            material=mp.Medium(epsilon=SMASK_EPS),
        ))

    # Simulated defect: a scratch (narrow groove) in the solder mask
    if include_defect:
        geom.append(mp.Block(
            size=mp.Vector3(0.2, SMASK_THICK * 2, mp.inf),
            center=mp.Vector3(-4.0, OBJECT_Y + FR4_THICK/2),
            material=mp.Medium(epsilon=1.0),   # air gap = scratch
        ))

    # GRIN lens
    geom.append(mp.Block(
        size=mp.Vector3(CELL_X, LENS_THICK, mp.inf),
        center=mp.Vector3(0, LENS_Y),
        material=mp.Medium(epsilon_func=grin_eps),
    ))

    return geom


def visualise_geometry():
    """Draw a schematic cross-section of the AOI layout."""
    fig, ax = plt.subplots(figsize=(8, 10))
    ax.set_xlim(-CELL_X/2, CELL_X/2)
    ax.set_ylim(-CELL_Y/2, CELL_Y/2)
    ax.set_facecolor("#0a0a0a")
    ax.set_xlabel("x (µm)")
    ax.set_ylabel("y (µm)")
    ax.set_title("AOI System — Cross-section (not to scale)", color="white")
    fig.patch.set_facecolor("#0a0a0a")
    ax.tick_params(colors="white")
    for spine in ax.spines.values():
        spine.set_edgecolor("white")

    def rect(x0, y0, w, h, color, label=None, alpha=0.8):
        patch = mpatches.FancyBboxPatch((x0, y0), w, h,
                                         boxstyle="square,pad=0",
                                         facecolor=color, edgecolor="white",
                                         linewidth=0.5, alpha=alpha, label=label)
        ax.add_patch(patch)

    # FR4
    rect(-CELL_X/2, OBJECT_Y - FR4_THICK/2, CELL_X, FR4_THICK,
         "#8B6914", label="FR4 substrate")
    # Copper trace
    rect(-TRACE_W/2, OBJECT_Y - FR4_THICK/2, TRACE_W, FR4_THICK,
         "#FFD700", label="Copper trace")
    # Solder mask
    for xc in [-4.0, 4.0]:
        rect(xc - 2.5, OBJECT_Y + FR4_THICK/2, 5.0, SMASK_THICK,
             "#2E7D32", label="Solder mask" if xc < 0 else None)
    # Lens
    rect(-APERTURE_R, LENS_Y - LENS_THICK/2, APERTURE_R*2, LENS_THICK,
         "#4FC3F7", alpha=0.5, label="GRIN Lens")
    # Source marker
    ax.plot(0, SOURCE_Y, "o", color="yellow", markersize=12, label="LED Source")
    ax.annotate("LED Source", (0, SOURCE_Y), (2, SOURCE_Y - 0.8),
                color="yellow", fontsize=8)
    # Sensor
    ax.axhline(SENSOR_Y, color="magenta", linewidth=2, label="Camera Sensor")
    ax.annotate("Camera Sensor", (-CELL_X/2 + 0.5, SENSOR_Y + 0.2), color="magenta")

    ax.legend(loc="upper right", fontsize=7, facecolor="#1a1a1a", labelcolor="white")
    plt.tight_layout()
    plt.savefig("aoi_geometry.png", dpi=150, facecolor=fig.get_facecolor())
    plt.show()
    print("Saved: aoi_geometry.png")


if __name__ == "__main__":
    visualise_geometry()
    print("Geometry objects:", len(build_geometry(include_defect=True)))
