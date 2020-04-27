from fastapi import APIRouter, Request, status, Response
from fastapi.responses import RedirectResponse
from pydantic import BaseModel

from credentials_variables import SESSION_TOKEN
from decorators.authorized import authorized

router = APIRouter()


class Patient(BaseModel):
    name: str
    surname: str


list_of_patients = {}


@router.post("/patient")
@authorized(SESSION_TOKEN)
def create_patient(request: Request, patient: Patient):
    global list_of_patients

    if len(list_of_patients.keys()) == 0:
        patient_id = 0
    else:
        patient_id = max(list_of_patients.keys()) + 1

    list_of_patients[patient_id] = patient

    return RedirectResponse(url=f"/patient/{patient_id}", status_code=status.HTTP_302_FOUND)


@router.get("/patient")
@authorized(SESSION_TOKEN)
def get_patients(request: Request, response: Response):
    global list_of_patients

    if len(list_of_patients) != 0:
        return list_of_patients

    response.status_code = status.HTTP_204_NO_CONTENT


@router.get("/patient/{pk}")
@authorized(SESSION_TOKEN)
def get_patient(request: Request, response: Response, pk: int):
    global list_of_patients

    if pk in list_of_patients.keys():
        return list_of_patients[pk]

    response.status_code = status.HTTP_204_NO_CONTENT


@router.delete("/patient/{pk}")
@authorized(SESSION_TOKEN)
def delete_patient(request: Request, response: Response, pk: int):
    global list_of_patients

    if pk in list_of_patients.keys():
        del list_of_patients[pk]

    response.status_code = status.HTTP_204_NO_CONTENT
