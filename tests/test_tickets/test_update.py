def test_update_ticket(client):
    new = client.post("/tickets/", json={"title": "Old", "description": "Desc"}).json()
    tid = new["id"]
    r = client.put(f"/tickets/{tid}", json={"title": "Updated", "description": "Changed"})
    assert r.status_code == 200
    assert r.json()["title"] == "Updated"


def test_update_ticket_not_found(client):
    payload = {"title": "Nouveau titre", "description": "Nouvelle description"}
    r = client.put("/tickets/999999", json=payload)
    assert r.status_code == 404
    assert r.json()["detail"] == "Ticket not found"
