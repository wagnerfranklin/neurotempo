"""
========================================================================================
BENCHMARK CANÔNICO DE PLASTICIDADE STDP NO BRIAN 2 (SONG & ABBOTT / STIMBERG 2019)
Ponte Neurocomputacional: Como o Hipocampo Grava Memórias via Diferença de Tempo (dt)
========================================================================================

TRADUÇÃO PARA ENGENHARIA MECATRÔNICA:
----------------------------------------------------------------------------------------
1. O NÓ PÓS-SINÁPTICO (Neurônio Leaky Integrate-and-Fire - LIF):
   - É um circuito RC em paralelo com dreno (leak) para o potencial de repouso (El = -70 mV).
   - Equação: C * dv/dt = -g_L*(v - El) + I_syn(t).
   - Constante de tempo tau_m = 20 ms.
   - Quando v(t) atinge o limiar Vt = -54 mV, o circuito "chaveia" um spike digital e reseta
     para Vr = -60 mV.

2. A REGRA DE CONTROLE ADAPTATIVO DE PESOS (STDP - Spike-Timing-Dependent Plasticity):
   - Cada sinapse tem um ganho ajustável 'w' (0 <= w <= gmax).
   - O neurônio mantém dois filtros passa-baixa de memória temporal (traços sinápticos):
     * Apre(t): memoriza quando o pré disparou (decaimento com tau_pre = 20 ms).
     * Apost(t): memoriza quando o pós disparou (decaimento com tau_post = 20 ms).
   - Se o pré disparou logo ANTES do pós (Causalidade positiva):
     w aumenta (Potenciação - LTP): w = clip(w + Apre, 0, gmax).
   - Se o pós disparou ANTES do pré (Sem causalidade):
     w diminui (Depressão - LTD): w = clip(w + Apost, 0, gmax).
========================================================================================
"""

import matplotlib.pyplot as plt
from brian2 import *

# Garante compatibilidade e execução rápida sem exigir compilador C++ externo
prefs.codegen.target = 'numpy'

# 1. Configuração temporal e semente de reprodutibilidade
seed(42)
defaultclock.dt = 0.1 * ms

# 2. Parâmetros Biofísicos / Circuito RC
tau_m = 20 * ms  # Constante de tempo do capacitor de membrana
El = -70 * mV  # Potencial de repouso (Bateria Thevenin)
Vt = -54 * mV  # Limiar de disparo (Threshold do comparador)
Vr = -60 * mV  # Tensão de reset pós-disparo

# Parâmetros da Plasticidade STDP (Ganhos de Aprendizado)
tau_pre = 20 * ms  # Janela temporal de aprendizado pré-sináptico
tau_post = 20 * ms  # Janela temporal de aprendizado pós-sináptico
gmax = 0.06  # Ganho sináptico máximo calibrado para regime de disparo pós-sináptico
dApre = 0.01 * gmax  # Incremento de LTP a cada spike pré
dApost = -dApre * 1.05  # Decremento de LTD (ligeiramente assimétrico para estabilidade)

# 3. Equações de Estado dos Neurônios
# Neurônio pós-sináptico LIF recebendo somatório de correntes sinápticas
eqs_post = """
dv/dt = (El - v)/tau_m + ge*(0*mV - v)/tau_m : volt (unless refractory)
dge/dt = -ge/(5*ms) : 1
"""

# População Pré-sináptica: 100 canais de entrada disparando pulsos de Poisson a 15 Hz
N_inputs = 100
P_pre = PoissonGroup(N_inputs, 15 * Hz)

# População Pós-sináptica: 1 neurônio comparador
P_post = NeuronGroup(
    1,
    eqs_post,
    threshold="v > Vt",
    reset="v = Vr",
    refractory=2 * ms,
    method="euler",
)
P_post.v = El

# 4. Sinapses com Regra STDP
eqs_syn = """
w : 1
dApre/dt = -Apre/tau_pre : 1 (event-driven)
dApost/dt = -Apost/tau_post : 1 (event-driven)
"""

syn = Synapses(
    P_pre,
    P_post,
    model=eqs_syn,
    on_pre="""
    ge_post += w
    Apre += dApre
    w = clip(w + Apost, 0, gmax)
    """,
    on_post="""
    Apost += dApost
    w = clip(w + Apre, 0, gmax)
    """,
)

