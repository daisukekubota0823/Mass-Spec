from fastapi import APIRouter, HTTPException
from app.schemas import NumbersPayload, MeanResult
import rpy2.robjects as ro

router = APIRouter()
ro.r.source("app/r_functions.R")
compute_mean = ro.globalenv["compute_mean"]

@router.post("/compute-mean", response_model=MeanResult)
def compute_mean_route(payload: NumbersPayload):
    try:
        # Ensure that the payload contains valid float values
        if not all(isinstance(x, (float, int)) for x in payload.values):
            raise HTTPException(status_code=422, detail="All values must be numeric")

        result = compute_mean(ro.FloatVector(payload.values))
        return {"status": "success", "mean": result[0]}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error processing request: {str(e)}")
