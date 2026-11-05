import os
import glob
import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
import seaborn as sns

out_dir = os.path.dirname(os.path.abspath(__file__))
planilhas_dir = os.path.join(out_dir, 'planilhas') if os.path.exists(os.path.join(out_dir, 'planilhas')) else out_dir
figuras_dir = os.path.join(out_dir, 'figuras')
os.makedirs(figuras_dir, exist_ok=True)
os.makedirs(out_dir, exist_ok=True)

# -------------------------------------------------------------
# 1. ANÁLISE DE HABITUAÇÃO INTER-SESSÕES (TREINO 1 vs TREINO 2 vs TESTE)
# -------------------------------------------------------------
p_treino_c4 = r'D:\NNC\COMPORTAMENTO\Animais serios\#4\#42 Treinamento\results\analysis_results.xlsx'
p_teste_c4 = r'D:\NNC\COMPORTAMENTO\Animais serios\#4\#43 Teste\results\analysis_results-Teste.xlsx'

df_tr4 = pd.read_excel(p_treino_c4)
df_ts4 = pd.read_excel(p_teste_c4).dropna(subset=['animal']).copy()

# Mapear grupos do Lote #4
grupo_map = {
    'cx9a1': 'Controle', 'cx9a2': 'Controle', 'cx10a3': 'Controle',
    'cx9a3': 'Grupo 1', 'cx9a5': 'Grupo 1',
    'cx9a4': 'Grupo 2', 'cx10a2': 'Grupo 2'
}

df_tr4['animal'] = df_tr4['animais'].astype(str).str.strip()
df_tr4['grupo'] = df_tr4['animal'].map(grupo_map)
df_tr4['fase'] = df_tr4['comport'].astype(str).str.strip()

# Criar tabela de medidas repetidas para Lote #4 (t1, t2, tt)
records = []
for an in grupo_map.keys():
    grp = grupo_map[an]
    
    # t1
    r_t1 = df_tr4[(df_tr4['animal'] == an) & (df_tr4['fase'] == 't1')]
    exp_t1 = float(r_t1['exploration_time (s)'].values[0]) if len(r_t1) > 0 else np.nan
    dist_t1 = float(r_t1['total distance (cm)'].values[0]) if len(r_t1) > 0 else np.nan
    vel_t1 = float(r_t1['mean velocity (cm/s)'].values[0]) if len(r_t1) > 0 else np.nan
    
    # t2
    r_t2 = df_tr4[(df_tr4['animal'] == an) & (df_tr4['fase'] == 't2')]
    exp_t2 = float(r_t2['exploration_time (s)'].values[0]) if len(r_t2) > 0 else np.nan
    dist_t2 = float(r_t2['total distance (cm)'].values[0]) if len(r_t2) > 0 else np.nan
    vel_t2 = float(r_t2['mean velocity (cm/s)'].values[0]) if len(r_t2) > 0 else np.nan
    
    # tt (teste)
    r_tt = df_ts4[df_ts4['animal'].astype(str).str.strip() == an]
    exp_tt = float(r_tt['exploration_time (s)'].values[0]) if len(r_tt) > 0 else np.nan
    dist_tt = float(r_tt['total distance (cm)'].values[0]) if len(r_tt) > 0 else np.nan
    vel_tt = float(r_tt['mean velocity (cm/s)'].values[0]) if len(r_tt) > 0 else np.nan
    
    records.append({
        'animal': an, 'grupo': grp,
        'exp_t1': exp_t1, 'exp_t2': exp_t2, 'exp_tt': exp_tt,
        'dist_t1': dist_t1, 'dist_t2': dist_t2, 'dist_tt': dist_tt,
        'vel_t1': vel_t1, 'vel_t2': vel_t2, 'vel_tt': vel_tt
    })

df_hab = pd.DataFrame(records)

print('='*75)
print('1. DINÂMICA DE HABITUAÇÃO TEMPORAL (LOTE #4: t1 -> t2 -> Teste)')
print('='*75)
print(f'N = {len(df_hab)} animais')
print(f'Exploração Média (s):')
print(f'  - Treino 1 (Objeto A): {df_hab["exp_t1"].mean():.2f} +/- {df_hab["exp_t1"].std():.2f} s')
print(f'  - Treino 2 (Objeto B): {df_hab["exp_t2"].mean():.2f} +/- {df_hab["exp_t2"].std():.2f} s')
print(f'  - Teste (A + B):       {df_hab["exp_tt"].mean():.2f} +/- {df_hab["exp_tt"].std():.2f} s')

# Teste t pareado t1 vs t2
t_exp_12 = stats.ttest_rel(df_hab['exp_t1'], df_hab['exp_t2'])
print(f'Comparação t1 vs t2 (Exploração): t = {t_exp_12.statistic:.4f}, p = {t_exp_12.pvalue:.4f}')

