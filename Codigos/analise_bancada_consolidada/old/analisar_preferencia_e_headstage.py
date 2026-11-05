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

# -------------------------------------------------------------
# 1. CARREGAR TESTES DE PREFERÊNCIA (SEM CIRURGIA / SEM HEADSTAGE)
# -------------------------------------------------------------
p_t1 = r'D:\NNC\COMPORTAMENTO\Animais serios\Teste de preferencia\#2 Teste 1\#22 Teste\#t1\results\analysis_results.xlsx'
p_t2 = r'D:\NNC\COMPORTAMENTO\Animais serios\Teste de preferencia\#2 Teste 1\#22 Teste\#t2\results\analysis_results-t2.xlsx'
p_t3 = r'D:\NNC\COMPORTAMENTO\Animais serios\Teste de preferencia\#3 Teste 2\#32 Teste\results\analysis_results-teste3.xlsx'

df_pref_3d = pd.read_excel(p_t1)
df_pref_real_1 = pd.read_excel(p_t2)
df_pref_t3 = pd.read_excel(p_t3)

# Normalizar colunas
for df in [df_pref_3d, df_pref_real_1]:
    df['DI'] = (df['exploration_time_right (s)'] - df['exploration_time_left (s)']) / df['exploration_time (s)']
    df['pct_right'] = (df['exploration_time_right (s)'] / df['exploration_time (s)']) * 100
    df['pct_time_moving'] = (df['time moving (S)'] / (df['time moving (S)'] + df['time resting (S)'])) * 100
    df['session_duration_s'] = df['time moving (S)'] + df['time resting (S)']
    df['explor_rate_s_per_min'] = df['exploration_time (s)'] / (df['session_duration_s'] / 60.0)

# Para teste 3 (tem sessões t1 e t2)
df_pref_t3['DI'] = (df_pref_t3['exploration_time_right (s)'] - df_pref_t3['exploration_time_left (s)']) / df_pref_t3['exploration_time (s)']
df_pref_t3['pct_right'] = (df_pref_t3['exploration_time_right (s)'] / df_pref_t3['exploration_time (s)']) * 100
df_pref_t3['pct_time_moving'] = (df_pref_t3['time moving (S)'] / (df_pref_t3['time moving (S)'] + df_pref_t3['time resting (S)'])) * 100
df_pref_t3['session_duration_s'] = df_pref_t3['time moving (S)'] + df_pref_t3['time resting (S)']
df_pref_t3['explor_rate_s_per_min'] = df_pref_t3['exploration_time (s)'] / (df_pref_t3['session_duration_s'] / 60.0)

# -------------------------------------------------------------
# 2. CARREGAR ANIMAIS COM CIRURGIA E HEADSTAGE (LOTES #2, #3, #4)
# -------------------------------------------------------------
df_cirurgia = pd.read_excel(os.path.join(planilhas_dir, 'consolidado_comportamento_19animais.xlsx'))
df_cirurgia['session_duration_s'] = df_cirurgia['tempo_movimento_s'] + df_cirurgia['tempo_repouso_s']
df_cirurgia['pct_time_moving'] = (df_cirurgia['tempo_movimento_s'] / df_cirurgia['session_duration_s']) * 100
df_cirurgia['explor_rate_s_per_min'] = df_cirurgia['tempo_exploracao_total_s'] / (df_cirurgia['session_duration_s'] / 60.0)

# -------------------------------------------------------------
# 3. ANÁLISE ESTATÍSTICA: PREFERÊNCIA DE OBJETOS (3D vs REAIS)
# -------------------------------------------------------------
print('='*70)
print('1. ANÁLISE DE PREFERÊNCIA ESPONTÂNEA DE OBJETOS (ANIMAIS NAIVE)')
print('='*70)

