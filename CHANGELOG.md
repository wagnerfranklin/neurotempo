# Changelog — Linha do Tempo de Desenvolvimento

Todas as modificações metodológicas, implementações de código e atualizações científicas deste projeto são registradas cronologicamente neste arquivo.

> **Regra Estrita de Governança:**  
> Itens só são adicionados a este documento após terem sido **efetivamente implementados, testados localmente e commitados** no repositório. Nada de promessas ou planos futuros nesta lista.

O formato é baseado no padrão [Keep a Changelog](https://keepachangelog.com/pt-BR/1.0.0/) e adota o versionamento semântico voltado à modelagem computacional.

---

## [Não Lançado]

*Nenhuma alteração de código pendente de liberação no momento. A implementação do novo microcircuito espacial de CA3 (Marco 2) será registrada aqui conforme cada tarefa for commitada.*

---

## [0.1.1] — 2026-11-06 — Marco Documental: Blindagem Metodológica e Antiviés

### Adicionado
* **Governança e Rastreabilidade (`CHANGELOG.md`):** Criação da linha do tempo oficial de mudanças para versionamento transparente da dissertação.
* **Documentação Geral Estável (`README.md`):** Reformulação do README para uma estrutura genérica e perene, desacoplada de nomes voláteis de scripts, com a fundamentação científica central e link para o changelog.
* **Especificação Rígida de Engenharia (`specs/`):**
  * `spec.md`: Especificação dos requisitos do modelo de CA3 ancorados 100% na literatura primária (zero dados inventados).
  * `plan.md`: Formalismo matemático das equações diferenciais (Izhikevich, Tsodyks-Markram, kinetics de opsinas).
  * `tasks.md`: Checklist granular de tarefas para execução sequencial.

### Alterado / Corrigido
* **Diretrizes Antiviés (`DIRETRIZES_MESTRADO_ANTIGRAVITY.md`):**
  * Ativação obrigatória do papel de **Revisor Crítico Adverso (*Devil's Advocate*)** para barrar viés de confirmação e condescendência.
  * Rigor terminológico da Engenharia Elétrica: banimento definitivo do termo "voltagem" em prol de **tensão elétrica**, **potencial de membrana ($V_m$)** e **diferença de potencial (DDP)**.
  * Delimitação de escopo: remoção formal do termo *"gêmeo digital"*, mantendo o foco estrito no **modelo computacional biofísico de CA3**.

---

## [0.1.0] — 2026-11-05 — Marco 1: Inicialização do Repositório e Proteção Legal

### Adicionado
* **Repositório Git e GitHub:** Inicialização do repositório público sob o nome `neurostimulation-temporal-coding`.
* **Licença Open Source (GPLv3):** Adoção formal da licença GNU General Public License v3 para proteção da autoria acadêmica e garantia de código aberto.
* **Configuração de Exclusão Seletiva (`.gitignore`):** Purgados do controle de versão os vídeos pesados de bancada (`NNC/`), livros protegidos por copyright (`livros/`), ambientes virtuais (`.venv/`) e caches do LaTeX.
* **Importação da Base de Código de Bancada e Testes Preliminares:**
  * Scripts preliminares de estimulação elétrica (`Codigos/testes/experimento_1_eletrica_wagner_brian2.py`) e optogenética em neurônio isolado (`Codigos/testes/experimento_2_optogenetica_laura_brian2.py`).
  * Relatório inicial da dissertação em LaTeX (`relatorios/relatorio_simulacao.tex`) e figuras.
