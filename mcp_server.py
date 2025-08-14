from fastapi import FastAPI
from pydantic import BaseModel
from app_core import get_planner

app = FastAPI(title="Travel MCP Tool Server")

class PlanPayload(BaseModel):
    destinations: str
    dates: str
    budget: int
    interests: str
    use_live: bool = False
    use_rag: bool = False

@app.post("/tools/plan_trip")
def plan_trip(p: PlanPayload):
    planner = get_planner(use_live=p.use_live, use_rag=p.use_rag)
    out = planner.invoke({
        "inputs": {
            "destinations": p.destinations,
            "dates": p.dates,
            "budget": p.budget,
            "interests": p.interests
        }
    })
    return out

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