# A. Objetos 3D (#t1)
t_3d = stats.ttest_1samp(df_pref_3d['DI'], 0)
print(f'Objetos Impressos 3D (#t1, N={len(df_pref_3d)}):')
print(f'  - Exploração Total: {df_pref_3d["exploration_time (s)"].mean():.2f} +/- {df_pref_3d["exploration_time (s)"].std():.2f} s')
print(f'  - DI Médio: {df_pref_3d["DI"].mean():.4f} +/- {df_pref_3d["DI"].std():.4f}')
print(f'  - % Lado Direito: {df_pref_3d["pct_right"].mean():.2f}% +/- {df_pref_3d["pct_right"].std():.2f}%')
print(f'  - Teste t contra zero (Preferência): t={t_3d.statistic:.4f}, p={t_3d.pvalue:.4f}')

# B. Objetos Reais (#t2)
t_real = stats.ttest_1samp(df_pref_real_1['DI'], 0)
print(f'\nObjetos Reais do Experimento (#t2, N={len(df_pref_real_1)}):')
print(f'  - Exploração Total: {df_pref_real_1["exploration_time (s)"].mean():.2f} +/- {df_pref_real_1["exploration_time (s)"].std():.2f} s')
print(f'  - DI Médio: {df_pref_real_1["DI"].mean():.4f} +/- {df_pref_real_1["DI"].std():.4f}')
print(f'  - % Lado Direito: {df_pref_real_1["pct_right"].mean():.2f}% +/- {df_pref_real_1["pct_right"].std():.2f}%')
print(f'  - Teste t contra zero (Preferência): t={t_real.statistic:.4f}, p={t_real.pvalue:.4f}')

# Comparação pareada 3D vs Real nos mesmos 10 animais
t_pair = stats.ttest_rel(df_pref_3d['exploration_time (s)'], df_pref_real_1['exploration_time (s)'])
print(f'\nComparação de Exploração Total (3D vs Reais nos mesmos animais):')
print(f'  - Teste t pareado: t={t_pair.statistic:.4f}, p={t_pair.pvalue:.4f}')

# -------------------------------------------------------------
# 4. COMPARAÇÃO: IMPACTO DA CIRURGIA E HEADSTAGE
# -------------------------------------------------------------
print('\n' + '='*70)
print('2. IMPACTO DO HEADSTAGE E CIRURGIA: NAIVE VS IMPLANTADOS')
print('='*70)

# Criar dataframe consolidado para comparação direta
naive_vel = df_pref_real_1['mean velocity (cm/s)']
cirurg_vel = df_cirurgia['velocidade_media_cms']

naive_mov_pct = df_pref_real_1['pct_time_moving']
cirurg_mov_pct = df_cirurgia['pct_time_moving']

naive_rate = df_pref_real_1['explor_rate_s_per_min']
cirurg_rate = df_cirurgia['explor_rate_s_per_min']

t_vel = stats.ttest_ind(naive_vel, cirurg_vel)
t_mov = stats.ttest_ind(naive_mov_pct, cirurg_mov_pct)
t_rate = stats.ttest_ind(naive_rate, cirurg_rate)

print(f'Velocidade Média (cm/s):')
print(f'  - Sem Headstage (Naive, N={len(naive_vel)}): {naive_vel.mean():.2f} +/- {naive_vel.std():.2f} cm/s')
print(f'  - Com Headstage (Implantados, N={len(cirurg_vel)}): {cirurg_vel.mean():.2f} +/- {cirurg_vel.std():.2f} cm/s')
print(f'  - Teste t: t={t_vel.statistic:.4f}, p={t_vel.pvalue:.4f}')

print(f'\nPorcentagem de Tempo em Movimento (%):')
print(f'  - Sem Headstage: {naive_mov_pct.mean():.2f}% +/- {naive_mov_pct.std():.2f}%')
print(f'  - Com Headstage: {cirurg_mov_pct.mean():.2f}% +/- {cirurg_mov_pct.std():.2f}%')
print(f'  - Teste t: t={t_mov.statistic:.4f}, p={t_mov.pvalue:.4f}')

