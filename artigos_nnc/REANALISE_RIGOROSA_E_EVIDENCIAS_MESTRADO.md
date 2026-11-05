# REANÁLISE CRÍTICA RIGOROSA DO PROJETO DE MESTRADO (PPGEE / UFMG)
## Auditoria de Evidências, Biofísica Formal e Mapeamento de Hipóteses

* **Pesquisador:** Wagner Mathias Fonseca Franklin (Engenheiro Mecatrônico, UFMG)
* **Programa:** Pós-Graduação em Engenharia Elétrica (PPGEE / UFMG)
* **Orientação:** Prof. Dr. Márcio Flávio Dutra Moraes (ICB / NNC) & Prof. Dr. Hani Camille Yehia (EE / Inteligência Computacional)
* **Marco Regulatório:** Método Científico Rigoroso (Feynman, 1974; Santos, 2008, Cap. 3 e 5) e Regra de Vinculação Mandatória à Evidência Primária (*Evidence Binding*).

---

## 1. Auditoria dos Dados Brutos e Limitações do Ensaio In Vivo

### A. Inventário Estrito dos Dados Comportamentais Coletados
Os registros brutos processados da fase de testes encontram-se na planilha `Dissertação de Mestrado/Dados/Comportamento/C4/analysis_results-Teste.xlsx`. A matriz numérica da leva C4 revelou uma amostragem de $N = 7$ animais:
* Grupo Controle ($c$): $N = 3$ (`cx9a1`, `cx9a2`, `cx10a3`)
* Grupo 1 ($g_1$): $N = 2$ (`cx9a3`, `cx9a5`)
* Grupo 2 ($g_2$): $N = 2$ (`cx9a4`, `cx10a2`)

*Nota Histórica Documentada:* O aluno realizou mais de 50 cirurgias estereotáxicas ao longo do projeto, das quais mais de 30 animais foram submetidos ao protocolo comportamental completo de Dix & Aggleton (1999). Apenas uma fração foi processada (leva C4), enquanto o restante dos dados brutos em vídeo permanece armazenado em disco externo.

### B. Invalidação da Inferência Estatística por Subdimensionamento Amostral na Leva Processada
* **Evidência:** $N_{\text{controle}} = 3$, $N_{g1} = 2$, $N_{g2} = 2$.
* **Demonstração Matemática de Poder:** Segundo a teoria clássica de dimensionamento amostral (Cohen, 1988, *Statistical Power Analysis for the Behavioral Sciences*), para uma ANOVA One-Way com 3 grupos, nível de significância $\alpha = 0{,}05$ e tamanho de efeito médio a grande ($f = 0{,}40$, equivalente a $d \approx 0{,}8$), o tamanho amostral necessário para atingir poder de $1 - \beta = 0{,}80$ é de $N = 21$ animais por grupo (total $N = 63$).
* **Fato:** Com $N = 2$ ou $3$ por grupo, o poder estatístico calculado é menor que $8\%$. Nessas condições, testes inferenciais paramétricos ou não-paramétricos são matematicamente incapazes de distinguir efeito experimental de flutuação amostral aleatória, incorrendo em inflação massiva de Erro Tipo II e alto risco de falsos positivos pelo efeito do pequeno $N$ (Button et al., 2013, *Nature Reviews Neuroscience*, DOI: 10.1038/nrn3475).

### C. Quebra da Validade Interna por Indeterminação Histológica
* **Evidência Documental:** Conforme registrado no projeto original (Wagner Franklin, 2024, Seção 4.1, p. 5-7), o protocolo cirúrgico baseou-se nas coordenadas do atlas de Paxinos & Franklin (2019) visando a área CA3 do hipocampo.
* **Fato:** A histologia das últimas levas não foi executada e os cortes prévios não confirmaram a ponta do eletrodo em CA3.
* **Impacto Biofísico:** A área CA3 é definida anatomicamente por suas projeções autoassociativas recorrentes colaterais (Amaral & Witter, 1989, *Neuroscience*, DOI: 10.1016/0306-4522(89)90392-7). Caso a ponta do eletrodo tenha se alojado no Giro Denteado, no subículo, na fímbria/fórnix ou em CA1, a topologia de circuito ativada é radicalmente diferente. Como a variável independente (localização anatômica do estímulo) não possui confirmação física, a correlação entre os estímulos aplicados e o comportamento torna-se cientificamente indeterminada.

---

## 2. Autópsia Biofísica dos Mecanismos de Estimulação

