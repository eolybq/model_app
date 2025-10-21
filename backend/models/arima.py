from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.stattools import adfuller 
import pandas as pd
import matplotlib.pyplot as plt
import warnings

def arima_model(train_df, test_df, model_params, order=(30, 0, 0)):
    warnings.filterwarnings("ignore", category=RuntimeWarning)


    predictions = []

    train = train_df["log_return"]
    test = test_df["log_return"]

    adf = adfuller(train, regression='c')
    print(adf)

    model = ARIMA(train, order=order)
    model_fit = model.fit()
    print(model_fit.summary())

    for t in range(len(test)):
        fcast = model_fit.forecast(1)[0]
        predictions.append(fcast)

        model_fit = model_fit.append(pd.Series(test.iloc[t]), refit=False)

    mse = sum((test - predictions) ** 2) / len(test)
    rmse = mse ** 0.5
    mae = sum(abs(test - predictions)) / len(test)
    return {"predictions": predictions, "real": test.tolist(), "mse": mse, "rmse": rmse, "mae": mae}

# df = pd.read_csv("data/TSLA.csv")
# df = df.dropna()
# split_point = int(len(df) * ((80 / 100)))
# train_df, test_df = df.iloc[:split_point], df.iloc[split_point:]
# # print(arima_model(train_df, test_df))

# predictions = arima_model(train_df, test_df)["predictions"]
# plt.figure(figsize=(10, 5))
# plt.plot(test_df["log_return"].values, label='Skutečné hodnoty', color='blue')
# plt.plot(predictions, label='Predikce', color='red')
# plt.legend()
# plt.show()