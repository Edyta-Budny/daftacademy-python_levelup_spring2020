from typing import Dict

from fastapi import FastAPI

from pydantic import BaseModel
from starlette.requests import Request

from fastapi.responses import JSONResponse

app = FastAPI()
app.counter = 0
app.patients = []


# exercises from lecture number 1
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
# end of exercises from lecture number 1


@app.get("/")
def hello_world():
    # example from lecture number 1: return {"message": "Hello World"}
    return {"message": "Hello World during the coronavirus pandemic!"}


@app.api_route("/method", methods=["GET", "POST", "DELETE", "PUT"])
async def method_name(request: Request):
    return {"method": request.method}


class CreatePatientRq(BaseModel):
    name: str
    surename: str


class CreatePatientResp(BaseModel):
    id = int
    patient = CreatePatientRq


@app.post("/patient", response_model=CreatePatientResp)
def create_patient(pt: CreatePatientRq):
    app.patients.append(pt)
    patient = CreatePatientRq(id=app.counter, patient=pt)
    app.counter += 1
    return patient


@app.get("/patient/{pk}", response_model=CreatePatientRq)
def verification_patient(pk: int):
    if pk >= app.counter or pk <= 0:
        raise JSONResponse(status_code=404)
    else:
        return app.patients[pk]
