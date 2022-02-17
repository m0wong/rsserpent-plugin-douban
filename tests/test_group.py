from starlette.testclient import TestClient


def test_group(client: TestClient) -> None:
    """Test `rsserpent_plugin_douban.route`."""
    response = client.get("/douban/group/727241")
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/xml"
    # assert response.text.count("我真见过世面小组 - 豆瓣") == 1
    assert "<title>\n    我真见过世面小组 - 豆瓣\n</title>" in response.text
