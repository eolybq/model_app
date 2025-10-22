from sklearn.metrics import accuracy_score
import numpy as np
import matplotlib as plt
import pandas as pd


def sigmoid(z):
    return 1 / (1 + np.exp(-z))


# TODO: dat threshold pro hodnoceni uspech / neuspech an test datech jako input do models_param 

def logit_model(lag_df, model_params):
    df = lag_df.copy()

    y = np.array(df.pop("log_return"))
    y = (y > 0.009).astype(int)
    X = np.array(df)

    # tt split
    split_point = int(len(lag_df) * ((model_params["tt_split"] / 100)))

    X_train, X_test = X[:split_point], X[split_point:]
    y_train, y_test = y[:split_point], y[split_point:]


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
    loss_history = []

    for epoch in range(epochs):
        z = np.dot(X_train, weight) + bias
        y_pred = sigmoid(z)
        # Binary cross-entropy loss
        loss = -np.mean(y_train * np.log(y_pred + 1e-8) + (1 - y_train) * np.log(1 - y_pred + 1e-8))
        loss_history.append(loss)

        # Gradient
        error = y_pred - y_train
        weight_grad = np.dot(X_train.T, error) / X_train.shape[0]
        bias_grad = np.sum(error) / X_train.shape[0]

        weight -= rate * weight_grad
        bias -= rate * bias_grad

        if epoch % 100 == 0:
            print(f"Epoch {epoch}, Loss: {loss:.6f}")

    # Predikce na test datech
    y_pred_test = sigmoid(np.dot(X_test, weight) + bias)
    y_pred_class = (y_pred_test > model_params["y_threshold"]).astype(int)

    print(f"Trefeno 1: {np.sum((y_pred_class == y_test) & (y_pred_class == 1))} Trefeno 0: {np.sum((y_pred_class == y_test) & (y_pred_class == 0))}, Celkem: {len(y_pred_class)}")

    print("Test accuracy:", accuracy_score(y_test, y_pred_class))