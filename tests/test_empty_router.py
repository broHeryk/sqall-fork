import pytest
from squall import Router, Squall
from squall.testclient import TestClient

app = Squall()

router = Router(prefix="/prefix")


@router.get("")
def get_empty():
    return ["OK"]


app.include_router(router)


client = TestClient(app)


def test_use_empty():
    with client:
        response = client.get("/prefix")
        assert response.status_code == 200, response.text
        assert response.json() == ["OK"]

        response = client.get("/prefix/")
        assert response.status_code == 200, response.text
        assert response.json() == ["OK"]


@pytest.mark.skip(reason="Should we raise an exception in such cases?")
def test_include_empty():
    # if both include and router.path are empty - it should raise exception
    with pytest.raises(Exception):
        app.include_router(router)
