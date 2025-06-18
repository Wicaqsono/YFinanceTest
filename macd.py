import yfinance as yf
import pandas as pd
import numpy as np
import json

symbol = "TSLA"
interval = "1d"
currency = "USD"
exchange = "NASDAQ"
exchange_timezone = "America/New_York"
mic_code = "XNGS"
type_ = "Common Stock"

# Parameter MACD
fast_period = 12
slow_period = 26
signal_period = 9

# Ambil data harga
data = yf.download(symbol, period="90d", interval=interval, auto_adjust=True)

# Hitung EMA cepat dan lambat
ema_fast = data['Close'].ewm(span=fast_period, adjust=False).mean()
ema_slow = data['Close'].ewm(span=slow_period, adjust=False).mean()

# Hitung MACD, Signal, dan Histogram
data['macd'] = ema_fast - ema_slow
data['macd_signal'] = data['macd'].ewm(span=signal_period, adjust=False).mean()
data['macd_hist'] = data['macd'] - data['macd_signal']

# Ambil data terakhir yang valid
latest = data.dropna().iloc[[-1]]  # Tetap sebagai DataFrame untuk indexing

macd = latest['macd'].iloc[0]
macd_signal = latest['macd_signal'].iloc[0]
macd_hist = latest['macd_hist'].iloc[0]
latest_date = latest.index[-1].strftime('%Y-%m-%d')

# Format JSON sesuai contoh
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
                "name": "MACD - Moving Average Convergence Divergence",
                "series_type": "close",
                "fast_period": fast_period,
                "slow_period": slow_period,
                "signal_period": signal_period
            }
        },
        "values": [
            {
                "datetime": latest_date,
                "macd": f"{macd:,.5f}",
                "macd_signal": f"{macd_signal:,.5f}",
                "macd_hist": f"{macd_hist:,.5f}"
            }
        ],
        "status": "ok"
    }
]

# Cetak hasil JSON
print(json.dumps(output, indent=2))
