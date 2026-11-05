import os
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

# -------------------------------------------------------------------------
# 1. CARREGAR E UNIFICAR OS 4 TESTES DE PREFERÊNCIA
# -------------------------------------------------------------------------
p_t1_1 = r'D:\NNC\COMPORTAMENTO\Animais serios\Teste de preferencia\#2 Teste 1\#22 Teste\#t1\results\analysis_results.xlsx'
p_t1_2 = r'D:\NNC\COMPORTAMENTO\Animais serios\Teste de preferencia\#2 Teste 1\#22 Teste\#t2\results\analysis_results-t2.xlsx'
p_t2 = r'D:\NNC\COMPORTAMENTO\Animais serios\Teste de preferencia\#3 Teste 2\#32 Teste\results\analysis_results-teste3.xlsx'

df_raw_11 = pd.read_excel(p_t1_1)
df_raw_12 = pd.read_excel(p_t1_2)
df_raw_2 = pd.read_excel(p_t2)

records = []

# --- TESTE 1.1: 3D Impresso (Círculo vs Pentágono) ---
for _, r in df_raw_11.iterrows():
    an = str(r.iloc[0]).split('-')[0].strip()
    exp_tot = float(r['exploration_time (s)'])
    exp_r = float(r['exploration_time_right (s)'])
    exp_l = float(r['exploration_time_left (s)'])
    di = (exp_r - exp_l) / exp_tot if exp_tot > 0 else 0
    records.append({
        'codigo_teste': 'Teste 1.1',
        'categoria_objeto': '3D Impresso',
        'tipo_material': 'Polímero 3D (PLA/Resina)',
        'animal': an,
        'objeto_esquerda': 'Círculo Extrudado 3D',
        'objeto_direita': 'Pentágono Extrudado 3D',
        'conteudo_esquerda': 'Maciço (Infill 3D)',
        'conteudo_direita': 'Maciço (Infill 3D)',
        'tempo_exploracao_total_s': exp_tot,
        'tempo_exploracao_esquerda_s': exp_l,
        'tempo_exploracao_direita_s': exp_r,
        'tempo_movimento_s': float(r['time moving (S)']),
        'tempo_repouso_s': float(r['time resting (S)']),
        'distancia_total_cm': float(r['total distance (cm)']),
        'velocidade_media_cms': float(r['mean velocity (cm/s)']),
        'DI_preferencia': di,
        'pct_direita': (exp_r / exp_tot) * 100 if exp_tot > 0 else 50
    })

# --- TESTE 1.2: Plástico Pitchulinha (Tampa Vermelha vs Tampa Branca) ---
for _, r in df_raw_12.iterrows():
    an = str(r.iloc[0]).split('-')[0].strip()
    exp_tot = float(r['exploration_time (s)'])
    exp_r = float(r['exploration_time_right (s)'])
    exp_l = float(r['exploration_time_left (s)'])
    di = (exp_r - exp_l) / exp_tot if exp_tot > 0 else 0
    records.append({
        'codigo_teste': 'Teste 1.2',
        'categoria_objeto': 'Real Físico',
        'tipo_material': 'Plástico (Pitchulinha)',
        'animal': an,
        'objeto_esquerda': 'Frasco Plástico Tampa Branca (Opaco)',
        'objeto_direita': 'Frasco Plástico Tampa Vermelha (Translúcido)',
        'conteudo_esquerda': 'Água',
        'conteudo_direita': 'Areia',
        'tempo_exploracao_total_s': exp_tot,
        'tempo_exploracao_esquerda_s': exp_l,
        'tempo_exploracao_direita_s': exp_r,
        'tempo_movimento_s': float(r['time moving (S)']),
        'tempo_repouso_s': float(r['time resting (S)']),
        'distancia_total_cm': float(r['total distance (cm)']),
        'velocidade_media_cms': float(r['mean velocity (cm/s)']),
        'DI_preferencia': di,
        'pct_direita': (exp_r / exp_tot) * 100 if exp_tot > 0 else 50
    })

