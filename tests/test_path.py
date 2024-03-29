import http
from typing import Optional

import pytest
from squall import Squall
from squall.params import Num, Path, Query, Str
from squall.testclient import TestClient

app = Squall()


@app.add_api("/api_route")
def non_operation():
    return {"message": "Hello World"}


def non_decorated_route():
    return {"message": "Hello World"}


app.add_api_route("/non_decorated_route", non_decorated_route)


@app.get("/text")
def get_text():
    return "Hello World"


@app.get("/path/{item_id}")
def get_id(item_id):
    return item_id


@app.get("/path/str/{item_id}")
def get_str_id(item_id: str):
    return item_id


@app.get("/path/int/{item_id}")
def get_int_id(item_id: int):
    return item_id


@app.get("/path/float/{item_id}")
def get_float_id(item_id: float):
    return item_id


@app.get("/path/param/{item_id}")
def get_path_param_id(item_id: Optional[str] = Path(None)):
    return item_id


@app.get("/path/param-required/{item_id}")
def get_path_param_required_id(item_id: str = Path(...)):
    return item_id


@app.get("/path/param-minlength/{item_id}")
def get_path_param_min_len(item_id: str = Path(..., valid=Str(min_len=3))):
    return item_id


@app.get("/path/param-maxlength/{item_id}")
def get_path_param_max_len(item_id: str = Path(..., valid=Str(max_len=3))):
    return item_id


@app.get("/path/param-min_maxlength/{item_id}")
def get_path_param_min_max_len(
    item_id: str = Path(..., valid=Str(max_len=3, min_len=2))
):
    return item_id


@app.get("/path/param-gt/{item_id}")
def get_path_param_gt(item_id: float = Path(..., valid=Num(gt=3))):
    return item_id


@app.get("/path/param-gt0/{item_id}")
def get_path_param_gt0(item_id: float = Path(..., valid=Num(gt=0))):
    return item_id


@app.get("/path/param-ge/{item_id}")
def get_path_param_ge(item_id: float = Path(..., valid=Num(ge=3))):
    return item_id


@app.get("/path/param-lt/{item_id}")
def get_path_param_lt(item_id: float = Path(..., valid=Num(lt=3))):
    return item_id


@app.get("/path/param-lt0/{item_id}")
def get_path_param_lt0(item_id: float = Path(..., valid=Num(lt=0))):
    return item_id


@app.get("/path/param-le/{item_id}")
def get_path_param_le(item_id: float = Path(..., valid=Num(le=3))):
    return item_id


@app.get("/path/param-lt-gt/{item_id}")
def get_path_param_lt_gt(item_id: float = Path(..., valid=Num(lt=3, gt=1))):
    return item_id


@app.get("/path/param-le-ge/{item_id}")
def get_path_param_le_ge(item_id: float = Path(..., valid=Num(le=3, ge=1))):
    return item_id


@app.get("/path/param-lt-int/{item_id}")
def get_path_param_lt_int(item_id: int = Path(..., valid=Num(lt=3))):
    return item_id


@app.get("/path/param-gt-int/{item_id}")
def get_path_param_gt_int(item_id: int = Path(..., valid=Num(gt=3))):
    return item_id


@app.get("/path/param-le-int/{item_id}")
def get_path_param_le_int(item_id: int = Path(..., valid=Num(le=3))):
    return item_id


@app.get("/path/param-ge-int/{item_id}")
def get_path_param_ge_int(item_id: int = Path(..., valid=Num(ge=3))):
    return item_id


@app.get("/path/param-lt-gt-int/{item_id}")
def get_path_param_lt_gt_int(item_id: int = Path(..., valid=Num(lt=3, gt=1))):
    return item_id


@app.get("/path/param-le-ge-int/{item_id}")
def get_path_param_le_ge_int(item_id: int = Path(..., valid=Num(le=3, ge=1))):
    return item_id


@app.get("/query")
def get_query(query):
    return f"foo bar {query}"


@app.get("/query/optional")
def get_query_optional(query=None):
    if query is None:
        return "foo bar"
    return f"foo bar {query}"


@app.get("/query/int")
def get_query_type(query: int):
    return f"foo bar {query}"


@app.get("/query/int/optional")
def get_query_type_optional(query: Optional[int] = None):
    if query is None:
        return "foo bar"
    return f"foo bar {query}"


@app.get("/query/int/default")
def get_query_type_int_default(query: int = 10):
    return f"foo bar {query}"


@app.get("/query/param")
def get_query_param(query=Query(None)):
    if query is None:
        return "foo bar"
    return f"foo bar {query}"


@app.get("/query/param-required")
def get_query_param_required(query=Query(...)):
    return f"foo bar {query}"


@app.get("/query/param-required/int")
def get_query_param_required_type(query: int = Query(...)):
    return f"foo bar {query}"


@app.get("/enum-status-code", status_code=http.HTTPStatus.CREATED)
def get_enum_status_code():
    return "foo bar"


client = TestClient(app)


def test_text_get():
    response = client.get("/text")
    assert response.status_code == 200, response.text
    assert response.json() == "Hello World"


def test_nonexistent():
    response = client.get("/nonexistent")
    assert response.status_code == 404, response.text
    assert response.json() == {"detail": "Not Found"}


response_not_valid_bool = {
    "detail": [
        {
            "loc": ["path", "item_id"],
            "msg": "value could not be parsed to a boolean",
            "type": "type_error.bool",
        }
    ]
}

response_not_valid_int = {
    "details": [
        {"loc": ["path_params", "item_id"], "msg": "Cast of `int` failed", "val": "2.7"}
    ]
}

response_not_valid_float = {
    "details": [
        {
            "loc": ["path_params", "item_id"],
            "msg": "Cast of `float` failed",
            "val": "True",
        }
    ]
}

