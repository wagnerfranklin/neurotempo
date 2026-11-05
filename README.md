# neurostimulation-temporal-coding

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Brian 2 Simulator](https://img.shields.io/badge/simulator-Brian%202-brightgreen.svg)](https://briansimulator.org/)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Institution: UFMG](https://img.shields.io/badge/UFMG-PPGEE%20%2F%20NNC-red.svg)](https://www.ppgee.ufmg.br/)

> **In silico Bio-computational Modeling of Temporally Coded Electrical and Optogenetic Neurostimulation in Hippocampal CA3 Networks**

Este repositório contém os modelos computacionais, rotinas de simulação biofísica e testes de hipóteses desenvolvidos na dissertação de mestrado pelo **Programa de Pós-Graduação em Engenharia Elétrica (PPGEE)** e pelo **Núcleo de Neurociências (NNC - ICB/UFMG)** na Universidade Federal de Minas Gerais.

---

## 🔬 Visão Geral do Projeto

A estimulação neural tradicional frequentemente utiliza trens periódicos de pulsos em alta ou baixa frequência. Em contrapartida, evidências pioneiras do NNC demonstram que o sistema nervoso central é sensível à **sintaxe temporal dos intervalos entre pulsos (IPIs)**, permitindo que trens de pulsos com a mesma carga e frequência média recrutem estados de rede distintos (análogo a uma porta de comunicação serial assíncrona).

Este projeto desenvolve um **Gêmeo Digital (*Digital Twin*) em Brian 2** do microcircuito de CA3 para responder a perguntas centrais da neuroengenharia:
1. **Biofísica do Transdutor:** Por que a estimulação elétrica direta preserva a precisão temporal de milissegundos enquanto a Canalrodopsina-2 clássica (ChR2 wild-type, $\tau_{\text{off}} \approx 13\text{ ms}$) atua como um filtro passa-baixas biológico? O uso de opsinas ultrarrápidas (Chronos, $\tau_{\text{off}} \approx 3{,}6\text{ ms}$) restabelece a fidelidade temporal?
2. **Dinâmica de Rede:** Como o balanço excitatório/inibitório (80 neurônios piramidais RS + 20 interneurônios Fast-Spiking) e a plasticidade de curto prazo (Tsodyks-Markram) filtram padrões temporais fixos versus estocásticos e livres de escala (*Scale-Free*)?
3. **Topologia de Mundo Pequeno (*Small-World*):** Como a conectividade recorrente e modular de CA3 governa a transição entre segregação de informação e sincronização global?

---

## 📚 Fundamentação Teórica

O arcabouço computacional e metodológico deste projeto é fundamentado em três pilares da literatura:

* **Nível Celular (Detecção de Coincidência):**  
  *König, Engel & Singer (1996)* — *Integrator or coincidence detector? The role of the cortical neuron revisited*, **Trends in Neurosciences**.  
  Demonstra que o estado de alta condutância (*in vivo*) e o *feedback* inibitório rápido estreitam a janela de integração para $< 5\text{ ms}$, tornando o neurônio um detector de coincidência temporal.
* **Nível Topológico (Estrutura de Grafos Complexos):**  
  *Liao, Vasilakos & He (2017)* — *Small-world human brain networks: Perspectives and challenges*, **Neuroscience and Biobehavioral Reviews**.  
  Demonstra que circuitos corticais e hipocampais operam sob arquitetura *Small-World* (Watts-Strogatz), equilibrando agrupamento local (segregação) e integração eficiente.
* **Nível Sistêmico e Protocolo Experimental:**  
  *Mourão et al. (2016)* — *Triggering Different Brain States Using Asynchronous Serial Communication to the Rat Amygdala*, **Cerebral Cortex**.  
  Demonstração empírica do NNC/UFMG de que palavras binárias com carga idêntica acionam circuitos cerebrais e comportamentos aversivos específicos com base exclusiva no padrão temporal dos pulsos.

---

## 📁 Estrutura do Repositório

```
neurostimulation-temporal-coding/
├── .gitignore                      <- Filtro de exclusão (vídeos brutos, PDFs com copyright, venv)
├── LICENSE                         <- GNU General Public License v3 (GPLv3)
├── README.md                       <- Apresentação e documentação do projeto
├── requirements.txt                <- Dependências Python reprodutíveis
│
├── Codigos/                        <- Scripts e modelos em Brian 2
│   ├── testes/
│   │   ├── experimento_1_eletrica_wagner_brian2.py     <- Simulação de microestimulação elétrica
│   │   ├── experimento_2_optogenetica_laura_brian2.py  <- Simulação ChR2 vs Chronos
│   │   └── teste_metodo_cientifico_laura_msf_vs_msr.py <- Avaliação estatística de equivalência
│   └── analise_bancada_consolidada/                    <- Pipelines de processamento
│
├── relatorios/                     <- Relatórios científicos e dissertação
│   ├── relatorio_cientifico.tex    <- Texto da dissertação / relatório técnico
│   ├── referencias.bib             <- Base bibliográfica completa
│   └── figuras/                    <- Gráficos e painéis gerados em alta resolução
│
└── artigos_nnc/                    <- Documentação dos experimentos biológicos do laboratório
```

---

## 🚀 Instalação e Uso

### 1. Clonar o Repositório
```bash
git clone https://github.com/SEU_USUARIO/neurostimulation-temporal-coding.git
cd neurostimulation-temporal-coding
```

### 2. Configurar o Ambiente Virtual Python
```bash
python -m venv .venv

# No Linux/macOS:
source .venv/bin/activate

# No Windows (PowerShell):
.venv\Scripts\Activate.ps1
```

### 3. Instalar Dependências
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Executar as Simulações
```bash
# Simulação da estimulação elétrica (Padrão 1 vs Padrão 2 em CA3):
python Codigos/testes/experimento_1_eletrica_wagner_brian2.py

# Simulação da filtragem biofísica optogenética (ChR2 vs Chronos):
python Codigos/testes/experimento_2_optogenetica_laura_brian2.py
```

---

## 📜 Licença

Este projeto é distribuído sob a licença **GNU General Public License v3 (GPLv3)**. Consulte o arquivo [LICENSE](LICENSE) para obter o texto integral.

---

## 🏛️ Autoria e Afiliação

* **Pesquisador:** Wagner Franklin
* **Orientação:** Prof. Dr. Márcio Flávio Dutra Moraes
* **Programa:** Programa de Pós-Graduação em Engenharia Elétrica (PPGEE / UFMG)
* **Laboratório:** Núcleo de Neurociências (NNC) — Departamento de Fisiologia e Biofísica, Instituto de Ciências Biológicas (ICB / UFMG)
