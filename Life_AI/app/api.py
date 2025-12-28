
from fastapi import FastAPI, BackgroundTasks
import uuid
from .schemas import RunConfig
from .worker import execute_run, runs

app = FastAPI()

@app.post("/runs")
async def start_run(config: RunConfig, background_tasks: BackgroundTasks):
    run_id = str(uuid.uuid4())
    runs[run_id] = {"status": "starting", "config": config.model_dump(), "trace": [], "results": [], "summary": {}}
    background_tasks.add_task(execute_run, run_id, config)
    return {"run_id": run_id}

@app.get("/runs/{run_id}/status")
async def get_run_status(run_id: str):
    run = runs.get(run_id)
    if not run:
        return {"error": "Run not found"}
    return {"status": run["status"]}

@app.get("/runs/{run_id}/results")
async def get_run_results(run_id: str):
    run = runs.get(run_id)
    if not run:
        return {"error": "Run not found"}
    return {"results": run.get("results", [])}

@app.get("/runs/{run_id}/trace")
async def get_run_trace(run_id: str):
    run = runs.get(run_id)
    if not run:
        return {"error": "Run not found"}
    return {"trace": run.get("trace", [])}

@app.get("/runs/{run_id}/summary")
async def get_run_summary(run_id: str):
    """Get summary statistics including failure breakdown"""
    run = runs.get(run_id)
    if not run:
        return {"error": "Run not found"}
    return {"summary": run.get("summary", {})}

