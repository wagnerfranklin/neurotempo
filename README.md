# neurostimulation-temporal-coding

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Brian 2 Simulator](https://img.shields.io/badge/simulator-Brian%202-brightgreen.svg)](https://briansimulator.org/)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Institution: UFMG](https://img.shields.io/badge/UFMG-PPGEE%20%2F%20NNC-red.svg)](https://www.ppgee.ufmg.br/)

> **In silico Bio-computational Modeling of Temporally Coded Electrical and Optogenetic Neurostimulation in Hippocampal CA3 Networks**

Este repositório contém a infraestrutura computacional, modelos biofísicos de redes neurais e testes estatísticos de hipóteses desenvolvidos na dissertação de mestrado pelo **Programa de Pós-Graduação em Engenharia Elétrica (PPGEE)** e pelo **Núcleo de Neurociências (NNC - ICB/UFMG)** na Universidade Federal de Minas Gerais.

Para acompanhar a evolução detalhada do código, novos módulos implementados e justificativas científicas a cada versão, consulte o histórico completo em [**CHANGELOG.md**](CHANGELOG.md).

---

## 🔬 Escopo Científico

O projeto investiga os mecanismos biofísicos e topológicos que permitem a microcircuitos recorrentes da sub-região **CA3 do hipocampo** decodificar **padrões temporais de estimulação**, avaliando a hipótese de **comunicação serial assíncrona** no encéfalo.

O trabalho desenvolve um **modelo computacional biofísico em Brian 2**, confrontando os limites de transdução entre duas modalidades físicas:
1. **Microestimulação Elétrica Extracelular:** Transmissão instantânea de carga somática com fidelidade temporal sub-milissegúndica.
2. **Estimulação Optogenética:** Avaliação da filtragem passa-baixas biológica imposta pela cinética de desativação de canalrodopsinas clássicas (ChR2 Wild-Type, $\tau_{\text{off}} \approx 13\text{ ms}$) versus opsinas ultrarrápidas de última geração (Chronos, $\tau_{\text{off}} \approx 3{,}6\text{ ms}$).

---

## 📚 Fundamentação Teórica

A modelagem é ancorada em três pilares canônicos da literatura revisada por pares:

* **Nível Celular (Detecção de Coincidência Temporal):**  
  *König, Engel & Singer (1996)* — *Integrator or coincidence detector? The role of the cortical neuron revisited*, **Trends in Neurosciences**.  
  Demonstra que o estado de alta condutância (*in vivo*) e o balanço excitatório/inibitório estreitam a constante de tempo efetiva de membrana ($\tau_{\text{eff}} < 5\text{ ms}$), tornando o neurônio um detector de sincronicidade e de intervalos precisos.
* **Nível Topológico (Grafos de Mundo Pequeno e Hubs GABAérgicos):**  
  *Liao, Vasilakos & He (2017)* — *Small-world human brain networks: Perspectives and challenges*, **Neurosci. Biobehav. Rev.**  
  *Guzman et al. (2016)* — *Synaptic mechanisms of pattern completion in the hippocampal CA3 network*, **Science**.  
  *Bonifazi et al. (2009)* — *GABAergic hub neurons orchestrate synchrony in developing hippocampal networks*, **Science**.  
  *Bartos, Vida & Jonas (2007)* — *Synaptic mechanisms of coordinated interneuron network oscillations*, **Nat. Rev. Neurosci.**  
  Demonstram que a rede hipocampal equilibra segregação modular local e integração global eficiente através de colaterais recorrentes e redes interneuronais acopladas.
* **Nível Sistêmico e Protocolo Experimental (Comunicação Serial Assíncrona):**  
  *Mourão et al. (2016)* — *Triggering Different Brain States Using Asynchronous Serial Communication to the Rat Amygdala*, **Cerebral Cortex**.  
  *Cota, Cançado & Moraes (2023)* — *On temporal scale-free non-periodic stimulation and its mechanisms as an infinite improbability drive of the brain's functional connectogram*, **Frontiers in Neuroinformatics**.  
  Comprovam experimentalmente no NNC/UFMG que palavras temporais com carga elétrica e frequência média rigorosamente equivalentes acionam estados neurais, dinâmicas de plasticidade e comportamentos completamente distintos.

---

## 📁 Arquitetura do Repositório

```
neurostimulation-temporal-coding/
├── CHANGELOG.md                    <- Linha do tempo de versões e alterações detalhadas
├── LICENSE                         <- Licença GNU General Public License v3 (GPLv3)
├── README.md                       <- Documentação geral e visão panorâmica da pesquisa
├── requirements.txt                <- Dependências Python reprodutíveis
│
├── Codigos/                        <- Modelos computacionais em Brian 2 e rotinas de análise
│   ├── testes/                     <- Simulações biofísicas, benchmarks e testes de hipóteses
│   └── analise_bancada_consolidada/<- Processamento e extração de dados experimentais
│
├── relatorios/                     <- Dissertação e relatórios técnicos em LaTeX
│   ├── relatorio_simulacao.tex     <- Documento mestre da dissertação
│   ├── referencias.bib             <- Base bibliográfica completa
│   ├── tabelas/                    <- Tabelas quantitativas compiladas
│   └── figuras/                    <- Gráficos e painéis em alta resolução (300 DPI e vetor PDF)
│
└── specs/                          <- Especificações formais de engenharia (Spec Kit)
    └── 001-ca3-recurrent-simulation/ <- Requisitos, equações e planos de implementação
```

---

## 🚀 Instalação e Ambiente

O projeto utiliza o simulador **Brian 2** em ambiente Python 3:

```bash
# 1. Clonar o repositório
git clone https://github.com/wagnerfranklin/neurostimulation-temporal-coding.git
cd neurostimulation-temporal-coding

# 2. Configurar o ambiente virtual
python -m venv .venv
source .venv/bin/activate  # No Windows: .venv\Scripts\Activate.ps1

# 3. Instalar dependências estritas
pip install --upgrade pip
pip install -r requirements.txt
```

As simulações numéricas e análises estatísticas são executadas a partir do diretório raiz utilizando os scripts localizados em `Codigos/testes/`.

---

## 📜 Licença e Propriedade Intelectual

Este projeto é software livre acadêmico licenciado sob os termos da **GNU General Public License v3 (GPLv3)**. Consulte o arquivo [LICENSE](LICENSE) para obter os termos integrais de cópia, distribuição e modificação.

---

## 🏛️ Autoria e Vínculo Institucional

* **Pesquisador:** Wagner Mathias Fonseca Franklin (Engenheiro Mecatrônico)
* **Orientação:** Prof. Dr. Márcio Flávio Dutra Moraes e Prof. Dr. Hani Camille Yehia
* **Programa:** Programa de Pós-Graduação em Engenharia Elétrica (**PPGEE / UFMG**)
* **Laboratório:** Núcleo de Neurociências (**NNC**) — Departamento de Fisiologia e Biofísica, Instituto de Ciências Biológicas (**ICB / UFMG**)
