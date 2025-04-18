# debug_binance.py
import os
import re
import socks
import socket
import requests
import json
import sys
from dotenv import load_dotenv

# Load .env
load_dotenv()

print(f"Python version: {sys.version}")
print(f"Using requests version: {requests.__version__}")

def setup_proxy():
    # Get proxy URL from .env
    PROXY_URL = os.getenv("PROXY_URL")
    if not PROXY_URL:
        print("Error: PROXY_URL not set in .env")
        return False
    
    print(f"Using proxy: {PROXY_URL}")
    
    # Parse the SOCKS5 proxy URL
    proxy_pattern = r"socks5://(.+):(.+)@(.+):(\d+)"
    match = re.match(proxy_pattern, PROXY_URL)
    if not match:
        print("Error: Invalid SOCKS5 proxy URL format")
        return False
    
    # Extract proxy details
    username = match.group(1)
    password = match.group(2)
    host = match.group(3)
    port = int(match.group(4))
    
    print(f"Proxy details: {host}:{port} with username: {username}")
    
    try:
        # Configure SOCKS proxy
        socks.set_default_proxy(
            socks.SOCKS5, 
            host, 
            port, 
            username=username, 
            password=password
        )
        socket.socket = socks.socksocket
        return True
    except Exception as e:
        print(f"Error setting up proxy: {str(e)}")
        return False

def test_binance_api():
    print("\n=== TESTING BINANCE API CONNECTION ===")
    
    if not setup_proxy():
        print("Failed to set up proxy, exiting.")
        return
    
    binance_url = "https://www.binance.com/bapi/apex/v1/public/apex/cms/article/list/query"
    
    # Test parameters
    test_params = [
        {"type": 1, "pageNo": 1, "pageSize": 1},
        {"type": 1, "pageNo": 1, "pageSize": 50}
    ]
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "en-US,en;q=0.9",
        "Origin": "https://www.binance.com",
        "Referer": "https://www.binance.com/",
    }
    
    # Check our IP first (through the proxy)
    try:
        print("\nChecking current IP (through proxy)...")
        ip_response = requests.get("http://ip-api.com/json", timeout=10)
        ip_data = ip_response.json()
        print(f"Current IP (should be proxy): {ip_data.get('query')}")
        print(f"Location: {ip_data.get('city')}, {ip_data.get('country')}")
    except Exception as e:
        print(f"Error checking IP: {str(e)}")
    
    # Test each parameter set
    for i, params in enumerate(test_params):
        print(f"\nTest {i+1}: Using params: {params}")
        
        try:
            print("Making request to Binance API...")
            response = requests.get(
                binance_url,
                params=params,
                headers=headers,
                timeout=15
            )
            
            print(f"Response status code: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print(f"Success! Response contains data")
                print(f"Data keys: {list(data.keys())}")
                
                if 'data' in data and 'catalogs' in data.get('data', {}):
                    catalogs = data['data']['catalogs']
                    print(f"Number of catalog items: {len(catalogs)}")
                    
                if 'success' in data:
                    print(f"Success status: {data['success']}")
                
                # Save first 100 chars of the response for inspection
                with open(f"binance_response_{i+1}.json", "w") as f:
                    json.dump(data, f, indent=2)
                print(f"Full response saved to binance_response_{i+1}.json")
            else:
                print(f"Error: Received status code {response.status_code}")
                print(f"Response text: {response.text[:200]}...")
                
        except Exception as e:
            print(f"Request error: {str(e)}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    test_binance_api()
