def test_perf_response_time(client):
    import time
    start = time.time()
    r = client.get("/tickets/")
    assert r.status_code == 200
    assert float(r.headers["X-Process-Time"].replace("ms", "")) < 200  # <200ms
