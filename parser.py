import pandas as pd

def parse_log(file_path):
    data = []

    with open(file_path, "r") as f:
        for line in f:
            parts = line.strip().split()

            # простий приклад: час + рівень + код
            if len(parts) >= 3:
                data.append({
                    "time": parts[0],
                    "level": parts[1],
                    "value": int(parts[2])
                })

    return pd.DataFrame(data)