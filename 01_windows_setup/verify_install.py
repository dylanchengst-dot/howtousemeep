"""Run this script to confirm MEEP is installed correctly."""

import sys

def check(label, fn):
    try:
        result = fn()
        print(f"  {label:20s}: {result}")
        return True
    except Exception as e:
        print(f"  {label:20s}: FAILED — {e}")
        return False

print("=== MEEP Installation Check ===\n")

ok = True
ok &= check("Python version", lambda: sys.version.split()[0])

import meep as mp
ok &= check("MEEP version", lambda: mp.__version__)
ok &= check("HDF5 support", lambda: mp.with_hdf5())
ok &= check("MPI support", lambda: mp.with_mpi())

import numpy, matplotlib
ok &= check("NumPy version", lambda: numpy.__version__)
ok &= check("Matplotlib version", lambda: matplotlib.__version__)

print()
if ok:
    print("All checks passed.")
else:
    print("Some checks failed. Review the errors above.")
