"""
Post-process the simulated sensor data from aoi_simulate.py.

Outputs:
  - Side-by-side sensor images (reference vs defect)
  - Difference map highlighting the defect
  - SNR and contrast metrics
"""

import numpy as np
import matplotlib.pyplot as plt
import os
import sys

OUT_DIR  = "output"
CELL_X   = 24.0
CELL_Y   = 20.0
SENSOR_Y =  8.0


def load(name):
    path = os.path.join(OUT_DIR, name)
    if not os.path.exists(path):
        print(f"ERROR: {path} not found. Run aoi_simulate.py first.")
        sys.exit(1)
    return np.load(path)


def extract_sensor_row(intensity: np.ndarray, sensor_y: float) -> np.ndarray:
    ny     = intensity.shape[1]
    row_j  = int((sensor_y + CELL_Y / 2) / CELL_Y * ny)
    row_j  = np.clip(row_j, 0, ny - 1)
    return intensity[:, row_j]


ref   = load("intensity_reference.npy")
defct = load("intensity_defect.npy")

ref_row   = extract_sensor_row(ref,   SENSOR_Y)
defct_row = extract_sensor_row(defct, SENSOR_Y)
diff_row  = defct_row - ref_row
x_vals    = np.linspace(-CELL_X / 2, CELL_X / 2, len(ref_row))

# ── SNR metric ──────────────────────────────────────────────────────────────
background = np.mean(ref_row)
signal     = np.max(np.abs(diff_row))
noise      = np.std(ref_row[ref_row < np.percentile(ref_row, 25)])
snr        = signal / (noise + 1e-12)
contrast   = signal / (background + 1e-12)
print(f"Background level : {background:.4f}")
print(f"Defect signal    : {signal:.4f}")
print(f"Noise floor      : {noise:.6f}")
print(f"SNR              : {snr:.1f}  ({20*np.log10(snr+1e-12):.1f} dB)")
print(f"Contrast         : {contrast:.3f}")

# ── Plot ─────────────────────────────────────────────────────────────────────
fig, axes = plt.subplots(2, 2, figsize=(14, 10))

extent = [-CELL_X/2, CELL_X/2, -CELL_Y/2, CELL_Y/2]

axes[0, 0].imshow(np.rot90(ref), cmap="inferno", origin="lower", extent=extent)
axes[0, 0].set_title("Reference — no defect")
axes[0, 0].set_xlabel("x (µm)")
axes[0, 0].set_ylabel("y (µm)")

axes[0, 1].imshow(np.rot90(defct), cmap="inferno", origin="lower", extent=extent)
axes[0, 1].set_title("With defect (scratch)")
axes[0, 1].set_xlabel("x (µm)")

diff_img = defct - ref
vmax = np.percentile(np.abs(diff_img), 99)
axes[1, 0].imshow(np.rot90(diff_img), cmap="bwr", origin="lower",
                  extent=extent, vmin=-vmax, vmax=vmax)
axes[1, 0].set_title("Difference map (defect − reference)")
axes[1, 0].set_xlabel("x (µm)")
axes[1, 0].set_ylabel("y (µm)")

axes[1, 1].plot(x_vals, ref_row,   label="Reference",   color="blue")
axes[1, 1].plot(x_vals, defct_row, label="With defect",  color="red")
axes[1, 1].plot(x_vals, diff_row,  label="Difference",   color="green",
                linestyle="--")
axes[1, 1].set_title(f"Sensor profile  |  SNR = {snr:.1f}")
axes[1, 1].set_xlabel("x (µm)  →  pixel position")
axes[1, 1].set_ylabel("Intensity |Ez|²")
axes[1, 1].legend()

plt.tight_layout()
plt.savefig("aoi_analysis.png", dpi=150)
plt.show()
print("Saved: aoi_analysis.png")
