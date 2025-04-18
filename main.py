# main.py
import os
import re
import socks
import socket
import json
from fastapi import FastAPI, HTTPException, Query
from dotenv import load_dotenv
import requests
import uvicorn

# Load .env
load_dotenv()

app = FastAPI()

BINANCE_URL = "https://www.binance.com/bapi/apex/v1/public/apex/cms/article/list/query"
PROXY_URL = os.getenv("PROXY_URL")
if not PROXY_URL:
    raise RuntimeError("PROXY_URL not set in .env")

# Parse the SOCKS5 proxy URL
proxy_pattern = r"socks5://(.+):(.+)@(.+):(\d+)"
match = re.match(proxy_pattern, PROXY_URL)
if not match:
    raise RuntimeError("Invalid SOCKS5 proxy URL format")

PROXY_USERNAME = match.group(1)
PROXY_PASSWORD = match.group(2)
PROXY_HOST = match.group(3)
PROXY_PORT = int(match.group(4))

def setup_socks_proxy():
    """Configure the SOCKS5 proxy for the current request"""
    socks.set_default_proxy(
        socks.SOCKS5, 
        PROXY_HOST, 
        PROXY_PORT, 
        username=PROXY_USERNAME, 
        password=PROXY_PASSWORD
    )
    socket.socket = socks.socksocket

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/binancedata")
async def binance_data(
    type: int = Query(..., description="article type"),
    pageNo: int = Query(..., description="page number"),
    pageSize: int = Query(..., description="page size"),
):
    print(f"Debug: Received request with type={type}, pageNo={pageNo}, pageSize={pageSize}")
    
    # This is where we set up the parameters
    params = {"type": type, "pageNo": pageNo, "pageSize": pageSize}
    
    # Setup headers for the request
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "en-US,en;q=0.9",
        "Origin": "https://www.binance.com",
        "Referer": "https://www.binance.com/",
    }
    
    print(f"Debug: Setting up SOCKS5 proxy at {PROXY_HOST}:{PROXY_PORT}")
    
    try:
        # Reset the socket to its original state before setting up the proxy again
        if hasattr(socket, '_orig_socket'):
            socket.socket = socket._orig_socket
        else:
            # Store the original socket for later
            socket._orig_socket = socket.socket
        
        # Setup the SOCKS proxy
        setup_socks_proxy()
        
        print(f"Debug: Making request to {BINANCE_URL}")
        
        # Make the request using the requests library (synchronously)
        response = requests.get(
            BINANCE_URL,
            params=params,
            headers=headers,
            timeout=15
        )
        
        print(f"Debug: Received response with status code {response.status_code}")
        
        # Check the response status
        response.raise_for_status()
        
        # Try to parse the response as JSON
        try:
            data = response.json()
            print(f"Debug: Successfully parsed JSON response")
            return data
        except json.JSONDecodeError as e:
            print(f"Debug: Failed to parse JSON: {e}")
            print(f"Response content: {response.text[:200]}...")
            raise HTTPException(500, f"Failed to parse response as JSON: {str(e)}")
        
    except requests.exceptions.RequestException as e:
        print(f"Debug: Request error: {e}")
        raise HTTPException(500, f"Request error: {str(e)}")
    except Exception as e:
        print(f"Debug: Unexpected error: {e}")
        raise HTTPException(500, f"Unexpected error: {str(e)}")

@app.get("/serverinfo")
async def server_info():
    """
    Returns the server's public IP address along with its country and city.
    This will show the proxy's IP if the proxy is working correctly.
    """
    ip_api_url = "http://ip-api.com/json"  # free IP geolocation service
    
    try:
        # Reset the socket to its original state before setting up the proxy again
        if hasattr(socket, '_orig_socket'):
            socket.socket = socket._orig_socket
        else:
            # Store the original socket for later
            socket._orig_socket = socket.socket
        
        # Setup the SOCKS proxy
        setup_socks_proxy()
        
        # Make the request using the requests library
        response = requests.get(ip_api_url, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        return {
            "ip":      data.get("query"),
            "country": data.get("country"),
            "city":    data.get("city"),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"IP lookup failed: {str(e)}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)