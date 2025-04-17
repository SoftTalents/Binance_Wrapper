## Usage

Install the requirements and start the server:

```bash
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000
```

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
The JSON payload returned by Binance’s API.

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

That's all! Keep your API key safe and enjoy your proxy server.