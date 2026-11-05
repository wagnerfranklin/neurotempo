"""
========================================================================================
MODELO CANÔNICO DO ARTIGO BRIAN 2 (STIMBERG ET AL., 2019 - FIGURA 2)
CASO DE ESTUDO 1: CIRCUITO PILÓRICO (OSCILADOR TRIFÁSICO DE INVERTEBRADO)
Artigo: Stimberg et al. (2019) eLife 8:e47314. DOI: 10.7554/eLife.47314
========================================================================================

TRADUÇÃO PARA ENGENHARIA MECATRÔNICA:
----------------------------------------------------------------------------------------
Este circuito biológico com 3 neurônios (ABPD, LP, PY) funciona exatamente como um:
  >>> OSCILADOR DE ANEL TRIFÁSICO COM CONTROLE AUTOMÁTICO DE GANHO (MALHA FECHADA) <<<

1. O NÓ DE CIRCUITO (Membrana Celular):
   - Capacitância C = 60 pF (a camada de gordura isolante da membrana).
   - O potencial 'v' varia conforme correntes entram e saem (Lei de Kirchhoff das Correntes).
   - A dinâmica não-linear de 'v' usa uma cúbica de FitzHugh-Nagumo/Izhikevich, gerando
     auto-oscilação e disparo contínuo (bursts) sem precisar de clock externo.

2. A MALHA DE CONTROLE HOMEOSTÁTICO (Controle Tipo PI):
   - Cada disparo faz entrar Cálcio (Ca += 0.1). O Cálcio é a INTEGRAL NO TEMPO do disparo.
   - O neurônio tem uma referência (Ca_target).
   - O erro (Ca - Ca_target) ajusta lentamente a variável 'z' (dz/dt = tanh(erro)/tau_z).
   - 'z' modula a condutância 'g' e a corrente 's', estabilizando a frequência de disparo!

3. AS SINAPSES INIBITÓRIAS CRUZADAS (Lógica de Chaveamento em Anel):
   - Os neurônios se inibem mutuamente em sequência:
     ABPD dispara -> inibe LP e PY.
     Quando ABPD cansa -> LP desinibe e dispara -> inibe PY e ABPD.
     Quando LP cansa -> PY desinibe e dispara.
   - O resultado é um ritmo cíclico de 3 fases (como um inversor trifásico de motor!).
========================================================================================
"""

import matplotlib.pyplot as plt
from brian2 import *

# Configura o gerador de código para numpy (evita necessidade do compilador C++)
prefs.codegen.target = 'numpy'

# --------------------------------------------------------------------------------------
# 1. PARÂMETROS FÍSICOS E CONFIGURAÇÃO DA INTEGRAÇÃO
# --------------------------------------------------------------------------------------
defaultclock.dt = 0.04 * ms  # Passo temporal ágil e estável

# Parâmetros de escala de tensão e constantes de tempo (RC)
Delta_T = 17.5 * mV  # Fator de sensibilidade térmica/limiar
v_T = -40 * mV  # Tensão limiar efetiva
tau = 2 * ms  # Constante de tempo da recuperação rápida (u no Izhikevich)
tau_adapt = 0.02 * second  # Adaptação
tau_Ca = 150 * ms  # Drenagem do sensor de cálcio (filtro passa-baixa)
tau_x = 2 * second  # Amortecimento lento
v_r = -68 * mV  # Tensão de repouso (Bateria Thevenin de Potássio)
tau_z = 5 * second  # Constante de tempo da malha de feedback homeostático

# Coeficientes da equação cúbica não-linear (geradora de oscilação e histerese)
a = 1 / Delta_T**3
b = 3 / Delta_T**2
c = 1.2 * nA
d = 2.5 * nA / Delta_T**2
C = 60 * pF  # Capacitor de membrana
S = 2 * nA / Delta_T
G = 28.5 * nS  # Condutância de repouso (1 / R)

# --------------------------------------------------------------------------------------
# 2. EQUAÇÕES DIFERENCIAIS ORDINÁRIAS DOS NEURÔNIOS (EQUAÇÕES DE ESTADO)
# --------------------------------------------------------------------------------------
eqs = """
# Equação da Tensão (Lei de Kirchhoff: C * dv/dt = Soma das Correntes)
dv/dt = (Delta_T*g*(-a*(v - v_T)**3 + b*(v - v_T)**2) + w - x - I_fast - I_slow)/C : volt

# Variável de recuperação rápida 'w' (amortecimento do spike)
dw/dt = (c - d*(v - v_T)**2 - w)/tau : amp

# Variável lenta de acomodação de corrente 'x'
dx/dt = (s*(v - v_r) - x)/tau_x : amp

# Ganhos adaptativos modulados pelo controle de homeostase 'z'
s = S*(1 - tanh(z)) : siemens
g = G*(1 + tanh(z)) : siemens

# Sensor de Cálcio (integrador de disparos com decaimento exponencial)
dCa/dt = -Ca/tau_Ca : 1

# Malha de realimentação homeostática: se Ca != Ca_target, corrige 'z'
dz/dt = tanh(Ca - Ca_target)/tau_z : 1

# Correntes sinápticas de entrada vindas de outros nós
I_fast : amp
I_slow : amp

# Parâmetros individuais de cada neurônio
Ca_target : 1 (constant)
label : integer (constant)
"""

