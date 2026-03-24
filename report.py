def save_report(df, path="output/report.txt"):
    total = len(df)
    anomalies = df["anomaly"].sum()

    with open(path, "w") as f:
        f.write(f"Total logs: {total}\n")
        f.write(f"Anomalies detected: {anomalies}\n")