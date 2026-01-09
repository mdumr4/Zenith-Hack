# server.py
from fastapi import FastAPI
import uvicorn
from core.router import route_input, route_chat

app = FastAPI()

@app.post("/predict")
async def predict(data: dict):
    # Team B: Implement latency-critical prediction here
    return {"suggestion": ""}

@app.post("/chat")
async def chat(data: dict):
    # Team B: Implement Plan Mode chat here
    return {"response": "..."}

if __name__ == "__main__":
    # Team A Protocol: Port 18492
    uvicorn.run(app, host="127.0.0.1", port=18492)
