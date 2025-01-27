from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class RetentionTimeLibrary(Base):
    __tablename__ = "retention_time_library"

    id = Column(Integer, primary_key=True, index=True)
    compoundName = Column(String)
    inchikey = Column(String)
    retentionTime = Column(Float)
