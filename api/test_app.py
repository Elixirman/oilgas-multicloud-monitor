from app import app
 
def test_health():
    client = app.test_client()
    res = client.get("/health")
    assert res.status_code == 200
 
def test_ingest_missing_fields():
    client = app.test_client()
    res = client.post("/api/ingest", json={})
    assert res.status_code == 400

