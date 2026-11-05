# Implementation Plan: CA3 Recurrent Network Simulation & Temporal Neuromodulation Analysis

**Branch**: `001-ca3-recurrent-simulation` | **Date**: 2026-10-30 | **Spec**: [spec.md](./spec.md)

---

## 1. Summary
Implement an integrated biophysical CA3 recurrent neural network in Python (Brian 2) to systematically test and resolve the two experimental paradoxes of the master's research:
1. Optical low-pass filtering of 14 ms bins in ChR2 (explaining the inconclusive Laura Costa 2026 results).
2. Continuous electrical stimulation saturation of fast-spiking inhibitory interneurons (explaining the Wagner Franklin bancada results).
3. Evaluation of corrective closed-loop event-triggered stimulation.
4. Direct pipeline linking simulation figures and statistics into the LaTeX thesis report (`relatorio_simulacao.tex`).

---

## 2. Technical Context

* **Language / Environment:** Python 3.14 (`Codigos/.venv`)
* **Primary Libraries:** `brian2` (v2.7+), `scipy`, `numpy`, `matplotlib`, `seaborn`
* **Editorial Toolchain:** TinyTeX pdflatex (`C:\Users\acesso-remoto\AppData\Roaming\TinyTeX\bin\windows\pdflatex.exe`)
* **Mathematical Framework:**
  * Neurons: Izhikevich 2D dynamical systems (Regular Spiking for Pyramidal cells; Fast Spiking for Basket cells).
  * Synapses: Conductance-based $\text{AMPA}$ ($E_{\text{rev}} = 0\text{ mV}$, $\tau = 2\text{ ms}$) and $\text{GABA}_A$ ($E_{\text{rev}} = -70\text{ mV}$, $\tau = 5\text{ ms}$) with Tsodyks-Markram short-term depression (STD).
  * Plasticity: Spike-Timing-Dependent Plasticity (STDP) with exponential windows ($\tau_+ = 20\text{ ms}, \tau_- = 20\text{ ms}, A_+ = 0.01, A_- = -0.0105$).
  * Phototransduction: 2-state opsin kinetics ($dO/dt = \alpha \cdot L(t) \cdot (1 - O) - O / \tau_{\text{off}}$) with $\tau_{\text{off}} = 13\text{ ms}$ (ChR2) and $\tau_{\text{off}} = 3.5\text{ ms}$ (Chronos).

---

## 3. Constitution Compliance Check

* **Principle I (Scientific Integrity):** Verified. Both optical and electrical protocols will be modeled with exact parameters from the lab; no tuning to force artificial significance.
* **Principle II (Complete Decoupling):** Verified. Simulation script runs in Python and outputs directly to `relatorios/figuras/` and `relatorios/tabelas/`.
* **Principle III (Biophysical Grounding):** Verified. Canonical parameters from Izhikevich (2003) and Bi & Poo (1998).
* **Principle IV (Anti-AI-ese):** Verified. LaTeX text is objective, structured, and free of emotional fluff.
* **Principle V (Test-Driven Reproducibility):** Verified. Explicit `seed(42)` and step-by-step verification.

---

## 4. Architecture & Execution Phases

```
Phase 1: Model Setup (CA3 Pyramidal + Basket Interneurons in Brian 2)
   │
   ├── Phase 2: Transduction Engine (ChR2 vs Chronos vs Electrical Pulses)
   │
   ├── Phase 3: Long-term Dynamics (Continuous 300s vs Closed-loop Bursts + STDP)
   │
   └── Phase 4: Automated Export to LaTeX Report & Build Verification
```

---

## 5. File Deliverables

* `Codigos/testes/simulacao_ca3_completa_brian2.py`: The unified simulation script.
* `relatorios/figuras/fig_ca3_recorrente_dinamica.pdf`: Multi-panel vector figure showing network rasters, membrane voltages, opsin filtering, and synaptic weights.
* `relatorios/tabelas/tabela_comparacao_biofisica.tex`: Quantitative table comparing modulation depth, calcium integrals, and phase-locking values.
* `relatorios/relatorio_simulacao.tex`: Updated thesis chapter with integrated findings.
