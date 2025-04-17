## Usage

Run this command.

```
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000
```

Send Get request on Postman.
```
http://localhost:8000/binancedata?type=1&pageNo=1&pageSize=50
```

That's all !

