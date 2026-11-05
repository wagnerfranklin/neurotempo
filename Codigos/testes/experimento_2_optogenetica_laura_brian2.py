"""
========================================================================================
EXPERIMENTO COMPUTACIONAL 2 (BRIAN 2): ESTIMULAÇÃO OPTOGENÉTICA (LAURA COSTA, 2026)
ANÁLISE DE FILTRAGEM BIOFÍSICA: ChR2 WILD-TYPE (tau_off = 13.0 ms) vs CHRONOS (tau_off = 3.6 ms)
========================================================================================
Parâmetros da Dissertação de Laura Amado Costa (UFMG, 2026):
  - Alvo Anatômico: Hipocampo Ventral (Sub-região CA3)
  - Coordenadas Estereotáxicas (pág. 33):
      Injeção viral: AP: -3.10 mm; ML: ±3.00 mm; DV: -3.90 mm
      Fibra óptica:  AP: -3.10 mm; ML: ±3.00 mm; DV: -3.80 mm
  - Estímulo Luminoso: Laser azul de 488 nm (10-12 mW na ponta, pulsos de 7 ms)
  - Sintaxe Temporal: Ciclo Teta de 140 ms (7.14 Hz) com pausa de 140 ms (ciclo total 280 ms)
      * Padrão Fixo (MSf): Palavra fixa de 10 bins [1, 0, 1, 0, 1, 0, 1, 1, 0, 1] (6 pulsos ativos)
      * Padrão Aleatório (MSr): Permutações estocásticas de 10 bins com 6 pulsos ativos
  - Opsinas Comparadas:
      1. Canalrodopsina-2 (ChR2 Wild-Type): tau_off = 13.0 ms (Nagel et al., 2003; Grossman et al., 2011)
      2. Chronos (Opsina Ultrarrápida): tau_off = 3.6 ms (Klapoetke et al., 2014)
========================================================================================
"""

import os
import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

import numpy as np
import matplotlib.pyplot as plt
from brian2 import *

# --------------------------------------------------------------------------------------
# 1. AMBIENTE E REPRODUTIBILIDADE
# --------------------------------------------------------------------------------------
prefs.codegen.target = "numpy"
seed(42)
np.random.seed(42)

defaultclock.dt = 0.05 * ms

# --------------------------------------------------------------------------------------
# 2. DEFINIÇÃO DA ESTIMULAÇÃO LUMINOSA
# --------------------------------------------------------------------------------------
f_theta = 7.14 * Hz
T_theta = 1.0 / f_theta                # 140.0 ms (janela de estimulação)
T_pause = 140.0 * ms                  # 140.0 ms (pausa entre ciclos)
T_cycle = T_theta + T_pause           # 280.0 ms por ciclo completo
n_bits = 10
bin_duration = T_theta / n_bits       # 14.0 ms por bin
pulse_duration = 7.0 * ms             # 7.0 ms de pulso de laser

# Padrão Fixo (MSf)
MSf_word = np.array([1, 0, 1, 0, 1, 0, 1, 1, 0, 1], dtype=int)

# Padrão Aleatório (MSr): Pool de permutações com 6 pulsos ativos
MSr_pool = []
for _ in range(50):
    middle = np.zeros(8, dtype=int)
    idx_ones = np.random.choice(8, size=4, replace=False)
    middle[idx_ones] = 1
    word = np.concatenate(([1], middle, [1]))
    MSr_pool.append(word)

n_cycles = 10
sim_time = n_cycles * T_cycle         # 2800.0 ms

total_steps = int(np.round(sim_time / defaultclock.dt))
steps_per_cycle = int(np.round(T_cycle / defaultclock.dt))
steps_stim_window = int(np.round(T_theta / defaultclock.dt))
steps_per_bin = int(np.round(bin_duration / defaultclock.dt))
steps_pulse = int(np.round(pulse_duration / defaultclock.dt))

L_MSf = np.zeros(total_steps, dtype=float)
L_MSr = np.zeros(total_steps, dtype=float)

for step in range(total_steps):
    c_idx = step // steps_per_cycle
    step_in_c = step % steps_per_cycle
    
    if step_in_c < steps_stim_window:
        b_idx = step_in_c // steps_per_bin
        step_in_b = step_in_c % steps_per_bin
        
        if step_in_b < steps_pulse:
            if b_idx < n_bits and MSf_word[b_idx] == 1:
                L_MSf[step] = 1.0
            
            curr_MSr = MSr_pool[c_idx % len(MSr_pool)]
            if b_idx < n_bits and curr_MSr[b_idx] == 1:
                L_MSr[step] = 1.0

