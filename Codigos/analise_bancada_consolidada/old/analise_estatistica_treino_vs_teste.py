import os
import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
import seaborn as sns

out_dir = os.path.dirname(os.path.abspath(__file__))
planilhas_dir = os.path.join(out_dir, 'planilhas') if os.path.exists(os.path.join(out_dir, 'planilhas')) else out_dir
os.makedirs(out_dir, exist_ok=True)

# 1. Carregar Tabela Mestra
fn_master = os.path.join(planilhas_dir, 'tabela_mestra_comportamento_treino_e_teste.xlsx')
df = pd.read_excel(fn_master)

# Filtrar subconjunto com ciclo completo (N=11)
df_comp = df[df['ciclo_completo'] == 'Sim'].copy()

# Criar pivots para analise longitudinal (t1, t2, Teste)
piv_exp = df_comp.pivot(index=['animal', 'lote', 'grupo_experimental'], columns='etapa', values='tempo_exploracao_total_s').reset_index()
piv_dist = df_comp.pivot(index=['animal', 'lote', 'grupo_experimental'], columns='etapa', values='distancia_total_cm').reset_index()
piv_vel = df_comp.pivot(index=['animal', 'lote', 'grupo_experimental'], columns='etapa', values='velocidade_media_cms').reset_index()
piv_mov = df_comp.pivot(index=['animal', 'lote', 'grupo_experimental'], columns='etapa', values='tempo_movimento_s').reset_index()
piv_rest = df_comp.pivot(index=['animal', 'lote', 'grupo_experimental'], columns='etapa', values='tempo_repouso_s').reset_index()

# -------------------------------------------------------------
# A. PREFERÊNCIA DE OBJETOS NO TREINAMENTO (Obj A em t1 vs Obj B em t2)
# -------------------------------------------------------------
print('='*75)
print('1. PREFERÊNCIA DE OBJETOS NO TREINAMENTO (COM HEADSTAGE, N=11)')
print('='*75)
exp_a = piv_exp['Treino 1']
exp_b = piv_exp['Treino 2']
exp_teste = piv_exp['Teste']

t_ab = stats.ttest_rel(exp_a, exp_b)
w_ab = stats.wilcoxon(exp_a, exp_b)

print(f'Tempo de Exploração:')
print(f'  - Objeto A (Treino 1): {exp_a.mean():.2f} +/- {exp_a.std():.2f} s')
print(f'  - Objeto B (Treino 2): {exp_b.mean():.2f} +/- {exp_b.std():.2f} s')
print(f'  - Diferença Pareada (B - A): {(exp_b - exp_a).mean():.2f} +/- {(exp_b - exp_a).std():.2f} s')
print(f'  - Teste t pareado (A vs B): t = {t_ab.statistic:.4f}, p = {t_ab.pvalue:.4f}')
print(f'  - Teste de Wilcoxon: W = {w_ab.statistic:.4f}, p = {w_ab.pvalue:.4f}')

# Índice de preferência de objeto no treino: (B - A) / (A + B)
pref_obj_treino = (exp_b - exp_a) / (exp_a + exp_b)
t_pref_obj = stats.ttest_1samp(pref_obj_treino, 0)
print(f'  - Índice de Preferência de Treino [(B - A)/(A + B)]: {pref_obj_treino.mean():.4f} +/- {pref_obj_treino.std():.4f}')
print(f'  - Teste t contra zero: t = {t_pref_obj.statistic:.4f}, p = {t_pref_obj.pvalue:.4f}')

# -------------------------------------------------------------
# B. COMPARAÇÃO TREINAMENTO vs TESTE (HABITUAÇÃO E RECUPERAÇÃO)
# -------------------------------------------------------------
print('\n' + '='*75)
print('2. COMPARAÇÃO TREINAMENTO vs TESTE (EVOLUÇÃO TEMPORAL, N=11)')
print('='*75)
print(f'Exploração Total:')
print(f'  - Média Treino (t1): {exp_a.mean():.2f} s')
print(f'  - Média Treino (t2): {exp_b.mean():.2f} s')
print(f'  - Média Teste (tt):  {exp_teste.mean():.2f} s')

# Treino Médio vs Teste
exp_treino_medio = (exp_a + exp_b) / 2.0
t_tr_vs_ts = stats.ttest_rel(exp_treino_medio, exp_teste)
print(f'  - Treino Médio vs Teste: t = {t_tr_vs_ts.statistic:.4f}, p = {t_tr_vs_ts.pvalue:.4f}')

# ANOVA de Medidas Repetidas (Friedman) entre t1, t2 e Teste
fried_stat, fried_p = stats.friedmanchisquare(exp_a, exp_b, exp_teste)
print(f'  - Teste de Friedman (t1 vs t2 vs Teste): Chi2 = {fried_stat:.4f}, p = {fried_p:.4f}')

