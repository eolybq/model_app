import pandas as pd
import numpy as np
# import tensorflow as tf 
from tensorflow import keras
from sklearn.preprocessing import StandardScaler
import joblib
import matplotlib.pyplot as plt

# physical_devices = tf.config.list_physical_devices('GPU')
# tf.config.experimental.set_memory_growth(physical_devices[0], True)

# tf.config.set_logical_device_configuration(
#     physical_devices[0],
#     [tf.config.experimental.VirtualDeviceConfiguration(memory_limit=3072)])


# Funkce pro vytvoření sekvencí z dat
def seq_maker(data, sequence, predicted_y):
    x, y = [], []
    for i in range(len(data) - sequence):
        x.append(data[i:i + sequence])
        y.append(predicted_y.iloc[i + sequence])
    print(len(x), len(y))
    return np.array(x), np.array(y)


# trénink na všech historických datech
def train_model(train_data, model_params):
    df = train_data.copy()
    predicted_y = df.pop('log_return')

    scaler = StandardScaler()
    train_scaled = scaler.fit_transform(df)

    # joblib.dump(scaler, './rnn/scaler_big_model.pkl')

    X_train, y_train = seq_maker(train_scaled, model_params["seq_len"], predicted_y)


    # Define the RNN model
    model = keras.models.Sequential()
    model.add(keras.layers.LSTM(model_params["neurons"], activation=model_params["activation_func"], input_shape=(X_train.shape[1], X_train.shape[2]), return_sequences=True))
    model.add(keras.layers.Dropout(0.2))
    model.add(keras.layers.LSTM(model_params["neurons"], activation=model_params["activation_func"]))
    model.add(keras.layers.Dropout(0.2))
    model.add(keras.layers.Dense(1))


    # Compile the model
    model.compile(optimizer = 'adam', loss = 'mean_squared_error', metrics = ["mean_absolute_error"])

    # Summary of the model
    model.summary()

    checkpoint = keras.callbacks.ModelCheckpoint(filepath='./rnn/big_model_checkpoint.keras', save_best_only=True, monitor='val_loss', mode='min')
    
    early_stopping = keras.callbacks.EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True)

    history = model.fit(X_train, y_train, shuffle = False, batch_size=model_params["batch_size"], epochs=model_params["epochs"], validation_split=0.2, callbacks=[checkpoint, early_stopping])

    # joblib.dump(history.history, './rnn/train_history.pkl')

    model.save('./rnn/big_model.keras')


    return model, scaler, history.history


# Predikce pomocí nových dat
def predict(test_data, model_params, model, scaler):
    # scaler = joblib.load('./rnn/scaler_big_model.pkl')
    df = test_data.copy()
    predicted_y = df.pop('log_return')



    model = keras.models.load_model('./rnn/big_model.keras')

    test_scaled = scaler.transform(df)


    X_test, y_test = seq_maker(test_scaled, model_params["seq_len"], predicted_y)

    number_features = X_test.shape[2]

    X_rs = np.array(X_test).reshape(-1, model_params["seq_len"], number_features)


    predictions = model.predict(X_rs)
    predictions = predictions.flatten()
    predictions = pd.Series(predictions, index = predicted_y.index[-len(predictions):])
    print(predictions)

    return predictions


def rnn_model(lag_df, model_params):
    # tt split
    split_point = int(len(lag_df) * ((model_params["tt_split"] / 100)))

    train_df, test_df = lag_df.iloc[:split_point], lag_df.iloc[split_point:]
    

    # wasted_test_rows = len(test_df) % 64

    # test_df = test_df[:-wasted_test_rows]

    model, scaler, history = train_model(train_df, model_params) 

    predictions = predict(test_df, model_params, model, scaler)



    fig, ax = plt.subplots(2, 1, figsize=(12, 8))
    ax[0].plot(test_df["log_return"], label='Real Close Prices')
    ax[0].plot(predictions, label='Predicted Close Prices')
    ax[0].legend()

    ax[1].plot(history['loss'], label='Training loss')
    ax[1].plot(history['val_loss'], label='Validation loss')
    ax[1].legend()
    plt.show()


lag_df = pd.read_csv("data/TSLA.csv")
lag_df.drop('date', axis=1, inplace=True)

model_params = {
    "model_type": "grad",
    "features": {},
    "learning_rate": 0.001,
    "epochs": 1,
    "batch_size": 32,
    "tt_split": 80,
    "neurons": 32,
    "seq_len": 64,
    "activation_func": "tanh"
}

rnn_model(lag_df, model_params)