# Conecta todos os 100 nós de entrada ao neurônio de saída
syn.connect()
# Inicializa os pesos com distribuição randômica uniforme
syn.w = "rand() * gmax"
w_inicial_medio = np.mean(syn.w)

# 5. Instrumentação: Monitores de Estado e Disparos
# Monitora a evolução do peso 'w' de 10 sinapses amostradas a cada 10 ms
mon_syn = StateMonitor(syn, "w", record=[0, 10, 20, 30, 40, 50, 60, 70, 80, 90], dt=10 * ms)
mon_v = StateMonitor(P_post, "v", record=0)
mon_spikes_pre = SpikeMonitor(P_pre)
mon_spikes_post = SpikeMonitor(P_post)

print(f"Peso sináptico médio inicial: {w_inicial_medio:.6f}")
print("Executando a simulação do modelo STDP no Brian 2 (duração: 5 segundos)...")
run(5 * second, report="text")

w_final_medio = np.mean(syn.w)
print(f"Simulação concluída! Peso sináptico médio final: {w_final_medio:.6f}")

# 6. Geração dos Gráficos Acadêmicos
fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(11, 8), gridspec_kw={"height_ratios": [2, 1.5, 2]})

# Painel 1: Janela inicial (primeiros 400 ms) dos spikes pré e pós
t_zoom = 400 * ms
mask_pre = mon_spikes_pre.t < t_zoom
mask_post = mon_spikes_post.t < t_zoom

ax1.scatter(mon_spikes_pre.t[mask_pre] / ms, mon_spikes_pre.i[mask_pre], s=4, color="royalblue", alpha=0.7, label="Spikes Pré-sinápticos (100 entradas)")
if len(mon_spikes_post.t[mask_post]) > 0:
    ax1.scatter(mon_spikes_post.t[mask_post] / ms, [102] * len(mon_spikes_post.t[mask_post]), s=40, color="crimson", marker="|", lw=2, label="Spikes Pós-sinápticos")
ax1.set_xlim(0, t_zoom / ms)
ax1.set_ylim(-2, 105)
ax1.set_ylabel("Índice do Canal", fontsize=10, fontweight="bold")
ax1.set_title("Benchmark STDP Brian 2: Sincronização e Competição Sináptica (Song & Abbott, 2000)", fontsize=12, fontweight="bold")
ax1.grid(True, linestyle=":", alpha=0.5)
ax1.legend(loc="upper right", framealpha=0.9)

# Painel 2: Voltagem do Neurônio Pós-sináptico nos primeiros 400 ms
mask_v = mon_v.t < t_zoom
ax2.plot(mon_v.t[mask_v] / ms, mon_v.v[0][mask_v] / mV, color="darkorange", lw=1.2, label="Tensão Vm(t)")
ax2.axhline(Vt / mV, color="red", linestyle="--", alpha=0.8, label=f"Limiar Vt ({Vt/mV:.0f} mV)")
ax2.axhline(El / mV, color="gray", linestyle=":", alpha=0.7, label=f"Repouso El ({El/mV:.0f} mV)")
ax2.set_xlim(0, t_zoom / ms)
ax2.set_ylabel("Tensão (mV)", fontsize=10, fontweight="bold")
ax2.set_title("Dinâmica de Integração e Reset do Neurônio Comparador", fontsize=11, fontweight="bold")
ax2.grid(True, linestyle=":", alpha=0.5)
ax2.legend(loc="upper right", framealpha=0.9)

# Painel 3: Evolução dos Pesos Sinápticos w(t) ao longo de toda a simulação (0 a 5 s)
for i in range(len(mon_syn.w)):
    ax3.plot(mon_syn.t / second, mon_syn.w[i] / gmax, lw=1.2, alpha=0.85)
ax3.set_xlabel("Tempo de Simulação (s)", fontsize=11, fontweight="bold")
ax3.set_ylabel("Peso Normalizado (w / gmax)", fontsize=10, fontweight="bold")
ax3.set_title("Evolução Temporal dos Pesos STDP: Separação Competitiva (LTP vs LTD)", fontsize=11, fontweight="bold")
ax3.grid(True, linestyle=":", alpha=0.5)

plt.tight_layout()
output_img = "figura_benchmark_stdp_brian2.png"
plt.savefig(output_img, dpi=300)
print(f"Gráfico do benchmark STDP salvo com sucesso em: {output_img}")
