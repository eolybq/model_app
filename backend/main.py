from flask import Flask, request, session
from flask_cors import CORS
from dotenv import load_dotenv
import os
import pandas as pd

from services.data_manipulation import fetch_save_ticker


load_dotenv()

app = Flask(__name__)
CORS(app)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")


# Dostani tickeru z frontend a ulozeni dat
@app.route("/api/ticker", methods=["POST"])
def post_ticker():
    try:
        data = request.get_json()
        if not data or "ticker" not in data:
            return {"error": "No ticker provided"}, 400
        ticker = data["ticker"].upper()
        session['selected_ticker'] = ticker
        df = fetch_save_ticker(ticker, data["period"], data["interval"])

        data_to_frontend = df[["date", "adjusted"]].to_dict(orient="records")
        return {"data": data_to_frontend}, 200
    except Exception as e:
        return {"error": str(e)}, 500


# Poslat seznam dostupných modelů
@app.route("/api/models", methods=["GET"])
def get_models():
    try:
        files = os.listdir("models") 
        file_names = [f for f in files if os.path.isfile(os.path.join("models", f))]
        model_names = [os.path.splitext(f)[0] for f in file_names]
        return {"models": model_names}, 200
    except Exception as e:
        return {"error": str(e)}, 500


# Poslat dostupné feature
# TODO: Udělat fixní list features ktere lze vytvorit z dat -> budou se vytvaret ve prepare_features
@app.route("/api/get_features/<string:stock>", methods=["GET"])
def get_features(stock):
    try:
        data = load_data(stock)
        columns = list(data.columns)
        columns.remove("date")
        return {"features": columns}, 200
    except Exception as e:
        return {"error": str(e)}, 500


# Výchozí parametry modelu
model_params = {
    "model_type": "grad",
    "features": {},
    "learning_rate": 0.001,
    "epochs": 100,
    "batch_size": 32
}

# Získat parametry modelu
@app.route("/api/train", methods=["POST"])
def post_model():
    try:
        data = request.get_json()
        if not data:
            return {"error": "No data provided"}, 400
        for param in data:
            if param in model_params:
               model_params[param] = data[param]

        # TODO: train_model(model_params, session['selected_ticker'])

        lag_df = lag_features(load_data(stock), model_params["features"])

        return {"message": "Model parameters updated", "model_params": model_params}, 200
    except Exception as e:
        return {"error": str(e)}, 500




if __name__ == "__main__":
    app.run(debug = True, host = "localhost", port = 5055)
