# GUIA DE INTEGRAÇÃO: SCIENTIFIC AGENT SKILLS NO ANTIGRAVITY
## Catálogo Curado Instalado para o Projeto de Mestrado (PPGEE / UFMG)

---

## 1. Status da Instalação Local

Todas as 13 habilidades científicas selecionadas foram instaladas diretamente no diretório do projeto:
`c:\Users\wfran\Documents\Antigravity\Mestrado UFMG\.agents\skills\`

O Antigravity faz a descoberta automática deste diretório na inicialização de cada sessão de trabalho.

---

## 2. Mapa de Habilidades Curadas por Necessidade Metodológica

### A. Interpretação e Síntese de Texto Científico
1. **`literature-review`**:
   * **Função**: Conduzir revisões bibliográficas sistemáticas e temáticas seguindo metodologia acadêmica rigorosa.
   * **Aplicação no Mestrado**: Analisar artigos do laboratório (Cota 2023, teses de Laura Costa, João Pedro Moreira, Vinícius Carvalho) extraindo premissas, variáveis dependentes e lacunas de conhecimento.
2. **`scholar-evaluation`**:
   * **Função**: Avaliação formativa, qualitativa e baseada em evidências de textos acadêmicos (artigos, rascunhos, propostas de pesquisa).
   * **Aplicação no Mestrado**: Avaliar criticamente a sua própria proposta de dissertação e artigos de referência antes de submeter a orientadores.

---

### B. Aplicação do Método Científico, Pensamento Crítico e Falseabilidade
3. **`scientific-critical-thinking`**:
   * **Função**: Avaliação sistemática de rigor científico. Detecta vieses de confirmação, variáveis de confusão (*confounding*), falhas de validade interna e externa, e avalia a qualidade da evidência (estruturas GRADE e Cochrane).
   * **Aplicação no Mestrado**: Garantir que as conclusões sobre estimulação neural decorram de relações causais comprovadas, impedindo conclusões precipitadas.
4. **`hypothesis-generation`**:
   * **Função**: Estruturação formal de hipóteses testáveis e falsificáveis. Transforma uma observação em um conjunto transparente de explicações candidatas ($H_0$ e $H_1$) com critérios operacionais de refutação pré-declarados.
   * **Aplicação no Mestrado**: Formular as hipóteses mecanicistas sobre a quebra de atratores por NPS e a ressonância inibitória em CA3 antes da execução computacional.
5. **`experimental-design`**:
   * **Função**: Protocolo de decisões tomadas **antes** da coleta de dados (variáveis controladas, variáveis manipuladas, pareamento, prevenção de pseudoreplicação e viés sistemático).
   * **Princípio Central**: *"Nenhuma análise posterior pode resgatar um desenho experimental confuso ou contaminado"*.
   * **Aplicação no Mestrado**: Desenhar os experimentos computacionais no Brian 2 com varredura paramétrica limpa e grupos controle idênticos.
6. **`peer-review`**:
   * **Função**: Simulação de um revisor anônimo de periódico de alto impacto. Avalia validade de métodos, consistência de dados e suficiência de evidências.
   * **Aplicação no Mestrado**: Atuar como "advogado do diabo" contra o seu projeto, antecipando as críticas e objeções que a banca de qualificação ou defesa do PPGEE fará.

---

### C. Redação, Análise Quantitativa e Padronização
7. **`scientific-writing`**:
   * **Função**: Redação acadêmica técnica sem inventar evidências ou ocultar incertezas, organizada na estrutura canônica IMRAD (Introdução, Métodos, Resultados e Discussão).
8. **`statistical-analysis`**:
   * **Função**: Execução de testes estatísticos apropriados (paramétricos vs não-paramétricos, ANOVA, GLM, correções de múltiplos testes FDR/Bonferroni).
9. **`statistical-power`**:
   * **Função**: Cálculo de poder estatístico (*a priori* power analysis) e tamanho ótimo de amostra/repetições.
10. **`nwb-conversion`**:
    * **Função**: Conversão e validação de sinais eletrofisiológicos para o padrão aberto **Neurodata Without Borders (NWB)** via `PyNWB` / `NeuroConv`.
11. **`neuropixels-analysis`**:
    * **Função**: Processamento de sinais de sondas multicanais e matrizes de microeletrodos via `SpikeInterface` (filtragem, ordenação de spikes e métricas de isolamento).
12. **`neurokit2`**:
    * **Função**: Processamento de biosinais (transformadas tempo-frequência, detecção de fases de ondas cerebrais, filtragem Butterworth/Wavelet).
13. **`database-lookup`**:
    * **Função**: Acesso rastreável a bancos de dados biológicos e bibliográficos públicos para coleta de parâmetros com procedência formal.

---

## 3. Próximo Passo Operacional

Com todas as 13 habilidades instaladas em `.agents/skills/`, a infraestrutura técnica está concluída. 

**Ao abrir uma nova conversa no Antigravity**:
1. O sistema carregará formalmente as 13 habilidades científicas no seu catálogo nativo.
2. A nova conversa lerá os arquivos persistidos em disco (`DIRETRIZES_MESTRADO_ANTIGRAVITY.md` e `artigos_nnc/PLANO_ESTUDO_IZHIKEVICH_BRIAN2.md`).
3. O trabalho começará com a janela de contexto 100% limpa, sem poluição de memória e com todo o arsenal analítico e computacional pronto para uso.