# Distância percorrida
print(f'\nDistância Total Média (cm):')
print(f'  - Treino 1: {df_hab["dist_t1"].mean():.1f} +/- {df_hab["dist_t1"].std():.1f} cm')
print(f'  - Treino 2: {df_hab["dist_t2"].mean():.1f} +/- {df_hab["dist_t2"].std():.1f} cm')
print(f'  - Teste:    {df_hab["dist_tt"].mean():.1f} +/- {df_hab["dist_tt"].std():.1f} cm')
t_dist_12 = stats.ttest_rel(df_hab['dist_t1'], df_hab['dist_t2'])
print(f'Comparação t1 vs t2 (Locomoção): t = {t_dist_12.statistic:.4f}, p = {t_dist_12.pvalue:.4f}')

# -------------------------------------------------------------
# 2. ANÁLISE DE TIGMOTAXIA E CINEMÁTICA ESPACIAL VIA DEEPLABCUT
# -------------------------------------------------------------
print('\n' + '='*75)
print('2. ANÁLISE ESPACIAL DE TIGMOTAXIA E FREEZING (CSVs DEEPLABCUT)')
print('='*75)

# Selecionar CSVs de teste do Lote #4
csv_dir = r'D:\NNC\COMPORTAMENTO\Animais serios\#4\#43 Teste\unwanted_files'
csv_files = glob.glob(os.path.join(csv_dir, '*DLC*.csv'))
print(f'CSVs encontrados na pasta de teste do Lote #4: {len(csv_files)}')

spatial_results = []
for cp in csv_files:
    fname = os.path.basename(cp)
    # Extrair ID do animal (ex: cx9a1)
    an_id = fname.split('DLC')[0].split('-')[0].strip()
    if an_id not in grupo_map:
        continue
    grp = grupo_map[an_id]
    
    # Ler coordenadas (usando as primeiras 3 linhas como multi-header)
    df_raw = pd.read_csv(cp, header=[1, 2], nrows=18000) # 10 a 15 min a 30 fps
    
    # Pegar coordenadas do Centro do corpo
    try:
        x = df_raw[('Centro', 'x')].values
        y = df_raw[('Centro', 'y')].values
        p = df_raw[('Centro', 'likelihood')].values
    except KeyError:
        continue
    
    # Filtrar coordenadas válidas (p > 0.6)
    valid_mask = p > 0.6
    x_v = x[valid_mask]
    y_v = y[valid_mask]
    
    if len(x_v) < 100:
        continue
    
    # Normalizar dimensões da arena para [0, 1]
    x_min, x_max = np.percentile(x_v, 1), np.percentile(x_v, 99)
    y_min, y_max = np.percentile(y_v, 1), np.percentile(y_v, 99)
    
    x_norm = (x_v - x_min) / (x_max - x_min + 1e-6)
    y_norm = (y_v - y_min) / (y_max - y_min + 1e-6)
    
    # Definir zona periférica (borda = outer 15% de cada lado)
    # Centro = [0.15, 0.85] em x e y
    is_center = (x_norm >= 0.15) & (x_norm <= 0.85) & (y_norm >= 0.15) & (y_norm <= 0.85)
    pct_center = np.mean(is_center) * 100
    pct_thigmotaxis = 100.0 - pct_center
    
    # Calcular velocidade instantânea frame-a-frame (pixels/frame -> aproximado)
    dx = np.diff(x_v)
    dy = np.diff(y_v)
    disp = np.sqrt(dx**2 + dy**2)
    # Frame rate = 30 fps. Freezing: deslocamento < 1.0 pixel/frame por > 45 frames (1.5 s)
    is_immobile = disp < 1.0
    pct_immobile = np.mean(is_immobile) * 100
    
    spatial_results.append({
        'animal': an_id, 'grupo': grp,
        'pct_tigmotaxia': pct_thigmotaxis,
        'pct_centro': pct_center,
        'pct_imobilidade': pct_immobile,
        'total_frames_validos': len(x_v)
    })

