from sklearn.ensemble import IsolationForest

def detect_anomalies(df, contamination=0.1):
    model = IsolationForest(contamination=contamination, random_state=42)

    # беремо тільки числові дані
    X = df[["value"]]

    df["anomaly"] = model.fit_predict(X)

    # -1 = аномалія, 1 = норм
    df["anomaly"] = df["anomaly"].map({1: 0, -1: 1})

    return df