print(f'\nTaxa de Exploração Ativa (segundos explorando por minuto de sessão):')
print(f'  - Sem Headstage: {naive_rate.mean():.2f} +/- {naive_rate.std():.2f} s/min')
print(f'  - Com Headstage: {cirurg_rate.mean():.2f} +/- {cirurg_rate.std():.2f} s/min')
print(f'  - Teste t: t={t_rate.statistic:.4f}, p={t_rate.pvalue:.4f}')

# -------------------------------------------------------------
# 5. GERAR GRÁFICO COMPARATIVO CIENTÍFICO
# -------------------------------------------------------------
fig, axes = plt.subplots(1, 3, figsize=(16, 5))

# Plot 1: Preferencia Objetos 3D vs Reais
ax1 = axes[0]
df_plot_pref = pd.DataFrame({
    'Tipo de Objeto': ['3D Impresso']*len(df_pref_3d) + ['Objetos Reais']*len(df_pref_real_1),
    'Índice DI': list(df_pref_3d['DI']) + list(df_pref_real_1['DI'])
})
sns.boxplot(data=df_plot_pref, x='Tipo de Objeto', y='Índice DI', hue='Tipo de Objeto', legend=False, ax=ax1, palette='Blues', boxprops=dict(alpha=0.6))
sns.stripplot(data=df_plot_pref, x='Tipo de Objeto', y='Índice DI', color='black', size=8, jitter=0.2, ax=ax1)
ax1.axhline(0, color='red', ls='--', alpha=0.7)
ax1.set_title('Preferência Espontânea de Objetos (Naive)\nDI = (Dir - Esq) / Total', fontweight='bold')
ax1.set_ylabel('Índice DI', fontweight='bold')

# Plot 2: Velocidade Media: Naive vs Implantados
ax2 = axes[1]
df_plot_vel = pd.DataFrame({
    'Condição': ['Sem Headstage (Naive)']*len(naive_vel) + ['Com Headstage (Cirurgia)']*len(cirurg_vel),
    'Velocidade (cm/s)': list(naive_vel) + list(cirurg_vel)
})
sns.boxplot(data=df_plot_vel, x='Condição', y='Velocidade (cm/s)', hue='Condição', legend=False, ax=ax2, palette='Oranges', boxprops=dict(alpha=0.6))
sns.stripplot(data=df_plot_vel, x='Condição', y='Velocidade (cm/s)', color='black', size=8, jitter=0.2, ax=ax2)
ax2.set_title(f'Velocidade Média de Locomoção\n(p = {t_vel.pvalue:.4f})', fontweight='bold')
ax2.set_ylabel('Velocidade (cm/s)', fontweight='bold')

# Plot 3: Taxa de Exploração por Minuto
ax3 = axes[2]
df_plot_rate = pd.DataFrame({
    'Condição': ['Sem Headstage (Naive)']*len(naive_rate) + ['Com Headstage (Cirurgia)']*len(cirurg_rate),
    'Taxa de Exploração (s/min)': list(naive_rate) + list(cirurg_rate)
})
sns.boxplot(data=df_plot_rate, x='Condição', y='Taxa de Exploração (s/min)', hue='Condição', legend=False, ax=ax3, palette='Purples', boxprops=dict(alpha=0.6))
sns.stripplot(data=df_plot_rate, x='Condição', y='Taxa de Exploração (s/min)', color='black', size=8, jitter=0.2, ax=ax3)
ax3.set_title(f'Engajamento com Objetos por Minuto\n(p = {t_rate.pvalue:.4f})', fontweight='bold')
ax3.set_ylabel('Exploração (s / minuto de sessão)', fontweight='bold')

plt.tight_layout()
plot_file = os.path.join(figuras_dir, 'comparacao_preferencia_e_impacto_headstage.png')
plt.savefig(plot_file, dpi=300)
print(f'\nGráfico comparativo salvo em: {plot_file}')
