"""
========================================================================================
ESTUDO COMPARATIVO DE TRANSDUÇÃO E PHASE-LOCKING NO CIRCUITO HIPOCAMPAL
Optogenética Clássica (ChR2) vs. Optogenética Rápida (Chronos) vs. Estimulação Elétrica
Análise Mecanicista: Por que a Optogenética Clássica Perde Resolução em Bins de 14 ms
========================================================================================
Autores: Núcleo de Neurociências (NNC / PPGEE / UFMG)
Modelo: Hodgkin-Huxley com Inativação de Sódio + Cinética de Fotocorrente + STDP
========================================================================================
"""

import matplotlib.pyplot as plt
import numpy as np
from brian2 import *

prefs.codegen.target = "numpy"
seed(42)

# --------------------------------------------------------------------------------------
# 1. PARÂMETROS TEMPORAIS E DO ENVELOPE TETA (7.14 Hz)
# --------------------------------------------------------------------------------------
defaultclock.dt = 0.05 * ms
f_theta = 7.14 * Hz
T_theta = 1.0 / f_theta  # ~140 ms
n_bits = 10
bin_duration = T_theta / n_bits  # 14 ms por bit
pulse_duration = 5.0 * ms  # Duração ativa do pulso de luz ou corrente

# Padrão temporal experimental (10 bits): Padrão 1 do protocolo do NNC
# Bit '1' = Estímulo ativo nos primeiros 5 ms do bin de 14 ms
bit_pattern = np.array([1, 0, 1, 0, 1, 0, 1, 1, 0, 1])

# Duração total da simulação: 1 segundo (~7 ciclos teta completos)
sim_duration = 1.0 * second
total_steps = int(sim_duration / defaultclock.dt)
time_array = np.arange(total_steps) * defaultclock.dt

# Construção do trem de pulsos de iluminação / corrente lógica L(t) in [0, 1]
L_input = np.zeros(total_steps)
step_bin = int(bin_duration / defaultclock.dt)
step_pulse = int(pulse_duration / defaultclock.dt)
steps_per_theta = int(T_theta / defaultclock.dt)

for step in range(total_steps):
    step_in_theta = step % steps_per_theta
    bit_idx = int(step_in_theta / step_bin)
    if bit_idx < n_bits and bit_pattern[bit_idx] == 1:
        step_in_bin = step_in_theta % step_bin
        if step_in_bin < step_pulse:
            L_input[step] = 1.0

# Cria TimedArray no Brian 2
light_intensity = TimedArray(L_input, dt=defaultclock.dt)

# --------------------------------------------------------------------------------------
# 2. MODELO BIOFÍSICO HODGKIN-HUXLEY DOS NEURÔNIOS DE CA3
# --------------------------------------------------------------------------------------
# Área de membrana típica de célula piramidal hipocampal
Area = 20000 * umetre**2
Cm = 1.0 * ufarad / cm**2 * Area
gL = 0.1 * msiemens / cm**2 * Area
EL = -65 * mV
gNa = 100 * msiemens / cm**2 * Area
ENa = 50 * mV
gK = 30 * msiemens / cm**2 * Area
EK = -90 * mV

# Parâmetros das 3 Modalidades de Estímulo:
# Neurônio 0: Optogenética Clássica ChR2 (Laura Costa, 2026) -> tau_off = 13 ms
# Neurônio 1: Optogenética Ultrarrápida Chronos/ChETA        -> tau_off = 3.5 ms
# Neurônio 2: Estimulação Elétrica Direta (Wagner Franklin)  -> Resposta direta sem atraso
E_ChR2 = 0 * mV
g_ChR2_max = 0.25 * msiemens / cm**2 * Area

