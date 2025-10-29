import pytest
import html

@pytest.mark.parametrize(
    "payload,expected_status",
    [
        ({"title": "Ticket A", "description": "Création test"}, 201),
        ({"title": "Incident fibre", "description": "Coupure réseau"}, 201),

        ({}, 422),
        ({"title": ""}, 422),
        ({"description": ""}, 422),
        ({"title": "Titre seul"}, 422),
        ({"description": "Description seule"}, 422),
        ({"title": "", "description": ""}, 422),

        ({"title": 123, "description": "Texte"}, 422),
        ({"title": "Texte", "description": 456}, 422),
        ({"title": None, "description": "Texte"}, 422),
        ({"title": "Texte", "description": None}, 422),
        ({"title": True, "description": "ok"}, 422),
        ({"title": "ok", "description": False}, 422),
        ({"title": ["liste"], "description": "Texte"}, 422),
        ({"title": "ok", "description": ["liste"]}, 422),
        ({"title": {"clé": "val"}, "description": "Texte"}, 422),
        ({"title": "ok", "description": {"clé": "val"}}, 422),

        ({"title": "ok", "description": "ok", "extra": "champ en trop"}, 201),

        ({"title": "<script>alert(1)</script>", "description": "Injection XSS"}, 201),
        ({"title": "DROP TABLE tickets;", "description": "Tentative SQL"}, 201),
        ({"title": "' OR '1'='1", "description": "Injection logique"}, 201),
    ]
)
def test_create_ticket(client, payload, expected_status):
    r_post = client.post("/tickets/", json=payload)
    assert r_post.status_code == expected_status

    if r_post.status_code != 201:
        return

    ticket = r_post.json()
    tid = ticket["id"]

    r_get = client.get(f"/tickets/{tid}")
    assert r_get.status_code == 200
    data = r_get.json()

    assert data["status"] == "open"

    expected_title = html.escape(payload.get("title", ""))
    assert data["title"] == expected_title, "XSS : fail"



'''
def test_create_ticket(client):
    payload = {"title": "Ticket A", "description": "Création test"}
    r = client.post("/tickets/", json=payload)
    assert r.status_code == 201
    data = r.json()
    assert data["title"] == payload["title"]
    assert data["status"] == "open"
'''
