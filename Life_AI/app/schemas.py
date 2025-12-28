
from pydantic import BaseModel
from typing import List, Dict

class RunConfig(BaseModel):
    objective: str
    seeds: List[str]
    filters: Dict[str, float]
    max_violations: int
    rounds: int = 1
    candidates_per_round: int = 10