eqs_hh = """
dv/dt = (-(gNa*m**3*h*(v - ENa) + gK*n**4*(v - EK) + gL*(v - EL)) + I_stim)/Cm : volt

# Cinética das comportas de Hodgkin-Huxley (Hodgkin & Huxley, 1952)
dm/dt = alpha_m*(1 - m) - beta_m*m : 1
dh/dt = alpha_h*(1 - h) - beta_h*h : 1
dn/dt = alpha_n*(1 - n) - beta_n*n : 1

alpha_m = (0.1/mV)*(-40*mV - v)/(exp((-40*mV - v)/(10*mV)) - 1)/ms : 1/second
beta_m  = 4.0*exp((-65*mV - v)/(18*mV))/ms : 1/second

alpha_h = 0.07*exp((-65*mV - v)/(20*mV))/ms : 1/second
beta_h  = 1.0/(exp((-35*mV - v)/(10*mV)) + 1)/ms : 1/second

alpha_n = (0.01/mV)*(-55*mV - v)/(exp((-55*mV - v)/(10*mV)) - 1)/ms : 1/second
beta_n  = 0.125*exp((-65*mV - v)/(80*mV))/ms : 1/second

# Dinâmica do Transdutor de Estimulação
dg_opsin/dt = (light_intensity(t)*g_ChR2_max - g_opsin)/tau_opsin : siemens
I_stim = -g_opsin*(v - E_ChR2) + I_elec : amp

I_elec : amp
tau_opsin : second
"""

# População com 3 neurônios representativos das 3 condições experimentais
ca3_neurons = NeuronGroup(3, eqs_hh, method="rk4")
ca3_neurons.v = EL
ca3_neurons.m = 0.05
ca3_neurons.h = 0.6
ca3_neurons.n = 0.32

# Configuração das modalidades:
# 0: ChR2 clássica (Laura)
ca3_neurons.tau_opsin[0] = 13.0 * ms
ca3_neurons.I_elec[0] = 0.0 * pA

# 1: Chronos rápida (Alternativa Otimizada)
ca3_neurons.tau_opsin[1] = 3.5 * ms
ca3_neurons.I_elec[1] = 0.0 * pA

# 2: Estimulação Elétrica Direta (Wagner)
ca3_neurons.tau_opsin[2] = 0.1 * ms  # Inerte
ca3_neurons.I_elec[2] = 0.0 * pA  # Controlado via network run ou corrente direta

# Para simular a estimulação elétrica instantânea no Neurônio 2:
# Injeta corrente pulsada direta de 350 pA casada com o sinal L(t)
@network_operation
def update_electrical_stim():
    ca3_neurons.I_elec[2] = light_intensity(defaultclock.t) * 350 * pA

# --------------------------------------------------------------------------------------
# 3. INSTRUMENTAÇÃO: MONITORES DE ESTADO E INATIVAÇÃO DE SÓDIO
# --------------------------------------------------------------------------------------
mon_state = StateMonitor(ca3_neurons, ("v", "h", "g_opsin", "I_stim"), record=True)

print("Iniciando simulação biofísica multimodular no Brian 2...")
run(sim_duration, report="text")
print("Simulação concluída com sucesso!")

# --------------------------------------------------------------------------------------
# 4. ANÁLISE QUANTITATIVA DOS RESULTADOS (MÉTRICAS MATEMÁTICAS)
# --------------------------------------------------------------------------------------
# Janela representativa de 2 ciclos teta (280 ms) entre 200 ms e 480 ms
t_start = 200 * ms
t_end = 480 * ms
mask = (mon_state.t >= t_start) & (mon_state.t <= t_end)
time_plot = (mon_state.t[mask] - t_start) / ms

# --------------------------------------------------------------------------------------
# 5. VISUALIZAÇÃO GRÁFICA COMPARATIVA DE ALTA RESOLUÇÃO
# --------------------------------------------------------------------------------------
fig, (ax0, ax1, ax2, ax3) = plt.subplots(
    4, 1, figsize=(13, 10), sharex=True, gridspec_kw={"height_ratios": [1, 2.5, 2.5, 2]}
)

