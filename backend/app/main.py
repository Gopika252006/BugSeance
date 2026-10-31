import os
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from .config import Settings, get_settings
from .schemas import AnalyzeRequest, AnalyzeResponse, HealthResponse, ModelInfo
from .services.analysis_service import analyze_bug

app = FastAPI()
# Allow frontend on localhost
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health endpoint will now check Ollama connection


@app.get("/api/health", response_model=HealthResponse)
def health(settings: Settings = Depends(get_settings)):
    """Return basic health information, including AI connection status if possible."""
    try:
        import httpx
        httpx.get(f"{settings.OLLAMA_BASE_URL}/api/tags", timeout=2.0).raise_for_status()
        connected = True
    except Exception:
        connected = False
    return HealthResponse(
        status="ok",
        model_connected=connected,
        model_name=settings.MODEL_NAME if connected else None,
    )

@app.get("/api/models", response_model=list[ModelInfo])
def list_models(settings: Settings = Depends(get_settings)):
    """List models available in the local Ollama instance."""
    try:
        import httpx
        resp = httpx.get(f"{settings.OLLAMA_BASE_URL}/api/tags", timeout=5.0)
        resp.raise_for_status()
        data = resp.json()
        models = [ModelInfo(name=m["name"], size=m.get("size", 0)) for m in data.get("models", [])]
        return models
    except Exception as e:
        raise HTTPException(status_code=503, detail="Ollama unavailable")

@app.post("/api/analyze", response_model=AnalyzeResponse)
def analyze(request: AnalyzeRequest, settings: Settings = Depends(get_settings)):
    """Accept user input and return structured analysis from the AI model."""
    if not request.input_text.strip():
        raise HTTPException(status_code=422, detail="Input text cannot be empty")
    try:
        result = analyze_bug(request.input_text, request.language, settings)
        return result
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))
