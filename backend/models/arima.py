from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.stattools import adfuller 
import pandas as pd
import warnings

# TODO: mozna AIC BIC vypsat pro data a pak at se rozhodne pro order na zaklade toho?

def arima_model(lag_df, model_params, order=(10, 0, 0)):
    # warnings.filterwarnings("ignore", category=RuntimeWarning)
    y = lag_df["log_return"]

    split_point = int(len(lag_df) * ((model_params["tt_split"] / 100)))
    y_train, y_test = y.iloc[:split_point], y.iloc[split_point:]

    predictions = []


    adf = adfuller(y_train, regression='c')

    model = ARIMA(y_train, order=order)
    model_fit = model.fit()
    # print(model_fit.summary())

    for i in range(len(y_test)):  
        fcast = model_fit.forecast(1)
        predictions.append(fcast.iloc[0])

        model_fit = model_fit.append(y_test.iloc[[i]], refit=False)

    mse = sum((y_test - predictions) ** 2) / len(y_test)
    rmse = mse ** 0.5
    mae = sum(abs(y_test - predictions)) / len(y_test)

    return {"adf": adf, "predictions": predictions, "real": y_test.tolist(), "mse": mse, "rmse": rmse, "mae": mae}