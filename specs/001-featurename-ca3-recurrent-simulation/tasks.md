# Tasks: CA3 Recurrent Network Simulation & Temporal Neuromodulation Analysis

**Feature Branch**: `001-ca3-recurrent-simulation`  
**Status**: Completed  
**Spec**: [spec.md](./spec.md) | **Plan**: [plan.md](./plan.md)  

---

## Task List

- [x] **Task 0: Spec Kit Infrastructure & Project Constitution**
  - [x] Install `specify-cli` via `uv` in environment.
  - [x] Initialize project with native Antigravity (`agy`) integration.
  - [x] Establish and ratify `.specify/memory/constitution.md` with 5 non-negotiable scientific and software principles.

- [x] **Task 1: Baseline CA3 Microcircuit Implementation in Brian 2** (P1)
  - [x] Implement Pyramidal (RS) and Basket Interneuron (FS) populations with Izhikevich equations.
  - [x] Implement Tsodyks-Markram short-term synaptic depression (vectorized).
  - [x] Implement GABA_A perisomatic shunting inhibition.

- [x] **Task 2: Refine Experiment 1 - Wagner Electrical Stimulation (CEUA)** (P1)
  - [x] Reorder simulation so Wagner's electrical case comes first.
  - [x] Implement 2-column side-by-side layout with shared Y-axes per row and bottom legends.
  - [x] Explicitly evaluate protocol biological plausibility (continuous 5-min open-loop vs closed-loop).
  - [x] Generate high-resolution figures (PNG 300 DPI + PDF vector) without conclusions in titles.

- [x] **Task 3: Refine Experiment 2 - Laura Optogenetic Filtering (ChR2)** (P1)
  - [x] Implement 2-state ChR2 kinetics ($\tau_{\text{off}} = 13\text{ ms}$) and intracellular calcium integration.
  - [x] Implement 2-column side-by-side layout with shared Y-axes per row and bottom legends.
  - [x] Quantify low-pass filtering and explain the non-significant c-Fos finding in Costa (2026).
  - [x] Generate high-resolution figures (PNG 300 DPI + PDF vector) without conclusions in titles.

- [x] **Task 4: Academic Editorial Section in LaTeX (`relatorio_simulacao.tex`)** (P1)
  - [x] Write educational/scientific introduction to Brian 2 and mathematical models in engineering language.
  - [x] Integrate standard BibTeX bibliography database (`referencias.bib`) with `abntex2cite`.
  - [x] Formulate statistical hypotheses ($H_0$ and $H_1$) and report failure to reject $H_0$ under empirical and continuous conditions.
  - [x] Remove adjectival "de engenharia" and maintain deep academic humility and tentative framing.
  - [x] Scope continuation exclusively to data consolidation and in silico computational neuroscience.
  - [x] Remove standalone glossary table and weave biological explanations into the engineering narrative.
  - [x] Standardize terminology: Padrão 1 ($S_1$) and Padrão 2 ($S_2$); $MS_f$ (microestimulação fixa) and $MS_r$ (microestimulação aleatória).
  - [x] Add panel letter labels (A), (B), (C), (D) directly to plots and reference them in captions.
  - [x] Quantify Tsodyks-Markram steady-state floor plateau ($R_{\text{ss}} \approx 0.106$) vs intermittent vesicle buffer recovery.
  - [x] Migrate all legacy units to modern `siunitx` v3 commands (`\qty` and `\unit`).
  - [x] Compile cleanly with pdflatex and bibtex (19 pages, exit code 0, 0 warnings).

