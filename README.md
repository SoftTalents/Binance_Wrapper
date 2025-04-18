# Binance Wrapper

A Python FastAPI application that serves as a proxy for Binance API requests.

## Usage

Install the requirements and start the server:

```bash
pip install -r requirements.txt
python main.py
```

The server will start on http://0.0.0.0:8000 by default.

## Endpoints

### 1. `/binancedata`
Fetches Binance article data and proxies the JSON directly.

- **Method:** GET  
- **Query Parameters:**  
  - `type` (int): Article type identifier.  
  - `pageNo` (int): Page number.  
  - `pageSize` (int): Number of articles per page.  

**Example Request:**
```
http://localhost:8000/binancedata?type=1&pageNo=1&pageSize=50
```

**Response:**  
The JSON payload returned by Binance's API.

---

### 2. `/serverinfo`
Returns information about the server where this API is running.

- **Method:** GET  

**Example Request:**
```
http://localhost:8000/serverinfo
```

**Example Response:**
```json
{
  "ip": "203.0.113.45",
  "country": "Colombia",
  "city": "Bogotá"
}
```

## Notes

- The application uses a SOCKS5 proxy to route requests to Binance's API
- Proxy configuration is stored in the `.env` file
- Debug endpoints are available for testing the proxy connection

## Debugging

If you encounter issues, you can use the provided debug scripts:

```bash
python debug.py         # Test the proxy connection
python debug_binance.py # Test the Binance API connection specifically
```

That's all! Keep your API key safe and enjoy your proxy server.