# -------------------------------------------------------------
# C. TESTE ESTATÍSTICO NO TESTE: CONTROLE vs G1 vs G2 (N=11 e N=19)
# -------------------------------------------------------------
print('\n' + '='*75)
print('3. TESTE ESTATÍSTICO NO TESTE (CONTROLE vs GRUPO 1 vs GRUPO 2)')
print('='*75)

# Apenas no subconjunto ciclo completo (N=11)
df_ts_comp = df_comp[df_comp['tipo_sessao'] == 'Teste'].copy()
df_ts_comp['DI'] = (df_ts_comp['tempo_exploracao_direita_s'] - df_ts_comp['tempo_exploracao_esquerda_s']) / df_ts_comp['tempo_exploracao_total_s']

g_c_11 = df_ts_comp[df_ts_comp['grupo_experimental'] == 'Controle']['DI']
g_1_11 = df_ts_comp[df_ts_comp['grupo_experimental'] == 'Grupo 1']['DI']
g_2_11 = df_ts_comp[df_ts_comp['grupo_experimental'] == 'Grupo 2']['DI']

f_11, p_11 = stats.f_oneway(g_c_11, g_1_11, g_2_11)
kw_11, kw_p_11 = stats.kruskal(g_c_11, g_1_11, g_2_11)

print('A. Animais com Ciclo Completo (N=11):')
print(f'  - Controle (N={len(g_c_11)}): DI = {g_c_11.mean():.4f} +/- {g_c_11.std():.4f}')
print(f'  - Grupo 1  (N={len(g_1_11)}): DI = {g_1_11.mean():.4f} +/- {g_1_11.std():.4f}')
print(f'  - Grupo 2  (N={len(g_2_11)}): DI = {g_2_11.mean():.4f} +/- {g_2_11.std():.4f}')
print(f'  - ANOVA One-Way (N=11): F = {f_11:.4f}, p = {p_11:.4f}')
print(f'  - Kruskal-Wallis (N=11): H = {kw_11:.4f}, p = {kw_p_11:.4f}')

# No conjunto total com Teste (N=19)
df_ts_all = df[df['tipo_sessao'] == 'Teste'].copy()
df_ts_all['DI'] = (df_ts_all['tempo_exploracao_direita_s'] - df_ts_all['tempo_exploracao_esquerda_s']) / df_ts_all['tempo_exploracao_total_s']

g_c_19 = df_ts_all[df_ts_all['grupo_experimental'] == 'Controle']['DI']
g_1_19 = df_ts_all[df_ts_all['grupo_experimental'] == 'Grupo 1']['DI']
g_2_19 = df_ts_all[df_ts_all['grupo_experimental'] == 'Grupo 2']['DI']

f_19, p_19 = stats.f_oneway(g_c_19, g_1_19, g_2_19)
print('\nB. Animais Totais com Teste (N=19):')
print(f'  - Controle (N={len(g_c_19)}): DI = {g_c_19.mean():.4f} +/- {g_c_19.std():.4f}')
print(f'  - Grupo 1  (N={len(g_1_19)}): DI = {g_1_19.mean():.4f} +/- {g_1_19.std():.4f}')
print(f'  - Grupo 2  (N={len(g_2_19)}): DI = {g_2_19.mean():.4f} +/- {g_2_19.std():.4f}')
print(f'  - ANOVA One-Way (N=19): F = {f_19:.4f}, p = {p_19:.4f}')

# -------------------------------------------------------------
# D. CINEMÁTICA E BALANÇO MOTOR (LOCOMOÇÃO vs REPOUSO vs EXPLORAÇÃO)
# -------------------------------------------------------------
print('\n' + '='*75)
print('4. CINEMÁTICA E BALANÇO MOTOR (TREINO 1 vs TREINO 2 vs TESTE, N=11)')
print('='*75)

for etapa in ['Treino 1', 'Treino 2', 'Teste']:
    sub = df_comp[df_comp['etapa'] == etapa]
    tot_session = sub['tempo_movimento_s'] + sub['tempo_repouso_s']
    pct_mov = (sub['tempo_movimento_s'] / tot_session) * 100
    pct_rest = (sub['tempo_repouso_s'] / tot_session) * 100
    pct_explor_of_moving = (sub['tempo_exploracao_total_s'] / sub['tempo_movimento_s']) * 100
    
    print(f'Etapa [{etapa}]:')
    print(f'  - Distância Total: {sub["distancia_total_cm"].mean():.1f} +/- {sub["distancia_total_cm"].std():.1f} cm')
    print(f'  - Velocidade Média: {sub["velocidade_media_cms"].mean():.2f} +/- {sub["velocidade_media_cms"].std():.2f} cm/s')
    print(f'  - Tempo em Movimento: {sub["tempo_movimento_s"].mean():.1f} s ({pct_mov.mean():.1f}%)')
    print(f'  - Tempo em Repouso:   {sub["tempo_repouso_s"].mean():.1f} s ({pct_rest.mean():.1f}%)')
    print(f'  - Eficiência Exploratória (Explor/Mov): {pct_explor_of_moving.mean():.1f}%')

