import os
import pandas as pd
import scipy.stats as stats
import matplotlib.pyplot as plt
import seaborn as sns
from statannotations.Annotator import Annotator
from matplotlib.ticker import MultipleLocator, FormatStrFormatter

# ==============================================================================
# CARREGAMENTO E PREPARAÇÃO DOS DADOS
# ==============================================================================
base_dir = os.path.dirname(os.path.abspath(__file__)) if '__file__' in locals() else '.'
planilhas_dir = os.path.join(base_dir, 'planilhas') if os.path.exists(os.path.join(base_dir, 'planilhas')) else base_dir

arquivo_comp = os.path.join(planilhas_dir, 'tabela_mestra_comportamento_treino_e_teste.xlsx')
df_comp = pd.read_excel(arquivo_comp)

# Cálculo do tempo total e proporções normalizadas
# t_total = tempo de movimento + tempo de repouso + tempo de exploração
df_comp['t_total'] = df_comp['tempo_movimento_s'] + df_comp['tempo_repouso_s'] + df_comp['tempo_exploracao_total_s']
df_comp['prop_exploracao'] = df_comp['tempo_exploracao_total_s'] / df_comp['t_total']
df_comp['prop_repouso'] = df_comp['tempo_repouso_s'] / df_comp['t_total']

# Configuração de diretórios para salvar as figuras
pasta_fig_local = os.path.join(base_dir, 'figuras')
pasta_fig_relatorios = os.path.abspath(os.path.join(base_dir, '..', '..', 'relatorios', 'figuras'))
os.makedirs(pasta_fig_local, exist_ok=True)
os.makedirs(pasta_fig_relatorios, exist_ok=True)

# Apaga as imagens 2x1 antigas conforme solicitado pelo usuário
antigas_2x1 = [
    'grafico_comportamento_preferencia_teste_lotes.png',
    'grafico_comportamento_grupos_movimento.png',
    'grafico_comportamento_etapas_movimento.png'
]
for f in antigas_2x1:
    for pasta in [pasta_fig_local, pasta_fig_relatorios]:
        p = os.path.join(pasta, f)
        if os.path.exists(p):
            try:
                os.remove(p)
                print(f"[REMOVIDO] Imagem 2x1 antiga: {p}")
            except Exception as e:
                print(f"[AVISO] Não foi possível remover {p}: {e}")

grps_order = ['Controle', 'Grupo 1', 'Grupo 2']
etapas_order = ['Treino 1', 'Treino 2', 'Teste']

paleta_grupos = {
    'Controle': '#7F8C8D',
    'Grupo 1': '#3498DB',
    'Grupo 2': '#9B59B6'
}

paleta_etapas = {
    'Treino 1': '#5D6D7E',
    'Treino 2': '#E67E22',
    'Teste': '#27AE60'
}

df_teste = df_comp[df_comp['tipo_sessao'] == 'Teste'].copy()

# ==============================================================================
# FIGURA 1: SESSÃO TESTE - LOTES #2 e #3 (OBJETOS TP4: VIDRO)
# ==============================================================================
sub23 = df_teste[df_teste['lote'].isin(['#2', '#3'])].copy()
sub23['prop_esq'] = sub23['tempo_exploracao_esquerda_s'] / sub23['tempo_exploracao_total_s']
sub23['prop_dir'] = sub23['tempo_exploracao_direita_s'] / sub23['tempo_exploracao_total_s']

n23_ctrl = len(sub23[sub23['grupo_experimental'] == 'Controle'])
n23_g1 = len(sub23[sub23['grupo_experimental'] == 'Grupo 1'])
n23_g2 = len(sub23[sub23['grupo_experimental'] == 'Grupo 2'])
n23_tot = len(sub23)

longo_23 = pd.melt(
    sub23,
    id_vars=['animal', 'grupo_experimental'],
    value_vars=['prop_esq', 'prop_dir'],
    var_name='lado',
    value_name='proporcao'
)
longo_23['Objeto'] = longo_23['lado'].map({
    'prop_esq': 'Vidro Cilíndrico Roxo',
    'prop_dir': 'Vidro Quadrangular Transparente'
})
paleta_tp4 = {
    'Vidro Cilíndrico Roxo': '#805AD5',
    'Vidro Quadrangular Transparente': '#B2EBF2'
}

