from pydantic import BaseModel
from typing import Optional


class RetentionTimeLibraryCreate(BaseModel):
    compoundName: str
    inchikey: str
    retentionTime: float
    
class Config:
    from_attributes = True