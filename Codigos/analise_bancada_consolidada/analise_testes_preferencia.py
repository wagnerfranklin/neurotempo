import os
import pandas as pd
import scipy.stats as stats

# Localização robusta das planilhas (mesma pasta ou subpasta 'planilhas')
base_dir = os.path.dirname(os.path.abspath(__file__)) if '__file__' in locals() else '.'
planilhas_dir = os.path.join(base_dir, 'planilhas') if os.path.exists(os.path.join(base_dir, 'planilhas')) else base_dir

arquivo_pref = os.path.join(planilhas_dir, 'tabela_unificada_testes_de_preferencia.xlsx')
df_pref = pd.read_excel(arquivo_pref)

col_di = 'DI [(t_Esq - t_Dir)/t_tot]'

# Análise estatística de preferência por teste (teste t unicaudal/bicaudal contra média 0)
resultados = []

for teste, grupo in df_pref.groupby('codigo_teste'):
    di = grupo[col_di].dropna()
    n = len(di)
    media_di = di.mean()
    sem_di = di.sem()
    
    # Teste de normalidade e Teste t de uma amostra contra zero (DI = 0 -> sem preferência)
    _, p_shapiro = stats.shapiro(di)
    t_stat, p_val = stats.ttest_1samp(di, popmean=0)
    
    # Interpretação biológica / experimental
    if p_val < 0.05:
        obj_pref = grupo['objeto_esquerda'].iloc[0] if media_di > 0 else grupo['objeto_direita'].iloc[0]
        status = f"Preferência por '{obj_pref}' (p={p_val:.4f})"
    else:
        status = f"Neutro / Sem preferência (p={p_val:.4f})"
        
    resultados.append({
        'Teste': teste,
        'N': n,
        'DI Médio': round(media_di, 3),
        'SEM': round(sem_di, 3),
        't': round(t_stat, 2),
        'p-valor (t-test)': round(p_val, 4),
        'Normalidade (p)': round(p_shapiro, 3),
        'Conclusão': status
    })

# Exibição dos resultados em tabela enxuta
tabela_resultados = pd.DataFrame(resultados)
print("\n=== AVALIAÇÃO DE PREFERÊNCIA INATA (H0: DI = 0) ===")
print(tabela_resultados.to_string(index=False))


# ==============================================================================
# GRÁFICO 2x2: PREFERÊNCIA DE OBJETOS COM BOXPLOT E STATANNOTATIONS
# ==============================================================================
import matplotlib.pyplot as plt
import seaborn as sns
from statannotations.Annotator import Annotator
from matplotlib.ticker import MultipleLocator, FormatStrFormatter

fig, axes = plt.subplots(2, 2, figsize=(9.5, 7.5))
fig.suptitle('Testes de Preferência de Objetos (n=10)', fontsize=14, fontweight='bold', y=0.98)

# Mapeamento do código na planilha para o título exibido
testes_info = [
    ('Teste 1.1', 'TP1'),
    ('Teste 1.2', 'TP2'),
    ('Teste 2.1', 'TP3'),
    ('Teste 2.2', 'TP4')
]

# Configuração única dos objetos: Nome na planilha -> (Nome exibido no gráfico, Cor)
objetos_config = {
    'Círculo Extrudado 3D': ('Prisma Circular PLA', '#E69F00'),
    'Pentágono Extrudado 3D': ('Prisma Pentagonal PLA', '#56B4E9'),
    'Frasco Plástico Tampa Vermelha (Translúcido)': ('PET Tampa Vermelha', '#E53E3E'),
    'Frasco Plástico Tampa Branca (Opaco)': ('PET Tampa Branca', '#EDF2F7'),
    'Prisma Triangular Extrudado 3D': ('Prisma Triangular PLA', '#3182CE'),
    'Prisma Quadrado Extrudado 3D': ('Prisma Quadrangular PLA', '#DD6B20'),
    'Garrafa Vidro Cilíndrica Roxa': ('Vidro Cilíndrico Roxo', '#805AD5'),
    'Garrafa Vidro Quadrada Transparente': ('Vidro Quadrangular Transparente', '#B2EBF2')
}

# Gerados automaticamente a partir de objetos_config (sem retrabalho):
nomes_curtos = {k: v[0] for k, v in objetos_config.items()}
paleta_cores = {v[0]: v[1] for k, v in objetos_config.items()}

