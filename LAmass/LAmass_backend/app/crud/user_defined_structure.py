from sqlalchemy.orm import Session
from app.models.user_defined_structure import UserDefinedStructure
from app.schemas.user_defined_structure import UserDefinedStructureCreate
from typing import List, Optional


def create_user_defined_structure(db: Session, user_defined_structure: UserDefinedStructureCreate) -> UserDefinedStructure:
    db_user_defined_structure= UserDefinedStructure(**user_defined_structure.dict())
    db.add(db_user_defined_structure)
    db.commit()
    db.refresh(db_user_defined_structure)
    return db_user_defined_structure