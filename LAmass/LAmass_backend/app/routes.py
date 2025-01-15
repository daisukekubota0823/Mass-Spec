from fastapi import APIRouter
from app.r_integration import run_r_script

router = APIRouter()

@router.post("/process-data")
async def process_data(data: dict):
    """
    Endpoint to process data using R.
    """
    try:
        result = run_r_script(data)
        return {"status": "success", "result": result}
    except Exception as e:
        return {"status": "error", "message": str(e)}
