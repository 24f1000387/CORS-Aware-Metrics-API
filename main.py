import time
import uuid
from fastapi import FastAPI, Request, Response

app = FastAPI()

MY_ALLOWED_ORIGIN = "https://dash-nt6awh.example.com"

# The Bulletproof Unified Middleware
# This handles the custom headers AND the strict CORS policy manually,
# bypassing any built-in framework quirks.
@app.middleware("http")
async def unified_middleware(request: Request, call_next):
    start_time = time.time()
    
    # 1. Intercept OPTIONS requests immediately for preflight success
    if request.method == "OPTIONS":
        response = Response(status_code=200)
    else:
        # Otherwise, let the request go to our /stats endpoint
        response = await call_next(request)
    
    # 2. Always attach the required custom headers (even to preflights!)
    process_time = time.time() - start_time
    response.headers["X-Request-ID"] = str(uuid.uuid4())
    response.headers["X-Process-Time"] = str(process_time)
    
    # 3. Manual Strict CORS Handling
    # If the origin matches exactly, attach the ACAO header. 
    # If it's an evil origin, this block is skipped and it gets nothing.
    origin = request.headers.get("origin")
    if origin == MY_ALLOWED_ORIGIN:
        response.headers["Access-Control-Allow-Origin"] = MY_ALLOWED_ORIGIN
        response.headers["Access-Control-Allow-Methods"] = "GET, OPTIONS"
        response.headers["Access-Control-Allow-Headers"] = "*"
        
    return response

@app.get("/stats")
async def calculate_statistics(values: str = ""):
    parsed_numbers = []
    if values:
        for val in values.split(","):
            val = val.strip()
            if val: 
                parsed_numbers.append(int(val))
    
    if len(parsed_numbers) == 0:
        return {
            "email": "24f1000387@ds.study.iitm.ac.inm",
            "count": 0,
            "sum": 0,
            "min": 0,
            "max": 0,
            "mean": 0.0
        }
    
    total_count = len(parsed_numbers)
    total_sum = sum(parsed_numbers)
    
    return {
        "email": "24f1000387@ds.study.iitm.ac.in", # <-- UPDATE THIS AGAIN!
        "count": total_count,
        "sum": total_sum,
        "min": min(parsed_numbers),
        "max": max(parsed_numbers),
        "mean": total_sum / total_count
    }