for i, (cod_teste, titulo_teste) in enumerate(testes_info):
    ax = axes.flat[i]
    sub = df_pref[df_pref['codigo_teste'] == cod_teste].copy()
    
    # p-valor do teste de preferência do DI contra zero
    di = sub[col_di].dropna()
    _, p_val = stats.ttest_1samp(di, popmean=0)
    
    # Normalização: Tempo de exploração do objeto / Tempo total
    sub['prop_esq'] = sub['tempo_exploracao_esquerda_s'] / sub['tempo_exploracao_total_s']
    sub['prop_dir'] = sub['tempo_exploracao_direita_s'] / sub['tempo_exploracao_total_s']
    
    sub_longo = pd.melt(
        sub,
        value_vars=['prop_esq', 'prop_dir'],
        var_name='lado',
        value_name='proporcao'
    )
    obj1 = nomes_curtos.get(sub['objeto_esquerda'].iloc[0])
    obj2 = nomes_curtos.get(sub['objeto_direita'].iloc[0])
    sub_longo['objeto'] = sub_longo['lado'].map({'prop_esq': obj1, 'prop_dir': obj2})
    
    # Linha de neutralidade (0.5 = 50% para cada objeto, sem preferência)
    ax.axhline(0.5, color='gray', linestyle='--', linewidth=1, alpha=0.7, zorder=1)
    
    # Boxplot colorido + dispersão dos pontos individuais
    sns.boxplot(
        data=sub_longo,
        x='objeto',
        y='proporcao',
        hue='objeto',
        palette=paleta_cores,
        legend=False,
        ax=ax,
        width=0.45,
        boxprops=dict(alpha=0.75, edgecolor='black', linewidth=1.2),
        medianprops=dict(color='black', linewidth=1.6),
        whiskerprops=dict(color='black', linewidth=1.2),
        capprops=dict(color='black', linewidth=1.2),
        zorder=2
    )
    sns.stripplot(
        data=sub_longo,
        x='objeto',
        y='proporcao',
        ax=ax,
        color='black',
        alpha=0.6,
        jitter=0.1,
        size=5,
        zorder=3
    )
    
    # Anotação de significância estatística
    annot = Annotator(ax, [(obj1, obj2)], data=sub_longo, x='objeto', y='proporcao')
    annot.configure(text_format='star', loc='inside')
    annot.set_pvalues([p_val])
    annot.annotate()
    
    ax.set_title(f"{titulo_teste} (p = {p_val:.3f})", fontweight='bold', fontsize=11, pad=8)
    ax.set_xlabel('')
    ax.set_ylabel('Tempo de Exploração Normalizado')
    
    # 1 casa decimal no eixo Y
    ax.yaxis.set_major_locator(MultipleLocator(0.1))
    ax.yaxis.set_major_formatter(FormatStrFormatter('%.1f'))

plt.tight_layout(rect=[0, 0, 1, 0.95])

# Salvar localmente em Codigos/analise_bancada_consolidada/figuras/
os.makedirs(os.path.join(base_dir, 'figuras'), exist_ok=True)
caminho_fig = os.path.join(base_dir, 'figuras', 'grafico_preferencia_obj.png')
plt.savefig(caminho_fig, dpi=300)
print(f"\n[INFO] Gráfico salvo com sucesso em: {caminho_fig}")

# Salvar também na pasta relatorios/figuras/
pasta_relatorios_fig = os.path.abspath(os.path.join(base_dir, '..', '..', 'relatorios', 'figuras'))
os.makedirs(pasta_relatorios_fig, exist_ok=True)
caminho_fig_relatorios = os.path.join(pasta_relatorios_fig, 'grafico_preferencia_obj.png')
plt.savefig(caminho_fig_relatorios, dpi=300)
print(f"[INFO] Gráfico salvo também em: {caminho_fig_relatorios}")

# ==============================================================================
# ANOVA E GRÁFICO 2x1: TEMPO DE EXPLORAÇÃO E REPOUSO / TEMPO TOTAL
# ==============================================================================
# t_total = tempo de movimento + tempo de repouso + tempo de exploração
df_pref['t_total'] = df_pref['tempo_movimento_s'] + df_pref['tempo_repouso_s'] + df_pref['tempo_exploracao_total_s']
df_pref['prop_exploracao'] = df_pref['tempo_exploracao_total_s'] / df_pref['t_total']
df_pref['prop_repouso'] = df_pref['tempo_repouso_s'] / df_pref['t_total']

