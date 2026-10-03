<div align="center">

# 🧮 NAPSS — Numerical Analysis Problem Solver System

**A sleek, high-precision desktop application for solving numerical differentiation using finite difference methods.**

[![Windows](https://img.shields.io/badge/Platform-Windows-0078D6?style=for-the-badge&logo=windows)](https://github.com)
[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python)](https://www.python.org/)
[![SymPy](https://img.shields.io/badge/Math-SymPy-3B5526?style=for-the-badge)](https://www.sympy.org/)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)

---

### 📥 [**Download Portable Windows Executable (.EXE)**](../../releases/latest)

</div>

<br/>

## 🎯 Key Features

* ⚡ **High Precision Computation**: Leverages **SymPy** for exact symbolic mathematics evaluation.
* 🌌 **Cyber-Neon Dark UI**: Modern custom-designed interface built with Tkinter & Canvas components.
* 📐 **Comprehensive Differentiation**:
  * **First Derivative $f'(x)$**: Backward, Central, and Forward formulas.
  * **Second Derivative $f''(x)$**: Backward, Central, and Forward formulas.
* 📊 **Dynamic Input UI**: Adaptable field inputs based on selected stencil points.
* 📜 **Calculation History**: Track past results seamlessly within the application session.
* 🚀 **Standalone Application**: Runs directly as a portable `.exe` without requiring Python environment.

---

## 💻 Tech Stack & Architecture

| Component | Technology | Purpose |
| :--- | :--- | :--- |
| **Language** | Python 3 | Core logic & scripting |
| **GUI Framework** | Tkinter & Canvas | UI rendering & dark mode theme |
| **Math Engine** | SymPy | Symbolic math manipulation & calculus |
| **Image Engine** | Pillow (PIL) | Dynamic circular icon masking |
| **Packaging** | PyInstaller | Standalone executable compilation |

---

## 📦 Quick Start (No Setup Needed)

1. Head over to the **[Releases Section](../../releases/latest)**.
2. Download `NAPSS_PRO.exe`.
3. Run the executable instantly on any Windows PC.

---

## 🛠️ Developer Setup (Run from Source)

If you wish to run or modify the source code locally:

```bash
# 1. Clone the repository
git clone [https://github.com/omersaker0100/NAPSS-Numerical-Analysis-Solver.git](https://github.com/omersaker0100/NAPSS-Numerical-Analysis-Solver.git)

# 2. Navigate into the directory
cd NAPSS-Numerical-Analysis-Solver

# 3. Install required packages
pip install sympy pillow pyinstaller

# 4. Launch the application
python NAPSS_PRO.py
