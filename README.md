# 🌟 Genetic Based Algorithm for UAV airfoil generation

> A short tagline or motto that makes your project stand out.

[![License](https://img.shields.io/github/license/FilStazi/GBA_airfoil_efficiency)](LICENSE)
[![Issues](https://img.shields.io/github/issues/FilStazi/GBA_airfoil_efficiency)](https://github.com/FilStazi/GBA_airfoil_efficiency/issues)
[![Stars](https://img.shields.io/github/stars/FilStazi/GBA_airfoil_efficiency)](https://github.com/FilStazi/GBA_airfoil_efficiency/stargazers)

---

## 🚀 About the Project

GBA for UAV Airfoil Generation is a Python-based tool developed as part of my undergraduate thesis. It automates the generation of airfoil shapes optimized to minimize a user-defined fitness function. The tool leverages a simple single-objective genetic algorithm and integrates with XFOIL for aerodynamic analysis, enabling efficient performance evaluation of evolved airfoils for UAV applications.

This tool was initially designed to just explore the capabilities of xfoil and the genetic algorithm but later proved to be very effective in minimizing the objective function.

This version uses the airfoil efficiency $\epsilon$ as the fitness function:

$$
minimize \quad \frac{1}{\epsilon} = \frac{C_D}{C_L}
$$

where:
- $C_L$ is the lift coefficient;
- $C_D$ is the drag coefficient.


---

## 📦 Installation

```bash
# Clone the repository
git clone https://github.com/FilStazi/GBA_airfoil_efficiency.git

# Navigate to the project folder
cd GBA_airfoil_efficiency

# Install dependencies (example: for Node.js or Python)
pip install -r requirements.txt
