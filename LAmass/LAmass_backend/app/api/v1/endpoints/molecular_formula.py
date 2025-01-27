from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.services.molecular_formula_predictor import predict_molecular_formula
from app.models import UserDefinedStructure, RetentionTimeStructure, RetentionTimeLibrary, CCSLibrary

router = APIRouter()

@router.post("/predict_formula/", response_model=schemas.MolecularFormulaPredictions)
async def predict_formula(mass_spectrum: schemas.MassSpectrumInput, db: Session = Depends(get_db)):
    try:
        custom_dbs = {
            "user_defined": db.query(UserDefinedStructure).all(),
            "retention_time_structure": db.query(RetentionTimeStructure).all(),
            "retention_time_library": db.query(RetentionTimeLibrary).all(),
            "ccs_library": db.query(CCSLibrary).all()
        }
        
        predictions = await predict_molecular_formula(mass_spectrum, custom_dbs, db)
        
        # Convert predictions to Pydantic model
        prediction_models = [schemas.MolecularFormulaPrediction(**pred) for pred in predictions]
        
        return {"predictions": prediction_models}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
