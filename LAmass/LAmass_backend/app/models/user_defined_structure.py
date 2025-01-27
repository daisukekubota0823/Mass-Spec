from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class UserDefinedStructure(Base):
    __tablename__ = "user_defined_structures"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    inchikey = Column(String)
    shortInchikey = Column(String)
    pubchemCid = Column(String)
    exactMass = Column(Float)
    formula = Column(String)
    smiles = Column(String)
    databaseId = Column(String)
