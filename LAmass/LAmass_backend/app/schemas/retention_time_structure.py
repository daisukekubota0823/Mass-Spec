from pydantic import BaseModel
from typing import Optional

class RetentionTimeStructureBase(BaseModel):
    metaboliteName: str
    retentionTime: float
    smiles: str

class RetentionTimeStructureCreate(RetentionTimeStructureBase):
    pass

class Config:
    from_attributes = True

class RetentionTimeStructure(RetentionTimeStructureInDBBase):
    pass