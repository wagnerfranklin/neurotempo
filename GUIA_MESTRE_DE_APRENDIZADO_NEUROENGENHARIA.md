# GUIA MESTRE DE NEUROENGENHARIA E NEUROCIÊNCIA COMPUTACIONAL
## Do Zero Absoluto à Modelagem de Memórias Artificiais no Hipocampo
### Um Roteiro de Aprendizado Acelerado Baseado nas 20 Regras do SuperMemo para Engenheiros Mecatrônicos

---

## 1. O MANIFESTO METODOLÓGICO: AS 20 REGRAS DO SUPERMEMO APLICADAS À SUA ROTINA

Para você dominar este conteúdo sem desanimar e sem tentar "decorar a biologia", este guia foi construído sob os princípios científicos de formulação do conhecimento de Piotr Wozniak (SuperMemo):

1. **Regra 1: Não tente memorizar o que não compreendeu.** Se uma frase em biologia parecer magia, pare. Traduza para circuito, diagrama de blocos ou equação de estado.
2. **Regra 2: Aprenda o todo antes dos detalhes (Abordagem Top-Down).** Primeiro você enxerga a arena e o camundongo; depois o hipocampo; depois a sinapse; depois o canal iônico.
3. **Regra 3: Construa sobre o básico.** Não tente entender STDP sem entender o que é potencial de ação; não tente entender potencial de ação sem entender capacitor de membrana.
4. **Regra 4: Princípio da Informação Mínima.** Os conceitos e exercícios são atômicos. Cada pergunta testa uma e apenas uma relação causal.
5. **Regra 5: Omissão de palavras (Cloze Deletion).** Use os exercícios de preenchimento para fixar a sintaxe técnica da neurofisiologia.
6. **Regra 13: Ancoragem em memórias prévias.** Todo conceito biológico é imediatamente pareado com um equivalente da Engenharia Mecatrônica (Leis de Kirchhoff, Circuitos RC, Fontes Thevenin, Filtros Passa-Baixa, Ganhos Adaptativos e Máquinas de Estado).
7. **Regra 18: Fontes explícitas.** Cada tópico aponta para o arquivo PDF exato que está na sua pasta `PARA_GEMINI_NOTEBOOK` com as páginas precisas.

---

## 2. O MAPA GERAL DO CONHECIMENTO (BIG PICTURE ROADMAP)

```
[ NÍVEL MACRO: O COMPORTAMENTO E O PROBLEMA BIOLÓGICO ]
  │  Tarefa de Reconhecimento Objeto-Contexto (Dix & Aggleton, 1999)
  │  Animais exploram o NOVO e habituam ao FAMILIAR.
  ▼
[ NÍVEL MESO-ALTO: O CIRCUITO DA MEMÓRIA (O HIPOCAMPO) ]
  │  Circuito Trissináptico: Córtex Entorrinal -> Giro Denteado -> CA3 -> CA1
  │  CA3 = Rede Recorrente Auto-associativa (Pattern Completion)
  │  CA1 = Comparador de Mismatch (Detector de Novidade)
  ▼
[ NÍVEL MESO: A FÍSICA DAS OSCILAÇÕES E ESTIMULAÇÃO ]
  │  Ritmo Teta (7.14 Hz) = O clock mestre de sincronização
  │  Microestimulação Elétrica: Padrão 1 vs Padrão 2 como contexto artificial
  ▼
[ NÍVEL MICRO-ALTO: A REGRA DE APRENDIZADO (PLASTICIDADE) ]
  │  Regra de Hebb e STDP (Spike-Timing-Dependent Plasticity)
  │  Ajuste de ganhos sinápticos baseado na diferença temporal (dt em ms)
  ▼
[ NÍVEL MICRO: O GATILHO E A SINAPSE (A COMUNICAÇÃO) ]
  │  Potencial de Ação: A chave não-linear (Spike de 1 ms)
  │  Sinapse Química: Conversão de tensão em corrente pós-sináptica (EPSP / IPSP)
  ▼
[ NÍVEL ZERO: O NÓ ELEMENTAR (O QUE É UM NEURÔNIO?) ]
  │  O Neurônio como Circuito Elétrico RC: Bicamada lipídica = Capacitor; Canais = Condutâncias
```

