from fastapi import Request, HTTPException

API_KEY = "7b6170b6bc4c09e3ff9376e5edc3c77cd3b2c2cc25c8dd52ff2d8013437f9a17"

async def validate_api_key(request: Request):
    apikey = request.query_params.get("apikey")
    print("🔥 API KEY MASUK:", apikey)

    if apikey != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")

    return apikey
