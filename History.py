import yfinance as yf
import json

# Ambil data saham TSLA (5 hari terakhir, interval harian)
symbol = 'TSLA'
data = yf.download(symbol, period='5d', interval='1d', auto_adjust=False)

# Susun data menjadi format JSON seperti contoh Anda
output = {
    "meta": {
        "symbol": symbol,
        "interval": "1day",
        "currency": "USD",
        "exchange_timezone": "America/New_York",
        "exchange": "NASDAQ",
        "mic_code": "XNGS",
        "type": "Common Stock"
    },
    "values": [],
    "status": "ok"
}

# Konversi baris per baris menjadi dict
for index, row in data.iterrows():
    output["values"].append({
        "datetime": index.strftime("%Y-%m-%d"),
        "open": float(row['Open']),
        "high": float(row['High']),
        "low": float(row['Low']),
        "close": float(row['Close']),
        "volume": int(row['Volume'])
    })

# Cetak hasil JSON ke terminal
print(json.dumps(output, indent=2))

# Simpan hasil ke file JSON
with open(f"{symbol}_data.json", "w") as f:
    json.dump(output, f, indent=2)