---

## 3. OS MÓDULOS DE APRENDIZADO ATÔMICOS

---

### MÓDULO 0: O NÍVEL ZERO — O QUE É UM NEURÔNIO?
**Tempo estimado de estudo:** 40 minutos

#### A. A Metáfora da Mecatrônica
Um neurônio não é uma gosma mística. Ele é um **nó de circuito eletroquímico com um capacitor em paralelo com resistores variáveis e fontes de tensão**.
* **O Corpo Celular (Soma)**: É o nó principal onde todas as correntes elétricas entram e se somam pela Lei de Kirchhoff das Correntes.
* **A Membrana Celular**: É uma camada de gordura isolante de $5\,\text{nm}$ de espessura. Na física, duas camadas condutoras separadas por um isolante fino formam um **Capacitor** ($C_m \approx 1\,\mu\text{F/cm}^2$).
* **Os Canais Iônicos**: São poros de proteínas que deixam íons (cargas elétricas) passarem. Funcionam como **Condutâncias Elétricas ($g = 1/R$)**.
* **As Bombas Iônicas (Sódio/Potássio)**: Gastam energia para jogar sódio para fora e potássio para dentro, criando um desequilíbrio químico de cargas. Funcionam como **Fontes de Tensão Contínua (Baterias Thevenin)** que mantêm o interior do neurônio em cerca de **$-65\,\text{mV}$** em repouso.
* **Os Dendritos**: São os condutores de entrada (cabos de sinal com capacitância distribuída e resistência).
* **O Axônio**: É a linha de transmissão de saída (o barramento que envia o pulso digital para outros nós).

#### B. O que ler (Fonte Exata)
* **Arquivo**: `PARA_GEMINI_NOTEBOOK/11 - KANDEL - Cap 06 - Potencial de Membrana e Propriedades Eletricas.pdf`
* **Páginas**: 144 a 155.
* **O que focar**: Olhe a Figura 6-1 e a Figura 6-4. Veja o circuito equivalente de circuito RC que o Kandel desenha. Você vai se sentir em casa: é exatamente análise de circuitos de primeiro ano de engenharia!

#### C. Banco de Flashcards Atômicos (Active Recall - SuperMemo)

1. **P:** Qual elemento físico da membrana celular do neurônio se comporta como um capacitor elétrico?
   * **R:** A bicamada lipídica isolante (que separa as cargas iônicas intra e extracelulares).
2. **P:** Qual elemento da membrana se comporta como uma condutância elétrica variável ($g$)?
   * **R:** Os canais iônicos (poros proteicos permeáveis a íons específicos).
3. **P:** O que representa a fonte de tensão equivalente (bateria) no circuito do neurônio?
   * **R:** O potencial de equilíbrio químico dos íons (equação de Nernst), mantido pelas bombas iônicas ativas.
4. **P:** Qual é o valor típico do potencial de membrana em repouso de um neurônio de mamífero?
   * **R:** Aproximadamente $-65\,\text{mV}$ (o interior é negativo em relação ao exterior).
5. **P (Cloze):** A membrana de um neurônio atua como um filtro [passa-baixa], porque possui uma [capacitância] que atrasa e suaviza variações bruscas de tensão.

#### D. Critério de Domínio
Explique em 60 segundos, sem olhar o papel: *"Por que o neurônio pode ser modelado como um circuito RC em paralelo com uma bateria?"*

---

### MÓDULO 1: O GATILHO NÃO-LINEAR — O POTENCIAL DE AÇÃO
**Tempo estimado de estudo:** 1 hora

