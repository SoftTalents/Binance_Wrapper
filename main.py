# main.py
import os
from fastapi import FastAPI, HTTPException, Query
from dotenv import load_dotenv
import httpx

# load .env
load_dotenv()

app = FastAPI()

BINANCE_URL = "https://www.binance.com/bapi/apex/v1/public/apex/cms/article/list/query"
PROXY_URL  = os.getenv("PROXY_URL")
if not PROXY_URL:
    raise RuntimeError("PROXY_URL not set in .env")

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/binancedata")
async def binance_data(
    type: int   = Query(..., description="article type"),
    pageNo: int = Query(..., description="page number"),
    pageSize: int = Query(..., description="page size"),
):
    params = {"type": type, "pageNo": pageNo, "pageSize": pageSize}

    async with httpx.AsyncClient(timeout=15.0) as client:
        try:
            resp = await client.get(
                BINANCE_URL,
                params=params,
                proxies=PROXY_URL,   
            )
            resp.raise_for_status()
        except httpx.RequestError as e:
            raise HTTPException(500, f"Proxy request error: {e!r}")
        except httpx.HTTPStatusError as e:
            raise HTTPException(e.response.status_code, "Binance fetch error")

    return resp.json()

@app.get("/serverinfo")
async def server_info():
    """
    Returns the server’s public IP address along with its country and city.
    """
    ip_api_url = "http://ip-api.com/json"  # free IP geolocation service
    async with httpx.AsyncClient() as client:
        resp = await client.get(ip_api_url)
    if resp.status_code != 200:
        raise HTTPException(status_code=resp.status_code, detail="IP lookup failed")
    data = resp.json()
    return {
        "ip":      data.get("query"),
        "country": data.get("country"),
        "city":    data.get("city"),
    }
