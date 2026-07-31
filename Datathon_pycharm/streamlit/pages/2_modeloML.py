import streamlit as st
import requests

# Dicionários de mapeamento para as variáveis do dataset PEDE
opcoes_genero = {
    "Femenino": "♀️ Feminino",
    "Masculino": "♂️ Masculino"
}

opcoes_fase = {
    "FASE 0": "🌱 Fase 0",
    "FASE 1": "🌿 Fase 1",
    "FASE 2": "🌳 Fase 2",
    "FASE 3": "🎓 Fase 3",
    "FASE 4": "🚀 Fase 4",
    "FASE 5": "⭐ Fase 5",
    "FASE 6": "🏆 Fase 6",
    "FASE 7": "👑 Fase 7",
    "FASE 8": "🥇 Fase 8"
}

opcoes_pedra = {
    "Quartzo": "🔮 Quartzo",
    "Ágata": "💎 Ágata",
    "Ametista": "💜 Ametista",
    "Topázio": "💛 Topázio"
}

opcoes_instituicao = {
    "Escola Pública": "🏫 Escola Pública",
    "Escola Privada": "🏛️ Escola Privada"
}

# Interface principal
st.title("🎓 Passos Mágicos: Avaliação de Estudantes")
st.write("Insira abaixo as características do estudante para realizar a predição de risco:")

st.markdown("---")

# Campos de entrada básicos
col_b1, col_b2, col_b3 = st.columns(3)

with col_b1:
    Ano_Referencia = st.number_input("Ano de Referência", min_value=2020, max_value=2030, value=2024, step=1)
with col_b2:
    Idade = st.number_input("Idade do Estudante", min_value=4.0, max_value=30.0, value=12.0, step=0.5)
with col_b3:
    Ano_Ingresso = st.number_input("Ano de Ingresso", min_value=2010, max_value=2030, value=2020, step=1)

col_b4, col_b5, col_b6 = st.columns(3)

with col_b4:
    Fase = st.selectbox("Fase Atual", options=list(opcoes_fase.keys()), format_func=lambda x: opcoes_fase[x])
with col_b5:
    Genero = st.selectbox("Gênero", options=list(opcoes_genero.keys()), format_func=lambda x: opcoes_genero[x])
with col_b6:
    Instituicao = st.selectbox("Tipo de Instituição", options=list(opcoes_instituicao.keys()),
                               format_func=lambda x: opcoes_instituicao[x])

Pedra_Atual = st.selectbox("Pedra Atual", options=list(opcoes_pedra.keys()), format_func=lambda x: opcoes_pedra[x])

st.markdown("---")
st.subheader("📊 Indicadores de Desempenho (0 a 10)")

col1, col2 = st.columns(2)

with col1:
    INDE = st.number_input("INDE (Índice de Dev. Educacional)", min_value=0.0, max_value=10.0, value=7.0, step=0.1)
    IAN = st.number_input("IAN (Indicador de Adequação Nível)", min_value=0.0, max_value=10.0, value=5.0, step=0.1)
    IDA = st.number_input("IDA (Indicador de Desempenho Acadêmico)", min_value=0.0, max_value=10.0, value=7.0, step=0.1)
    IEG = st.number_input("IEG (Indicador de Engajamento)", min_value=0.0, max_value=10.0, value=8.0, step=0.1)

with col2:
    IAA = st.number_input("IAA (Indicador de Autoavaliação)", min_value=0.0, max_value=10.0, value=8.0, step=0.1)
    IPS = st.number_input("IPS (Indicador Psicossocial)", min_value=0.0, max_value=10.0, value=7.0, step=0.1)
    IPV = st.number_input("IPV (Indicador Ponto de Virada)", min_value=0.0, max_value=10.0, value=7.0, step=0.1)

st.markdown("---")
st.subheader("📚 Notas de Disciplinas (0 a 10)")

col_mat, col_por, col_ing = st.columns(3)

with col_mat:
    Matematica = st.number_input("Matemática", min_value=0.0, max_value=10.0, value=7.0, step=0.1)

with col_por:
    Portugues = st.number_input("Português", min_value=0.0, max_value=10.0, value=7.0, step=0.1)

with col_ing:
    usa_ingles = st.checkbox("Possui nota de Inglês?")
    Ingles = st.number_input("Inglês", min_value=0.0, max_value=10.0, value=7.0, step=0.1) if usa_ingles else None

usa_ipp = st.checkbox("Possui valor de IPP (Indicador Psicopedagógico)?")
IPP = st.number_input("IPP", min_value=0.0, max_value=10.0, value=5.0, step=0.1) if usa_ipp else None

st.markdown("---")

# Botão para realizar a predição
if st.button("🔮 Calcular Predição", use_container_width=True):

    input_data = {
        "Ano_Referencia": int(Ano_Referencia),
        "Idade": float(Idade),
        "Ano_Ingresso": int(Ano_Ingresso),
        "Fase": Fase,
        "Gênero": Genero,
        "Instituicao": Instituicao,
        "Pedra_Atual": Pedra_Atual,
        "INDE": float(INDE),
        "IAN": float(IAN),
        "IDA": float(IDA),
        "IEG": float(IEG),
        "IAA": float(IAA),
        "IPS": float(IPS),
        "IPP": float(IPP) if IPP is not None else None,
        "IPV": float(IPV),
        "Matematica": float(Matematica),
        "Portugues": float(Portugues),
        "Ingles": float(Ingles) if Ingles is not None else None
    }

    try:
        response = requests.post(
            "http://127.0.0.1:5000/predict",
            json=input_data,
            timeout=30
        )

        if response.status_code == 200:
            result = response.json()
            predicao = result['data']['prediction']

            st.markdown("### 🎯 Resultado da Análise:")

            # Tratamento visual do resultado
            if predicao == "1":
                st.error("⚠️ **ALERTA: ESTUDANTE EM RISCO DE DEFASAGEM**")
                st.write(
                    "O modelo prevê que este aluno tem alta probabilidade de cursar uma fase abaixo da ideal para a sua idade no próximo ano. Recomenda-se acompanhamento pedagógico e psicossocial prioritário.")
            elif predicao == "0":
                st.success("✅ **PROGRESSÃO ADEQUADA: SEM RISCO DE DEFASAGEM**")
                st.write(
                    "O modelo prevê que este aluno continuará progredindo normalmente de acordo com a sua fase ideal.")
                st.balloons()  # Animação visual no Streamlit
            else:
                st.warning(f"Predição retornou um valor não esperado: {predicao}")

        else:
            st.error(f"Erro da API ({response.status_code}): {response.text}")

    except requests.exceptions.ConnectionError:
        st.error("❌ Não foi possível conectar à API. Verifique se o servidor Flask está rodando no terminal.")

    except requests.exceptions.Timeout:
        st.error("⏰ A API demorou muito para responder. Tente novamente.")

    except Exception as e:
        st.error(f"⚠️ Erro inesperado: {e}")