# Section 1 — Installing MEEP on Windows

MEEP does not have a native Windows build. The recommended path is
**WSL2 (Windows Subsystem for Linux 2)** with a Conda environment.

---

## Step 1 — Enable WSL2

Open **PowerShell as Administrator** and run:

```powershell
wsl --install
```

Restart your PC when prompted. Windows will install Ubuntu by default.

If you already have WSL1, upgrade to WSL2:

```powershell
wsl --set-default-version 2
wsl --set-version Ubuntu 2
```

Verify:

```powershell
wsl --list --verbose
# Expected: Ubuntu   Running   2
```

---

## Step 2 — Install Miniconda inside WSL2

Open the **Ubuntu** terminal and run:

```bash
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
bash Miniconda3-latest-Linux-x86_64.sh -b -p $HOME/miniconda3
$HOME/miniconda3/bin/conda init bash
source ~/.bashrc
```

---

## Step 3 — Create the MEEP Conda Environment

```bash
conda create -n meep-env -c conda-forge pymeep=*=mpi_mpich* python=3.11 -y
conda activate meep-env
```

> **Why this channel?**  `conda-forge` provides pre-compiled MEEP binaries with
> MPI support, avoiding the need to compile from source.

Install additional dependencies used in this tutorial:

```bash
conda install -n meep-env -c conda-forge \
    matplotlib numpy scipy jupyter h5py -y
```

---

## Step 4 — Verify the Installation

```bash
conda activate meep-env
python verify_install.py
```

Expected output:

```
MEEP version : 1.x.x
HDF5 support : True
MPI support  : True
All checks passed.
```

---

## Step 5 — IDE Integration (VS Code on Windows)

1. Install [VS Code](https://code.visualstudio.com/) on Windows.
2. Install the **WSL** extension (ms-vscode-remote.remote-wsl).
3. In the Ubuntu terminal:

```bash
code .
```

VS Code opens connected to WSL2. Select the `meep-env` Python interpreter
(`Ctrl+Shift+P` → "Python: Select Interpreter" → choose the Conda env path).

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| `wsl --install` not recognized | Update Windows to build 19041+ |
| Conda command not found | Run `source ~/.bashrc` after init |
| MEEP import error | Ensure `meep-env` is activated |
| Slow file I/O in WSL2 | Keep project files inside WSL2 filesystem (`~/`) not `/mnt/c/` |

---

Next: [Section 2 — FDTD Basics](../02_fdtd_basics/README.md)
