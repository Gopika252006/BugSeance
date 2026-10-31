from pydantic import BaseModel, Field
from typing import Optional, List

class HealthResponse(BaseModel):
    status: str = Field(..., description="Overall service status")
    model_connected: bool = Field(..., description="Whether Ollama model connection is verified")
    model_name: Optional[str] = Field(None, description="Configured model name if connection succeeded")

class ModelInfo(BaseModel):
    name: str
    size: Optional[int] = None

class AnalyzeRequest(BaseModel):
    input_text: str = Field(..., description="Code snippet, error, or stack trace to analyze")
    language: Optional[str] = Field(None, description="Programming language hint")
    extra_context: Optional[str] = Field(None, description="Any additional user-provided context")

class Section(BaseModel):
    title: str
    content: str

class AnalyzeResponse(BaseModel):
    ghost_message: str = Field(..., description="Spooky opening line")
    problem_summary: str = Field(..., description="Clear explanation of the issue")
    root_cause: str = Field(..., description="Likely cause of the bug")
    evidence: str = Field(..., description="Evidence extracted from input")
    proposed_fix: str = Field(..., description="Suggested fix description")
    code_patch: Optional[str] = Field(None, description="Before/after code snippet if applicable")
    verification_steps: str = Field(..., description="How to verify the fix")
    confidence: str = Field(..., description="Confidence level and reasoning")
    limitations: Optional[str] = Field(None, description="Missing info or limitations")
