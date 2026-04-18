# MEEP on Windows — AOI System Tutorial

A step-by-step guide to installing MEEP on Windows and building an FDTD-based
optical simulation for an **Automated Optical Inspection (AOI)** system.

## Project Goal

Simulate the full optical path of an AOI system:

```
Light Source → Object (PCB/Component) → Reflected Light → Lens → Camera Sensor
```

Then integrate the optical model with a mechanical system design to form a
complete AOI platform.

## Tutorial Sections

| # | Folder | Topic |
|---|--------|-------|
| 1 | `01_windows_setup/` | Installing MEEP on Windows (WSL2 + Conda) |
| 2 | `02_fdtd_basics/` | FDTD concepts and first MEEP simulation |
| 3 | `03_light_source/` | Modeling a light source (LED / laser) |
| 4 | `04_optics_pipeline/` | Reflection, lens, and camera sensor |
| 5 | `05_aoi_system/` | Full AOI system integration |

## Prerequisites

- Windows 10 version 2004+ or Windows 11
- Basic Python knowledge
- Familiarity with optics concepts (optional but helpful)

## Quick Start

```bash
# After completing Section 1 (WSL2 + Conda setup):
conda activate meep-env
cd 03_light_source
python point_source.py
```

## Repository Layout

```
howtousemeep/
├── README.md
├── 01_windows_setup/
│   ├── README.md          ← Installation guide
│   └── verify_install.py  ← Verify your MEEP installation
├── 02_fdtd_basics/
│   ├── README.md          ← FDTD theory overview
│   └── hello_meep.py      ← Minimal first simulation
├── 03_light_source/
│   ├── README.md          ← Light source modeling guide
│   └── point_source.py    ← LED/point-source simulation
├── 04_optics_pipeline/
│   ├── README.md          ← Lens + sensor pipeline guide
│   ├── reflection_demo.py ← Object surface reflection
│   ├── lens_focus.py      ← Thin-lens focusing
│   └── sensor_capture.py  ← Camera sensor flux capture
└── 05_aoi_system/
    ├── README.md          ← Full AOI system design
    └── scripts/
        ├── aoi_geometry.py   ← Build full geometry
        ├── aoi_simulate.py   ← Run full simulation
        └── aoi_analyze.py    ← Post-process sensor data
```