#### A. A Metáfora da Mecatrônica
Se o neurônio fosse só um circuito RC passivo, um sinal elétrico morreria depois de percorrer alguns milímetros devido à dissipação ôhmica.
Para transmitir informação a longas distâncias (do cérebro até a pata do camundongo), o sistema nervoso inventou um **repetidor digital regenerativo não-linear**: o **Potencial de Ação (Spike)**.
* **O Limiar (Threshold)**: Quando a soma das correntes que entram no neurônio faz a tensão subir de $-65\,\text{mV}$ para cerca de **$-50\,\text{mV}$**, portas de canais de Sódio sensíveis à tensão se abrem repentinamente.
* **O Feedback Positivo**: A entrada de Sódio despolariza a célula, o que abre mais canais de Sódio. Ocorre uma avalanche não-linear ultrarrápida: a tensão dispara até $+30\,\text{mV}$ em menos de $1\,\text{ms}$.
* **O Reset**: Os canais de sódio se fecham sozinhos (inativação) e canais de Potássio se abrem para drenar carga positiva, jogando a tensão de volta para $-70\,\text{mV}$.
* **O Modelo de Izhikevich (2003)**: Em vez de resolver as 4 equações diferenciais acopladas de Hodgkin-Huxley cheias de exponenciais, o Izhikevich mostrou que **duas equações simples** fazem exatamente o mesmo:
  $$\dot{v} = 0.04v^2 + 5v + 140 - u + I$$
  $$\dot{u} = a(bv - u)$$
  $$\text{se } v \ge 30\,\text{mV}, \text{ então } v \leftarrow c \text{ e } u \leftarrow u + d$$
  Onde $v$ é a tensão, $u$ é a variável de recuperação (amortecimento) e $I$ é a corrente injetada (pelo eletrodo ou sinapses).

#### B. O que ler (Fontes Exatas)
1. **Arquivo**: `PARA_GEMINI_NOTEBOOK/12 - KANDEL - Cap 07 - Potencial de Acao e Propagacao de Sinal.pdf`
   * **Páginas**: 163 a 174. Entenda a curva do spike e o conceito de período refratário.
2. **Arquivo**: `PARA_GEMINI_NOTEBOOK/02 - ARTIGO CHAVE - Izhikevich (2003) - Simple model of spiking neurons.pdf`
   * **Páginas**: Leia o artigo inteiro (são só 4 páginas!). Olhe a **Figura 1**.

#### C. Banco de Flashcards Atômicos (SuperMemo)

1. **P:** O que acontece quando a despolarização da membrana atinge o limiar (*threshold*)?
   * **R:** Abrem-se os canais de sódio voltagem-dependentes, disparando um potencial de ação no formato tudo-ou-nada.
2. **P:** O que é o período refratário de um neurônio?
   * **R:** O intervalo de tempo logo após o disparo em que o neurônio não consegue disparar outro potencial de ação, limitando a frequência máxima de disparo.
3. **P:** No modelo de Izhikevich, o que acontece matematicamente quando a variável $v$ atinge $30\,\text{mV}$?
   * **R:** Ocorre um chaveamento discreto: $v$ é resetado para o valor $c$, e $u$ é incrementado por $d$.
4. **P (Cloze):** Os neurônios piramidais excitatórios de CA3 exibem disparo do tipo [regular spiking / adaptação de frequência], enquanto a maioria dos interneurônios inibitórios exibe disparo do tipo [fast spiking / disparos rápidos e sem adaptação].

#### D. Critério de Domínio
Desenhe em um rascunho o gráfico de $v(t)$ de um potencial de ação e aponte: onde está o repouso, o limiar, o pico e o reset.

---

### MÓDULO 2: A REDE E A COMUNICAÇÃO — SINAPSES E INTEGRAÇÃO
**Tempo estimado de estudo:** 45 minutos

