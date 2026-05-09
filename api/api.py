from flask import Flask, request, jsonify
from pydantic import BaseModel, ValidationError
import pandas as pd
import joblib


app = Flask(__name__)

model = joblib.load("/model_data/obesity_model.pkl")


class InputData(BaseModel):
    Gender: str
    Age: float
    Height: float
    Weight: float
    family_history: str
    FAVC: str
    FCVC: float
    NCP: float
    CAEC: str
    SMOKE: str
    CH2O: float
    SCC: str
    FAF: float
    TUE: float
    CALC: str
    MTRANS: str


@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "status": "API funcionando",
        "message": "API de predição de obesidade"
    })


@app.route("/predict", methods=["POST"])
def predict():
    try:
        input_data = InputData(**request.get_json())

        data = pd.DataFrame([{
            "Gender": input_data.Gender,
            "Age": input_data.Age,
            "Height": input_data.Height,
            "Weight": input_data.Weight,
            "family_history": input_data.family_history,
            "FAVC": input_data.FAVC,
            "FCVC": round(input_data.FCVC),
            "NCP": round(input_data.NCP),
            "CAEC": input_data.CAEC,
            "SMOKE": input_data.SMOKE,
            "CH2O": round(input_data.CH2O),
            "SCC": input_data.SCC,
            "FAF": round(input_data.FAF),
            "TUE": round(input_data.TUE),
            "CALC": input_data.CALC,
            "MTRANS": input_data.MTRANS
        }])

        prediction = model.predict(data)[0]
        probabilities = model.predict_proba(data)[0]
        classes = model.classes_

        probabilities_dict = {
            str(classes[i]): float(probabilities[i])
            for i in range(len(classes))
        }

        return jsonify({
            "status": "success",
            "prediction": prediction,
            "probabilities": probabilities_dict
        }), 200

    except ValidationError as error:
        return jsonify({
            "status": "error",
            "message": "Dados de entrada inválidos",
            "details": error.errors()
        }), 400

    except Exception as error:
        return jsonify({
            "status": "error",
            "message": str(error)
        }), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)