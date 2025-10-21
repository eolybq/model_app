import pandas as pd
import pandas_ta as ta

def ema_model(df, span, min_periods):
    close_series = df["close"]
    ema = close_series.ewm(span=span, adjust=False, min_periods=min_periods).mean()
    return ema


#rsi
def rsi_model(df):
    close_floats = df["close"].astype(float)
    rsi = ta.rsi(close_floats)
    return rsi

def atr_model(df, n=14):
    high = df["high"].astype(float)
    low = df["low"].astype(float)
    close = df["close"].astype(float)
    
    tr0 = high - close
    tr1 = high - (close.shift()).abs()
    tr2 = (low - close.shift()).abs()

    tr = pd.concat([tr0, tr1, tr2], axis=1).max(axis=1)

    atr = tr.rolling(window=n).mean()
    return atr


def calculate_features(features, df):
    all_f_df = df.copy()
    all_features = set()
    for lag in features.values():
        for feature in lag:
            all_features.add(feature)

    feature_funcs = {
        "rsi": rsi_model,
        "atr": atr_model,
        "ema": ema_model
    }
    for feature in all_features:
        if feature.startswith("ema"):
            span = int(feature.replace("ema", ""))
            all_f_df[feature] = feature_funcs["ema"](all_f_df, span, span)
        elif feature in feature_funcs:
            all_f_df[feature] = feature_funcs[feature](all_f_df)
    
    return all_f_df

# Vytvořit lag features
def lag_features(features, df):
    lag_df = pd.DataFrame({"log_return": df["log_return"]})
    for lag in features:
        lag_num = int(lag.replace("lag_", ""))
        for feature in features[lag]:
            lag_df[f"{feature}_{lag}"] = df[feature].shift(lag_num)
    return lag_df


# model_params = {
#     "model_type": "grad",
#     "features": {
#         "1": ["rsi"],
#         "2": ["ema10", "rsi"],
#         "3": ["rsi", "ema50", "atr"]
#     },
#     "learning_rate": 0.001,
#     "epochs": 100,
#     "batch_size": 32
# }

# df = pd.read_csv("data/TSLA.csv")

# print(lag_features(model_params["features"], calculate_features(model_params["features"], df)))