light_MSf = TimedArray(L_MSf, dt=defaultclock.dt)
light_MSr = TimedArray(L_MSr, dt=defaultclock.dt)

# --------------------------------------------------------------------------------------
# 3. FUNÇÃO DE SIMULAÇÃO PARAMÉTRICA DE OPSINA
# --------------------------------------------------------------------------------------
alpha_light = 0.8 / ms         # Taxa de abertura fotônica
E_rev = 0.0 * mV               # Potencial de reversão
g_max = 38.0                   # Condutância máxima normalizada
tau_Ca = 150.0 * ms            # Cinética de clearance de cálcio
delta_Ca = 1.0                 # Incremento por potencial de ação

def run_optogenetics(tau_off_val):
    start_scope()
    
    eqs = """
    dv/dt = (0.04/mV * v**2 + 5 * v + 140*mV - u + I_opsin + I_noise) / ms : volt
    du/dt = 0.02 * (0.2 * v - u) / ms : volt
    dO/dt = alpha_light * L_input(t) * (1.0 - O) - (O / tau_off_val) : 1
    I_opsin = g_max * O * (E_rev - v) : volt
    I_noise : volt
    dCa/dt = -Ca / tau_Ca : 1
    """
    
    eqs_f = eqs.replace("L_input(t)", "light_MSf(t)")
    eqs_r = eqs.replace("L_input(t)", "light_MSr(t)")
    
    G_f = NeuronGroup(1, eqs_f, threshold="v >= 30*mV", reset="v = -65*mV; u += 8*mV; Ca += delta_Ca", method="euler")
    G_r = NeuronGroup(1, eqs_r, threshold="v >= 30*mV", reset="v = -65*mV; u += 8*mV; Ca += delta_Ca", method="euler")
    
    for G in [G_f, G_r]:
        G.v = -65.0 * mV
        G.u = 0.2 * (-65.0) * mV
        G.O = 0.0
        G.Ca = 0.0
        G.I_noise = "1.0*mV * randn()"
        
    spk_f = SpikeMonitor(G_f)
    spk_r = SpikeMonitor(G_r)
    st_f = StateMonitor(G_f, ["v", "O", "Ca"], record=True)
    st_r = StateMonitor(G_r, ["v", "O", "Ca"], record=True)
    
    run(sim_time)
    
    int_ca_f = float(np.trapezoid(st_f.Ca[0], st_f.t / second))
    int_ca_r = float(np.trapezoid(st_r.Ca[0], st_r.t / second))
    
    return {
        "spk_f": spk_f, "spk_r": spk_r,
        "st_f": st_f, "st_r": st_r,
        "int_ca_f": int_ca_f, "int_ca_r": int_ca_r
    }

print("\n" + "="*80)
print("EXECUTANDO EXPERIMENTO 2: COMPARAÇÃO BIOFÍSICA ChR2 (13.0 ms) vs CHRONOS (3.6 ms)")
print("="*80)

print("[1/2] Simulando com Canalrodopsina-2 Wild-Type (tau_off = 13.0 ms)...")
res_chr2 = run_optogenetics(13.0 * ms)

print("[2/2] Simulando com Chronos (tau_off = 3.6 ms)...")
res_chronos = run_optogenetics(3.6 * ms)

# --------------------------------------------------------------------------------------
# 4. QUANTIFICAÇÕES E ANÁLISE COMPARATIVA
# --------------------------------------------------------------------------------------
spk_chr2_f = res_chr2["spk_f"].num_spikes
spk_chr2_r = res_chr2["spk_r"].num_spikes
diff_spk_chr2 = abs(spk_chr2_f - spk_chr2_r) / max(spk_chr2_f, spk_chr2_r) * 100.0
diff_ca_chr2 = abs(res_chr2["int_ca_f"] - res_chr2["int_ca_r"]) / max(res_chr2["int_ca_f"], res_chr2["int_ca_r"]) * 100.0

spk_chronos_f = res_chronos["spk_f"].num_spikes
spk_chronos_r = res_chronos["spk_r"].num_spikes
diff_spk_chronos = abs(spk_chronos_f - spk_chronos_r) / max(spk_chronos_f, spk_chronos_r) * 100.0
diff_ca_chronos = abs(res_chronos["int_ca_f"] - res_chronos["int_ca_r"]) / max(res_chronos["int_ca_f"], res_chronos["int_ca_r"]) * 100.0