# --- TESTE 2.1 (3D Triângulo vs Quadrado) & TESTE 2.2 (Vidro Roxo vs Quadrado Transparente) ---
for _, r in df_raw_2.iterrows():
    an = str(r['animal']).strip()
    teste_flag = str(r['teste']).strip()
    exp_tot = float(r['exploration_time (s)'])
    exp_r = float(r['exploration_time_right (s)'])
    exp_l = float(r['exploration_time_left (s)'])
    di = (exp_r - exp_l) / exp_tot if exp_tot > 0 else 0
    
    if teste_flag == 't1':
        cod = 'Teste 2.1'
        cat = '3D Impresso'
        mat = 'Polímero 3D (PLA/Resina)'
        obj_l = 'Prisma Triangular Extrudado 3D'
        obj_r = 'Prisma Quadrado Extrudado 3D'
        cont_l = 'Maciço (Infill 3D)'
        cont_r = 'Maciço (Infill 3D)'
    else: # t2 ou t2r
        cod = 'Teste 2.2'
        cat = 'Real Físico'
        mat = 'Vidro'
        obj_l = 'Garrafa Vidro Cilíndrica Roxa'
        obj_r = 'Garrafa Vidro Quadrada Transparente'
        cont_l = 'Água'
        cont_r = 'Areia'
    
    records.append({
        'codigo_teste': cod,
        'categoria_objeto': cat,
        'tipo_material': mat,
        'animal': an if teste_flag != 't2r' else f'{an}_repeticao',
        'objeto_esquerda': obj_l,
        'objeto_direita': obj_r,
        'conteudo_esquerda': cont_l,
        'conteudo_direita': cont_r,
        'tempo_exploracao_total_s': exp_tot,
        'tempo_exploracao_esquerda_s': exp_l,
        'tempo_exploracao_direita_s': exp_r,
        'tempo_movimento_s': float(r['time moving (S)']),
        'tempo_repouso_s': float(r['time resting (S)']),
        'distancia_total_cm': float(r['total distance (cm)']),
        'velocidade_media_cms': float(r['mean velocity (cm/s)']),
        'DI_preferencia': di,
        'pct_direita': (exp_r / exp_tot) * 100 if exp_tot > 0 else 50
    })

df_unificado = pd.DataFrame(records)

# Salvar planilha unificada
fn_out_excel = os.path.join(planilhas_dir, 'tabela_unificada_testes_de_preferencia.xlsx')
df_unificado.to_excel(fn_out_excel, index=False)
print(f'Planilha unificada salva em: {fn_out_excel}')
print(f'Total de observações consolidadas: {len(df_unificado)}')
print(df_unificado['codigo_teste'].value_counts())

# -------------------------------------------------------------------------
# 2. ANÁLISE ESTATÍSTICA DE PREFERÊNCIA INTRÍNSECA (DI CONTRA ZERO)
# -------------------------------------------------------------------------
print('\n' + '='*75)
print('1. TESTE DE PREFERÊNCIA INTRÍNSECA POR TESTE (DI contra ZERO)')
print('='*75)

# Filtrar repetições para manter N=10 pareado por teste
df_clean = df_unificado[~df_unificado['animal'].str.contains('repeticao')].copy()

testes = ['Teste 1.1', 'Teste 1.2', 'Teste 2.1', 'Teste 2.2']
pref_summary = []

for t_nome in testes:
    sub = df_clean[df_clean['codigo_teste'] == t_nome]
    t_stat, p_val = stats.ttest_1samp(sub['DI_preferencia'], 0)
    w_stat, w_pval = stats.wilcoxon(sub['DI_preferencia'])
    
    mat = sub['tipo_material'].iloc[0]
    cat = sub['categoria_objeto'].iloc[0]
    obj_l = sub['objeto_esquerda'].iloc[0]
    obj_r = sub['objeto_direita'].iloc[0]
    
    print(f'[{t_nome}] Material: {mat} ({cat})')
    print(f'  Esquerda: {obj_l} | Direita: {obj_r}')
    print(f'  N = {len(sub)}')
    print(f'  Exploração Total: {sub["tempo_exploracao_total_s"].mean():.2f} +/- {sub["tempo_exploracao_total_s"].std():.2f} s')
    print(f'  DI Médio: {sub["DI_preferencia"].mean():.4f} +/- {sub["DI_preferencia"].std():.4f}')
    print(f'  % Direita: {sub["pct_direita"].mean():.2f}% +/- {sub["pct_direita"].std():.2f}%')
    print(f'  Teste t contra 0: t = {t_stat:.4f}, p = {p_val:.4f}')
    print(f'  Wilcoxon: W = {w_stat:.4f}, p = {w_pval:.4f}')
    print('-'*50)
    
    pref_summary.append({
        'Teste': t_nome, 'Categoria': cat, 'Material': mat,
        'N': len(sub),
        'Exploracao_Media_s': sub['tempo_exploracao_total_s'].mean(),
        'DI_Medio': sub['DI_preferencia'].mean(),
        'DI_DP': sub['DI_preferencia'].std(),
        'Pct_Direita': sub['pct_direita'].mean(),
        't_stat': t_stat, 'p_valor': p_val, 'Wilcoxon_p': w_pval
    })

