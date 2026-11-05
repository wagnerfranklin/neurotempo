import os
import shutil
import pandas as pd
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt

# Caminhos
base_dir = os.path.dirname(os.path.abspath(__file__))
planilhas_dir = os.path.join(base_dir, 'planilhas') if os.path.exists(os.path.join(base_dir, 'planilhas')) else base_dir
pref_path = os.path.join(planilhas_dir, 'tabela_unificada_testes_de_preferencia.xlsx')
comp_path = os.path.join(planilhas_dir, 'tabela_mestra_comportamento_treino_e_teste.xlsx')
artifact_fig_dir = r'C:\Users\acesso-remoto\.gemini\antigravity\brain\fc783141-8880-43b1-bc52-c353712a58d0\figuras'
local_fig_dir = os.path.join(base_dir, 'figuras')
os.makedirs(local_fig_dir, exist_ok=True)
os.makedirs(artifact_fig_dir, exist_ok=True)

df_pref = pd.read_excel(pref_path)
df_comp = pd.read_excel(comp_path)

# Estilo Prism 9
plt.rcParams['font.sans-serif'] = 'Arial'
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['axes.edgecolor'] = '#111111'
plt.rcParams['axes.linewidth'] = 1.3
plt.rcParams['xtick.major.width'] = 1.3
plt.rcParams['ytick.major.width'] = 1.3
plt.rcParams['xtick.direction'] = 'out'
plt.rcParams['ytick.direction'] = 'out'
plt.rcParams['xtick.major.size'] = 5
plt.rcParams['ytick.major.size'] = 5

# ==============================================================================
# FIGURA 1: TESTE DE PREFERÊNCIA DE OBJETOS (GRAPHPAD PRISM STYLE)
# 4 Painéis comparando Objeto Esquerda vs Objeto Direita em cada sessão
# ==============================================================================
fig, axes = plt.subplots(2, 2, figsize=(10, 8.5), dpi=300)

configs = [
    {
        'ax': axes[0, 0],
        'code': 'Teste 1.1',
        'title': 'A. Teste 1.1: Polímeros 3D (PLA)',
        'obj_names': ('Cilindro PLA', 'Prisma Pentagonal'),
        'color': '#2C3E50',
        'y_max': 95
    },
    {
        'ax': axes[0, 1],
        'code': 'Teste 1.2',
        'title': 'B. Teste 1.2: Frascos PET (Padronizados)',
        'obj_names': ('PET Opaco (Água)', 'PET Translúcido (Areia)'),
        'color': '#16A085',
        'y_max': 95
    },
    {
        'ax': axes[1, 0],
        'code': 'Teste 2.1',
        'title': 'C. Teste 2.1: Polímeros 3D (PLA)',
        'obj_names': ('Prisma Triangular', 'Paralelepípedo PLA'),
        'color': '#2980B9',
        'y_max': 70
    },
    {
        'ax': axes[1, 1],
        'code': 'Teste 2.2',
        'title': 'D. Teste 2.2: Frascos de Vidro Borossilicato',
        'obj_names': ('Vidro Cilíndrico', 'Vidro Prismático'),
        'color': '#C0392B',
        'y_max': 95
    }
]

