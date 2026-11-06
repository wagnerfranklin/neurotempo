# Changelog — Linha do Tempo de Desenvolvimento

Todas as modificações metodológicas, implementações de código e atualizações científicas deste projeto são registradas cronologicamente neste arquivo.

O formato é baseado no padrão [Keep a Changelog](https://keepachangelog.com/pt-BR/1.0.0/) e adota o versionamento semântico voltado à modelagem computacional.

---

## [Não Lançado / Em Desenvolvimento] — Marco 2: Modelo Computacional Espacialmente Incorporado de CA3

### Adicionado
* **Estrutura de Grafo Espacial nas 4 Vias Sinápticas:**
  * Topologia de Watts-Strogatz em $W_{EE}$ (80 células piramidais RS conectadas a 8 vizinhos locais com $10\%$ de atalhos axônicos de longo alcance), ancorada em Guzman et al. (*Science*, 2016) e Liao et al. (*Neurosci. Biobehav. Rev.*, 2017).
  * Conectividade com decaimento de distância em $W_{EI}$ e $W_{IE}$, reproduzindo a inibição perissomática e a inibição lateral circundante (*surround inhibition*).
  * Rede interneuronal $W_{II}$ entre os 20 interneurônios Fast-Spiking para sustentação de coerência Gama ($30\text{--}80\text{ Hz}$), conforme Bartos et al. (*Nat. Rev. Neurosci.*, 2007).
  * 2 nós inibitórios divergentes de amplo alcance (Hubs GABAérgicos), conforme Bonifazi et al. (*Science*, 2009).
* **Estado In Vivo de Alta Condutância:**
  * Fontes pré-sinápticas Poisson basais (excitatórias e inibitórias) que reduzem a constante de tempo efetiva para a escala sub-milissegúndica ($\tau_{\text{eff}} \approx 3\text{--}5\text{ ms}$), operando em modo estrito de detecção de coincidência (König, Engel & Singer, 1996).
* **Motor de Estimulação com Isocarga Estrita e Controle Negativo:**
  * Protocolo comparativo com exatamente 6 pulsos ativos em 10 bins de $14\text{ ms}$ ($140\text{ ms}$ ativo): Padrão A (concentrado), Padrão B (alternado) e Padrão C (Escala Livre / Cota et al., 2023).
  * Controle negativo falsificável (*Shuffle*) com permutação aleatória de pulsos.
  * Atenuação radial de intensidade ($1/r^2$) a partir do centro da fibra/eletrodo.
* **Métrica Temporal de van Rossum:**
  * Implementação da métrica $D_{vR}(\tau)$ com varredura temporal $\tau \in [1, 100]\text{ ms}$ (van Rossum, 2001) e acompanhamento da evolução da matriz STDP.

### Corrigido / Eliminado
* **Eliminação do Viés de Carga:** Removida a comparação desigual de 6 pulsos contra 7 pulsos presente nos testes preliminares, garantindo isoenergia estrita (Mourão et al., 2016).
* **Unificação do Modelo de Optogenética:** Eliminada a simulação de opsinas em neurônio único isolado ($N=1$). A ChR2 ($\tau_{\text{off}} = 13\text{ ms}$) e a Chronos ($\tau_{\text{off}} = 3{,}6\text{ ms}$) agora operam dentro da mesma rede de 100 neurônios sob inibição lateral.
* **Rigor Terminológico da Engenharia Elétrica:** Abolição total do termo coloquial "voltagem" em prol de **tensão elétrica**, **potencial de membrana ($V_m$)** e **diferença de potencial (DDP)**.

---

## [0.1.0] — 2026-11-05 — Marco 1: Inicialização do Repositório e Proteção Legal

### Adicionado
* **Criação do Repositório Git e GitHub:** Inicialização do repositório sob o nome definitivo `neurostimulation-temporal-coding`.
* **Licenciamento Open Source:** Adoção formal da licença **GNU General Public License v3 (GPLv3)** para proteção de autoria acadêmica e garantia de código aberto perpétuo.
* **Configuração de Exclusão Seletiva (`.gitignore`):**
  * Purgados e ignorados do controle de versão: vídeos pesados de bancada (`NNC/`), livros protegidos por copyright (`livros/`), ambientes virtuais (`.venv/`) e caches do LaTeX.
  * Mantidos no Git estritamente o código-fonte (`Codigos/`), o relatório técnico da dissertação (`relatorios/`), documentação e dependências (`requirements.txt`).
* **Estruturação Preliminar dos Experimentos em Brian 2:**
  * Importação dos scripts iniciais de estimulação elétrica (Experimento 1) e de comparação de fotocorrente (Experimento 2).