map_teste = {'Teste 1.1': 'TP1', 'Teste 1.2': 'TP2', 'Teste 2.1': 'TP3', 'Teste 2.2': 'TP4'}
df_pref['teste_label'] = df_pref['codigo_teste'].map(map_teste)

# ANOVA de uma via para Exploração e Repouso
grupos_exp = [g['prop_exploracao'].values for _, g in df_pref.groupby('teste_label')]
f_exp, p_exp = stats.f_oneway(*grupos_exp)

grupos_rep = [g['prop_repouso'].values for _, g in df_pref.groupby('teste_label')]
f_rep, p_rep = stats.f_oneway(*grupos_rep)

print("\n=== ANOVA: TEMPO DE EXPLORAÇÃO E REPOUSO (NORMALIZADOS POR T_TOTAL) ===")
print(f"1) Proporção de Exploração: F = {f_exp:.2f}, p-valor = {p_exp:.4f}")
print(f"2) Proporção de Repouso:    F = {f_rep:.2f}, p-valor = {p_rep:.4f}")

# Figura 2 linhas x 1 coluna
fig2, (ax1, ax2) = plt.subplots(2, 1, figsize=(7.5, 9))
fig2.suptitle('Comparação de Comportamento Global entre Testes (vs. TP2)', fontsize=13, fontweight='bold', y=0.98)

paleta_testes = {
    'TP1': '#5D6D7E',
    'TP2': '#E74C3C',  # Destaque para o Teste 2 (objeto escolhido)
    'TP3': '#3498DB',
    'TP4': '#9B59B6'
}

pairs_vs_teste2 = [('TP1', 'TP2'), ('TP2', 'TP3'), ('TP2', 'TP4')]

# --- Painel 1: Proporção de Exploração ---
sns.boxplot(data=df_pref, x='teste_label', y='prop_exploracao', hue='teste_label', palette=paleta_testes, legend=False, ax=ax1, width=0.45, boxprops=dict(alpha=0.75, edgecolor='black', linewidth=1.2), medianprops=dict(color='black', linewidth=1.6))
sns.stripplot(data=df_pref, x='teste_label', y='prop_exploracao', ax=ax1, color='black', alpha=0.6, jitter=0.1, size=5)

annot1 = Annotator(ax1, pairs_vs_teste2, data=df_pref, x='teste_label', y='prop_exploracao')
annot1.configure(test='t-test_ind', text_format='star', loc='inside')
annot1.apply_and_annotate()

ax1.set_title(f'Proporção de Tempo de Exploração dos Objetos (ANOVA: p = {p_exp:.3f})', fontsize=11, fontweight='bold')
ax1.set_xlabel('')
ax1.set_ylabel('Tempo Exploração / Tempo Total')

# --- Painel 2: Proporção de Repouso ---
sns.boxplot(data=df_pref, x='teste_label', y='prop_repouso', hue='teste_label', palette=paleta_testes, legend=False, ax=ax2, width=0.45, boxprops=dict(alpha=0.75, edgecolor='black', linewidth=1.2), medianprops=dict(color='black', linewidth=1.6))
sns.stripplot(data=df_pref, x='teste_label', y='prop_repouso', ax=ax2, color='black', alpha=0.6, jitter=0.1, size=5)

annot2 = Annotator(ax2, pairs_vs_teste2, data=df_pref, x='teste_label', y='prop_repouso')
annot2.configure(test='t-test_ind', text_format='star', loc='inside')
annot2.apply_and_annotate()

ax2.set_title(f'Proporção de Tempo de Repouso (Imobilidade) (ANOVA: p = {p_rep:.3f})', fontsize=11, fontweight='bold')
ax2.set_xlabel('')
ax2.set_ylabel('Tempo Repouso / Tempo Total')

plt.tight_layout(rect=[0, 0, 1, 0.96])

caminho_fig2 = os.path.join(base_dir, 'figuras', 'grafico_exploracao_repouso_anova.png')
plt.savefig(caminho_fig2, dpi=300)
print(f"\n[INFO] Gráfico ANOVA salvo com sucesso em: {caminho_fig2}")

caminho_fig2_relatorios = os.path.join(pasta_relatorios_fig, 'grafico_exploracao_repouso_anova.png')
plt.savefig(caminho_fig2_relatorios, dpi=300)
print(f"[INFO] Gráfico ANOVA salvo também em: {caminho_fig2_relatorios}")

plt.show()