# Medições cinéticas da fração aberta O(t) na janela ativa de 140 ms
t_arr = np.array(res_chr2["st_f"].t / ms)
mask_stim1 = (t_arr >= 7.0) & (t_arr <= 140.0)

mean_O_chr2_f = float(np.mean(res_chr2["st_f"].O[0][mask_stim1]))
mean_O_chr2_r = float(np.mean(res_chr2["st_r"].O[0][mask_stim1]))
min_O_chr2_f = float(np.min(res_chr2["st_f"].O[0][mask_stim1]))

mean_O_chronos_f = float(np.mean(res_chronos["st_f"].O[0][mask_stim1]))
mean_O_chronos_r = float(np.mean(res_chronos["st_r"].O[0][mask_stim1]))
min_O_chronos_f = float(np.min(res_chronos["st_f"].O[0][mask_stim1]))

print("\n" + "="*80)
print("DADOS NUMÉRICOS EXTRAÍDOS DA SIMULAÇÃO (EXPERIMENTO 2)")
print("="*80)
print("ChR2 WILD-TYPE (tau_off = 13.0 ms - Costa, 2026 / Grossman et al., 2011):")
print(f"  - Disparos: MSf = {spk_chr2_f} | MSr = {spk_chr2_r} (Diferença: {diff_spk_chr2:.2f}%)")
print(f"  - Fração Aberta O(t) na estimulação: Média MSf = {mean_O_chr2_f:.3f} | Mínimo entre pulsos = {min_O_chr2_f:.3f}")
print(f"  - Integral de Cálcio: MSf = {res_chr2['int_ca_f']:.3f} | MSr = {res_chr2['int_ca_r']:.3f} (Diferença: {diff_ca_chr2:.2f}%)")
print("-"*80)
print("CHRONOS (tau_off = 3.6 ms - Klapoetke et al., 2014):")
print(f"  - Disparos: MSf = {spk_chronos_f} | MSr = {spk_chronos_r} (Diferença: {diff_spk_chronos:.2f}%)")
print(f"  - Fração Aberta O(t) na estimulação: Média MSf = {mean_O_chronos_f:.3f} | Mínimo entre pulsos = {min_O_chronos_f:.3f}")
print(f"  - Integral de Cálcio: MSf = {res_chronos['int_ca_f']:.3f} | MSr = {res_chronos['int_ca_r']:.3f} (Diferença: {diff_ca_chronos:.2f}%)")
print("="*80)

# --------------------------------------------------------------------------------------
# 5. GERAÇÃO DE FIGURA PUBLICÁVEL: 4 LINHAS E 2 COLUNAS (ChR2 vs CHRONOS SEPARADOS)
# --------------------------------------------------------------------------------------
fig, axes = plt.subplots(4, 2, figsize=(11, 11.5), sharey="row", dpi=300)

t_max_zoom = 560.0  # 2 ciclos teta completos (560 ms)
t_pad = 16.0         # Margem de 16 ms na esquerda e na direita (~3% da janela)
mask_plot = t_arr <= t_max_zoom
t_plot = t_arr[mask_plot]

L_plot_msf = np.array([light_MSf(t_val * ms) for t_val in t_plot])
L_plot_msr = np.array([light_MSr(t_val * ms) for t_val in t_plot])

# LINHA 1 (A): TRANSMISSOR (PULSOS DE LASER AZUL)
axes[0, 0].plot(t_plot, L_plot_msf, color="#1F4E79", lw=1.5)
axes[0, 0].set_ylabel("Laser $L(t)$", fontsize=9)
axes[0, 0].set_title("(A) $MS_f$ (microestimulação fixa): Pulsos de Laser", fontsize=10, fontweight="bold")
axes[0, 0].set_xlim(-t_pad, t_max_zoom + t_pad)
axes[0, 0].set_xlabel("Tempo (ms)", fontsize=9)
axes[0, 0].grid(True, linestyle=":", alpha=0.5)

axes[0, 1].plot(t_plot, L_plot_msr, color="#D9534F", lw=1.5)
axes[0, 1].set_title("(A) $MS_r$ (microestimulação aleatória): Pulsos de Laser", fontsize=10, fontweight="bold")
axes[0, 1].set_xlim(-t_pad, t_max_zoom + t_pad)
axes[0, 1].set_xlabel("Tempo (ms)", fontsize=9)
axes[0, 1].grid(True, linestyle=":", alpha=0.5)

