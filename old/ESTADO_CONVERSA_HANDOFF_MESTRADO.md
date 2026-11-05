# PACOTE DE TRANSIÇÃO E HERANÇA DE ESTADO (SESSION HANDOFF)
## Conversa de Origem: `0f5d4624-c159-4aba-8d26-c56696e860df`
**Link Direto de Conversação**: [Conversa Anterior](conversation://0f5d4624-c159-4aba-8d26-c56696e860df)
**Data de Consolidação**: 20/10/2026

---

## 1. Identidade do Pesquisador e Situação Acadêmica

* **Pesquisador**: Wagner Mathias Fonseca Franklin (Engenheiro Mecatrônico, UFMG).
* **Programa**: Pós-Graduação em Engenharia Elétrica (**PPGEE / UFMG**), Linha de Engenharia Biomédica e Inteligência Computacional.
* **Orientação**:
  * Prof. Dr. Márcio Flávio Dutra Moraes (NNC / ICB / UFMG - Engenharia Biomédica).
  * Prof. Dr. Hani Camille Yehia (PPGEE / UFMG - Inteligência Computacional).
* **Diagnóstico Experimental e Decisões Tomadas**:
  1. **Falha de Histologia nos Testes Anteriores**: Os cérebros fatiados não atingiram o CA3 ventral e as levas subsequentes não foram fatiadas. Portanto, a variável independente (localização anatômica da ponta do eletrodo) é indeterminada. Atribuir os efeitos comportamentais ao CA3 seria cientificamente inválido.
  2. **Abandono do Comportamento Animal (*In Vivo*)**: O protocolo comportamental (Dix & Aggleton, 1999) foi encerrado definitivamente pelo aluno. Os gigabytes de vídeo brutos do Behavython/DeepLabCut serão documentados em um apêndice crítico-metodológico, mas não serão usados para inferência causal sobre CA3.
  3. **Pivô Metodológico para a Neuroengenharia Computacional**: Migração total para modelagem computacional in silico no **Brian 2**, alinhando-se aos trabalhos de modelagem e dinâmica não linear do NNC (ex: João Pedro Carvalho Moreira, Vinícius Rezende Carvalho).
* **Cronograma Crítico**:
  * Final de Outubro / Início de Novembro de 2026: Reaproximação formal com os orientadores com protótipo funcional e proposta in silico.
  * 03/11/2026: Prazo de inscrição/reingresso no processo seletivo do PPGEE.

---

## 2. Fatos e Resultados Científicos Consolidados

1. **Aplicação do Método Científico Rigoroso (Santos / Feynman)**:
   * Proibição estrita de viés de confirmação, bajulação ou ajuste de narrativas para tentar forçar conclusões. Assume-se ignorância *a priori*.
2. **Refutação da Hipótese Ingênua de Bloqueio da ChR2**:
   * Uma hipótese anterior sugeria que a ChR2 colapsava por despolarização contínua engolindo metade dos bits. O experimento computacional em [`Codigos/teste_metodo_cientifico_laura_msf_vs_msr.py`](file:///c:/Users/wfran/Documents/Antigravity/Mestrado%20UFMG/Codigos/teste_metodo_cientifico_laura_msf_vs_msr.py) provou que **a ChR2 não sofreu bloqueio total**, disparando 59 de 60 pulsos no padrão fixo (MSf) e 54 de 60 no padrão aleatório (MSr).
3. **Explicação da Inconclusividade de c-Fos de Laura Costa (2026)**:
   * A integral de cálcio intracelular acumulada ($\int [Ca^{2+}] dt$, proxy de c-Fos) divergiu em **apenas 7,48%** entre MSf e MSr. Como a imunofluorescência biológica tem ruído de bancada superior a $15\text{--}25\%$, o c-Fos atuou como filtro passa-baixa e afogou a diferença no ruído, corroborando rigorosamente o valor empírico de $p = 0{,}9888$ encontrado na dissertação.
4. **Princípio Biofísico Estabelecido**:
   * Em nível de neurônio único desacoplado, sinais temporais que entregam a mesma energia média produzem resposta celular idêntica.
   * **A sintaxe temporal só sobrevive se houver dinâmica de rede recorrente com inibição por realimentação (interneurônios GABAérgicos rápidos) e/ou acoplamento em fase fechada (*closed-loop phase-locking*)**.

---

## 3. Infraestrutura Instalada e Disponível no Workspace

### A. Ferramentas e Bibliotecas Python
* Ambiente Virtual: `Codigos/.venv` (Python 3.14, Brian2 2.10.1, Matplotlib 3.11.2, PyMuPDF 1.28.2).

### B. Catálogo de 13 Habilidades Científicas (`.agents/skills/`)
1. `scientific-critical-thinking` (avaliação de rigor, viés de confirmação, variáveis de confusão, GRADE/Cochrane).
2. `hypothesis-generation` (formulação de hipóteses formais testáveis $H_0$ e $H_1$).
3. `experimental-design` (decisões pré-experimento, pareamento, controles, prevenção de pseudoreplicação).
4. `literature-review` (revisão sistemática de literatura e verificação de citações).
5. `scholar-evaluation` (avaliação qualitativa e formativa de trabalhos acadêmicos).
6. `peer-review` (revisão por pares crítica e detecção de pontos fracos).
7. `scientific-writing` (redação científica estruturada IMRAD).
8. `statistical-analysis` (testes de hipóteses estatísticos inferenciais).
9. `statistical-power` (cálculo de poder estatístico e tamanho amostral).
10. `nwb-conversion` (padronização Neurodata Without Borders via PyNWB).
11. `neuropixels-analysis` (processamento de eletrofisiologia via SpikeInterface).
12. `neurokit2` (processamento de sinais fisiológicos e oscilações).
13. `database-lookup` (consulta estruturada a bases biológicas).

### C. Inventário de Documentos Persistidos
* [`DIRETRIZES_MESTRADO_ANTIGRAVITY.md`](file:///c:/Users/wfran/Documents/Antigravity/Mestrado%20UFMG/DIRETRIZES_MESTRADO_ANTIGRAVITY.md) — Diretrizes permanentes do aluno e método científico.
* [`artigos_nnc/PLANO_ESTUDO_IZHIKEVICH_BRIAN2.md`](file:///c:/Users/wfran/Documents/Antigravity/Mestrado%20UFMG/artigos_nnc/PLANO_ESTUDO_IZHIKEVICH_BRIAN2.md) — Parametrização da micro-rede de CA3 ($N=1000$) e os 3 experimentos (NPS Cota 2023, Padrão 1 vs 2 Wagner, Malha Fechada Teta).
* [`GUIA_TRANSIÇÃO_E_ARVORE_DECISAO_BRIAN2.md`](file:///c:/Users/wfran/Documents/Antigravity/Mestrado%20UFMG/GUIA_TRANSI%C3%87%C3%83O_E_ARVORE_DECISAO_BRIAN2.md) — Árvore de decisão arquitetural para modelagem in silico.
* [`artigos_nnc/RELATORIO_CIENTIFICO_LAURA_MSF_VS_MSR.md`](file:///c:/Users/wfran/Documents/Antigravity/Mestrado%20UFMG/artigos_nnc/RELATORIO_CIENTIFICO_LAURA_MSF_VS_MSR.md) — Relatório da simulação controlada MSf vs MSr.
* [`artigos_nnc/REAVALIACAO_COTA_E_PROJETO_MESTRADO_BRIAN2.md`](file:///c:/Users/wfran/Documents/Antigravity/Mestrado%20UFMG/artigos_nnc/REAVALIACAO_COTA_E_PROJETO_MESTRADO_BRIAN2.md) — Reavaliação detalhada do artigo de Cota (2023).

---

## 4. Missão para a Nova Conversa

Na nova conversa, o assistente deverá:
1. Ler este documento e as diretrizes permanentes.
2. Ativar as novas habilidades científicas (`scientific-critical-thinking`, `hypothesis-generation`, `peer-review`, `experimental-design`).
3. Reavaliar criticamente todo o histórico e apresentar uma **análise comparativa de caminhos ótimos para a dissertação de mestrado no PPGEE**:
   * **Caminho A**: O Gêmeo Digital da NPS (Cota et al., 2023) — Foco em epilepsia, quebra de atratores e dinâmica não linear.
   * **Caminho B**: A Teoria da Sintaxe Temporal em CA3 — Foco na discriminabilidade biofísica dos Padrões 1 e 2 via inibição recorrente e estimulação em malha fechada.
   * **Caminho C**: Dissertação Híbrida / Unificada — Investigação da ressonância de fase teta conectando a teoria de NPS com a eletroestimulação do NNC.
4. Definir formalmente as hipóteses $H_0$ e $H_1$ do caminho escolhido e implementar a simulação da micro-rede de Izhikevich no Brian 2.
