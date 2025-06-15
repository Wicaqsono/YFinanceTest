# timeseries.py
import yfinance as yf

class TimeSeries:
    def __init__(self, symbol: str, period: str = "60d", interval: str = "1d"):
        self.symbol = symbol
        self.period = period
        self.interval = interval

    def get_json(self):
        data = yf.download(self.symbol, period=self.period, interval=self.interval, auto_adjust=False)
        print("download data:", data)
        output = {
            "meta": {
                "symbol": self.symbol,
                "interval": self.interval
            },
            "values": [],
            "status": "ok"
        }

        for index, row in data.iterrows():
            output["values"].append({
                "datetime": index.strftime("%Y-%m-%d %H:%M:%S"),
                "open": float(row["Open"]),
                "high": float(row["High"]),
                "low": float(row["Low"]),
                "close": float(row["Close"]),
                "volume": int(row["Volume"])
            })

            output["values"].reverse()

        return output
