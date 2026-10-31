import httpx
from typing import Any, Dict
from ..config import Settings

def get_model_tags(settings: Settings) -> Dict[str, Any]:
    """Retrieve the list of available models from Ollama.
    Returns the parsed JSON response.
    """
    url = f"{settings.OLLAMA_BASE_URL}/api/tags"
    resp = httpx.get(url, timeout=5.0)
    resp.raise_for_status()
    return resp.json()

def generate_completion(settings: Settings, prompt: str, model: str | None = None) -> str:
    """Send a prompt to Ollama and return the generated text.
    Uses the /api/generate endpoint.
    """
    model_name = model or settings.MODEL_NAME
    payload = {
        "model": model_name,
        "prompt": prompt,
        "stream": False,
        "temperature": 0.7,
    }
    url = f"{settings.OLLAMA_BASE_URL}/api/generate"
    resp = httpx.post(url, json=payload, timeout=30.0)
    resp.raise_for_status()
    data = resp.json()
    # Ollama returns {'response': 'text', ...}
    return data.get("response", "")
