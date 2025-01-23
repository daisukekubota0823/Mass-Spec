from pydantic import BaseModel
from typing import Optional

class MassSpectrumBase(BaseModel):
    name: Optional[str] = None
    smile: Optional[str] = None
    spectrum_type: str
    ion_mode: str
    precursor_type: Optional[str] = None
    inchikey: Optional[str] = None
    ontology: Optional[str] = None
    collision_energy: Optional[str] = None
    precursor_mz: float
    retention_time: Optional[float] = None
    instrument: Optional[str] = None
    instrument_type: Optional[str] = None
    comment: Optional[str] = None
    sulfur_count: Optional[int] = None
    nitrogen_count: Optional[int] = None
    carbon_count: Optional[int] = None
    peak_number_ms1: Optional[int] = None
    mstype_ms1_row1: Optional[str] = None
    mstype_ms1_row2: Optional[str] = None
    peak_number_ms2: Optional[int] = None
    mstype_ms2_row1: Optional[str] = None
    mstype_ms2_row2: Optional[str] = None

class MassSpectrumCreate(MassSpectrumBase):
    pass

class MassSpectrumUpdate(MassSpectrumBase):
    pass

class MassSpectrumInDBBase(MassSpectrumBase):
    id: int

class Config:
    from_attributes = True  # Instead of orm_mode = True

class MassSpectrum(MassSpectrumInDBBase):
    pass
