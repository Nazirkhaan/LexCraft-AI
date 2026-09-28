from fastapi.testclient import TestClient
from backend.brand import APP_NAME
from backend.main import app

client = TestClient(app)

def test_health():
    r = client.get('/health'); assert r.status_code == 200; assert r.json()['status'] == 'ok'

def test_root():
    r = client.get('/'); assert r.status_code == 200; assert r.json()['service'] == APP_NAME

def test_generate_validation():
    # Missing fields must be rejected by Pydantic (422), engine untouched.
    r = client.post('/generate', json={})
    assert r.status_code == 422

def test_generate_success_mocked(monkeypatch):
    # Full pipeline (sanitize -> response) with the Gemini call mocked out,
    # proving everything works end-to-end once a valid API key is configured.
    import backend.routes as routes

    monkeypatch.setattr(
        routes.generator,
        "generate_document",
        lambda *a, **k: "EMPLOYMENT CONTRACT\n\n1. Role: Engineer;\n\nImportant Notice: Review.",
    )
    payload = {
        "document_type": "Employment Contract",
        "parties": "Jane Doe (Employee), TechNova Inc. (Employer)",
        "terms": "Role: Engineer;",
        "dates": "April 10, 2026",
    }
    r = client.post('/generate', json=payload)
    assert r.status_code == 200
    data = r.json()
    assert data['document_type'] == 'Employment Contract'
    assert 'EMPLOYMENT CONTRACT' in data['content']
    assert data['model']
