def test_list_tickets(client):
    r = client.get("/tickets/")
    assert r.status_code == 200
    data = r.json()
    assert isinstance(data, dict)
    assert "total" in data
    assert "total_pages" in data
    assert "current_page" in data
    assert "per_page" in data
    assert "tickets" in data
    assert isinstance(data["tickets"], list)

def test_pagination_empty_page(client):
    for i in range(3):
        client.post("/tickets/", json={"title": f"Ticket {i}", "description": "Test"})
    r1 = client.get("/tickets/?page=1&per_page=2")
    assert r1.status_code == 200
    data1 = r1.json()
    assert data1["total"] >= 3
    assert len(data1["tickets"]) <= 2

    r2 = client.get("/tickets/?page=999&per_page=2")
    assert r2.status_code == 200
    data2 = r2.json()
    assert isinstance(data2["tickets"], list)
    assert len(data2["tickets"]) == 0 or len(data2["tickets"]) <= 2

def test_get_nonexistent_ticket(client):
    r = client.get("/tickets/999999")
    assert r.status_code == 404
    assert r.json()["detail"] == "Ticket not found"