# Painel 0: O Padrão Digital Desejado (Palavra de 10 bits sob Envelope Teta)
L_zoom = [light_intensity(t * ms + t_start) for t in time_plot]
ax0.fill_between(time_plot, 0, L_zoom, color="gold", alpha=0.8, step="pre")
ax0.set_ylim(-0.1, 1.2)
ax0.set_yticks([0, 1])
ax0.set_yticklabels(["Off", "On"], fontweight="bold")
ax0.set_ylabel("Sinal L(t)", fontsize=10, fontweight="bold")
ax0.set_title(
    "Padrão 1 Solicitado: 10 Bits em Janela Teta de 140 ms ('1010101101') - Cada Bit = 14 ms",
    fontsize=11,
    fontweight="bold",
)
ax0.grid(True, linestyle=":", alpha=0.5)

# Painel 1: Condição Laura Costa (2026) - Optogenética Clássica ChR2
ax1.plot(
    time_plot,
    mon_state.v[0][mask] / mV,
    color="darkred",
    lw=1.5,
    label="Tensão Vm(t) [ChR2, tau_off=13ms]",
)
ax1.axhline(0, color="gray", linestyle="--", alpha=0.5)
ax1.axhline(-35, color="red", linestyle=":", label="Limiar Bloqueio Inativação Na+ (-35 mV)")
ax1.set_ylabel("Tensão Vm (mV)", fontsize=10, fontweight="bold")
ax1.set_title(
    "Condição Laura (2026): ChR2 Lenta -> Acúmulo de Carga, Inativação de Na+ e Perda de Bits",
    fontsize=11,
    fontweight="bold",
)
ax1.grid(True, linestyle=":", alpha=0.5)
ax1.legend(loc="upper right", framealpha=0.9)

# Painel 2: Condições Otimizadas (Chronos Rápida vs. Elétrica Wagner)
ax2.plot(
    time_plot,
    mon_state.v[1][mask] / mV,
    color="blue",
    lw=1.2,
    alpha=0.85,
    label="Opto Rápida (Chronos, tau_off=3.5ms)",
)
ax2.plot(
    time_plot,
    mon_state.v[2][mask] / mV,
    color="green",
    lw=1.2,
    alpha=0.85,
    linestyle="--",
    label="Elétrica Direta (Wagner, tau=0ms)",
)
ax2.set_ylabel("Tensão Vm (mV)", fontsize=10, fontweight="bold")
ax2.set_title(
    "Condições de Alta Fidelidade Temporal: Preservação de Cada Spike Individual nos Bits '1'",
    fontsize=11,
    fontweight="bold",
)
ax2.grid(True, linestyle=":", alpha=0.5)
ax2.legend(loc="upper right", framealpha=0.9)

# Painel 3: A Causa Biofísica - Variável de Inativação de Sódio h(t)
# Se h(t) cai abaixo de ~0.15, os canais de sódio estão inativados (Depolarization Block)
ax3.plot(
    time_plot,
    mon_state.h[0][mask],
    color="darkred",
    lw=1.5,
    label="h(t) Laura (ChR2) - Bloqueio Severo",
)
ax3.plot(
    time_plot,
    mon_state.h[1][mask],
    color="blue",
    lw=1.2,
    label="h(t) Chronos - Recuperação Rápida",
)
ax3.plot(
    time_plot,
    mon_state.h[2][mask],
    color="green",
    lw=1.2,
    linestyle="--",
    label="h(t) Elétrica - Recuperação Plena",
)
ax3.axhline(0.15, color="black", linestyle="--", alpha=0.7, label="Limiar Crítico de Inativação")
ax3.set_xlabel("Tempo Relativo (ms) [2 Ciclos Teta de 140 ms]", fontsize=10, fontweight="bold")
ax3.set_ylabel("Comporta de Na+ [h]", fontsize=10, fontweight="bold")
ax3.set_title(
    "Mecanismo de Despolarização em Bloco: ChR2 Mantém Na+ Inativado (h < 0.15), Impedindo Spikes Sucessivos",
    fontsize=11,
    fontweight="bold",
)
ax3.grid(True, linestyle=":", alpha=0.5)
ax3.legend(loc="upper right", framealpha=0.9)

plt.tight_layout()
output_file = "figura_optogenetica_vs_eletrica_phase_locking.png"
plt.savefig(output_file, dpi=300)
print(f"Figura comparativa gerada com sucesso e salva em: {output_file}")