#### A. A Metáfora da Mecatrônica
Um potencial de ação que chega ao fim do axônio precisa falar com o próximo neurônio. Isso ocorre na **Sinapse Química**.
* **O Transmissor (Terminal Pré-sináptico)**: O spike elétrico faz entrar cálcio, liberando pequenos pacotes químicos (neurotransmissores) na fenda sináptica de $20\,\text{nm}$.
* **O Receptor (Terminal Pós-sináptico)**: Os químicos se ligam a receptores na membrana seguinte e abrem canais iônicos, gerando uma corrente de entrada $I_{\text{syn}}(t)$.
* **Dois Tipos de Sinal**:
  1. **Glutamato (Excitatório)**: Injeta corrente positiva, despolariza o neurônio, puxa a tensão para cima (EPSP - *Excitatory Postsynaptic Potential*).
  2. **GABA (Inibitório)**: Injeta carga negativa, hiperpolariza o neurônio, freia o disparo e trava a rede (IPSP - *Inhibitory Postsynaptic Potential*).
* **Integração no Nó**: O neurônio pós-sináptico recebe centenas de EPSPs e IPSPs simultaneamente. Ele faz uma **somação temporal e espacial**. Se a soma líquida ultrapassar o limiar, ele dispara.

#### B. O que ler (Fonte Exata)
* **Arquivo**: `PARA_GEMINI_NOTEBOOK/13 - KANDEL - Cap 10 - Integracao Sinaptica no SNC.pdf`
* **Páginas**: 218 a 230.
* **O que focar**: Figuras 10-1 e 10-2 (Somação temporal e somação espacial).

#### C. Banco de Flashcards Atômicos (SuperMemo)

1. **P:** Qual é o principal neurotransmissor excitatório do sistema nervoso central de mamíferos?
   * **R:** O Glutamato (gera potenciais excitatórios - EPSPs).
2. **P:** Qual é o principal neurotransmissor inibitório do encéfalo?
   * **R:** O GABA (ácido gama-aminobutírico, gera potenciais inibitórios - IPSPs).
3. **P:** Qual a diferença entre somação espacial e somação temporal em um neurônio?
   * **R:** Espacial é a soma de sinais vindos de diferentes sinapses simultaneamente; temporal é a soma de sinais repetidos que chegam em rápida sucessão na mesma sinapse.
4. **P (Cloze):** No simulador Brian 2, uma sinapse excitatória é modelada como um acréscimo pontual na [condutância pós-sináptica ou corrente], deflagrado no exato [timestamp] em que o neurônio pré-sináptico atinge o limiar.

#### D. Critério de Domínio
Diferencie com clareza: o que acontece no neurônio pós-sináptico se ele receber 10 sinapses de Glutamato versus 10 sinapses de GABA?

---

### MÓDULO 3: A ARQUITETURA DA MEMÓRIA — O CIRCUITO HIPOCAMPAL
**Tempo estimado de estudo:** 1 hora

#### A. A Metáfora da Mecatrônica
Agora subimos para o nível do circuito. O **Hipocampo** é a unidade de processamento e indexação de memória episódica do cérebro.
Pense nele como uma **arquitetura de pipeline trissináptico com buffer de realimentação**:

```
[ Córtex Entorrinal (Entrada de Dados) ]
      │  (Via Perfurante)
      ▼
[ Giro Denteado (DG) ]  -----> Filtro de Esparsidade / Separação de Padrões
      │  (Fibras Musgosas)
      ▼
[ CA3 (Corno de Amon 3) ] ---> MEMÓRIA AUTO-ASSOCIATIVA / REDE RECORRENTE
      │                        (Possui conexões de realimentação nele mesmo!)
      │  (Colaterais de Schaffer)
      ▼
[ CA1 (Corno de Amon 1) ] ---> COMPARADOR DE ERRO / DETECTOR DE NOVIDADE
      │
      ▼
[ Saída para o Córtex ]
```