fig, ax = plt.subplots(figsize=(7.2, 4.4), dpi=300)
ax.axhline(0.5, color='gray', linestyle='--', linewidth=1, alpha=0.7, zorder=1)
sns.boxplot(
    data=longo_23, x='grupo_experimental', y='proporcao', hue='Objeto', order=grps_order,
    palette=paleta_tp4, ax=ax, width=0.5,
    boxprops=dict(alpha=0.75, edgecolor='black', linewidth=1.2),
    medianprops=dict(color='black', linewidth=1.6),
    whiskerprops=dict(color='black', linewidth=1.2),
    capprops=dict(color='black', linewidth=1.2), zorder=2
)
sns.stripplot(
    data=longo_23, x='grupo_experimental', y='proporcao', hue='Objeto', order=grps_order,
    dodge=True, ax=ax, color='black', alpha=0.6, jitter=0.08, size=5, legend=False, zorder=3
)

pairs_23 = [
    (('Controle', 'Vidro Cilíndrico Roxo'), ('Controle', 'Vidro Quadrangular Transparente')),
    (('Grupo 1', 'Vidro Cilíndrico Roxo'), ('Grupo 1', 'Vidro Quadrangular Transparente')),
    (('Grupo 2', 'Vidro Cilíndrico Roxo'), ('Grupo 2', 'Vidro Quadrangular Transparente'))
]
annot1_1 = Annotator(ax, pairs_23, data=longo_23, x='grupo_experimental', y='proporcao', hue='Objeto', order=grps_order)
annot1_1.configure(test='t-test_paired', text_format='star', loc='inside')
annot1_1.apply_and_annotate()

ax.set_title(f'Sessão Teste: Lotes #2 e #3 — Objetos TP4 (Vidro)\n(Total n={n23_tot}: Controle n={n23_ctrl}, G1 n={n23_g1}, G2 n={n23_g2})', fontsize=10.5, fontweight='bold', pad=8)
ax.set_xlabel('')
ax.set_ylabel('Tempo de Exploração Normalizado')
ax.legend(title='Objeto', loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=2, frameon=True, fontsize=9, title_fontsize=9)
ax.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
plt.tight_layout()

f1_local = os.path.join(pasta_fig_local, 'grafico_comportamento_preferencia_lotes_vidro.png')
f1_rel = os.path.join(pasta_fig_relatorios, 'grafico_comportamento_preferencia_lotes_vidro.png')
plt.savefig(f1_local, dpi=300, bbox_inches='tight')
plt.savefig(f1_rel, dpi=300, bbox_inches='tight')
plt.close(fig)
print(f"[OK] Gerado: {f1_rel}")


# ==============================================================================
# FIGURA 2: SESSÃO TESTE - LOTE #4 (OBJETOS TP2: FRASCOS PET)
# ==============================================================================
sub4 = df_teste[df_teste['lote'] == '#4'].copy()
sub4['prop_esq'] = sub4['tempo_exploracao_esquerda_s'] / sub4['tempo_exploracao_total_s']
sub4['prop_dir'] = sub4['tempo_exploracao_direita_s'] / sub4['tempo_exploracao_total_s']

n4_ctrl = len(sub4[sub4['grupo_experimental'] == 'Controle'])
n4_g1 = len(sub4[sub4['grupo_experimental'] == 'Grupo 1'])
n4_g2 = len(sub4[sub4['grupo_experimental'] == 'Grupo 2'])
n4_tot = len(sub4)

longo_4 = pd.melt(
    sub4,
    id_vars=['animal', 'grupo_experimental'],
    value_vars=['prop_esq', 'prop_dir'],
    var_name='lado',
    value_name='proporcao'
)
longo_4['Objeto'] = longo_4['lado'].map({
    'prop_esq': 'PET Tampa Vermelha',
    'prop_dir': 'PET Tampa Branca'
})
paleta_tp2 = {
    'PET Tampa Vermelha': '#E53E3E',
    'PET Tampa Branca': '#EDF2F7'
}

