from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class CCSLibrary(Base):
    __tablename__ = "ccs_library"

    id = Column(Integer, primary_key=True, index=True)
    compoundName = Column(String)
    inchikey = Column(String)
    adduct = Column(String)
    ccs = Column(Float)
