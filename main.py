from typing import Dict

from fastapi import FastAPI

from pydantic import BaseModel
from starlette.requests import Request

app = FastAPI()


@app.get("/")
def hello_world():
    # example from lecture number 1
    # return {"message": "Hello World"}
    return {"message": "Hello World during the coronavirus pandemic!"}


class HelloResp(BaseModel):
    msg: str


@app.get("/hello/{name}", response_model=HelloResp)
def read_item(name: str):
    return HelloResp(msg=f"Hello {name}")


class GiveMeSomethingRq(BaseModel):
    first_key: str


class GiveMeSomethingResp(BaseModel):
    received: Dict
    constant_data: str = "python jest super"


@app.post("/dej/mi/coś", response_model=GiveMeSomethingResp)
def receive_something(rq: GiveMeSomethingRq):
    return GiveMeSomethingResp(received=rq.dict())


@app.api_route("/method", methods=["GET", "POST", "DELETE", "PUT"])
async def method_name(request: Request):
    return {"method": request.method}
