import json
import plotly.graph_objects as go
from datetime import datetime
from timeseries import TimeSeries
import plotly.io as pio

def format_datetime_string(date_str, interval):
    # Parsing string menjadi datetime object, fleksibel terhadap format
    try:
        dt = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        dt = datetime.strptime(date_str, "%Y-%m-%d")

    # Format sesuai dengan interval
    if interval.endswith("d"):
        return dt.strftime("%Y-%m-%d")
    elif interval.endswith("h"):
        return dt.strftime("%Y-%m-%d %H:00")
    elif interval.endswith("m"):
        return dt.strftime("%Y-%m-%d %H:%M")
    else:
        return dt.isoformat()

def parse_datetime(date_str):
    try:
        return datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        return datetime.strptime(date_str, "%Y-%m-%d")

def create_candlestick_chart(symbol: str, period: str = "60d", interval: str = "1d"):
    ts = TimeSeries(symbol, period, interval)
    data = ts.get_json()
    print("Data retrieved:", data)

    if data["status"] != "ok":
        raise ValueError("Failed to retrieve data")

    values = data["values"]
    if not values:
        raise ValueError("No data available for the given symbol and period")

    # Parsing datetime sesuai format
    dates = [parse_datetime(item["datetime"]) for item in values]
    opens = [item["open"] for item in values]
    highs = [item["high"] for item in values]
    lows = [item["low"] for item in values]
    closes = [item["close"] for item in values]

    fig = go.Figure(data=[go.Candlestick(
        x=dates,
        open=opens,
        high=highs,
        low=lows,
        close=closes
    )])

    # Tentukan format label x-axis
    if interval.endswith("d"):
        tickformat = "%Y-%m-%d"
    elif interval.endswith("h"):
        tickformat = "%Y-%m-%d\n%H:00"
    elif interval.endswith("m"):
        tickformat = "%Y-%m-%d\n%H:%M"
    else:
        tickformat = "%Y-%m-%d"

    fig.update_layout(
        title=f"{symbol} Candlestick Chart",
        xaxis_title="Date",
        yaxis_title="Price (IDR)",
        xaxis_rangeslider_visible=False,
        xaxis=dict(
            tickformat=tickformat,
            tickangle=-45
        )
    )

    print("Figure created successfully")

    # Simpan sebagai JPG
    filename = f"{symbol}_candlestick.jpg"
    pio.write_image(fig, filename, format="jpg", width=800, height=600)
    print(f"Chart saved as {filename}")

    return filename
