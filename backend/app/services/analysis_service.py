import json
from typing import Optional
from fastapi import HTTPException

from ..config import Settings
from ..schemas import AnalyzeRequest, AnalyzeResponse
from .ollama_service import generate_completion

# System prompt defining ghost personality and required structured response
SYSTEM_PROMPT = (
    "You are a helpful debugging ghost. Respond with a JSON object containing the following keys:"
    " ghost_message, problem_summary, root_cause, evidence, proposed_fix, code_patch, verification_steps, confidence, limitations."
    " Use concise, clear language. Do NOT fabricate line numbers or evidence not present in the input."
    " If any field is not applicable, provide an empty string."
)

def build_prompt(user_input: str, language: Optional[str] = None, extra_context: Optional[str] = None) -> str:
    prompt = SYSTEM_PROMPT + "\nUser input: " + user_input
    if language:
        prompt += f"\nLanguage hint: {language}"
    if extra_context:
        prompt += f"\nAdditional context: {extra_context}"
    prompt += "\nReturn ONLY the JSON object."
    return prompt

def analyze_bug(input_text: str, language: Optional[str], settings: Settings) -> AnalyzeResponse:
    # Build prompt for Ollama
    prompt = build_prompt(input_text, language)
    try:
        raw_response = generate_completion(settings, prompt)
    except Exception as exc:
        # Propagate as 503 Service Unavailable for downstream handling
        raise HTTPException(status_code=503, detail="Ollama service unavailable")
    try:
        data = json.loads(raw_response)
    except json.JSONDecodeError as e:
        raise Exception(f"Malformed AI response: {e}")
    # Validate required keys exist; missing ones become empty strings
    def get(key: str) -> str:
        return str(data.get(key, ""))
    response = AnalyzeResponse(
        ghost_message=get("ghost_message"),
        problem_summary=get("problem_summary"),
        root_cause=get("root_cause"),
        evidence=get("evidence"),
        proposed_fix=get("proposed_fix"),
        code_patch=get("code_patch"),
        verification_steps=get("verification_steps"),
        confidence=get("confidence"),
        limitations=get("limitations"),
    )
    return response