axes[0, 0].set_ylim(-0.1, 1.2)
axes[0, 1].set_ylim(-0.1, 1.2)

# LINHA 2 (B): CINÉTICA O(t) DA CANALRODOPSINA-2 (ChR2)
axes[1, 0].plot(t_plot, res_chr2["st_f"].O[0][mask_plot], color="#1F4E79", lw=1.6, label="ChR2 ($O(t)$)")
axes[1, 0].axhline(mean_O_chr2_f, color="#1F4E79", linestyle="--", lw=1.3, alpha=0.85, label=f"$O_{{\\mathrm{{médio}}}} = {mean_O_chr2_f:.3f}$")
axes[1, 0].set_ylabel("Fração $O_{\\mathrm{ChR2}}(t)$", fontsize=9)
axes[1, 0].set_title("(B) Cinética de Deativação ChR2 ($MS_f$, $\\tau_{\\mathrm{off}} = 13{,}0\\ \\mathrm{ms}$)", fontsize=10, fontweight="bold")
axes[1, 0].set_xlim(-t_pad, t_max_zoom + t_pad)
axes[1, 0].set_xlabel("Tempo (ms)", fontsize=9)
axes[1, 0].grid(True, linestyle=":", alpha=0.5)
axes[1, 0].legend(loc="upper center", bbox_to_anchor=(0.5, -0.27), ncol=2, fontsize=8, frameon=True)

axes[1, 1].plot(t_plot, res_chr2["st_r"].O[0][mask_plot], color="#D9534F", lw=1.6, label="ChR2 ($O(t)$)")
axes[1, 1].axhline(mean_O_chr2_r, color="#D9534F", linestyle="--", lw=1.3, alpha=0.85, label=f"$O_{{\\mathrm{{médio}}}} = {mean_O_chr2_r:.3f}$")
axes[1, 1].set_title("(B) Cinética de Deativação ChR2 ($MS_r$, $\\tau_{\\mathrm{off}} = 13{,}0\\ \\mathrm{ms}$)", fontsize=10, fontweight="bold")
axes[1, 1].set_xlim(-t_pad, t_max_zoom + t_pad)
axes[1, 1].set_xlabel("Tempo (ms)", fontsize=9)
axes[1, 1].grid(True, linestyle=":", alpha=0.5)
axes[1, 1].legend(loc="upper center", bbox_to_anchor=(0.5, -0.27), ncol=2, fontsize=8, frameon=True)

axes[1, 0].set_ylim(0.0, 1.15)
axes[1, 1].set_ylim(0.0, 1.15)

# LINHA 3 (C): CINÉTICA O(t) DA OPSINA ULTRARRÁPIDA CHRONOS
axes[2, 0].plot(t_plot, res_chronos["st_f"].O[0][mask_plot], color="#2CA02C", lw=1.6, label="Chronos ($O(t)$)")
axes[2, 0].axhline(mean_O_chronos_f, color="#2CA02C", linestyle="--", lw=1.3, alpha=0.85, label=f"$O_{{\\mathrm{{médio}}}} = {mean_O_chronos_f:.3f}$")
axes[2, 0].set_ylabel("Fração $O_{\\mathrm{Chronos}}(t)$", fontsize=9)
axes[2, 0].set_title("(C) Cinética de Deativação Chronos ($MS_f$, $\\tau_{\\mathrm{off}} = 3{,}6\\ \\mathrm{ms}$)", fontsize=10, fontweight="bold")
axes[2, 0].set_xlim(-t_pad, t_max_zoom + t_pad)
axes[2, 0].set_xlabel("Tempo (ms)", fontsize=9)
axes[2, 0].grid(True, linestyle=":", alpha=0.5)
axes[2, 0].legend(loc="upper center", bbox_to_anchor=(0.5, -0.27), ncol=2, fontsize=8, frameon=True)