* **A Mágica de CA3**: Os axônios dos neurônios piramidais de CA3 se ramificam e fazem sinapse **nos próprios neurônios de CA3** (colaterais recorrentes). Na engenharia, isso é um **sistema com realimentação positiva / rede de Hopfield**. Ele serve para fazer **Completamento de Padrão (*Pattern Completion*)**: se você apresenta apenas uma parte da memória (ex: o cheiro de um objeto), a rede recorrente inteira entra em ressonância e reconstrói a memória inteira!
* **O Papel de CA1**: CA1 recebe a memória recuperada de CA3 e recebe a informação sensorial em tempo real do Córtex. Se houver descompasso (*mismatch*), CA1 dispara forte: *"Isto é NOVO!"*.

#### B. O que ler (Fonte Exata)
* **Arquivo**: `PARA_GEMINI_NOTEBOOK/16 - KANDEL - Cap 67 - Hipocampo e Armazenamento de Memoria Explicita.pdf`
* **Páginas**: 1329 a 1345.
* **O que focar**: A anatomia funcional do circuito trissináptico (Fig. 67-1 e 67-2) e a seção sobre células de lugar (*place cells*).

#### C. Banco de Flashcards Atômicos (SuperMemo)

1. **P:** Quais são as três sinapses consecutivas que compõem o circuito trissináptico hipocampal clássico?
   * **R:** 1) Via perfurante (Córtex Entorrinal $\rightarrow$ Giro Denteado); 2) Fibras musgosas (Giro Denteado $\rightarrow$ CA3); 3) Colaterais de Schaffer (CA3 $\rightarrow$ CA1).
2. **P:** Qual característica anatômica fundamental torna a região CA3 do hipocampo capaz de operar como uma memória auto-associativa?
   * **R:** A presença massiva de conexões axonais recorrentes (sinapses que neurônios piramidais fazem entre si na mesma estrutura).
3. **P:** O que é a função de "completamento de padrão" (*pattern completion*) no hipocampo?
   * **R:** A capacidade da rede de recuperar uma representação mnemônica completa a partir de uma pista sensorial parcial ou degradada.
4. **P (Cloze):** No seu projeto de mestrado, o eletrodo de estimulação elétrica foi implantado na região [CA3], e os eletrodos de registro foram implantados bilateralmente em [CA1].

#### D. Critério de Domínio
Desenhe o diagrama de blocos do circuito trissináptico (DG $\rightarrow$ CA3 $\rightarrow$ CA1) e aponte onde você estimula e onde você registra.

---

### MÓDULO 4: A REGRA DE AJUSTE DE GANHOS — PLASTICIDADE STDP E LTP
**Tempo estimado de estudo:** 1 hora

#### A. A Metáfora da Mecatrônica
Como o cérebro "grava" uma memória? Ele não grava bits num disco rígido; ele **modifica a condutância (o peso $w$) das sinapses**.
* **A Regra de Hebb (1949)**: *"Neurônios que disparam juntos, conectam-se juntos."*
* **LTP (Potenciação de Longa Duração)**: Se você estimula uma via com alta frequência, as sinapses ficam mais fortes por horas, dias ou semanas.
* **STDP (Spike-Timing-Dependent Plasticity)**: É a versão moderna, contínua e precisa no tempo da regra de Hebb:
  * Seja $\Delta t = t_{\text{pós}} - t_{\text{pré}}$ (tempo do spike pós-sináptico menos o pré-sináptico):
  * **Se $\Delta t > 0$ (o pré disparou de 1 a 20 ms ANTES do pós)**: A sinapse causou o disparo pós-sináptico $\rightarrow$ **LTP** (o peso sináptico $w$ aumenta!).
  * **Se $\Delta t < 0$ (o pré disparou DEPOIS do pós)**: O pré não teve causalidade sobre o disparo $\rightarrow$ **LTD** (o peso sináptico $w$ diminui!).
* **No seu modelo do Brian 2**:
  Essa regra vira duas equações diferenciais simples de traços sinápticos ($A_{\text{pre}}$ e $A_{\text{post}}$) que atualizam o peso $w$ a cada spike!

