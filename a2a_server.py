from fastapi import FastAPI
from pydantic import BaseModel
import requests
import os

MCP_URL = os.getenv("MCP_URL", "http://localhost:8001/tools/plan_trip")

app = FastAPI(title="A2A Server")

class A2ARequest(BaseModel):
    action: str
    payload: dict

@app.post("/a2a")
def a2a(req: A2ARequest):
    if req.action != "plan_trip":
        return {"status": "error", "message": "Unknown action"}
    r = requests.post(MCP_URL, json=req.payload, timeout=60)
    r.raise_for_status()
    return {"status": "ok", "data": r.json()}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=9000)