# -------------------------------------------------------------
# E. GERAR PAINEL GRÁFICO CIENTÍFICO FINAL
# -------------------------------------------------------------
fig, axes = plt.subplots(2, 2, figsize=(15, 11))

# 1. Preferencia A vs B no Treinamento
ax1 = axes[0, 0]
df_tr_plot = pd.DataFrame({
    'Objeto': ['Objeto A (Treino 1)']*len(exp_a) + ['Objeto B (Treino 2)']*len(exp_b),
    'Tempo de Exploração (s)': list(exp_a) + list(exp_b)
})
sns.boxplot(data=df_tr_plot, x='Objeto', y='Tempo de Exploração (s)', hue='Objeto', legend=False, ax=ax1, palette='Blues', boxprops=dict(alpha=0.6))
sns.stripplot(data=df_tr_plot, x='Objeto', y='Tempo de Exploração (s)', color='black', size=8, jitter=0.2, ax=ax1)
ax1.set_title(f'Preferência no Treinamento: Objeto A vs B (N=11)\n(Teste pareado: t = {t_ab.statistic:.2f}, p = {t_ab.pvalue:.4f})', fontweight='bold')

# 2. DI no Teste por Grupo (N=11)
ax2 = axes[0, 1]
sns.boxplot(data=df_ts_comp, x='grupo_experimental', y='DI', hue='grupo_experimental', legend=False, ax=ax2, palette='Set2', boxprops=dict(alpha=0.6))
sns.stripplot(data=df_ts_comp, x='grupo_experimental', y='DI', color='black', size=8, jitter=0.2, ax=ax2)
ax2.axhline(0, color='red', ls='--', alpha=0.7)
ax2.set_title(f'Índice DI no Teste (N=11 Ciclo Completo)\n(ANOVA: F = {f_11:.2f}, p = {p_11:.3f})', fontweight='bold')
ax2.set_ylabel('DI = (Obj B - Obj A) / Total', fontweight='bold')

# 3. Evolução de Distância Total
ax3 = axes[1, 0]
means_d = [piv_dist['Treino 1'].mean(), piv_dist['Treino 2'].mean(), piv_dist['Teste'].mean()]
stds_d = [piv_dist['Treino 1'].std(), piv_dist['Treino 2'].std(), piv_dist['Teste'].std()]
ax3.errorbar(['Treino 1', 'Treino 2', 'Teste'], means_d, yerr=stds_d, marker='s', color='darkred', lw=2.5, capsize=5)
ax3.set_title('Distância Total Percorrida na Arena (N=11)', fontweight='bold')
ax3.set_ylabel('Distância Total (cm)', fontweight='bold')

# 4. Eficiência Exploratória (% Tempo Movimento em Contato com Objeto)
ax4 = axes[1, 1]
eff_t1 = (df_comp[df_comp['etapa'] == 'Treino 1']['tempo_exploracao_total_s'].values / df_comp[df_comp['etapa'] == 'Treino 1']['tempo_movimento_s'].values) * 100
eff_t2 = (df_comp[df_comp['etapa'] == 'Treino 2']['tempo_exploracao_total_s'].values / df_comp[df_comp['etapa'] == 'Treino 2']['tempo_movimento_s'].values) * 100
eff_tt = (df_comp[df_comp['etapa'] == 'Teste']['tempo_exploracao_total_s'].values / df_comp[df_comp['etapa'] == 'Teste']['tempo_movimento_s'].values) * 100
df_eff = pd.DataFrame({
    'Etapa': ['Treino 1']*len(eff_t1) + ['Treino 2']*len(eff_t2) + ['Teste']*len(eff_tt),
    'Eficiência (%)': list(eff_t1) + list(eff_t2) + list(eff_tt)
})
sns.boxplot(data=df_eff, x='Etapa', y='Eficiência (%)', hue='Etapa', legend=False, ax=ax4, palette='Purples', boxprops=dict(alpha=0.6))
sns.stripplot(data=df_eff, x='Etapa', y='Eficiência (%)', color='black', size=8, jitter=0.2, ax=ax4)
ax4.set_title('Eficiência Exploratória (% Tempo Movimento com Objeto)', fontweight='bold')
ax4.set_ylabel('% do Tempo em Movimento', fontweight='bold')

plt.tight_layout()
plot_path = os.path.join(out_dir, 'figuras', 'painel_estatistico_completo_treino_e_teste.png')
plt.savefig(plot_path, dpi=300)
print(f'\nPainel gráfico salvo em: {plot_path}')

# Salvar planilha de dados pareados
piv_exp.to_excel(os.path.join(planilhas_dir, 'dados_pareados_ciclo_completo_11animais.xlsx'), index=False)
print('Tabela de dados pareados salva com sucesso!')
