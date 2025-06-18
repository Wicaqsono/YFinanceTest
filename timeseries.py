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
                "open": float(row["Open"].iloc[0]),
                "high": float(row["High"].iloc[0]),
                "low": float(row["Low"].iloc[0]),
                "close": float(row["Close"].iloc[0]),
                "volume": int(row["Volume"].iloc[0]),
            })

            output["values"].reverse()

        return output
    
class BBands:
    def __init__(self, symbol: str, period: str = "60d", interval: str = "1d",window: int = 20, std_multiplier: int = 2):
        self.symbol = symbol
        self.period = period
        self.interval = interval
        self.window = window
        self.std_multiplier = std_multiplier

    def get_json(self):

        # Ambil data
        data = yf.download(self.symbol, period=self.period, interval=self.interval, auto_adjust=True)
        
        # Hitung Bollinger Bands manual
        data['rolling_mean'] = data['Close'].rolling(window=self.window).mean()
        data['rolling_std'] = data['Close'].rolling(window=self.window).std()
        data['bb_upper'] = data['rolling_mean'] + (self.std_multiplier * data['rolling_std'])
        data['bb_lower'] = data['rolling_mean'] - (self.std_multiplier * data['rolling_std'])

        # Drop NA
        clean_data = data.dropna()
        if clean_data.empty:
            return {
            "status": "error",
            "message": f"Tidak ada data cukup untuk hitung Bollinger Bands ({self.window} window)."
        }
    
        # Ambil data terakhir yang valid
        latest = data.dropna().iloc[[-1]]  # <--- Pastikan tetap dataframe agar indexing aman

        # Ambil scalar dengan .iloc[0] atau .item()
        upper_band = latest['bb_upper'].iloc[0]
        middle_band = latest['rolling_mean'].iloc[0]
        lower_band = latest['bb_lower'].iloc[0]
        latest_date = latest.index[-1].strftime('%Y-%m-%d')
        print("download data:", data)
        output = {
            "meta": {
                "symbol": self.symbol,
                "interval": self.interval,
                "indicator": {
                "name": "BBANDS - Bollinger Bands®",
                "series_type": "close",
                "time_period": self.window,
                "sd": self.std_multiplier,
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
        return output
    
class MACD:
    def __init__(self, symbol: str, period: str = "90d", interval: str = "1d", fast_period: int = 12, slow_period: int = 26, signal_period: int = 9):
        self.symbol = symbol
        self.period = period
        self.interval = interval
        self.fast_period = fast_period
        self.slow_period = slow_period
        self.signal_period = signal_period

    def get_json(self):
        # Ambil data harga
        data = yf.download(self.symbol, period=self.period, interval=self.interval, auto_adjust=True)

        # Hitung EMA cepat dan lambat
        ema_fast = data['Close'].ewm(span=self.fast_period, adjust=False).mean()
        ema_slow = data['Close'].ewm(span=self.slow_period, adjust=False).mean()

        # Hitung MACD, Signal, dan Histogram
        data['macd'] = ema_fast - ema_slow
        data['macd_signal'] = data['macd'].ewm(span=self.signal_period, adjust=False).mean()
        data['macd_hist'] = data['macd'] - data['macd_signal']

        # Ambil data terakhir yang valid
        latest = data.dropna().iloc[[-1]]  # Tetap sebagai DataFrame untuk indexing aman

        macd = latest['macd'].iloc[0]
        macd_signal = latest['macd_signal'].iloc[0]
        macd_hist = latest['macd_hist'].iloc[0]
        latest_date = latest.index[-1].strftime('%Y-%m-%d')

        output = {
            "meta": {
                "symbol": self.symbol,
                "interval": self.interval,
                "indicator": {
                    "name": "MACD - Moving Average Convergence Divergence",
                    "series_type": "close",
                    "fast_period": self.fast_period,
                    "slow_period": self.slow_period,
                    "signal_period": self.signal_period
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
        return output
