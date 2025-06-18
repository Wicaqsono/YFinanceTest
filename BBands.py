import yfinance as yf
import pandas as pd
import numpy as np
import json
from datetime import datetime

symbol = "ANTAM.JK"
interval = "1d"
currency = "USD"
exchange = "NASDAQ"
exchange_timezone = "America/New_York"
mic_code = "XNGS"
type_ = "Common Stock"

window = 20
std_multiplier = 2

# Ambil data
data = yf.download(symbol, period="60d", interval=interval, auto_adjust=True)

# Hitung Bollinger Bands manual
data['rolling_mean'] = data['Close'].rolling(window=window).mean()
data['rolling_std'] = data['Close'].rolling(window=window).std()
data['bb_upper'] = data['rolling_mean'] + (std_multiplier * data['rolling_std'])
data['bb_lower'] = data['rolling_mean'] - (std_multiplier * data['rolling_std'])

# Ambil data terakhir yang valid
latest = data.dropna().iloc[[-1]]  # <--- Pastikan tetap dataframe agar indexing aman

# Ambil scalar dengan .iloc[0] atau .item()
upper_band = latest['bb_upper'].iloc[0]
middle_band = latest['rolling_mean'].iloc[0]
lower_band = latest['bb_lower'].iloc[0]
latest_date = latest.index[-1].strftime('%Y-%m-%d')

# Format JSON sesuai kebutuhan
output = [
    {
        "meta": {
            "symbol": symbol,
            "interval": "1day",
            "currency": currency,
            "exchange_timezone": exchange_timezone,
            "exchange": exchange,
            "mic_code": mic_code,
            "type": type_,
            "indicator": {
                "name": "BBANDS - Bollinger Bands®",
                "series_type": "close",
                "time_period": window,
                "sd": std_multiplier,
                "ma_type": "SMA"
            }
        },
        "values": [
            {
                "datetime": latest_date,
                "upper_band": f"{upper_band:,.5f}",
                "middle_band": f"{middle_band:,.5f}",
                "lower_band": f"{lower_band:,.5f}",
            }
        ],
        "status": "ok"
    }
]

# Print JSON
print(json.dumps(output, indent=2))