df_pref_sum = pd.DataFrame(pref_summary)

# -------------------------------------------------------------------------
# 3. COMPARAÇÕES CONCORRENTES: 3D vs REAIS | VIDRO vs PLÁSTICO
# -------------------------------------------------------------------------
print('\n' + '='*75)
print('2. COMPARAÇÕES DIRETAS ENTRE TIPOS DE OBJETOS')
print('='*75)

# A. 3D (1.1) vs 3D (2.1)
di_3d_1 = df_clean[df_clean['codigo_teste'] == 'Teste 1.1']['DI_preferencia'].values
di_3d_2 = df_clean[df_clean['codigo_teste'] == 'Teste 2.1']['DI_preferencia'].values
t_3d_comp = stats.ttest_rel(di_3d_1, di_3d_2)
print(f'A. Comparação entre os dois testes 3D (Teste 1.1 vs Teste 2.1):')
print(f'  - DI 1.1: {di_3d_1.mean():.4f} | DI 2.1: {di_3d_2.mean():.4f}')
print(f'  - Teste t pareado: t = {t_3d_comp.statistic:.4f}, p = {t_3d_comp.pvalue:.4f}')

# B. Objetos Reais: Plástico (1.2) vs Vidro (2.2)
di_plast = df_clean[df_clean['codigo_teste'] == 'Teste 1.2']['DI_preferencia'].values
di_vidro = df_clean[df_clean['codigo_teste'] == 'Teste 2.2']['DI_preferencia'].values
t_real_comp = stats.ttest_rel(di_plast, di_vidro)
print(f'\nB. Comparação entre Objetos Reais (Plástico [1.2] vs Vidro [2.2]):')
print(f'  - DI Plástico: {di_plast.mean():.4f} | DI Vidro: {di_vidro.mean():.4f}')
print(f'  - Teste t pareado: t = {t_real_comp.statistic:.4f}, p = {t_real_comp.pvalue:.4f}')

# C. Global: 3D Impressos vs Objetos Reais (Exploração Total e DI)
exp_3d = df_clean[df_clean['categoria_objeto'] == '3D Impresso']['tempo_exploracao_total_s']
exp_real = df_clean[df_clean['categoria_objeto'] == 'Real Físico']['tempo_exploracao_total_s']
t_exp_glob = stats.ttest_ind(exp_3d, exp_real)

di_3d_glob = df_clean[df_clean['categoria_objeto'] == '3D Impresso']['DI_preferencia']
di_real_glob = df_clean[df_clean['categoria_objeto'] == 'Real Físico']['DI_preferencia']
t_di_glob = stats.ttest_ind(di_3d_glob, di_real_glob)

print(f'\nC. Global: 3D Impressos (N={len(exp_3d)}) vs Objetos Reais (N={len(exp_real)}):')
print(f'  - Exploração Total: 3D = {exp_3d.mean():.2f} +/- {exp_3d.std():.2f} s | Reais = {exp_real.mean():.2f} +/- {exp_real.std():.2f} s')
print(f'  - Teste t: t = {t_exp_glob.statistic:.4f}, p = {t_exp_glob.pvalue:.4f}')
print(f'  - DI Médio: 3D = {di_3d_glob.mean():.4f} | Reais = {di_real_glob.mean():.4f}')
print(f'  - Teste t: t = {t_di_glob.statistic:.4f}, p = {t_di_glob.pvalue:.4f}')

# -------------------------------------------------------------------------
# 4. COMPARAÇÃO DE CINEMÁTICA E MOVIMENTO ENTRE OS 4 TESTES
# -------------------------------------------------------------------------
print('\n' + '='*75)
print('3. CINEMÁTICA E LOCOMOÇÃO ENTRE OS 4 TESTES')
print('='*75)

# ANOVA entre os 4 testes para velocidade e distancia
vel_11 = df_clean[df_clean['codigo_teste'] == 'Teste 1.1']['velocidade_media_cms']
vel_12 = df_clean[df_clean['codigo_teste'] == 'Teste 1.2']['velocidade_media_cms']
vel_21 = df_clean[df_clean['codigo_teste'] == 'Teste 2.1']['velocidade_media_cms']
vel_22 = df_clean[df_clean['codigo_teste'] == 'Teste 2.2']['velocidade_media_cms']
f_vel, p_vel = stats.f_oneway(vel_11, vel_12, vel_21, vel_22)

