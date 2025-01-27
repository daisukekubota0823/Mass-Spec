from pydantic import BaseModel
from typing import Optional


class CCSLibraryCreate(BaseModel):
    compoundName: str
    inchikey: str
    adduct: str
    ccs: float

class Config:
    from_attributes = True