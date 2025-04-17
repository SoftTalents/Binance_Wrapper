# main.py
from fastapi import FastAPI, HTTPException, Query
import httpx

app = FastAPI()

BINANCE_URL = "https://www.binance.com/bapi/apex/v1/public/apex/cms/article/list/query"

@app.get("/binancedata")
async def binance_data(
    type: int       = Query(..., description="article type"),
    pageNo: int     = Query(..., description="page number"),
    pageSize: int   = Query(..., description="page size"),
):
    params = {"type": type, "pageNo": pageNo, "pageSize": pageSize}
    async with httpx.AsyncClient() as client:
        resp = await client.get(BINANCE_URL, params=params)
    if resp.status_code != 200:
        raise HTTPException(status_code=resp.status_code, detail="Binance fetch error")
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