fig, ax = plt.subplots(figsize=(7.2, 4.4), dpi=300)
ax.axhline(0.5, color='gray', linestyle='--', linewidth=1, alpha=0.7, zorder=1)
sns.boxplot(
    data=longo_4, x='grupo_experimental', y='proporcao', hue='Objeto', order=grps_order,
    palette=paleta_tp2, ax=ax, width=0.5,
    boxprops=dict(alpha=0.75, edgecolor='black', linewidth=1.2),
    medianprops=dict(color='black', linewidth=1.6),
    whiskerprops=dict(color='black', linewidth=1.2),
    capprops=dict(color='black', linewidth=1.2), zorder=2
)
sns.stripplot(
    data=longo_4, x='grupo_experimental', y='proporcao', hue='Objeto', order=grps_order,
    dodge=True, ax=ax, color='black', alpha=0.6, jitter=0.08, size=5, legend=False, zorder=3
)

pairs_4 = [
    (('Controle', 'PET Tampa Vermelha'), ('Controle', 'PET Tampa Branca')),
    (('Grupo 1', 'PET Tampa Vermelha'), ('Grupo 1', 'PET Tampa Branca')),
    (('Grupo 2', 'PET Tampa Vermelha'), ('Grupo 2', 'PET Tampa Branca'))
]
annot1_2 = Annotator(ax, pairs_4, data=longo_4, x='grupo_experimental', y='proporcao', hue='Objeto', order=grps_order)
annot1_2.configure(test='t-test_paired', text_format='star', loc='inside')
annot1_2.apply_and_annotate()

ax.set_title(f'Sessão Teste: Lote #4 — Objetos TP2 (Frascos PET)\n(Total n={n4_tot}: Controle n={n4_ctrl}, G1 n={n4_g1}, G2 n={n4_g2})', fontsize=10.5, fontweight='bold', pad=8)
ax.set_xlabel('')
ax.set_ylabel('Tempo de Exploração Normalizado')
ax.legend(title='Objeto', loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=2, frameon=True, fontsize=9, title_fontsize=9)
ax.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
plt.tight_layout()

f2_local = os.path.join(pasta_fig_local, 'grafico_comportamento_preferencia_lote_pet.png')
f2_rel = os.path.join(pasta_fig_relatorios, 'grafico_comportamento_preferencia_lote_pet.png')
plt.savefig(f2_local, dpi=300, bbox_inches='tight')
plt.savefig(f2_rel, dpi=300, bbox_inches='tight')
plt.close(fig)
print(f"[OK] Gerado: {f2_rel}")


# ==============================================================================
# FIGURA 3: MOVIMENTO GERAL - PROPORÇÃO DE EXPLORAÇÃO POR GRUPO EXPERIMENTAL
# ==============================================================================
grupos_exp = [df_comp[df_comp['grupo_experimental'] == grp]['prop_exploracao'].values for grp in grps_order]
f2_exp, p2_exp = stats.f_oneway(*grupos_exp)

n_ctrl = len(df_comp[df_comp['grupo_experimental'] == 'Controle'])
n_g1 = len(df_comp[df_comp['grupo_experimental'] == 'Grupo 1'])
n_g2 = len(df_comp[df_comp['grupo_experimental'] == 'Grupo 2'])
tot_obs = len(df_comp)
pairs_grupos = [('Controle', 'Grupo 1'), ('Controle', 'Grupo 2'), ('Grupo 1', 'Grupo 2')]

fig, ax = plt.subplots(figsize=(6.8, 4.2), dpi=300)
sns.boxplot(
    data=df_comp, x='grupo_experimental', y='prop_exploracao', order=grps_order,
    palette=paleta_grupos, ax=ax, width=0.45,
    boxprops=dict(alpha=0.75, edgecolor='black', linewidth=1.2),
    medianprops=dict(color='black', linewidth=1.6),
    whiskerprops=dict(color='black', linewidth=1.2),
    capprops=dict(color='black', linewidth=1.2)
)
sns.stripplot(data=df_comp, x='grupo_experimental', y='prop_exploracao', order=grps_order, ax=ax, color='black', alpha=0.6, jitter=0.1, size=5)

