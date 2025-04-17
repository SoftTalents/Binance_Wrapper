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
