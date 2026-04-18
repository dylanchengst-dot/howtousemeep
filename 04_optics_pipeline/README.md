# Section 4 — Optics Pipeline: Reflection → Lens → Sensor

This section builds the full optical chain step by step.

```
[Light Source] → [Object Surface] → [Reflected beam] → [Lens] → [Camera Sensor]
```

---

## 4.1 Object Surface Reflection (`reflection_demo.py`)

The inspected object (PCB, component, or wafer) reflects light.
We model it as a **flat dielectric slab** with optional surface roughness.

| Object type | Material model |
|-------------|----------------|
| PCB substrate (FR4) | `epsilon = 4.1` |
| Copper trace | `epsilon = -inf` (metal, use Drude model) |
| Solder mask (green) | `epsilon = 3.5` |
| Silicon die | `epsilon = 11.7` |

Key output: the **reflection spectrum** and **angular distribution** of
scattered light reaching the lens aperture.

### Running

```bash
python reflection_demo.py
```

Outputs `reflection_spectrum.png`.

---

## 4.2 Thin-Lens Focusing (`lens_focus.py`)

MEEP does not have a built-in lens object. We model a lens using the
**gradient-index (GRIN)** approach: a slab whose refractive index varies
with transverse position to impose a quadratic phase shift.

```
n(r) = n0 * sqrt(1 - (r/f)^2)   ← paraxial approximation
```

Alternatively, for a simple tutorial demo we use a **phase-screen** implemented
as a thin slab with spatially varying epsilon.

Key parameters:

| Parameter | Symbol | Typical value |
|-----------|--------|---------------|
| Focal length | f | 50 mm → 50 µm in model |
| Numerical aperture | NA | 0.1 – 0.4 |
| Working distance | WD | f × (1 + 1/M) |
| Magnification | M | 0.1× – 5× |

### Running

```bash
python lens_focus.py
```

Outputs `lens_focus.png` showing field converging to a focal point.

---

## 4.3 Camera Sensor Capture (`sensor_capture.py`)

The camera sensor is modeled as a **flux monitor plane** placed at the
image plane of the lens.

We record:
- Total flux (optical power) incident on the sensor
- Spatial field distribution → simulated "image"
- Spectral response (if multi-frequency run)

### Running

```bash
python sensor_capture.py
```

Outputs `sensor_image.png` — a 1-D or 2-D intensity distribution at the
sensor plane.

---

## Coordinate System Used in All Scripts

```
y
^
|   [Sensor]       y = +6 µm
|   [Lens]         y = +4 µm
|   [Air gap]
|   [Object]       y =  0 µm
|   [Source]       y = -3 µm
+-----> x
```

All scripts share this coordinate convention so they can be combined in
Section 5.

---

## Parameter Cheat Sheet

```python
# Shared constants (µm)
WAVELENGTH  = 0.55      # green light
F0          = 1 / WAVELENGTH
OBJECT_Y    = 0.0
LENS_Y      = 4.0
SENSOR_Y    = 6.0
SOURCE_Y    = -3.0
```

---

Next: [Section 5 — Full AOI System](../05_aoi_system/README.md)
