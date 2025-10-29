def test_close_ticket(client):
    new = client.post("/tickets/", json={"title": "To Close", "description": "Close me"}).json()
    tid = new["id"]
    r = client.patch(f"/tickets/{tid}/close")
    assert r.status_code == 200
    assert r.json()["status"] == "closed"
