def test_analytics_counts_and_response_rate(client, auth_headers):
    applied = client.post(
        "/applications",
        json={"company": "Infosys", "role": "Engineer", "status": "Applied"},
        headers=auth_headers,
    ).json()
    client.post(
        "/applications",
        json={"company": "TCS", "role": "Developer", "status": "Wishlist"},
        headers=auth_headers,
    )

    before = client.get("/analytics", headers=auth_headers).json()
    assert before["total"] == 2
    assert before["interviews"] == 0
    assert before["response_rate"] == 0

    client.patch(
        f"/applications/{applied['id']}",
        json={"status": "Interview"},
        headers=auth_headers,
    )

    after = client.get("/analytics", headers=auth_headers).json()
    assert after["interviews"] == 1
    assert after["response_rate"] == 100
    counts = {row["status"]: row["count"] for row in after["by_status"]}
    assert counts["Interview"] == 1
    assert counts["Applied"] == 0