#### B. O que ler (Fontes Exatas)
1. **Arquivo**: `PARA_GEMINI_NOTEBOOK/16 - KANDEL - Cap 67 - Hipocampo e Armazenamento de Memoria Explicita.pdf`
   * **Páginas**: 1345 a 1358 (Seção de LTP, receptores NMDA e AMPA).
2. **Arquivo**: `PARA_GEMINI_NOTEBOOK/03 - ARTIGO CHAVE - Stimberg et al (2019) - Brian 2 neural simulator.pdf`
   * **Seção**: *"Synapses and plasticity"* (veja o código de STDP).

#### C. Banco de Flashcards Atômicos (SuperMemo)

1. **P:** Qual receptor sináptico de glutamato atua como um "detector de coincidência" molecular para indução de LTP?
   * **R:** O receptor NMDA (ele só conduz quando há glutamato ligado E a membrana está despolarizada para expulsar o íon Magnésio que bloqueia seu poro).
2. **P:** Na regra de plasticidade STDP, qual é a condição temporal exata para que uma sinapse seja fortalecida (LTP)?
   * **R:** O neurônio pré-sináptico deve disparar poucos milissegundos antes do neurônio pós-sináptico ($\Delta t > 0$, causalidade positiva).
3. **P:** O que acontece na sinapse se o neurônio pós-sináptico disparar antes do pré-sináptico ($\Delta t < 0$)?
   * **R:** Ocorre depressão de longa duração (LTD - *Long-Term Depression*), enfraquecendo a conexão.
4. **P (Cloze):** A associação entre a representação de um Objeto e um padrão de estimulação elétrica no hipocampo ocorre porque os disparos coincidentes ativam a plasticidade [STDP / LTP], aumentando o peso sináptico $w$ entre essas populações.

#### D. Critério de Domínio
Explique com as suas palavras: *"Por que a ordem de disparo de poucos milissegundos dita se uma memória é reforçada ou apagada?"*

---

### MÓDULO 5: O CONTROLE E A SINTAXE — RITMO TETA E ESTIMULAÇÃO TEMPORAL
**Tempo estimado de estudo:** 1 hora

#### A. A Metáfora da Mecatrônica
Um microprocessador precisa de um sinal de *clock* para sincronizar barramentos de dados. O hipocampo usa as **oscilações teta ($4-8\,\text{Hz}$)** como seu clock biológico.
* **A Frequência de 7.14 Hz**: É exatamente o período de $T = 140\,\text{ms}$. É o ritmo predominante quando o camundongo está caminhando, farejando e explorando a arena.
* **A Teoria de Sintaxe Neural do Buzsáki / Prof. Márcio**: O cérebro não se importa apenas com a intensidade da corrente; ele se importa com a **ordem temporal dos pulsos**.
* **Seu Projeto Original**:
  * Você usou **Padrão 1**: `1010101101` (com pulsos e silêncios a cada ciclo de $140\,\text{ms}$).
  * E **Padrão 2**: `1110010111`.
  * Na biofísica: o padrão de bits cria **fases distintas de excitabilidade**. Se o neurônio do Objeto A dispara durante uma janela de desinibição do Padrão 1, a plasticidade STDP explode. Se cair na janela inibitória, o aprendizado é bloqueado!

#### B. O que ler (Fontes Exatas)
1. **Arquivo**: `PARA_GEMINI_NOTEBOOK/04 - ARTIGO NNC 2026 - Xavier, Guarnieri, Moraes - Temporally Coded Stimulation.pdf`
   * **Seções**: *"Materials and Methods -> Electrical stimulation protocols"* e a discussão sobre acoplamento.
2. **Arquivo**: `PARA_GEMINI_NOTEBOOK/05 - ARTIGO NNC 2023 - Cota, Cancado, Moraes - Scale-Free Non-Periodic Stimulation.pdf`
   * Leia a introdução para entender a visão do laboratório sobre padrões temporais.

