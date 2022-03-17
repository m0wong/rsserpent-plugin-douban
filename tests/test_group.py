from starlette.testclient import TestClient


def test_group(client: TestClient) -> None:
    """Test `rsserpent_plugin_douban.route`."""
    response = client.get("/douban/group/727241")
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/xml"
    assert "<title>烂照拯救小组小组的讨论</title>" in response.text
