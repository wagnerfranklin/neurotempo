"""
Simulação no Brian 2 do Modelo Leaky Integrate-and-Fire (LIF)
Exporta figuras em alta resolução vetorial (.pdf) e rasterizada (.png)
diretamente para a pasta 'relatorios/figuras/'.
"""

import os
from brian2 import *
import matplotlib.pyplot as plt
import seaborn as sns

# ---------------------------------------------------------------------------
# Definição de Caminhos
# ---------------------------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUT_FIG_DIR = os.path.abspath(os.path.join(BASE_DIR, "..", "..", "relatorios", "figuras"))
LOCAL_FIG_DIR = os.path.join(BASE_DIR, "figuras")

os.makedirs(OUT_FIG_DIR, exist_ok=True)
os.makedirs(LOCAL_FIG_DIR, exist_ok=True)

# Configuração de Estilo Visual
sns.set_theme(style="ticks")
plt.rcParams['font.size'] = 10
plt.rcParams['figure.dpi'] = 300

# ---------------------------------------------------------------------------
# 1. Parâmetros Fisiológicos e Simulação Brian 2
# ---------------------------------------------------------------------------
start_scope()
tau = 20 * ms
E_L = -70 * mV
V_th = -50 * mV
V_reset = -75 * mV
R_m = 20 * Mohm
I_ext = 1.4 * nA

eqs = '''
dv/dt = (-(v - E_L) + R_m * I_ext) / tau : volt (unless refractory)
'''

G = NeuronGroup(1, eqs, threshold='v > V_th', reset='v = V_reset', refractory=3*ms, method='exact')
G.v = E_L

statemon = StateMonitor(G, 'v', record=True)
spikemon = SpikeMonitor(G)

run(150 * ms)

# ---------------------------------------------------------------------------
# 2. Plotagem Científica
# ---------------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(7, 3.2))
ax.plot(statemon.t / ms, statemon.v[0] / mV, color='#1f77b4', lw=1.8, label='$v(t)$')
ax.axhline(V_th / mV, color='#d62728', ls='--', lw=1.2, label='Limiar $V_{th}$')
ax.axhline(E_L / mV, color='gray', ls=':', lw=1.0, label='Repouso $E_L$')

for t_spike in spikemon.t:
    ax.axvline(t_spike / ms, color='#2ca02c', alpha=0.3, ls='-')

ax.set_xlabel('Tempo (ms)')
ax.set_ylabel('Potencial de Membrana (mV)')
ax.set_title('Dinâmica de Potencial Transmembrana e Trens de Disparos (LIF)')
ax.legend(loc='lower right', frameon=True)
sns.despine(ax=ax)
plt.tight_layout()

# ---------------------------------------------------------------------------
# 3. Exportação para Relatórios e Cópia Local
# ---------------------------------------------------------------------------
for folder in [OUT_FIG_DIR, LOCAL_FIG_DIR]:
    plt.savefig(os.path.join(folder, "fig_dinamica_lif.pdf"), bbox_inches='tight')
    plt.savefig(os.path.join(folder, "fig_dinamica_lif.png"), dpi=300, bbox_inches='tight')

plt.close(fig)
print(f"[OK] Figuras da simulação LIF salvas em:\n - {OUT_FIG_DIR}\n - {LOCAL_FIG_DIR}")
