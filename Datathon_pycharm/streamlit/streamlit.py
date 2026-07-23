import streamlit as st
import sys
import os
import pandas as pd
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

from api import graficos as graf
caminho_csv = os.path.join(BASE_DIR, "api", "dados_tratados.csv")
dados = pd.read_csv(caminho_csv)
st.set_page_config(page_title="Datathon")

st.title(":blue[DATA]THON",text_alignment="center")

st.markdown('<span style="font-size:26px">PROJETO'
            '<span style="color:#6baed6;" > PASSOS</span>'
            '<span style="color:#2171b5"> MÁGICO</span> '
            '</span>',unsafe_allow_html=True,text_alignment="center")

#Pergunta 1 IAN
st.subheader("1. Adequação do nível (IAN)",text_alignment="justify")
st.markdown(
    "Adequação do Nível (IAN) entre os anos de 2022 e 2024 — pontos identificados:"
    "<br>- **2022:** 573 alunos (66,63%) estavam em defasagem moderada e apenas 259 (30,12%) no nível adequado."
    "<br>- **2023:** O número de defasagem moderada diminuiu para 538 (53,06%) e houve um aumento de 15,44% em alunos adequados, totalizando 462 (45,56%)."
    "<br>- **2024:** Houve um aumento de 9,80% nos alunos adequados, chegando a 662 (55,35%), e uma diminuição de 8,66% nos alunos com defasagem moderada, caindo para 531 (44,40%)."
    "<br><br>Mesmo com o aumento na quantidade total de alunos, a taxa de defasagem severa diminuiu, chegando a apenas 3 alunos em 2024.",
    unsafe_allow_html=True,
)
df1 = graf.dados_ian.tabela_ian(dados)
st.bar_chart( df1,color=["#8FFFE1", "#0BA3FF", "#FF7074"],stack=False)

st.markdown(
    "Do ano de 2022 para 2023, 185 alunos melhoraram, 104 pioraram e 320 permaneceram no mesmo nível."
    "<br><span style='color: #8FFFE1;'>- De 2023 para 2024, houve um aumento de 69,19% nos alunos que melhoraram, passando de 185 para 313.</span>"
    "<br><span style='color: #0BA3FF;'>- De 2023 para 2024, a quantidade de alunos que mantiveram o nível permaneceu estável, variando de 320 para 311 (redução de 2,89%).</span>"
    "<br><span style='color: #FF7074;'>- De 2023 para 2024, houve um aumento de 26,92% nos alunos que pioraram, passando de 104 para 132.</span>",
    unsafe_allow_html=True,
)
df2 = graf.dados_ian.tabela_melhora(dados)
st.bar_chart(df2,color=["#8FFFE1", "#0BA3FF", "#FF7074"],stack=False)

#Pergunta 2 IDA
st.subheader("2. Desempenho acadêmico (IDA)",text_alignment="justify")

st.markdown(
    "**O desempenho acadêmico médio (IDA) sofreu oscilações, mantendo-se em um patamar de estabilidade ao longo do período.**"
    "<br><span style='color: #8FFFE1;'>- De 2022 para 2023, houve melhoria: a média subiu de 6,09 para 6,66 (+9,36%) e as notas ficaram mais homogêneas.</span>"
    "<br><span style='color: #FF7074;'>- De 2023 para 2024, houve uma leve queda: a média recuou de 6,66 para 6,35 (-4,68%) com maior dispersão nas notas.</span>"
    "<br><span style='color: #0BA3FF;'>- No acumulado geral (2022 a 2024), a média teve um saldo ligeiramente positivo (de 6,09 para 6,35), mesmo com o aumento do total de alunos (de 860 para 1.055).</span>",
    unsafe_allow_html=True,
)
ida = graf.dados_ida.ida_media(dados)
st.pyplot(ida)
st.markdown(
    "**Análise do IDA Médio por Fase ao longo dos anos (2022 - 2024):**"
    "<br><span >- As fases iniciais (ALFA, Fase 1) e finais (Fase 6 e Fase 8) apresentam o melhor desempenho acadêmico, atingindo médias de até 8,00.</span>"
    "<br><span >- As fases intermediárias (especialmente Fase 3) concentram as menores médias do período, variando entre 5,14 e 5,75.</span>"
    "<br><span >- A maioria das fases seguiu o padrão geral: alta expressiva em 2023 (como a Fase 7, que saltou de 5,25 para 7,81) seguida de uma retração em 2024.</span>",
    unsafe_allow_html=True,
)
ida = graf.dados_ida.ida_heatmap(dados)
st.pyplot(ida)

