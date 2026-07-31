import os
import joblib
import pandas as pd
from typing import Optional
from flask import Flask, request, jsonify
from pydantic import BaseModel, Field, ValidationError

app = Flask(__name__)

# ==========================================
# 1. CARREGAMENTO DOS ARQUIVOS JOBLIB
# ==========================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CAMINHO_MODELO = os.path.join(BASE_DIR, "modelo_risco_defasagem.joblib")
CAMINHO_METADADOS = os.path.join(BASE_DIR, "metadados_modelo.joblib")

try:
    # 1. Carrega o modelo executável real
    pipeline = joblib.load(CAMINHO_MODELO)
    print("✅ Modelo carregado com sucesso!")

    # 2. Carrega os metadados (para extrair o limiar, se existir)
    if os.path.exists(CAMINHO_METADADOS):
        metadados = joblib.load(CAMINHO_METADADOS)
        limiar = metadados.get("limiar", 0.5)
    else:
        limiar = 0.5

except Exception as e:
    print(f"❌ Erro ao carregar os arquivos: {e}")
    pipeline = None
    limiar = 0.5


# ==========================================
# 2. DEFINIÇÃO DOS DADOS DE ENTRADA (PYDANTIC)
# ==========================================
class InputData(BaseModel):
    Ano_Referencia: int
    Idade: float
    Ano_Ingresso: int
    Fase: str
    Genero: str = Field(..., alias="Gênero")
    Instituicao: str
    Pedra_Atual: str
    INDE: float
    IAN: float
    IDA: float
    IEG: float
    IAA: float
    IPS: float
    IPP: Optional[float] = None
    IPV: float
    Matematica: float
    Portugues: float
    Ingles: Optional[float] = None

    class Config:
        populate_by_name = True


# ==========================================
# 3. ROTA DA API
# ==========================================
@app.route("/predict", methods=["POST"])
def predict():
    if pipeline is None:
        return jsonify({"error": "Modelo não foi carregado corretamente no servidor."}), 500

    try:
        data = request.get_json()
        input_data = InputData(**data)

        # Converte em DataFrame
        features = pd.DataFrame([input_data.model_dump(by_alias=True)])

        # IMPORTANTE: A ordem das colunas no DataFrame precisa ser a mesma usada no treino.
        # Caso o pipeline falhe por conta da ordem das features, descomente a linha abaixo
        # (se você extrair a lista de features do arquivo metadados)
        # features = features[metadados["features"]]

        # Executa a predição no objeto do modelo extraído
        if hasattr(pipeline, "predict_proba"):
            proba = pipeline.predict_proba(features)[:, 1]
            prediction = int(proba[0] >= limiar)
        else:
            prediction = pipeline.predict(features)[0]

        return jsonify({
            "status": "200 OK",
            "data": {
                "prediction": str(prediction)
            }
        }), 200

    except ValidationError as e:
        return jsonify({"error": e.errors()}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ==========================================
# 4. INICIALIZAÇÃO DO SERVIDOR
# ==========================================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    print(f"🚀 Iniciando servidor Flask na porta {port}...")
    app.run(host="0.0.0.0", port=port, debug=True)