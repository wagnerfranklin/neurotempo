# REAVALIAÇÃO CRÍTICA: ARTIGO COTA ET AL. (2023) E PROJETO DE MESTRADO WAGNER FRANKLIN
## Abordagem por Neuroengenharia Computacional no Brian 2 (PPGEE / UFMG)

---

## 1. Contexto e Reavaliação à Luz do Método Científico

### 1.1. O que o Experimento Computacional Controlado nos Ensinou
A simulação quantitativa rigorosa (`teste_metodo_cientifico_laura_msf_vs_msr.py`) estabeleceu um fato físico e biofísico:
> **Em nível de neurônio individual desacoplado, sinais temporais que entregam a mesma energia total (6 pulsos em 140 ms) produzem respostas celulares essencialmente idênticas (diferença de cálcio de apenas 7,48% e variação nula em STDP feedforward).**
> A capacitância de membrana ($C_m$) e os tempos de decaimento iônico/enzimático atuam como filtros passa-baixa, eliminando as sutilezas da sintaxe temporal de milissegundos.

Esse resultado muda radicalmente a interpretação tanto do artigo de Cota et al. (2023) quanto do projeto original de mestrado do Wagner.

---

### 1.2. Reavaliação do Artigo Cota, Cançado & Moraes (2023)
* **A Tese Teórica do Artigo**: A estimulação não-periódica com lei de potência (NPS, média de 4 Hz) suprime crises epilépticas e quebra atratores patológicos, enquanto a estimulação periódica regular (4 Hz) sincroniza e piora o atrator hipersincrônico.
* **O Gargalo Inerente da Bancada**: 
  O artigo de 2023 é um manifesto **teórico e empírico de nível macroscópico** (dados de LFP e crises comportamentais com PTZ). Ele postula que o mecanismo subjacente é a "plasticidade STDP competitiva" e a "fragmentação de rotas sinápticas". 
  **Contudo, o NNC nunca pôde verificar esse mecanismo diretamente no nível celular/sináptico na bancada**. 
  *Motivo biofísico*: O pulso elétrico ou óptico gera um **artefato de estimulação** que satura os amplificadores de registro por vários milissegundos, tornando impossível registrar os spikes e as variações de condutâncias sinápticas exatas ocorridas durante o estímulo. Além disso, não existe tecnologia biológica capaz de ler simultaneamente os pesos sinápticos individuais de centenas de sinapses em tempo real.
* **Diagnóstico**: O artigo de 2023 carece de uma **comprovação biofísica mecanicista em malha fina**.

---

### 1.3. Reavaliação do Projeto Original do Wagner
* **Proposta Original**: "Programação de Memórias Contextuais Artificiais por Estimulações Temporalmente Organizadas" (CA3 dorsal, eletrodos bipolares, tarefa de reconhecimento de objetos de Dix & Aggleton, 1999).
* **Protocolo**:
  * Padrão 1: `1010101101` ($7{,}14\text{ Hz}$, $25\ \mu\text{A}$, 6 pulsos ativos).
  * Padrão 2: `1110010111` ($7{,}14\text{ Hz}$, $25\ \mu\text{A}$, 6 pulsos ativos).
* **O Ponto Cego de Bancada**:
  Na bancada comportamental cega (experimentos C1 a C4), assumiu-se que o cérebro interpretaria o Padrão 1 e o Padrão 2 como "contextos diferentes". 
  Porém, se a rede CA3 não possuir uma ressonância inibitória sintonizada na diferença específica entre essas duas palavras, a carga líquida injetada é exatamente a mesma. A frustração de bancada (resultados inconsistentes entre animais) não decorre necessariamente de "erro cirúrgico", mas do fato de que **o estímulo pode não produzir diferenciação funcional na microestrutura do circuito**.
* **Diagnóstico**: Ir para a bancada sem mapear o espaço de parâmetros no computador é atuar por tentativa e erro em um sistema altamente não linear.

---

## 2. O Que SÓ É Possível Fazer e Explicar com o Brian 2

| Limitação Insuperável da Bancada (In Vivo) | Solução Exclusiva via Brian 2 (In Silico) |
| :--- | :--- |
| **Artefato de Estimulação**: O choque elétrico cega o amplificador por 2–10 ms, impedindo a leitura dos spikes imediatos. | **Transparência Total**: Resolução temporal de $0{,}01\text{ ms}$ sem saturação instrumental. Monitoramento simultâneo de condutâncias ($g_{\text{Na}}, g_{\text{K}}, g_{\text{AMPA}}, g_{\text{GABA}}$). |
| **Inobservabilidade Sináptica**: Impossível medir a evolução dos pesos individuais ($w_{ij}$) de milhares de conexões em um tecido vivo. | **Acesso Direto à Matriz de Conectividade**: Rastreamento da evolução da matriz $W(t)$ sob regras de plasticidade STDP milissegundo a milissegundo. |
| **Variabilidade Incontrolável**: Diferenças de impedância do eletrodo, inflamação glial, posição micrométrica da cânula, estresse do animal. | **Reprodutibilidade Estrita e Isolamento Causal**: Controle paramétrico determinístico, permitindo alterar uma única variável (ex: $\tau_{\text{GABA}}$) mantendo todo o resto idêntico. |
| **Custo e Tempo de Varredura Paramétrica**: Testar 10 padrões em 5 frequências exigiria centenas de animais e anos de biotério. | **Exploração Rápida de Espaço de Estados**: Execução em lote (*batch grid search*) com geração de código C++ em minutos ou horas. |