annot2_1 = Annotator(ax, pairs_grupos, data=df_comp, x='grupo_experimental', y='prop_exploracao', order=grps_order)
annot2_1.configure(test='t-test_ind', text_format='star', loc='inside')
annot2_1.apply_and_annotate()

ax.set_title('Proporção de Tempo de Exploração dos Objetos por Grupo', fontsize=11, fontweight='bold', pad=8)
ax.set_xlabel('')
ax.set_ylabel('Tempo Exploração / Tempo Total')
ax.yaxis.set_major_locator(MultipleLocator(0.05))
ax.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
plt.tight_layout()

f3_local = os.path.join(pasta_fig_local, 'grafico_comportamento_grupos_exploracao.png')
f3_rel = os.path.join(pasta_fig_relatorios, 'grafico_comportamento_grupos_exploracao.png')
plt.savefig(f3_local, dpi=300, bbox_inches='tight')
plt.savefig(f3_rel, dpi=300, bbox_inches='tight')
plt.close(fig)
print(f"[OK] Gerado: {f3_rel}")


# ==============================================================================
# FIGURA 4: MOVIMENTO GERAL - PROPORÇÃO DE REPOUSO POR GRUPO EXPERIMENTAL
# ==============================================================================
grupos_rep = [df_comp[df_comp['grupo_experimental'] == grp]['prop_repouso'].values for grp in grps_order]
f2_rep, p2_rep = stats.f_oneway(*grupos_rep)

fig, ax = plt.subplots(figsize=(6.8, 4.2), dpi=300)
sns.boxplot(
    data=df_comp, x='grupo_experimental', y='prop_repouso', order=grps_order,
    palette=paleta_grupos, ax=ax, width=0.45,
    boxprops=dict(alpha=0.75, edgecolor='black', linewidth=1.2),
    medianprops=dict(color='black', linewidth=1.6),
    whiskerprops=dict(color='black', linewidth=1.2),
    capprops=dict(color='black', linewidth=1.2)
)
sns.stripplot(data=df_comp, x='grupo_experimental', y='prop_repouso', order=grps_order, ax=ax, color='black', alpha=0.6, jitter=0.1, size=5)

annot2_2 = Annotator(ax, pairs_grupos, data=df_comp, x='grupo_experimental', y='prop_repouso', order=grps_order)
annot2_2.configure(test='t-test_ind', text_format='star', loc='inside')
annot2_2.apply_and_annotate()

ax.set_title('Proporção de Tempo de Repouso (Imobilidade) por Grupo', fontsize=11, fontweight='bold', pad=8)
ax.set_xlabel('')
ax.set_ylabel('Tempo Repouso / Tempo Total')
ax.yaxis.set_major_locator(MultipleLocator(0.1))
ax.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
plt.tight_layout()

f4_local = os.path.join(pasta_fig_local, 'grafico_comportamento_grupos_repouso.png')
f4_rel = os.path.join(pasta_fig_relatorios, 'grafico_comportamento_grupos_repouso.png')
plt.savefig(f4_local, dpi=300, bbox_inches='tight')
plt.savefig(f4_rel, dpi=300, bbox_inches='tight')
plt.close(fig)
print(f"[OK] Gerado: {f4_rel}")


# ==============================================================================
# FIGURA 5: MOVIMENTO POR ETAPA - PROPORÇÃO DE EXPLORAÇÃO (TREINO 1 VS 2 VS TESTE)
# ==============================================================================
etapas_exp = [df_comp[df_comp['etapa'] == et]['prop_exploracao'].values for et in etapas_order]
f3_exp, p3_exp = stats.f_oneway(*etapas_exp)

n_t1 = len(df_comp[df_comp['etapa'] == 'Treino 1'])
n_t2 = len(df_comp[df_comp['etapa'] == 'Treino 2'])
n_tst = len(df_comp[df_comp['etapa'] == 'Teste'])
pairs_etapas = [('Treino 1', 'Treino 2'), ('Treino 2', 'Teste'), ('Treino 1', 'Teste')]

