from flask import Flask
from flask import request
from flask_cors import CORS
from dotenv import load_dotenv
import os
import datetime
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from io import BytesIO
import base64
matplotlib.use('Agg')

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

# Poslat obrazek jako base64
def df_to_base64(df):
    fig, ax = plt.subplots()
    ax.plot(df["date"], df["adjusted"])
    ax.set_xlabel('Date')
    ax.set_ylabel('Close')
    ax.set_title("Stock price")
    buf = BytesIO()
    fig.savefig(buf, format="png")
    buf.seek(0)
    plt.close(fig)
    return base64.b64encode(buf.read()).decode("utf-8")
@app.route("/api/stock/<string:stock>", methods=["GET"])
def get_stock_plot(stock):
    try:
        data = load_data(stock)
        print(stock)
        img_base64 = df_to_base64(data)
        return {"image": img_base64}, 200
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
# TODO: dodělat že if tam nejaky parametr neni tak pouzij default nebo tak nejak?
model_params = {
    "model_type": "grad",
    "features": {},
    "learning_rate": 0.001,
    "epochs": 100,
    "batch_size": 32
}

# Získat parametry modelu
@app.route("/api/<string:stock>/train", methods=["POST"])
def get_model(stock):
    try:
        data = request.get_json()
        if not data:
            return {"error": "No data provided"}, 400
        for param in data:
            if param in model_params:
               model_params[param] = data[param]

        lag_features(load_data(stock), model_params)

        return {"message": "Model parameters updated", "model_params": model_params}, 200
    except Exception as e:
        return {"error": str(e)}, 500

# Vytvořit lag features
def lag_features(df, model_params):
    for lag in model_params['features']:
        for feature in model_params['features'][lag]:
            df[f"{feature}_{lag}"] = df[feature].shift(int(lag))

    print(df.head())

    return df



if __name__ == "__main__":
    app.run(debug=True)