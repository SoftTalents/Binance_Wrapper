# debug.py
import os
import re
import socks
import socket
import requests
import sys
from dotenv import load_dotenv

print(f"Python version: {sys.version}")
print(f"Using requests version: {requests.__version__}")

# Load .env
load_dotenv()

def test_proxy_connection():
    print("\n======= PROXY TEST DIAGNOSTIC TOOL =======")
    print("This script will test your SOCKS5 proxy configuration")
    print("============================================\n")

    # Get proxy URL from .env
    PROXY_URL = os.getenv("PROXY_URL")
    if not PROXY_URL:
        print("❌ Error: PROXY_URL not set in .env")
        return
    
    print(f"📋 Testing proxy: {PROXY_URL}")
    
    # Parse the SOCKS5 proxy URL
    proxy_pattern = r"socks5://(.+):(.+)@(.+):(\d+)"
    match = re.match(proxy_pattern, PROXY_URL)
    if not match:
        print("❌ Error: Invalid SOCKS5 proxy URL format")
        print("   Expected format: socks5://username:password@host:port")
        return
    
    # Extract proxy details
    username = match.group(1)
    password = match.group(2)
    host = match.group(3)
    port = int(match.group(4))
    
    print(f"📋 Proxy details:")
    print(f"   Host: {host}")
    print(f"   Port: {port}")
    print(f"   Username: {username}")
    print(f"   Password: {'*' * len(password)}")
    
    # Test direct connection first
    print("\n🔍 Testing direct connection (no proxy)...")
    try:
        direct_response = requests.get('http://ip-api.com/json', timeout=5)
        direct_data = direct_response.json()
        print(f"✅ Direct connection successful")
        print(f"   Your IP without proxy: {direct_data.get('query')}")
        print(f"   Location: {direct_data.get('city')}, {direct_data.get('country')}")
    except Exception as e:
        print(f"❌ Direct connection failed: {str(e)}")
    
    # Method 1: Test with requests session proxies
    print("\n🔍 METHOD 1: Testing with requests session proxies...")
    try:
        # Configure a SOCKS5 proxy with requests
        session = requests.Session()
        session.proxies = {
            'http': PROXY_URL,
            'https': PROXY_URL
        }
        
        print("   Making request via proxy...")
        response = session.get('http://ip-api.com/json', timeout=10)
        print(f"✅ Response status: {response.status_code}")
        
        data = response.json()
        print(f"✅ Proxy IP: {data.get('query')}")
        print(f"   Location: {data.get('city')}, {data.get('country')}")
        
        # Verify proxy is working by comparing IPs
        if data.get('query') != direct_data.get('query'):
            print("✅ PROXY VERIFIED: Your IP address changed with the proxy")
        else:
            print("⚠️ WARNING: Proxy might not be working correctly - IP didn't change")
            
    except requests.exceptions.ProxyError as e:
        print(f"❌ Proxy Error: {str(e)}")
        print("   This usually means the proxy configuration is incorrect or the proxy is down")
    except requests.exceptions.ConnectionError as e:
        print(f"❌ Connection Error: {str(e)}")
        print("   This could mean the proxy host is unreachable")
    except requests.exceptions.Timeout as e:
        print(f"❌ Timeout Error: {str(e)}")
        print("   The proxy connection timed out")
    except Exception as e:
        print(f"❌ Method 1 Error: {str(e)}")
    
    print("\n🔍 METHOD 2: Testing with socket monkey patching...")
    try:
        # Reset socket to default before monkey patching
        socket.socket = socket._socketobject if hasattr(socket, '_socketobject') else socket._realsocket
        
        # Configure and apply SOCKS proxy
        print(f"   Configuring SOCKS5 proxy at {host}:{port}")
        socks.set_default_proxy(
            socks.SOCKS5, 
            host, 
            port, 
            username=username, 
            password=password
        )
        socket.socket = socks.socksocket
        
        # Test connection
        print("   Making request via monkey-patched socket...")
        response = requests.get('http://ip-api.com/json', timeout=10)
        print(f"✅ Response status: {response.status_code}")
        
        data = response.json()
        print(f"✅ Proxy IP: {data.get('query')}")
        print(f"   Location: {data.get('city')}, {data.get('country')}")
        
        # Test Binance connection
        print("\n🔍 Testing Binance connection through proxy...")
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "en-US,en;q=0.9",
            "Origin": "https://www.binance.com",
            "Referer": "https://www.binance.com/",
        }
        binance_url = "https://www.binance.com/bapi/apex/v1/public/apex/cms/article/list/query"
        params = {"type": 1, "pageNo": 1, "pageSize": 1}
        
        binance_response = requests.get(binance_url, params=params, headers=headers, timeout=15)
        print(f"✅ Binance response status: {binance_response.status_code}")
        
        if binance_response.status_code == 200:
            print("✅ Successfully connected to Binance API!")
            print(f"   Response contains {len(binance_response.json())} keys")
        else:
            print(f"⚠️ Binance returned status code: {binance_response.status_code}")
            print(f"   Response: {binance_response.text[:100]}...")
            
    except socks.ProxyConnectionError as e:
        print(f"❌ Proxy Connection Error: {str(e)}")
        print("   Cannot connect to the SOCKS server")
    except socks.GeneralProxyError as e:
        print(f"❌ General Proxy Error: {str(e)}")
    except socket.timeout as e:
        print(f"❌ Socket Timeout: {str(e)}")
    except Exception as e:
        print(f"❌ Method 2 Error: {str(e)}")
        import traceback
        traceback.print_exc()
    
    print("\n============================================")
    print("Proxy test complete!")

if __name__ == "__main__":
    test_proxy_connection()
