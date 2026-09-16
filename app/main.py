from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from .database import engine, Base, SessionLocal
from . import models
from .schemas import PatientCreate, PatientUpdate

Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def home():
    return {"message": "Voice Patient API is running!"}
@app.get("/patients/{patient_id}")
def get_patient(patient_id: str, db: Session = Depends(get_db)):
    patient = db.query(models.Patient).filter(
        models.Patient.patient_id == patient_id,
        models.Patient.deleted_at.is_(None)
    ).first()

    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    return {
        "data": patient,
        "error": None
    }

@app.post("/patients", status_code=201)
def create_patient(patient: PatientCreate, db: Session = Depends(get_db)):
    new_patient = models.Patient(**patient.model_dump())

    db.add(new_patient)
    db.commit()
    db.refresh(new_patient)

    return {
        "data": new_patient,
        "error": None
    }


@app.get("/patients")
def get_patients(
    last_name: str | None = None,
    date_of_birth: str | None = None,
    phone_number: str | None = None,
    db: Session = Depends(get_db)
):
    query = db.query(models.Patient).filter(
        models.Patient.deleted_at.is_(None)
    )

    if last_name:
        query = query.filter(
            models.Patient.last_name.ilike(last_name)
        )

    if date_of_birth:
        query = query.filter(
            models.Patient.date_of_birth == date_of_birth
        )

    if phone_number:
        digits = "".join(filter(str.isdigit, phone_number))
        query = query.filter(
            models.Patient.phone_number == digits
        )

    patients = query.all()

    return {
        "data": patients,
        "error": None
    }
@app.put("/patients/{patient_id}")
def update_patient(
    patient_id: str,
    patient_update: PatientUpdate,
    db: Session = Depends(get_db)
):
    patient = db.query(models.Patient).filter(
        models.Patient.patient_id == patient_id,
        models.Patient.deleted_at.is_(None)
    ).first()

    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    update_data = patient_update.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(patient, field, value)

    db.commit()
    db.refresh(patient)

    return {
        "data": patient,
        "error": None
    }
@app.delete("/patients/{patient_id}")
def delete_patient(
    patient_id: str,
    db: Session = Depends(get_db)
):
    patient = db.query(models.Patient).filter(
        models.Patient.patient_id == patient_id,
        models.Patient.deleted_at.is_(None)
    ).first()

    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    patient.deleted_at = models.utc_now()

    db.commit()
    db.refresh(patient)

    return {
        "data": patient,
        "error": None
    }