axes[2, 1].plot(t_plot, res_chronos["st_r"].O[0][mask_plot], color="#2CA02C", lw=1.6, label="Chronos ($O(t)$)")
axes[2, 1].axhline(mean_O_chronos_r, color="#2CA02C", linestyle="--", lw=1.3, alpha=0.85, label=f"$O_{{\\mathrm{{médio}}}} = {mean_O_chronos_r:.3f}$")
axes[2, 1].set_title("(C) Cinética de Deativação Chronos ($MS_r$, $\\tau_{\\mathrm{off}} = 3{,}6\\ \\mathrm{ms}$)", fontsize=10, fontweight="bold")
axes[2, 1].set_xlim(-t_pad, t_max_zoom + t_pad)
axes[2, 1].set_xlabel("Tempo (ms)", fontsize=9)
axes[2, 1].grid(True, linestyle=":", alpha=0.5)
axes[2, 1].legend(loc="upper center", bbox_to_anchor=(0.5, -0.27), ncol=2, fontsize=8, frameon=True)

axes[2, 0].set_ylim(0.0, 1.15)
axes[2, 1].set_ylim(0.0, 1.15)

# LINHA 4 (D): SENSOR DE CÁLCIO [Ca2+](t) (PROXY DE c-Fos)
axes[3, 0].plot(t_plot, res_chr2["st_f"].Ca[0][mask_plot], color="#1F4E79", lw=1.6, label=f"ChR2 ({res_chr2['int_ca_f']:.1f} u.a.*s)")
axes[3, 0].plot(t_plot, res_chronos["st_f"].Ca[0][mask_plot], color="#2CA02C", lw=1.4, linestyle="--", label=f"Chronos ({res_chronos['int_ca_f']:.1f} u.a.*s)")
axes[3, 0].set_xlabel("Tempo (ms)", fontsize=9)
axes[3, 0].set_ylabel("Cálcio $[\\text{Ca}^{2+}]$ (u.a.)", fontsize=9)
axes[3, 0].set_title("(D) Sensor de Cálcio Intracelular ($MS_f$)", fontsize=10, fontweight="bold")
axes[3, 0].set_xlim(-t_pad, t_max_zoom + t_pad)
axes[3, 0].grid(True, linestyle=":", alpha=0.5)
axes[3, 0].legend(loc="upper center", bbox_to_anchor=(0.5, -0.27), ncol=2, fontsize=8, frameon=True)

axes[3, 1].plot(t_plot, res_chr2["st_r"].Ca[0][mask_plot], color="#D9534F", lw=1.6, label=f"ChR2 ({res_chr2['int_ca_r']:.1f} u.a.*s)")
axes[3, 1].plot(t_plot, res_chronos["st_r"].Ca[0][mask_plot], color="#2CA02C", lw=1.4, linestyle="--", label=f"Chronos ({res_chronos['int_ca_r']:.1f} u.a.*s)")
axes[3, 1].set_xlabel("Tempo (ms)", fontsize=9)
axes[3, 1].set_title("(D) Sensor de Cálcio Intracelular ($MS_r$)", fontsize=10, fontweight="bold")
axes[3, 1].set_xlim(-t_pad, t_max_zoom + t_pad)
axes[3, 1].grid(True, linestyle=":", alpha=0.5)
axes[3, 1].legend(loc="upper center", bbox_to_anchor=(0.5, -0.27), ncol=2, fontsize=8, frameon=True)

max_ca = max(np.max(res_chr2["st_f"].Ca[0][mask_plot]), np.max(res_chr2["st_r"].Ca[0][mask_plot]))
axes[3, 0].set_ylim(0.0, max_ca * 1.25)
axes[3, 1].set_ylim(0.0, max_ca * 1.25)

plt.subplots_adjust(top=0.96, bottom=0.08, left=0.09, right=0.96, hspace=0.68, wspace=0.18)

out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "relatorios", "figuras")
os.makedirs(out_dir, exist_ok=True)
out_file_png = os.path.join(out_dir, "experimento_2_optogenetica_laura_brian2.png")
out_file_pdf = os.path.join(out_dir, "experimento_2_optogenetica_laura_brian2.pdf")

plt.savefig(out_file_png, dpi=300)
plt.savefig(out_file_pdf)

# Salva também como experimento_1_optogenetica para retrocompatibilidade
plt.savefig(os.path.join(out_dir, "experimento_1_optogenetica_laura_brian2.png"), dpi=300)
plt.savefig(os.path.join(out_dir, "experimento_1_optogenetica_laura_brian2.pdf"))

plt.close()
print(f"\n[OK] Gráfico do Experimento 2 salvo com sucesso em:\n  - {out_file_png}\n  - {out_file_pdf}")
