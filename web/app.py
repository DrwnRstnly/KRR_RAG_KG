
import json
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path

from src.rag.llm import llm
from src.rag.pipeline import RAGPipeline

app = FastAPI(title="Clash Royale KG RAG")


BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))


app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")


pipeline = RAGPipeline(llm, verbose=False)


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/api/chat/stream")
async def chat_stream(question: str):
    
    async def event_generator():
        try:
            for event_type, data in pipeline.query_with_streaming(question):

                if event_type == "done":

                    yield f"event: done\n"
                    yield f"data: {json.dumps(data)}\n\n"
                else:

                    yield f"event: {event_type}\n"
                    if '\n' in str(data):
                        for line in str(data).split('\n'):
                            yield f"data: {line}\n"
                        yield "\n"
                    else:
                        yield f"data: {data}\n\n"
        except Exception as e:
            yield f"event: error\n"
            yield f"data: {str(e)}\n\n"

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no"
        }
    )


@app.on_event("startup")
async def startup_event():
    
    if pipeline.test_connection():
        print("[OK] Connected to Neo4j knowledge graph")
    else:
        print("[ERR] Failed to connect to Neo4j")


@app.on_event("shutdown")
async def shutdown_event():
    
    pipeline.close()
    print("[OK] Pipeline closed")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
