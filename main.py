from typing import Dict

from fastapi import FastAPI

from pydantic import BaseModel

from fastapi.requests import Request

from fastapi.responses import JSONResponse


app = FastAPI()
counter = 0
patients = []


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


@app.post("/patient")
def create_patient(patient: CreatePatientRq):
    global counter, patients

    patient = CreatePatientResp(id=counter, patient=patient)
    patients.append(patient)
    counter += 1
    return patient


@app.get("/patient/{pk}")
def verification_patient(pk: int):
    global patients

    patient_searched = next((patient for patient in patients if patient.id == pk), None)
    if patient_searched:
        return patient_searched.patient
    else:
        return JSONResponse(status_code=204, content={})
