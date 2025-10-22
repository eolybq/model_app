import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def gradient_lr_model(lag_df, model_params):
    df = lag_df.copy()

    y = np.array(df.pop("log_return"))
    X = np.array(df)

    # tt split
    split_point = int(len(lag_df) * ((model_params["tt_split"] / 100)))

    X_train, X_test = X[:split_point], X[split_point:]
    y_train, y_test = y[:split_point], y[split_point:]

    print(X_train)
    print(X_test)

    num_features = X_train.shape[1]

    for i in range(num_features):
        mean = X_train[:, i].mean()
        std = X_train[:, i].std()

        X_train[:, i] = (X_train[:, i] - mean) / std


        X_test[:, i] = (X_test[:, i] - mean) / std


    weight = np.zeros(X_train.shape[1])
    bias = 0

    rate = model_params["learning_rate"]
    epochs = model_params["epochs"]
    print(epochs)
    mse_history = []

    for epoch in range(epochs):
        y_pred = np.dot(X_train, weight) + bias

        error = y_pred - y_train

        weight_grad = (2 / X_train.shape[0]) * X_train.T.dot(error)
        bias_grad = (2 / X_train.shape[0]) * np.sum(error)

        weight -= rate * weight_grad
        bias -= rate * bias_grad

        mse = (1 / X_train.shape[0]) * np.sum(np.square(y_pred - y_train))
        mse_history.append(mse)

        if epoch % 100 == 0:
            print(f"Epoch {epoch}, MSE: {mse:.6f}", weight)


    # predikce modelu na test datech
    y_pred_test = np.dot(X_test, weight) + bias
    test_mse = sum((y_test - y_pred_test) ** 2) / len(y_test)
    test_rmse = test_mse ** 0.5
    test_mae = sum(abs(y_test - y_pred_test)) / len(y_test)

    return {"y_pred": y_pred_test, "train_mse": mse_history, "test_mse": test_mse, "test_rmse": test_rmse, "test_mae": test_mae}