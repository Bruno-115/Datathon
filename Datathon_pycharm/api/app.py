import streamlit as st
import pandas as pd
import joblib
import os

# 1. Carrega o modelo no topo do arquivo Streamlit
# Ajuste o caminho para onde o seu joblib realmente está na nuvem
caminho_modelo = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'api', 'modelo_risco_defasagem.joblib'))

try:
    pipeline = joblib.load(caminho_modelo)
except Exception as e:
    st.error(f"Erro ao carregar o modelo: {e}")
    pipeline = None

# ... (seu código de interface visual, selects, number_inputs, etc) ...

if st.button("🔮 Calcular Predição", use_container_width=True):
    if pipeline is None:
        st.error("O modelo não pôde ser carregado. Verifique os arquivos.")
    else:
        # 2. Cria o DataFrame direto com as variáveis do Streamlit
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

        features = pd.DataFrame([input_data])

        try:
            # 3. Faz a predição diretamente no Streamlit (sem usar API)
            if hasattr(pipeline, "predict_proba"):
                proba = pipeline.predict_proba(features)[:, 1]
                predicao = int(proba[0] >= 0.5)  # Limiar padrão
            else:
                predicao = int(pipeline.predict(features)[0])

            # Tratamento visual do resultado
            st.markdown("### 🎯 Resultado da Análise:")
            if predicao == 1:
                st.error("⚠️ **ALERTA: ESTUDANTE EM RISCO DE DEFASAGEM**")
                st.write(
                    "O modelo prevê que este aluno tem alta probabilidade de cursar uma fase abaixo da ideal para a sua idade no próximo ano.")
            elif predicao == 0:
                st.success("✅ **PROGRESSÃO ADEQUADA: SEM RISCO DE DEFASAGEM**")
                st.write(
                    "O modelo prevê que este aluno continuará progredindo normalmente de acordo com a sua fase ideal.")
                st.balloons()

        except Exception as e:
            st.error(f"Erro ao processar predição: {e}")