---

## 3. Três Estudos de Caso Propostos para a Dissertação (Brian 2)

### Estudo de Caso 1: Teste Mecanicista da NPS (Cota et al., 2023) — Quebra de Atratores
* **Objetivo**: Provar computacionalmente a hipótese central do Prof. Márcio: a NPS de 4 Hz desmantela atratores patológicos sem saturar o circuito, enquanto a estimulação periódica de 4 Hz reforça o atrator.
* **Arquitetura da Rede**:
  * População recorrente $E \leftrightarrow I$ de CA3: 800 neurônios excitatórios piramidais + 200 interneurônios inibitórios GABAérgicos rápidos (células em cesto).
  * Sinapses recorrentes $E \to E$ com plasticidade STDP.
* **Protocolo Experimental**:
  1. Condição Basal: Induzir um atrator hiper-síncrono (análogo à atividade epileptiforme ou engrama hiper-reverberante).
  2. Protocolo Periódico: Injetar pulsos regulares a 4 Hz ($\Delta t = 250\text{ ms}$).
  3. Protocolo NPS: Injetar pulsos com intervalos sorteados de uma distribuição de Lei de Potência ($P(\text{IPI}) \propto \text{IPI}^{-\alpha}$, média = 4 Hz).
* **Métricas de Saída**:
  * Distribuição dos pesos sinápticos finais $W(t)$ (LTP vs LTD).
  * Coeficiente de Sincronia Populacional e Entropia de Disparo.
* **Contribuição**: Primeira comprovação biofísica de canal e sinapse do modelo de Cota et al. (2023).

---

### Estudo de Caso 2: Discriminabilidade Biofísica dos Padrões do Wagner (Padrão 1 vs Padrão 2)
* **Objetivo**: Determinar em quais condições biofísicas de rede a microestrutura temporal do Padrão 1 (`1010101101`) diverge do Padrão 2 (`1110010111`).
* **Mecanismo Testado**: Ação dos interneurônios inibitórios com diferentes cinéticas de decaimento ($\tau_{\text{GABA}_A} = 5\text{ ms}$ a $25\text{ ms}$).
  * No Padrão 1, bits '1' ocorrem alternados ou aos pares (`1010101101`).
  * No Padrão 2, há uma trinca de bits '1' consecutivos (`1110010111`).
  * *Hipótese de Engenharia*: A trinca consecutiva colide com o pico da condutância inibitória gerada pelo primeiro pulso. A rede só conseguirá discriminar os dois padrões se a constante de tempo da inibição for menor que o intervalo entre os bits ($14\text{ ms}$).
* **Métricas de Saída**:
  * Distância de Van Rossum ou Victor-Purpura entre os trens de disparos da população.
  * Resposta diferencial pós-sináptica em CA1 (alvo eferente).
* **Contribuição**: Explica formalmente por que o experimento de bancada do Wagner pode ter falhado ou funcionado apenas em condições limítrofes.

---

### Estudo de Caso 3: Acoplamento em Malha Fechada (*Phase-Locking*) e Filtro de Fase Teta
* **Objetivo**: Avaliar se a eficácia de gravação de memória depende da estimulação estar acoplada à fase teta endógena (*closed-loop*).
* **Protocolo**:
  * Injetar oscilação de corrente sinusoidal de fundo ($7{,}14\text{ Hz}$, simulando o ritmo teta gerado pelo Septo Medial).
  * Comparar:
    1. Estimulação em malha aberta (pulsos disparam em fases aleatórias da onda teta).
    2. Estimulação em malha fechada ancorada no vale da onda (máxima excitabilidade / inibição mínima).
    3. Estimulação em malha fechada ancorada no pico da onda (mínima excitabilidade / inibição máxima).
* **Métricas de Saída**:
  * Valor de Bloqueio de Fase ($\text{PLV}$).
  * Potenciação de Longa Duração líquida ($\Delta W_{\text{STDP}}$).
* **Contribuição**: Estabelece os requisitos de controle de engenharia (latência máxima de detecção e disparo) para projetar um estimulador cerebral de malha fechada no NNC.

---

## 4. Como Estruturar o Trabalho para o PPGEE / UFMG

A dissertação deixa de ser uma tentativa frustrada de cirurgia de bancada e se torna uma **Dissertação de Engenharia de Sistemas Dinâmicos e Neuroengenharia Computacional**:

1. **Capítulo 1**: Introdução Teórica — Oscilações teta, sintaxe temporal e a teoria de NPS do NNC (Cota et al., 2023).
2. **Capítulo 2**: O Modelo Biofísico no Brian 2 — Formalização matemática das equações diferenciais dos neurônios de CA3/CA1, sinapses STDP e cinéticas de transdução.
3. **Capítulo 3**: Análise Crítica dos Ensaios de Bancada — Simulação do protocolo de Laura Costa (por que c-Fos e ChR2 mascaram padrões temporais) e do protocolo de Wagner Franklin (análise do teste C4).
4. **Capítulo 4**: Resultados in silico dos Estudos de Caso (Quebra de Atratores por NPS, Discriminabilidade de Padrões P1 vs P2 e Estimulação em Malha Fechada).
5. **Capítulo 5**: Diretrizes de Projeto para a Próxima Geração de Neuroestimuladores do NNC.
