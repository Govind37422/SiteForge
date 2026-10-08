from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json()["status"] == "online"

def test_get_templates():
    response = client.get("/api/templates")
    assert response.status_code == 200
    templates = response.json()
    assert len(templates) >= 4
    assert "mobile-fitness" in [t["id"] for t in templates]

def test_project_lifecycle():
    # 1. Generate (simulated short prompt triggers fallback for speed)
    res_gen = client.post("/api/generate", json={"prompt": "A crypto tracking app."})
    assert res_gen.status_code == 200
    project = res_gen.json()
    assert "id" in project
    assert "files" in project
    
    project_id = project["id"]
    
    # 2. Get Project
    res_get = client.get(f"/api/projects/{project_id}")
    assert res_get.status_code == 200
    assert res_get.json()["id"] == project_id
    
    # 3. Preview
    res_prev = client.get(f"/api/preview/{project_id}")
    assert res_prev.status_code == 200
    assert b"<html" in res_prev.content or b"<!DOCTYPE" in res_prev.content
    
    # 4. Refine
    res_ref = client.post("/api/refine", json={"project_id": project_id, "prompt": "Make the background dark."})
    assert res_ref.status_code == 200
    assert res_ref.json()["revision_number"] > 1
    
    # 5. Delete
    res_del = client.delete(f"/api/projects/{project_id}")
    assert res_del.status_code == 200
    
    # Ensure deleted
    res_get_deleted = client.get(f"/api/projects/{project_id}")
    assert res_get_deleted.status_code == 404
