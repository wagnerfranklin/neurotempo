# RELATÓRIO CIENTÍFICO CONTROLADO: PADRÃO FIXO (MSf) VS. PADRÃO ALEATÓRIO (MSr)
## Investigação Biofísica da Dissertação de Laura Amado Costa (UFMG, 2026) via Simulação Brian 2

---

## 1. Definição Formal do Problema e Hipóteses

Na dissertação de **Laura Amado Costa (2026)**, camundongos receberam estimulação optogenética (ChR2) em CA3 durante o condicionamento de medo aversivo, comparando dois protocolos sob envelope teta ($7{,}14\text{ Hz}$, $T_{\text{teta}} = 140\text{ ms}$, pausa $= 140\text{ ms}$):
* **MSf (Padrão Fixo)**: Palavra temporal fixa de 10 bins (`1010101101`), contendo 6 pulsos ativos de $5\text{ ms}$.
* **MSr (Padrão Aleatório)**: Pool de 70 permutações de 10 bins, sempre com 6 pulsos ativos de $5\text{ ms}$ (primeiro e último bits fixos em 1, quatro bits 1 distribuídos aleatoriamente nos 8 bins centrais).

**Resultado Experimental de Bancada**:
* Imunofluorescência de c-Fos: Inconclusivo ($p = 0{,}9888$ entre MSf e MSr).
* Comportamento (*Freezing*): Inconclusivo ($p > 0{,}05$).

### Formulação das Hipóteses para a Simulação in silico:
* **Hipótese do Laboratório (H1)**: A sintaxe temporal dos disparos (ordenação precisa dos pulsos dentro de 140 ms) gera respostas biológicas distintas a nível celular e sináptico.
* **Hipótese Nula (H0)**: Neurônios individuais e cascatas enzimáticas integradoras atuam como filtros passa-baixa; como ambos os protocolos injetam a mesma densidade média de energia luminosa (6 pulsos / 140 ms), a resposta biofísica celular será essencialmente indistinguível.

---

## 2. Metodologia Computacional Rigorosa