### A. Equivalência de Energia dos Padrões 1 e 2
No projeto original de Wagner Franklin (2024, p. 6), os parâmetros definidos foram:
* Frequência portadora: $f_{\theta} = 7{,}14\text{ Hz} \implies T = \frac{1}{7{,}14} \approx 140\text{ ms}$ por ciclo.
* Divisão temporal: 10 bins por ciclo $\implies \Delta t_{\text{bin}} = 14\text{ ms}$.
* Pulso elétrico: Onda quadrada bifásica, amplitude $I = 25\ \mu\text{A}$, largura de pulso $t_{\text{pulse}} = 100\ \mu\text{s}$.
* Palavra binária do Padrão 1: `1010101101` $\implies$ 6 pulsos ativos em 10 bins.
* Palavra binária do Padrão 2: `1110010111` $\implies$ 6 pulsos ativos em 10 bins.

A carga elétrica total injetada por ciclo em ambos os padrões é formalmente:
$$Q_{\text{ciclo}} = N_{\text{pulsos}} \times I \times t_{\text{pulse}} = 6 \times 25\ \mu\text{A} \times 100\ \mu\text{s} = 15\text{ nC}$$
Ambos os padrões entregam a mesma carga líquida e a mesma taxa média intraciclo ($f_{\text{média}} = \frac{6}{140\text{ ms}} = 42{,}86\text{ Hz}$).

### B. Efeito Filtro Passa-Baixa da Membrana Passiva
De acordo com a equação clássica do cabo e do circuito equivalente de membrana celular (Dayan & Abbott, 2001, *Theoretical Neuroscience*, Cap. 5, Eq. 5.5):
$$c_m \frac{dV(t)}{dt} = -\frac{V(t) - E_L}{r_m} + \frac{I_e(t)}{A}$$
onde a constante de tempo da membrana é $\tau_m = r_m c_m$.
* **Valores Empíricos em Piramidais de CA3:** Em registros *whole-cell patch-clamp* em fatias hipocampais de roedores, a constante de tempo de membrana de neurônios piramidais varia tipicamente entre $\tau_m \approx 15\text{ ms}$ e $35\text{ ms}$ (Spruston & Johnston, 1992, *J. Neurophysiol.*, 67(6):1503-1523; Hemond et al., 2008, *J. Neurophysiol.*, 99(3):1335-1355).
* **Consequência Biofísica:** Como os pulsos nos bins ocorrem a cada $14\text{ ms}$ (intervalo inferior ou comparável a $\tau_m$), a capacitância de membrana integra a corrente injetada. Em um neurônio passivo ou isolado, variações de permutação entre bits discretos colapsam em uma curva suave de despolarização média, impossibilitando a descriminação da ordem temporal a nível de neurônio único desacoplado.

### C. A Falha do c-Fos como Biomarcador Temporal na Dissertação de Laura Costa (2026)
Na dissertação de Laura Costa (2026, p. 37-38 e 48-50), foi comparada a estimulação optogenética em CA3 por Padrão Fixo (MSf, 6 pulsos em 10 bins) contra Padrão Aleatório (MSr, pool de permutações com 6 pulsos em 10 bins):
* **Resultado Empírico Documentado:** A contagem de células c-Fos na camada piramidal de CA3 resultou em:
  $$t = 0{,}01423, \quad df = 14, \quad p = 0{,}9888$$
  não havendo qualquer diferença estatística detectável entre os grupos.
* **Mecanismo Biofísico Molecular:** A expressão do gene imediato precoce *c-Fos* depende da fosforilação de CREB mediada por influxo sustentado de $Ca^{2+}$ intracelular (Sheng & Greenberg, 1990, *Neuron*, DOI: 10.1016/0896-6273(90)90351-M). O decaimento de $Ca^{2+}$ livre no citosol possui cinética lenta ($\tau_{Ca} \approx 200\text{--}1000\text{ ms}$), e a fosforilação de CREB ocorre na escala de minutos (Bito, Deisseroth & Tsien, 1996, *Cell*, 87(7):1203-1214). Logo, a transcrição de c-Fos atua biofisicamente como uma integral temporal passa-baixa de longo prazo da energia de ativação celular. Padrões com mesmo número de pulsos/segundo produzem níveis idênticos de c-Fos, corroborando o valor empírico de $p = 0{,}9888$.

### D. A Variável de Fase Teta (*Open-Loop Phase Dispersion*)
As oscilações teta ($4\text{--}8\text{ Hz}$) no hipocampo orquestram flutuações cíclicas de excitabilidade (Buzsáki, 2002, *Neuron*, DOI: 10.1016/S0896-6273(02)00586-X).
* Os disparos piramidais concentram-se preferencialmente no vale do LFP (fase de menor inibição perissomática), enquanto o estímulo no pico colide com inibição sináptica máxima (Brankack, Stewart & Fox, 1993, *Brain Res.*; Skaggs et al., 1996, *Hippocampus*).
* **Falha de Estimulação em Malha Aberta (*Open-Loop*):** Ao injetar trens de pulsos sem sincronismo com o LFP endógeno, a fase inicial de injeção $\theta_0$ varia uniformemente ($\theta_0 \sim \mathcal{U}[0, 2\pi)$). O mesmo trem de pulsos incide ora durante facilitação, ora durante bloqueio inibitório, introduzindo variância estocástica incontrolável entre ensaios sucessivos.