#### C. Banco de Flashcards Atômicos (SuperMemo)

1. **P:** Qual a faixa de frequência típica do ritmo teta hipocampal em roedores em comportamento exploratório ativo?
   * **R:** De $4$ a $8\,\text{Hz}$ (centralizada em torno de $7$ a $8\,\text{Hz}$).
2. **P:** Qual é o período temporal ($T$) de uma oscilação na frequência de $7.14\,\text{Hz}$ utilizada no seu protocolo experimental?
   * **R:** $T = 1 / 7.14 \approx 140\,\text{ms}$.
3. **P:** Por que um padrão temporal de pulsos discretos (ex: `1010101101`) pode ter efeitos biológicos diferentes de um trem contínuo periódico de pulsos, mesmo com a mesma quantidade total de energia injetada?
   * **R:** Porque padrões temporais distintos interagem com janelas alternadas de facilitação e depressão sináptica e com as fases oscilatórias dos interneurônios inibitórios locais.
4. **P (Cloze):** Segundo os trabalhos recentes do laboratório do Prof. Márcio (Xavier 2026; Cota 2023), a estimulação com sintaxes temporais organizadas modula o [acoplamento funcional / conectograma] da rede neural, interferindo em processos de plasticidade e sincronização.

#### D. Critério de Domínio
Explique: *"Por que injetar pulsos elétricos com padrão de bits a 7.14 Hz em CA3 funciona biologicamente como um 'contexto artificial'?"*

---

## 4. O CRONOGRAMA DE EXECUÇÃO TOP-DOWN (3 SEMANAS PARA ESTAR COM A FACA E O QUEIJO NA MÃO)

| Semana | Foco de Leitura e Fixação | Prática no Computador | Meta de Entrega |
| :---: | :--- | :--- | :--- |
| **Semana 1** | Módulos 0, 1 e 2 (Neurônio RC, Potencial de Ação, Izhikevich 2003, Kandel Caps 06, 07 e 10). | Instalar o Brian 2 e rodar um script mínimo de 1 neurônio de Izhikevich disparando na tela. | Compreender as equações diferenciais e ver o spike no gráfico. |
| **Semana 2** | Módulos 3 e 4 (Circuito CA3-CA1, Kandel Cap 67, STDP no Brian 2, Dix & Aggleton 1999). | Montar a população de neurônios de CA3 conectando em CA1 com sinapses STDP e injeção do trem de pulsos a 7.14 Hz. | Demonstrar a matriz de pesos $W$ mudando de valor após a estimulação. |
| **Semana 3** | Módulo 5 e Artigos do NNC (Xavier 2026, Cota 2023, cruzamento com o seu projeto). | Fechar a malha com a arena 2D e plotar o gráfico de novidade (mismatch de CA1) para o Objeto A vs Objeto B. | **Relatório Completo de Transição de Dissertação** pronto para levar ao Prof. Márcio e Prof. Hani! |

---

## 5. COMO ALIMENTAR ESTE GUIA NO SEU GEMINI NOTEBOOK

1. O arquivo deste guia está salvo em: [`c:\Users\wfran\Documents\Antigravity\Mestrado UFMG\GUIA_MESTRE_DE_APRENDIZADO_NEUROENGENHARIA.md`](file:///c:/Users/wfran/Documents/Antigravity/Mestrado%20UFMG/GUIA_MESTRE_DE_APRENDIZADO_NEUROENGENHARIA.md).
2. Suba este arquivo no seu **Gemini Notebook (NotebookLM)** junto com os 18 PDFs da pasta `PARA_GEMINI_NOTEBOOK`.
3. Pronto! Toda vez que você pedir para o NotebookLM te sabatinar, use o prompt:
   > *"Com base no Guia Mestre e no Módulo [X], faça-me 5 perguntas atômicas de active recall seguindo as regras do SuperMemo para testar se eu realmente entendi o conceito antes de avançar."*
