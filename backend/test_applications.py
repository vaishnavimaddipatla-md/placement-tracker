def make_app(client, headers, company="Infosys", role="Systems Engineer", status="Applied"):
    res = client.post(
        "/applications",
        json={"company": company, "role": role, "status": status},
        headers=headers,
    )
    assert res.status_code == 201
    return res.json()


def test_create_application_defaults_to_wishlist(client, auth_headers):
    res = client.post(
        "/applications",
        json={"company": "TCS", "role": "Developer"},
        headers=auth_headers,
    )
    assert res.status_code == 201
    body = res.json()
    assert body["status"] == "Wishlist"
    assert body["id"]


def test_create_application_rejects_invalid_status(client, auth_headers):
    res = client.post(
        "/applications",
        json={"company": "TCS", "role": "Developer", "status": "Hired"},
        headers=auth_headers,
    )
    assert res.status_code == 422


def test_list_search_and_status_filter(client, auth_headers):
    make_app(client, auth_headers, company="Infosys", status="Applied")
    make_app(client, auth_headers, company="TCS", status="Wishlist")

    everything = client.get("/applications", headers=auth_headers).json()
    assert len(everything) == 2

    searched = client.get("/applications", params={"search": "tcs"}, headers=auth_headers).json()
    assert len(searched) == 1
    assert searched[0]["company"] == "TCS"

    filtered = client.get("/applications", params={"status": "Applied"}, headers=auth_headers).json()
    assert len(filtered) == 1
    assert filtered[0]["company"] == "Infosys"


def test_update_status_keeps_other_fields(client, auth_headers):
    created = make_app(client, auth_headers)
    res = client.patch(
        f"/applications/{created['id']}",
        json={"status": "Interview"},
        headers=auth_headers,
    )
    assert res.status_code == 200
    assert res.json()["status"] == "Interview"
    assert res.json()["company"] == "Infosys"


def test_delete_application(client, auth_headers):
    created = make_app(client, auth_headers)
    res = client.delete(f"/applications/{created['id']}", headers=auth_headers)
    assert res.status_code == 204
    res = client.get(f"/applications/{created['id']}", headers=auth_headers)
    assert res.status_code == 404


def test_users_cannot_access_each_others_applications(client, auth_headers, other_headers):
    created = make_app(client, auth_headers)
    app_url = f"/applications/{created['id']}"

    assert client.get("/applications", headers=other_headers).json() == []
    assert client.get(app_url, headers=other_headers).status_code == 404
    assert client.patch(app_url, json={"status": "Offer"}, headers=other_headers).status_code == 404
    assert client.delete(app_url, headers=other_headers).status_code == 404

    # the owner still has it
    assert client.get(app_url, headers=auth_headers).status_code == 200