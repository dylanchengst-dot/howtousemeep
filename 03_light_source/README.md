# Section 3 — Modeling a Light Source

In an AOI system the light source is typically one of:

| Type | Characteristics | MEEP model |
|------|-----------------|------------|
| LED array | Broad spectrum, Lambertian emission | Gaussian pulse, large `fwidth` |
| Ring light | Uniform illumination at oblique angle | Multiple angled sources |
| Coaxial laser | Narrow beam, coherent | CW source or narrow Gaussian |
| Line scan laser | Linear beam, scanning | Line source or planar EigenMode |

This section uses a **point source** (2-D) as a simplified LED model, then
promotes it to a **line source** representing a ring-light segment.

---

## Key Parameters

```python
# Visible light range (1 MEEP unit = 1 µm)
WAVELENGTH_MIN = 0.40   # µm (violet)
WAVELENGTH_MAX = 0.70   # µm (red)
FREQUENCY_CEN  = 1 / 0.55          # centre frequency
FREQUENCY_WIDTH = (1/WAVELENGTH_MIN - 1/WAVELENGTH_MAX)  # bandwidth
```

---

## Source Types in MEEP

```python
# Narrowband (laser-like)
mp.GaussianSource(frequency=f0, fwidth=0.1*f0)

# Broadband (LED-like)
mp.GaussianSource(frequency=f0, fwidth=0.5*f0)

# Continuous wave (CW, steady state)
mp.ContinuousSource(frequency=f0)
```

---

## Running the Demo

```bash
conda activate meep-env
cd 03_light_source
python point_source.py
```

The script outputs:
- `source_field.png` — snapshot of Ez field at t=30
- `source_flux.png`  — radiated power spectrum

---

## What to Observe

1. The field spreads outward from the source as circular wavefronts.
2. The PML layer absorbs the field at the boundaries (no reflections).
3. The flux spectrum peaks at the centre frequency and tapers off at the edges.

---

## Design Notes for AOI

- For a **coaxial AOI** system, place the source on-axis (centre of the lens).
- For a **dark-field AOI** system, place sources at oblique angles to suppress
  specular reflection and highlight surface defects.
- The source `fwidth` controls coherence length — wider bandwidth = shorter
  coherence = less speckle noise in the simulated image.

---

Next: [Section 4 — Optics Pipeline](../04_optics_pipeline/README.md)
