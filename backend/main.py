from flask import Flask, request, session
from flask_cors import CORS
from dotenv import load_dotenv
import os
import pandas as pd

from services.data_manipulation import fetch_save_ticker, load_user_data
from services.prepare_features import lag_features, calculate_features, ema_model, rsi_model, atr_model

from models.arima import arima_model

load_dotenv()

app = Flask(__name__)
CORS(app)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")


# Dostani tickeru z frontend a ulozeni dat
@app.route("/api/<string:ticker>/ticker", methods=["GET"])
def post_ticker(ticker):
    try:
        df = fetch_save_ticker(ticker)

        min_date = df["date"].min().strftime("%Y-%m-%d")
        max_date = df["date"].max().strftime("%Y-%m-%d")

        out = pd.DataFrame({
            "date": df["date"].dt.strftime("%Y-%m-%d"),
            "close": df["close"]
        })

        data_to_frontend = out.to_dict(orient="records")
        return {"data": data_to_frontend, "min_date": min_date, "max_date": max_date}, 200
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

# Nahrani celeho df na client side
@app.route("/api/<string:ticker>/df_data", methods=["POST", "GET"])
def get_df_data(ticker):
    try:
        data = request.get_json()
        if not data:
            return {"error": "No data provided"}, 400
        
        df = load_user_data(ticker, data.get("start_date"), data.get("end_date"), data.get("interval"))

        if data["features"]:
            out = calculate_features(data.get("features"), df)

        print(data["features"])
        out = out.round(3)
        print(out)
        out = out.fillna("NaN")
        out["date"] = out["date"].dt.strftime("%Y-%m-%d")

        return {"df": out.to_dict(orient="split")}

    except Exception as e:
        return {"error":str(e)}, 500



# Výchozí parametry modelu
model_params = {
    "model_type": "grad",
    "features": {},
    "learning_rate": 0.001,
    "epochs": 100,
    "batch_size": 32,
    "tt_split": 80
# TODO: pridat ORDER na ARIMA
}

models_dict = {
    "logit": logit,
    "arima": arima_model,
    "rnn": rnn,
    "gradient_lr": gradient
}
        
# Získat parametry modelu
@app.route("/api/<string:ticker>/train", methods=["POST"])
def post_model(ticker):
    try:
        data = request.get_json()
        if not data:
            return {"error": "No data provided"}, 400

        model_params_in = data.get("model_params", {})
        for param in model_params_in:
            if param in model_params:
               model_params[param] = model_params_in[param]

        stock_info = data.get("stock_info", {})

        df = load_user_data(ticker, stock_info.get("start_date"), stock_info.get("end_date"), stock_info.get("interval"))

        unique_features_df = calculate_features(model_params["features"], df)
        lag_df = lag_features(model_params["features"], unique_features_df)


        split_point = int(len(lag_df) * ((model_params["tt_split"] / 100)))
        train_df, test_df = lag_df.iloc[:split_point], lag_df.iloc[split_point:]

        model_function = models_dict.get(model_params["model_type"])
        model_function(train_df, test_df, model_params)

        return {"message": "Model parameters updated", "model_params": model_params}, 200
    except Exception as e:
        return {"error": str(e)}, 500



if __name__ == "__main__":
    app.run(debug = True, host = "localhost", port = 5055)
