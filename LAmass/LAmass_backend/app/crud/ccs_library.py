from sqlalchemy.orm import Session
from app.models.ccs_library import CCSLibrary
from app.schemas.ccs_library import CCSLibraryCreate
from typing import List, Optional


def create_css_library(db: Session, ccs_library: CCSLibraryCreate) -> CCSLibrary:
    db_ccs_library = CCSLibrary(**ccs_library.dict())
    db.add(db_ccs_library)
    db.commit()
    db.refresh(db_ccs_library)
    return db_ccs_library