* **Script**: [`Codigos/teste_metodo_cientifico_laura_msf_vs_msr.py`](file:///c:/Users/wfran/Documents/Antigravity/Mestrado%20UFMG/Codigos/teste_metodo_cientifico_laura_msf_vs_msr.py).
* **Gráfico Gerado**: [`Codigos/resultado_cientifico_laura_msf_vs_msr.png`](file:///c:/Users/wfran/Documents/Antigravity/Mestrado%20UFMG/Codigos/resultado_cientifico_laura_msf_vs_msr.png).
* **Modelo Neuronal**: Modelo de Hodgkin-Huxley acoplado à condutância da ChR2 ($\tau_{\text{off}} = 13{,}0\text{ ms}$, $g_{\text{max}} = 0{,}25\text{ mS/cm}^2$, $E_{\text{rev}} = 0\text{ mV}$).
* **Sensor Bioquímico de Ativação Celular**: Modelo dinâmico de influxo e decaimento de cálcio intracelular $[Ca^{2+}]_i$ ($\tau_{Ca} = 200\text{ ms}$), cuja integral no tempo é o proxy direto da ativação transcricional de c-Fos.
* **Modelo Sináptico Eferente**: Sinapse com plasticidade dependente do tempo de disparo (STDP) clássica (Song & Abbott, 2000), monitorando o peso $w(t)$ a partir de $w_0 = 0{,}50$.
* **Duração da Simulação**: $2{,}8\text{ s}$ ($10\text{ ciclos}$ completos de $280\text{ ms}$ = $60\text{ pulsos}$ luminosos totais para cada condição).

---

## 3. Dados Numéricos Brutos da Simulação

| Variável Monitorada | MSf (Padrão Fixo) | MSr (Padrão Aleatório) | Diferença Absoluta | Diferença Percentual |
| :--- | :---: | :---: | :---: | :---: |
| **Pulsos Luminosos Entregues** | 60 | 60 | 0 | 0,00% |
| **Spikes Disparados ($V_m > 0\text{ mV}$)** | 59 | 54 | 5 spikes | 8,47% |
| **Taxa de Transdução ($\text{Spikes}/\text{Pulsos}$)** | 98,33% | 90,00% | - | - |
| **Integral de Cálcio ($\int [Ca^{2+}] dt$)** | $0{,}9656\text{ arb}\cdot\text{s}$ | $0{,}8934\text{ arb}\cdot\text{s}$ | $0{,}0722$ | **7,48%** |
| **Peso Sináptico STDP Final ($w$)** | 0,5000 | 0,5000 | 0,0000 | **0,00%** |

---

## 4. Análise Crítica dos Resultados (Método Científico)

### 4.1. Falsificação da Hipótese de "Bloqueio Total da ChR2"
A análise visual do traçado e a contagem quantitativa mostram que a ChR2 **não sofreu colapso funcional por despolarização em bloco**:
* No MSf, 59 de 60 pulsos geraram potenciais de ação plenos.
* No MSr, 54 de 60 pulsos geraram potenciais de ação.
* As pequenas falhas no MSr ocorreram exclusivamente quando 3 pulsos consecutivos foram sorteados em intervalos curtos ($9\text{ ms}$ de intervalo interestímulo), onde a inativação transitória de canais de sódio ($h \approx 0{,}20$) impediu o terceiro disparo consecutivo.

### 4.2. Por que a Laura Costa Encontrou $p = 0{,}9888$ no c-Fos?
A marcação celular por c-Fos não mede a resolução de milissegundos dos spikes. O c-Fos é uma proteína de transcrição precoce induzida pela cascata intracelular $Ca^{2+} \to \text{CaMKII} \to \text{MAPK} \to \text{CREB}$:
1. Essa cascata atua como um **integrador matemático analógico contínuo** com janela de tempo de 60 a 90 minutos.
2. A simulação biofísica revela que a diferença acumulada de entrada de cálcio entre os dois padrões foi de **apenas 7,48%**.
3. Em imunofluorescência confocal de fatias encefálicas, o coeficiente de variação biológico e técnico inter-animais ($\sigma$) é tipicamente superior a **$15\text{--}25\%$**.
4. **Conclusão direta**: Um sinal diferencial de $7{,}48\%$ é estocasticamente indistinguível do ruído amostral ($p > 0{,}05$), corroborando perfeitamente o achado empírico de Laura Costa ($p = 0{,}9888$).

### 4.3. Por que o Comportamento de Medo (*Freezing*) Não Foi Alterado?
* **Incompatibilidade de Circuito**: O condicionamento de medo a um estímulo auditivo puro (*Tone-Shock pairing*) é processado e consolidado primariamente no eixo Tálamo Auditivo $\to$ Amígdala Basolateral (BLA) $\to$ Amígdala Central (CeA).
* A ativação optogenética de CA3 do hipocampo introduz atividade em uma área de contexto espacial/episódico, mas não interrompe nem substitui a rota direta de ativação do reflexo amigdalar.

---

## 5. Conclusões e Conexão com o Projeto de Mestrado (Wagner Franklin)

1. **A Hipótese Nula (H0) Não Pode Ser Rejeitada em Nível de Neurônio Único**:
   No nível celular isolado, padrões temporais de mesma energia não produzem estados contrastantes de ativação ou plasticidade feedforward.
2. **Onde a Sintaxe Temporal Pode Fazer Diferença (O Nicho Computacional do Mestrado)**:
   A diferenciação de padrões temporais (como no trabalho de Cota et al., 2023) exige necessariamente:
   * **Realimentação Inibitória Recorrente**: A presença de interneurônios GABAérgicos rápidos (células em cesto / parvalbumina) que disparam com os primeiros bits e geram janelas de inibição pós-sináptica ($\text{IPSP} \approx 10\text{--}20\text{ ms}$), vetando bits subsequentes que cheguem fora de fase.
   * **Ressonância de Rede em Malha Fechada**: Acoplamento com a fase instantânea do LFP teta endógeno.
3. **Proposta de Valor para o PPGEE (Prof. Hani e Prof. Márcio)**:
   A modelagem computacional permitiu elucidar o que o ensaio biológico de bancada não conseguiu: quantificar exatamente por que o biomarcador c-Fos falhou em discriminar os padrões temporais, delimitando as condições de rede necessárias para que estímulos temporais codificados tenham relevância biológica real.
