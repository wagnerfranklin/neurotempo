# Feature Specification: CA3 Recurrent Network Simulation & Temporal Neuromodulation Analysis

**Feature Branch**: `001-ca3-recurrent-simulation`  
**Created**: 2026-10-30  
**Status**: Ready for Planning / Implementation  
**Context**: PPGEE / UFMG Master's Thesis (Neurociência Computacional / Processamento de Sinais)  

---

## 1. Problem Statement & Research Motivation

In animal behavioral experiments (Wagner Franklin, CEUA protocol), continuous 7.14 Hz electrical microstimulation ($\mu$ES, $25\ \mu\text{A}$, 10-bit patterns) in CA3 of ventral hippocampus during a 5-minute object-context recognition task yielded inconclusive behavioral discrimination. Concurrently, optogenetic microstimulation in ventral CA3 (Laura Amado Costa, 2026) using identical temporal windows (140 ms theta cycle, 10 bits, 6 pulses) in auditory fear conditioning was also inconclusive (no difference in freezing or c-Fos expression between fixed and random patterns).

This project transitions from inconclusive *in vivo* trials to an *in silico* biophysical investigation in Brian 2 to answer two fundamental signal-processing questions:
1. **The Optical Low-Pass Filter Paradox (Laura Costa 2026):** Why did fixed ($MS_f$) and random ($MS_r$) optical trains produce indistinguishable c-Fos and freezing? (Hypothesis: channelrhodopsin-2 deactivation kinetics act as a biological low-pass filter with $\tau_{\text{off}} \approx 13\text{ ms}$, blurring 14 ms bins into an unmodulated DC plateau).
2. **The Continuous Electrical Saturation Paradox (Wagner Franklin):** Why did 5-minute continuous electrical stimulation fail to establish artificial context-object associations? (Hypothesis: continuous electrical stimulation preferentially recruits low-threshold fast-spiking $PV^+$ GABAergic interneurons, causing chronic feedforward inhibition and short-term synaptic depression that shuts down CA3 pattern separation).

---

## 2. User & Researcher Scenarios (Prioritized)

### User Story 1 — Two-Population Recurrent CA3 Microcircuit in Brian 2 (Priority: P1 - MVP)
As a neuroengineering researcher, I want a reproducible biophysical simulation of a CA3 microcircuit containing excitatory Pyramidal cells (RS) and inhibitory Fast-Spiking interneurons ($PV^+$ basket cells) interconnected with AMPA and $\text{GABA}_A$ conductances.

* **Why this priority:** It is the foundational substrate required to simulate any stimulation protocol.
* **Independent Test:** Run `python simulacao_ca3_brian2.py`. The network must exhibit spontaneous/driven theta-gamma nested oscillations without unconstrained epileptic runaway.
* **Acceptance Scenarios:**
  1. **Given** baseline resting potential ($V_{\text{rest}} = -65\text{ mV}$), **When** background Poisson noise is applied, **Then** pyramidal cells fire at $1\text{--}5\text{ Hz}$ and interneurons at $10\text{--}25\text{ Hz}$.
  2. **Given** a current step, **When** injected into RS cells, **Then** spike-frequency adaptation is observed matching Izhikevich (2003) parameters ($a=0.02, b=0.2, c=-65, d=8$).

---

### User Story 2 — Comparative Transduction Simulation: Optical (ChR2/Chronos) vs. Electrical (Priority: P1)
As a researcher, I want to inject the exact 10-bit temporal sequences used in the UFMG laboratory into the simulated CA3 network under three transduction mechanisms:
1. Optogenetics with ChR2 ($\tau_{\text{off}} = 13\text{ ms}$).
2. Fast Optogenetics with Chronos ($\tau_{\text{off}} = 3.5\text{ ms}$).
3. Direct Electrical Stimulation (instantaneous extracellular charge injection).

* **Why this priority:** Directly tests and resolves the core thesis question regarding signal attenuation and phase-locking.
* **Independent Test:** Compare vector strength / phase-locking value (PLV) and intracellular calcium integral across the three conditions.
* **Acceptance Scenarios:**
  1. **Given** 14 ms bit bins, **When** ChR2 is simulated, **Then** membrane depolarization modulation depth is attenuated by $>70\%$ compared to input pulses, producing $<2\%$ difference in calcium accumulation between fixed and random patterns.
  2. **Given** 14 ms bit bins, **When** Chronos or direct electrical pulses are simulated, **Then** distinct action potentials lock to individual 14 ms active slots.

---

### User Story 3 — Continuous Stimulation vs. Closed-Loop / Event-Triggered Stimulation (Priority: P2)
As a researcher, I want to simulate the difference between:
- **Continuous 5-Minute Stimulation** (as applied in the thesis cohort).
- **Closed-Loop / Proximity-Triggered Stimulation** (active only during the $\approx 3\text{--}5\text{ s}$ exploratory bouts near the object).

* **Why this priority:** Establishes the corrective guideline for future biological experiments at NNC/UFMG, transforming a negative result into an actionable design recommendation.
* **Independent Test:** Measure synaptic weight evolution under STDP rules for 300 s continuous vs. burst-exploratory regimes.
* **Acceptance Scenarios:**
  1. **Given** continuous 7.14 Hz stimulation for 300 s, **When** recurrent synapses are tracked, **Then** short-term depression (STD) drives synaptic efficacy to $<15\%$ of baseline.
  2. **Given** event-triggered bursts, **When** paired with object interaction, **Then** stable long-term potentiation (LTP) is induced in object-coding cell assemblies.

---

### User Story 4 — Automated Figure & Table Export to LaTeX (Priority: P2)
As an author, I want all simulation outputs to save publication-grade vector PDFs and summary tables into `relatorios/figuras/` and `relatorios/tabelas/`, automatically updating the compiled master thesis report (`relatorio_simulacao.tex`).

* **Independent Test:** Execute the simulation pipeline, then run `compilar_latex.bat`. The LaTeX compilation must exit with code 0 and include the updated figures.

---

## 3. Biophysical & Computational Constraints

1. **Simulator:** Brian 2 (`brian2`), NumPy target.
2. **Numerical Time Step:** $dt \le 0.05\text{ ms}$ for accurate Hodgkin-Huxley or Izhikevich integration.
3. **Random Seed:** Strict seed definition (`seed(42)`) for 100% deterministic reproducibility.
4. **Data Contract:** No ad-hoc file paths; all relative to repository root.
5. **Editorial Decoupling:** Pure Python $\rightarrow$ Pure LaTeX. No web daemons.