response_at_least_3 = {
    "details": [
        {"loc": ["path_params", "item_id"], "msg": "Validation error", "val": "fo"}
    ]
}


response_at_least_2 = {
    "details": [
        {"loc": ["path_params", "item_id"], "msg": "Validation error", "val": "f"}
    ]
}


response_maximum_3 = {
    "details": [
        {"loc": ["path_params", "item_id"], "msg": "Validation error", "val": "foobar"}
    ]
}


response_greater_than_3 = {
    "details": [
        {"loc": ["path_params", "item_id"], "msg": "Validation error", "val": 2}
    ]
}


response_greater_than_0 = {
    "details": [
        {"loc": ["path_params", "item_id"], "msg": "Validation error", "val": 0.0}
    ]
}


response_greater_than_1 = {
    "details": [
        {"loc": ["path_params", "item_id"], "msg": "Validation error", "val": 0}
    ]
}


response_greater_than_equal_3 = {
    "details": [
        {"loc": ["path_params", "item_id"], "msg": "Validation error", "val": 2}
    ]
}


response_less_than_3 = {
    "details": [
        {"loc": ["path_params", "item_id"], "msg": "Validation error", "val": 4}
    ]
}


response_less_than_0 = {
    "details": [
        {"loc": ["path_params", "item_id"], "msg": "Validation error", "val": 0}
    ]
}


response_less_than_equal_3 = {
    "details": [
        {"loc": ["path_params", "item_id"], "msg": "Validation error", "val": 4}
    ]
}


@pytest.mark.parametrize(
    "path,expected_status,expected_response",
    [
        ("/path/foobar", 200, "foobar"),
        ("/path/str/foobar", 200, "foobar"),
        ("/path/str/42", 200, "42"),
        ("/path/str/True", 200, "True"),
        ("/path/int/2.7", 400, response_not_valid_int),
        ("/path/int/42", 200, 42),
        ("/path/int/2.7", 400, response_not_valid_int),
        ("/path/float/True", 400, response_not_valid_float),
        ("/path/float/42", 200, 42),
        ("/path/float/42.5", 200, 42.5),
        ("/path/param/foo", 200, "foo"),
        ("/path/param-required/foo", 200, "foo"),
        ("/path/param-minlength/foo", 200, "foo"),
        ("/path/param-minlength/fo", 400, response_at_least_3),
        ("/path/param-maxlength/foo", 200, "foo"),
        ("/path/param-maxlength/foobar", 400, response_maximum_3),
        ("/path/param-min_maxlength/foo", 200, "foo"),
        ("/path/param-min_maxlength/foobar", 400, response_maximum_3),
        ("/path/param-min_maxlength/f", 400, response_at_least_2),
        ("/path/param-gt/4", 200, 4),
        ("/path/param-gt/2", 400, response_greater_than_3),
        ("/path/param-gt0/0.05", 200, 0.05),
        ("/path/param-gt0/0", 400, response_greater_than_0),
        ("/path/param-ge/4", 200, 4),
        ("/path/param-ge/3", 200, 3),
        ("/path/param-ge/2", 400, response_greater_than_equal_3),
        ("/path/param-lt/4", 400, response_less_than_3),
        ("/path/param-lt/2", 200, 2),
        ("/path/param-lt0/-1", 200, -1),
        ("/path/param-lt0/0", 400, response_less_than_0),
        ("/path/param-le/4", 400, response_less_than_equal_3),
        ("/path/param-le/3", 200, 3),
        ("/path/param-le/2", 200, 2),
        ("/path/param-lt-gt/2", 200, 2),
        ("/path/param-lt-gt/4", 400, response_less_than_3),
        ("/path/param-lt-gt/0", 400, response_greater_than_1),
        ("/path/param-le-ge/2", 200, 2),
        ("/path/param-le-ge/1", 200, 1),
        ("/path/param-le-ge/3", 200, 3),
        ("/path/param-le-ge/4", 400, response_less_than_equal_3),
        ("/path/param-lt-int/2", 200, 2),
        ("/path/param-lt-int/4", 400, response_less_than_3),
        ("/path/param-lt-int/2.7", 400, response_not_valid_int),
        ("/path/param-gt-int/4", 200, 4),
        ("/path/param-gt-int/2", 400, response_greater_than_3),
        ("/path/param-gt-int/2.7", 400, response_not_valid_int),
        ("/path/param-le-int/4", 400, response_less_than_equal_3),
        ("/path/param-le-int/3", 200, 3),
        ("/path/param-le-int/2", 200, 2),
        ("/path/param-le-int/2.7", 400, response_not_valid_int),
        ("/path/param-ge-int/42", 200, 42),
        ("/path/param-ge-int/3", 200, 3),
        ("/path/param-ge-int/2", 400, response_greater_than_equal_3),
        ("/path/param-ge-int/2.7", 400, response_not_valid_int),
        ("/path/param-lt-gt-int/2", 200, 2),
        ("/path/param-lt-gt-int/4", 400, response_less_than_3),
        ("/path/param-lt-gt-int/0", 400, response_greater_than_1),
        ("/path/param-lt-gt-int/2.7", 400, response_not_valid_int),
        ("/path/param-le-ge-int/2", 200, 2),
        ("/path/param-le-ge-int/1", 200, 1),
        ("/path/param-le-ge-int/3", 200, 3),
        ("/path/param-le-ge-int/4", 400, response_less_than_equal_3),
        ("/path/param-le-ge-int/2.7", 400, response_not_valid_int),
    ],
)
def test_get_path(path, expected_status, expected_response):
    response = client.get(path)
    assert response.status_code == expected_status
    assert response.json() == expected_response
