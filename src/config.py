import os
from dotenv import load_dotenv

load_dotenv()

DEFAULT_TICKERS = ["AAPL", "MSFT", "AMZN", "GOOGL", "META"]
DEFAULT_PERIOD = "10y"
DEFAULT_INTERVAL = "1d"


ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(ROOT_DIR, "data")
RAW_DATA_DIR = os.path.join(DATA_DIR, "raw")
NORMALIZED_DATA_DIR = os.path.join(DATA_DIR, "normalized")
PROCESSED_DATA_DIR = os.path.join(DATA_DIR, "processed")
MODELS_DIR = os.path.join(ROOT_DIR, "models")


for directory in [RAW_DATA_DIR, NORMALIZED_DATA_DIR, PROCESSED_DATA_DIR, MODELS_DIR]:
    os.makedirs(directory, exist_ok=True)


WINDOW_SIZES = [5, 10, 20, 50, 200] # for ma
BOLLINGER_WINDOW = 20
BOLLINGER_STD = 2
RSI_WINDOW = 14
MACD_FAST = 12
MACD_SLOW = 26
MACD_SIGNAL = 9


def get_config():
    return {
        "tickers": DEFAULT_TICKERS,
        "period": DEFAULT_PERIOD,
        "interval": DEFAULT_INTERVAL,
        "paths": {
            "root": ROOT_DIR,
            "data": DATA_DIR,
            "raw": RAW_DATA_DIR,
            "normalized": NORMALIZED_DATA_DIR,
            "processed": PROCESSED_DATA_DIR,
            "models": MODELS_DIR
        },
        "features": {
            "window_sizes": WINDOW_SIZES,
            "bollinger": {
                "window": BOLLINGER_WINDOW,
                "std": BOLLINGER_STD
            },
            "rsi": {
                "window": RSI_WINDOW
            },
            "macd": {
                "fast": MACD_FAST,
                "slow": MACD_SLOW,
                "signal": MACD_SIGNAL
            }
        }
    }