dist_11 = df_clean[df_clean['codigo_teste'] == 'Teste 1.1']['distancia_total_cm']
dist_12 = df_clean[df_clean['codigo_teste'] == 'Teste 1.2']['distancia_total_cm']
dist_21 = df_clean[df_clean['codigo_teste'] == 'Teste 2.1']['distancia_total_cm']
dist_22 = df_clean[df_clean['codigo_teste'] == 'Teste 2.2']['distancia_total_cm']
f_dist, p_dist = stats.f_oneway(dist_11, dist_12, dist_21, dist_22)

print(f'Velocidade Média (cm/s):')
print(f'  - Teste 1.1 (3D Círculo/Pentágono):   {vel_11.mean():.2f} +/- {vel_11.std():.2f}')
print(f'  - Teste 1.2 (Plástico Pitchulinha):   {vel_12.mean():.2f} +/- {vel_12.std():.2f}')
print(f'  - Teste 2.1 (3D Triângulo/Quadrado):  {vel_21.mean():.2f} +/- {vel_21.std():.2f}')
print(f'  - Teste 2.2 (Vidro Roxo/Quadrado):    {vel_22.mean():.2f} +/- {vel_22.std():.2f}')
print(f'  - ANOVA Velocidade: F = {f_vel:.4f}, p = {p_vel:.4f}')
print(f'  - ANOVA Distância:  F = {f_dist:.4f}, p = {p_dist:.4f}')

# -------------------------------------------------------------------------
# 5. GERAR PAINEL GRÁFICO CIENTÍFICO CONSOLIDADO DOS TESTES DE PREFERÊNCIA
# -------------------------------------------------------------------------
fig, axes = plt.subplots(2, 2, figsize=(16, 11))

# Plot 1: DIs dos 4 Testes
ax1 = axes[0, 0]
sns.boxplot(data=df_clean, x='codigo_teste', y='DI_preferencia', hue='codigo_teste', legend=False, ax=ax1, palette='Set2', boxprops=dict(alpha=0.6))
sns.stripplot(data=df_clean, x='codigo_teste', y='DI_preferencia', color='black', size=8, jitter=0.2, ax=ax1)
ax1.axhline(0, color='red', ls='--', alpha=0.7)
ax1.set_title('Preferência Espontânea de Objetos (DI = [Dir - Esq] / Total)', fontweight='bold')
ax1.set_ylabel('Índice DI', fontweight='bold')
ax1.set_xlabel('Teste de Preferência', fontweight='bold')

# Plot 2: Tempo de Exploração Total nos 4 Testes
ax2 = axes[0, 1]
sns.boxplot(data=df_clean, x='codigo_teste', y='tempo_exploracao_total_s', hue='codigo_teste', legend=False, ax=ax2, palette='Blues', boxprops=dict(alpha=0.6))
sns.stripplot(data=df_clean, x='codigo_teste', y='tempo_exploracao_total_s', color='black', size=8, jitter=0.2, ax=ax2)
ax2.set_title('Tempo de Exploração Total (s)', fontweight='bold')
ax2.set_ylabel('Tempo (s)', fontweight='bold')
ax2.set_xlabel('Teste de Preferência', fontweight='bold')

# Plot 3: Velocidade Média de Locomoção nos 4 Testes
ax3 = axes[1, 0]
sns.boxplot(data=df_clean, x='codigo_teste', y='velocidade_media_cms', hue='codigo_teste', legend=False, ax=ax3, palette='Oranges', boxprops=dict(alpha=0.6))
sns.stripplot(data=df_clean, x='codigo_teste', y='velocidade_media_cms', color='black', size=8, jitter=0.2, ax=ax3)
ax3.set_title('Velocidade Média de Locomoção (cm/s)', fontweight='bold')
ax3.set_ylabel('Velocidade (cm/s)', fontweight='bold')
ax3.set_xlabel('Teste de Preferência', fontweight='bold')

# Plot 4: Distância Total Percorrida na Arena
ax4 = axes[1, 1]
sns.boxplot(data=df_clean, x='codigo_teste', y='distancia_total_cm', hue='codigo_teste', legend=False, ax=ax4, palette='Purples', boxprops=dict(alpha=0.6))
sns.stripplot(data=df_clean, x='codigo_teste', y='distancia_total_cm', color='black', size=8, jitter=0.2, ax=ax4)
ax4.set_title('Distância Total Percorrida (cm)', fontweight='bold')
ax4.set_ylabel('Distância (cm)', fontweight='bold')
ax4.set_xlabel('Teste de Preferência', fontweight='bold')

plt.tight_layout()
plot_pref_out = os.path.join(figuras_dir, 'painel_testes_preferencia_4condicoes.png')
plt.savefig(plot_pref_out, dpi=300)
print(f'\nPainel gráfico salvo em: {plot_pref_out}')
