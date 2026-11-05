"""
========================================================================================
EXPERIMENTO COMPUTACIONAL CONTROLADO: PADRÃO FIXO (MSf) VS. PADRÃO ALEATÓRIO (MSr)
Aplicação Estrita do Método Científico (Santos, Cap. 3 / Feynman, 1974)
========================================================================================
Hipótese Testada (H1 do NNC):
  "A sintaxe temporal repetitiva de 10 bits (MSf) produz uma resposta biológica
   diferente da sintaxe aleatória (MSr), mesmo mantendo o número idêntico de pulsos (6/10)."

Hipótese Nula (H0):
  "Não há diferença mensurável entre MSf e MSr na taxa de disparo, na integral de cálcio
   (proxy de c-Fos) ou na modulação sináptica líquida, pois ambos entregam a mesma energia total."
========================================================================================
"""

import matplotlib.pyplot as plt
import numpy as np
from brian2 import *

prefs.codegen.target = "numpy"
seed(100)

# --------------------------------------------------------------------------------------
# 1. PARÂMETROS TEMPORAIS IDÊNTICOS À DISSERTAÇÃO DE LAURA COSTA (2026, PÁGS. 37-38)
# --------------------------------------------------------------------------------------
defaultclock.dt = 0.05 * ms
f_theta = 7.14 * Hz
T_theta = 140.0 * ms  # Janela de estimulação de 140 ms
T_pause = 140.0 * ms  # Janela de pausa de 140 ms (Laura, pág. 37)
T_cycle = T_theta + T_pause  # Ciclo completo = 280 ms
n_bits = 10
bin_duration = T_theta / n_bits  # 14 ms
pulse_duration = 5.0 * ms  # 5 ms ativo

# Padrão Fixo (MSf): Sempre a mesma palavra de 6 pulsos '1'
# Inicia com bit 1, termina com bit 1 (Laura Costa, pág. 37)
MSf_word = np.array([1, 0, 1, 0, 1, 0, 1, 1, 0, 1])

# Pool de Padrões Aleatórios (MSr): Permutações com exatamente 6 bits '1'
# Primeiro e último bits fixos em 1. Os 4 bits '1' restantes são distribuídos nos 8 bins centrais
np.random.seed(42)
MSr_pool = []
for _ in range(70):
    middle = np.zeros(8, dtype=int)
    ones_idx = np.random.choice(8, size=4, replace=False)
    middle[ones_idx] = 1
    word = np.concatenate(([1], middle, [1]))
    MSr_pool.append(word)

# Duração: 2.8 segundos (10 ciclos de 280 ms)
sim_duration = 2.8 * second
total_steps = int(sim_duration / defaultclock.dt)
time_array = np.arange(total_steps) * defaultclock.dt

# Construção dos trens temporais de iluminação L_MSf(t) e L_MSr(t)
L_MSf = np.zeros(total_steps)
L_MSr = np.zeros(total_steps)

steps_per_cycle = int(T_cycle / defaultclock.dt)
steps_per_theta = int(T_theta / defaultclock.dt)
steps_per_bin = int(bin_duration / defaultclock.dt)
steps_pulse = int(pulse_duration / defaultclock.dt)

for step in range(total_steps):
    cycle_idx = step // steps_per_cycle
    step_in_cycle = step % steps_per_cycle
    
    # Apenas estimula durante os primeiros 140 ms do ciclo (pausa nos 140 ms finais)
    if step_in_cycle < steps_per_theta:
        bin_idx = step_in_cycle // steps_per_bin
        step_in_bin = step_in_cycle % steps_per_bin
        
        if step_in_bin < steps_pulse:
            # MSf
            if MSf_word[bin_idx] == 1:
                L_MSf[step] = 1.0
            # MSr (cada ciclo sorteia uma das palavras do pool)
            current_MSr_word = MSr_pool[cycle_idx % len(MSr_pool)]
            if current_MSr_word[bin_idx] == 1:
                L_MSr[step] = 1.0

light_MSf = TimedArray(L_MSf, dt=defaultclock.dt)
light_MSr = TimedArray(L_MSr, dt=defaultclock.dt)