st.markdown("Abaixo está a tabela de alunos dos anos de 2022 para 2023, e de 2023 para 2024 com % de melhoria e variação")
ida = graf.dados_ida.evo_ida(dados)
st.table(ida)

#Pergunta 3 IEG
st.subheader("3. Engajamento nas atividades (IEG)",text_alignment="justify")
st.markdown(
    "**Sim, o engajamento dos alunos (IEG) possui relação direta e positiva com o desempenho acadêmico (IDA) e o ponto de virada (IPV):**"
    "<br><span>- **Engajamento x Ponto de Virada (IEG x IPV):** Apresenta correlação positiva moderada a forte (r = 0,542), mostrando que maior engajamento aumenta expressivamente as chances do aluno atingir o ponto de virada.</span>"
    "<br><span>- **Engajamento x Desempenho (IEG x IDA):** Correlação positiva de r = 0,498, confirmando que o aumento do engajamento acompanha o crescimento das notas/desempenho do estudante.</span>"
    "<br><span>- **Relação Direta (IDA x IPV):** A correlação mais alta do conjunto é entre o desempenho e o ponto de virada (r = 0,557), demonstrando a sinergia entre todas as métricas.</span>"
    "<br>Abaixo está o grafíco de scatter plot e a tabela de relação:",
    unsafe_allow_html=True,
)
fig, df = graf.dados_ieg.ieg(dados)
st.pyplot(fig,width=1200)
st.table(df)

#Pergunta 4 IAA
st.subheader("4. Autoavaliação (IAA)",text_alignment="justify")
st.markdown(
    "**Não são totalmente coerentes: há uma tendência geral dos alunos de superestimarem seu desempenho (IAA > IDA):**"
    "<br><span>- **Autoavaliação Otimista (IAA vs IDA):** No gráfico de dispersão, a grande maioria dos pontos está situada acima da linha pontilhada ($y = x$), demonstrando que as notas de autoavaliação são sistematicamente maiores que as notas reais.</span>"
    "<br><span>- **Gap de Autoavaliação Positivo:** O boxplot confirma essa distorção: a mediana da diferença ($IAA - IDA$) permanece positiva em todos os anos (entre +1,0 e +2,0 pontos).</span>"
    "<br><span>- **Presença de Discrepâncias Extremas:** Em 2023 e 2024, há uma presença expressiva de *outliers* negativos (alunos que se avaliaram muito abaixo do desempenho real), além dos casos graves de superestimativa na parte superior.</span>",
    unsafe_allow_html=True,
)
iaa = graf.dados_iaa.grafico_iaa(dados)
st.pyplot(iaa)

#Pergunta 5
st.subheader("5. Aspectos psicossociais (IPS)",text_alignment="justify")
st.markdown(
    "**Sim, o Índice Psicossocial (IPS) revela padrões claros sobre a probabilidade e a intensidade das quedas no desempenho (IDA) e no engajamento (IEG):**"
    "<br><span>- **Vulnerabilidade em Faixas Críticas (IPS Baixo: 2.5 a 5.0):** Alunos nessa faixa apresentam a maior taxa de queda no engajamento (61,57%) e as perdas médias mais severas no período (Delta IDA de -0,46 e Delta IEG de -0,76).</span>"
    "<br><span>- **Zona de Proteção e Crescimento (IPS Moderado-Alto: 6.9 a 7.5):** É a única faixa onde a variação média foi POSITIVA (Delta IDA de +0,22 e Delta IEG de +0,19), apresentando também as menores taxas de queda (45,16% no IDA e 37,54% no IEG).</span>"
    "<br><span>- **Anomalia na Faixa Superior (IPS Alto: 7.5 a 10.0):** Alunos no topo do IPS voltam a registrar queda acentuada (54,35% no IDA e 56,88% no IEG), indicando que pontuações psicossociais muito altas também exigem acompanhamento contra queda de rendimento.</span>",
    unsafe_allow_html=True,
)
ips = graf.dados_ips.df_ips(dados)
st.table(ips)

