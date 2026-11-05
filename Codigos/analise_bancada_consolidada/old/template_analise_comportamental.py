"""
=============================================================================
GUIA & TEMPLATE: Análise Estatística Comportamental, Gráficos e Exportação LaTeX
=============================================================================
Este script serve como modelo para sua análise de mestrado:
  1. Carregamento e limpeza de planilhas Excel (Pandas)
  2. Cálculo do Índice de Discriminação (DI)
  3. Testes Estatísticos (Shapiro-Wilk, Teste t, Mann-Whitney, ANOVA)
  4. Gráficos de publicação com Seaborn + Matplotlib + statannotations (asteriscos)
  5. Exportação automática de tabelas resumo formatadas em código LaTeX (booktabs)
=============================================================================
"""

import os
import numpy as np
import pandas as pd
import scipy.stats as stats
import matplotlib.pyplot as plt
import seaborn as sns
from statannotations.Annotator import Annotator

# ---------------------------------------------------------------------------
# 0. DEFINIÇÃO DE PASTAS E ESTILO VISUAL
# ---------------------------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Pasta de planilhas (dentro de Codigos/analise_bancada_consolidada/)
PLANILHAS_DIR = os.path.join(BASE_DIR, "planilhas")
if not os.path.exists(PLANILHAS_DIR):
    PLANILHAS_DIR = BASE_DIR

# Pastas de saída do relatório em LaTeX
RELATORIOS_FIGURAS = os.path.abspath(os.path.join(BASE_DIR, "..", "..", "relatorios", "figuras"))
RELATORIOS_TABELAS = os.path.abspath(os.path.join(BASE_DIR, "..", "..", "relatorios", "tabelas"))
LOCAL_FIG_DIR = os.path.join(BASE_DIR, "figuras")

os.makedirs(RELATORIOS_FIGURAS, exist_ok=True)
os.makedirs(RELATORIOS_TABELAS, exist_ok=True)
os.makedirs(LOCAL_FIG_DIR, exist_ok=True)

# Estilo científico de publicação (Nature / J. Neuroscience)
sns.set_theme(style="ticks")
plt.rcParams['font.size'] = 11
plt.rcParams['axes.labelsize'] = 12
plt.rcParams['axes.titlesize'] = 13
plt.rcParams['xtick.labelsize'] = 10
plt.rcParams['ytick.labelsize'] = 10
plt.rcParams['figure.dpi'] = 300

# ---------------------------------------------------------------------------
# 1. CARREGAMENTO E LIMPEZA DE DADOS DO EXCEL
# ---------------------------------------------------------------------------
ARQUIVO_PREF = os.path.join(PLANILHAS_DIR, "tabela_unificada_testes_de_preferencia.xlsx")

print("--- [PASSO 1] Carregando Planilha de Preferência ---")
df = pd.read_excel(ARQUIVO_PREF)

print(f"Total de registros carregados: {len(df)}")
print("Colunas disponíveis:", list(df.columns))

# Limpeza e Padronização:
# a) Se a coluna DI não existisse, poderíamos calculá-la assim:
# df['DI_calculado'] = (df['tempo_exploracao_esquerda_s'] - df['tempo_exploracao_direita_s']) / df['tempo_exploracao_total_s']

# b) Renomear coluna do DI para facilitar o manuseio no código:
col_di = 'DI [(t_Esq - t_Dir)/t_tot]'
df = df.rename(columns={col_di: 'DI'})

# c) Remover linhas onde o DI seja nulo (caso algum animal não tenha explorado):
df_limpo = df.dropna(subset=['DI']).copy()

# d) Filtrar colunas de interesse para análise:
cols_interesse = ['codigo_teste', 'categoria_objeto', 'tipo_material', 'animal', 
                  'tempo_exploracao_total_s', 'DI']
df_analise = df_limpo[cols_interesse].copy()

print(f"Registros válidos após limpeza: {len(df_analise)}\n")


# ---------------------------------------------------------------------------
# 2. ANÁLISE ESTATÍSTICA (Passo a Passo)
# ---------------------------------------------------------------------------
print("--- [PASSO 2] Executando Testes Estatísticos ---")

# Exemplo: O DI difere entre "3D Impresso" e "Real Físico"?
grupo_3d = df_analise[df_analise['categoria_objeto'] == '3D Impresso']['DI']
grupo_real = df_analise[df_analise['categoria_objeto'] == 'Real Físico']['DI']

# a) Teste de Normalidade (Shapiro-Wilk)
stat_3d, p_norm_3d = stats.shapiro(grupo_3d)
stat_real, p_norm_real = stats.shapiro(grupo_real)
print(f"Normalidade (Shapiro-Wilk) - 3D Impresso: p = {p_norm_3d:.4f}")
print(f"Normalidade (Shapiro-Wilk) - Real Físico: p = {p_norm_real:.4f}")

# b) Teste t de Student (ou Mann-Whitney U se não-normal)
if p_norm_3d > 0.05 and p_norm_real > 0.05:
    t_stat, p_val = stats.ttest_ind(grupo_3d, grupo_real, equal_var=False)
    tipo_teste = "Teste t de Student (Welch)"