# --------------------------------------------------------------------------------------
# 2. MODELO NEURONAL COM CHR2 E SENSOR DE CÁLCIO (PROXY DE C-FOS)
# --------------------------------------------------------------------------------------
# Neurônio 0: Submetido a MSf (Padrão Fixo)
# Neurônio 1: Submetido a MSr (Padrão Aleatório)
Area = 20000 * umetre**2
Cm = 1.0 * ufarad / cm**2 * Area
gL = 0.1 * msiemens / cm**2 * Area
EL = -65 * mV
gNa = 100 * msiemens / cm**2 * Area
ENa = 50 * mV
gK = 30 * msiemens / cm**2 * Area
EK = -90 * mV
g_ChR2_max = 0.25 * msiemens / cm**2 * Area
tau_ChR2 = 13.0 * ms
E_ChR2 = 0 * mV
tau_Ca = 200 * ms  # Drenagem de cálcio intracelular

eqs = """
dv/dt = (-(gNa*m**3*h*(v - ENa) + gK*n**4*(v - EK) + gL*(v - EL)) - g_ChR2*(v - E_ChR2))/Cm : volt
dm/dt = alpha_m*(1 - m) - beta_m*m : 1
dh/dt = alpha_h*(1 - h) - beta_h*h : 1
dn/dt = alpha_n*(1 - n) - beta_n*n : 1

alpha_m = (0.1/mV)*(-40*mV - v)/(exp((-40*mV - v)/(10*mV)) - 1)/ms : 1/second
beta_m  = 4.0*exp((-65*mV - v)/(18*mV))/ms : 1/second
alpha_h = 0.07*exp((-65*mV - v)/(20*mV))/ms : 1/second
beta_h  = 1.0/(exp((-35*mV - v)/(10*mV)) + 1)/ms : 1/second
alpha_n = (0.01/mV)*(-55*mV - v)/(exp((-55*mV - v)/(10*mV)) - 1)/ms : 1/second
beta_n  = 0.125*exp((-65*mV - v)/(80*mV))/ms : 1/second

# Dinâmica da ChR2 com entrada dependente do neurônio
dg_ChR2/dt = (L_stim*g_ChR2_max - g_ChR2)/tau_ChR2 : siemens
L_stim : 1

# Sensor de Cálcio Intracelular (Integral de ativação celular -> Proxy de c-Fos)
# Entra cálcio proporcional à condutância e despolarização quando v > -20 mV
dCa/dt = clip((v - EL)/(10*mV), 0, 10)/tau_Ca - Ca/tau_Ca : 1
"""

neurons = NeuronGroup(2, eqs, threshold="v > 0*mV", refractory=3*ms, method="rk4")
neurons.v = EL
neurons.m = 0.05
neurons.h = 0.6
neurons.n = 0.32
neurons.Ca = 0.0

@network_operation
def update_stimuli():
    t_now = defaultclock.t
    neurons.L_stim[0] = light_MSf(t_now)
    neurons.L_stim[1] = light_MSr(t_now)

# Conexão sináptica eferente com STDP para testar se há divergência sináptica
post_neurons = NeuronGroup(2, "dv/dt = (EL - v)/(20*ms) : volt", threshold="v > -50*mV", reset="v = EL", method="exact")
post_neurons.v = EL

syn_eqs = """
w : 1
dApre/dt = -Apre/(20*ms) : 1 (event-driven)
dApost/dt = -Apost/(20*ms) : 1 (event-driven)
"""
syn = Synapses(neurons, post_neurons, model=syn_eqs,
               on_pre="""
               v_post += w * 15 * mV
               Apre += 0.01
               w = clip(w + Apost, 0, 1.0)
               """,
               on_post="""
               Apost -= 0.0105
               w = clip(w + Apre, 0, 1.0)
               """)
syn.connect(i=[0, 1], j=[0, 1])
syn.w = 0.5

# Monitores
mon = StateMonitor(neurons, ("v", "Ca", "g_ChR2"), record=True)
spikes = SpikeMonitor(neurons)
mon_syn = StateMonitor(syn, "w", record=True)

print("Executando simulação comparativa estrita MSf vs. MSr...")
run(sim_duration, report="text")
print("Simulação concluída!")

# --------------------------------------------------------------------------------------
# 3. EXTRAÇÃO DE DADOS NUMÉRICOS REAIS (SEM INTERPRETAÇÃO PRÉ-CONCEBIDA)
# --------------------------------------------------------------------------------------
spikes_MSf = len(spikes.t[spikes.i == 0])
spikes_MSr = len(spikes.t[spikes.i == 1])