#Pergunta 6
st.subheader("6. Aspectos psicopedagógicos (IPP)",text_alignment="justify")
st.markdown(
    "**As avaliações psicopedagógicas (IPP) confirmam apenas parcialmente a defasagem do IAN, apresentando baixa diferenciação entre as faixas:**"
    "<br><span>- **Coerência na Média Geral:** A nota média do IPP diminui gradativamente conforme a severidade do IAN — caindo de 7,68 (Adequado) para 7,46 (Defasagem moderada) e 7,01 (Defasagem severa).</span>"
    "<br><span>- **Convergência nas Medianas:** As medianas dos grupos de defasagem moderada e severa são idênticas (7,50), e a do grupo adequado é apenas ligeiramente superior (7,71), mostrando sobreposição quase total nos boxplots.</span>"
    "<br><span>- **Discrepância nos Casos Críticos:** Alunos com Defasagem Severa ainda mantêm média elevada no IPP (7,01), sugerindo que a avaliação psicopedagógica identifica potencial pedagógico mesmo em estudantes com grande defasagem de nível/idade.</span>",
    unsafe_allow_html=True,
)
fig, df = graf.dados_ipp_VS_ian.ippVSian(dados)
st.pyplot(fig)
st.table(df)

#Pergunta 7
st.subheader("7. Ponto de virada (IPV)",text_alignment="justify")
st.markdown(
    "**Com base na importância das variáveis (Feature Importance por permutação), os aspectos psicopedagógicos, de engajamento e acadêmicos são os determinantes para explicar o IPV:**"
    "<br>- **Aspectos Psicopedagógicos (IPP):** O IPP é a variável de maior impacto absoluto na explicação do IPV (queda de R² superior a 0.25), destacando que a avaliação psicopedagógica e o acompanhamento do desenvolvimento do aluno são o fator mais decisivo."
    "<br>- **Engajamento (IEG) e Desempenho (IDA):** Formam o segundo pilar mais importante. O nível de engajamento diário/comportamental (IEG) e os resultados acadêmicos concretos (IDA) possuem peso expressivo e direto no ponto de virada."
    "<br>- **Menor Impacto Relativo (IPS, IAA, IAN e Demográficos):** Fatores como aspecto psicossocial (IPS), autoavaliação (IAA), idade e a defasagem de idade-série (IAN) apresentam impacto marginal na variação do R² em comparação às métricas pedagógicas e de engajamento.",
    unsafe_allow_html=True,
)
ipv = graf.dados_ipv.ipv(dados)
st.pyplot(ipv)

#Pergunta 8
st.subheader("8. Multidimensionalidade dos indicadores",text_alignment="justify")
st.markdown(
    "**As combinações que mais elevam o INDE concentram-se no alto desempenho (IDA), engajamento (IEG) e suporte psicopedagógico (IPP):**"
    "\n\n- **Combinação Máxima (8,42):** A junção de todos os indicadores em nível alto (IDA + IEG + IPS + IPP) atinge o maior INDE médio do programa (8,4229 em 307 alunos)."
    "\n- **A Força do Núcleo IDA + IEG:** Conforme a matriz de correlação, IDA (r = 0,78) e IEG (r = 0,71) são as variáveis mais determinantes. Na tabela, manter IDA e IEG altos com pelo menos IPP alto garante INDE acima de 8,08, mesmo se o IPS for baixo."
    "\n- **Impacto Secundário do IPS:** O IPS apresenta a menor correlação direta com o INDE (r = 0,26). Sua presença potencializa a nota máxima, mas isoladamente não sustenta um INDE elevado."
)
fig,df = graf.dados_Muldidimensao.indicador(dados)
st.pyplot(fig)
st.table(df)

#Pergunta 9
st.subheader("9. Previsão de risco com Machine Learning",text_alignment="justify")
st.markdown(
    "**Análise do Modelo Preditivo e Padrões de Risco de Defasagem:**"
    "\n\n- Modelo Preditivo Selecionado (Random Forest):** Apresentou a melhor performance preditiva entre os testados, atingindo **Acurácia de 73,07%**, **Precisão de 74,29%** e **ROC_AUC de 0,7961**, demonstrando alta capacidade de discriminação para estimar a probabilidade de risco dos alunos.")
df = graf.dados_risco.comp_model()
st.table(df)

