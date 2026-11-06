# Changelog — Modelagem Computacional Biofísica

Registro cronológico estrito de versões e alterações metodológicas implementadas nos modelos de simulação em Brian 2.

---

## [0.1.0] — 2026-11-05 — Modelos Computacionais Preliminares de CA3

### Metodologia e Modelagem
* **Simulação de Microestimulação Elétrica em CA3 (`Codigos/testes/experimento_1_eletrica_wagner_brian2.py`):**
  * Modelagem de microcircuito de 100 neurônios (80 piramidais RS + 20 interneurônios FS) utilizando o formalismo dinâmico 2D de Izhikevich (2003).
  * Sinapses recorrentes excitatórias (AMPA, $\tau = 2\text{ ms}$) e inibitórias ($\text{GABA}_A$, $\tau = 6\text{ ms}$) com depressão sináptica de curto prazo de Tsodyks-Markram (1998) ($\tau_{\text{rec}} = 600\text{ ms}, U_{\text{SE}} = 0{,}45$).
  * Injeção de pulsos elétricos contínuos sob envelope teta de $140\text{ ms}$ ($7{,}14\text{ Hz}$).
* **Simulação de Filtragem Optogenética (`Codigos/testes/experimento_2_optogenetica_laura_brian2.py`):**
  * Implementação da cinética de fotoisomerização de 2 estados para comparação de transdução entre Canalrodopsina-2 clássica (ChR2 wild-type, $\tau_{\text{off}} = 13{,}0\text{ ms}$; Grossman et al., 2011) e opsina ultrarrápida (Chronos, $\tau_{\text{off}} = 3{,}6\text{ ms}$; Klapoetke et al., 2014).
  * Quantificação do filtro passa-baixas biológico sobre pulsos de $7\text{ ms}$ em bins de $14\text{ ms}$ e cálculo da integral de cálcio intracelular como proxy de ativação celular.
