from flask import Flask
from flask import request
from flask_cors import CORS
from dotenv import load_dotenv
import os
import datetime
import pandas as pd
from io import BytesIO
import base64

load_dotenv()

app = Flask(__name__)
CORS(app)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")



# Poslat seznam dostupných akcií
@app.route("/api/stocks", methods=["GET"])
def get_stocks():
    try:
        files = os.listdir("data") 
        file_names = [f for f in files if os.path.isfile(os.path.join("data", f))]
        stock_names = [os.path.splitext(f)[0] for f in file_names]
        return {"stocks": stock_names}, 200
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


def load_data(stock):
    data = pd.read_csv(f"data/{stock}.csv")
    return data


# Poslat adjusted close data
@app.route("/api/stock/<string:stock>/data", methods=["GET"])
def get_stock_data(stock):
    try:
        data = load_data(stock)
        data["date"] = pd.to_datetime(data["date"]).dt.strftime('%Y-%m-%d')
        data = data[["date", "adjusted"]].to_dict(orient="records")
        return {"data": data}, 200
    except Exception as e:
        return {"error": str(e)}, 500


# Poslat dostupné feature
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
@app.route("/api/<string:stock>/train", methods=["POST"])
def post_model(stock):
    try:
        data = request.get_json()
        if not data:
            return {"error": "No data provided"}, 400
        for param in data:
            if param in model_params:
               model_params[param] = data[param]

        lag_df = lag_features(load_data(stock), model_params["features"])

        return {"message": "Model parameters updated", "model_params": model_params}, 200
    except Exception as e:
        return {"error": str(e)}, 500


# Vytvořit lag features
def lag_features(df, features):
    lag_df = pd.DataFrame()
    for lag in features:
        for feature in features[lag]:
            lag_df[f"{feature}_{lag}"] = df[feature].shift(int(lag))

    return lag_df



if __name__ == "__main__":
    app.run(debug=True)