from sqlalchemy.orm import Session
from app.models.retention_time_library import RetentionTimeLibrary
from app.schemas.retention_time_library import RetentionTimeLibraryCreate
from typing import List, Optional


def retention_time_library(db: Session, retention_time_library: RetentionTimeLibraryCreate) -> RetentionTimeLibrary:
    db_retention_time_library = RetentionTimeLibrary(**retention_time_library.dict())
    db.add(db_retention_time_library)
    db.commit()
    db.refresh(db_retention_time_library)
    return db_retention_time_library