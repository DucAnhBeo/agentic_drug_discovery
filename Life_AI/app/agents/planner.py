
from typing import Dict, Any

class PlannerAgent:
    def __init__(self, config: Dict[str, Any]):
        self.config = config

    def get_plan(self):
        return self.config
