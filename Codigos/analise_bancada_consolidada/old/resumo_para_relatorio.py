import os
import pandas as pd
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt
import seaborn as sns

# Caminhos
base_dir = os.path.dirname(os.path.abspath(__file__))
planilhas_dir = os.path.join(base_dir, 'planilhas') if os.path.exists(os.path.join(base_dir, 'planilhas')) else base_dir
pref_path = os.path.join(planilhas_dir, 'tabela_unificada_testes_de_preferencia.xlsx')
comp_path = os.path.join(planilhas_dir, 'tabela_mestra_comportamento_treino_e_teste.xlsx')

df_pref = pd.read_excel(pref_path)
df_comp = pd.read_excel(comp_path)

print("="*60)
print("1. TESTES DE PREFERÊNCIA DE OBJETOS (ANIMAIS NAIVE, SEM HEADSTAGE)")
print("="*60)

pref_results = []
for code, grp in df_pref.groupby('codigo_teste'):
    mat = grp['tipo_material'].iloc[0]
    obj_l = grp['objeto_esquerda'].iloc[0]
    obj_r = grp['objeto_direita'].iloc[0]
    n = len(grp)
    t_l = grp['tempo_exploracao_esquerda_s'].values
    t_r = grp['tempo_exploracao_direita_s'].values
    di = grp['DI_preferencia'].values
    
    # Teste t pareado entre Objeto Esquerda e Objeto Direita
    t_stat_pair, p_pair = stats.ttest_rel(t_r, t_l)
    # Teste t de uma amostra contra zero no DI
    t_stat_di, p_di = stats.ttest_1samp(di, 0.0)
    
    pref_results.append({
        'codigo': code,
        'material': mat,
        'objeto_esq': obj_l,
        'objeto_dir': obj_r,
        'N': n,
        't_esq_mean': np.mean(t_l),
        't_esq_sem': stats.sem(t_l),
        't_dir_mean': np.mean(t_r),
        't_dir_sem': stats.sem(t_r),
        'di_mean': np.mean(di),
        'di_sem': stats.sem(di),
        'di_std': np.std(di, ddof=1),
        't_stat': t_stat_di,
        'p_value': p_di
    })
    print(f"Teste {code} (N={n}, {mat}):")
    print(f"  {obj_l}: {np.mean(t_l):.2f} +/- {stats.sem(t_l):.2f} s")
    print(f"  {obj_r}: {np.mean(t_r):.2f} +/- {stats.sem(t_r):.2f} s")
    print(f"  DI: {np.mean(di):.4f} +/- {stats.sem(di):.4f} (SD={np.std(di, ddof=1):.4f})")
    print(f"  t({n-1}) = {t_stat_di:.4f}, p = {p_di:.5f}")
    stars = 'ns' if p_di >= 0.05 else ('*' if p_di >= 0.01 else ('**' if p_di >= 0.001 else '***'))
    print(f"  Significância: {stars}\n")

df_pref_summary = pd.DataFrame(pref_results)

print("="*60)
print("2. ANÁLISE DE COMPORTAMENTO: LOTES 2 & 3 (OBJETOS DE VIDRO)")
print("="*60)

# Lotes 2 e 3 na fase de teste
df_test = df_comp[df_comp['tipo_sessao'].str.lower() == 'teste'].copy()
df_lote23 = df_test[df_test['lote'].isin(['#2', '#3'])].copy()
df_lote23['DI'] = (df_lote23['tempo_exploracao_direita_s'] - df_lote23['tempo_exploracao_esquerda_s']) / (
    df_lote23['tempo_exploracao_direita_s'] + df_lote23['tempo_exploracao_esquerda_s'] + 1e-6
)

print(f"Total animais Lotes 2 e 3 em teste: N={len(df_lote23)}")
for grp_name, sub in df_lote23.groupby('grupo_experimental'):
    print(f"  {grp_name} (N={len(sub)}): DI = {sub['DI'].mean():.4f} +/- {sub['DI'].sem():.4f}")