st.markdown(
    "\n\n- **Principais Padrões e Variáveis Antecipadoras:**"
    "\n  * **IAN (Adequação de Nível):** É com folga a variável de maior relevância preditiva no modelo. Histórico de instabilidade no IAN é o principal gatilho de risco."
    "\n  * **IPV (Ponto de Virada) e Fase:** Formam o segundo pilar mais forte. Alunos em fases específicas ou com queda no IPV sinalizam fragilidade iminente no desempenho."
    "\n  * **Idade e INDE:** Completam os 5 principais preditores de risco, mostrando que a distorção idade-série e o indicador global antecedem perdas acadêmicas maiores."
    "\n  * **Desempenho por Matéria (Matemática x Português):** Dificuldades específicas em Matemática possuem peso consideravelmente superior às de Português ou Inglês para prever o risco."
    "\n\n- **3. Aplicação Prática (Probabilidade de Risco Individual):** A tabela de inferência calcula a probabilidade individual de risco para cada aluno (RA). Isso possibilita intervenções preventivas da equipe pedagógica antes que a queda de desempenho ou defasagem se consolide de fato.",
)
test = graf.dados_risco.imp_var()
st.pyplot(test)
st.markdown("\n\n- Abaixo está a lista de 50 alunos com maior probabilidade de risco:")
df = graf.dados_risco.st_prior()
st.dataframe(df)

#Pergunta 10
st.subheader("10. Efetividade do programa",text_alignment="justify")
st.markdown(
    "**Visão Geral do Ciclo (2022 a 2024): Melhora Parcial, sem Consistência Irrestrita**\n\n"
    "- **INDE e IAN em Crescimento Contínuo:** O indicador global (**INDE**) apresentou evolução gradual positiva no acumulado (7,04 em 2022 $\\rightarrow$ 7,34 em 2023 $\\rightarrow$ 7,40 em 2024). A adequação de nível (**IAN**) foi o grande destaque positivo, subindo de 6,42 em 2022 para 7,68 em 2024.\n"
    "- **Oscilação nos Demais Indicadores (Pico em 2023):** Indicadores fundamentais como **IDA** (desempenho), **IEG** (engajamento) e **IPV** (ponto de virada) atingiram seu ponto máximo em 2023, porém sofreram recuo em 2024 (ex: IDA caiu de 6,66 para 6,35; IEG caiu de 8,70 para 7,38).\n"
    "- **Recuperação Emocional em 2024:** Enquanto o engajamento caiu em 2024, a autoavaliação (**IAA**) e o aspecto psicossocial (**IPS**) recuperaram-se fortemente após a queda de 2023."
)
line = graf.dados_efetivo.efetividade(dados)
st.table(line)
st.line_chart(line.T,y_label="Média",x_label="Ano")
st.markdown(
    "**Análise das Transições Individuais dos Alunos:**\n\n"
    "- **Transição 2022 $\\rightarrow$ 2023 (Avanço no Ponto de Virada e Engajamento):** Mais da metade dos alunos apresentou melhoria no engajamento (**55,5% no IEG**) e, principalmente, no ponto de virada (**64,5% no IPV**, com variação média positiva de +0,52).\n"
    "- **Transição 2023 $\\rightarrow$ 2024 (Desafios de Manutenção):** A maioria dos alunos registrou queda individual no engajamento e desempenho (apenas **28,36% melhoraram no IEG** e **37,65% no IDA**). Por outro lado, **55,16% dos alunos melhoraram no IPS** e **47,71% no IAA**.\n"
    "- **Consistência do IAN:** Em ambas as transições, a adequação de nível manteve variação média positiva (+0,39 e +0,57), comprovando a redução constante da defasagem no programa."
)
df = graf.dados_efetivo.variacao(dados)
st.table(df)
st.markdown(
    "**Evolução por Fase/Pedra e Redução da Defasagem:**\n\n"
    "- **Hierarquia Clara entre as Pedras:** O desempenho acompanha diretamente a evolução das pedras: **Topázio** apresenta os maiores indicadores em todos os anos (INDE de ~8,40 a 8,46 e IDA > 8,10), seguido por **Ametista** (~7,50), **Ágata** (~6,50 a 6,60) e **Quartzo** (~5,24 a 5,55).\n"
    "- **Redução Substancial da Defasagem Média:** Todas as pedras reduziram significativamente a defasagem ao longo dos anos. O destaque é o **Topázio**, que quase zerou a defasagem em 2024 (-0,0399 contra -0,3385 em 2022).\n"
    "- **Conclusão sobre o Impacto do Programa:** O programa confirma impacto real e estrutural no combate à defasagem (**IAN**) e na elevação da nota global (**INDE**), porém a variação negativa de **IDA** e **IEG** entre 2023 e 2024 nas fases intermediárias (Quartzo e Ágata) demonstra que a melhora não é totalmente linear ou contínua para todos os alunos."
)
test = graf.dados_efetivo.stone(dados)
st.table(test)
