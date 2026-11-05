import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

# -------------------------------------------------------------
# 1. PARÂMETROS TEMPORAIS DA SIMULAÇÃO
# -------------------------------------------------------------
dt = 0.5            # Passo de integração (ms)
T = 300.0           # Tempo total de simulação (ms)Agent

time = np.arange(0, T, dt)
n_steps = len(time)

# Degrau de corrente injetada I(t): liga em 30 ms e vai até 250 ms
def get_stimulus(I_amp):
    I = np.zeros(n_steps)
    I[(time >= 30.0) & (time <= 250.0)] = I_amp
    return I

# -------------------------------------------------------------
# 2. MOTOR DE INTEGRAÇÃO DAS EQUAÇÕES DE IZHIKEVICH (Euler)
# -------------------------------------------------------------
def simulate(a, b, c, d, I_amp):
    v = np.zeros(n_steps)
    u = np.zeros(n_steps)

    # Condições iniciais (repouso biofísico)
    v[0] = -65.0
    u[0] = b * v[0]

    I = get_stimulus(I_amp)

    for t in range(n_steps - 1):
        # Disparo e Chaveamento (Reset não-linear)
        if v[t] >= 30.0:
            v[t] = 30.0     # Trava o gráfico no pico do spike
            v[t + 1] = c
            u[t + 1] = u[t] + d
        else:
            # Integração numérica das duas equações diferenciais
            # dv/dt = 0.04*v^2 + 5*v + 140 - u + I
            v[t + 1] = v[t] + dt * (0.04 * v[t]**2 + 5.0 * v[t] + 140.0 - u[t] + I[t])
            # du/dt = a*(b*v - u)
            u[t + 1] = u[t] + dt * (a * (b * v[t] - u[t]))

    return v, u, I

# -------------------------------------------------------------
# 3. INTERFACE VISUAL INTERATIVA (O SEU "SIMULINK")
# -------------------------------------------------------------
# Valores iniciais: Neurônio Piramidal de CA3 (Regular Spiking)
init_a = 0.02
init_b = 0.20
init_c = -65.0
init_d = 8.0
init_I = 10.0

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 7), sharex=True)
plt.subplots_adjust(left=0.1, bottom=0.35, right=0.9, top=0.92, hspace=0.15)
fig.canvas.manager.set_window_title("Mestrado UFMG - Painel de Controle Izhikevich")

# Simulação inicial
v_init, u_init, I_init = simulate(init_a, init_b, init_c, init_d, init_I)

# Gráfico 1: Tensão de Membrana v(t) - O Osciloscópio
line_v, = ax1.plot(time, v_init, 'b-', lw=1.5, label='Tensão de Membrana v(t) [mV]')
ax1.axhline(30, color='gray', ls='--', alpha=0.5, label='Pico do Spike (+30 mV)')
ax1.axhline(-65, color='gray', ls=':', alpha=0.5, label='Repouso (-65 mV)')
ax1.set_ylabel("Tensão v (mV)", fontweight='bold')
ax1.set_ylim(-90, 45)
ax1.grid(True, alpha=0.3)
ax1.legend(loc='upper right')
ax1.set_title("Osciloscópio de Disparo Neuronal (Modelo de Izhikevich)", fontweight='bold')

# Gráfico 2: Corrente Injetada e Variável de Amortecimento u(t)
line_I, = ax2.plot(time, I_init, 'r--', lw=1.2, label='Corrente Injetada I(t) [pA]')
line_u, = ax2.plot(time, u_init, 'g-', lw=1.2, label='Amortecimento u(t)')
ax2.set_xlabel("Tempo (ms)", fontweight='bold')
ax2.set_ylabel("Corrente / Amortecimento", fontweight='bold')
ax2.set_ylim(-20, 40)
ax2.grid(True, alpha=0.3)
ax2.legend(loc='upper right')

# -------------------------------------------------------------
# 4. CRIAÇÃO DOS SLIDERS (KNOBS DE CONTROLE)
# -------------------------------------------------------------
axcolor = '#e2e8f0'
ax_I = plt.axes([0.15, 0.22, 0.70, 0.025], facecolor=axcolor)
ax_a = plt.axes([0.15, 0.17, 0.70, 0.025], facecolor=axcolor)
ax_b = plt.axes([0.15, 0.12, 0.70, 0.025], facecolor=axcolor)
ax_c = plt.axes([0.15, 0.07, 0.70, 0.025], facecolor=axcolor)
ax_d = plt.axes([0.15, 0.02, 0.70, 0.025], facecolor=axcolor)

s_I = Slider(ax_I, 'Corrente I (pA)', 0.0, 30.0, valinit=init_I, valstep=0.5)
s_a = Slider(ax_a, 'Parâmetro a', 0.005, 0.20, valinit=init_a, valstep=0.005)
s_b = Slider(ax_b, 'Parâmetro b', 0.05, 0.35, valinit=init_b, valstep=0.01)
s_c = Slider(ax_c, 'Reset c (mV)', -80.0, -45.0, valinit=init_c, valstep=1.0)
s_d = Slider(ax_d, 'Reset d', 0.1, 15.0, valinit=init_d, valstep=0.5)

# Função de atualização em tempo real
def update(val):
    a = s_a.val
    b = s_b.val
    c = s_c.val
    d = s_d.val
    I_amp = s_I.val

    v_new, u_new, I_new = simulate(a, b, c, d, I_amp)
    line_v.set_ydata(v_new)
    line_u.set_ydata(u_new)
    line_I.set_ydata(I_new)
    fig.canvas.draw_idle()

s_I.on_changed(update)
s_a.on_changed(update)
s_b.on_changed(update)
s_c.on_changed(update)
s_d.on_changed(update)

plt.show()
