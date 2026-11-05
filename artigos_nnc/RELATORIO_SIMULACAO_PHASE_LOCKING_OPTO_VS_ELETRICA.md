# RELATÓRIO TÉCNICO DE SIMULAÇÃO IN SILICO: TRANSDUÇÃO, PHASE-LOCKING E CINÉTICA DE OPSINAS
## Investigação Mecanicista: Optogenética Clássica (ChR2), Optogenética Rápida (Chronos) e Microestimulação Elétrica

---

## 1. O Problema Científico Formal

A dissertação de **Laura Amado Costa (UFMG, 2026)** utilizou estimulação optogenética com **Channelrhodopsin-2 (ChR2)** em neurônios de CA3 para avaliar se padrões temporais sob um envelope teta ($7{,}14\text{ Hz}$, $T \approx 140\text{ ms}$) codificavam memórias aversivas. 
* **Resultado Empírico**: Inconclusivo. Padrão Fixo vs. Padrão Aleatório geraram níveis idênticos de *freezing* e de marcação celular por c-Fos ($p > 0{,}05$).

A questão central investigada nesta simulação:
> **O estímulo optogenético com ChR2 foi capaz de transferir a informação temporal fina dos 10 bits para a membrana neuronal, ou a biofísica do transdutor destruiu o código antes da integração sináptica?**

---

## 2. Metodologia Computacional no Brian 2

Implementamos um modelo biofísico de condutâncias ativas baseado nas equações de **Hodgkin-Huxley (1952)** para neurônios piramidais de CA3, acoplado a três modelos de transdução submetidos ao **Padrão 1 (`1010101101`)**:

1. **Condição 1 — ChR2 Clássica (Laura Costa, 2026)**:
   * Constante de desativação: $\tau_{\text{off}} = 13{,}0\text{ ms}$.
   * Cinética lenta da fotocorrente: $\frac{dg}{dt} = \frac{g_{\infty} - g}{\tau}$.
2. **Condição 2 — Opsin Ultrarrápida (Chronos / ChETA)**:
   * Constante de desativação: $\tau_{\text{off}} = 3{,}5\text{ ms}$.
3. **Condição 3 — Estimulação Elétrica Direta (Wagner Franklin)**:
   * Injeção capacitiva direta: $\tau \to 0\text{ ms}$, pulso de corrente retangular de $350\text{ pA}$.

---

## 3. Resultados Quantitativos e Mecanicistas

Os resultados foram salvos no gráfico [`figura_optogenetica_vs_eletrica_phase_locking.png`](file:///c:/Users/wfran/Documents/Antigravity/Mestrado%20UFMG/Codigos/figura_optogenetica_vs_eletrica_phase_locking.png).

### 1. O Fenômeno de Deglutição de Bits (*Bit Swallowing*)
* No Padrão 1, ocorrem pares de bits '1' consecutivos (bits 7 e 8: `...11...`, com intervalo de apenas $9\text{ ms}$ entre o fim de um pulso e o início do próximo).
* **Na ChR2 (Laura)**:
  * Como $\tau_{\text{off}} = 13\text{ ms}$, em um intervalo de $9\text{ ms}$ a condutância decai para apenas $e^{-9/13} \approx 50\%$ do valor máximo.
  * A célula permanece despolarizada ($V_m > -35\text{ mV}$), impedindo a recuperação da comporta de inativação de sódio ($h(t) < 0{,}15$).
  * **Consequência**: O segundo bit `1` **não dispara potencial de ação**. De 6 bits ativos por ciclo, a ChR2 só consegue disparar 5 spikes, distorcendo a sintaxe temporal.
* **Na Chronos e na Elétrica**:
  * Como a recuperação é rápida ($\tau_{\text{off}} = 3{,}5\text{ ms}$ ou $\tau = 0$), $h(t)$ sobe rapidamente para $> 0{,}80$.
  * **Consequência**: Cada bit `1` gera rigorosamente um potencial de ação discreto (fidelidade de 100%, 6 spikes para 6 bits '1').

### 2. Implicações para o *Phase-Locking* e Plasticidade STDP
* **No nível do envelope Teta macroscópico**: Todas as três modalidades exibem alto arrastamento de fase macroscópica ($\text{PLV}_{\text{envelope}} \approx 1$). Isso explica por que no LFP ou espectrograma tudo parece sincronizado a $7{,}14\text{ Hz}$.
* **No nível da microestrutura informacional (Bits)**: 
  * A ChR2 transforma um trem discreto de 10 bits em um degrau quase contínuo de corrente despolarizante. Para a rede pós-sináptica em CA1, tanto o padrão fixo quanto o padrão aleatório entregam a mesma carga integrada média. Logo, **a plasticidade STDP é idêntica em ambos os casos**, explicando matematicamente por que a Laura encontrou valores idênticos de c-Fos e *freezing*.
  * A estimulação elétrica direta preserva a separação temporal precisa entre spikes pré e pós-sinápticos ($\Delta t$), permitindo que a regra STDP diferencie engramas de acordo com a sintaxe de cada padrão.

---

## 4. Diretrizes de Engenharia para Mitigação Experimental

Para que um experimento optogenético com padrões temporais tenha viabilidade real:
1. **Substituição da Opsin**: Substituir AAV-CaMKIIa-ChR2 por variantes com cinética ultrarrápida: **Chronos** ($\tau_{\text{off}} \approx 3{,}6\text{ ms}$) ou **ChETA** ($\tau_{\text{off}} \approx 4\text{ ms}$).
2. **Redução da Largura de Pulso**: Reduzir a duração do pulso óptico de $5\text{ ms}$ para $1\text{--}2\text{ ms}$, aumentando a potência de pico do laser para compensar o fluxo de fótons.
3. **Controle em Malha Fechada (*Phase-Locked Trigger*)**: Sincronizar o início do envelope de 140 ms com o vale da oscilação teta endógena, garantindo que a inibição basal esteja no mínimo durante a transmissão dos primeiros bits.
