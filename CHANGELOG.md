# Changelog — Modelagem Computacional Biofísica

Registro cronológico estrito de versões e alterações metodológicas implementadas nos modelos de simulação em Brian 2.

---

## [0.1.0] — 2026-11-05 — Modelos Computacionais Preliminares de CA3

### Metodologia e Modelagem
* **Simulação de Microestimulação Elétrica em CA3 (`simulacao/S_experimento_1_eletrica_wagner_brian2.py`):**
  * Modelagem de microcircuito de 100 neurônios (80 piramidais RS + 20 interneurônios FS) utilizando o formalismo dinâmico 2D de Izhikevich (2003).
  * Sinapses recorrentes excitatórias (AMPA, τ = 2 ms) e inibitórias (GABA_A, τ = 6 ms) com depressão sináptica de curto prazo de Tsodyks-Markram (1998) (τ_rec = 600 ms, U_SE = 0.45).
  * Injeção de pulsos elétricos contínuos sob envelope teta de 140 ms (7.14 Hz).
* **Simulação de Filtragem Optogenética (`simulacao/S_experimento_2_optogenetica_laura_brian2.py`):**
  * Implementação da cinética de fotoisomerização de 2 estados para comparação de transdução entre Canalrodopsina-2 clássica (ChR2 wild-type, τ_off = 13.0 ms; Grossman et al., 2011) e opsina ultrarrápida (Chronos, τ_off = 3.6 ms; Klapoetke et al., 2014).
  * Quantificação do filtro passa-baixas biológico sobre pulsos de 7 ms em bins de 14 ms e cálculo da integral de cálcio intracelular como proxy de ativação celular.
* **Fundamentação Bibliográfica (`relatorios/referencias.bib`):**
  * Parâmetros biofísicos de condutância e cinéticas de transdução fundamentados na literatura indexada no arquivo `relatorios/referencias.bib`.
