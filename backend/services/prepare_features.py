# Vytvořit lag features
def lag_features(df, features):
    lag_df = pd.DataFrame()
    for lag in features:
        for feature in features[lag]:
            lag_df[f"{feature}_{lag}"] = df[feature].shift(int(lag))

    return lag_df