df_spatial = pd.DataFrame(spatial_results)
if len(df_spatial) > 0:
    print(df_spatial[['animal', 'grupo', 'pct_tigmotaxia', 'pct_centro', 'pct_imobilidade']].to_string())
    
    # Estatística por grupo
    print('\nResumo de Tigmotaxia e Imobilidade por Grupo:')
    sp_sum = df_spatial.groupby('grupo').agg(
        N=('animal', 'count'),
        Tigmotaxia_mean=('pct_tigmotaxia', 'mean'),
        Tigmotaxia_std=('pct_tigmotaxia', 'std'),
        Centro_mean=('pct_centro', 'mean'),
        Imobilidade_mean=('pct_imobilidade', 'mean')
    )
    print(sp_sum.to_string())
    
    # ANOVA Tigmotaxia
    g_c = df_spatial[df_spatial['grupo'] == 'Controle']['pct_tigmotaxia']
    g_1 = df_spatial[df_spatial['grupo'] == 'Grupo 1']['pct_tigmotaxia']
    g_2 = df_spatial[df_spatial['grupo'] == 'Grupo 2']['pct_tigmotaxia']
    if len(g_c) > 0 and len(g_1) > 0 and len(g_2) > 0:
        f_tig, p_tig = stats.f_oneway(g_c, g_1, g_2)
        print(f'\nANOVA Tigmotaxia (Bordas vs Centro): F = {f_tig:.4f}, p = {p_tig:.4f}')

# -------------------------------------------------------------
# 3. GERAR PAINEL GRÁFICO CIENTÍFICO CONSOLIDADO
# -------------------------------------------------------------
fig, axes = plt.subplots(1, 3, figsize=(16, 5))

# Plot 1: Curva de Habituacao (t1 -> t2 -> Teste)
ax1 = axes[0]
for idx, row in df_hab.iterrows():
    ax1.plot(['Treino 1 (Obj A)', 'Treino 2 (Obj B)', 'Teste (A + B)'], 
             [row['exp_t1'], row['exp_t2'], row['exp_tt']], 
             marker='o', color='gray', alpha=0.5, lw=1.2)
# Media
means = [df_hab['exp_t1'].mean(), df_hab['exp_t2'].mean(), df_hab['exp_tt'].mean()]
stds = [df_hab['exp_t1'].std(), df_hab['exp_t2'].std(), df_hab['exp_tt'].std()]
ax1.errorbar(['Treino 1 (Obj A)', 'Treino 2 (Obj B)', 'Teste (A + B)'], 
             means, yerr=stds, marker='s', color='darkblue', lw=2.5, capsize=5, label='Média +/- DP')
ax1.set_title(f'Dinâmica de Exploração Inter-Sessões\n(t1 vs t2: p = {t_exp_12.pvalue:.4f})', fontweight='bold')
ax1.set_ylabel('Tempo de Exploração Total (s)', fontweight='bold')
ax1.legend(loc='upper left')

# Plot 2: Distância Total Percorrida Inter-Sessões
ax2 = axes[1]
means_d = [df_hab['dist_t1'].mean(), df_hab['dist_t2'].mean(), df_hab['dist_tt'].mean()]
stds_d = [df_hab['dist_t1'].std(), df_hab['dist_t2'].std(), df_hab['dist_tt'].std()]
ax2.errorbar(['Treino 1', 'Treino 2', 'Teste'], 
             means_d, yerr=stds_d, marker='^', color='darkred', lw=2.5, capsize=5)
ax2.set_title(f'Locomoção Global Inter-Sessões\n(t1 vs t2: p = {t_dist_12.pvalue:.4f})', fontweight='bold')
ax2.set_ylabel('Distância Total (cm)', fontweight='bold')

# Plot 3: Tigmotaxia (% tempo na borda da arena)
ax3 = axes[2]
if len(df_spatial) > 0:
    sns.boxplot(data=df_spatial, x='grupo', y='pct_tigmotaxia', hue='grupo', legend=False, ax=ax3, palette='Set2', boxprops=dict(alpha=0.6))
    sns.stripplot(data=df_spatial, x='grupo', y='pct_tigmotaxia', color='black', size=8, jitter=0.2, ax=ax3)
    ax3.set_title('Tigmotaxia na Fase de Teste\n(% Tempo nas Bordas da Arena)', fontweight='bold')
    ax3.set_ylabel('% Tempo na Borda', fontweight='bold')
    ax3.set_xlabel('Grupo Experimental', fontweight='bold')

plt.tight_layout()
plot_hab = os.path.join(figuras_dir, 'habituação_dinamica_e_tigmotaxia.png')
plt.savefig(plot_hab, dpi=300)
print(f'\nGráfico salvo em: {plot_hab}')

# Salvar planilha consolidada de habituação
out_hab_excel = os.path.join(planilhas_dir, 'analise_habituacao_e_espacial_lote4.xlsx')
with pd.ExcelWriter(out_hab_excel) as writer:
    df_hab.to_excel(writer, sheet_name='Habituacao_Inter_Sessoes', index=False)
    if len(df_spatial) > 0:
        df_spatial.to_excel(writer, sheet_name='Tigmotaxia_DeepLabCut', index=False)
print(f'Planilha salva em: {out_hab_excel}')