---

## 3. Parâmetros e Equações do Simulador Brian 2

### A. O Modelo Neuronal de Izhikevich (2003)
O sistema dinâmico bidimensional formulado por Izhikevich (2003, *IEEE TNN*, Vol. 14, No. 6, p. 1569-1572, Eqs. 1-3) é:
$$\frac{dv}{dt} = 0{,}04 v^2 + 5 v + 140 - u + I$$
$$\frac{du}{dt} = a(b v - u)$$
$$\text{se } v \ge 30\text{ mV}, \quad \text{então } \begin{cases} v \leftarrow c \\ u \leftarrow u + d \end{cases}$$

Parâmetros canônicos de Izhikevich (2003, Fig. 2):
1. **Neurônios Piramidais Excitatórios (Regular Spiking - RS):**
   * $a = 0{,}02$, $b = 0{,}2$, $c = -65\text{ mV}$, $d = 8$.
2. **Interneurônios Inibitórios GABAérgicos (Fast Spiking - FS):**
   * $a = 0{,}1$, $b = 0{,}2$, $c = -65\text{ mV}$, $d = 2$.

### B. Regra de Plasticidade Sináptica STDP
Parametrização de Song, Miller & Abbott (2000, *Nat. Neurosci.*, 3:919–926) baseada em Bi & Poo (1998):
$$\Delta w = \begin{cases} 
A_+ \exp\left(-\frac{\Delta t}{\tau_+}\right), & \text{se } \Delta t > 0 \quad (\text{LTP}) \\
-A_- \exp\left(\frac{\Delta t}{\tau_-}\right), & \text{se } \Delta t < 0 \quad (\text{LTD}) 
\end{cases}$$
com $\tau_+ = \tau_- = 20\text{ ms}$, $A_+ = 0{,}01$, e $A_- = 0{,}0105$.

### C. Métricas Formais de Distância entre Trens de Disparos
1. **Distância de Victor-Purpura ($D^{\text{spike}}[q]$)** (Victor & Purpura, 1996, *Nature*; 1997, *J. Neurophysiol.*):
   * Custo de inserção/deleção de spike: $1{,}0$.
   * Custo de translação temporal de spike por $\Delta t$: $q \cdot |\Delta t|$.
2. **Distância de van Rossum ($D_R^2$)** (van Rossum, 2001, *Neural Computation*):
   $$D_R^2 = \frac{1}{\tau_R} \int_0^\infty [v_1(t) - v_2(t)]^2 dt$$

---

## 4. Formulação Formal de Hipóteses para o Caminho B

* **Hipótese Nula ($H_0$):**
  > Em uma micro-rede de CA3 parametrizada com neurônios de Izhikevich (RS e FS) e plasticidade STDP, a distância métrica entre as respostas da rede ($D^{\text{spike}}[q]$ de Victor-Purpura e $D_R^2$ de van Rossum) e a divergência da matriz de pesos sinápticos ($\Delta W = \|W_{P1} - W_{P2}\|_F$) sob estimulação com o Padrão 1 (`1010101101`) e Padrão 2 (`1110010111`) não diferem significativamente da variação estocástica induzida por ruído gaussiano intrínseco, qualquer que seja a fase de acoplamento com a oscilação teta ($p > 0{,}05$).

* **Hipótese Alternativa Primária ($H_{1A}$ - Travamento de Fase / Closed-Loop):**
  > A discriminação temporal entre os Padrões 1 e 2 é estritamente dependente da fase de injeção $\theta$ relativa à oscilação teta endógena ($7\text{ Hz}$). Quando o início do trem é travado em malha fechada (*phase-locking*) no vale despolarizante da oscilação ($\theta = \pi$), a distância de Victor-Purpura $D^{\text{spike}}[q=100\text{ s}^{-1}]$ entre os trens de saída de CA3 é significativamente maior do que sob injeção em malha aberta com fase aleatória uniforme ($\theta \sim \mathcal{U}[0, 2\pi)$), atingindo $p < 0{,}001$.

* **Hipótese Alternativa Secundária ($H_{1B}$ - Inibição Recorrente Rápida por Interneurônios FS):**
  > A divergência nos pesos sinápticos finais ($\Delta W_{\text{STDP}}$) entre o Padrão 1 e o Padrão 2 requer uma razão mínima de interneurônios inibitórios rápidos ($FS \ge 15\%$). Na ausência de realimentação inibitória rápida (rede puramente excitatória com interneurônios desconectados), os neurônios piramidais entram em saturação de disparo por auto-excitação recorrente, colapsando a distância métrica $D^{\text{spike}}$ para valores indistinguíveis da hipótese nula ($p > 0{,}05$).
