from sqlalchemy.orm import Session
from app.models.mass_spectrum import MassSpectrum
from app.schemas.mass_spectrum import MassSpectrumCreate, MassSpectrumUpdate
from typing import List, Optional

def get_mass_spectrum(db: Session, mass_spectrum_id: int) -> Optional[MassSpectrum]:
    return db.query(MassSpectrum).filter(MassSpectrum.id == mass_spectrum_id).first()

def get_mass_spectra(
    db: Session, 
    skip: int = 0, 
    limit: int = 100, 
    filters: dict = {}
) -> List[MassSpectrum]:
    query = db.query(MassSpectrum)
    for key, value in filters.items():
        if hasattr(MassSpectrum, key):
            query = query.filter(getattr(MassSpectrum, key) == value)
    return query.offset(skip).limit(limit).all()

def create_mass_spectrum(db: Session, mass_spectrum: MassSpectrumCreate) -> MassSpectrum:
    db_mass_spectrum = MassSpectrum(**mass_spectrum.dict())
    db.add(db_mass_spectrum)
    db.commit()
    db.refresh(db_mass_spectrum)
    return db_mass_spectrum

def update_mass_spectrum(
    db: Session, 
    mass_spectrum_id: int, 
    mass_spectrum: MassSpectrumUpdate
) -> Optional[MassSpectrum]:
    db_mass_spectrum = get_mass_spectrum(db, mass_spectrum_id)
    if db_mass_spectrum:
        update_data = mass_spectrum.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_mass_spectrum, key, value)
        db.commit()
        db.refresh(db_mass_spectrum)
    return db_mass_spectrum

def delete_mass_spectrum(db: Session, mass_spectrum_id: int) -> Optional[MassSpectrum]:
    db_mass_spectrum = get_mass_spectrum(db, mass_spectrum_id)
    if db_mass_spectrum:
        db.delete(db_mass_spectrum)
        db.commit()
    return db_mass_spectrum


def delete_all_mass_spectra(db: Session) -> int:
    deleted_count = db.query(MassSpectrum).delete()
    db.commit()
    return deleted_count