# Integral do Cálcio ao longo do tempo (Área sob a curva = biomarcador de c-Fos)
dt_val = defaultclock.dt / second
integral_Ca_MSf = np.sum(mon.Ca[0]) * dt_val
integral_Ca_MSr = np.sum(mon.Ca[1]) * dt_val
diff_Ca_percent = abs(integral_Ca_MSf - integral_Ca_MSr) / integral_Ca_MSf * 100

final_w_MSf = mon_syn.w[0][-1]
final_w_MSr = mon_syn.w[1][-1]

print("\n" + "="*70)
print("RELATÓRIO DE DADOS EXPERIMENTAIS OBTIDOS DA SIMULAÇÃO:")
print("="*70)
print(f"Total de Spikes disparados (2.8 s):")
print(f"  - Padrão Fixo (MSf):     {spikes_MSf} spikes")
print(f"  - Padrão Aleatório (MSr): {spikes_MSr} spikes")
print(f"Integral de Cálcio Acumulado (Proxy de c-Fos):")
print(f"  - MSf: {integral_Ca_MSf:.4f} unidades*s")
print(f"  - MSr: {integral_Ca_MSr:.4f} unidades*s")
print(f"  - Diferença percentual: {diff_Ca_percent:.2f}%")
print(f"Peso Sináptico Final (w):")
print(f"  - MSf: {final_w_MSf:.4f}")
print(f"  - MSr: {final_w_MSr:.4f}")
print("="*70 + "\n")

# --------------------------------------------------------------------------------------
# 4. PLOTAGEM DOS DADOS BRUTOS
# --------------------------------------------------------------------------------------
fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(12, 8), sharex=True)

# Janela de zoom: 2 ciclos (560 ms)
t_zoom = 560 * ms
mask = mon.t <= t_zoom
t_ms = mon.t[mask] / ms

ax1.plot(t_ms, mon.v[0][mask] / mV, color="red", lw=1.2, label=f"MSf (Fixo) - Spikes: {spikes_MSf}")
ax1.plot(t_ms, mon.v[1][mask] / mV, color="blue", lw=1.2, alpha=0.7, linestyle="--", label=f"MSr (Aleatório) - Spikes: {spikes_MSr}")
ax1.set_ylabel("Tensão Vm (mV)", fontsize=10, fontweight="bold")
ax1.set_title("Dinâmica de Disparo: MSf (Padrão Fixo) vs. MSr (Padrão Aleatório) sob ChR2", fontsize=11, fontweight="bold")
ax1.grid(True, linestyle=":", alpha=0.6)
ax1.legend(loc="upper right")

ax2.plot(t_ms, mon.Ca[0][mask], color="red", lw=1.5, label="Cálcio MSf (Fixo)")
ax2.plot(t_ms, mon.Ca[1][mask], color="blue", lw=1.5, linestyle="--", label="Cálcio MSr (Aleatório)")
ax2.set_ylabel("Nível de Ca2+ [arb]", fontsize=10, fontweight="bold")
ax2.set_title(f"Sensor de Cálcio Intracelular (Proxy de c-Fos): Diferença Acumulada = {diff_Ca_percent:.2f}%", fontsize=11, fontweight="bold")
ax2.grid(True, linestyle=":", alpha=0.6)
ax2.legend(loc="upper right")

ax3.plot(mon_syn.t / second, mon_syn.w[0], color="red", lw=1.5, label=f"Peso Sináptico w (MSf) -> Final: {final_w_MSf:.3f}")
ax3.plot(mon_syn.t / second, mon_syn.w[1], color="blue", lw=1.5, linestyle="--", label=f"Peso Sináptico w (MSr) -> Final: {final_w_MSr:.3f}")
ax3.set_xlabel("Tempo de Simulação (s)", fontsize=10, fontweight="bold")
ax3.set_ylabel("Peso w", fontsize=10, fontweight="bold")
ax3.set_title("Evolução Sináptica Eferente sob Regra STDP", fontsize=11, fontweight="bold")
ax3.grid(True, linestyle=":", alpha=0.6)
ax3.legend(loc="upper right")

plt.tight_layout()
out_plot = "resultado_cientifico_laura_msf_vs_msr.png"
plt.savefig(out_plot, dpi=300)
print(f"Gráfico do teste salvo em: {out_plot}")
