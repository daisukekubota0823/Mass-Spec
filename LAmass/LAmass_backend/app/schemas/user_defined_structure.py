from pydantic import BaseModel
from typing import Optional

class UserDefinedStructureBase(BaseModel):
    title: str
    inchikey: str
    shortInchikey: str
    pubchemCid: Optional[str] = None
    exactMass: float
    formula: str
    smiles: str
    databaseId: Optional[str] = None

class UserDefinedStructureCreate(UserDefinedStructureBase):
    pass

class Config:
    from_attributes = True

class UserDefinedStructure(UserDefinedStructureInDBBase):
    pass