# ANOVA Lotes 2 e 3
f_val23, p_val23 = stats.f_oneway(
    *[sub['DI'].dropna().values for _, sub in df_lote23.groupby('grupo_experimental')]
)
print(f"ANOVA Lotes 2 e 3: F = {f_val23:.4f}, p = {p_val23:.4f}")

print("\n" + "="*60)
print("3. ANÁLISE DE COMPORTAMENTO: LOTE 4 ISOLADO (FRASCOS POLIMÉRICOS / PITCHULINHA)")
print("="*60)

df_lote4 = df_test[df_test['lote'] == '#4'].copy()
df_lote4['DI'] = (df_lote4['tempo_exploracao_direita_s'] - df_lote4['tempo_exploracao_esquerda_s']) / (
    df_lote4['tempo_exploracao_direita_s'] + df_lote4['tempo_exploracao_esquerda_s'] + 1e-6
)

print(f"Total animais Lote 4 em teste: N={len(df_lote4)}")
for grp_name, sub in df_lote4.groupby('grupo_experimental'):
    print(f"  {grp_name} (N={len(sub)}): DI = {sub['DI'].mean():.4f} +/- {sub['DI'].sem():.4f}")

if len(df_lote4['grupo_experimental'].unique()) > 1:
    f_val4, p_val4 = stats.f_oneway(
        *[sub['DI'].dropna().values for _, sub in df_lote4.groupby('grupo_experimental')]
    )
    print(f"ANOVA Lote 4: F = {f_val4:.4f}, p = {p_val4:.4f}")
else:
    print("Apenas um grupo presente no Lote 4.")

print("\n" + "="*60)
print("4. GERAÇÃO DE FIGURAS ESTILO GRAPHPAD PRISM 9")
print("="*60)

# Configuração estética Prism 9
plt.rcParams['font.sans-serif'] = 'Arial'
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['axes.edgecolor'] = '#000000'
plt.rcParams['axes.linewidth'] = 1.2
plt.rcParams['xtick.major.width'] = 1.2
plt.rcParams['ytick.major.width'] = 1.2
plt.rcParams['xtick.direction'] = 'out'
plt.rcParams['ytick.direction'] = 'out'

fig, axes = plt.subplots(1, 2, figsize=(11, 5), dpi=300)

# Painel A: Teste 1 (Impressão 3D vs Frascos Poliméricos Neutros)
ax1 = axes[0]
t1_sub = df_pref[df_pref['codigo_teste'].isin(['Teste 1.1', 'Teste 1.2'])].copy()

# Mapear para nomenclatura científica
name_map = {
    'Teste 1.1': 'Poliácido Láctico (PLA)\nCilindro vs. Pentágono',
    'Teste 1.2': 'Frascos Poliméricos\nÁgua vs. Areia'
}
t1_sub['label'] = t1_sub['codigo_teste'].map(name_map)

codes = ['Teste 1.1', 'Teste 1.2']
x_pos = [0, 1]

for i, code in enumerate(codes):
    sub = t1_sub[t1_sub['codigo_teste'] == code]
    vals = sub['DI_preferencia'].values
    mean_val = np.mean(vals)
    sem_val = stats.sem(vals)
    
    # Barra Prism transparente com borda sólida
    ax1.bar(i, mean_val, width=0.5, color='#E0E4E8', edgecolor='#1F4E79', linewidth=1.5, alpha=0.7, zorder=2)
    # Erro SEM
    ax1.errorbar(i, mean_val, yerr=sem_val, fmt='none', ecolor='#1F4E79', elinewidth=2, capsize=5, capthick=1.5, zorder=3)
    # Scatter individual (jitter)
    np.random.seed(42)
    jitter = np.random.normal(0, 0.05, size=len(vals))
    ax1.scatter(i + jitter, vals, color='#1F4E79', edgecolors='black', linewidth=0.8, s=45, alpha=0.85, zorder=4)

ax1.axhline(0, color='gray', linestyle='--', linewidth=1, zorder=1)
ax1.set_xticks(x_pos)
ax1.set_xticklabels([name_map[c] for c in codes], fontsize=10, fontweight='bold')
ax1.set_ylabel('Índice de Discriminação (DI)', fontsize=11, fontweight='bold')
ax1.set_title('A. Validação Inicial de Objetos (Bateria 1)', fontsize=12, fontweight='bold', pad=12)
ax1.set_ylim(-0.5, 0.7)

