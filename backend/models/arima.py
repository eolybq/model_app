from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.stattools import adfuller 
import pandas as pd
import warnings

def arima_model(train_df, test_df, model_params, order=(30, 0, 0)):
    # warnings.filterwarnings("ignore", category=RuntimeWarning)

    predictions = []

    train = train_df["log_return"]
    test = test_df["log_return"]

    adf = adfuller(train, regression='c')

    model = ARIMA(train, order=order)
    model_fit = model.fit()
    # print(model_fit.summary())

    for i in range(len(test)):
        fcast = model_fit.forecast(1)
        predictions.append(fcast.iloc[0])

        model_fit = model_fit.append(test.iloc[[i]], refit=False)

    mse = sum((test - predictions) ** 2) / len(test)
    rmse = mse ** 0.5
    mae = sum(abs(test - predictions)) / len(test)

    return {"adf": adf, "predictions": predictions, "real": test.tolist(), "mse": mse, "rmse": rmse, "mae": mae}




# import matplotlib.pyplot as plt
# model_params = {
#     "model_type": "grad",
#     "features": {},
#     "learning_rate": 0.001,
#     "epochs": 100,
#     "batch_size": 32,
#     "tt_split": 80
# }

# df = pd.read_csv("data/TSLA.csv")
# # NOTE: musi se opravit index aby zacinal od 0 kvuli odhozenemu prvnimu radku NA
# df = df.dropna().reset_index(drop=True)
# split_point = int(len(df) * ((80 / 100)))
# train_df, test_df = df.iloc[:split_point], df.iloc[split_point:]
# print(arima_model(train_df, test_df, model_params))

# # predictions = arima_model(train_df, test_df)["predictions"]
# # plt.figure(figsize=(10, 5))
# # plt.plot(test_df["log_return"].values, label='Skutečné hodnoty', color='blue')
# # plt.plot(predictions, label='Predikce', color='red')
# # plt.legend()
# # plt.show()
