import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Request
from contextlib import asynccontextmanager
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from .agent import create_agent
from .knowledge import knowledge_base
import asyncio


# Compute the .env path relative to this file’s location
base_dir = os.path.abspath(os.path.dirname(__file__))      # backend/app
project_root = os.path.dirname(os.path.dirname(base_dir))  # backend
env_path = os.path.join(project_root, ".env")
load_dotenv(env_path)

reindex_db = os.getenv("REINDEX", "false").lower() == "true"

app = FastAPI(title="Agentic RAG API")

@asynccontextmanager
async def lifespan(app: FastAPI):
    load_dotenv()
    from .knowledge import index_is_empty
    # This runs before the app starts handling request
    global agent
    agent = create_agent()
    if reindex_db or  index_is_empty(knowledge_base.vector_db):
        # This runs once, and subsequent reloads will skip .load()
        await asyncio.to_thread(knowledge_base.load, recreate=False, upsert=True)
    yield


app.router.lifespan_context = lifespan


class QueryRequest(BaseModel):
    text: str

class QueryResponse(BaseModel):
    answer: str
    reasoning: list[str]


@app.exception_handler(Exception)
async def all_exception_handler(request: Request, exc: Exception):
    # Optionally log exc here
    return JSONResponse(
        status_code=500,
        content={"error": str(exc)}
    )


@app.post("/query", response_model=QueryResponse)
async def query_endpoint(req: QueryRequest):
    try:
        # Execute the agent call with full reasoning but not streaming
        run_response = await agent.arun(
            req.text,
            stream=False,
            show_full_reasoning=True,
            stream_intermediate_steps=True,
        )
        
        answer = getattr(run_response, "content", "")
        # No reasoning for summarization by default
        reasoning = []
        if run_response.extra_data and run_response.extra_data.reasoning_steps:
            for step in run_response.extra_data.reasoning_steps:
                step_text = f"**Title**: {step.title}\n**Reasoning**: {step.reasoning}\n**Action**: {step.action or 'None'}\n**Confidence**: {step.confidence}"
                if step.result:
                    step_text += f"\n**Result**: {step.result}"
                reasoning.append(step_text)

        return QueryResponse(answer=answer, reasoning=reasoning)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
