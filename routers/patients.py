from fastapi import APIRouter, Request, Response, status
from fastapi.responses import RedirectResponse
from pydantic import BaseModel

from security_credentials import SESSION_TOKEN
from decorators.authorized import authorized


class Patient(BaseModel):
    name: str
    surname: str


router = APIRouter()
list_of_patients = {}


@router.post("/patient")
@authorized(SESSION_TOKEN)
async def create_patient(request: Request, patient: Patient):
    global list_of_patients

    if len(list_of_patients.keys()) == 0:
        patient_id = 0
    else:
        patient_id = max(list_of_patients.keys()) + 1

    list_of_patients[patient_id] = patient

    return RedirectResponse(url=f"/patient/{patient_id}", status_code=status.HTTP_302_FOUND)


@router.get("/patient")
@authorized(SESSION_TOKEN)
async def get_patients(request: Request):
    return list_of_patients


@router.get("/patient/{pk}")
@authorized(SESSION_TOKEN)
async def get_patient(request: Request, pk: int):
    global list_of_patients

    if pk in list_of_patients.keys():
        return list_of_patients[pk]
    else:
        return Response(status_code=204)


@router.delete("/patient/{pk}")
@authorized(SESSION_TOKEN)
async def delete_patient(request: Request, pk: int):
    global list_of_patients

    if pk in list_of_patients.keys():
        del list_of_patients[pk]

    return Response(status_code=204)
