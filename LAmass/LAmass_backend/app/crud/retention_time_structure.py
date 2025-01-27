from sqlalchemy.orm import Session
from app.models.retention_time_structure import RetentionTimeStructure
from app.schemas.retention_time_structure import RetentionTimeStructureCreate
from typing import List, Optional


def create_retention_time_structure(db: Session, retention_time_structure: RetentionTimeStructureCreate) -> RetentionTimeStructure:
    db_retention_time_structure= RetentionTimeStructure(**retention_time_structure.dict())
    db.add(db_retention_time_structure)
    db.commit()
    db.refresh(db_retention_time_structure)
    return db_retention_time_structure