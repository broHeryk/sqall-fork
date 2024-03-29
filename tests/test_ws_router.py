from squall import Router, Squall, WebSocket
from squall.testclient import TestClient

router = Router()
prefix_router = Router(prefix="/prefix")
app = Squall()


@app.websocket("/")
async def index(websocket: WebSocket):
    await websocket.accept()
    await websocket.send_text("Hello, world!")
    await websocket.close()


@app.websocket("/some/{param}")
async def index_with_param(websocket: WebSocket, param: str):
    await websocket.accept()
    await websocket.send_text(f"Param: {param}")
    await websocket.close()


@router.websocket("/router")
async def routerindex(websocket: WebSocket):
    await websocket.accept()
    await websocket.send_text("Hello, router!")
    await websocket.close()


@prefix_router.websocket("/")
async def routerprefixindex(websocket: WebSocket):
    await websocket.accept()
    await websocket.send_text("Hello, router with prefix!")
    await websocket.close()


@router.websocket("/router2")
async def routerindex2(websocket: WebSocket):
    await websocket.accept()
    await websocket.send_text("Hello, router!")
    await websocket.close()


app.include_router(router)
app.include_router(prefix_router)


def test_app():
    client = TestClient(app)
    with client.websocket_connect("/") as websocket:
        data = websocket.receive_text()
        assert data == "Hello, world!"


def test_router():
    client = TestClient(app)
    with client.websocket_connect("/router") as websocket:
        data = websocket.receive_text()
        assert data == "Hello, router!"


def test_prefix_router():
    client = TestClient(app)
    with client.websocket_connect("/prefix/") as websocket:
        data = websocket.receive_text()
        assert data == "Hello, router with prefix!"


def test_router2():
    client = TestClient(app)
    with client.websocket_connect("/router2") as websocket:
        data = websocket.receive_text()
        assert data == "Hello, router!"


def test_get_path_param():
    client = TestClient(app)
    with client.websocket_connect("/some/test") as websocket:
        data = websocket.receive_text()
        assert data == "Param: test"