# Identificadores inteiros para os 3 tipos de neurônios
ABPD, LP, PY = 0, 1, 2

# Criamos a população com 3 neurônios usando integração Runge-Kutta de 2ª ordem (rk2)
circuit = NeuronGroup(
    3,
    eqs,
    threshold="v > -20*mV",
    refractory="v > -20*mV",
    reset="Ca += 0.1",  # A cada spike, soma uma gota de cálcio
    method="rk2",
)

# Configuração individual das identidades e setpoints
circuit.label = [ABPD, LP, PY]
circuit.v = v_r  # Inicializa na tensão de repouso (-68 mV)
circuit.w = "-5*nA*rand()"  # Condição inicial randômica para quebrar simetria
circuit.z = "rand()*0.2 - 0.1"
circuit.Ca_target = [0.048, 0.0384, 0.06]  # Setpoint de cada neurônio

# --------------------------------------------------------------------------------------
# 3. CONEXÕES SINÁPTICAS (AS MALHAS DE REALIMENTAÇÃO INIBITÓRIA)
# --------------------------------------------------------------------------------------
# Sinapses Inibitórias Rápidas (Transistores de chaveamento rápido)
s_fast = 0.2 / mV
V_fast = -50 * mV
E_syn = -75 * mV  # Tensão de Nernst reversa inibitória (puxa para baixo de -68mV)

eqs_fast = """
g_fast : siemens (constant)
I_fast_post = g_fast*(v_post - E_syn)/(1+exp(s_fast*(V_fast-v_pre))) : amp (summed)
"""
fast_synapses = Synapses(circuit, circuit, model=eqs_fast)
fast_synapses.connect(
    "label_pre != label_post and not (label_pre == PY and label_post == ABPD)"
)
fast_synapses.g_fast["label_pre == ABPD and label_post == LP"] = 0.015 * uS
fast_synapses.g_fast["label_pre == ABPD and label_post == PY"] = 0.005 * uS
fast_synapses.g_fast["label_pre == LP and label_post == ABPD"] = 0.01 * uS
fast_synapses.g_fast["label_pre == LP and label_post == PY"] = 0.02 * uS
fast_synapses.g_fast["label_pre == PY and label_post == LP"] = 0.005 * uS

# Sinapses Inibitórias Lentas Graduadas (Filtro Passa-Baixa Dinâmico)
s_slow = 1 / mV
V_slow = -55 * mV
k_1 = 1 / ms
eqs_slow = """
k_2 : 1/second (constant)
g_slow : siemens (constant)
I_slow_post = g_slow*m_slow*(v_post-E_syn) : amp (summed)
dm_slow/dt = k_1*(1-m_slow)/(1+exp(s_slow*(V_slow-v_pre))) - k_2*m_slow : 1 (clock-driven)
"""
slow_synapses = Synapses(circuit, circuit, model=eqs_slow, method="exact")
slow_synapses.connect("label_pre == ABPD and label_post != ABPD")
slow_synapses.g_slow["label_post == LP"] = 0.025 * uS
slow_synapses.k_2["label_post == LP"] = 0.03 / ms
slow_synapses.g_slow["label_post == PY"] = 0.015 * uS
slow_synapses.k_2["label_post == PY"] = 0.008 / ms

# --------------------------------------------------------------------------------------
# 4. INSTRUMENTAÇÃO VIRTUAL: MONITORES DE SINAL
# --------------------------------------------------------------------------------------
# No artigo original, eles rodavam 59.5s. Vamos monitorar os sinais nos últimos 3 segundos
# para visualizar a estabilização perfeita do ritmo trifásico!
mon_v = StateMonitor(circuit, ("v", "Ca", "z"), record=True)
mon_spikes = SpikeMonitor(circuit)

print("Iniciando a simulação do circuito no Brian 2...")
# Rodamos uma simulação de 3 segundos para demonstrar o ritmo trifásico com rapidez
run(3 * second, report="text")
print("Simulação concluída com sucesso!")

