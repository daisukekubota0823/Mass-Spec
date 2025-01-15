from pydantic import BaseModel
from typing import List

class NumbersPayload(BaseModel):
    values: List[float]

class MeanResult(BaseModel):
    status: str
    mean: float