for cfg in configs:
    ax = cfg['ax']
    sub = df_pref[df_pref['codigo_teste'] == cfg['code']]
    t_l = sub['tempo_exploracao_esquerda_s'].values
    t_r = sub['tempo_exploracao_direita_s'].values
    n = len(sub)
    
    # Teste t pareado
    t_stat, p_val = stats.ttest_rel(t_r, t_l)
    
    # Médias e SEM
    m_l, sem_l = np.mean(t_l), stats.sem(t_l)
    m_r, sem_r = np.mean(t_r), stats.sem(t_r)
    
    # Barras Prism (estilo coluna vazada com borda grossa)
    bar_width = 0.45
    ax.bar(0, m_l, width=bar_width, color=cfg['color'], alpha=0.2, edgecolor=cfg['color'], linewidth=1.8, zorder=2)
    ax.bar(1, m_r, width=bar_width, color=cfg['color'], alpha=0.2, edgecolor=cfg['color'], linewidth=1.8, zorder=2)
    
    # Error bars (Mean + SEM)
    ax.errorbar(0, m_l, yerr=sem_l, fmt='none', ecolor=cfg['color'], elinewidth=2, capsize=6, capthick=1.5, zorder=3)
    ax.errorbar(1, m_r, yerr=sem_r, fmt='none', ecolor=cfg['color'], elinewidth=2, capsize=6, capthick=1.5, zorder=3)
    
    # Linhas conectando pares de cada animal (GraphPad Prism Before-After / Paired style)
    for i in range(n):
        ax.plot([0, 1], [t_l[i], t_r[i]], color='#7F8C8D', alpha=0.45, linewidth=1, zorder=3)
        ax.scatter([0, 1], [t_l[i], t_r[i]], color=cfg['color'], edgecolors='black', linewidth=0.7, s=40, zorder=4)
        
    ax.set_xticks([0, 1])
    ax.set_xticklabels([f"{cfg['obj_names'][0]}", f"{cfg['obj_names'][1]}"], fontsize=10, fontweight='bold')
    ax.set_ylabel('Tempo de Exploração (s)', fontsize=10, fontweight='bold')
    ax.set_title(f"{cfg['title']}\n(N = {n} camundongos naïve)", fontsize=11, fontweight='bold', pad=10)
    ax.set_ylim(0, cfg['y_max'])
    
    # Bracket Prism e Asteriscos
    bracket_y = cfg['y_max'] * 0.88
    tip_len = cfg['y_max'] * 0.03
    ax.plot([0, 0, 1, 1], [bracket_y - tip_len, bracket_y, bracket_y, bracket_y - tip_len], color='black', lw=1.3)
    
    if p_val < 0.001:
        stars = '***'
    elif p_val < 0.01:
        stars = '**'
    elif p_val < 0.05:
        stars = '*'
    else:
        stars = 'ns'
        
    label_text = f"{stars}\np = {p_val:.3f}" if stars != 'ns' else f"ns (p = {p_val:.3f})"
    ax.text(0.5, bracket_y + (cfg['y_max'] * 0.02), label_text, ha='center', va='bottom', fontsize=10, fontweight='bold',
            color='#C0392B' if stars != 'ns' else '#2C3E50')
    
    # Limpeza de espinhas superiores e direitas (Prism standard)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

plt.tight_layout()
fig1_path_local = os.path.join(local_fig_dir, 'figura_1_testes_preferencia_estilo_prism.png')
fig1_path_art = os.path.join(artifact_fig_dir, 'figura_1_testes_preferencia_estilo_prism.png')
fig.savefig(fig1_path_local, dpi=300)
fig.savefig(fig1_path_art, dpi=300)
plt.close(fig)
print(f"Figura 1 salva em:\n  {fig1_path_local}\n  {fig1_path_art}")


# ==============================================================================
# FIGURA 2: COMPORTAMENTO - LOTES 2 & 3 (VIDRO) VS LOTE 4 (PET NEUTRO)
# Painel A: Lotes 2 e 3 (Controle vs G1 vs G2)
# Painel B: Lote 4 (Controle vs G1 vs G2)
# ==============================================================================
fig, axes = plt.subplots(1, 2, figsize=(10, 4.8), dpi=300)

df_test = df_comp[df_comp['tipo_sessao'].str.lower() == 'teste'].copy()
df_test['DI'] = (df_test['tempo_exploracao_direita_s'] - df_test['tempo_exploracao_esquerda_s']) / (
    df_test['tempo_exploracao_direita_s'] + df_test['tempo_exploracao_esquerda_s'] + 1e-6
)

# Painel A: Lotes 2 & 3
ax = axes[0]
sub23 = df_test[df_test['lote'].isin(['#2', '#3'])].copy()
grps = ['Controle', 'Grupo 1', 'Grupo 2']
palette = {'Controle': '#7F8C8D', 'Grupo 1': '#2980B9', 'Grupo 2': '#8E44AD'}

