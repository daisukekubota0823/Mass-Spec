from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app import crud, schemas
from app.db.session import get_db

router = APIRouter()

@router.post("/mass_spectra/", response_model=schemas.MassSpectrum)
def create_mass_spectrum(
    mass_spectrum: schemas.MassSpectrumCreate, 
    db: Session = Depends(get_db)
):
    return crud.mass_spectrum.create_mass_spectrum(db=db, mass_spectrum=mass_spectrum)

@router.get("/mass_spectra/", response_model=List[schemas.MassSpectrum])
def read_mass_spectra(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db),
    filters: dict = {}
):
    mass_spectra = crud.mass_spectrum.get_mass_spectra(db, skip=skip, limit=limit, filters=filters)
    return mass_spectra

@router.get("/mass_spectra/{mass_spectrum_id}", response_model=schemas.MassSpectrum)
def read_mass_spectrum(mass_spectrum_id: int, db: Session = Depends(get_db)):
    db_mass_spectrum = crud.mass_spectrum.get_mass_spectrum(db, mass_spectrum_id=mass_spectrum_id)
    if db_mass_spectrum is None:
        raise HTTPException(status_code=404, detail="Mass spectrum not found")
    return db_mass_spectrum

@router.put("/mass_spectra/{mass_spectrum_id}", response_model=schemas.MassSpectrum)
def update_mass_spectrum(
    mass_spectrum_id: int, 
    mass_spectrum: schemas.MassSpectrumUpdate, 
    db: Session = Depends(get_db)
):
    db_mass_spectrum = crud.mass_spectrum.update_mass_spectrum(db, mass_spectrum_id, mass_spectrum)
    if db_mass_spectrum is None:
        raise HTTPException(status_code=404, detail="Mass spectrum not found")
    return db_mass_spectrum

@router.delete("/mass_spectra/{mass_spectrum_id}", response_model=schemas.MassSpectrum)
def delete_mass_spectrum(mass_spectrum_id: int, db: Session = Depends(get_db)):
    db_mass_spectrum = crud.mass_spectrum.delete_mass_spectrum(db, mass_spectrum_id=mass_spectrum_id)
    if db_mass_spectrum is None:
        raise HTTPException(status_code=404, detail="Mass spectrum not found")
    return db_mass_spectrum


@router.delete("/mass_spectra/", response_model=dict)
def delete_all_mass_spectra(db: Session = Depends(get_db)):
    deleted_count = crud.mass_spectrum.delete_all_mass_spectra(db)
    return {"message": f"Deleted {deleted_count} mass spectra"}

