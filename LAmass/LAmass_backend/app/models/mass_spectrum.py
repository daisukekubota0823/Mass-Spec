from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class MassSpectrum(Base):
    __tablename__ = "mass_spectra"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    smile = Column(String)
    spectrum_type = Column(String)
    ion_mode = Column(String)
    precursor_type = Column(String)
    inchikey = Column(String)
    ontology = Column(String)
    collision_energy = Column(String)
    precursor_mz = Column(Float)
    retention_time = Column(Float)
    instrument = Column(String)
    instrument_type = Column(String)
    comment = Column(String)
    sulfur_count = Column(Integer)
    nitrogen_count = Column(Integer)
    carbon_count = Column(Integer)
    peak_number_ms1 = Column(Integer)
    mstype_ms1_row1 = Column(String)
    mstype_ms1_row2 = Column(String)
    peak_number_ms2 = Column(Integer)
    mstype_ms2_row1 = Column(String)
    mstype_ms2_row2 = Column(String)
