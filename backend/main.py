import asyncio
import uuid
from datetime import datetime
from typing import Dict

from fastapi import FastAPI, BackgroundTasks, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

load_dotenv(dotenv_path="../.env")

from models import WorkflowRequest, WorkflowStatus, WorkflowStatusResponse, AgentStep, StepStatus, SubmitResponse
from agent_runner import run_agent
from verticals.registry import list_verticals

app = FastAPI(title="MedBridge Platform API", version="2.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173",
                   "http://localhost:5174", "http://localhost:5175",
                   "http://localhost:5176", "http://localhost:5177",
                   "http://localhost:5200", "http://127.0.0.1:5200"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

store: Dict[str, WorkflowStatusResponse] = {}


async def process_workflow(workflow_id: str, request: WorkflowRequest):
    store[workflow_id].status = WorkflowStatus.processing
    store[workflow_id].updated_at = datetime.utcnow().isoformat()

    async def step_callback(step: AgentStep):
        existing = store[workflow_id].steps
        updated = False
        for i, s in enumerate(existing):
            if s.tool_name == step.tool_name and s.status == StepStatus.running and step.status == StepStatus.done:
                existing[i] = step
                updated = True
                break
        if not updated:
            existing.append(step)
        store[workflow_id].steps = existing
        store[workflow_id].updated_at = datetime.utcnow().isoformat()

    try:
        result = await run_agent(request.vertical_id, request.ai_provider, request.form_data, step_callback)
        store[workflow_id].status = WorkflowStatus.submitted
        store[workflow_id].result = result
        store[workflow_id].updated_at = datetime.utcnow().isoformat()
    except Exception as e:
        store[workflow_id].status = WorkflowStatus.needs_info
        store[workflow_id].result = f"Error during processing: {str(e)}"
        store[workflow_id].updated_at = datetime.utcnow().isoformat()


@app.get("/api/verticals")
async def get_verticals():
    return list_verticals()


@app.post("/api/workflow/submit", response_model=SubmitResponse)
async def submit_workflow(request: WorkflowRequest, background_tasks: BackgroundTasks):
    workflow_id = str(uuid.uuid4())
    now = datetime.utcnow().isoformat()

    store[workflow_id] = WorkflowStatusResponse(
        workflow_id=workflow_id,
        vertical_id=request.vertical_id,
        ai_provider=request.ai_provider,
        status=WorkflowStatus.pending,
        created_at=now,
        updated_at=now,
        steps=[],
        result=None,
        form_data=request.form_data
    )

    background_tasks.add_task(process_workflow, workflow_id, request)

    return SubmitResponse(
        workflow_id=workflow_id,
        status=WorkflowStatus.pending,
        message="Workflow started."
    )


@app.get("/api/workflow/{workflow_id}/status", response_model=WorkflowStatusResponse)
async def get_status(workflow_id: str):
    if workflow_id not in store:
        raise HTTPException(status_code=404, detail="Workflow not found")
    return store[workflow_id]


@app.get("/api/workflow/history/all")
async def get_history():
    return sorted([
        {
            "workflow_id": wf.workflow_id,
            "vertical_id": wf.vertical_id,
            "status": wf.status,
            "created_at": wf.created_at,
            "summary": next((v for k, v in (wf.form_data or {}).items() if k in ["patient_name", "client_name", "applicant_name"]), "Unknown"),
        }
        for wf in store.values()
    ], key=lambda x: x["created_at"], reverse=True)


@app.post("/api/demo/reset")
async def reset():
    store.clear()
    return {"message": "Reset complete"}


@app.get("/health")
async def health():
    return {"status": "ok", "service": "MedBridge Platform", "version": "2.0.0"}
