import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_no_ollama():
    response = client.get('/api/health')
    assert response.status_code == 200
    data = response.json()
    assert data['status'] == 'ok'
    assert data['model_connected'] is False

def test_analyze_input_validation():
    # Empty input should return 422
    response = client.post('/api/analyze', json={'input_text': ''})
    assert response.status_code == 422
    assert response.json()['detail'] == 'Input text cannot be empty'

def test_analyze_mock_success(monkeypatch):
    # Mock Ollama generate_completion to return fixed JSON
    def mock_generate_completion(settings, prompt, model=None):
        return '{"ghost_message": "boo", "problem_summary": "summary", "root_cause": "cause", "evidence": "evidence", "proposed_fix": "fix", "code_patch": "patch", "verification_steps": "steps", "confidence": "high", "limitations": "none"}'
    monkeypatch.setattr('app.services.analysis_service.generate_completion', mock_generate_completion)
    response = client.post('/api/analyze', json={'input_text': 'some code'})
    assert response.status_code == 200
    data = response.json()
    assert data['ghost_message'] == 'boo'
    assert data['problem_summary'] == 'summary'

def test_analyze_ollama_unavailable():
    response = client.post('/api/analyze', json={'input_text': 'some code'})
    assert response.status_code == 503
    assert response.json()['detail'] == 'Ollama service unavailable'