else:
    t_stat, p_val = stats.mannwhitneyu(grupo_3d, grupo_real)
    tipo_teste = "Teste de Mann-Whitney U"

print(f"{tipo_teste}: estatística = {t_stat:.3f}, p-valor = {p_val:.4f}")
significativo = "SIM (p < 0.05)" if p_val < 0.05 else "NÃO (p >= 0.05)"
print(f"Diferença estatisticamente significativa? {significativo}\n")

# c) ANOVA One-Way (comparando os 4 testes de preferência)
grupos_testes = [grupo['DI'].values for _, grupo in df_analise.groupby('codigo_teste')]
f_val, p_anova = stats.f_oneway(*grupos_testes)
print(f"ANOVA One-Way entre Testes: F = {f_val:.3f}, p-valor = {p_anova:.4f}\n")


# ---------------------------------------------------------------------------
# 3. GRÁFICOS DE PUBLICAÇÃO COM STATANNOTATIONS (Boxplot + Pontos + Asteriscos)
# ---------------------------------------------------------------------------
print("--- [PASSO 3] Gerando Figuras Científicas com Asteriscos ---")

fig, ax = plt.subplots(figsize=(5.5, 4.5))

# Boxplot elegante
sns.boxplot(
    data=df_analise, 
    x='categoria_objeto', 
    y='DI', 
    hue='categoria_objeto',
    legend=False,
    ax=ax, 
    palette=['#a1c9f4', '#ffb482'],
    width=0.45,
    boxprops=dict(alpha=0.75, lw=1.3),
    medianprops=dict(color='black', lw=2),
    showcaps=True
)

# Stripplot sobreposto (pontos individuais dos animais)
sns.stripplot(
    data=df_analise, 
    x='categoria_objeto', 
    y='DI', 
    ax=ax, 
    color='#222222', 
    size=6.5, 
    alpha=0.75, 
    jitter=0.15
)

# Linha de referência no DI = 0 (sem preferência)
ax.axhline(0, color='gray', linestyle=':', lw=1.2, label='Sem Preferência (DI=0)')

# Anotação de Significância Estatística (statannotations com asteriscos)
pares_comparacao = [("3D Impresso", "Real Físico")]
annotator = Annotator(ax, pares_comparacao, data=df_analise, x='categoria_objeto', y='DI')
annotator.configure(
    test='Mann-Whitney' if 'Mann-Whitney' in tipo_teste else 't-test_ind',
    text_format='star',  # Exibe *, **, ***, ou ns
    loc='inside',
    color='black',
    line_width=1.2
)
annotator.apply_and_annotate()

ax.set_xlabel('Tipo de Objeto Testado', fontweight='bold', labelpad=8)
ax.set_ylabel('Índice de Discriminação (DI)', fontweight='bold', labelpad=8)
ax.set_title('Preferência Exploratória: 3D Impresso vs Físico', pad=12)
sns.despine(ax=ax, top=True, right=True)
plt.tight_layout()

# Salva na pasta relatorios/figuras/ (para o LaTeX) e cópia local
for folder in [RELATORIOS_FIGURAS, LOCAL_FIG_DIR]:
    plt.savefig(os.path.join(folder, "grafico_preferencia_3d_vs_real.pdf"), bbox_inches='tight')
    plt.savefig(os.path.join(folder, "grafico_preferencia_3d_vs_real.png"), dpi=300, bbox_inches='tight')

plt.close(fig)
print(f"[OK] Gráfico salvo em: {RELATORIOS_FIGURAS}/grafico_preferencia_3d_vs_real.pdf")


# ---------------------------------------------------------------------------
# 4. EXPORTAÇÃO AUTOMÁTICA DE TABELAS RESUMO PARA LATEX (Booktabs)
# ---------------------------------------------------------------------------
print("--- [PASSO 4] Exportando Tabela Resumo para Código LaTeX ---")

resumo_stats = df_analise.groupby('categoria_objeto')['DI'].agg(
    N='count',
    Media='mean',
    DesvioPadrao='std',
    Mediana='median',
    Minimo='min',
    Maximo='max'
).reset_index()

resumo_stats.columns = ['Categoria do Objeto', 'N', 'Média', 'Desvio Padrão', 'Mediana', 'Mínimo', 'Máximo']

caminho_tex_tabela = os.path.join(RELATORIOS_TABELAS, "tabela_resumo_estatistico.tex")
codigo_latex = resumo_stats.to_latex(
    index=False,
    float_format="%.3f",
    caption="Resumo estatístico do Índice de Discriminação (DI) por categoria de objeto.",
    label="tab:resumo_di",
    position="htbp"
)

with open(caminho_tex_tabela, "w", encoding="utf-8") as f:
    f.write(codigo_latex)

print(f"[OK] Tabela LaTeX exportada em: {caminho_tex_tabela}")
print("\n=== EXECUÇÃO CONCLUÍDA COM SUCESSO ===")
