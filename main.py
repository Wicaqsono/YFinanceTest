from fastapi import FastAPI, Depends
from timeseries import TimeSeries
from auth import validate_api_key
from candlestick_chart import create_candlestick_chart
from fastapi.responses import FileResponse

app = FastAPI()


@app.get("/test")
def test_api(apikey: str = Depends(validate_api_key)):
    return {"message": "API Key Valid", "apikey": apikey}

@app.get("/ohlcv")
def get_ohlcv(
    symbol: str = "TSLA",
    period: str = "5d",
    interval: str = "1d",
    apikey: str = Depends(validate_api_key)
):
    
    ts = TimeSeries(symbol, period, interval)
    return ts.get_json()

@app.get("/candlestick")
def get_ohlcv(
    symbol: str = "TSLA",
    period: str = "5d",
    interval: str = "1d",
    apikey: str = Depends(validate_api_key)
):
    
   filepath = create_candlestick_chart(symbol, period, interval)  # <-- return JPG path
   print("Candlestick chart saved at:", filepath)
   return FileResponse(filepath, media_type="image/jpeg", filename=filepath)

# @app.get("/candlestick/html", response_class=HTMLResponse)
# def get_candlestick_html(
#     symbol: str = "TSLA",
#     period: str = "5d",
#     interval: str = "1d",
#     apikey: str = Depends(validate_api_key)
# ):
#     fig = create_candlestick_figure(symbol, period, interval)  # fungsi yg return figure
#     html = fig.to_html(full_html=False)
#     return HTMLResponse(content=html)
