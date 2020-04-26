from fastapi import APIRouter
from fastapi.requests import Request

router = APIRouter()


# class Patient(BaseModel):
#     name: str
#     surename: str
#
#
# counter = 0
# list_of_patients: Dict[int, Patient] = {}


# @app.get("/")
# async def hello_world():
#     example from lecture number 1: return {"message": "Hello World"}
#     return {"message": "Hello World during the coronavirus pandemic!"}


@router.api_route("/method", methods=["GET", "POST", "DELETE", "PUT"])
async def method_name(request: Request):
    return {"method": request.method}


# @router.post("/patient")
# def create_patient(patient: Patient):
#     global counter, list_of_patients
#
#     resp = {id: counter, "patient": patient}
#     list_of_patients[counter] = patient
#     counter += 1
#     return resp
#
#
# @router.get("/patient/{pk}")
# def verification_patient(pk: int):
#     global list_of_patients
#
#     if pk in list_of_patients:
#         return list_of_patients.get(pk)
#     else:
#         return JSONResponse(status_code=204, content={})