x_coords = [0, 1, 2]
for i, g in enumerate(grps):
    data_g = sub23[sub23['grupo_experimental'] == g]['DI'].values
    m = np.mean(data_g)
    sem = stats.sem(data_g) if len(data_g) > 1 else 0
    
    ax.bar(i, m, width=0.5, color=palette[g], alpha=0.25, edgecolor=palette[g], linewidth=1.8, zorder=2)
    ax.errorbar(i, m, yerr=sem, fmt='none', ecolor=palette[g], elinewidth=2, capsize=6, capthick=1.5, zorder=3)
    
    np.random.seed(10)
    jitter = np.random.normal(0, 0.06, size=len(data_g))
    ax.scatter(i + jitter, data_g, color=palette[g], edgecolors='black', linewidth=0.8, s=45, zorder=4)

ax.axhline(0, color='gray', linestyle='--', linewidth=1, zorder=1)
ax.set_xticks(x_coords)
ax.set_xticklabels([f"Controle\n(N=3)", f"Grupo 1\n(N=4)", f"Grupo 2\n(N=5)"], fontsize=10, fontweight='bold')
ax.set_ylabel('Índice de Discriminação (DI)', fontsize=11, fontweight='bold')
ax.set_title('A. Lotes #2 e #3: Objetos de Vidro\n(Viés Inato Presente, F = 0.70, p = 0.522)', fontsize=11, fontweight='bold', pad=10)
ax.set_ylim(-0.6, 0.8)

# Bracket ns geral
ax.plot([0, 0, 2, 2], [0.65, 0.68, 0.68, 0.65], color='black', lw=1.2)
ax.text(1, 0.70, 'ns (p = 0.522)', ha='center', va='bottom', fontsize=10, fontweight='bold')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

# Painel B: Lote 4
ax2 = axes[1]
sub4 = df_test[df_test['lote'] == '#4'].copy()

for i, g in enumerate(grps):
    data_g = sub4[sub4['grupo_experimental'] == g]['DI'].values
    m = np.mean(data_g)
    sem = stats.sem(data_g) if len(data_g) > 1 else 0
    
    ax2.bar(i, m, width=0.5, color=palette[g], alpha=0.25, edgecolor=palette[g], linewidth=1.8, zorder=2)
    ax2.errorbar(i, m, yerr=sem, fmt='none', ecolor=palette[g], elinewidth=2, capsize=6, capthick=1.5, zorder=3)
    
    np.random.seed(10)
    jitter = np.random.normal(0, 0.06, size=len(data_g))
    ax2.scatter(i + jitter, data_g, color=palette[g], edgecolors='black', linewidth=0.8, s=45, zorder=4)

ax2.axhline(0, color='gray', linestyle='--', linewidth=1, zorder=1)
ax2.set_xticks(x_coords)
ax2.set_xticklabels([f"Controle\n(N=3)", f"Grupo 1\n(N=2)", f"Grupo 2\n(N=2)"], fontsize=10, fontweight='bold')
ax2.set_ylabel('Índice de Discriminação (DI)', fontsize=11, fontweight='bold')
ax2.set_title('B. Lote #4: Frascos PET Neutros\n(Poder Insuficiente, F = 0.39, p = 0.698)', fontsize=11, fontweight='bold', pad=10)
ax2.set_ylim(-0.6, 0.8)

# Bracket ns geral
ax2.plot([0, 0, 2, 2], [0.65, 0.68, 0.68, 0.65], color='black', lw=1.2)
ax2.text(1, 0.70, 'ns (p = 0.698)', ha='center', va='bottom', fontsize=10, fontweight='bold')
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)

plt.tight_layout()
fig2_path_local = os.path.join(local_fig_dir, 'figura_2_comportamento_lotes23_vs_4.png')
fig2_path_art = os.path.join(artifact_fig_dir, 'figura_2_comportamento_lotes23_vs_4.png')
fig.savefig(fig2_path_local, dpi=300)
fig.savefig(fig2_path_art, dpi=300)
plt.close(fig)
print(f"Figura 2 salva em:\n  {fig2_path_local}\n  {fig2_path_art}")
