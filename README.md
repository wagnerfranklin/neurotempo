# NeuroTempo

[![Python 3.14.7](https://img.shields.io/badge/python-3.14.7-blue.svg)](https://www.python.org/downloads/)
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
2. **Estimulação Optogenética:** Avaliação da filtragem passa-baixas biológica imposta pela cinética de desativação de canalrodopsinas clássicas (ChR2 Wild-Type, τ_off ≈ 13 ms) versus opsinas ultrarrápidas de última geração (Chronos, τ_off ≈ 3.6 ms).

---

## 🔬 Resumo da Pesquisa

Este projeto estabelece uma estrutura rigorosa de modelagem biofísica computacional em **Brian 2** para investigar o processamento temporal de sinais e os limites de transmissão de informação na sub-região CA3 do hipocampo.

O microcircuito modelado integra neurônios piramidais excitatórios de adaptação lenta (*Regular Spiking* — RS) e interneurônios inibitórios rápidos perissomáticos PV⁺ (*Fast Spiking* — FS) governados pelo formalismo dinâmico bidimensional de Izhikevich (2003), acoplados a plasticidade sináptica de curto prazo de Tsodyks-Markram (τ_rec = 600 ms, U_SE = 0.45) e condutâncias inibitórias de *shunting* perissomático (E_GABA = -75 mV):

1. **Microestimulação Elétrica Extracelular (`simulacao/S_experimento_1_eletrica_brian2.py`):**  
   Sob estimulação contínua com envelope teta de 140 ms (7.14 Hz) em malha aberta, demonstra-se colapso vesicular acentuado (R_ss ≈ 0.11, atenuação de 89% no feedback excitatório) e forte inibição por condutância. No domínio escalar de taxa média de disparos, o Teste de Equivalência Biológica (TOST, margem de 15%) comprova equivalência estatística estrita entre padrões temporais (p_TOST = 7.12 × 10⁻⁷, p < 0.001), enquanto no domínio temporal a correlação linear de Pearson no PSTH (bins de 14 ms) revela desfasamento estrito (r = -0.3035).

2. **Transdução Optogenética Comparativa (`simulacao/S_experimento_2_optogenetica_brian2.py`):**  
   Confrontando Canalrodopsina-2 clássica (ChR2 wild-type, τ_off = 13.0 ms) com a opsina ultrarrápida Chronos (τ_off = 3.6 ms) sob cinética fotoquímica calibrada de 2 estados, comprova-se que, embora Chronos feche entre pulsos adjacentes (O_mín ≈ 0), a integral intracelular de cálcio Ca²⁺(t) (proxy molecular de c-Fos) é invariante à dose total de fótons pareada em malha aberta (p = 0.2791), justificando quantitativamente a ausência de diferença na histologia de bancada (p = 0.9888).

Toda a base bibliográfica que fundamenta estes parâmetros está catalogada em `relatorios/referencias.bib` e detalhada no relatório técnico (`relatorios/relatorio_simulacao.pdf`).

---

## 📁 Arquitetura do Repositório

```
neurotempo/
├── .gitattributes                  <- Configuração de detecção de linguagem do GitHub
├── CHANGELOG.md                    <- Linha do tempo de versões e alterações metodológicas
├── LICENSE                         <- Licença GNU General Public License v3 (GPLv3)
├── README.md                       <- Documentação geral e visão panorâmica da pesquisa
├── requirements.txt                <- Dependências Python reprodutíveis
│
├── simulacao/                      <- Modelos computacionais biofísicos em Brian 2
│   ├── S_experimento_1_eletrica_brian2.py
│   └── S_experimento_2_optogenetica_brian2.py
│
└── relatorios/                     <- Relatório técnico da dissertação em LaTeX
    ├── relatorio_simulacao.tex     <- Documento mestre em LaTeX
    ├── relatorio_simulacao.pdf     <- Relatório compilado
    ├── referencias.bib             <- Base bibliográfica completa
    ├── figuras/simulacao/          <- Gráficos e painéis em alta resolução
    └── tabelas/simulacao/          <- Tabelas quantitativas formatadas
```

---

## 🚀 Instalação e Ambiente

O projeto utiliza o simulador **Brian 2** em ambiente **Python 3.14.7**:

```bash
# 1. Clonar o repositório
git clone https://github.com/wagnerfranklin/neurotempo.git
cd neurotempo

# 2. Configurar o ambiente virtual
python -m venv .venv
source .venv/bin/activate  # No Windows: .venv\Scripts\Activate.ps1

# 3. Instalar dependências estritas
pip install --upgrade pip
pip install -r requirements.txt
```

---

## 📜 Licença e Propriedade Intelectual

Este projeto é distribuído sob os termos da licença **GNU General Public License v3 (GPLv3)**. Consulte o arquivo [LICENSE](LICENSE) para obter os termos integrais de uso, modificação e distribuição de código aberto acadêmico.

---

## 🏛️ Autoria e Vínculo Institucional

* **Pesquisador:** Wagner Mathias Fonseca Franklin (Engenheiro Mecatrônico)
* **Orientação:** Prof. Dr. Márcio Flávio Dutra Moraes e Prof. Dr. Hani Camille Yehia
* **Programa:** Programa de Pós-Graduação em Engenharia Elétrica (**PPGEE / UFMG**)
* **Laboratório:** Núcleo de Neurociências (**NNC**) — Departamento de Fisiologia e Biofísica, Instituto de Ciências Biológicas (**ICB / UFMG**)