# --------------------------------------------------------------------------------------
# 5. VISUALIZAÇÃO GRÁFICA DIDÁTICA (PADRÃO ENGENHARIA)
# --------------------------------------------------------------------------------------
fig, (ax1, ax2, ax3) = plt.subplots(
    3, 1, figsize=(12, 8), sharex=True, gridspec_kw={"height_ratios": [3, 1.5, 2]}
)

# Janela de zoom para visualização nítida (últimos 2 segundos da simulação)
t_min = 1 * second
t_mask = mon_v.t >= t_min

time_ms = (mon_v.t[t_mask] - t_min) / ms

# Subplot 1: Osciloscópio das Tensões de Membrana v(t) - O Ritmo Trifásico
ax1.plot(
    time_ms,
    mon_v.v[0][t_mask] / mV,
    color="crimson",
    lw=1.5,
    label="Neurônio ABPD (Marca-passo / Fase 1)",
)
ax1.plot(
    time_ms,
    mon_v.v[1][t_mask] / mV,
    color="dodgerblue",
    lw=1.5,
    label="Neurônio LP (Fase 2)",
)
ax1.plot(
    time_ms,
    mon_v.v[2][t_mask] / mV,
    color="forestgreen",
    lw=1.5,
    label="Neurônio PY (Fase 3)",
)
ax1.axhline(
    -20, color="gray", linestyle="--", alpha=0.6, label="Limiar de Spike (-20 mV)"
)
ax1.set_ylabel("Tensão Vm (mV)", fontsize=11, fontweight="bold")
ax1.set_title(
    "Caso 1 do Artigo Brian 2 (Stimberg et al., 2019): Oscilador Biológico Trifásico de Invertebrado",
    fontsize=13,
    fontweight="bold",
)
ax1.grid(True, linestyle=":", alpha=0.6)
ax1.legend(loc="upper right", framealpha=0.9)

# Subplot 2: Raster Plot de Disparos Digitais
for idx, (label_name, cor) in enumerate(
    [("ABPD", "crimson"), ("LP", "dodgerblue"), ("PY", "forestgreen")]
):
    spike_times = mon_spikes.t[mon_spikes.i == idx]
    spikes_zoom = spike_times[spike_times >= t_min]
    if len(spikes_zoom) > 0:
        ax2.vlines(
            (spikes_zoom - t_min) / ms,
            idx - 0.35,
            idx + 0.35,
            color=cor,
            lw=2,
            label=f"Spikes {label_name}",
        )
ax2.set_yticks([0, 1, 2])
ax2.set_yticklabels(["ABPD", "LP", "PY"], fontweight="bold")
ax2.set_ylabel("Nó / Canal", fontsize=11, fontweight="bold")
ax2.set_title(
    "Diagrama de Estados Lógicos de Disparo (Sequência Cíclica: ABPD -> LP -> PY)",
    fontsize=11,
    fontweight="bold",
)
ax2.grid(True, linestyle=":", alpha=0.6)

# Subplot 3: Variável de Controle Homeostático de Cálcio Ca(t) vs Setpoint
ax3.plot(
    time_ms,
    mon_v.Ca[0][t_mask],
    color="crimson",
    lw=1.5,
    label="Cálcio ABPD (Integral do Disparo)",
)
ax3.plot(time_ms, mon_v.Ca[1][t_mask], color="dodgerblue", lw=1.5, label="Cálcio LP")
ax3.plot(
    time_ms, mon_v.Ca[2][t_mask], color="forestgreen", lw=1.5, label="Cálcio PY"
)
ax3.axhline(
    circuit.Ca_target[0],
    color="crimson",
    linestyle=":",
    alpha=0.7,
    label="Setpoint ABPD",
)
ax3.axhline(
    circuit.Ca_target[1],
    color="dodgerblue",
    linestyle=":",
    alpha=0.7,
    label="Setpoint LP",
)
ax3.axhline(
    circuit.Ca_target[2],
    color="forestgreen",
    linestyle=":",
    alpha=0.7,
    label="Setpoint PY",
)
ax3.set_xlabel(
    "Tempo Relativo na Janela de Análise (ms)", fontsize=11, fontweight="bold"
)
ax3.set_ylabel("Nível de Cálcio [Ca]", fontsize=11, fontweight="bold")
ax3.set_title(
    "Malha de Feedback Homeostático: O Sistema Controla a Frequência em Torno do Setpoint",
    fontsize=11,
    fontweight="bold",
)
ax3.grid(True, linestyle=":", alpha=0.6)
ax3.legend(loc="upper right", framealpha=0.9, ncol=2)

plt.tight_layout()
output_fig = "figura_modelo_pilorico_brian2.png"
plt.savefig(output_fig, dpi=300)
print(f"Gráfico didático de alta resolução salvo com sucesso em: {output_fig}")
