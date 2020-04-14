from typing import Dict

from fastapi import FastAPI
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel


class Patient(BaseModel):
    name: str
    surename: str


app = FastAPI()
counter = 0
list_of_patients: Dict[int, Patient] = {}


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


# homework from lecture number 1
@app.get("/")
def hello_world():
    # example from lecture number 1: return {"message": "Hello World"}
    return {"message": "Hello World during the coronavirus pandemic!"}


@app.api_route("/method", methods=["GET", "POST", "DELETE", "PUT"])
async def method_name(request: Request):
    return {"method": request.method}


@app.post("/patient")
def create_patient(patient: Patient):
    global counter, list_of_patients

    resp = {id: counter, "patient": patient}
    list_of_patients[counter] = patient
    counter += 1
    return resp


@app.get("/patient/{pk}")
def verification_patient(pk: int):
    global list_of_patients

    if pk in list_of_patients:
        return list_of_patients.get(pk)
    else:
        return JSONResponse(status_code=204, content={})
# end of homework from lecture number 1