# Anotação Prism de asteriscos / ns
# Teste 1.1: p = 0.0579 (ns)
ax1.plot([0, 0], [0.52, 0.55], color='black', lw=1.2)
ax1.plot([0, 0], [0.55, 0.55], color='black', lw=1.2)
ax1.text(0, 0.57, 'ns\np = 0.058', ha='center', va='bottom', fontsize=9, fontweight='bold')

# Teste 1.2: p = 0.787 (ns - perfeitamente neutro)
ax1.plot([1, 1], [0.42, 0.45], color='black', lw=1.2)
ax1.text(1, 0.47, 'ns\np = 0.787', ha='center', va='bottom', fontsize=9, fontweight='bold')

# Painel B: Teste 2 (Impressão 3D vs Frascos de Vidro)
ax2 = axes[1]
t2_sub = df_pref[df_pref['codigo_teste'].isin(['Teste 2.1', 'Teste 2.2'])].copy()
name_map2 = {
    'Teste 2.1': 'Poliácido Láctico (PLA)\nTriângulo vs. Quadrado',
    'Teste 2.2': 'Frascos de Vidro\nCilíndrico vs. Quadrado'
}
t2_sub['label'] = t2_sub['codigo_teste'].map(name_map2)
codes2 = ['Teste 2.1', 'Teste 2.2']

for i, code in enumerate(codes2):
    sub = t2_sub[t2_sub['codigo_teste'] == code]
    vals = sub['DI_preferencia'].values
    mean_val = np.mean(vals)
    sem_val = stats.sem(vals)
    
    # Barra Prism
    color_bar = '#F8D7DA' if code == 'Teste 2.2' else '#E0E4E8'
    edge_bar = '#B02A37' if code == 'Teste 2.2' else '#1F4E79'
    ax2.bar(i, mean_val, width=0.5, color=color_bar, edgecolor=edge_bar, linewidth=1.5, alpha=0.7, zorder=2)
    ax2.errorbar(i, mean_val, yerr=sem_val, fmt='none', ecolor=edge_bar, elinewidth=2, capsize=5, capthick=1.5, zorder=3)
    np.random.seed(42)
    jitter = np.random.normal(0, 0.05, size=len(vals))
    ax2.scatter(i + jitter, vals, color=edge_bar, edgecolors='black', linewidth=0.8, s=45, alpha=0.85, zorder=4)

ax2.axhline(0, color='gray', linestyle='--', linewidth=1, zorder=1)
ax2.set_xticks([0, 1])
ax2.set_xticklabels([name_map2[c] for c in codes2], fontsize=10, fontweight='bold')
ax2.set_ylabel('Índice de Discriminação (DI)', fontsize=11, fontweight='bold')
ax2.set_title('B. Detecção de Viés Inato de Objeto (Bateria 2)', fontsize=12, fontweight='bold', pad=12)
ax2.set_ylim(-0.5, 0.7)

# Anotação Prism de asteriscos
# Teste 2.1: p = 0.0033 (**)
ax2.plot([0, 0], [0.45, 0.48], color='black', lw=1.2)
ax2.text(0, 0.50, '**\np = 0.003', ha='center', va='bottom', fontsize=10, fontweight='bold')

# Teste 2.2: p = 0.0094 (**)
ax2.plot([1, 1], [0.55, 0.58], color='black', lw=1.2)
ax2.text(1, 0.60, '**\np = 0.009', ha='center', va='bottom', fontsize=10, fontweight='bold', color='#B02A37')

sns.despine(fig=fig, top=True, right=True)
plt.tight_layout()

# Salvar figura em pasta acessível
figures_dir = os.path.join(base_dir, 'figuras')
os.makedirs(figures_dir, exist_ok=True)
fig_path = os.path.join(figures_dir, 'figura_1_testes_preferencia_estilo_prism.png')
fig.savefig(fig_path, dpi=300)
plt.close()
print(f"Figura gerada com sucesso: {fig_path}")
