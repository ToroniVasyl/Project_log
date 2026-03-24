import logging
import json

def setup_logger():
    with open("config.json", "r") as f:
        config = json.load(f)

    logging.basicConfig(
        filename=config["log_file"],
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )

    return logging.getLogger()