fig, ax = plt.subplots(figsize=(6.8, 4.2), dpi=300)
sns.boxplot(
    data=df_comp, x='etapa', y='prop_exploracao', order=etapas_order,
    palette=paleta_etapas, ax=ax, width=0.45,
    boxprops=dict(alpha=0.75, edgecolor='black', linewidth=1.2),
    medianprops=dict(color='black', linewidth=1.6),
    whiskerprops=dict(color='black', linewidth=1.2),
    capprops=dict(color='black', linewidth=1.2)
)
sns.stripplot(data=df_comp, x='etapa', y='prop_exploracao', order=etapas_order, ax=ax, color='black', alpha=0.6, jitter=0.1, size=5)

annot3_1 = Annotator(ax, pairs_etapas, data=df_comp, x='etapa', y='prop_exploracao', order=etapas_order)
annot3_1.configure(test='t-test_ind', text_format='star', loc='inside')
annot3_1.apply_and_annotate()

ax.set_title('Proporção de Tempo de Exploração dos Objetos por Etapa', fontsize=11, fontweight='bold', pad=8)
ax.set_xlabel('')
ax.set_ylabel('Tempo Exploração / Tempo Total')
ax.yaxis.set_major_locator(MultipleLocator(0.05))
ax.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
plt.tight_layout()

f5_local = os.path.join(pasta_fig_local, 'grafico_comportamento_etapas_exploracao.png')
f5_rel = os.path.join(pasta_fig_relatorios, 'grafico_comportamento_etapas_exploracao.png')
plt.savefig(f5_local, dpi=300, bbox_inches='tight')
plt.savefig(f5_rel, dpi=300, bbox_inches='tight')
plt.close(fig)
print(f"[OK] Gerado: {f5_rel}")


# ==============================================================================
# FIGURA 6: MOVIMENTO POR ETAPA - PROPORÇÃO DE REPOUSO (TREINO 1 VS 2 VS TESTE)
# ==============================================================================
etapas_rep = [df_comp[df_comp['etapa'] == et]['prop_repouso'].values for et in etapas_order]
f3_rep, p3_rep = stats.f_oneway(*etapas_rep)

fig, ax = plt.subplots(figsize=(6.8, 4.2), dpi=300)
sns.boxplot(
    data=df_comp, x='etapa', y='prop_repouso', order=etapas_order,
    palette=paleta_etapas, ax=ax, width=0.45,
    boxprops=dict(alpha=0.75, edgecolor='black', linewidth=1.2),
    medianprops=dict(color='black', linewidth=1.6),
    whiskerprops=dict(color='black', linewidth=1.2),
    capprops=dict(color='black', linewidth=1.2)
)
sns.stripplot(data=df_comp, x='etapa', y='prop_repouso', order=etapas_order, ax=ax, color='black', alpha=0.6, jitter=0.1, size=5)

annot3_2 = Annotator(ax, pairs_etapas, data=df_comp, x='etapa', y='prop_repouso', order=etapas_order)
annot3_2.configure(test='t-test_ind', text_format='star', loc='inside')
annot3_2.apply_and_annotate()

ax.set_title('Proporção de Tempo de Repouso (Imobilidade) por Etapa', fontsize=11, fontweight='bold', pad=8)
ax.set_xlabel('')
ax.set_ylabel('Tempo Repouso / Tempo Total')
ax.yaxis.set_major_locator(MultipleLocator(0.1))
ax.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
plt.tight_layout()

f6_local = os.path.join(pasta_fig_local, 'grafico_comportamento_etapas_repouso.png')
f6_rel = os.path.join(pasta_fig_relatorios, 'grafico_comportamento_etapas_repouso.png')
plt.savefig(f6_local, dpi=300, bbox_inches='tight')
plt.savefig(f6_rel, dpi=300, bbox_inches='tight')
plt.close(fig)
print(f"[OK] Gerado: {f6_rel}")

print("\n[SUCESSO] Todas as 6 figuras individuais foram geradas e salvas com sucesso.")
