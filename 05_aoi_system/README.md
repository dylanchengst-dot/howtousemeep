# Section 5 — Full AOI System Design

## What is an AOI System?

**Automated Optical Inspection (AOI)** uses cameras and structured light to
detect defects on PCBs, semiconductor wafers, or mechanical parts without
contact.

```
┌──────────────────────────────────────────────────────────┐
│                    AOI System Overview                    │
│                                                          │
│  ┌─────────┐    ┌──────────┐    ┌──────┐    ┌────────┐  │
│  │  Light  │───▶│  Object  │───▶│ Lens │───▶│Camera  │  │
│  │ Source  │    │ (PCB/Die)│    │System│    │Sensor  │  │
│  └─────────┘    └──────────┘    └──────┘    └────────┘  │
│       ▲               │                                   │
│  ┌────┴────┐    ┌─────▼──────┐                           │
│  │Illum.   │    │ Defect /   │                           │
│  │Control  │    │ Feature    │                           │
│  └─────────┘    └────────────┘                           │
│                                                          │
│  ┌───────────────────────────────────────────────────┐   │
│  │         Image Processing & Analysis               │   │
│  │   threshold → edge detect → pattern match →       │   │
│  │   defect classify → pass/fail report              │   │
│  └───────────────────────────────────────────────────┘   │
└──────────────────────────────────────────────────────────┘
```

---

## 5.1 Mechanical + Optical Architecture

### Illumination Modes

| Mode | Light position | Best for |
|------|----------------|----------|
| Coaxial (BF) | On-axis, beamsplitter | Flat surfaces, pads |
| Ring light (BF) | 45 ° ring above object | Component bodies |
| Dark field | Oblique, grazing angle | Surface scratches |
| Structured light | Fringe projector | 3-D height map |

### Optical Train Parameters

```
Object plane
    │   Working Distance (WD)
    ▼
  [Objective Lens]   NA, magnification M
    │   Tube length
    ▼
  [Tube Lens]
    │   Back focal distance
    ▼
  [Camera Sensor]   pixel pitch p, array N×M pixels
```

### Field of View

```
FOV = sensor_size / M
Depth of Field (DOF) ≈ λ / NA²
Lateral resolution ≈ 0.61 λ / NA   (Rayleigh criterion)
```

---

## 5.2 Simulation Strategy

### Step 1 — Optical sub-system (MEEP)

Run `scripts/aoi_simulate.py` to:
1. Illuminate the object with the chosen source type
2. Capture reflected field at the lens entrance pupil
3. Propagate through the lens model to the sensor plane
4. Record intensity map → synthetic sensor image

### Step 2 — Defect modelling

Add geometric perturbations to `aoi_geometry.py`:
- Missing solder: remove a small copper region
- Scratch: a thin low-reflectance groove
- Lifted component lead: a displaced metal block

### Step 3 — Analysis (`aoi_analyze.py`)

Post-process the simulated sensor images to:
- Compute SNR (signal-to-noise ratio) between defect and background
- Determine minimum detectable defect size for the chosen NA
- Plot contrast vs. defect depth / width

---

## 5.3 Running the Full Pipeline

```bash
conda activate meep-env
cd 05_aoi_system/scripts

# Build and check geometry
python aoi_geometry.py

# Run full MEEP simulation (may take several minutes)
python aoi_simulate.py

# Analyse the output data
python aoi_analyze.py
```

---

## 5.4 Scaling to 3-D

The 2-D scripts in this tutorial are sufficient for understanding the physics.
For production-grade simulation:

1. Upgrade to 3-D by setting `cell_size = mp.Vector3(X, Y, Z)`.
2. Use MPI parallelism: `mpirun -np 4 python aoi_simulate.py`
3. Use HDF5 output for large data volumes.
4. Consider RCWA (rigorous coupled-wave analysis) for periodic structures.

---

## 5.5 Next Steps Towards a Real AOI Machine

| Phase | Task |
|-------|------|
| Optical design | Validate NA, WD, FOV with Zemax or OpticsStudio |
| Mechanical design | Model motion stage, Z-focus, vibration isolation |
| Illumination | Measure LED uniformity, implement Köhler illumination |
| Camera | Select pixel pitch for Nyquist sampling of the PSF |
| Software | Build image acquisition, stitching, and defect classification pipeline |
| Calibration | Flat-field correction, distortion map, colour calibration |

---

## References

- MEEP documentation: https://meep.readthedocs.io
- Smith, W.J. — *Modern Optical Engineering*
- Goodman, J.W. — *Introduction to Fourier Optics*
- IPC-7711/7721 — AOI acceptance criteria standards
