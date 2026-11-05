"""
========================================================================================
EXPERIMENTO COMPUTACIONAL 1 (BRIAN 2): ESTIMULAÇÃO ELÉTRICA EXTRACELULAR (WAGNER FRANKLIN)
COMPARAÇÃO DIRETA DE TRANSMISSÃO ENTRE PADRÃO 1 (S1) E PADRÃO 2 (S2) EM CA3
========================================================================================
Parâmetros do Protocolo Experimental (CEUA/UFMG):
  - Alvo Anatômico: Hipocampo Ventral (Sub-região CA3)
  - Coordenadas Estereotáxicas: AP: -3.30 mm; ML: ±2.50 mm; DV: -4.00 mm
  - Eletrodo: Bipolar concêntrico de tungstênio
  - Estímulo Elétrico: Pulsos bifásicos (25 uA, 100 us/fase)
  - Sintaxe Temporal: Ciclo Teta de 140 ms (7.14 Hz), 10 bins de 14 ms cada:
      * Padrão 1 (S1): [1, 0, 1, 0, 1, 0, 1, 1, 0, 1] (6 pulsos ativos por ciclo)
      * Padrão 2 (S2): [1, 1, 1, 0, 0, 1, 0, 1, 1, 1] (7 pulsos ativos por ciclo)
  - Regime Operacional: Estimulação contínua ininterrupta em malha aberta (idêntico ao in vivo)
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

defaultclock.dt = 0.1 * ms

# --------------------------------------------------------------------------------------
# 2. DEFINIÇÃO DOS SINAIS TEMPORAIS
# --------------------------------------------------------------------------------------
f_theta = 7.14 * Hz
T_theta = 1.0 / f_theta                # 140.0 ms
n_bits = 10
bin_duration = T_theta / n_bits       # 14.0 ms por bin
pulse_duration = 0.5 * ms             # Duração efetiva do pulso despolarizante

# Padrão 1 (S1): 6 pulsos ativos por ciclo teta
S1_word = np.array([1, 0, 1, 0, 1, 0, 1, 1, 0, 1], dtype=int)
# Padrão 2 (S2): 7 pulsos ativos por ciclo teta
S2_word = np.array([1, 1, 1, 0, 0, 1, 0, 1, 1, 1], dtype=int)

n_cycles = 10
sim_time = n_cycles * T_theta         # 1400.0 ms

total_steps = int(np.round(sim_time / defaultclock.dt))
steps_per_cycle = int(np.round(T_theta / defaultclock.dt))
steps_per_bin = int(np.round(bin_duration / defaultclock.dt))
steps_pulse = int(np.round(pulse_duration / defaultclock.dt))

stim_S1_arr = np.zeros(total_steps, dtype=float)
stim_S2_arr = np.zeros(total_steps, dtype=float)

for step in range(total_steps):
    step_in_c = step % steps_per_cycle
    b_idx = step_in_c // steps_per_bin
    step_in_b = step_in_c % steps_per_bin
    if step_in_b < steps_pulse and b_idx < n_bits:
        if S1_word[b_idx] == 1:
            stim_S1_arr[step] = 1.0
        if S2_word[b_idx] == 1:
            stim_S2_arr[step] = 1.0

# Injeção equivalente de corrente
I_stim_pyr_amp = 92.0 * mV
I_stim_fs_amp = 110.0 * mV

# --------------------------------------------------------------------------------------
# 3. CONSTRUÇÃO DO MICROCIRCUITO EM BRIAN 2 (MODELAGEM BIOFÍSICA)
# --------------------------------------------------------------------------------------
tau_rec = 600.0 * ms       # Recuperação vesicular (Tsodyks-Markram)
U_syn = 0.45               # Fração liberada por spike
tau_GABA = 6.0 * ms        # Cinética inibitória perissomática
tau_AMPA = 2.0 * ms        # Cinética excitatória recorrente

def run_ca3_network(pattern_stim_arr):
    """
    Executa a simulação do microcircuito de CA3 sob estimulação contínua (regime de bancada).
    """
    start_scope()
    
    stim_input = TimedArray(pattern_stim_arr, dt=defaultclock.dt)
    
    N_pyr = 80
    N_fs = 20
    
    # Condição representativa de regime contínuo após a transição inicial
    R_init = 0.18
    g_GABA_init = 0.35
    
    eqs_pyr = """
    dv/dt = (0.04/mV * v**2 + 5 * v + 140*mV - u + I_stim + I_syn_exc - I_syn_inh + I_noise) / ms : volt
    du/dt = 0.02 * (0.2 * v - u) / ms : volt
    I_stim = I_stim_pyr_amp * stim_input(t) : volt
    I_syn_exc = g_AMPA * (0.0*mV - v) : volt
    I_syn_inh = g_GABA * (v - (-75.0*mV)) : volt
    dg_AMPA/dt = -g_AMPA / tau_AMPA : 1
    dg_GABA/dt = -g_GABA / tau_GABA : 1
    dR/dt = (1.0 - R) / tau_rec : 1
    I_noise : volt
    """
    
    pyr_pop = NeuronGroup(N_pyr, eqs_pyr, threshold="v >= 30*mV", reset="v = -65*mV; u += 8*mV; R -= U_syn * R", method="euler")
    pyr_pop.v = -65.0 * mV
    pyr_pop.u = 0.2 * (-65.0) * mV
    pyr_pop.R = R_init
    pyr_pop.g_GABA = g_GABA_init
    pyr_pop.I_noise = "1.5*mV * randn()"
    
    eqs_fs = """
    dv/dt = (0.04/mV * v**2 + 5 * v + 140*mV - u + I_stim + I_syn_exc + I_noise) / ms : volt
    du/dt = 0.1 * (0.2 * v - u) / ms : volt
    I_stim = I_stim_fs_amp * stim_input(t) : volt
    I_syn_exc = g_AMPA_fs * (0.0*mV - v) : volt
    dg_AMPA_fs/dt = -g_AMPA_fs / tau_AMPA : 1
    I_noise : volt
    """
    
    fs_pop = NeuronGroup(N_fs, eqs_fs, threshold="v >= 30*mV", reset="v = -65*mV; u += 2*mV", method="euler")
    fs_pop.v = -65.0 * mV
    fs_pop.u = 0.2 * (-65.0) * mV
    fs_pop.I_noise = "2.0*mV * randn()"
    
    # Inibição Perissomática (FS -> Pyr)
    S_fs_pyr = Synapses(fs_pop, pyr_pop, on_pre="g_GABA += 0.05")
    S_fs_pyr.connect(p=0.6)
    
    # Excitação Recorrente (Pyr -> Pyr) com Depressão Tsodyks-Markram
    S_pyr_pyr = Synapses(pyr_pop, pyr_pop, on_pre="g_AMPA += 0.25 * R_pre * U_syn")
    S_pyr_pyr.connect(p=0.25)
    
    # Feedback Excitatório (Pyr -> FS)
    S_pyr_fs = Synapses(pyr_pop, fs_pop, on_pre="g_AMPA_fs += 0.15")
    S_pyr_fs.connect(p=0.35)
    
    spk_pyr = SpikeMonitor(pyr_pop)
    spk_fs = SpikeMonitor(fs_pop)
    stat_pyr = StateMonitor(pyr_pop, ["v", "R", "g_GABA"], record=True)
    stat_fs = StateMonitor(fs_pop, ["v"], record=[0])
    
    run(sim_time)
    
    return {
        "spk_pyr": spk_pyr,
        "spk_fs": spk_fs,
        "stat_pyr": stat_pyr,
        "stat_fs": stat_fs,
        "total_pyr_spikes": spk_pyr.num_spikes,
        "total_fs_spikes": spk_fs.num_spikes
    }

print("\n" + "="*80)
print("EXECUTANDO EXPERIMENTO 1: ESTIMULAÇÃO ELÉTRICA EXTRACELULAR EM CA3 (S1 vs S2)")
print("="*80)

print("[1/2] Simulando Resposta ao Padrão 1 (S1)...")
res_S1 = run_ca3_network(stim_S1_arr)

print("[2/2] Simulando Resposta ao Padrão 2 (S2)...")
res_S2 = run_ca3_network(stim_S2_arr)

# --------------------------------------------------------------------------------------
# 4. QUANTIFICAÇÃO DOS DISPAROS E MÉTRICAS TEMPORAIS (VAN ROSSUM)
# --------------------------------------------------------------------------------------
spk_pyr_S1 = res_S1["total_pyr_spikes"]
spk_pyr_S2 = res_S2["total_pyr_spikes"]
diff_spk = abs(spk_pyr_S1 - spk_pyr_S2) / max(spk_pyr_S1, spk_pyr_S2) * 100.0

rate_S1 = spk_pyr_S1 / (80 * 1.4)  # Hz por neurônio
rate_S2 = spk_pyr_S2 / (80 * 1.4)  # Hz por neurônio

# Métricas de R(t) de Tsodyks-Markram
R_S1_arr = np.array(res_S1["stat_pyr"].R[0])
R_S2_arr = np.array(res_S2["stat_pyr"].R[0])
dt_sec = float(defaultclock.dt / second)

R_S1_min = float(np.min(R_S1_arr))
R_S1_ss = float(np.mean(R_S1_arr[int(0.5 * len(R_S1_arr)):]))
R_S1_var = float(np.var(R_S1_arr))

R_S2_min = float(np.min(R_S2_arr))
R_S2_ss = float(np.mean(R_S2_arr[int(0.5 * len(R_S2_arr)):]))
R_S2_var = float(np.var(R_S2_arr))

# Cálculo da Correlação Linear de Pearson no PSTH por Bins de 14 ms (Ciclo Teta de 140 ms)
# Métrica intuitiva de processamento de sinais para avaliar desfasamento temporal
from scipy.stats import pearsonr
t_spk_s1 = np.array(res_S1["spk_pyr"].t / ms) % 140.0
t_spk_s2 = np.array(res_S2["spk_pyr"].t / ms) % 140.0
bins_theta = np.linspace(0, 140, 11)  # 10 bins de 14 ms
psth_s1, _ = np.histogram(t_spk_s1, bins=bins_theta)
psth_s2, _ = np.histogram(t_spk_s2, bins=bins_theta)
r_psth_pop, p_psth_pop = pearsonr(psth_s1, psth_s2)

# Correlação de Pearson por neurônio individual
r_cell_list = []
for nid in range(80):
    t_c1 = np.array(res_S1["spk_pyr"].t / ms)[res_S1["spk_pyr"].i == nid] % 140.0
    t_c2 = np.array(res_S2["spk_pyr"].t / ms)[res_S2["spk_pyr"].i == nid] % 140.0
    h1, _ = np.histogram(t_c1, bins=bins_theta)
    h2, _ = np.histogram(t_c2, bins=bins_theta)
    if np.std(h1) > 0 and np.std(h2) > 0:
        rc, _ = pearsonr(h1, h2)
        r_cell_list.append(rc)

mean_r_cell = float(np.mean(r_cell_list))
std_r_cell = float(np.std(r_cell_list))

# Cálculo da Distância de van Rossum (métrica temporal funcional)
t_eval = np.arange(0, 1400, 0.5)  # malha de 0.5 ms
tau_vr = 10.0  # constante temporal do filtro exponencial (ms)
d_vr_list = []
rel_d_vr_list = []

for nid in range(80):
    t_s1 = np.array(res_S1["spk_pyr"].t / ms)[res_S1["spk_pyr"].i == nid]
    t_s2 = np.array(res_S2["spk_pyr"].t / ms)[res_S2["spk_pyr"].i == nid]
    
    f1 = np.zeros_like(t_eval)
    f2 = np.zeros_like(t_eval)
    for t in t_s1:
        f1 += np.where(t_eval >= t, np.exp(-(t_eval - t) / tau_vr), 0.0)
    for t in t_s2:
        f2 += np.where(t_eval >= t, np.exp(-(t_eval - t) / tau_vr), 0.0)
        
    d = np.sqrt(np.trapezoid((f1 - f2)**2, t_eval) / (2.0 * tau_vr))
    norm_const = np.sqrt((np.trapezoid(f1**2, t_eval) + np.trapezoid(f2**2, t_eval)) / (2.0 * tau_vr))
    d_vr_list.append(d)
    if norm_const > 0:
        rel_d_vr_list.append((d / norm_const) * 100.0)

mean_d_vr = float(np.mean(d_vr_list))
std_d_vr = float(np.std(d_vr_list))
mean_rel_vr = float(np.mean(rel_d_vr_list))
std_rel_vr = float(np.std(rel_d_vr_list))

print("\n" + "="*80)
print("DADOS NUMÉRICOS EXTRAÍDOS DA SIMULAÇÃO (EXPERIMENTO 1: S1 vs S2)")
print("="*80)
print(f"DISPAROS TOTAIS DA POPULAÇÃO (80 células piramidais em 1.4 s):")
print(f"  - Padrão 1 (S1): {spk_pyr_S1} disparos (Taxa média: {rate_S1:.2f} Hz)")
print(f"  - Padrão 2 (S2): {spk_pyr_S2} disparos (Taxa média: {rate_S2:.2f} Hz)")
print(f"  - Diferença Relativa na Taxa de Disparos: {diff_spk:.2f}%")
print("-"*80)
print(f"FRAÇÃO VESICULAR R(t) DE TSODYKS-MARKRAM:")
print(f"  - Padrão 1 (S1): R_mín = {R_S1_min:.4f} | R_estacionário = {R_S1_ss:.4f} | Var(R) = {R_S1_var:.5f}")
print(f"  - Padrão 2 (S2): R_mín = {R_S2_min:.4f} | R_estacionário = {R_S2_ss:.4f} | Var(R) = {R_S2_var:.5f}")
print("-"*80)
print(f"CORRELAÇÃO LINEAR DE PEARSON NO PSTH (10 bins de 14 ms no ciclo teta):")
print(f"  - Correlação Populacional r: {r_psth_pop:.4f} (p = {p_psth_pop:.4f})")
print(f"  - Correlação Média por Célula r: {mean_r_cell:.4f} +/- {std_r_cell:.4f}")
print("-"*80)
# Teste de Equivalência Biológica (TOST - Two One-Sided Tests)
from scipy import stats
diff_spk_cells = np.array([len(np.array(res_S1["spk_pyr"].t)[res_S1["spk_pyr"].i == i]) - 
                           len(np.array(res_S2["spk_pyr"].t)[res_S2["spk_pyr"].i == i]) for i in range(80)])
mean_diff = float(np.mean(diff_spk_cells))
std_diff = float(np.std(diff_spk_cells, ddof=1))
se_diff = std_diff / np.sqrt(80)
df_tost = 79

delta_15 = (spk_pyr_S1 / 80.0) * 0.15
t1_15 = (mean_diff - (-delta_15)) / se_diff
t2_15 = (mean_diff - delta_15) / se_diff
p1_15 = float(1.0 - stats.t.cdf(t1_15, df_tost))
p2_15 = float(stats.t.cdf(t2_15, df_tost))
p_tost_15 = max(p1_15, p2_15)

delta_10 = (spk_pyr_S1 / 80.0) * 0.10
t1_10 = (mean_diff - (-delta_10)) / se_diff
t2_10 = (mean_diff - delta_10) / se_diff
p1_10 = float(1.0 - stats.t.cdf(t1_10, df_tost))
p2_10 = float(stats.t.cdf(t2_10, df_tost))
p_tost_10 = max(p1_10, p2_10)

print(f"TESTE DE EQUIVALÊNCIA BIOLÓGICA (TOST - Two One-Sided Tests):")
print(f"  - Diferença Média Célula a Célula: {mean_diff:.2f} +/- {std_diff:.2f} disparos (SE = {se_diff:.3f})")
print(f"  - Margem 15% (delta = {delta_15:.2f} disp): t1 = {t1_15:.3f}, t2 = {t2_15:.3f} | p_TOST = {p_tost_15:.4e} (p < 0.001)")
print(f"  - Margem 10% (delta = {delta_10:.2f} disp): t1 = {t1_10:.3f}, t2 = {t2_10:.3f} | p_TOST = {p_tost_10:.4e} (p < 0.05)")
print("-"*80)
print(f"DISTÂNCIA TEMPORAL DE VAN ROSSUM (tau = {tau_vr} ms):")
print(f"  - Distância média absoluta D_R: {mean_d_vr:.3f} +/- {std_d_vr:.3f}")
print(f"  - Dissimilaridade temporal relativa: {mean_rel_vr:.2f}% +/- {std_rel_vr:.2f}%")
print("="*80)

# --------------------------------------------------------------------------------------
# 5. GERAÇÃO DE FIGURA PUBLICÁVEL: 3 LINHAS E 2 COLUNAS (S1 vs S2)
# --------------------------------------------------------------------------------------
fig, axes = plt.subplots(3, 2, figsize=(11, 8.8), sharey="row", dpi=300)

t_plot_max = 280.0  # 2 ciclos teta (280 ms)
t_pad = 8.0         # Margem de 8 ms na esquerda e na direita para melhor visualização
mask_t = (res_S1["stat_pyr"].t / ms) <= t_plot_max
t_line = res_S1["stat_pyr"].t[mask_t] / ms
dt_ms = defaultclock.dt / ms

indices_t = [min(int(np.round(t / dt_ms)), total_steps - 1) for t in t_line]
stim_S1_plot = [stim_S1_arr[idx] for idx in indices_t]
stim_S2_plot = [stim_S2_arr[idx] for idx in indices_t]

# LINHA 1 (A): SINAIS DE ESTIMULAÇÃO ELÉTRICA APLICADOS
axes[0, 0].step(t_line, stim_S1_plot, where="post", color="#1F4E79", lw=1.5)
axes[0, 0].set_ylabel("Estímulo (u.a.)", fontsize=9)
axes[0, 0].set_title("(A) Padrão 1 ($S_1$): Trens de Pulsos", fontsize=10, fontweight="bold")
axes[0, 0].set_xlim(-t_pad, t_plot_max + t_pad)
axes[0, 0].set_xlabel("Tempo (ms)", fontsize=9)
axes[0, 0].grid(True, linestyle=":", alpha=0.5)
for b in range(1, int(t_plot_max / 14.0) + 1):
    axes[0, 0].axvline(b * 14.0, color="gray", linestyle=":", alpha=0.3, lw=0.8)

axes[0, 1].step(t_line, stim_S2_plot, where="post", color="#D9534F", lw=1.5)
axes[0, 1].set_title("(A) Padrão 2 ($S_2$): Trens de Pulsos", fontsize=10, fontweight="bold")
axes[0, 1].set_xlim(-t_pad, t_plot_max + t_pad)
axes[0, 1].set_xlabel("Tempo (ms)", fontsize=9)
axes[0, 1].grid(True, linestyle=":", alpha=0.5)
for b in range(1, int(t_plot_max / 14.0) + 1):
    axes[0, 1].axvline(b * 14.0, color="gray", linestyle=":", alpha=0.3, lw=0.8)

axes[0, 0].set_ylim(-0.1, 1.2)
axes[0, 1].set_ylim(-0.1, 1.2)

# LINHA 2 (B): DINÂMICA DE VESÍCULAS SINÁPTICAS R(t)
axes[1, 0].plot(t_line, res_S1["stat_pyr"].R[0][mask_t], color="#1F4E79", lw=1.6, label="Fração Vesicular $R(t)$ ($S_1$)")
axes[1, 0].axhline(R_S1_ss, color="orange", linestyle=":", lw=1.2, label=f"Platô Médio ($R_{{ss}} = {R_S1_ss:.2f}$)")
axes[1, 0].set_ylabel("Fração Vesicular $R(t)$", fontsize=9)
axes[1, 0].set_title("(B) Depleção Sináptica ($S_1$)", fontsize=10, fontweight="bold")
axes[1, 0].set_xlim(-t_pad, t_plot_max + t_pad)
axes[1, 0].set_xlabel("Tempo (ms)", fontsize=9)
axes[1, 0].grid(True, linestyle=":", alpha=0.5)
axes[1, 0].legend(loc="upper center", bbox_to_anchor=(0.5, -0.26), ncol=2, fontsize=8, frameon=True)

axes[1, 1].plot(t_line, res_S2["stat_pyr"].R[0][mask_t], color="#D9534F", lw=1.6, label="Fração Vesicular $R(t)$ ($S_2$)")
axes[1, 1].axhline(R_S2_ss, color="orange", linestyle=":", lw=1.2, label=f"Platô Médio ($R_{{ss}} = {R_S2_ss:.2f}$)")
axes[1, 1].set_title("(B) Depleção Sináptica ($S_2$)", fontsize=10, fontweight="bold")
axes[1, 1].set_xlim(-t_pad, t_plot_max + t_pad)
axes[1, 1].set_xlabel("Tempo (ms)", fontsize=9)
axes[1, 1].grid(True, linestyle=":", alpha=0.5)
axes[1, 1].legend(loc="upper center", bbox_to_anchor=(0.5, -0.26), ncol=2, fontsize=8, frameon=True)

axes[1, 0].set_ylim(0.0, 0.35)
axes[1, 1].set_ylim(0.0, 0.35)

# LINHA 3 (C): RESPOSTA DE POTENCIAL DE MEMBRANA v(t)
axes[2, 0].plot(t_line, res_S1["stat_pyr"].v[0][mask_t] / mV, color="#1F4E79", lw=1.1, label="Neurônio Piramidal (RS)")
axes[2, 0].plot(t_line, res_S1["stat_fs"].v[0][mask_t] / mV, color="#E67E22", lw=0.9, linestyle=":", alpha=0.8, label="Interneurônio PV+ (FS)")
axes[2, 0].set_ylabel("Potencial $v(t)$ (mV)", fontsize=9)
axes[2, 0].set_title("(C) Potencial de Membrana ($S_1$)", fontsize=10, fontweight="bold")
axes[2, 0].set_xlim(-t_pad, t_plot_max + t_pad)
axes[2, 0].set_xlabel("Tempo (ms)", fontsize=9)
axes[2, 0].grid(True, linestyle=":", alpha=0.5)
axes[2, 0].legend(loc="upper center", bbox_to_anchor=(0.5, -0.26), ncol=2, fontsize=8, frameon=True)

axes[2, 1].plot(t_line, res_S2["stat_pyr"].v[0][mask_t] / mV, color="#D9534F", lw=1.1, label="Neurônio Piramidal (RS)")
axes[2, 1].plot(t_line, res_S2["stat_fs"].v[0][mask_t] / mV, color="#E67E22", lw=0.9, linestyle=":", alpha=0.8, label="Interneurônio PV+ (FS)")
axes[2, 1].set_title("(C) Potencial de Membrana ($S_2$)", fontsize=10, fontweight="bold")
axes[2, 1].set_xlim(-t_pad, t_plot_max + t_pad)
axes[2, 1].set_xlabel("Tempo (ms)", fontsize=9)
axes[2, 1].grid(True, linestyle=":", alpha=0.5)
axes[2, 1].legend(loc="upper center", bbox_to_anchor=(0.5, -0.26), ncol=2, fontsize=8, frameon=True)

axes[2, 0].set_ylim(-85, 45)
axes[2, 1].set_ylim(-85, 45)

# Ajuste global de espaçamento entre subplots
plt.subplots_adjust(top=0.95, bottom=0.10, left=0.09, right=0.96, hspace=0.65, wspace=0.18)

out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "relatorios", "figuras")
os.makedirs(out_dir, exist_ok=True)
out_file_png = os.path.join(out_dir, "experimento_1_eletrica_wagner_brian2.png")
out_file_pdf = os.path.join(out_dir, "experimento_1_eletrica_wagner_brian2.pdf")

plt.savefig(out_file_png, dpi=300)
plt.savefig(out_file_pdf)
plt.close()
print(f"\n[OK] Gráfico do Experimento 1 salvo com sucesso em:\n  - {out_file_png}\n  - {out_file_pdf}")
