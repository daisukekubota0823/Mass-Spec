from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class RetentionTimeStructure(Base):
    __tablename__ = "retention_time_structures"

    id = Column(Integer, primary_key=True, index=True)
    metaboliteName = Column(String)
    retentionTime = Column(Float)
    smiles = Column(String)